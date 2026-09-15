"""One resident policy, official LIBERO episode loop, paired numeric experiments."""
import argparse
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import numpy as np
import torch

SOURCE=Path('/home/nc23/experiments/turbovla_profile/2026-09-12_192541/source')
PRETRAIN=SOURCE.parent/'pretrained'
CKPT=PRETRAIN/'TurboVLA/checkpoints/libero/turbovla_libero.pth'
sys.path[:0]=[str(SOURCE),str(SOURCE/'third_party/vla_adapter')]
from quant_core import QuantMode, force_math

def now(): return datetime.datetime.now().isoformat(timespec='seconds')
def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,default=str))

def load_policy(legacy=False):
    from turbovla.evaluation import policy as pm
    pm._checkpoint_state_dict=lambda c:c.get('ema_model_state_dict',c.get('model_state_dict'))
    from turbovla.evaluation.suite_policy import TurboVLAPolicy
    p=TurboVLAPolicy(ckpt_path=str(CKPT),dinov3_path=str(PRETRAIN/'assets/dinov3_local'),
        bert_path=str(PRETRAIN/'assets/bert_local'),stats_path=str(SOURCE/'experiments/libero/configs/libero_all4_stats.json'),
        stats_key='libero_all4_no_noops',precision='fp32',allow_hf_download=False,verbose=False)
    if not legacy:
        p.model.vision_encoder.config.compute_precision='fp32'
        p.model.float()
        force_math()
    def raw_output_guard(module,inputs,output):
        if not bool(torch.isfinite(output).all()):
            raise RuntimeError('Nonfinite raw policy output before upstream sanitization')
    p.model.register_forward_hook(raw_output_guard)
    return p

def config(name,cal=None):
    if name.endswith('_fixed'):
        m=config(name[:-6],cal);m.fixed=True;return m
    if name in ('fp32','legacy_fp32','legacy_w8a8'): return None
    if name=='observe': return QuantMode(observe=True,calibration=cal)
    if name.startswith('smooth'): return QuantMode(alpha=float(name.split('_')[1]),calibration=cal)
    if name.startswith('group'): return QuantMode(group=int(name.split('_')[1]),clipping=name.endswith('_mse'))
    if name in ('weight_only','activation_only','attention_only'): return QuantMode(diagnostic=name)
    return QuantMode(scheme=name)

def attach(p,mode):
    if mode: mode.install_hooks(p.model)
    original=p.predict_normalized_action_chunk
    calls=[]
    def predict(*args,**kwargs):
        start=time.perf_counter()
        if mode:
            with mode: out=original(*args,**kwargs)
        else: out=original(*args,**kwargs)
        calls.append((copy.deepcopy(args),copy.deepcopy(kwargs),np.array(out),time.perf_counter()-start))
        return out
    p.predict_normalized_action_chunk=predict
    return original,calls

def episodes(args):
    import vla_adapter.rollout as r
    from turbovla.evaluation.suite_policy import set_seed_everywhere,get_libero_dummy_action,rotate_libero_image
    cfg=r.GenerateConfig(libero_root='/home/nc23/workspace/LIBERO',mujoco_gl='egl',pyopengl_platform='egl',
                         precision='fp32',save_video=False)
    r._ensure_libero_import_path(cfg)
    from libero.libero import benchmark
    set_seed_everywhere(7)
    p=load_policy(args.mode.startswith('legacy'))
    if args.mode=='legacy_w8a8':
        sys.path.insert(0,'/home/nc23/experiments/turbovla_quant_2026-09-12_215112/scripts')
        from quantization import apply_fake_quant,finalize_model_dtype
        apply_fake_quant(p.model,'w8a8');finalize_model_dtype(p.model,'w8a8')
    cal=torch.load(args.root/'calibration.pt',weights_only=False) if (args.root/'calibration.pt').exists() else {}
    mode=config(args.mode,cal)
    original,calls=attach(p,mode)
    for suite in args.suites.split(','):
        cfg.task_suite_name=suite
        task_suite=benchmark.get_benchmark_dict()[suite]()
        for task_id in (0,1):
            set_seed_everywhere(7)
            env,description=r._make_libero_env(task_suite.get_task(task_id),cfg)
            states=task_suite.get_task_init_states(task_id)
            try:
                for state_id in range(args.start,args.end):
                    key=f'{args.mode}_{suite}_t{task_id}_s{state_id}'
                    result_path=args.root/'episodes'/(key+'.json')
                    if result_path.exists(): continue
                    # Explicit per-episode seed for new validation; legacy replay
                    # preserves the upstream task-level RNG contract.
                    if not args.mode.startswith('legacy'): set_seed_everywhere(7+state_id)
                    calls.clear(); started=now();t=time.perf_counter()
                    try:
                        ok,frames,actions=r._run_episode(cfg,env,p,description,states[state_id],get_libero_dummy_action,rotate_libero_image)
                        del frames
                        result={'status':'success' if ok else 'task_failure','success':bool(ok),
                                'actions':actions,'planning_calls':len(calls)}
                        if args.capture:
                            ids=np.unique(np.linspace(0,len(calls)-1,min(6,len(calls))).round().astype(int)) if calls else []
                            samples=[{'args':calls[i][0],'kwargs':calls[i][1],'output':calls[i][2],
                                      'planning_index':int(i),'seed':7+state_id} for i in ids]
                            target=args.root/'observations'/(key+'.pt');target.parent.mkdir(exist_ok=True)
                            torch.save(samples,target)
                    except Exception as e:
                        result={'status':'program_error','error':repr(e)}
                        raise
                    finally:
                        result.update(mode=args.mode,suite=suite,task=task_id,initial_state_id=state_id,
                            task_description=description,
                            initial_state_sha256=hashlib.sha256(np.asarray(states[state_id]).tobytes()).hexdigest(),
                            started=started,finished=now(),elapsed_s=time.perf_counter()-t,
                            seed=7 if args.mode.startswith('legacy') else 7+state_id,chunk_size=12)
                        dump(result_path,result)
                        print(json.dumps({k:v for k,v in result.items() if k!='actions'}),flush=True)
                    if mode: dump(args.root/'coverage'/(args.mode+'.json'),{'calls':mode.audit,'operators':mode.records})
            finally: env.close()

def replay(args):
    from turbovla.evaluation.suite_policy import set_seed_everywhere
    p=load_policy()
    files=sorted((args.root/'observations').glob('fp32_*.pt'))
    if not files: raise RuntimeError('No development observations')
    samples=[s for f in files for s in torch.load(f,weights_only=False)]
    if args.limit: samples=samples[:args.limit]
    cal={}
    modes=args.modes.split(',')
    if (args.root/'calibration.pt').exists(): cal=torch.load(args.root/'calibration.pt',weights_only=False)
    for name in modes:
        m=config(name,cal)
        if m:m.install_hooks(p.model)
        errors=[];started=now();t=time.perf_counter()
        try:
            for idx,s in enumerate(samples):
                set_seed_everywhere(s['seed'])
                if m:
                    with m: out=p.predict_normalized_action_chunk(*s['args'],**s['kwargs'])
                else:out=p.predict_normalized_action_chunk(*s['args'],**s['kwargs'])
                diff=np.asarray(out)-s['output']
                errors.append({'sample':idx,'mae':float(np.abs(diff).mean()),'max':float(np.abs(diff).max()),
                    'arm_mae':float(np.abs(diff[:,:6]).mean()),'gripper_mae':float(np.abs(diff[:,6]).mean())})
                if idx%6==0: print(name,idx,len(samples),errors[-1],flush=True)
        finally:
            if m:m.remove_hooks()
        if name=='observe':torch.save({k:v.cpu() for k,v in cal.items()},args.root/'calibration.pt')
        if m and not m.observe and m.diagnostic=='all':
            if m.audit['linear']<280*len(samples) or m.audit['conv2d']!=2*len(samples):
                raise RuntimeError('Incomplete full model arithmetic coverage: '+str(m.audit))
            target=args.root/'integer_fixtures';target.mkdir(exist_ok=True)
            torch.save(m.fixtures,target/(name+'.pt'))
        dump(args.root/'replay'/(name+'.json'),{'mode':name,'n':len(samples),'started':started,'finished':now(),
             'elapsed_s':time.perf_counter()-t,'mae':float(np.mean([x['mae'] for x in errors])),
             'max':max(x['max'] for x in errors),'samples':errors,'calls':m.audit if m else {},
             'operators':m.records if m else {},'operator_types':m.operator_types if m else {}})

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--stage',choices=['episodes','replay'],default='episodes')
    ap.add_argument('--mode',default='fp32');ap.add_argument('--modes',default='fp32,observe,tensor,token,smooth_0.25,smooth_0.5,smooth_0.75,group_128,group_64,group_32')
    ap.add_argument('--suites',default='libero_spatial,libero_object,libero_goal,libero_10')
    ap.add_argument('--start',type=int,default=0);ap.add_argument('--end',type=int,default=3)
    ap.add_argument('--capture',action='store_true');ap.add_argument('--limit',type=int,default=0)
    args=ap.parse_args();args.root.mkdir(parents=True,exist_ok=True)
    launch={'started':now(),'arguments':vars(args),'torch':torch.__version__,
            'visible_gpu':os.environ.get('CUDA_VISIBLE_DEVICES'),
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                (Path(__file__),Path(__file__).with_name('quant_core.py'))}}
    dump(args.root/'launches'/(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')+'.json'),launch)
    if args.stage=='episodes':episodes(args)
    else:replay(args)
