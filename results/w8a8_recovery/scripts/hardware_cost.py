"""Operand/scale traffic accounting, not a claim of implemented FPGA timing."""
import argparse,csv,datetime,json,math
from pathlib import Path

def main(root):
    rows=[];summaries=[]
    for path in sorted((root/'replay').glob('*.json')):
        d=json.loads(path.read_text())
        if d['n']!=144 or d['mode'].endswith('_fixed') or d['mode'] in ('observe','fp32','weight_only','activation_only','attention_only'):continue
        rr=[]
        for key,r in d['operators'].items():
            a,b=r['a_shape'],r['b_shape'];m,k,n=a[-2],a[-1],b[-1]
            batches=math.prod(__import__('numpy').broadcast_shapes(tuple(a[:-2]),tuple(b[:-2])))
            groups=math.ceil(k/r['group_k']);outputs=batches*m*n
            ab,bb=math.prod(a),math.prod(b)
            # No claim of unique DDR transactions: this counts logical operand
            # visits, including repeated weights, and exposes that assumption.
            base_bytes=2*ab+(bb if r['weight'] else 2*bb)
            operand_bytes=ab+bb
            partial=r['partial_values_per_call']
            scaled=r['scale_values_per_call']*4
            c={'mode':d['mode'],'module':r['module'],'op':r['op'],'calls':r['calls'],
               'm':m,'n':n,'k':k,'batch':batches,'groups':groups,
               'int8_operand_bytes':operand_bytes,'a16_reference_operand_bytes':base_bytes,
               'fp32_scale_bytes':scaled,'int32_partial_bytes':partial*4,
               'spill_roundtrip_bytes':partial*8,'scale_merge_multiplications':partial,
               'scale_pair_multiplications':partial,
               'scale_merge_additions':outputs*max(groups-1,0),
               'dynamic_absmax_elements':ab+(0 if r['weight'] else bb),
               'dynamic_clipping_trial_elements':6*(ab+(0 if r['weight'] else bb)) if d['mode'].endswith('_mse') else 0,
               'macs':r['macs'],'array_ideal_cycles_1536mac':r['macs']/1536,
               'merge_cycles_if_24values_per_cycle':partial/24,
               'weight_static':r['weight']}
            rr.append(c);rows.append(c)
        sums={k:sum(r[k]*r['calls'] for r in rr)/d['n'] for k in
              ('int8_operand_bytes','a16_reference_operand_bytes','fp32_scale_bytes','int32_partial_bytes',
               'spill_roundtrip_bytes','scale_merge_multiplications','scale_merge_additions','dynamic_absmax_elements',
               'scale_pair_multiplications',
               'dynamic_clipping_trial_elements',
               'macs','array_ideal_cycles_1536mac','merge_cycles_if_24values_per_cycle')}
        sums['mode']=d['mode'];sums['operand_reduction_pct']=100*(1-sums['int8_operand_bytes']/sums['a16_reference_operand_bytes'])
        summaries.append(sums)
    if rows:
        with (root/'hardware_cost.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (root/'hardware_cost.json').write_text(json.dumps({'generated':datetime.datetime.now().isoformat(timespec='seconds'),
       'scope':'Mean per planning call over 144 development observations. Logical operand visits, NOT measured DDR traffic.',
       'assumptions':['A16 comparison uses INT16 A, INT8 static weights, INT16 dynamic second operand.',
         '4-byte scales and INT32 partials. Partial spill is optional worst traffic, not added if kept on chip.',
         '1536 MAC/cycle and 24 merge values/cycle are independent hypothetical rates; no RTL timing measured.',
         'scale_merge_multiplications counts partial times combined scale; computing A_scale times B_scale is separately counted.',
         'No nonlinear, DMA arbitration, quantization division, or scheduling cycle omitted as free; full cycles unknown.',
         'MSE clipping search is dynamic in this software experiment, not a frozen static hardware threshold.',
         'Fixed-output validation variant is excluded; its extra dynamic output-scale pass and INT64 conversion are not costed here.',
         'Scales for padded groups included; operand bytes exclude padding and intermediates.'],
       'summaries':summaries},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);main(p.parse_args().root)
