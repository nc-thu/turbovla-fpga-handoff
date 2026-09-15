import argparse,csv,json
from pathlib import Path

def main(root):
    sources={n:json.loads((root/'replay'/(n+'.json')).read_text())['operators'] for n in ('tensor','token','group_32')}
    rows=[]
    for key,r in sources['tensor'].items():
        row={'module':r['module'],'op':r['op'],'shape':str(r['a_shape'])+' x '+str(r['b_shape'])}
        for name,operators in sources.items():
            stats=operators.get(key,{}).get('first_call_stats',{})
            for k in ('a_zero_fraction','b_zero_fraction','a_endpoint_fraction','b_endpoint_fraction','output_nrmse','output_mae','output_max'):
                row[name+'_'+k]=stats.get(k)
        rows.append(row)
    rows.sort(key=lambda r:r['tensor_output_nrmse'] or 0,reverse=True)
    with (root/'layer_comparison.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (root/'layer_comparison.json').write_text(json.dumps({'scope':'First observed call of each module/op/shape; current input differs after upstream quantization. Not a dataset-wide saturation average.',
        'rows':rows},indent=2))
    print(json.dumps(rows[:3],indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);main(p.parse_args().root)
