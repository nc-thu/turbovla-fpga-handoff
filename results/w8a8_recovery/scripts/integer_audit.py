"""Actual-operand INT64 products and integer scale conversion, CPU only."""
import argparse,json,math
import torch
from quant_core import QuantMode

def main(root):
    results=[]
    for path in sorted((root/'integer_fixtures').glob('*.pt')):
        for op,r in torch.load(path,weights_only=False).items():
            m=QuantMode(scheme=r['scheme'],clipping=r['clipping'])
            a,b=r['a'],r['b'];k=a.shape[-1];g=r['group'] or k
            parts=[];scales=[];errors=[]
            for lo in range(0,k,g):
                qa,sa=m.grid(a[:,lo:lo+g],m.scheme=='tensor')
                qb,sb=m.grid(b[lo:lo+g,:].T)
                z=qa.to(torch.int64)@qb.to(torch.int64).T
                errors.append(float(((qa@qb.T).double()-z.double()).abs().max()))
                parts.append(z);scales.append((sa*sb.T).double())
            y=sum(z.double()*s for z,s in zip(parts,scales))
            out_scale=max(float(y.abs().max())/127,1e-12)
            reference=(y/out_scale).round().clamp(-127,127).to(torch.int64)
            # Per-output multiplier, shared shift, wide integer accumulation.
            ratios=[s/out_scale for s in scales]
            largest=max(float(x.abs().max()) for x in ratios)
            maxacc=sum(int(z.abs().max()) for z in parts)
            shift=min(30,max(0,math.floor(math.log2((2**61)/max(1,largest*maxacc)))))
            merged=sum(z*(s*(2**shift)).round().to(torch.int64) for z,s in zip(parts,ratios))
            # Round ties to even entirely in integer arithmetic.
            mag=merged.abs();div=2**shift;q=mag//div;rem=mag%div
            q=q+((rem>div//2)|((rem==div//2)&((q&1)==1))).to(torch.int64) if shift else q
            fixed=(q*merged.sign()).clamp(-127,127)
            results.append({'mode':path.stem,'op':op,'module':r['module'],'k':k,'group':g,
                'max_integer_product_error':max(errors),'fixed_output_max_lsb':int((fixed-reference).abs().max()),
                'merge_shift':shift,'scope':'representative slices; not full model fixed point'})
    (root/'integer_audit.json').write_text(json.dumps(results,indent=2))
    print(json.dumps({'fixtures':len(results),'product_errors':sum(r['max_integer_product_error']!=0 for r in results),
                      'fixed_max_lsb':max((r['fixed_output_max_lsb'] for r in results),default=None)}))

if __name__=='__main__':
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);main(p.parse_args().root)
