"""Rebuild paper plots from frozen, versioned local evidence. No experiments run."""
from pathlib import Path
import json, hashlib, shutil, datetime, csv
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parents[1]
ROOT=OUT.parents[1]
for p in ['data','figures','tables']:(OUT/p).mkdir(parents=True,exist_ok=True)
SOURCES={
 'arch':'arch/v8_2026-09-11_2315_gemm_util_design/util_decomp.json',
 'cycles':'hw/v8_2026-09-12_0054_rtl_util_r5/results/p2_cyc.json',
 'write':'hw/v8_2026-09-12_0054_rtl_util_r5/results/r5_wr_compare.json',
 'hier':'hw/v8_2026-09-12_0054_rtl_util_r5/results/hier_modsum.json',
 'pe':'hw/v9_2026-09-12_1102_preadd_pack2/results/summary_v9.json',
 'v10_verdict':'hw/v10_2026-09-12_1148_engfull_preadd/notes/regression_verdict.md',
 'compiler':'compiler/v7_2026-09-10_1258_f4_ybase_pong/sw/compiler.py',
 'clock_rtl':'hw/v8_2026-09-12_0054_rtl_util_r5/rtl_p2/ae_gemm_p2d.sv',
 'arch_script':'arch/v8_2026-09-11_2315_gemm_util_design/util_decomp.py',
 'pe_base_util':'hw/v9_2026-09-12_1102_preadd_pack2/results/synth_base48/util.rpt',
 'pe_cand_util':'hw/v9_2026-09-12_1102_preadd_pack2/results/synth_cand48/util.rpt',
 'pe_base_hier':'hw/v9_2026-09-12_1102_preadd_pack2/results/synth_base48/util_hier.rpt',
 'pe_cand_hier':'hw/v9_2026-09-12_1102_preadd_pack2/results/synth_cand48/util_hier.rpt',
 'pe_base_route':'hw/v9_2026-09-12_1102_preadd_pack2/results/synth_base48/wns_route.txt',
 'pe_cand_route':'hw/v9_2026-09-12_1102_preadd_pack2/results/synth_cand48/wns_route.txt',
 'pe_math_log':'hw/v9_2026-09-12_1102_preadd_pack2/notes/math_exhaustive_out.txt',
 'pe_verilator_log':'hw/v9_2026-09-12_1102_preadd_pack2/results/run_pe_pair_verilator.log',
 'pe_xsim_log':'hw/v9_2026-09-12_1102_preadd_pack2/results/run_pe_pair_xsim.log',
}
manifest=[]; D={}
old_manifest={r['id']:r for r in json.loads((OUT/'data/manifest.json').read_text(encoding='utf8'))} if (OUT/'data/manifest.json').exists() else {}
for name,rel in SOURCES.items():
 src=ROOT/rel; dest=OUT/'data'/(name+src.suffix)
 # Freeze once: later builds never silently incorporate ongoing experiment results.
 if not dest.exists():shutil.copy2(src,dest)
 b=dest.read_bytes()
 source_time=old_manifest.get(name,{}).get('source_mtime') or (datetime.datetime.fromtimestamp(src.stat().st_mtime).isoformat() if src.exists() else None)
 manifest.append(dict(id=name,source=rel,snapshot=str(dest.relative_to(OUT)),sha256=hashlib.sha256(b).hexdigest(),source_mtime=source_time,snapshot_mtime=datetime.datetime.fromtimestamp(dest.stat().st_mtime).isoformat()))
 if dest.suffix=='.json':D[name]=json.loads(b.decode('utf-8-sig'))
(OUT/'data/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
plt.rcParams.update({'font.family':'Arial','font.size':8,'axes.labelsize':8,'axes.titlesize':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42,'savefig.bbox':'tight','axes.axisbelow':True})
COL=['#a9c9e2','#edc191','#add6bd','#c9bcda']
def save(fig,name):
 fig.savefig(OUT/f'figures/{name}.pdf');fig.savefig(OUT/f'figures/{name}.png',dpi=220);plt.close(fig)
def bars(ax,groups,series,labels,ylabel):
 x=np.arange(len(groups));w=.8/len(series)
 for j,(v,l) in enumerate(zip(series,labels)):
  ax.bar(x-.4+w/2+j*w,v,w,label=l,color=COL[j],edgecolor='black',linewidth=.7)
 ax.set_xticks(x,groups);ax.set_ylabel(ylabel);ax.grid(axis='y',alpha=.2)

a=D['arch']; b=a['k_dist']['buckets']
fig,ax=plt.subplots(1,2,figsize=(7.1,2.35),gridspec_kw={'width_ratios':[1.3,1]})
groups=[f"{v['lo']}–{v['hi']-1}" for v in b];groups[-1]='1024–4096*'
bars(ax[0],groups,[[v['cyc_share'] for v in b],[v['mac_G']/a['meta']['macs_G']*100 for v in b]],['Modeled cycle share','MAC share'],'Share (%)')
ax[0].tick_params(axis='x',labelrotation=45);ax[0].legend(fontsize=7);ax[0].set_title('(a) Reduction length K (arch v8 trace)')
s=a['shapes_top'][:6]
ax[1].barh([f"K={v['k']}, N={v['n']}" for v in s][::-1],[v['share'] for v in s][::-1],color=COL[0],edgecolor='black',linewidth=.7)
ax[1].set_xlabel('Modeled GEMM cycle share (%)');ax[1].set_title('(b) Frequent costly shapes');fig.tight_layout();save(fig,'shape_distribution')

c=D['cycles']; keys=['base48','pp48_wb1','pp48_wb2','p2d48']
if keys[0] not in c: keys[0]='p2_base48'
fig,ax=plt.subplots(1,2,figsize=(7.1,2.25))
for i,(case,title) in enumerate([('L1','K=64'),('L2','K=2049')]):
 vals=[]
 for k in keys:
  entry=c[k]['L'].get(case,c[k]['L'].get(case+'b'))
  vals.append(entry['cycles']/entry['mt'])
 bars(ax[i],['Base','Overlap','+ 2 reads','+ 2x core'],[vals],['RTL'],'Interface cycles / row group')
 for j,v in enumerate(vals):ax[i].text(j,v+max(vals)*.015,str(Decimal(str(v)).quantize(Decimal('.1'),rounding=ROUND_HALF_UP)),ha='center',fontsize=8)
 ax[i].set_ylim(0,max(vals)*1.2);ax[i].set_title(f'({chr(97+i)}) {title}; amortized including startup')
fig.tight_layout();save(fig,'rtl_ablation')

w=D['write'];fig,ax=plt.subplots(1,2,figsize=(7.1,2.3))
groups=[v['seg'].replace('seg_','') for v in w]
for i,(base,new,ttl) in enumerate([('base_cyc','r5_cyc','Complete segment'),('base_wr','r5_wr','Write-channel activity')]):
 bars(ax[i],groups,[[v[base]/1000 for v in w],[v[new]/1000 for v in w]],['Base','Burst writer'],'Interface cycles (thousands)')
 ax[i].set_title(f'({chr(97+i)}) {ttl}');ax[i].legend(fontsize=7)
 for j,v in enumerate(w):ax[i].text(j,max(v[base],v[new])/1000+max(x[base] for x in w)/1000*.02,f"−{100*(1-v[new]/v[base]):.1f}%",ha='center',fontsize=7)
 ax[i].set_ylim(0,max(v[base] for v in w)/1000*1.23)
fig.tight_layout();save(fig,'write_results')

p=D['pe'];r=p['R4R5_ooc_synth'];fig,ax=plt.subplots(1,3,figsize=(7.1,2.1))
bars(ax[0],['LUT / PE'],[[r['per_PE_hier']['LUT'][0]],[r['per_PE_hier']['LUT'][1]]],['Base','Preadder'],'LUTs')
bars(ax[1],['LUT','FF'],[[r['strip_total']['LUT'][0],r['strip_total']['FF'][0]],[r['strip_total']['LUT'][1],r['strip_total']['FF'][1]]],['Base','Preadder'],'48-PE strip resources')
bars(ax[2],['Route WNS'],[[p['R6_route']['wns_ns']['base']],[p['R6_route']['wns_ns']['cand']]],['Base','Preadder'],'Slack (ns), 3.298 ns constraint')
ax[0].set_title('(a) LUT −14.9%');ax[1].set_title('(b) LUT −12.4%; 48 DSPs both');ax[2].set_title('(c) Both meet strip timing');ax[0].legend(fontsize=7)
fig.tight_layout();save(fig,'pe_resources')

lad=a['ladder'][:5];fig,ax=plt.subplots(figsize=(7.1,2.1))
x=np.arange(5)
ax.plot(x,[v['frame_s'] for v in lad],'-o',color='#476c99',label='Original write model')
ax.plot(x,[v['frame_r5_s'] for v in lad],'--s',color='#b26735',label='Burst-write model')
ax.set_xticks(x,['Base','Overlap','+ 2 reads','+ 2x core','+ N merge'])
ax.set_ylabel('Projected frame latency (s)');ax.set_ylim(.45,1);ax.legend(ncol=2,fontsize=8);ax.grid(alpha=.2)
ax.set_title('Historical arch v8 projection — not measured system performance')
fig.tight_layout();save(fig,'model_interaction')

with (OUT/'tables/quality_template.csv').open('w',newline='',encoding='utf8') as f:
 writer=csv.writer(f);writer.writerow(['benchmark','task','seed_list','episodes','reference_success','integer_success','delta_percentage_points','confidence_interval','checkpoint_sha256','quantization_sha256'])
 for name in ['LIBERO (suite TBD)','RoboTwin (tasks TBD)']:writer.writerow([name]+['']*9)
summary={'short_K_lt64_modeled_cycle_share_pct':sum(v['cyc_share'] for v in b[:3]),'short_K_lt64_MAC_share_pct':sum(v['mac_G'] for v in b[:3])/a['meta']['macs_G']*100,'pe_lut_reduction_pct':100*(1-103/121),'strip_lut_reduction_pct':100*(1-6124/6988),'clock_note':'single clock peak1536 MAC/iface cycle; 2x core peak3072, assuming768 DSPs and2 products/core cycle','quality_values':None,'full_engine_preadder_results':None}
(OUT/'data/derived_metrics.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
print(json.dumps({'output':str(OUT),'figures':5,'snapshots':len(manifest),'derived':summary},indent=2))
