import sys, os, difflib
from collections import Counter
sys.path.insert(0, '/tmp/compiler_v6/sw')
import golden_interp as gi
NCW = 10

def load(build):
    sdir = os.path.join(build, 'segments')
    out = []
    for s in sorted(f for f in os.listdir(sdir) if f.startswith('seg_')):
        seq = gi.load_seq(os.path.join(sdir, s))
        ops, ys, pc = Counter(), set(), 0
        while pc < len(seq):
            f = gi.decode(seq[pc]); op = f['op']
            if op == 15: ops[15] += 1; break
            ops[op] += 1
            if op in (0,1,2): ys.add(f['y_base']); pc += NCW
            else:
                if op in (5,6): ys.add(f['y_base'])
                pc += 1
        out.append((s, '%s|%s' % (tuple(sorted(ops.items())), tuple(sorted(ys)))))
    return out

a = load(sys.argv[1]); b = load(sys.argv[2])
sm = difflib.SequenceMatcher(None, [x[1] for x in a], [x[1] for x in b], autojunk=False)
nblocks = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal': continue
    nblocks += 1
    if nblocks <= 8:
        print(tag, 'v6[%d:%d]' % (i1,i2), [a[k][0] for k in range(i1,min(i2,i1+4))],
              '-> v7[%d:%d]' % (j1,j2), [b[k][0] for k in range(j1,min(j2,j1+4))])
        if i2-i1 <= 3 and j2-j1 <= 3:
            for k in range(i1,i2): print('   v6:', a[k][1][:150])
            for k in range(j1,j2): print('   v7:', b[k][1][:150])
print('total change blocks:', nblocks)
