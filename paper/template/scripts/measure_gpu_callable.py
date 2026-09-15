"""Measure a project adapter's callable with exclusive GPU-device power.
Example: python measure_gpu_callable.py --factory hb_measure_adapter:make_call --out gpu.json
The adapter must load the fixed checkpoint/observation before returning (callable, metadata).
This measures GPU-device energy, not total platform energy.
"""
import argparse,importlib,time,json,threading,os
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--factory',required=True);p.add_argument('--out',required=True);p.add_argument('--warmup',type=int,default=5);p.add_argument('--repeat',type=int,default=20);p.add_argument('--nvml-index',type=int,default=0);a=p.parse_args()
 import torch,pynvml,numpy as np
 pynvml.nvmlInit();h=pynvml.nvmlDeviceGetHandleByIndex(a.nvml_index)
 def exclusive():
  foreign=[v.pid for v in pynvml.nvmlDeviceGetComputeRunningProcesses(h) if v.pid!=os.getpid()]
  if foreign:raise RuntimeError('GPU has other processes; do not report their power as model power')
 exclusive();module,func=a.factory.split(':');call,metadata=getattr(importlib.import_module(module),func)()
 for key in ['checkpoint_sha256','input_sha256','model_config_sha256','denoising_steps','action_chunk','precision','timed_scope']:
  if key not in metadata or metadata[key] is None:raise ValueError('Adapter must provide '+key)
 exclusive()
 with torch.inference_mode():
  for _ in range(a.warmup):call();torch.cuda.synchronize()
  samples=[];stop=threading.Event()
  def monitor():
   while not stop.is_set():samples.append([time.perf_counter(),pynvml.nvmlDeviceGetPowerUsage(h)/1000]);stop.wait(.05)
  th=threading.Thread(target=monitor);th.start();time.sleep(.06);intervals=[]
  try:
   for _ in range(a.repeat):
    exclusive();torch.cuda.synchronize();start=time.perf_counter();call();torch.cuda.synchronize();end=time.perf_counter();intervals.append([start,end])
   time.sleep(.06)
  finally:stop.set();th.join()
 times=np.array(samples)[:,0];watts=np.array(samples)[:,1];rows=[]
 for start,end in intervals:
  ts=np.r_[start,times[(times>start)&(times<end)],end];pw=np.interp(ts,times,watts);energy=float(np.trapz(pw,ts));rows.append({'latency_s':end-start,'gpu_device_energy_j':energy})
 result={'metadata':metadata,'gpu_uuid':pynvml.nvmlDeviceGetUUID(h),'power_scope':'GPU device only; host excluded','samples':samples,'calls':rows,'calls_per_s':len(rows)/sum(x['latency_s'] for x in rows),'calls_per_joule':len(rows)/sum(x['gpu_device_energy_j'] for x in rows),'note':'Sampled NVML power. Inspect sensor resolution, timestamp coverage and idle baseline separately.'}
 Path(a.out).write_text(json.dumps(result,indent=2));print(a.out)
if __name__=='__main__':main()
