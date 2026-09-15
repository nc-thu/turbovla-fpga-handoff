from pathlib import Path
import json,datetime,requests,concurrent.futures,hashlib
P=Path(__file__).resolve().parents[1];L=P/'data/literature';now=datetime.datetime.now().isoformat(timespec='seconds')
fields=['target_scope','substrate','full_model_host','iteration_reuse','shape_overlap','low_precision_packing','public_artifacts']
rows=[]
def add(name,key,group,vals,locs,url):
 rows.append({'name':name,'cite':key,'group':group,'source':url,'cells':{k:{'judgment':v,'locator':s} for k,v,s in zip(fields,vals,locs)}})
add('DiTPA','ditpa','Embodied / diffusion',
 ['DiT action planner','ASIC','P: planner only; upstream VLM external','S: features + actions','S: reconfigurable PE; modality scheduler','P: low precision; DSP N/A','NR: compiler / simulator / RTL release'],
 ['PDF p.1 Fig.1','PDF p.8 Sec.V-A (28 nm)','PDF p.1 Fig.1','PDF pp.2-6 Fig.2; algorithms','PDF pp.6-8 hardware design','PDF p.8 implementation setup; no FPGA DSP substrate','PDF pp.1-12: no release URL identified'],
 'local DiTPA PDF; DOI 10.1109/ISCA66397.2026.00188')
add('Cambricon-D','camd','Embodied / diffusion',
 ['Diffusion; sign-mask dataflow','Custom; NR*','NR*: host boundary','S: temporal differences','NR*: detailed schedule','NR*: numeric datapath','NR*: official release'],
 ['ICT author-institution report, paragraphs 4-5','Full text unavailable; not inferred from title','Full text unavailable','ICT report paragraph 4 describes iterative differences','Full text unavailable','Full text unavailable','No official release established; third-party SCALE-Sim excluded'],
 'https://ict.cas.cn/xwgg/jssxw/202404/t20240408_7083571.html')
add('Ditto','ditto','Embodied / diffusion',
 ['Diffusion linear + special functions','ASIC','P: model engine; host boundary NR','S: temporal difference','S: Defo + unit pipeline','S: 4/8-bit; DSP N/A','NR: official source release'],
 ['PDF p.7 Sec.V-A','PDF p.9 Sec.VI-A (45 nm)','PDF p.7 VPU functions; full host audit NR','PDF pp.4-6 Sec.IV','PDF p.7 pipeline; p.10 overlap discussion','PDF pp.7-8 Compute Unit','PDF pp.1-15: no project source URL identified'],
 'https://arxiv.org/pdf/2501.11211')
add('EXION','exion','Embodied / diffusion',
 ['Multimodal diffusion','ASIC','P: diffusion core; host boundary NR','S: FFN reuse','S: ConMerge; overlap NR','P: mixed domains; DSP N/A','NR: release; simulator described'],
 ['PDF p.1 abstract','PDF p.10 Sec.V-B (14 nm)','PDF pp.6-9 Sec.IV','PDF pp.4-5 Sec.III-A','PDF pp.5-8 ConMerge / SDUE','PDF pp.8-9 eager prediction datapath','PDF p.10 custom simulator described, no release location'],
 'https://arxiv.org/pdf/2501.05680')
add('Diff-DiT','diffdit','Embodied / diffusion',
 ['Low-bit DiT inference','FPGA','P: DiT kernel; host boundary NR','S: differential attention','S: cross-cast + pipelining','S: low-bit; packing code','P: HLS + tests; compiler NR'],
 ['IEEE abstract; README modes 0-12','IEEE abstract; src/TOP.cpp','README mode table; full host boundary not established','IEEE abstract ADA; src masks','IEEE abstract contributions 2-3','src/AMA_rtl.cpp; src/TOP.cpp; exact packing details require code audit','README Code Structure: TOP.cpp, test.cpp; not claimed full compiler/RTL release'],
 'https://github.com/Glinttsd/Diff-DiT')
add('FlightLLM','flight','Transformer / general FPGA',
 ['LLM prefill + decode','FPGA','S: LLM operators; host orchestration','N/A: diffusion reuse','S: MM/MV + fused dataflow','S: mixed precision; DSP chain','P: profiling + board demo'],
 ['PDF pp.3-6 architecture','PDF p.1 abstract','PDF pp.3-4 SFU, controller; host demo','Target is autoregressive LLM, not diffusion iteration reuse','PDF pp.4-6 Fig.5-8','PDF pp.4-5 DSP VPU / chain','Official README profile/ and fpga_implementation/; not full source assertion'],
 'https://github.com/FlightLLM/flightllm_test_demo')
add('Quasar-ViT','quasar','Transformer / general FPGA',
 ['ViT GEMM + SLS','FPGA','P: ARM norm / GELU / Softmax','N/A: diffusion reuse','S: tiling + double buffers','S: hybrid signed DSP packing','NR: official source release'],
 ['PDF p.7 Sec.4.1','PDF p.7 Fig.6','PDF p.7 Sec.4.1 explicitly names ARM modules','ViT target; no diffusion iteration axis','PDF p.7 Sec.4.1; p.10 cycle model','PDF pp.7-9 Sec.4.2-4.3, Fig.7','PDF pp.1-14: no release URL; no official repository established'],
 'https://arxiv.org/pdf/2407.18175')
add('FINN','finn','Transformer / general FPGA',
 ['Binarized neural networks','FPGA','S: supported BNN; host I/O','N/A: diffusion reuse','S: folding + streaming','S: binary; DSP packing N/A','S: compiler + tests + RTL library*'],
 ['PDF pp.4-5 Sec.4','PDF p.1','PDF pp.4-6 heterogeneous network streaming','BNN target, not iterative diffusion','PDF pp.4-6 Sec.4.1 / 4.4','PDF pp.4-5 XNOR-popcount / thresholds','Official repo src/finn, tests, finn-rtllib; current repo differs from 2017 prototype'],
 'https://github.com/Xilinx/finn')
add('VLA-FPGA','', 'This work',
 ['Traced HoloBrain-0 segments','FPGA','P: explicit HostOp boundaries','NR: no new reuse method','P: overlap; merge pending','S: exact INT8 Pack2 preadder','P: local compiler / simulator / RTL; release planned'],
 ['data/arch.json; compiler snapshot','data/clock_rtl.sv','data/compiler.py HostOp','No inter-iteration reuse optimization claimed','v8 RTL + arch model; compiler merge not integrated','v9 preadder reports; v10 synthesis not routed','https://github.com/nc-thu/vector-core-r3c; no permission/publication changes'],
 'data/manifest.json')
(P/'data/capabilities.json').write_text(json.dumps({'generated_at':now,'legend':{'S':'supported','P':'partial','NR':'not reported in checked source','N/A':'not applicable','NR*':'not verified because full text unavailable'},'rows':rows},indent=2),encoding='utf8')
md=f'# 相关架构逐项核查\n\n生成与本轮核查完成时间：{now}。\n\nS＝支持，P＝部分支持，NR＝所查来源未报告，N/A＝不适用。NR* 特指全文未取得，不能解释为论文未报告。所有结论只覆盖下列定位范围。FINN 的公开情况来自当前官方仓库，不回溯成 2017 年已经公开同样文件。\n\n'
for row in rows:
 md+=f'## {row["name"]}\n\n来源：{row["source"]}\n\n|比较项|判断|原文或代码位置|\n|---|---|---|\n'
 for k,v in row['cells'].items():md+=f'|{k}|{v["judgment"]}|{v["locator"]}|\n'
md+='\nCambricon-D 的正式发表信息已核实；IEEE 页面触发机器人检查，全文未取得。因此本文没有凭题名补齐其宿主、数值电路或源码能力。Diff-DiT 的公开代码与 IEEE 摘要可查，尚不宣称它公开了完整编译器。\n'
(P/'2026-09-12_相关工作逐项证据.md').write_text(md,encoding='utf8')
def esc(s):return s.replace('&',r'\&').replace('_',r'\_').replace('×',r'$\times$')
tex=r'''\begin{table*}[t]\centering
\caption{Architecture capabilities, grouped by target scope. S: supported; P: partial; NR: not reported in the checked source; N/A: not applicable. NR* indicates unavailable full text, not a negative judgment. Detailed source locations are provided with the artifact.}\label{tab:related}
\fontsize{7}{8.5}\selectfont\setlength{\tabcolsep}{2pt}\renewcommand{\arraystretch}{1.22}
\begin{tabularx}{\textwidth}{@{}p{.095\textwidth}p{.105\textwidth}p{.05\textwidth}XXXX X@{}}\toprule
Architecture & Target / scope & Device & Full model / host & Iteration reuse & Shape / overlap & Arithmetic / packing & Public artifacts\\\midrule
'''
last=None
for row in rows:
 if row['group']!=last:tex+=r'\multicolumn{8}{l}{\textit{'+row['group']+r'}}\\'+'\n';last=row['group']
 name=row['name']+(r'~\cite{'+row['cite']+'}' if row['cite'] else '')
 tex+=name+' & '+' & '.join(esc(v['judgment']) for v in row['cells'].values())+r'\\'+'\n'
tex+=r'\bottomrule\end{tabularx}\end{table*}'
(P/'tables/capabilities.tex').write_text(tex,encoding='utf8')

# Add four formally published works using publisher-deposited Crossref metadata.
dois={'camd':'10.1109/ISCA59077.2024.00070','ditto':'10.1109/HPCA61900.2025.00035','exion':'10.1109/HPCA61900.2025.00034','diffdit':'10.1109/ICCAD66269.2025.11240791'}
audit=json.loads((P/'data/references_audit.json').read_text(encoding='utf8'));bib=(P/'references.bib').read_text(encoding='utf8')
for key,doi in dois.items():
 path=L/(key+'_crossref.json')
 if not path.exists():
  d=requests.get('https://api.crossref.org/works/'+doi,timeout=25).json()['message'];path.write_text(json.dumps(d,indent=2),encoding='utf8')
 d=json.loads(path.read_text());authors=' and '.join(v.get('given','')+' '+v['family'] for v in d['author']);year=d['published']['date-parts'][0][0];title=d['title'][0];venue=d['container-title'][0]
 if key not in {x['key'] for x in audit}:
  audit.append({'key':key,'title':title,'authors':authors,'venue':venue,'year':year,'url':'https://doi.org/'+doi,'doi':doi,'counts_toward_21':True,'verified':now,'claim':'Capability comparison; no cross-model performance reuse','verification':'Publisher-deposited Crossref metadata + capability audit'})
  bib+='\n@inproceedings{'+key+',\n  title={{'+title+'}},\n  author={'+authors+'},\n  booktitle={'+venue+'},\n  year={'+str(year)+'},\n  doi={'+doi+'}\n}\n'
(P/'references.bib').write_text(bib,encoding='utf8');(P/'data/references_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
print('Capability table:',len(rows),'rows;',len(audit),'references')
md=f'# 参考文献核验\n\n生成时间：{now}。33 条参考文献，其中 26 篇计入正式顶会论文，6 篇领域会议论文另计，1 份厂商文档。元数据核验不等于全文所有能力已核实；Cambricon-D 的全文访问缺口另列。\n\n|键|论文与来源|发表信息|支持论点|\n|---|---|---|---|\n'
for r in audit:md+=f'|{r["key"]}|[{r["title"]}]({r["url"]})|{r["venue"]}, {r["year"]}|{r["claim"]}|\n'
(P/'2026-09-12_references_audit.md').write_text(md,encoding='utf8')
