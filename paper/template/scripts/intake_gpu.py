from pathlib import Path
import json,numpy as np,hashlib,datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parents[1];D=P/'data';g=json.loads((D/'gpu_rough.json').read_text());s=json.loads((D/'gpu_stages.json').read_text());a=json.loads((D/'arch.json').read_text())
assert hashlib.sha256((D/'model.config.json').read_bytes()).hexdigest()==g['model_config_sha256']
groups={'Visual':['backbone','neck','backbone_3d','neck_3d'],'Language / interaction':['text_encoder','text_feat_map','feature_enhancer','spatial_enhancer'],'Action':['decoder']}
stages={k:np.mean([sum(r['top_level_modules_s'].get(n,0) for n in names) for r in s['rows']])*1000 for k,names in groups.items()}
stages['Other / preprocess']=np.mean([r['model_forward_s'] for r in s['rows']])*1000-sum(stages.values())
plt.rcParams.update({'font.family':'Arial','font.size':8,'pdf.fonttype':42,'svg.fonttype':'none'});C=['#d3d3d3','#c8b38e','#2c8199','#d76a00']
fig,axs=plt.subplots(3,1,figsize=(7.15,4.65))
ax=axs[0];mean=g['mean_latency_s']*1000;ax.bar([0],[mean],color=C[0],edgecolor='black',width=.45);ax.errorbar([0],[mean],yerr=[[mean-g['min_latency_s']*1000],[g['max_latency_s']*1000-mean]],fmt='none',ecolor='black',capsize=4);ax.set_xticks([0,1,2],['V100 shared, FP32','FPGA baseline','FPGA optimized']);ax.set_xlim(-.5,2.5);ax.set_ylim(0,520);ax.set_ylabel('Model forward (ms)');ax.text(0,450,f'{mean:.1f} ms; {1/g["mean_latency_s"]:.2f} forwards/s',ha='center',fontsize=7)
for x in [1,2]:ax.text(x,180,'Matched full-forward\nmeasurement pending',ha='center',fontsize=7,color='#555555')
ax.set_title('(a) Exploratory GPU forward latency: s000, 12 calls; not full policy latency')
ax=axs[1];vs=list(stages.values());ax.bar(range(4),vs,color=C,edgecolor='black',width=.55);ax.set_xticks(range(4),list(stages));ax.set_ylabel('Stage duration (ms)');ax.set_ylim(0,390);ax.set_title('(b) Separate GPU stage profile: 3 instrumented forwards, synchronized boundaries')
for i,v in enumerate(vs):ax.text(i,v+8,f'{v:.1f}',ha='center',fontsize=8)
ax=axs[2];vs=[r['G'] for r in a['ladder'][:4]];bars=ax.bar(range(4),vs,color=C,edgecolor='black',width=.55);bars[-1].set_hatch('///');ax.set_xticks(range(4),['Serial','+ overlap','+ dual readout','+ 2× core*']);ax.set_ylabel('GEMM cycles (million)');ax.set_ylim(0,230);ax.set_title('(c) Archived FPGA schedule prediction: GEMM only; scope differs from (a)')
for i,v in enumerate(vs):ax.text(i,v+5,f'{v:.1f}',ha='center',fontsize=8)
for ax in axs:ax.grid(axis='y',alpha=.15)
fig.tight_layout(h_pad=1.4)
for ext in ['pdf','svg','png']:fig.savefig(P/f'figures/core4_performance.{ext}',bbox_inches='tight',dpi=240)
samples=np.asarray(g['samples']);fig,ax=plt.subplots(figsize=(7.15,1.85));ax.plot(samples[:,0]-samples[0,0],samples[:,1],color=C[2]);ax.set_xlabel('Elapsed sampling time (s)');ax.set_ylabel('Shared GPU power (W)');ax.grid(alpha=.2);ax.set_title('Exploratory board telemetry: includes resident foreign processes')
fig.tight_layout()
for ext in ['pdf','png','svg']:fig.savefig(P/f'figures/gpu_shared_power.{ext}',bbox_inches='tight',dpi=220)
rec=json.loads((D/'figure_records.json').read_text());r={k:None for k in rec['records'][0]};r.update(model='HoloBrain-0',model_sha256=g['model_config_sha256'],checkpoint_sha256=g['checkpoint_sha256'],input_sha256=g['input_sha256'],workload='s000: episode_0000000.hdf5 t=40',configuration='FP32 shared V100 GPU1, MHA slow path',latency_s=g['mean_latency_s'],power_w=g['mean_shared_gpu_power_w'],power_scope=g['power_scope'],power_source='nvidia-smi board sensor, shared GPU',evidence='exploratory measured model forward; not complete policy call',raw_file='data/gpu_rough.json',source_sha256=hashlib.sha256((D/'gpu_rough.json').read_bytes()).hexdigest());rec['records'].append(r)
(D/'figure_records.json').write_text(json.dumps(rec,indent=2),encoding='utf8')
(D/'gpu_derived.json').write_text(json.dumps({'generated_at':datetime.datetime.now().isoformat(timespec='seconds'),'mean_forward_ms':mean,'forwards_per_second':1/g['mean_latency_s'],'stage_ms':stages,'action_stage_fraction':stages['Action']/sum(stages.values()),'shared_board_power_mean_w':g['mean_shared_gpu_power_w'],'energy_per_policy_call_j':None,'calls_per_joule':None,'quality_success_rate':None},indent=2),encoding='utf8')
print('GPU rough intake:',mean,'ms;',stages)
