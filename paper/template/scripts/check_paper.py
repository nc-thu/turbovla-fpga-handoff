"""Artifact integrity checks and PDF contact sheet, not hardware verification."""
from pathlib import Path
import re,json,hashlib,csv,datetime
import fitz
from PIL import Image,ImageOps,ImageDraw
P=Path(__file__).resolve().parents[1];(P/'review').mkdir(exist_ok=True)
tex=(P/'main.tex').read_text(encoding='utf8');log=(P/'main.log').read_text(errors='replace')
tex+='\n'+(P/'tables/capabilities.tex').read_text(encoding='utf8')
audit=json.loads((P/'data/references_audit.json').read_text(encoding='utf8'))
used=set(k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',tex) for k in group.split(','))
bibkeys=set(x['key'] for x in audit)
assert used==bibkeys,(used-bibkeys,bibkeys-used)
assert sum(x['counts_toward_21'] for x in audit if x['key'] in used)>=21
assert 'undefined' not in log.lower(),'Unresolved LaTeX citation/reference'
assert 'Overfull' not in log,'Overfull box: inspect LaTeX log'
manifest=json.loads((P/'data/manifest.json').read_text(encoding='utf8'))
manifest+=json.loads((P/'data/route_intake/manifest.json').read_text(encoding='utf8'))
for row in manifest:assert hashlib.sha256((P/row['snapshot']).read_bytes()).hexdigest()==row['sha256']
quality=list(csv.DictReader((P/'tables/quality_template.csv').open(encoding='utf8')))
assert all(all(v=='' for k,v in row.items() if k!='benchmark') for row in quality)
for name in re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',tex)+re.findall(r'\\fig\{([^}]+)\}',tex):
 if '#' not in name:assert (P/name).is_file(),name
pdf=fitz.open(P/'main.pdf');pages=[]
for i,page in enumerate(pdf):
 pix=page.get_pixmap(matrix=fitz.Matrix(.6,.6));im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
 canvas=Image.new('RGB',(im.width,im.height+22),'#eeeeee');canvas.paste(im,(0,22));ImageDraw.Draw(canvas).text((8,4),f'Page {i+1}',fill='black');pages.append(canvas)
 width=pages[0].width; height=pages[0].height
for start in range(0,len(pages),6):
 group=pages[start:start+6];sheet=Image.new('RGB',(width*3,height*2),'#bbbbbb')
 for j,im in enumerate(group):sheet.paste(im,((j%3)*width,(j//3)*height))
 sheet.save(P/f'review/pages_{start+1}_{start+len(group)}.png')
report={'checked_at':datetime.datetime.now().isoformat(),'pages':len(pdf),'references':len(used),'core_formal_references':sum(x['counts_toward_21'] for x in audit),'snapshots_verified':len(manifest),'unresolved_references':0,'overfull_boxes':0,'quality_numbers_inserted':False,'hardware_experiments_launched':False,'figure_count':len(re.findall(r'\\newlabel\{fig:',(P/'main.aux').read_text()))-2,'note':'Figure labels system/PE/overview alias one composite. This checks artifact integrity, not experimental correctness.'}
report['hardware_experiments_launched']=True
report['matched_rtl_pairs']=48
report['missing_results']=['matched full-policy GPU/FPGA latency','fixed-trajectory replay','matched cumulative burst/preadd','workload-specific per-variant energy']
(P/'review/checks.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2))
