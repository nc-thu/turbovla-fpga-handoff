"""Explicit INT8 operand grids; floating kernels simulate integer products.

All aten mm/addmm/bmm and conv2d are intercepted. SDPA math decomposition and
disabled MHA fastpath expose attention products. Unsupported fused ops fail.
"""
import collections
import math
import torch
import torch.nn.functional as F
from torch.utils._python_dispatch import TorchDispatchMode


class QuantMode(TorchDispatchMode):
    def __init__(self, scheme='token', group=0, alpha=0., calibration=None,
                 observe=False, clipping=False, diagnostic='all'):
        super().__init__()
        self.scheme, self.group, self.alpha = scheme, group, alpha
        self.calibration = calibration if calibration is not None else {}
        self.observe, self.clipping, self.diagnostic = observe, clipping, diagnostic
        self.path = '<root>'
        self.audit = collections.Counter()
        self.records = {}
        self.operator_types = collections.Counter()
        self.fixtures={}
        self.weight_cache={}
        self.fixed=False

    def grid(self, x, tensor=False):
        x = x.float()
        maximum = x.abs().amax() if tensor else x.abs().amax(-1, keepdim=True)
        s = maximum.clamp_min(1e-12) / 127.
        if self.clipping:
            best, err = s, torch.full_like(s, float('inf'))
            for factor in (1., .995, .99, .98, .95, .90):
                trial = s * factor
                loss = (x - (x / trial).round().clamp(-127, 127) * trial).square().mean(-1, keepdim=True)
                choose = loss < err
                best, err = torch.where(choose, trial, best), torch.minimum(err, loss)
            s = best
        q = (x / s).round().clamp(-127, 127)
        return q, s

    def product(self, a, b, weight=False, name='mm'):
        a, b = a.float(), b.float()
        weight_key=(b.untyped_storage().data_ptr(),b.storage_offset(),tuple(b.shape),tuple(b.stride())) if weight else None
        key = self.path + '|' + name + '|' + str(tuple(a.shape)) + '|' + str(tuple(b.shape))
        if self.observe:
            if weight:
                peak = a.abs().reshape(-1, a.shape[-1]).amax(0).detach()
                prior = self.calibration.get(self.path)
                self.calibration[self.path] = peak if prior is None else torch.maximum(prior, peak)
            self.audit[name] += 1
            return a @ b
        if self.alpha and weight and self.path in self.calibration:
            peak = self.calibration[self.path].to(a.device)
            wpeak = b.abs().amax(-1).clamp_min(1e-8)
            smooth = (peak.clamp_min(1e-8).pow(self.alpha) / wpeak.pow(1-self.alpha)).clamp(1e-4,1e4)
            a, b = a / smooth, b * smooth[:,None]
        k = a.shape[-1]
        group = self.group or k
        total = None
        scale_count = partial_count = 0
        quantize_a = self.diagnostic != 'weight_only'
        quantize_b = self.diagnostic != 'activation_only' or not weight
        if self.diagnostic == 'attention_only' and weight:
            return a @ b
        if self.diagnostic == 'weight_only' and not weight:
            return a @ b
        if self.group:
            ng=math.ceil(k/group)
            # Group is a batch dimension, never merged into K before rescaling.
            aa=F.pad(a,(0,ng*group-k)).reshape(*a.shape[:-1],ng,group).transpose(-3,-2)
            bt=b.transpose(-1,-2)
            bb=F.pad(bt,(0,ng*group-k)).reshape(*bt.shape[:-1],ng,group).transpose(-3,-2)
            qa,sa=self.grid(aa)
            if weight_key in self.weight_cache: qb,sb=self.weight_cache[weight_key]
            else:
                qb,sb=self.grid(bb)
                if weight_key is not None:self.weight_cache[weight_key]=(qb,sb)
            partial=qa @ qb.transpose(-1,-2)
            total=(partial*(sa*sb.transpose(-1,-2))).sum(-3)
            scale_count=sa.numel()+sb.numel()
            partial_count=partial.numel()
            merge_parts=partial
            merge_scales=sa*sb.transpose(-1,-2)
        for lo in ([] if self.group else range(0,k,group)):
            aa, bb = a[...,lo:lo+group], b[...,lo:lo+group,:].transpose(-1,-2)
            qa, sa = self.grid(aa, self.scheme == 'tensor') if quantize_a else (aa, torch.ones((),device=a.device))
            if weight_key in self.weight_cache and quantize_b:qb,sb=self.weight_cache[weight_key]
            else:
                qb, sb = self.grid(bb) if quantize_b else (bb, torch.ones((),device=a.device))
                if weight_key is not None and quantize_b:self.weight_cache[weight_key]=(qb,sb)
            # Integer-valued products accumulated by FP32; oracle tests quantify
            # representability. No unquantized dot product in production modes.
            p = qa @ qb.transpose(-1,-2)
            scale = sa * (sb.transpose(-1,-2) if sb.ndim >= 2 else sb)
            merge_parts=p.unsqueeze(-3)
            merge_scales=scale.unsqueeze(-3) if scale.ndim>=2 else scale
            p = p * scale
            total = p if total is None else total + p
            scale_count += sa.numel() + sb.numel()
            partial_count += p.numel()
        if self.fixed:
            # Explicit dynamic output scale. This extra reduction is a hardware
            # requirement, not assumed free or fused with the current array.
            oscale=total.abs().amax(-1,keepdim=True).clamp_min(1e-12)/127.
            ratios=merge_scales/oscale.unsqueeze(-3)
            bound=float((merge_parts.abs().double()*ratios.abs().double()).sum(-3).amax())
            shift=min(30,max(0,math.floor(math.log2((2**60)/max(bound,1.)))))
            mult=(ratios.double()*(2**shift)).round().to(torch.int64)
            merged=(merge_parts.round().to(torch.int64)*mult).sum(-3)
            mag=merged.abs();div=2**shift;rounded=mag//div
            if shift:
                rem=mag%div
                rounded=rounded+((rem>div//2)|((rem==div//2)&((rounded&1)==1))).to(torch.int64)
            total=(rounded*merged.sign()).clamp(-127,127).float()*oscale
        self.audit[name] += 1
        sample_stats=self.records.get(key,{}).get('first_call_stats')
        if sample_stats is None:
            reference=a@b
            diff=total-reference
            sample_stats={'a_zero_fraction':float((qa==0).float().mean()),
                         'a_endpoint_fraction':float((qa.abs()==127).float().mean()),
                         'b_zero_fraction':float((qb==0).float().mean()),
                         'b_endpoint_fraction':float((qb.abs()==127).float().mean()),
                         'a_clipped_fraction':float((aa.abs()>127*sa).float().mean()),
                         'b_clipped_fraction':float((bb.abs()>127*sb).float().mean()),
                         'output_mae':float(diff.abs().mean()),'output_max':float(diff.abs().max()),
                         'output_nrmse':float(diff.square().mean().sqrt()/reference.square().mean().sqrt().clamp_min(1e-12)),
                         'scope':'first call for module/op/shape, includes zero padding'}
        if name not in self.fixtures:
            self.fixtures[name]={'a':a.reshape(-1,a.shape[-2],k)[0,:3].detach().cpu(),
                'b':b.reshape(-1,k,b.shape[-1])[0,:,:3].detach().cpu(),
                'group':self.group,'scheme':self.scheme,'clipping':self.clipping,'module':self.path}
        count=self.records.get(key,{}).get('calls',0)+1
        self.records[key] = {'first_call_stats':sample_stats,'calls':count,'op':name,'module':self.path,'a_shape':list(a.shape),
            'b_shape':list(b.shape),'a_bits':8,'b_bits':8,'group_k':group,
            'scale_values_per_call':scale_count,'partial_values_per_call':partial_count,
            'macs': math.prod(total.shape)*k,'weight':weight}
        return total

    def __torch_dispatch__(self, func, types, args=(), kwargs=None):
        kwargs = kwargs or {}
        name = func._schema.name.split('::')[-1]
        self.operator_types[name]+=1
        if self.observe:
            if name in ('mm','addmm','linear'):
                a,b=(args[:2] if name=='linear' else args[-2:])
                peak=a.float().abs().reshape(-1,a.shape[-1]).amax(0).detach()
                prior=self.calibration.get(self.path)
                if prior is None or prior.shape==peak.shape:
                    self.calibration[self.path]=peak if prior is None else torch.maximum(prior.to(peak.device),peak)
            self.audit[name]+=1
            return func(*args,**kwargs)
        if name=='linear':
            a,w=args[:2]
            bias=args[2] if len(args)>2 else kwargs.get('bias')
            out=self.product(a,w.transpose(-1,-2),True,'linear')
            return out if bias is None else out+bias
        if name=='matmul':
            a,b=args[:2]
            if a.ndim<2 or b.ndim<2:raise RuntimeError('Vector matmul requires explicit lowering')
            return self.product(a,b,b.untyped_storage().data_ptr() in getattr(self,'weight_storage',set()),'matmul')
        if name in ('mm','bmm','addmm','baddbmm'):
            if name in ('addmm','baddbmm'):
                bias,a,b=args[:3]
                out=self.product(a,b,weight=name=='addmm',name=name)
                beta=kwargs.get('beta',1)
                return out*kwargs.get('alpha',1)+(bias*beta if beta else 0)
            a,b=args[:2]
            # Parameters/views do not require grads in inference; module context
            # and matrix rank determine static projections vs dynamic products.
            static=name=='mm' and (self.path in self.linear_paths or b.untyped_storage().data_ptr() in getattr(self,'weight_storage',set()))
            return self.product(a,b,weight=static,name=name)
        if name in ('convolution','conv2d'):
            if name=='convolution': x,w,bias,stride,pad,dil,transposed,outpad,groups=args[:9]
            else:
                x,w=args[:2]
                bias=args[2] if len(args)>2 else kwargs.get('bias')
                stride=args[3] if len(args)>3 else kwargs.get('stride',[1,1])
                pad=args[4] if len(args)>4 else kwargs.get('padding',[0,0])
                dil=args[5] if len(args)>5 else kwargs.get('dilation',[1,1])
                groups=args[6] if len(args)>6 else kwargs.get('groups',1)
                transposed=False
            if x.ndim!=4 or transposed or groups!=1:
                raise RuntimeError('Unsupported convolution: '+str((x.shape,groups,transposed)))
            patches=F.unfold(x.float(),w.shape[-2:],dilation=dil,padding=pad,stride=stride).transpose(1,2)
            out=self.product(patches,w.float().flatten(1).T,True,'conv2d')
            if bias is not None: out=out+bias
            h=(x.shape[-2]+2*pad[0]-dil[0]*(w.shape[-2]-1)-1)//stride[0]+1
            return out.transpose(1,2).reshape(x.shape[0],w.shape[0],h,-1)
        if name=='scaled_dot_product_attention':
            q,k,v=args[:3]
            mask=args[3] if len(args)>3 else kwargs.get('attn_mask')
            dropout=args[4] if len(args)>4 else kwargs.get('dropout_p',0.)
            causal=args[5] if len(args)>5 else kwargs.get('is_causal',False)
            if dropout:raise RuntimeError('Nonzero attention dropout in evaluation')
            if kwargs.get('enable_gqa',False):
                repeat=q.shape[-3]//k.shape[-3]
                k=k.repeat_interleave(repeat,-3);v=v.repeat_interleave(repeat,-3)
            scale=kwargs.get('scale')
            if scale is None:scale=q.shape[-1]**-.5
            logits=self.product(q,k.transpose(-1,-2),False,'attention_qk')*scale
            if causal:
                keep=torch.ones(q.shape[-2],k.shape[-2],device=q.device,dtype=torch.bool).tril()
                logits=logits.masked_fill(~keep,float('-inf'))
            if mask is not None:
                logits=logits.masked_fill(~mask,float('-inf')) if mask.dtype==torch.bool else logits+mask
            probabilities=torch.softmax(logits,-1).nan_to_num(nan=0.)
            return self.product(probabilities,v,False,'attention_av')
        if 'scaled_dot_product' in name or name == '_native_multi_head_attention':
            raise RuntimeError('Fused attention escaped decomposition: '+name)
        if any(token in name for token in ('linear','matmul','addmm','bmm','convol')):
            raise RuntimeError('Uncovered arithmetic operator: '+name)
        return func(*args, **kwargs)

    def install_hooks(self, model):
        self.linear_paths={n for n,m in model.named_modules() if isinstance(m,torch.nn.Linear)}
        self.weight_storage={p.untyped_storage().data_ptr() for p in model.parameters() if p.ndim>=2}
        self.handles=[]
        self.stack=[]
        for path,m in model.named_modules():
            def pre(mod, args, path=path):
                self.stack.append(self.path); self.path=path
            def post(mod,args,out):
                self.path=self.stack.pop()
            self.handles += [m.register_forward_pre_hook(pre),m.register_forward_hook(post)]

    def remove_hooks(self):
        for h in self.handles: h.remove()


def force_math():
    torch.backends.mha.set_fastpath_enabled(False)
    torch.backends.cuda.enable_flash_sdp(False)
    torch.backends.cuda.enable_mem_efficient_sdp(False)
    torch.backends.cuda.enable_math_sdp(True)
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False
