from pathlib import Path
import shutil,hashlib,json,datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parents[1]; R=P.parents[1];O=P/'data/route_intake';O.mkdir(exist_ok=True)
src=Path('E:/ae_syn/hb_h10/runs/base_pa48/synth')
manifest=[]
for name in ['power_route.rpt','timing_summary_route.rpt','util_route.rpt','wns_route.txt']:
 dest=O/('v10_base_pa48_'+name)
 if not dest.exists():shutil.copy2(src/name,dest)
 manifest.append({'source':str(src/name),'snapshot':str(dest.relative_to(P)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
old=R/'hw/v5_2026-09-08_2000_h2_r2_b64_pwr/results/eng48/route/power.rpt';dest=O/'v5_power.rpt'
if not dest.exists():shutil.copy2(old,dest)
manifest.append({'source':str(old),'snapshot':str(dest.relative_to(P)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
(O/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
meta={'received_at':datetime.datetime.now().isoformat(timespec='seconds'),'scope':'top_eng48 OOC engine; vectorless routed estimate','device':'xczu7ev-ffvc1156-2-e','period_ns':3.298,'temperature_ambient_C':25,'old':{'version':'v5','lut':118356,'power_w':8.321},'new':{'version':'v10_base_pa48','lut':104066,'ff':169969,'dsp':768,'bram':0,'power_w':7.043,'dynamic_w':6.414,'static_w':.629,'wns_ns':.034,'whs_ns':.014,'timing_closed':True},'lut_reduction_pct':(1-104066/118356)*100,'power_reduction_pct':(1-7.043/8.321)*100,'energy_per_call_j':None,'notes':'Historical-to-current comparison, not simultaneous rerun. Same nominal clock and ambient conditions; switching activity is vectorless, not measured workload activity.'}
(O/'summary.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
plt.rcParams.update({'font.family':'Arial','font.size':8,'pdf.fonttype':42,'svg.fonttype':'none'})
fig,ax=plt.subplots(figsize=(7.15,2.2));left=[0,0];labels=['Clocks','CLB logic','Signals','DSPs','Static'];cols=['#d3d3d3','#c8b38e','#2c8199','#d76a00','#b5a1cb']
for vals,label,c in zip(zip([1.224,2.668,3.125,.667,.637],[1.125,1.982,2.668,.639,.629]),labels,cols):
 ax.barh([1,0],vals,left=left,color=c,edgecolor='black',label=label,height=.55);left=[a+b for a,b in zip(left,vals)]
ax.set_yticks([1,0],['v5 original PE','v10 preadder PE']);ax.set_xlim(0,9.5);ax.set_xlabel('Engine-only vectorless power estimate (W)');ax.text(8.4,1,'8.321 W',va='center');ax.text(7.13,0,'7.043 W',va='center');ax.legend(ncol=5,fontsize=7,loc='upper center',bbox_to_anchor=(.5,1.3));fig.tight_layout()
for ext in ['pdf','png','svg']:fig.savefig(P/f'figures/core4_power_boundary.{ext}',bbox_inches='tight',dpi=240)
rec=json.loads((P/'data/figure_records.json').read_text(encoding='utf8'))
for version,power,lut in [('v5',8.321,118356),('v10_base_pa48',7.043,104066)]:
 d={k:None for k in rec['records'][0]};d.update(configuration=version,workload='OOC engine implementation',interface_mhz=1000/3.298,core_mhz=1000/3.298,power_w=power,power_scope='engine only, vectorless',power_source='Vivado 2021.2 report_power',evidence='routed estimate',timing_closed=True,raw_file='data/route_intake/'+('v5_power.rpt' if version=='v5' else 'v10_base_pa48_power_route.rpt'),lut=lut,dsp=768,bram=0);d['source_sha256']=hashlib.sha256((P/d['raw_file']).read_bytes()).hexdigest();rec['records'].append(d)
(P/'data/figure_records.json').write_text(json.dumps(rec,indent=2),encoding='utf8')
print(json.dumps(meta,indent=2))
