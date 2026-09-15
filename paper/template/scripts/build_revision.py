"""Versioned revision assets. Missing evidence is never converted into zero."""
from pathlib import Path
import json,hashlib,datetime,shutil,re,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch
P=Path(__file__).resolve().parents[1];R=P.parents[1]; F=P/'figures'
NOW=datetime.datetime.now().isoformat(timespec='seconds')
A=json.loads((P/'data/arch.json').read_text(encoding='utf8'))
plt.rcParams.update({'font.family':'Arial','font.size':8,'font.weight':'bold','axes.labelsize':8,'axes.titlesize':8,'pdf.fonttype':42,'svg.fonttype':'none','savefig.bbox':'tight','axes.axisbelow':True})
C=['#d3d3d3','#c8b38e','#2c8199','#d76a00'];light=['#e1ecd8','#f8e2ce','#dcecf5','#e7e0ef']
def save(fig,name):
 for ext in ['pdf','svg','png']:fig.savefig(F/f'{name}.{ext}',dpi=240)
 plt.close(fig)
def txt(ax,x,y,s,size=8,**kw):ax.text(x,y,s,ha='center',va='center',fontsize=size,**kw)
def box(ax,x,y,w,h,s='',color='white',size=8,dash=False):
 ax.add_patch(Rectangle((x,y),w,h,facecolor=color,edgecolor='black',lw=1.1,linestyle='--' if dash else '-'));txt(ax,x+w/2,y+h/2,s,size)
def arrow(ax,x,y,xx,yy,color='black'):
 ax.add_patch(FancyArrowPatch((x,y),(xx,yy),arrowstyle='-|>',mutation_scale=9,lw=1.05,color=color))
def canvas(w,h):
 fig,ax=plt.subplots(figsize=(w,h));ax.set(xlim=(0,100),ylim=(0,100));ax.axis('off');fig.subplots_adjust(left=.01,right=.99,bottom=.01,top=.99);return fig,ax

# Group 1: corrected vector master; raster generation is retained as a draft.
fig,ax=canvas(7.15,3.85)
box(ax,0,53,100,47);box(ax,0,0,100,49)
scene=plt.imread(P/'data/scene_head.png');ax.imshow(scene,extent=(2,15,76,94),aspect='auto',zorder=2);txt(ax,8.5,96,'RGB observation',7)
box(ax,2,66,13,7,'Depth',light[0]);box(ax,2,56,13,7,'Instruction',light[1])
for y,label,col in [(80,'RGB Swin',light[0]),(69,'Depth Swin',light[0]),(59,'BERT',light[1])]:
 box(ax,21,y-3,17,8,label,col);arrow(ax,15,y+1,21,y+1);arrow(ax,38,y+1,44,y+1)
box(ax,44,58,18,29,'Spatial +\nmultimodal\nfeatures',light[2]);arrow(ax,62,72,67,72)
box(ax,67,63,14,17,'Action\ndecoder',light[3]);box(ax,67,85,14,8,'Robot state',light[1]);arrow(ax,74,85,74,80)
arrow(ax,81,72,86,72);box(ax,86,63,12,17,'Action\nsequence',light[3]);txt(ax,51,96,'(a) HoloBrain-0 dataflow',9)
txt(ax,57,55,'Partition inside modules: FPGA GEMMs + HostOp boundaries',7)
txt(ax,50,45,'(b) One policy call: action-head iteration and execution',9)
box(ax,2,16,15,22,'Encoded\nfeatures',light[2]);arrow(ax,17,28,22,28)
box(ax,22,9,59,30);txt(ax,51.5,36,'10 denoising steps',8)
for x,label in [(25,'Block 1'),(39,'Block 2'),(61,'Block 6')]:box(ax,x,22,12,9,label,light[3],7)
arrow(ax,37,26,39,26);txt(ax,56,26,'…',13);arrow(ax,73,26,77,26)
txt(ax,49,18,'Joint / image / text attention + FFN',7)
box(ax,27,11,21,5,'Upsample head',light[3],7);box(ax,55,11,22,5,'Scheduler update',light[1],7);arrow(ax,48,13.5,55,13.5)
ax.plot([77,79,79,25,25,27],[26,26,20,20,13.5,13.5],color='black',lw=1);arrow(ax,25,13.5,27,13.5)
ax.plot([66,66,23,23],[11,6,6,24],color='black',lw=1);arrow(ax,23,24,25,24)
ax.plot([77,83,83],[13.5,13.5,25],color='black',lw=1);arrow(ax,83,25,85,25);box(ax,85,18,13,17,'Predicted\nsequence',light[3],7)
txt(ax,91.5,11,'Controller',7);txt(ax,50,3,'Execute up to 32 actions per chunk → acquire the next observation',7)
save(fig,'core1_model')

# Group 2: actual mini plots; no statistics are drawn by the image generator.
fig,ax=canvas(7.15,4.35)
for x in [0,5,36.67,68.33,100]:ax.plot([x,x],[0,100],'k-',lw=1.1)
for y in [0,34,67,100]:ax.plot([0,100],[y,y],'k-',lw=1.1)
for y,s in [(83.5,'Observation'),(50.5,'Compilation / scheduling'),(17,'Hardware')]:txt(ax,2.5,y,s,7,rotation=90)
for x,s in [(20.5,'C1: Heterogeneous shapes'),(52.5,'C2: Short write transactions'),(84.5,'C3: Repeated PE correction')]:txt(ax,x,96,s,8)
# inset axes positions are explicit within source figure.
ax1=fig.add_axes([.10,.79,.22,.12]);short=sum(b['mac_G'] for b in A['k_dist']['buckets'] if b['hi']<=64)/A['meta']['macs_G']*100;cyc=sum(b['cyc_share'] for b in A['k_dist']['buckets'] if b['hi']<=64)
ax1.bar([0,1],[short,cyc],color=[C[1],C[2]],edgecolor='black',width=.5);ax1.set_xticks([0,1],['MAC','Cycles']);ax1.set_ylim(0,38);ax1.set_yticks([0,20]);ax1.set_ylabel('%');ax1.tick_params(labelsize=7)
for i,v in enumerate([short,cyc]):ax1.text(i,v+1,f'{v:.1f}%',ha='center',fontsize=7)
txt(ax,21,70,'K < 64; architecture-model prediction',6.9)
ax2=fig.add_axes([.416,.79,.22,.12]);v=A['write_channel']['run_hist'][-1]['byte_share'];ax2.barh([0],[v],color=C[2],edgecolor='black');ax2.set_xlim(0,100);ax2.set_yticks([]);ax2.set_xticks([0,50,100]);ax2.text(50,0,f'{v:.1f}% of bytes',ha='center',va='center',color='white',fontsize=8)
txt(ax,52.5,70,'Contiguous runs ≥ 2048 bytes; trace',6.9)
ax3=fig.add_axes([.753,.79,.22,.12]);ax3.bar([0,1],[121,103],color=[C[1],C[3]],edgecolor='black',width=.5);ax3.set_xticks([0,1],['Original','Preadder']);ax3.set_ylim(0,155);ax3.set_ylabel('LUT / PE');ax3.tick_params(labelsize=7)
for i,v in enumerate([121,103]):ax3.text(i,v+4,str(v),ha='center',fontsize=7)
txt(ax,84.5,70,'−14.9% LUT; isolated PE synthesis',6.9)
for x in [8,40,72]:
 box(ax,x,48,8,10,'Tiles' if x==8 else ('Addr.' if x==40 else 'INT8'),light[0],7);arrow(ax,x+8,53,x+12,53)
box(ax,20,46,14,14,'Shape\ngroups',light[2],7);txt(ax,21,62,'Classify → schedule',8);txt(ax,21,39,'Legal column merge: pending',7,color='#a32620')
box(ax,52,46,14,14,'Base +\nlength',light[2],7);txt(ax,52,62,'Identify contiguous runs',8);txt(ax,52,39,'Burst layout: segment prototype',7)
box(ax,84,46,14,14,'Packed\nweights',light[3],7);txt(ax,84,62,'Preserve integer semantics',8);txt(ax,84,39,'Exact products; unchanged quantization',6.8)
box(ax,8,18,8,10,'Slice\n0 / 1',light[0],7);arrow(ax,16,23,19,23);box(ax,19,18,7,10,'PEs',light[2],7);arrow(ax,26,23,29,23);box(ax,29,18,6,10,'Snap.',light[3],6.5)
for y,x,s,col in [(11,9,'Compute g+1',C[2]),(7,16,'Read g',C[1])]:box(ax,x,y,18,3,s,col,6)
txt(ax,21,30,'Overlap + paired delivery',8);txt(ax,21,2.5,'2× core: timing not closed',6.8,color='#a32620')
for x,w,s,col in [(40,7,'FIFO',light[0]),(50,9,'Burst\nwriter',light[2]),(62,5,'DDR',light[1])]:box(ax,x,17,w,11,s,col,6.8)
arrow(ax,47,22,50,22);arrow(ax,59,22,62,22);txt(ax,53,11,'AW / W / B; backpressure',7);txt(ax,53,4,'Amortize transaction overhead',7,color='#246788')
box(ax,71,13,18,15,'(A + D) → ×B\nDSP48E2',light[3],7);arrow(ax,89,21,92,21);box(ax,92,13,7,15,'Borrow\n+ acc.',light[2],6.5);txt(ax,84,30,'Internal bias correction',8);txt(ax,84,6,'Retain high-product +P[15]',7);txt(ax,84,2,'No additional DSP',7,color='#246788')
save(fig,'core2_codesign')

# All result records have explicit evidence boundaries.
records=[]
def record(**kw):
 d={k:None for k in ['model','model_sha256','checkpoint_sha256','input_sha256','workload','configuration','effective_mac','interface_mhz','core_mhz','cycles','latency_s','power_w','power_scope','power_source','evidence','raw_file','source_sha256','timing_closed','calls_per_joule']};d.update(kw);records.append(d);return d
for variant in ['GPU HoloBrain-0','FPGA baseline','FPGA optimized']:
 record(model='HoloBrain-0',workload='place_empty_cup',configuration=variant,evidence='pending matched full-policy measurement',power_scope='full platform including host and external memory')
for i,row in enumerate(A['ladder'][:4]):
 record(model='HoloBrain-0 archived trace',workload='49569-GEMM archived schedule',configuration=f'arch_v8_stage_{i}',effective_mac=A['meta']['macs_G']*1e9,interface_mhz=A['meta']['f_iface_MHz'],cycles=row['G']*1e6,latency_s=row['G']/A['meta']['f_iface_MHz'],evidence='architecture prediction; GEMM only; not policy latency',raw_file='data/arch.json',source_sha256=hashlib.sha256((P/'data/arch.json').read_bytes()).hexdigest())

# Group 4: numeric comparison is visibly pending; historical cycles are separate.
fig,axs=plt.subplots(3,1,figsize=(7.15,4.45),gridspec_kw={'height_ratios':[1,1,1.3]})
for ax,title in zip(axs[:2],['(a) Policy calls/s and fixed-trajectory inference time','(b) Energy per call and calls/J — matched platform boundary']):
 ax.set_xlim(-.5,2.5);ax.set_ylim(0,1);ax.set_yticks([]);ax.set_xticks(range(3),['HoloBrain-0 GPU','FPGA baseline','FPGA optimized']);ax.set_title(title)
 for x in range(3):ax.text(x,.55,'Not yet measured',ha='center',va='center',fontsize=8,color='#555555')
 ax.spines[['top','right','left']].set_visible(False)
vals=[r['G'] for r in A['ladder'][:4]]; ax=axs[2];bars=ax.bar(range(4),vals,color=C,edgecolor='black',width=.55);bars[-1].set_hatch('///')
ax.set_xticks(range(4),['Serial','+ overlap','+ dual readout','+ 2× core*']);ax.set_ylabel('GEMM cycles (million)');ax.set_title('(c) Archived schedule prediction; excludes HostOp and transfers')
for i,v in enumerate(vals):ax.text(i,v+3,f'{v:.1f}',ha='center',fontsize=8)
ax.set_ylim(0,max(vals)*1.23);ax.grid(axis='y',alpha=.2);fig.tight_layout(h_pad=1.35);save(fig,'core4_performance')
fig,ax=plt.subplots(figsize=(7.15,1.8));pieces=[1.224,2.668,3.125,.667,.637];labels=['Clocks','CLB logic','Signals','DSPs','Static'];left=0
for val,label,color in zip(pieces,labels,[C[0],C[1],C[2],C[3],'#b5a1cb']):
 ax.barh([0],val,left=left,label=f'{label}: {val:.3f} W',color=color,edgecolor='black');left+=val
ax.set_xlim(0,9);ax.set_yticks([]);ax.set_xlabel('Routed v5 engine estimate (W); not complete-system power');ax.legend(ncol=3,loc='upper center',bbox_to_anchor=(.5,1.5),fontsize=7);ax.text(8.45,0,'8.321 W',ha='left',va='center',fontsize=7)
fig.tight_layout();save(fig,'core4_power_boundary')

# Group 5: only matched verified simulation records enter the cycle comparison.
logs=P/'data/matched48'; variants=['base','overlap','read2','core2'];cases=['shortK','mediumK','deepK','narrowN'];parsed={}
for var in variants:
 path=logs/var/'run.log'
 if not path.exists():continue
 text=path.read_text(errors='replace');passed='MATCHED ALL PASS' in text and 'FAIL' not in text
 parsed[var]={}
 for match in re.finditer(r'\[(shortK|mediumK|deepK|narrowN)\] cycles=(\d+) mac=(\d+) m=(\d+) n=(\d+) nl=(\d+) j0=(\d+) k=(\d+)',text):
  case,cycles,mac,m,n,nl,j0,k=match.groups();parsed[var][case]=int(cycles) if passed else None
  record(model='deterministic INT8 GEMM',workload=case,configuration=f'PCOLS48_{var}_M32',effective_mac=int(m)*int(nl)*int(k),cycles=int(cycles) if passed else None,evidence='RTL bit-exact simulation',raw_file=str(path.relative_to(P)),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),power_scope='engine',timing_closed=None,input_definition_sha256=hashlib.sha256((P/'experiment_inputs/matched48/sim/tb_gemm_p2.sv').read_bytes()).hexdigest(),input_hash_note='Definition hash covers baseline testbench and deterministic seed; actual input tensor hash not exported.')
fig,axs=plt.subplots(2,1,figsize=(7.15,3.45),gridspec_kw={'height_ratios':[1.7,1]})
x=np.arange(4);width=.18
for j,var in enumerate(variants):
 values=[parsed.get('base',{}).get(c)/parsed[var][c] if parsed.get('base',{}).get(c) and parsed.get(var,{}).get(c) else np.nan for c in cases]
 bars=axs[0].bar(x+(j-1.5)*width,values,width,color=C[j],edgecolor='black',label=['Pack2 baseline','+ overlap','+ dual readout','+ 2× core (cycles only)'][j],hatch='///' if j==3 else None)
 for bar,v in zip(bars,values):
  if np.isfinite(v):axs[0].text(bar.get_x()+width/2,v+.035,f'{v:.2f}×',ha='center',rotation=90,fontsize=7)
axs[0].set_xticks(x,['Short K=5','K=64','Deep K=2049','Narrow N=6']);axs[0].set_ylim(0,2.7);axs[0].set_ylabel('Baseline cycles / cycles');axs[0].grid(axis='y',alpha=.2);fig.legend(ncol=2,fontsize=7,loc='upper center',bbox_to_anchor=(.5,1.0));axs[0].set_title('(a) Equal-workload RTL cycles: M=32, two row groups, PCOLS=48',pad=8)
axs[1].axis('off');axs[1].text(.5,.82,'(b) Normalized energy efficiency — pending matched power',ha='center',fontsize=8);axs[1].text(.5,.44,'Workload-matched power is missing; no energy bars are inferred.\nPreadder paired checks: unchanged cycles. Burst writer is not integrated.\nColumn merging remains pending equivalence validation.',ha='center',va='center',fontsize=8,color='#555555')
fig.tight_layout(h_pad=1.5,rect=(0,0,1,.83));save(fig,'core5_ablation')
(P/'data/figure_records.json').write_text(json.dumps({'generated_at':NOW,'records':records},ensure_ascii=False,indent=2),encoding='utf8')
print('Revision plots and explicit-null records generated',NOW)
