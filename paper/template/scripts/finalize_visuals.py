"""Use corrected imagegen artwork; only quantitative insets use Matplotlib.
PDF composition preserves the artwork, and preview PNGs render those same PDFs.
"""
from pathlib import Path
import json, datetime, hashlib
import fitz
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parents[1]
F=P/'figures'; S=F/'visual_sources'; S.mkdir(exist_ok=True)
A=json.loads((P/'data/arch.json').read_text(encoding='utf8'))
D=json.loads((P/'data/derived_metrics.json').read_text(encoding='utf8'))
values={'mac_pct':D['short_K_lt64_MAC_share_pct'],'cycles_pct':D['short_K_lt64_modeled_cycle_share_pct'],'long_run_byte_pct':A['write_channel']['run_hist'][-1]['byte_share'],'pe_lut':[121,103]}
plt.rcParams.update({'font.family':'Arial','font.size':14,'font.weight':'bold','axes.labelweight':'bold','pdf.fonttype':42,'axes.linewidth':1.1})
for n in range(3):
 fig,ax=plt.subplots(figsize=([(2.43,2.19),(1.86,2.19),(2.64,2.20)][n]))
 fig.subplots_adjust(left=.24,right=.88,bottom=.33,top=.83)
 if n==0:
  vv=[values['mac_pct'],values['cycles_pct']]
  ax.bar([0,1],vv,color=['#c8b38e','#2c8199'],edgecolor='black',width=.65)
  ax.set_xticks([0,1],['MAC','Cycles']);ax.set_ylim(0,40);ax.set_yticks([0,20,40]);ax.set_ylabel('%')
  for i,v in enumerate(vv):ax.text(i,v+1,f'{v:.1f}%',ha='center')
  fig.text(.52,.075,'K < 64; model prediction',ha='center',fontsize=10.5)
 elif n==1:
  ax.barh([0],[values['long_run_byte_pct']],color='#2c8199',edgecolor='black',height=.6)
  ax.set_xlim(0,100);ax.set_ylim(-.6,.6);ax.set_yticks([]);ax.set_xticks([0,50,100]);ax.set_xlabel('%')
  ax.text(50,0,f"{values['long_run_byte_pct']:.1f}%",ha='center',va='center',color='white',fontsize=14)
  ax.set_title('Bytes in long runs',fontsize=12)
  fig.text(.52,.04,'Runs ≥ 2048 B',ha='center',fontsize=11)
 else:
  vv=values['pe_lut'];ax.bar([0,1],vv,color=['#c8b38e','#d76a00'],edgecolor='black',width=.65)
  ax.set_xticks([0,1],['Original','Preadder']);ax.set_ylim(0,150);ax.set_yticks([0,50,100,150]);ax.set_ylabel('LUT / PE')
  for i,v in enumerate(vv):ax.text(i,v+4,str(v),ha='center')
  fig.text(.53,.075,'Isolated PE synthesis',ha='center',fontsize=11)
 fig.savefig(S/f'inset_{n+1}.pdf');plt.close(fig)

for name,source in [('model','model_corrected.png'),('codesign','codesign_corrected.png')]:
 img=fitz.open(F/'concepts'/source);pdf=fitz.open('pdf',img.convert_to_pdf());img.close()
 pg=pdf[0];w,h=pg.rect.width,pg.rect.height
 if name=='codesign':
  # Coordinates in the 1844x849 source artwork; keep all mechanism art untouched.
  for n,box in enumerate([(99,57,342,276),(1068,57,1254,276),(1563,57,1827,277)]):
   rect=fitz.Rect(box[0]/1844*w,box[1]/849*h,box[2]/1844*w,box[3]/849*h)
   pg.draw_rect(rect,color=None,fill=(1,1,1),overlay=True)
   ins=fitz.open(S/f'inset_{n+1}.pdf');pg.show_pdf_page(rect,ins,0,keep_proportion=False);ins.close()
 out=F/f'publication_{name}.pdf'
 pdf.save(out,garbage=4,deflate=True)
 pg.get_pixmap(matrix=fitz.Matrix(2,2)).save(F/f'publication_{name}.png');pdf.close()

t=(P/'main.tex').read_text(encoding='utf8')
t=t.replace('figures/core1_model.pdf','figures/publication_model.pdf').replace('figures/core2_codesign.pdf','figures/publication_codesign.pdf')
t=t.replace('Revision 2 --- September 12, 2026','Revision 3 --- September 12, 2026')
t=t.replace('The camera inset is the existing local scene capture.','The RGB inset illustrates the existing local scene; the depth grid is schematic. The recorded prediction has 64 steps, whereas the controller executes up to 32 per chunk. Robot icons are schematic. The artwork is AI-assisted and checked against the recorded configuration.')
t=t.replace('All three numerical insets are generated from frozen evidence;','The corrected AI-assisted mechanism artwork retains the original visual composition. All three numerical insets are independently script-generated from frozen evidence and embedded as vector graphics;')
(P/'main.tex').write_text(t,encoding='utf8')
now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
manifest={'completed_at':now,'method':'Built-in imagegen local edits; vector data insets; PDF composition; no Visio reconstruction','values':values,'sources':['data/arch.json','data/derived_metrics.json','2026-09-12_证据索引_r2.md'],'artifacts':[]}
for name in ['model','codesign']:
 for ext in ['pdf','png']:
  f=F/f'publication_{name}.{ext}';manifest['artifacts'].append({'path':str(f.relative_to(P)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(P/'data/visual_revision.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
html=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>论文正文两张图 · 修订三版</title><style>body{{font:18px Arial,"Microsoft YaHei";max-width:1500px;margin:32px auto;padding:0 20px;color:#222}}img{{width:100%;border:1px solid #bbb}}p{{line-height:1.7}}a{{color:#176c9a}}</style><h1>论文正文使用的两张图</h1><p>生成时间：{now}。两张图保留原视觉草案的风格，局部修正技术内容。没有用 Visio 重画。以下预览直接由正文引用的同一份 PDF 渲染。</p><p><a href="main.pdf">打开论文 PDF</a> · <a href="figures/publication_model.pdf">模型图 PDF</a> · <a href="figures/publication_codesign.pdf">机制图 PDF</a></p><h2>模型与执行层次</h2><p>这图怎么看：上图从观测走到实际执行；下图分开 10 步去噪、64 步预测序列和最多 32 步执行动作。</p><img src="figures/publication_model.png"><h2>观察、软件与硬件机制</h2><p>这图怎么看：每一列从真实观察走到对应的软件和硬件机制。三张统计小图由原始数据脚本生成，高位乘积单独做借位校正。</p><img src="figures/publication_codesign.png"><p>性能、功耗和消融数据保持修订二版数值，未新增实验。</p></html>'''
(P/'2026-09-12_视觉定稿预览.html').write_text(html,encoding='utf8')
old=(P/'data/base_preview_r2.html').read_text(encoding='utf8')
old=old.replace('figures/core1_model.png','figures/publication_model.png').replace('figures/core2_codesign.png','figures/publication_codesign.png')
old=old.replace('figures/concepts/model_draft.png','figures/publication_model.png').replace('figures/concepts/codesign_draft.png','figures/publication_codesign.png')
old=old.replace('<body>',f'<body><p>视觉修订完成：{now}。前两张图已采用修正后的原视觉草案，与论文一致。未使用 Visio。</p>')
(P/'2026-09-12_五组图表预览.html').write_text(old,encoding='utf8')
(P/'README.md').write_text(f'''# 论文修订三版：正文采用视觉草案\n\n生成时间：{now}。\n\n本版只修改前两张图及图注。打开 main.pdf 或 2026-09-12_视觉定稿预览.html 查看同一套最终图。\n\n完成时间：{now}。内置 imagegen 在原草案上局部编辑，保留布局与配色；三张统计小图由冻结数据生成并嵌入 PDF。没有使用 Visio，没有 .vsdx。图像源文件在 figures/concepts/*_corrected.png；统计 PDF 在 figures/visual_sources；生成提示词在 data/visual_prompts.json；可重复排版脚本为 scripts/finalize_visuals.py。\n\n运行 build.ps1 重建论文；不启动硬件实验。原修订二版目录未修改。性能、功耗、成功率及缺失实验保持原状态。中文实验与文献说明沿用二版日期记录，以本说明作为前两张图的新状态。\n''',encoding='utf8')
print('Corrected visual artwork installed; quantitative insets rendered from frozen data.')
