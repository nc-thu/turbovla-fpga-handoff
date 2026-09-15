from pathlib import Path
import zipfile,datetime,json
P=Path(__file__).resolve().parents[1]
stamp=datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
out=P.parent/f'VLA_FPGA_r3_{stamp}.zip'
exclude={'.aux','.out','.blg','.zip','.pyc'}
files=[]
for p in P.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(P);s=rel.as_posix()
 if p.suffix in exclude or '__pycache__' in s or s.startswith('figures/references/') or s.startswith('review/pages_'):continue
 if p.suffix=='.log' and p.parent==P:continue
 if s.startswith('data/literature/') and p.suffix in {'.pdf','.txt'}:continue
 files.append((p,rel))
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for p,rel in files:z.write(p,str(Path('VLA_FPGA_r3')/rel))
print(json.dumps({'archive':str(out),'files':len(files),'reference_screenshots_excluded':True,'third_party_full_text_excluded':True},ensure_ascii=False))
