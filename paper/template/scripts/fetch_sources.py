from pathlib import Path
import requests,fitz,json,concurrent.futures
P=Path(__file__).resolve().parents[1];O=P/'data/literature';O.mkdir(exist_ok=True)
urls={'ditto':'https://arxiv.org/pdf/2501.11211','exion':'https://arxiv.org/pdf/2501.05680','flight':'https://arxiv.org/pdf/2401.03868','quasar':'https://arxiv.org/pdf/2407.18175','finn':'https://arxiv.org/pdf/1612.07119','diffdit_code':'https://raw.githubusercontent.com/Glinttsd/Diff-DiT/master/README.md'}
def run(kv):
 k,u=kv
 try:
  r=requests.get(u,timeout=40);r.raise_for_status();ext='.pdf' if r.content.startswith(b'%PDF') else '.md';p=O/(k+ext);p.write_bytes(r.content)
  if ext=='.pdf':
   doc=fitz.open(p);(O/(k+'.txt')).write_text('\n'.join(f'\n=== PDF PAGE {i+1} ===\n'+page.get_text() for i,page in enumerate(doc)),encoding='utf8')
  return {'key':k,'url':u,'file':str(p),'status':'downloaded'}
 except Exception as e:return {'key':k,'url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:result=list(ex.map(run,urls.items()))
(O/'sources.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result,indent=2))
