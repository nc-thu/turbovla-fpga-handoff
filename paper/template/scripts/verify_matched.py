from pathlib import Path
import re,json,hashlib,datetime
P=Path(__file__).resolve().parents[1];data={};manifest=[]
for group in ['matched','matched48','matched48_pa']:
 data[group]={}
 for var in ['base','overlap','read2','core2']:
  p=P/'data'/group/var/'run.log';t=p.read_text();assert 'MATCHED ALL PASS' in t and 'FAIL' not in t,(group,var)
  rows={}
  for m in re.finditer(r'\[(shortK|mediumK|deepK|narrowN)\] cycles=(\d+) mac=(\d+) m=(\d+) n=(\d+) nl=(\d+) j0=(\d+) k=(\d+)',t):
   case,cycles,counter,M,N,NL,J,K=m.groups();rows[case]={'cycles':int(cycles),'effective_mac':int(M)*int(NL)*int(K),'raw_mac_counter':int(counter),'m':int(M),'n':int(N),'n_loc':int(NL),'k':int(K)}
  assert len(rows)==4;data[group][var]=rows;manifest.append({'file':str(p.relative_to(P)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for var in data['matched48']:
 assert data['matched48'][var]==data['matched48_pa'][var],var
report={'checked_at':datetime.datetime.now().isoformat(timespec='seconds'),'passed_pairs':48,'full_width_original_pairs':16,'full_width_preadder_pairs':16,'preliminary_4column_pairs':16,'preadder_cycle_change':0,'raw_counter_note':'Hardware MAC counter includes padded lanes; use M*n_loc*K for effective work','data':data,'logs':manifest}
(P/'data/matched_audit.json').write_text(json.dumps(report,indent=2),encoding='utf8')
rec=json.loads((P/'data/figure_records.json').read_text(encoding='utf8'))
for var,rows in data['matched48_pa'].items():
 for case,row in rows.items():
  d={k:None for k in rec['records'][0]};path=P/'data/matched48_pa'/var/'run.log';d.update(model='deterministic INT8 GEMM',workload=case,configuration='PCOLS48_'+var+'_preadder_M32',effective_mac=row['effective_mac'],cycles=row['cycles'],evidence='RTL bit-exact simulation; preadder substitution',raw_file=str(path.relative_to(P)),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest());rec['records'].append(d)
(P/'data/figure_records.json').write_text(json.dumps(rec,indent=2),encoding='utf8')
print('48 cases passed; 16 full-width preadder cases preserve exact cycle counts')
