"""User-authorized shared-GPU rough measurement. Does not measure closed-loop success."""
from pathlib import Path
import os,sys,time,json,hashlib,threading,subprocess,statistics,datetime
HB=Path('/home/nc23/workspace/holobrain');sys.path[:0]=[str(HB),str(HB/'quant'),str(HB/'shims'),str(HB/'robo_orchard_lab'),'/tmp/alg_refq']
os.chdir(HB)
import torch,numpy as np
import refq_lib as R
OUT=Path(__file__).resolve().parent;device=int(os.environ.get('PHYSICAL_GPU','1'))
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def occupants():
 return subprocess.check_output(['nvidia-smi','--query-compute-apps=gpu_uuid,pid,used_memory','--format=csv,noheader'],text=True)
start_time=datetime.datetime.now().isoformat();before=occupants();torch.set_num_threads(2);torch.backends.cuda.matmul.allow_tf32=False
_,model,_=R.load_env();model=model.cuda().float().eval();batch=R.get_batch('s000')
assert model.decoder.num_inference_timesteps==10
print('MODEL_READY',flush=True)
with torch.no_grad():
 for _ in range(3):torch.manual_seed(R.SEED_DEPLOY);model(batch);torch.cuda.synchronize()
samples=[]
proc=subprocess.Popen(['nvidia-smi','-i',str(device),'--query-gpu=power.draw,utilization.gpu,memory.used','--format=csv,noheader,nounits','-lms','50'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
def read():
 for line in proc.stdout:
  try:samples.append([time.perf_counter()]+[float(v.strip()) for v in line.split(',')])
  except ValueError:pass
th=threading.Thread(target=read,daemon=True);th.start();time.sleep(.2);intervals=[];output=None
with torch.no_grad():
 for i in range(12):
  torch.manual_seed(R.SEED_DEPLOY);torch.cuda.synchronize();t=time.perf_counter();output=model(batch);torch.cuda.synchronize();end=time.perf_counter();intervals.append([t,end]);print('CALL',i,end-t,flush=True)
time.sleep(.15);proc.terminate();th.join(timeout=3)
arr=np.asarray(samples);rows=[]
for s,e in intervals:
 ts=np.r_[s,arr[(arr[:,0]>s)&(arr[:,0]<e),0],e];powers=np.interp(ts,arr[:,0],arr[:,1]);rows.append({'latency_s':e-s,'shared_gpu_total_energy_j':float(np.trapz(powers,ts))})
trace=json.load(open('/tmp/ae_hostdrv/trace_s000.json'))['meta'];bundle=HB/'ckpt/HoloBrain_v0.0_GD/post_training_robotwin'
result={'started_at':start_time,'finished_at':datetime.datetime.now().isoformat(),'gpu':torch.cuda.get_device_name(0),'physical_index':device,'torch':torch.__version__,'precision':'FP32, TF32 disabled; no fake quantization','denoising_steps':10,'output_shape':list(output[0]['pred_actions'].shape),'input_description':trace['input'],'input_path':'/tmp/ae_hostdrv/batch_s000.pt','input_sha256':sha('/tmp/ae_hostdrv/batch_s000.pt'),'checkpoint_sha256':sha(bundle/'model.safetensors'),'model_config_sha256':sha(bundle/'model.config.json'),'configuration':json.loads((bundle/'model.config.json').read_text()),'timed_scope':'model(batch), includes internal data_preprocessor and complete denoising; excludes external processor/token scene conversion and action post_process','environment':'shared GPU rough measurement, explicitly authorized by user; resident foreign processes retained','power_scope':'total GPU board sensor including other processes; not model-attributable energy or full host platform','occupants_before':before,'occupants_after':occupants(),'samples':samples,'calls':rows,'mean_latency_s':statistics.mean(r['latency_s'] for r in rows),'median_latency_s':statistics.median(r['latency_s'] for r in rows),'min_latency_s':min(r['latency_s'] for r in rows),'max_latency_s':max(r['latency_s'] for r in rows),'mean_shared_gpu_power_w':float(arr[:,1].mean()),'mean_shared_gpu_energy_j':statistics.mean(r['shared_gpu_total_energy_j'] for r in rows),'seed':R.SEED_DEPLOY}
(OUT/'gpu_rough.json').write_text(json.dumps(result,indent=2));print('DONE',result['mean_latency_s'],result['mean_shared_gpu_power_w'],flush=True)
