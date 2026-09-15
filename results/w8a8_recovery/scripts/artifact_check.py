"""Structural HTML and arithmetic checks; not a substitute for visual review."""
import argparse,datetime,json,math,re
from html.parser import HTMLParser
from pathlib import Path
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.external=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='a' and 'href' in d:self.links.append(d['href'])
        if tag in ('script','link','img'):
            self.external += [v for k,v in attrs if k in ('src','href') and v.startswith(('http:','https:'))]
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);args=p.parse_args();root=args.root
page=sorted(root.glob('*_w8a8_recovery.html'))[-1];body=page.read_text();parser=Links();parser.feed(body)
checks={'filename_seconds':bool(re.match(r'\d{4}-\d{2}-\d{2}_\d{6}_',page.name)),
        'header_seconds':bool(re.search(r'生成时刻：\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',body)),
        'local_links':all((root/x).exists() for x in parser.links if not x.startswith('#')),
        'no_external_dependencies':not parser.external,'no_nan_label':'>nan<' not in body.lower()}
h=json.loads((root/'hardware_cost.json').read_text())
checks['cycle_formula']=all(math.isclose(r['macs']/1536,r['array_ideal_cycles_1536mac']) for r in h['summaries'])
checks['byte_formula']=all(math.isclose(100*(1-r['int8_operand_bytes']/r['a16_reference_operand_bytes']),r['operand_reduction_pct']) for r in h['summaries'])
result={'generated':datetime.datetime.now().isoformat(timespec='seconds'),'html':page.name,'checks':checks,
        'pass':all(checks.values()),'visual_review':'Automated browser file navigation was blocked by tool URL policy; not claimed as visually verified.'}
(root/'artifact_check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
assert result['pass']
