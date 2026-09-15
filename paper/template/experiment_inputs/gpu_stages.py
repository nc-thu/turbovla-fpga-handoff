from pathlib import Path
import os,sys,json,time,statistics
HB=Path('/home/nc23/workspace/holobrain');sys.path[:0]=[str(HB),str(HB/'quant'),str(HB/'shims'),str(HB/'robo_orchard_lab'),'/tmp/alg_refq'];os.chdir(HB)
import torch
import refq_lib as R
torch.set_num_threads(2);torch.backends.cuda.matmul.allow_tf32=False
_,model,_=R.load_env();model=model.cuda().float().eval();batch=R.get_batch('s000')
with torch.no_grad():model(batch);torch.cuda.synchronize()
starts={};elapsed={};handles=[]
def pre(name):
 def h(*args):torch.cuda.synchronize();starts[name]=time.perf_counter()
 return h
def post(name):
 def h(*args):torch.cuda.synchronize();elapsed[name]=elapsed.get(name,0)+time.perf_counter()-starts[name]
 return h
for name,child in model.named_children():
 handles.extend([child.register_forward_pre_hook(pre(name)),child.register_forward_hook(post(name))])
rows=[]
with torch.no_grad():
 for i in range(3):
  elapsed.clear();torch.manual_seed(R.SEED_DEPLOY);torch.cuda.synchronize();t=time.perf_counter();model(batch);torch.cuda.synchronize();rows.append({'model_forward_s':time.perf_counter()-t,'top_level_modules_s':dict(elapsed)});print(rows[-1],flush=True)
for h in handles:h.remove()
groups={'visual':['backbone','backbone_3d','neck','neck_3d'],'language_interaction':['text_encoder','feature_enhancer','spatial_enhancer'],'action':['decoder'],'internal_preprocess':['data_preprocessor']}
result={'scope':'s000 HoloBrain-0 FP32 shared V100 GPU1; top-level module wall times with CUDA synchronization at boundaries; separate instrumented run, not the primary latency samples','rows':rows,'stage_mean_s':{k:statistics.mean(sum(r['top_level_modules_s'].get(n,0) for n in names) for r in rows) for k,names in groups.items()},'groups':groups}
Path(__file__).with_name('gpu_stages.json').write_text(json.dumps(result,indent=2))
