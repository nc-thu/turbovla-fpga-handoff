"""Regenerate a factual HTML from persisted results, including unfinished stages."""
import argparse,collections,datetime,html,json,math
from pathlib import Path

def wilson(k,n,z=2.2414027276):
    if not n:return (0.,1.)
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-h,c+h

def main(root):
    rows=[json.loads(p.read_text()) for p in (root/'episodes').glob('*.json')]
    groups=collections.defaultdict(list)
    for r in rows: groups[(r['mode'],r['suite'],'开发' if r['initial_state_id']<3 else '留出')].append(r)
    summary=[]
    for (mode,suite,split),rr in sorted(groups.items()):
        valid=[r for r in rr if r['status'] in ('success','task_failure')]
        summary.append({'mode':mode,'suite':suite,'split':split,'success':sum(r['success'] for r in valid),
            'valid':len(valid),'exceptions':len(rr)-len(valid),'elapsed_s':sum(r['elapsed_s'] for r in rr)})
    frozen=json.loads((root/'frozen_candidate.json').read_text()) if (root/'frozen_candidate.json').exists() else {}
    paired=[]
    if frozen:
        chosen=frozen['candidate']
        for suite in ('libero_spatial','libero_object','libero_goal','libero_10','all'):
            filtered=[r for r in rows if r['initial_state_id']>=3 and (suite=='all' or r['suite']==suite)]
            base={(r['suite'],r['task'],r['initial_state_id']):r for r in filtered if r['mode']=='fp32' and 'success' in r}
            quant={(r['suite'],r['task'],r['initial_state_id']):r for r in filtered if r['mode']==chosen and 'success' in r}
            counts=collections.Counter()
            for k in base.keys()&quant.keys():
                assert base[k]['initial_state_sha256']==quant[k]['initial_state_sha256']
                counts[(base[k]['success'],quant[k]['success'])]+=1
            n=sum(counts.values());loss=counts[(True,False)];gain=counts[(False,True)]
            if not n:continue
            lg,ug=wilson(gain,n);ll,ul=wilson(loss,n)
            paired.append({'suite':suite,'pairs':n,'both_success':counts[(True,True)],'fp32_only':loss,
                'w8a8_only':gain,'both_failure':counts[(False,False)],'difference':(gain-loss)/n if n else None,
                'ci95_conservative':[lg-ul,ug-ll]})
    replay=[];full_replay={}
    for p in (root/'replay').glob('*.json'):
        d=json.loads(p.read_text())
        if d['n']!=144:continue
        full_replay[d['mode']]=d
        replay.append({k:d[k] for k in ('mode','n','mae','max','elapsed_s')})
    now=datetime.datetime.now();stamp=now.strftime('%Y-%m-%d_%H%M%S')
    complete=(root/'pipeline_complete.json').exists()
    hardware=json.loads((root/'hardware_cost.json').read_text()) if (root/'hardware_cost.json').exists() else {}
    integer=json.loads((root/'integer_audit.json').read_text()) if (root/'integer_audit.json').exists() else []
    fixed=[r for r in replay if r['mode'].endswith('_fixed')]
    fixed_note=''
    if fixed and frozen.get('candidate') in full_replay:
        base_mae=full_replay[frozen['candidate']]['mae']
        fixed_note=f'<p class="note">额外加入定点尺度合并和逐行 INT8 输出重量化后，144 次输入的动作 MAE 从 {base_mae:.6f} 增至 {fixed[0]["mae"]:.6f}，约为原来的 {fixed[0]["mae"]/base_mae:.2f} 倍。这次同时改变了合并与输出量化，不能把增大的误差全部归因于整数乘法。该版本未测成功率；156/160 只属于主软件假量化版本。</p>'
    data={'generated':now.isoformat(timespec='seconds'),'completed':complete,'episodes':summary,'paired':paired,
          'replay':replay,'candidate':frozen,'fixed_point_full_model':fixed or '未验证','rtl':'未做',
          'hardware':hardware,'integer_audit':integer}
    (root/'summary.json').write_text(json.dumps(data,indent=2,ensure_ascii=False))
    labels={'mode':'方案','suite':'任务套件','split':'数据用途','success':'成功次数','valid':'有效回合',
        'exceptions':'程序／环境异常','elapsed_s':'耗时（秒）','n':'规划输入数','mae':'动作 MAE','max':'最大误差',
        'pairs':'配对回合','both_success':'都成功','fp32_only':'仅 FP32 成功','w8a8_only':'仅 W8A8 成功',
        'both_failure':'都失败','difference':'成功率差','ci95_conservative':'95% 区间',
        'op':'矩阵乘类型','calls_per_forward':'每次规划调用数','operand_bits':'乘法操作数',
        'int8_mib':'INT8 操作数 MiB','a16_mib':'A16 参考 MiB','scale_mib':'scale 访问 MiB',
        'partial_mib':'INT32 部分和 MiB','reduction':'操作数字节减少','stage':'实验单元',
        'start':'开始时刻','end':'结束时刻','returncode':'退出码'}
    def display(k,v):
        if v is None:return '未完成'
        if k=='difference' and v is not None:return f'{v*100:+.2f} 个百分点'
        if k=='ci95_conservative':return f'[{v[0]*100:.2f}, {v[1]*100:.2f}] 个百分点'
        if isinstance(v,float):return f'{v:.6g}'
        return str(v)
    def table(rr):
        if not rr:return '<p>尚未完成。</p>'
        keys=list(rr[0]);return '<table><tr>'+''.join('<th>'+html.escape(labels.get(k,k))+'</th>' for k in keys)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(display(k,r.get(k,'')))+'</td>' for k in keys)+'</tr>' for r in rr)+'</table>'
    eligible=[r for r in replay if r['mode'] not in ('fp32','observe','weight_only','activation_only','attention_only') and not r['mode'].endswith('_fixed')]
    best=min(eligible,key=lambda r:r['mae']) if eligible else None
    coarse=full_replay.get('tensor',{}).get('mae')
    opening='实验仍在运行；以下数字只覆盖已经完成的输入和回合。'
    if best and coarse:
        opening+=f' 在 144 次固定规划输入上，{best["mode"]} 的动作 MAE 为 {best["mae"]:.5f}，比全矩阵乘粗粒度方案降低 {100*(1-best["mae"]/coarse):.1f}%。这不是成功率结论。'
    finalpair=next((r for r in paired if r['suite']=='all' and r['pairs']==160),None)
    if finalpair:
        bs=finalpair['both_success']+finalpair['fp32_only'];qs=finalpair['both_success']+finalpair['w8a8_only']
        opening=f'160 对留出回合已经完成：严格 FP32 成功 {bs}/160，{frozen["candidate"]} 成功 {qs}/160，差 {(qs-bs)/160*100:+.2f} 个百分点。'
        opening+=' 观测成功次数已追平。' if qs>=bs else ' 观测成功次数尚未追平。'
        opening+=' 当前区间仍不能排除超过 2 个百分点的损失，不能声称统计等价。' if finalpair['ci95_conservative'][0]<-.02 else ' 区间下界不低于 -2 个百分点，但本轮只覆盖每套两个任务。'
    coverage=[]
    for op,c in full_replay.get('group_32',full_replay.get('token',{})).get('calls',{}).items():
        coverage.append({'op':op,'calls_per_forward':c/144,'operand_bits':'INT8 × INT8'})
    costrows=[{'mode':r['mode'],'int8_mib':r['int8_operand_bytes']/2**20,
        'a16_mib':r['a16_reference_operand_bytes']/2**20,'scale_mib':r['fp32_scale_bytes']/2**20,
        'partial_mib':r['int32_partial_bytes']/2**20,'reduction':str(round(r['operand_reduction_pct'],2))+'%'}
        for r in hardware.get('summaries',[])]
    g32=next((r for r in hardware.get('summaries',[]) if r['mode']=='group_32'),None)
    balance=''
    if g32:
        demand=math.ceil(g32['scale_merge_multiplications']/g32['array_ideal_cycles_1536mac'])
        ratio=g32['merge_cycles_if_24values_per_cycle']/g32['array_ideal_cycles_1536mac']
        balance=f'<p class="note">条件算例：若阵列每拍完成 1536 MAC，而尺度合并每拍只接收 24 个部分和，32 分组的合并拍数约为纯乘加理想拍数的 {ratio:.2f} 倍。要在这个理想上限下跟上阵列，平均至少需每拍处理 {demand} 个部分和。这里未计填充、搬运和系数生成，也没有做资源综合；它说明合并通路需要单独设计，不能直接宣称吞吐翻倍。</p>'
    events=[json.loads(x) for x in (root/'stage_events.jsonl').read_text().splitlines()] if (root/'stage_events.jsonl').exists() else []
    taskmap={(r['suite'],r['task']):r['task_description'] for r in rows if r.get('task_description')}
    taskrows=[{'suite':s,'任务编号':t,'实际指令':v,'留出状态编号':'3–22'} for (s,t),v in sorted(taskmap.items())]
    dots=''
    maxscale=max((r['fp32_scale_bytes']/2**20 for r in hardware.get('summaries',[])),default=1)
    for r in hardware.get('summaries',[]):
        if r['mode'] not in full_replay or r['mode'] not in ('tensor','token','group_128','group_64','group_32'):continue
        err=full_replay[r['mode']]['mae'];x=70+r['fp32_scale_bytes']/2**20/maxscale*650
        y=250-(math.log10(max(err,1e-4))+4)/3*190
        dots+=f'<circle cx="{x}" cy="{y}" r="5" fill="#287e8d"/><text x="{x+7}" y="{y-7}" font-size="11">{r["mode"]}</text>'
    curve=f'<svg viewBox="0 0 850 300"><path d="M70 30 V250 H790" fill="none" stroke="#333"/><text x="80" y="20">动作 MAE（对数坐标）</text><text x="300" y="285">每次规划的 scale 访问量（MiB，逻辑访问）</text>{dots}'
    for value in (.0001,.001,.01,.1):
        y=250-(math.log10(value)+4)/3*190
        curve+=f'<text x="8" y="{y+4}" font-size="12">{value}</text><path d="M70 {y} H790" stroke="#ddd" stroke-dasharray="3 3"/>'
    for fraction in (0,.25,.5,.75,1):
        x=70+650*fraction;curve+=f'<text x="{x}" y="267" text-anchor="middle" font-size="12">{fraction*maxscale:.1f}</text>'
    curve+='</svg>'
    layerpath=root/'layer_comparison.json'
    layers=json.loads(layerpath.read_text())['rows'] if layerpath.exists() else []
    examples=[{'模块':r['module'],'操作':r['op'],'粗 scale 输入归零':f'{r["tensor_a_zero_fraction"]*100:.1f}%',
               '逐 token 输入归零':f'{r["token_a_zero_fraction"]*100:.1f}%',
               '32 分组输入归零':f'{r["group_32_a_zero_fraction"]*100:.1f}%',
               '粗 scale 局部 NRMSE':r['tensor_output_nrmse'],'32 分组局部 NRMSE':r['group_32_output_nrmse']}
              for r in layers[:5]]
    extra=f'''<h2>本页结论</h2><p class="note">{opening}</p>{table(paired)}
      <p>上表只统计两边都完成的留出场景。方案冻结时刻：{frozen.get('frozen_at','尚未冻结')}。不根据留出成绩修改 scale。这里是每套两个固定任务，不是论文四套完整 benchmark。</p>
      <h2>粗 scale 把许多小数值变成了零</h2>{table(examples)}
      <p>每行取该模块／形状第一次观察到的调用，不是全数据集平均。上游量化会改变下一层输入，因此不同方案的这一表不是完全相同输入的单层消融。NRMSE 是局部输出均方根误差除以参考输出均方根，越小越好。完整的逐层数据保留在 layer_comparison.csv。</p>
      <h2>更小的误差用了多少 scale</h2><p>scale 是整数与原始数值之间的换算比例。tensor 表示整个输入张量共用一个比例；token 表示每行单独使用；group_32 表示每 32 个参与求和的输入元素使用一个比例。smooth 是等价通道缩放，mse 是裁剪搜索。它们都不是重新训练。</p>{curve}<p>这图怎么看：越靠下，平均动作误差越小；越靠右，scale 的逻辑访问量越大。这里没有把更小误差换算成成功率，也没有把 scale 访问量当作必须同时驻留的容量。相近的点用下方完整数值表区分。</p>
      <h2>全部矩阵乘检查到了哪里</h2>{table(coverage)}
      <p>Linear 是带固定权重的线性层；QK 和 AV 是注意力中的两个动态矩阵乘。卷积先展开为矩阵。每个调用都把两个乘法操作数映射到有符号 INT8 数值网格。GPU 用 FP32 核模拟这些整数乘积，不代表 V100 正在执行 INT8 加速核。</p>
      <p>Embedding 查表、归一化、Softmax、GELU、bias、残差及分组尺度合并仍使用浮点。Embedding 不属于矩阵乘；本轮不声称模型全部权重或全部算子都已整数化。关闭包装器和只观察输入的版本，在 144 次规划上的输出最大差分别为 {full_replay.get('fp32',{}).get('max','未测')}、{full_replay.get('observe',{}).get('max','未测')}。</p>
      <p>诊断记录在每种模块／形状的首次调用额外计算一次浮点参考矩阵乘，只用于统计误差，不参与动作输出。因此本轮 GPU 耗时包含观察和软件量化开销，不用来声称 INT8 CUDA 核加速。旧方案还量化了 Embedding 查表，新方案明确保留浮点查表；旧、新成功率差不能全部归因于 scale。97.2% 的动作误差降低取自新版内部相同量化范围的粗粒度与 32 分组对照。</p>
      <h2>增加 scale 后，乘法仍是 INT8，但部分和不能直接相加</h2>
      <svg viewBox="0 0 960 150" role="img" aria-label="分组整数乘加和尺度合并"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8Z" fill="#333"/></marker></defs>
      <g fill="#edf3f8" stroke="#333"><rect x="10" y="35" width="200" height="70"/><rect x="265" y="35" width="200" height="70"/><rect x="520" y="35" width="200" height="70"/><rect x="775" y="35" width="175" height="70"/></g>
      <g font-size="16" text-anchor="middle"><text x="110" y="63">沿 K 每 32 个数分组</text><text x="110" y="87">各组单独量化</text><text x="365" y="63">INT8 × INT8</text><text x="365" y="87">得到 INT32 部分和</text><text x="620" y="63">每组乘自己的 scale</text><text x="620" y="87">再合并部分和</text><text x="860" y="75">bias / 下一个算子</text></g>
      <g stroke="#333" stroke-width="2" marker-end="url(#a)"><path d="M210 70 H260"/><path d="M465 70 H515"/><path d="M720 70 H770"/></g></svg>
      <p>这图怎么看：分组缩小了同一 scale 要兼顾的数值范围，误差会减小。但每组的结果单位不同，需要先换到共同尺度。不能把不同组的 INT32 结果直接相加。</p>
      {table(costrows)}<p>以上是每次规划平均的逻辑操作数访问量，不是实测 DDR 流量。重复权重未扣除；部分和可以留在片上，也可以写出再读回。后者额外流量是表中部分和字节数的两倍。A16 参考按静态权重 INT8、动态第二操作数 INT16 计算，不冒充旧 W8A16 实测。</p>
      <p>该表仅包含矩阵乘的操作数访问，不含浮点 Embedding 表、bias、归一化等数据，不能当成整个模型的驻留容量或完整访存量。</p>{balance}<p>24 个 scale 合并通道、1536 MAC/拍等仅作独立条件估算，完整周期仍未知。MSE clipping 版本在软件运行时搜索六个裁剪比例，这个检测开销不免费；若要上硬件，需要固定或专门实现该处理。LUT、DSP、BRAM、功耗和时序本轮未综合。</p>
      <h2>整数乘积和定点合并分别验证</h2><p>已保存 {len(integer)} 个代表性算子输入切片。整数乘积有 {sum(r['max_integer_product_error']!=0 for r in integer)} 个切片与 INT64 黄金模型不一致；定点合并后的最大误差为 {max((r['fixed_output_max_lsb'] for r in integer),default='未测')} 个输出量化单位。这只证明这些切片，不代表整个模型或 RTL 逐位通过。</p>{table(fixed)}
      <p>分组不超过 128 时，单组最坏整数和为 128 × 127² = 2,064,512，小于 FP32 连续精确表示整数的上限 16,777,216。因此在禁止 TF32 的当前路径中，这些分组整数积累加不需要靠浮点近似；随后乘 scale、跨组合并仍是浮点。未分组的长 K 基线不享有这个保证。</p>
      <p>带 fixed 后缀的回放增加了整数 multiplier/shift 合并和 INT8 输出重量化。动态输出 scale 的生成、bias 和非线性仍是浮点。它与主候选不是同一数值路径；主候选成功率不能直接归给这个版本。未跑 fixed 闭环成功率。</p>
      {fixed_note}
      <h2>下一轮硬件优先核对两件事</h2><p>第一，组间部分和应尽量留在片上合并，避免反复写入外存。第二，可在新的开发实验中对不敏感层尝试 64／128 分组，减少 scale 和转换次数；所有矩阵乘仍保持 INT8。当前留出集已经用于检验 32 分组，不能再把它当成新方案的独立测试集。</p>
      <p>本轮没有测量新的 DSP、LUT 或 BRAM 占用。软件精度恢复不代表现有 W8A8 引擎无需修改，也不代表保持 768 DSP 后吞吐一定翻倍。</p>
      <h2>复现文件与实验时间</h2><p>逐回合结果在 episodes/；回放误差、逐层归零率和端点比例在 replay/；整数对拍在 integer_audit.json；硬件计算账在 hardware_cost.csv；版本与输入散列在 provenance.json。原始日志保留在 logs/。</p>
      <p><a href="summary.json">机器可读汇总</a> · <a href="hardware_cost.csv">硬件成本明细</a> · <a href="layer_comparison.csv">逐层误差</a> · <a href="integer_audit.json">整数核对</a> · <a href="validation.json">配对与覆盖核对</a> · <a href="README.md">复现说明</a></p>
      <details><summary>本轮实际测试的八个任务</summary>{table(taskrows)}</details>
      <details><summary>每个实验单元的开始、结束与耗时</summary>{table(events)}</details>
      <pre>python scripts/run_recovery.py --root ROUND --stage replay --modes group_32\npython scripts/run_recovery.py --root ROUND --mode group_32 --suites libero_spatial --start 3 --end 8\npython scripts/integer_audit.py --root ROUND\npython scripts/hardware_cost.py --root ROUND\npython scripts/report.py --root ROUND</pre>'''
    bars=''
    for i,r in enumerate(summary):
        rate=r['success']/r['valid'] if r['valid'] else 0;y=30+i*27
        bars+=f'<text x="5" y="{y+15}" font-size="12">{html.escape(r["mode"]+" / "+r["suite"]+" / "+r["split"])}</text><rect x="360" y="{y}" width="{rate*350}" height="18" fill="#4477aa"/><text x="720" y="{y+15}" font-size="12">{r["success"]}/{r["valid"]}</text>'
    page=f'''<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TurboVLA W8A8 精度恢复实验</title><style>body{{max-width:1100px;margin:30px auto;padding:20px;font:16px/1.7 Arial,"Microsoft YaHei",sans-serif;color:#222}}table{{border-collapse:collapse;font-size:13px;display:block;overflow:auto}}td,th{{border:1px solid #ddd;padding:6px}}svg{{width:100%;height:auto}}.note{{background:#fff2d4;padding:16px}}</style><h1>TurboVLA W8A8 精度恢复实验</h1><p>生成时刻：{now:%Y-%m-%d %H:%M:%S}。状态：{'软件评测完成' if complete else '实验进行中，结果随逐回合文件更新'}。</p><p class="note">本页成功率属于软件量化数值实验。全部矩阵乘的 INT8 操作数由底层包装器检查；非线性保留浮点。完整定点后处理和 RTL 尚未验证。</p><h2>旧方案只用了每个张量一个尺度</h2><p>旧 24 回合 FP32 为 22/24，W8A8 为 7/24。旧 FP32 的视觉编码实际使用 BF16 autocast。本轮另建严格 FP32 参考，因此不能把两种参考混成一个结果。</p><h2>每套任务成功了多少</h2><svg viewBox="0 0 800 {max(100,60+len(summary)*27)}">{bars}</svg><p>这图怎么看：横条长度是成功率，右侧数字是成功次数／有效回合数。开发场景用于选方案；留出场景只验证冻结后的方案。</p>{table(summary)}<h2>相同输入的动作误差</h2>{table(sorted(replay,key=lambda r:r['mae']))}<p>动作 MAE 用于选候选，不代表任务成功率。不同方案运行完整模型。</p><h2>留出场景的配对比较</h2>{table(paired)}<p>置信区间用两个不一致结果概率的 97.5% Wilson 区间合成，保守覆盖约 95%；不足以排除 2 个百分点损失时，不声称与 FP32 等价。</p><h2>硬件需要付出的代价</h2><p>K 维分组保持 INT8×INT8 乘法，但每组需要独立尺度和部分和转换。scale 存储、检测和部分和相加的成本仍须核算，不能只按激活字节减半推断整机加速。</p><h2>待完成</h2><p>逐层量化误差、完整定点 scale 合并验证、硬件周期分析以及完整四套 benchmark（40 个任务）尚未交付。本轮只覆盖每套固定两个任务。</p></html>'''
    page=page.replace('<h2>旧方案只用了每个张量一个尺度</h2>',extra+'<h2>旧方案的复现边界</h2>')
    page=page.replace('旧 24 回合 FP32 为 22/24，W8A8 为 7/24。','历史 24 回合 FP32 为 22/24，W8A8 为 7/24；本轮旧方案复现分别为 22/24 和 6/24。差异出现在 Spatial task 1。原因尚未确定，不写成完全复现。')
    page=page.replace('逐层量化误差、完整定点 scale 合并验证、硬件周期分析以及完整四套 benchmark（40 个任务）尚未交付。','完整整数非线性、RTL 实现、硬件实际周期与完整四套 benchmark（40 个任务）未做。')
    page=page.replace('动作 MAE 用于选候选，不代表任务成功率。不同方案运行完整模型。','动作 MAE 对每次完整 12×7 归一化动作计算，数值没有弧度或米的单位，不能当成关节角误差。它用于选候选，不代表任务成功率。不同方案运行完整模型。')
    page=page.replace('<h2>留出场景的配对比较</h2>'+table(paired),'<h2>配对区间怎么算</h2>')
    out=root/(stamp+'_w8a8_recovery.html');out.write_text(page,encoding='utf-8')
    print(out)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);main(p.parse_args().root)
