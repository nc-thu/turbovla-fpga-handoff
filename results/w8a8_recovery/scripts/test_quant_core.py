import json
import torch
import torch.nn.functional as F
from quant_core import QuantMode,force_math

torch.manual_seed(17)
force_math()
checks={}
for k in (1,32,64,127,128,257,768,3072,4096):
    a=torch.randint(-127,128,(3,k),dtype=torch.int64)
    b=torch.randint(-127,128,(k,5),dtype=torch.int64)
    exact=a@b
    observed=a.float()@b.float()
    checks['random_int_'+str(k)]=bool(torch.equal(observed.double(),exact.double()))
    # Grouped integer sums are exact in FP32 for group <=128.
    a.fill_(127);b.fill_(127)
    for g in (32,64,128):
        checks[f'extreme_partial_{k}_{g}']=all(torch.equal(
            (a[:,i:i+g].float()@b[i:i+g].float()).double(),
            (a[:,i:i+g]@b[i:i+g]).double()) for i in range(0,k,g))
q=torch.randn(1,2,5,8);k=torch.randn(1,2,7,8);v=torch.randn(1,2,7,8)
m=QuantMode();m.linear_paths=set()
with m: out=F.scaled_dot_product_attention(q,k,v)
checks['sdpa_two_products']=m.audit['bmm']==2
checks['finite_sdpa']=bool(out.isfinite().all())
model=torch.nn.Sequential(torch.nn.Linear(17,23),torch.nn.GELU(),torch.nn.Linear(23,5)).eval()
x=torch.randn(2,17)
ref=model(x)
m=QuantMode(observe=True);m.install_hooks(model)
with m: obs=model(x)
m.remove_hooks()
checks['observer_equal']=bool(torch.equal(ref,obs))
m=QuantMode(group=32);m.install_hooks(model)
with m: out=model(x)
m.remove_hooks()
checks['linear_covered']=sum(m.audit.values())==2
for g in (32,64,128):
    a=torch.randn(2,3,137);b=torch.randn(2,137,5)
    m=QuantMode(group=g);m.path='test'
    actual=m.product(a,b)
    expected=torch.zeros(2,3,5)
    for lo in range(0,137,g):
        qa,sa=m.grid(a[...,lo:lo+g]);qb,sb=m.grid(b[...,lo:lo+g,:].transpose(-1,-2))
        expected+=(qa@qb.transpose(-1,-2))*(sa*sb.transpose(-1,-2))
    checks[f'group_layout_{g}']=bool(torch.allclose(actual,expected,atol=1e-5,rtol=1e-5))
conv=torch.nn.Conv2d(3,4,3,stride=2,padding=1).eval();xx=torch.randn(1,3,9,9)
m=QuantMode(observe=True);m.install_hooks(conv)
with m: yy=conv(xx)
m.remove_hooks()
checks['conv_observer_close']=bool(torch.allclose(yy,conv(xx),atol=1e-6,rtol=1e-5))
for kind in ('none','boolean','additive','causal','scale'):
    q=torch.randn(1,2,5,8);key=torch.randn(1,2,7,8);v=torch.randn(1,2,7,6)
    mask=None;causal=kind=='causal';scale=.25 if kind=='scale' else 8**-.5
    if kind=='boolean':mask=torch.rand(5,7)>.3;mask[:,0]=True
    if kind=='additive':mask=torch.randn(5,7)*.2
    m=QuantMode(group=32)
    got=m.__torch_dispatch__(torch.ops.aten.scaled_dot_product_attention.default,(),
        (q,key,v,mask,0.,causal),{'scale':scale})
    refmode=QuantMode(group=32)
    logits=refmode.product(q,key.transpose(-1,-2))*scale
    if causal:logits=logits.masked_fill(~torch.ones(5,7,dtype=torch.bool).tril(),float('-inf'))
    if mask is not None:logits=logits.masked_fill(~mask,float('-inf')) if mask.dtype==torch.bool else logits+mask
    ref=refmode.product(logits.softmax(-1),v)
    checks['explicit_sdpa_'+kind]=bool(torch.equal(got,ref))
    checks['explicit_sdpa_both_'+kind]=m.audit['attention_qk']==1 and m.audit['attention_av']==1
fixed=QuantMode(group=32);fixed.fixed=True
checks['fixed_zero']=bool(torch.equal(fixed.product(torch.zeros(2,65),torch.randn(65,3)),torch.zeros(2,3)))
print(json.dumps({'checks':checks,'pass':all(checks.values())},indent=2))
assert all(checks.values())
