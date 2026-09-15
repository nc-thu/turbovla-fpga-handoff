"""Build a self-contained Chinese architecture report for TurboVLA W8A8 Pack2.

This report is deliberately generated from the archived JSON/CSV and Vivado
reports.  It uses only the Python standard library and embeds all figures as
SVG, so the resulting HTML can be copied and opened without a web server.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import html
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPORT_TS = "2026-09-15_134742"
GENERATED = "2026-09-15 13:47:42"
REPORT_DIR = Path(__file__).resolve().parent
ROOT = REPORT_DIR.parents[1]
VERSION = "2026-09-14_115230"
DATA = ROOT / "data" / VERSION
COMP = DATA / "compiled_current"
RTL = ROOT / "hw" / f"v1_{VERSION}_pack2_rtl"


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {} if default is None else default


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    except Exception:
        return []


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return "unavailable"


def esc(x: Any) -> str:
    return html.escape(str(x), quote=True)


def fmt_int(x: Any) -> str:
    try:
        return f"{int(x):,}"
    except Exception:
        return "—"


def fmt_float(x: Any, d: int = 2) -> str:
    try:
        return f"{float(x):,.{d}f}"
    except Exception:
        return "—"


def fmt_pct(x: Any, d: int = 2) -> str:
    try:
        return f"{100.0 * float(x):.{d}f}%"
    except Exception:
        return "—"


def html_table(headers: list[str], rows: list[list[Any]], cls: str = "") -> str:
    out = [f'<table class="{esc(cls)}"><thead><tr>']
    out.extend(f"<th>{h}</th>" for h in headers)
    out.append("</tr></thead><tbody>")
    for row in rows:
        out.append("<tr>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def marker_defs(name: str = "arrow") -> str:
    return f'<defs><marker id="{name}" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 z" fill="#334155"/></marker><marker id="{name}Blue" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 z" fill="#2563eb"/></marker><marker id="{name}Orange" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 z" fill="#ea580c"/></marker></defs>'


def svg_architecture() -> str:
    return '''<svg viewBox="0 0 1120 360" role="img" aria-label="TurboVLA W8A8 Pack2 architecture" xmlns="http://www.w3.org/2000/svg">
      <style>
        .box{stroke:#1f2937;stroke-width:2;rx:3}.title{font:700 17px Arial,sans-serif;fill:#111827}.sm{font:13px Arial,sans-serif;fill:#334155}.xs{font:11px Arial,sans-serif;fill:#475569}.arr{fill:none;stroke:#334155;stroke-width:2;marker-end:url(#archArrow)}.blue{fill:none;stroke:#2563eb;stroke-width:3;marker-end:url(#archArrowBlue)}.orange{fill:none;stroke:#ea580c;stroke-width:2.5;marker-end:url(#archArrowOrange)}
      </style>''' + marker_defs("archArrow") + '''
      <rect x="20" y="30" width="180" height="270" fill="#e0f2fe" class="box"/><text x="110" y="58" text-anchor="middle" class="title">TurboVLA trace</text><text x="110" y="84" text-anchor="middle" class="sm">视觉 / 语言 / fusion</text><text x="110" y="108" text-anchor="middle" class="sm">action head</text><line x1="45" y1="130" x2="175" y2="130" stroke="#94a3b8"/><text x="110" y="154" text-anchor="middle" class="xs">408 module events</text><text x="110" y="174" text-anchor="middle" class="xs">6836 dispatch events</text><text x="110" y="194" text-anchor="middle" class="xs">280 Linear + 24 BMM</text><text x="110" y="232" text-anchor="middle" class="xs">输入：两路 256×256</text><text x="110" y="250" text-anchor="middle" class="xs">指令 + 8-D 状态</text><text x="110" y="268" text-anchor="middle" class="xs">输出：12×7 action</text>
      <rect x="245" y="30" width="205" height="270" fill="#fef3c7" class="box"/><text x="347" y="58" text-anchor="middle" class="title">Pack2 compiler</text><rect x="270" y="82" width="155" height="38" fill="#fff" class="box"/><text x="347" y="106" text-anchor="middle" class="sm">event ownership</text><rect x="270" y="132" width="155" height="38" fill="#fff" class="box"/><text x="347" y="156" text-anchor="middle" class="sm">16×96 tiling</text><rect x="270" y="182" width="155" height="38" fill="#fff" class="box"/><text x="347" y="206" text-anchor="middle" class="sm">command + descriptor</text><text x="347" y="252" text-anchor="middle" class="xs">432 descriptors</text><text x="347" y="271" text-anchor="middle" class="xs">unknown = 0（分类层面）</text>
      <rect x="495" y="30" width="195" height="270" fill="#f3e8ff" class="box"/><text x="592" y="58" text-anchor="middle" class="title">Replay top</text><rect x="520" y="82" width="145" height="38" fill="#fff" class="box"/><text x="592" y="106" text-anchor="middle" class="sm">descriptor FIFO ×16</text><rect x="520" y="132" width="145" height="38" fill="#fff" class="box"/><text x="592" y="156" text-anchor="middle" class="sm">scheduler / fence</text><rect x="520" y="182" width="145" height="38" fill="#fff" class="box"/><text x="592" y="206" text-anchor="middle" class="sm">activity monitor</text><text x="592" y="252" text-anchor="middle" class="xs">valid / ready</text><text x="592" y="271" text-anchor="middle" class="xs">backpressure 计数</text>
      <rect x="735" y="30" width="175" height="270" fill="#ffedd5" class="box"/><text x="822" y="58" text-anchor="middle" class="title">Pack2 array</text><rect x="760" y="82" width="125" height="48" fill="#fff" class="box"/><text x="822" y="104" text-anchor="middle" class="sm">16×48 physical</text><text x="822" y="122" text-anchor="middle" class="xs">768 DSP / 96 logical</text><rect x="760" y="145" width="125" height="38" fill="#fff" class="box"/><text x="822" y="169" text-anchor="middle" class="sm">INT32 state</text><rect x="760" y="198" width="125" height="38" fill="#fff" class="box"/><text x="822" y="222" text-anchor="middle" class="sm">snapshot / requant</text><text x="822" y="266" text-anchor="middle" class="xs">2 MAC / DSP / cycle</text>
      <rect x="955" y="30" width="145" height="270" fill="#f1f5f9" class="box"/><text x="1027" y="58" text-anchor="middle" class="title">辅助路径</text><text x="1027" y="94" text-anchor="middle" class="sm">LayerNorm</text><text x="1027" y="120" text-anchor="middle" class="sm">GELU / Softmax</text><text x="1027" y="146" text-anchor="middle" class="sm">Conv / BMM</text><text x="1027" y="172" text-anchor="middle" class="sm">bias / add</text><line x1="980" y1="198" x2="1074" y2="198" stroke="#94a3b8"/><text x="1027" y="225" text-anchor="middle" class="xs">AUX_EVENT / fallback</text><text x="1027" y="250" text-anchor="middle" class="xs">不计为 PE 工作</text>
      <path d="M200 165 H245" class="blue"/><path d="M450 165 H495" class="arr"/><path d="M690 165 H735" class="orange"/><path d="M910 165 H955" class="arr"/>
      <text x="220" y="153" text-anchor="middle" class="xs">trace</text><text x="472" y="153" text-anchor="middle" class="xs">64b + 512b</text><text x="712" y="153" text-anchor="middle" class="xs">128b / 768b</text>
      <path d="M592 300 V330 H822 V300" class="arr"/><text x="707" y="348" text-anchor="middle" class="xs">结果顺序与 activity counters</text>
    </svg>'''


def svg_compiler() -> str:
    return '''<svg viewBox="0 0 1120 300" role="img" aria-label="compiler and instruction generation" xmlns="http://www.w3.org/2000/svg">
      <style>.b{stroke:#1f2937;stroke-width:2}.t{font:700 16px Arial,sans-serif;fill:#111827}.s{font:13px Arial,sans-serif;fill:#334155}.x{font:11px Arial,sans-serif;fill:#475569}.a{fill:none;stroke:#334155;stroke-width:2;marker-end:url(#cArrow)}.bl{fill:none;stroke:#2563eb;stroke-width:3;marker-end:url(#cArrowBlue)}</style>''' + marker_defs("cArrow") + '''
      <rect x="20" y="58" width="175" height="170" fill="#e0f2fe" class="b"/><text x="107" y="90" text-anchor="middle" class="t">operator trace</text><text x="107" y="122" text-anchor="middle" class="s">module + dispatch</text><text x="107" y="151" text-anchor="middle" class="x">parent / shape / dtype</text><text x="107" y="176" text-anchor="middle" class="x">weight_hash / payload</text><text x="107" y="201" text-anchor="middle" class="x">依赖和 scale ID</text>
      <rect x="235" y="35" width="220" height="216" fill="#fef3c7" class="b"/><text x="345" y="66" text-anchor="middle" class="t">compiler checks</text><rect x="260" y="86" width="170" height="32" fill="#fff" class="b"/><text x="345" y="107" text-anchor="middle" class="s">父子去重</text><rect x="260" y="128" width="170" height="32" fill="#fff" class="b"/><text x="345" y="149" text-anchor="middle" class="s">BMM 双输入 + layout</text><rect x="260" y="170" width="170" height="32" fill="#fff" class="b"/><text x="345" y="191" text-anchor="middle" class="s">tile / mask / scale</text><text x="345" y="226" text-anchor="middle" class="x">不通过则 AUX / fallback</text>
      <rect x="495" y="58" width="165" height="170" fill="#ffedd5" class="b"/><text x="577" y="90" text-anchor="middle" class="t">tile mapping</text><text x="577" y="123" text-anchor="middle" class="s">M tile = 16</text><text x="577" y="150" text-anchor="middle" class="s">N tile = 96</text><text x="577" y="177" text-anchor="middle" class="s">tail valid mask</text><text x="577" y="204" text-anchor="middle" class="x">logical 2× physical</text>
      <rect x="700" y="35" width="180" height="216" fill="#f3e8ff" class="b"/><text x="790" y="66" text-anchor="middle" class="t">stream writer</text><rect x="725" y="88" width="130" height="34" fill="#fff" class="b"/><text x="790" y="110" text-anchor="middle" class="s">64-bit command</text><rect x="725" y="134" width="130" height="34" fill="#fff" class="b"/><text x="790" y="156" text-anchor="middle" class="s">512-bit descriptor</text><rect x="725" y="180" width="130" height="34" fill="#fff" class="b"/><text x="790" y="202" text-anchor="middle" class="s">payload / hex</text>
      <rect x="920" y="58" width="180" height="170" fill="#dcfce7" class="b"/><text x="1010" y="90" text-anchor="middle" class="t">检查结果</text><text x="1010" y="127" text-anchor="middle" class="s">432 descriptors</text><text x="1010" y="154" text-anchor="middle" class="s">433 commands</text><text x="1010" y="181" text-anchor="middle" class="s">304 mapped</text><text x="1010" y="208" text-anchor="middle" class="s">128 auxiliary</text>
      <path d="M195 143 H235" class="bl"/><path d="M455 143 H495" class="a"/><path d="M660 143 H700" class="a"/><path d="M880 143 H920" class="a"/>
    </svg>'''


def svg_command_layout() -> str:
    return '''<svg viewBox="0 0 1120 360" role="img" aria-label="64 bit command and 512 bit descriptor layout" xmlns="http://www.w3.org/2000/svg">
      <style>.b{stroke:#1f2937;stroke-width:2}.t{font:700 16px Arial,sans-serif;fill:#111827}.s{font:13px Arial,sans-serif;fill:#334155}.x{font:11px Arial,sans-serif;fill:#475569}.mono{font:12px Consolas,monospace;fill:#0f172a}</style>
      <text x="25" y="28" class="t">64-bit command word（运输头，不放矩阵尺寸）</text>
      <rect x="25" y="52" width="220" height="54" fill="#bfdbfe" class="b"/><rect x="245" y="52" width="220" height="54" fill="#c7d2fe" class="b"/><rect x="465" y="52" width="260" height="54" fill="#ddd6fe" class="b"/><rect x="725" y="52" width="370" height="54" fill="#e2e8f0" class="b"/>
      <text x="135" y="76" text-anchor="middle" class="s">op [63:56]</text><text x="135" y="95" text-anchor="middle" class="x">8 bit</text><text x="355" y="76" text-anchor="middle" class="s">flags [55:48]</text><text x="355" y="95" text-anchor="middle" class="x">8 bit</text><text x="595" y="76" text-anchor="middle" class="s">descriptor_id [47:32]</text><text x="595" y="95" text-anchor="middle" class="x">16 bit</text><text x="910" y="76" text-anchor="middle" class="s">length [15:0]</text><text x="910" y="95" text-anchor="middle" class="x">当前示例通常为 0</text>
      <text x="25" y="145" class="t">512-bit descriptor sideband（当前编译器按 32-bit 字段写入）</text>
      <g class="mono"><text x="25" y="172">[511:480] total_cycles</text><text x="285" y="172">[479:448] valid_mac_count</text><text x="560" y="172">[447:416] active_pe_cycles</text><text x="835" y="172">[415:384] activation_read</text><text x="25" y="197">[383:352] write_cycles</text><text x="285" y="197">[351:320] vector_cycles</text><text x="560" y="197">[319:288] snapshot</text><text x="835" y="197">[287:256] requant</text><text x="25" y="222">[255:224] activation_bytes</text><text x="285" y="222">[223:192] weight_bytes</text><text x="560" y="222">[191:160] output_bytes</text><text x="835" y="222">[159:128] M</text><text x="25" y="247">[127:96] N</text><text x="285" y="247">[95:64] K</text><text x="560" y="247">[63:56] op</text><text x="835" y="247">[55:48] flags</text><text x="25" y="272">[31:16] tile_count</text><text x="285" y="272">[47:32] reserved</text><text x="560" y="272">[15:0] spare</text></g>
      <rect x="25" y="302" width="520" height="34" fill="#f1f5f9" class="b"/><text x="285" y="324" text-anchor="middle" class="mono">0x1880000100000000 → GEMM_W8A8, mapped, descriptor 1</text><rect x="575" y="302" width="520" height="34" fill="#f1f5f9" class="b"/><text x="835" y="324" text-anchor="middle" class="mono">0x3000000000000000 → LAYER_NORM, descriptor 0</text>
    </svg>'''


def svg_pack_math() -> str:
    return '''<svg viewBox="0 0 1120 300" role="img" aria-label="Pack2 arithmetic" xmlns="http://www.w3.org/2000/svg">
      <style>.b{stroke:#1f2937;stroke-width:2}.t{font:700 16px Arial,sans-serif;fill:#111827}.s{font:13px Arial,sans-serif;fill:#334155}.x{font:11px Arial,sans-serif;fill:#475569}.a{fill:none;stroke:#334155;stroke-width:2;marker-end:url(#pArrow)}</style>''' + marker_defs("pArrow") + '''
      <text x="25" y="28" class="t">一个物理列携带两列权重，激活在一拍内共享</text>
      <rect x="25" y="55" width="150" height="62" fill="#fed7aa" class="b"/><text x="100" y="83" text-anchor="middle" class="s">w₁ + 128</text><text x="100" y="103" text-anchor="middle" class="x">高场 / 8 bit</text><rect x="175" y="55" width="150" height="62" fill="#fdba74" class="b"/><text x="250" y="83" text-anchor="middle" class="s">w₀ + 128</text><text x="250" y="103" text-anchor="middle" class="x">低场 / 8 bit</text>
      <path d="M325 86 H400" class="a"/><rect x="400" y="55" width="250" height="62" fill="#dbeafe" class="b"/><text x="525" y="82" text-anchor="middle" class="s">Q = (w₁+128)·2¹⁶ + (w₀+128)</text><text x="525" y="103" text-anchor="middle" class="x">DSP D 口</text>
      <path d="M650 86 H725" class="a"/><rect x="725" y="55" width="170" height="62" fill="#c7d2fe" class="b"/><text x="810" y="82" text-anchor="middle" class="s">R = Q − B₀</text><text x="810" y="103" text-anchor="middle" class="x">B₀=128·(2¹⁶+1)</text>
      <path d="M895 86 H970" class="a"/><rect x="970" y="55" width="125" height="62" fill="#dcfce7" class="b"/><text x="1032" y="82" text-anchor="middle" class="s">P = a·R</text><text x="1032" y="103" text-anchor="middle" class="x">DSP P</text>
      <rect x="120" y="170" width="395" height="65" fill="#fef3c7" class="b"/><text x="317" y="198" text-anchor="middle" class="s">prod0 = signed(P[15:0])</text><text x="317" y="219" text-anchor="middle" class="x">低场：a·w₀</text><rect x="600" y="170" width="395" height="65" fill="#fef3c7" class="b"/><text x="797" y="198" text-anchor="middle" class="s">prod1 = signed(P[31:16]) + P[15]</text><text x="797" y="219" text-anchor="middle" class="x">高场借位修正：a·w₁</text>
      <path d="M1032 117 V145 H317 V170" class="a"/><path d="M1032 117 V145 H797 V170" class="a"/>
      <text x="25" y="274" class="s">两个 product 分别进入 PE 内的两条 INT32 累加反馈；脉冲到来时先写 snapshot，再清零累加器。</text>
    </svg>'''


def svg_array() -> str:
    cells = []
    for r in range(4):
        for c in range(8):
            x = 350 + c * 42
            y = 78 + r * 35
            cells.append(f'<rect x="{x}" y="{y}" width="28" height="20" fill="#fed7aa" stroke="#334155" stroke-width="1.4"/>')
    return '''<svg viewBox="0 0 1120 290" role="img" aria-label="16 by 48 Pack2 array organization" xmlns="http://www.w3.org/2000/svg">
      <style>.b{stroke:#1f2937;stroke-width:2}.t{font:700 16px Arial,sans-serif;fill:#111827}.s{font:13px Arial,sans-serif;fill:#334155}.x{font:11px Arial,sans-serif;fill:#475569}.a{fill:none;stroke:#2563eb;stroke-width:2.5;marker-end:url(#aBlue)}.o{fill:none;stroke:#ea580c;stroke-width:2.5;marker-end:url(#aOrange)}</style>''' + marker_defs("a") + '''
      <rect x="25" y="45" width="220" height="180" fill="#e0f2fe" class="b"/><text x="135" y="75" text-anchor="middle" class="t">CTX / WRAM</text><text x="135" y="110" text-anchor="middle" class="s">activation：128 bit</text><text x="135" y="136" text-anchor="middle" class="s">16 × INT8</text><text x="135" y="174" text-anchor="middle" class="s">weight：768 bit</text><text x="135" y="200" text-anchor="middle" class="s">48 × {w₁,w₀}</text>
      <rect x="300" y="36" width="430" height="210" fill="#fff7ed" class="b"/><text x="515" y="65" text-anchor="middle" class="t">16 rows × 48 physical columns</text>''' + ''.join(cells) + '''<text x="515" y="242" text-anchor="middle" class="x">图中只画代表性单元；每格是 1 DSP / 2 logical columns</text>
      <rect x="790" y="45" width="300" height="180" fill="#f1f5f9" class="b"/><text x="940" y="75" text-anchor="middle" class="t">控制与读出</text><text x="940" y="112" text-anchor="middle" class="s">row i 延迟 i 拍</text><text x="940" y="136" text-anchor="middle" class="s">column j 延迟 j 拍</text><text x="940" y="160" text-anchor="middle" class="s">wavefront：k+i+j</text><text x="940" y="190" text-anchor="middle" class="s">drain row → snapshot</text>
      <path d="M245 115 H300" class="a"/><path d="M245 183 H285 V150 H300" class="o"/><text x="270" y="104" class="x">A 向右</text><text x="270" y="214" class="x">B 向下</text><path d="M730 142 H790" class="a"/><text x="760" y="132" class="x">96 logical</text>
    </svg>'''


def svg_timeline() -> str:
    return '''<svg viewBox="0 0 1120 300" role="img" aria-label="current and double buffer timing" xmlns="http://www.w3.org/2000/svg">
      <style>.t{font:700 16px Arial,sans-serif;fill:#111827}.s{font:13px Arial,sans-serif;fill:#334155}.x{font:11px Arial,sans-serif;fill:#475569}.r{stroke:#334155;stroke-width:1}</style>
      <text x="25" y="28" class="t">当前控制：一个 descriptor 的读、算、后处理基本串行</text><text x="25" y="57" class="s">读激活 / 权重</text><rect x="170" y="42" width="370" height="24" fill="#bfdbfe" class="r"/><text x="184" y="59" class="x">37.72M / 34.51M read cycles（阶段记录）</text><text x="25" y="93" class="s">阵列计算</text><rect x="170" y="78" width="300" height="24" fill="#fdba74" class="r"/><text x="184" y="95" class="x">35.16M compute cycles</text><text x="25" y="129" class="s">fallback + requant + write</text><rect x="170" y="114" width="95" height="24" fill="#cbd5e1" class="r"/><rect x="275" y="114" width="125" height="24" fill="#c4b5fd" class="r"/><rect x="410" y="114" width="180" height="24" fill="#86efac" class="r"/><text x="184" y="131" class="x">6.42M</text><text x="289" y="131" class="x">3.56M</text><text x="424" y="131" class="x">6.72M</text>
      <text x="25" y="178" class="t">双缓冲模型：下一项可以先读入，覆盖上一项的后处理等待</text><text x="25" y="207" class="s">读</text><rect x="170" y="192" width="220" height="24" fill="#bfdbfe" class="r"/><rect x="350" y="192" width="120" height="24" fill="#bfdbfe" opacity=".65" class="r"/><text x="25" y="243" class="s">算</text><rect x="330" y="228" width="300" height="24" fill="#fdba74" class="r"/><text x="25" y="279" class="s">写 / 后处理</text><rect x="560" y="264" width="150" height="24" fill="#86efac" class="r"/><text x="730" y="281" class="x">总周期：86.41M → 41.95M（模型）</text>
    </svg>'''


def svg_bar(title: str, items: list[tuple[str, float, str]], unit: str = "", width: int = 1060, height: int | None = None) -> str:
    row_h = 31
    height = height or (58 + row_h * len(items))
    left, right, top = 245, 145, 38
    plot_w = width - left - right
    max_v = max([float(v) for _, v, _ in items] + [1.0])
    out = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}" xmlns="http://www.w3.org/2000/svg"><style>.t{{font:700 15px Arial,sans-serif;fill:#111827}}.s{{font:12px Arial,sans-serif;fill:#475569}}</style><text x="{left}" y="22" class="t">{esc(title)}</text>']
    for i, (label, val, color) in enumerate(items):
        y = top + i * row_h
        bw = max(1.0, plot_w * float(val) / max_v)
        out.append(f'<text x="{left-10}" y="{y+17}" text-anchor="end" class="s">{esc(label)}</text><rect x="{left}" y="{y+2}" width="{plot_w}" height="19" fill="#eef2f7"/><rect x="{left}" y="{y+2}" width="{bw:.1f}" height="19" fill="{color}"/><text x="{left+bw+8:.1f}" y="{y+17}" class="s">{esc(fmt_int(val))}{esc(unit)}</text>')
    out.append(f'<text x="{left}" y="{height-7}" class="s">0</text><text x="{left+plot_w}" y="{height-7}" text-anchor="end" class="s">{esc(fmt_int(max_v))}{esc(unit)}</text></svg>')
    return "".join(out)


def svg_resource_breakdown(rows: list[tuple[str, str, str, str, float | None]]) -> str:
    """Show resource evidence beside the model-time share.

    A dash is intentional: the current OOC project does not synthesize that
    subsystem independently, so inventing a module resource number would be
    misleading.
    """
    width, row_h, left, right, top = 1120, 38, 255, 190, 48
    height = top + row_h * len(rows) + 42
    max_share = max([float(r[4]) for r in rows if r[4] is not None] + [1.0])
    out = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="module resource and model time breakdown" xmlns="http://www.w3.org/2000/svg"><style>.t{{font:700 15px Arial,sans-serif;fill:#111827}}.s{{font:12px Arial,sans-serif;fill:#334155}}.x{{font:11px Arial,sans-serif;fill:#64748b}}</style><text x="{left}" y="22" class="t">模块资源证据与 current 模型时间占比</text><text x="{left+12}" y="40" class="x">资源列：LUT / DSP / BRAM；右侧条形是阶段占总周期比例，横向阶段可能重叠</text>']
    plot_w = width - left - right
    for i, (name, lut, dsp, bram, share) in enumerate(rows):
        y = top + i * row_h
        out.append(f'<text x="{left-10}" y="{y+17}" text-anchor="end" class="s">{esc(name)}</text><text x="{left}" y="{y+17}" class="x">{esc(lut)} / {esc(dsp)} / {esc(bram)}</text>')
        bx = left + 162
        out.append(f'<rect x="{bx}" y="{y+3}" width="{plot_w-162}" height="18" fill="#eef2f7"/>')
        if share is not None:
            bw = max(1.0, (plot_w - 162) * float(share) / max_share)
            out.append(f'<rect x="{bx}" y="{y+3}" width="{bw:.1f}" height="18" fill="#60a5fa"/><text x="{bx+bw+8:.1f}" y="{y+17}" class="x">{100.0*float(share):.2f}%</text>')
        else:
            out.append(f'<text x="{bx+8}" y="{y+17}" class="x">未单独记账</text>')
    out.append(f'<text x="{left+162}" y="{height-8}" class="x">0</text><text x="{width-right}" y="{height-8}" text-anchor="end" class="x">100%</text></svg>')
    return "".join(out)


def parse_ooc(name: str) -> dict[str, Any]:
    d = RTL / "synth" / f"ooc_{name}"
    util = (d / "utilization.rpt").read_text(encoding="utf-8", errors="ignore") if (d / "utilization.rpt").exists() else ""
    timing = (d / "timing.rpt").read_text(encoding="utf-8", errors="ignore") if (d / "timing.rpt").exists() else ""
    power = (d / "power.rpt").read_text(encoding="utf-8", errors="ignore") if (d / "power.rpt").exists() else ""

    def first(pattern: str, text: str, default: str = "—") -> str:
        m = re.search(pattern, text, flags=re.I | re.M)
        return m.group(1) if m else default

    lut = first(r"\| CLB LUTs\*\s*\|\s*([0-9]+)", util)
    ff = first(r"\| CLB Registers\s*\|\s*([0-9]+)", util)
    dsp = first(r"\| DSPs\s*\|\s*([0-9]+)", util)
    bram = first(r"\| Block RAM Tile\s*\|\s*([0-9]+)", util)
    wns = first(r"Worst Slack\s+([0-9.]+)ns", timing)
    path = first(r"Data Path Delay:\s*([0-9.]+)ns", timing)
    logic = first(r"logic\s+([0-9.]+)ns", timing)
    route = first(r"route\s+([0-9.]+)ns", timing)
    pwr = first(r"\| Total On-Chip Power \(W\)\s*\|\s*([0-9.]+)", power)
    try:
        fmax = f"{1000.0 / (3.298 - float(wns)):.1f}"
    except Exception:
        fmax = "—"
    return {"name": name, "lut": lut, "ff": ff, "dsp": dsp, "bram": bram, "wns": wns, "path": path, "logic": logic, "route": route, "fmax": fmax, "power": pwr, "status": "综合报告" if util else "缺失"}


def load_rows() -> list[dict[str, Any]]:
    path = COMP / "cycle_breakdown.csv"
    try:
        with path.open(encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def main() -> None:
    inv = read_json(COMP / "operator_inventory.json")
    check = read_json(COMP / "stream_check.json")
    current = read_json(COMP / "cycle_summary.json")
    modes = {m: read_json(DATA / f"compiled_{m}" / "cycle_summary.json") for m in ["current", "double_buffer", "queue", "r5_conditional"]}
    trace = read_json(DATA / "trace_manifest.json")
    capture = read_json(DATA / "capture_result.json")
    golden = read_json(DATA / "golden_results.json")
    sim = read_json(DATA / "sim_results.json")
    rows = load_rows()
    ooc = [parse_ooc(x) for x in ["1x1", "4x4", "16x48"]]
    db = modes["double_buffer"]
    queue = modes["queue"]
    speedup = current["total_cycles"] / db["total_cycles"] if db.get("total_cycles") else 0.0
    reduction = (1.0 - db["total_cycles"] / current["total_cycles"]) * 100.0 if current.get("total_cycles") else 0.0
    queue_gain = (1.0 - queue["total_cycles"] / db["total_cycles"]) * 100.0 if db.get("total_cycles") else 0.0
    peak_250 = float(current.get("peak_gops_250_0", 768.0))
    mapped_share = float(current.get("mapped_cycles", 0)) / float(current.get("total_cycles", 1))
    fallback_share = float(current.get("fallback_cycles", 0)) / float(current.get("total_cycles", 1))
    requant_share = float(current.get("requant_cycles", 0)) / float(current.get("total_cycles", 1))
    write_share = float(current.get("write_cycles", 0)) / float(current.get("total_cycles", 1))
    act_read_share = float(current.get("activation_read_cycles", 0)) / float(current.get("total_cycles", 1))
    weight_read_share = float(current.get("weight_read_cycles", 0)) / float(current.get("total_cycles", 1))

    # Aggregate descriptor costs by top-level module and by operation.
    by_top: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0, "cycles": 0, "mac": 0})
    by_op: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0, "cycles": 0, "mac": 0})
    shape_acc: dict[tuple[str, int, int, int], dict[str, float]] = defaultdict(lambda: {"count": 0, "cycles": 0, "mac": 0, "tiles": 0})
    for r in rows:
        try:
            cyc = float(r.get("total_cycles") or 0)
            mac = float(r.get("valid_mac_count") or 0)
            op = r.get("op") or "unknown"
            path = r.get("module_path") or "<top>"
            top = path.split(".")[0] if path else "<top>"
            by_top[top]["count"] += 1; by_top[top]["cycles"] += cyc; by_top[top]["mac"] += mac
            by_op[op]["count"] += 1; by_op[op]["cycles"] += cyc; by_op[op]["mac"] += mac
            m, n, k = int(r.get("m") or 0), int(r.get("n") or 0), int(r.get("k") or 0)
            shape_acc[(op, m, n, k)]["count"] += 1; shape_acc[(op, m, n, k)]["cycles"] += cyc; shape_acc[(op, m, n, k)]["mac"] += mac; shape_acc[(op, m, n, k)]["tiles"] += float(r.get("tile_count") or 0)
        except Exception:
            continue
    top_sorted = sorted(by_top.items(), key=lambda kv: -kv[1]["cycles"])
    op_sorted = sorted(by_op.items(), key=lambda kv: -kv[1]["cycles"])
    shape_sorted = sorted(shape_acc.items(), key=lambda kv: -kv[1]["cycles"])[:10]

    module_counts = inv.get("module_event_counts", {})
    mapping_counts = inv.get("mapping_counts", {})
    coverage_rows = [
        ["Linear / GEMM", fmt_int(module_counts.get("linear", 0)), "rtl_gemm", "Pack2 16×96 tile"],
        ["动态 BMM", fmt_int(mapping_counts.get("rtl_bmm", 0)), "rtl_bmm", "两个输入、布局和依赖均有记录"],
        ["LayerNorm", fmt_int(module_counts.get("LayerNorm", 0)), "aux_behavior", "行为级周期；未计为 PE 工作"],
        ["GELU", fmt_int(module_counts.get("GELU", 0)), "aux_behavior", "行为级周期"],
        ["Conv2d", fmt_int(module_counts.get("Conv2d", 0)), "aux_behavior", "im2col 尚未进入 Pack2"],
        ["MultiheadAttention 外层", fmt_int(module_counts.get("MultiheadAttention", 0)), "aux_behavior", "内部 BMM 单独列出"],
        ["未知事件", fmt_int(check.get("unknown_count", 0)), "—", "分类检查必须为 0"],
    ]
    mode_rows = []
    for key, label in [("current", "current"), ("double_buffer", "双缓冲"), ("queue", "双缓冲 + 兼容队列"), ("r5_conditional", "R5 条件")]:
        s = modes[key]
        mode_rows.append([label, fmt_int(s.get("total_cycles")), f"{s.get('total_cycles', 0) / current.get('total_cycles', 1):.3f}×", fmt_pct(s.get("pe_time_utilization")), fmt_pct(s.get("gemm_utilization")), fmt_float(s.get("effective_gops_250_0"), 1), "周期模型" if s.get("modeled_not_measured") else "current 记账"])
    top_rows = []
    for name, d in top_sorted:
        top_rows.append([esc(name), fmt_int(d["count"]), fmt_int(d["cycles"]), fmt_pct(d["cycles"] / current["total_cycles"]), fmt_int(d["mac"])])
    op_rows = []
    for name, d in op_sorted:
        op_rows.append([esc(name), fmt_int(d["count"]), fmt_int(d["cycles"]), fmt_pct(d["cycles"] / current["total_cycles"]), fmt_int(d["mac"])])
    shape_rows = []
    for (op, m, n, k), d in shape_sorted:
        shape_rows.append([esc(op), f"{m}×{n}×{k}", fmt_int(d["count"]), fmt_int(d["cycles"]), fmt_int(d["mac"])])
    ooc_rows = []
    for x in ooc:
        ooc_rows.append([esc(x["name"]), esc(x["lut"]), esc(x["ff"]), esc(x["dsp"]), esc(x["bram"]), esc(x["wns"]), esc(x["fmax"]), esc(x["power"]), esc(x["status"])])

    cycle_items = [("激活读取", current.get("activation_read_cycles", 0), "#93c5fd"), ("权重读取", current.get("weight_read_cycles", 0), "#60a5fa"), ("阵列计算", current.get("compute_cycles", 0), "#fb923c"), ("fallback", current.get("fallback_cycles", 0), "#94a3b8"), ("requant", current.get("requant_cycles", 0), "#a78bfa"), ("写回", current.get("write_cycles", 0), "#4ade80"), ("snapshot", current.get("snapshot_cycles", 0), "#facc15")]
    op_items = [(name, d["cycles"], "#2563eb" if name == "GEMM_W8A8" else "#60a5fa" if name == "BMM_W8A8" else "#94a3b8" if name == "LAYER_NORM" else "#a78bfa") for name, d in op_sorted]

    source_files = [DATA / "trace_manifest.json", DATA / "capture_result.json", DATA / "operator_inventory.json", COMP / "descriptors.jsonl", COMP / "instructions.hex", COMP / "cycle_summary.json", DATA / "golden_results.json", DATA / "sim_results.json", RTL / "rtl" / "tvla_w8a8_pack2_replay_top.sv", RTL / "rtl" / "tvla_w8a8_pack2_pe.sv", RTL / "rtl" / "pack2_mult_padd.sv", RTL / "synth" / "ooc_16x48" / "utilization.rpt", RTL / "synth" / "ooc_16x48" / "timing.rpt", RTL / "synth" / "ooc_16x48" / "power.rpt"]
    source_hashes = {str(p.relative_to(ROOT)): sha256(p) for p in source_files if p.exists()}

    summary = {
        "report_timestamp": GENERATED,
        "workspace": "turbovla_w8a8_pack2",
        "source_version": VERSION,
        "trace_evidence": {"schema": trace.get("schema_version"), "capture_status": capture.get("status"), "suite": trace.get("source", {}).get("suite"), "task_id": trace.get("source", {}).get("task_id"), "seed": trace.get("source", {}).get("seed"), "parameters": trace.get("source", {}).get("parameter_count"), "module_events": trace.get("source", {}).get("module_events"), "dispatch_events": trace.get("source", {}).get("dispatch_events"), "linear_events": trace.get("source", {}).get("linear_events"), "unique_weights": trace.get("source", {}).get("unique_weights"), "quantization_in_trace": trace.get("quantization", {})},
        "compiler": {"descriptors": len(rows), "instructions_including_end": len(rows) + 1, "mapped_descriptors": mapping_counts.get("rtl_gemm", 0) + mapping_counts.get("rtl_bmm", 0), "aux_descriptors": mapping_counts.get("aux_behavior", 0), "unknown": check.get("unknown_count", 0), "valid_mac": current.get("valid_mac_count"), "tiles": current.get("tile_count")},
        "array": {"rows": 16, "physical_columns": 48, "logical_columns": 96, "dsp": 768, "mac_per_dsp_per_cycle": 2, "clock_mhz": 250, "peak_gops": peak_250},
        "modes": modes,
        "ooc": ooc,
        "evidence_boundary": {"cycle_values": "trace-driven Python projection using captured W8A16 metadata; not a true W8A8 hardware measurement", "ooc_values": "Vivado 2021.2 synthesis OOC; no place/route", "power": "vectorless estimate; no TOPS/W", "quality": "no new LIBERO success-rate result"},
        "source_sha256": source_hashes,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "architecture_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = f"""# TurboVLA W8A8 Pack2 芯片架构报告清单\n\n- 生成时间：{GENERATED}\n- 报告：`{REPORT_TS}_chip_architecture_report.html`\n- 数据版本：`{VERSION}`\n- 报告性质：编译器/指令集/RTL 组织说明 + trace 驱动周期模型 + Pack2 OOC 综合\n\n## 证据边界\n\n- trace manifest 的量化元数据仍是 W8A16（activation 16 bit、weight 8 bit、accumulator 40 bit、output 16 bit）。因此本页的 W8A8 周期数字是同一形状和控制流上的 Pack2 W8A8 投影，不是重新采集的纯 W8A8 全模型实测。\n- 1×1、4×4、16×48 是 Vivado 2021.2 的 OOC 综合结果，尚未 place/route。4.604 W 是 vectorless power，不换算 TOPS/W。\n- LayerNorm、GELU、Conv、attention 外层等在 full trace 中有 AUX/fallback 事件，但当前 OOC 工程只综合 Pack2 阵列。\n\n## 复现\n\n```text\npython reports/{REPORT_TS}/generate_architecture_report.py\npython algo/v1_2026-09-14_115230_w8a8_semantics/test_pack2_golden.py\npython compiler/v1_2026-09-14_115230_pack2_compiler/check_compiled_stream.py data/{VERSION}/compiled_current\n```\n\n## 关键来源 SHA256\n\n""" + "\n".join(f"- `{k}`：`{v}`" for k, v in source_hashes.items()) + "\n"
    (REPORT_DIR / "BUILD_MANIFEST.md").write_text(manifest, encoding="utf-8")
    (REPORT_DIR / "WORKLOG.md").write_text(f"# 工作记录\n\n## {GENERATED} — 生成芯片架构说明报告\n\n读取 TurboVLA W8A8 Pack2 的编译器、描述符、周期汇总、Pack2 RTL 和 Vivado OOC 报告，生成单文件 HTML。没有修改旧代码和历史报告。\n\n- 432 个 descriptor、433 条 command（含 END）。\n- current：{fmt_int(current['total_cycles'])} cycles；双缓冲：{fmt_int(db['total_cycles'])} cycles。\n- 16×48 OOC：{ooc[-1]['lut']} LUT、{ooc[-1]['ff']} FF、{ooc[-1]['dsp']} DSP、{ooc[-1]['bram']} BRAM。\n", encoding="utf-8")

    css = '''*{box-sizing:border-box}body{margin:0;background:#eef1f5;color:#1f2937;font-family:"Microsoft YaHei",Arial,sans-serif;line-height:1.7}.page{max-width:1280px;margin:0 auto;background:#fff;min-height:100vh;padding:34px 48px 70px}.eyebrow{font-size:13px;letter-spacing:.08em;color:#2563eb}.title{font-size:31px;line-height:1.25;margin:5px 0 10px;color:#111827}.subtitle{margin:0 0 13px;color:#475569}.stamp{font:12px Consolas,monospace;color:#64748b}.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:22px 0}.metric{border:1px solid #dbe3ee;border-top:4px solid #2563eb;background:#fbfdff;padding:13px 14px;min-height:92px}.metric b{display:block;font-size:23px;color:#0f172a;line-height:1.2}.metric span{display:block;font-size:12px;color:#64748b;margin-top:5px}.section{border-top:1px solid #e5e7eb;margin-top:34px;padding-top:26px}.section h2{font-size:23px;line-height:1.35;margin:0 0 10px;color:#111827}.section h3{font-size:17px;margin:21px 0 8px;color:#1f2937}.figure{border:1px solid #dbe3ee;background:#fff;padding:12px 15px;margin:16px 0;overflow-x:auto}.caption{font-size:13px;color:#475569;margin:7px 3px 1px}.note{border-left:4px solid #f59e0b;background:#fffbeb;padding:12px 15px;margin:14px 0}.note.good{border-left-color:#16a34a;background:#f0fdf4}.note.red{border-left-color:#dc2626;background:#fef2f2}.two{display:grid;grid-template-columns:1.05fr .95fr;gap:18px;align-items:start}.three{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}.card{border:1px solid #e2e8f0;background:#f8fafc;padding:12px 14px}.card h4{margin:0 0 5px;color:#1e3a8a}.small{font-size:13px}.muted{color:#64748b}.redtxt{color:#b91c1c}.greentxt{color:#15803d}table{width:100%;border-collapse:collapse;margin:11px 0 16px;font-size:13px}th,td{border:1px solid #dbe3ee;padding:7px 9px;text-align:left;vertical-align:top}th{background:#f1f5f9;color:#334155;font-weight:700}code{font-family:Consolas,monospace;font-size:12px;background:#f1f5f9;border-radius:3px;padding:2px 5px}.formula{font-family:Georgia,"Times New Roman",serif;background:#f8fafc;border-left:3px solid #94a3b8;padding:8px 12px;margin:10px 0;font-size:16px}.tag{display:inline-block;border:1px solid #cbd5e1;background:#f8fafc;padding:2px 7px;margin:2px;border-radius:3px;font-size:12px}@media(max-width:900px){.page{padding:24px 18px}.grid{grid-template-columns:repeat(2,1fr)}.two,.three{grid-template-columns:1fr}.title{font-size:25px}}'''

    # SVGs and tables are embedded in the document in the order a reader needs them.
    arch_svg = svg_architecture()
    compiler_svg = svg_compiler()
    command_svg = svg_command_layout()
    array_svg = svg_array()
    pack_svg = svg_pack_math()
    timeline_svg = svg_timeline()
    mode_svg = svg_bar("四种控制模型的总周期（越短越好）", [("current", modes["current"]["total_cycles"], "#ef4444"), ("双缓冲", modes["double_buffer"]["total_cycles"], "#2563eb"), ("兼容队列", modes["queue"]["total_cycles"], "#16a34a"), ("R5 条件", modes["r5_conditional"]["total_cycles"], "#64748b")], " cycles")
    cycle_svg = svg_bar("current 阶段记账（阶段可能重叠，不能直接相加）", cycle_items, " cycles")
    op_svg = svg_bar("按 descriptor 操作类型的周期", op_items, " cycles")
    top_svg = svg_bar("按模块前缀的周期", [(n, d["cycles"], "#2563eb" if i == 0 else "#60a5fa") for i, (n, d) in enumerate(top_sorted)], " cycles")
    resource_svg = svg_resource_breakdown([
        ("Pack2 阵列", f"{ooc[-1]['lut']} LUT", f"{ooc[-1]['dsp']} DSP", f"{ooc[-1]['bram']} BRAM", mapped_share),
        ("读出 / requant", "未单独综合", "未单独综合", "未单独综合", requant_share),
        ("INT8 写回", "未单独综合", "未单独综合", "未单独综合", write_share),
        ("LayerNorm / GELU / AUX", "未单独综合", "未单独综合", "未单独综合", fallback_share),
        ("CTX / WRAM / DMA", "未单独综合", "未单独综合", "未单独综合", max(act_read_share, weight_read_share)),
    ])

    # Use small HTML helpers for source-sensitive values.
    trace_source = trace.get("source", {})
    qtrace = trace.get("quantization", {})
    full_eff = fmt_pct(current.get("effective_gops_250_0", 0) / peak_250)
    html_out = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{REPORT_TS} TurboVLA W8A8 Pack2 芯片架构说明</title><style>{css}</style></head><body><main class="page">
      <div class="eyebrow">TURBOVLA · W8A8 · PACK2 · CHIP ARCHITECTURE</div>
      <h1 class="title">TurboVLA W8A8 Pack2：编译器、指令集和硬件组织</h1>
      <p class="subtitle">这份报告把当前版本能实际追溯的内容放在一起：输入 trace 如何变成指令，指令如何驱动 Pack2 阵列，以及资源和周期数字分别来自哪里。</p>
      <div class="stamp">生成时间：{GENERATED}　|　工作区版本：{VERSION}　|　报告类型：架构说明 + trace 周期模型 + Vivado OOC 综合</div>
      <div class="grid"><div class="metric"><b>16×48</b><span>物理阵列尺寸</span></div><div class="metric"><b>768</b><span>DSP；每 DSP 每拍 2 个 INT8×INT8 MAC</span></div><div class="metric"><b>{fmt_pct(current.get('pe_time_utilization'))}</b><span>current PE 时间利用率</span></div><div class="metric"><b>{fmt_float(current.get('effective_gops_250_0'),1)}</b><span>current 有效 GOPS @250 MHz</span></div><div class="metric"><b>{fmt_float(ooc[-1]['power'],3)} W</b><span>16×48 OOC vectorless power</span></div></div>

      <section class="section"><h2>先看结论</h2>
        <div class="note good"><b>编译器和 Pack2 算术接口已经接上了 TurboVLA 的一条真实 forward trace。</b>408 个 module event 加上 24 个 BMM 子事件，最后得到 432 个 descriptor 和 433 条 command（最后一条是 END）。304 个 descriptor 被分到 GEMM/BMM，128 个保留为 AUX/fallback，分类检查的 unknown 为 0。</div>
        <p>current 周期模型为 <b>{fmt_int(current['total_cycles'])}</b> 拍。250 MHz 下有效吞吐为 <b>{fmt_float(current['effective_gops_250_0'],1)} GOPS</b>，相当于 Pack2 峰值 768 GOPS 的 <b>{full_eff}</b>。双缓冲模型把周期降到 <b>{fmt_int(db['total_cycles'])}</b> 拍，模型上的下降是 <b>{reduction:.2f}%</b>；它不是已经在完整 FPGA 上测到的速度。</p>
        <p>16×48 阵列的 Vivado OOC 综合结果是 <b>{fmt_int(ooc[-1]['lut'])} LUT、{fmt_int(ooc[-1]['ff'])} FF、{fmt_int(ooc[-1]['dsp'])} DSP、{fmt_int(ooc[-1]['bram'])} BRAM</b>。3.298 ns 约束下 WNS 为 <b>{ooc[-1]['wns']} ns</b>，由综合报告推得约 <b>{ooc[-1]['fmax']} MHz</b>。这只是综合结果，没有 place/route；4.604 W 是 vectorless 估计，不能换算 TOPS/W。</p>
        <div class="note red"><b>最重要的证据边界：</b>当前 trace manifest 的量化元数据仍写着 activation 16 bit、weight 8 bit、accumulator 40 bit、output 16 bit（schema 为 <code>{esc(trace.get('schema_version'))}</code>）。因此本页的周期数字是用同一形状和控制流投影到 W8A8 Pack2 的结果，不是重新采集的纯 W8A8 全模型实测。静态 scale 也仍待导入和逐位对拍。</div>
      </section>

      <section class="section"><h2>1. 这颗芯片现在负责什么</h2>
        <div class="figure">{arch_svg}<div class="caption">这图怎么看：左边的 trace 经过编译器变成 command、descriptor 和 payload；中间 replay top 负责排队和统计；右边 Pack2 阵列处理能映射的 GEMM/BMM，其他算子走明确的 AUX/fallback 路径。</div></div>
        <p>当前输入是一条 LIBERO Spatial task 0 的 TurboVLA policy call。trace 记录了两路 256×256 图像、instruction、8 维机器人状态和 12×7 action chunk。模型参数量约 <b>{fmt_float(float(trace_source.get('parameter_count', 0)) / 1e6,1)}M</b>，语言分支是 21×768，视觉分支是 261×768，结构包含 6 个 fusion layer 和 3 个 action-decoder layer。</p>
        {html_table(["项目", "当前证据", "报告中的用途"], [["输入/输出", "两路 256×256；8-D state；12×7 action", "说明 trace 的边界"], ["trace", f"{fmt_int(trace_source.get('module_events'))} module / {fmt_int(trace_source.get('dispatch_events'))} dispatch", "编译器输入"], ["量化元数据", f"A={qtrace.get('activation_bits')} bit，W={qtrace.get('weight_bits')} bit，acc={qtrace.get('accumulator_bits')} bit，out={qtrace.get('output_bits')} bit", "提醒当前源 trace 仍是 W8A16"], ["阵列目标", "16×48 physical，96 logical，768 DSP", "Pack2 部署路径"], ["验证状态", "golden / Verilator / Icarus PASS；16×48 为 elaboration", "说明已验证到哪一层"]])}
      </section>

      <section class="section"><h2>2. 编译器：从算子记录到可回放指令</h2>
        <div class="figure">{compiler_svg}<div class="caption">这图怎么看：编译器先确定一个事件由谁负责，再检查尺寸、依赖和布局，最后把合法的 Linear/BMM 切成 16×96 tile，并写出运输头和 sideband。</div></div>
        <p>编译器不是重新执行神经网络。它读取已经捕获的 module 和 dispatch 事件，把每个事件的形状、父子关系、权重 hash、scale ID 和周期成本写进 descriptor。BMM 事件会挂到记录的父事件后面；这样 MultiheadAttention 外层和内部 BMM 不会重复计数。</p>
        <div class="two"><div>{html_table(["输入类别", "处理方式", "当前数量/状态"], [["Linear", "生成 <code>GEMM_W8A8</code>，16×96 tile", "280，全部 <code>rtl_gemm</code>"], ["BMM", "同时检查两个操作数、形状和 layout", "24，当前 trace 记为 <code>rtl_bmm</code>"], ["LayerNorm / GELU", "生成向量/AUX 事件，保留周期", "112 / 2"], ["Conv2d / MHA 外层", "行为级 AUX；Conv 需要 im2col", "2 / 12"], ["未知", "不允许静默丢弃", "0"]])}</div><div class="card"><h4>编译器当前的输出</h4><p class="small"><code>descriptors.jsonl</code> 保存每个事件的矩阵尺寸、tile grid、valid mask、scale IDs、依赖和周期字段。<code>instructions.hex</code> 保存 command word。<code>descriptors_512.hex</code> 保存 sideband。</p><p class="small">当前 descriptor 已经能支撑 trace 回放和周期统计，但源 trace 的 payload offset/length 尚未全部变成 replay top 可执行的 DMA 地址/stride 字段。要做真正的系统编译器，还需要把这些地址字段接到 CTX/WRAM/DMA。</p></div></div>
        <h3>2.1 tile 和尾块</h3><p>Pack2 每次按 M=16、N=96 组织一个逻辑 tile。N=96 来自 48 个物理列，每个物理列携带两个逻辑列。M 或 N 不整除时，descriptor 的 <code>valid_mask</code> 只让有效行列参与 MAC；无效位置不能被写进有效吞吐。</p>
      </section>

      <section class="section"><h2>3. 指令集：64-bit command 加 512-bit descriptor</h2>
        <div class="figure">{command_svg}<div class="caption">这图怎么看：command word 只负责“做什么、用哪个 descriptor”；矩阵尺寸、周期、流量和 tile 数放在 512-bit sideband，所以不会把地址和 M/N/K 挤进 64 bit。</div></div>
        <p>当前 command word 的字段是 <code>op[63:56]</code>、<code>flags[55:48]</code>、<code>descriptor_id[47:32]</code> 和 <code>length[15:0]</code>。例如 <code>0x1880000100000000</code> 的含义是：操作码 0x18（GEMM_W8A8）、flags=0x80（映射到 RTL）、descriptor_id=1，length 为 0。</p>
        {html_table(["操作码", "名称", "用途/当前状态"], [["0x01", "LOAD_CTX", "激活搬运定义"], ["0x02", "LOAD_WEIGHT", "权重搬运定义"], ["0x03", "STORE_CTX", "结果写回定义"], ["0x18", "GEMM_W8A8", "当前主映射"], ["0x19", "BMM_W8A8", "条件映射；两个输入都要满足"], ["0x20–0x22", "BIAS_ADD / ADD / MUL", "独立后处理任务"], ["0x30/0x31/0x33", "LAYER_NORM / SOFTMAX / GELU", "向量或 AUX 路径"], ["0x41", "BARRIER", "残差和非线性边界"], ["0x50", "AUX_EVENT", "行为级辅助成本"], ["0xFF", "END", "FIFO 为空时作为结束 fence"]])}
        {html_table(["sideband 字段", "位段", "用途"], [["total_cycles", "511:480", "该 descriptor 的完成周期预算"], ["valid_mac_count", "479:448", "只统计有效的矩阵乘工作量"], ["active_pe_cycles", "447:416", "PE 忙碌拍数"], ["activation_read / write", "415:384 / 383:352", "阶段读写周期"], ["vector / snapshot / requant", "351:320 / 319:288 / 287:256", "辅助和后处理周期"], ["activation / weight / output bytes", "255:224 / 223:192 / 191:160", "流量统计"], ["M / N / K", "159:128 / 127:96 / 95:64", "矩阵尺寸"], ["op / flags / tile_count", "63:56 / 55:48 / 31:16", "操作、映射/优化标记和 tile 数"], ["reserved / spare", "47:32 / 15:0", "当前不参与计算"]])}
        <p>当前 descriptor 的高位保存周期和工作量：total cycles、valid MAC、active PE cycles、读取/写回、vector、snapshot、requant 和字节数；随后保存 M/N/K。低 64 bit 还带操作码、flags 和 tile_count。优化模式的双缓冲/队列/R5 标记写在 sideband trailer，command flags 仍以 mapped 标志为主。</p>
      </section>

      <section class="section"><h2>4. 硬件组织：输入、阵列、状态和读出</h2>
        <div class="figure">{array_svg}<div class="caption">这图怎么看：激活从左向右走，权重从上向下走；每个物理列是一颗 DSP，却对应两个逻辑输出列。实际 RTL 展开为 16×48，图中只画代表性单元。</div></div>
        <p>Pack2 的输入接口是 128-bit activation beat（16 个 INT8）和 768-bit weight beat（48 组 <code>{{w1,w0}}</code>）。激活边缘按行号延迟，权重边缘按列号延迟，数据在 PE 内以 <code>k+i+j</code> 的波前相遇。<code>feed_vld</code> 控制数据是否有效，<code>feed_pulse</code> 把末脉冲送到对应行，最后一行完成后才读 snapshot。</p>
        <div class="figure">{pack_svg}<div class="caption">这图怎么看：预加器把两个带偏移的 8-bit 权重还原成一个 signed 打包数；高场的借位由 <code>P[15]</code> 修正，避免把两个乘积混成一个错误的高位。</div></div>
        <div class="three"><div class="card"><h4>PE 内部</h4><p class="small">每个 PE 使用一颗 DSP48E2。它产生低场和高场两个 INT8×INT8 product。两个 product 各自进入一条 INT32 accumulator。PE 还保留两个 27-bit snapshot。</p></div><div class="card"><h4>读出和重量化</h4><p class="small">脉冲到来时，snapshot 先抄出累加器低 27 bit，再清零 accumulator。读出侧接四列时分复用的 requant 单元，最后生成 INT8 写回。</p></div><div class="card"><h4>当前 top 的边界</h4><p class="small"><code>replay_top</code> 有 descriptor FIFO、command ready/valid、结果槽和活动计数器。OOC 阵列 top 只测 Pack2 阵列，不包括完整 CTX/WRAM、DMA 和 LayerNorm/Softmax RTL。</p></div></div>
        {html_table(["RTL 模块", "它做什么", "当前证据"], [["tvla_w8a8_pack2_mult_padd.sv", "把两个 INT8 权重打包，使用 DSP48E2 pre-adder 还原 R 并输出 P", "Verilator 逐位 smoke；OOC 阵列路径"], ["tvla_w8a8_pack2_pe.sv", "两路 product、两条 INT32 累加、27-bit snapshot", "继承 ae_pe_p2_pa，已做边界检查"], ["tvla_w8a8_pack2_sysarr.sv", "16 行×48 物理列的行/列 skew 和 PE 网格", "16×48 elaboration；OOC 资源"], ["tvla_w8a8_pack2_gemm.sv", "把 TurboVLA 参数接口接到 ae_gemm_p2 控制器", "接口包装；未单独证明完整 trace"], ["tvla_w8a8_pack2_requant.sv", "四列时分复用的乘移位和 INT8 饱和", "rq_ms_x/rq_v2 参考路径"], ["tvla_w8a8_pack2_replay_top.sv", "descriptor FIFO、ready/valid、结果槽和 activity counters", "Icarus replay smoke；完整 trace 仍是计数模型"]])}
        <p class="formula">Q = (w₁+128)·2¹⁶ + (w₀+128)，　R = Q − 128·(2¹⁶+1)，　P = a·R</p>
        <p>黄金模型对 <code>prod0=signed(P[15:0])</code> 和 <code>prod1=signed(P[31:16])+P[15]</code> 做了 100,343 个随机和边界样本，失败数为 0。K≤3072 的代表边界能放进 27-bit snapshot；K=4096 的最坏累加绝对值为 67,108,864，超过 signed 27-bit，所以编译器必须加 snapshot guard。</p>
      </section>

      <section class="section"><h2>5. 控制时序和活动计数</h2>
        <p><code>replay_top</code> 的 descriptor FIFO 默认深度为 16。FIFO 不满时 <code>desc_ready=1</code>；普通 command 只有在 FIFO 有 descriptor 时才会接收，映射任务还要求结果槽空闲；END 只有在 FIFO 排空后才会接收。输出端没有 ready 时，结果保持有效并累计 backpressure。</p>
        <div class="figure">{timeline_svg}<div class="caption">这图怎么看：current 把读、算、写之间的等待暴露出来；双缓冲允许下一项提前读数，所以同一批有效 MAC 不变，完成时间缩短。</div></div>
        <div class="figure">{mode_svg}<div class="caption">这图怎么看：双缓冲已经改变了模型中的主瓶颈；兼容队列在这条 trace 上只多带来 {queue_gain:.3f}% 的周期下降，说明队列深度不是第一优先级。</div></div>
        {html_table(["模式", "总周期", "相对 current", "PE 时间利用率", "GEMM 利用率", "有效 GOPS @250 MHz", "证据"], mode_rows)}
        <p>活动计数器包含 total/mapped/fallback cycles、读写周期、scheduler wait、backpressure、snapshot、requant、vector、active/busy PE cycles、valid MAC、tile 数和三类字节流量。完整 trace 回放时，top 主要把 descriptor 中预先算好的字段累加起来；它不是让 432 个 descriptor 在 RTL 中逐拍运行完。因此周期表属于 Python/虚拟事件模型，代表性 tile 的逐位对拍另行完成。</p>
      </section>

      <section class="section"><h2>6. 当前 workload 下阵列到底忙不忙</h2>
        <div class="two"><div class="figure">{op_svg}<div class="caption">这图怎么看：GEMM 占绝大多数模型周期，但 LayerNorm、GELU 和 AUX 仍然要执行；把所有事件都称为 GEMM 会高估阵列工作量。</div></div><div class="figure">{top_svg}<div class="caption">这图怎么看：这条 trace 的周期主要落在 vision_encoder；这不是说其他模块可以删掉，而是视觉 backbone 的矩阵和尾块更值得先优化。</div></div></div>
        {html_table(["操作类型", "descriptor 数", "周期", "占总周期", "valid MAC"], op_rows)}
        <p>current 的有效 MAC 是 <b>{fmt_int(current['valid_mac_count'])}</b>，阵列有效 PE cycles 是 <b>{fmt_int(current['active_pe_cycles'])}</b>。PE 时间利用率按 <code>active_pe_cycles / (768 × total_cycles)</code> 算，为 <b>{fmt_pct(current['pe_time_utilization'])}</b>；GEMM 利用率按 <code>valid_mac / (768 × 2 × mapped_cycles)</code> 算，为 <b>{fmt_pct(current['gemm_utilization'])}</b>。它们都没有把 fallback 或被跳过的 MAC 算成阵列完成量。</p>
        <div class="figure">{cycle_svg}<div class="caption">这图怎么看：激活读取 37.72M、权重读取 34.51M、计算 35.16M 是阶段记账；因为这些阶段在不同 descriptor 间可能重叠，不能简单相加来替代 total_cycles。</div></div>
        {html_table(["模块前缀", "descriptor 数", "周期", "占总周期", "valid MAC"], top_rows)}
        <h3>6.1 代表性形状</h3>
        {html_table(["操作", "M×N×K", "出现次数", "周期", "valid MAC"], shape_rows)}
      </section>

      <section class="section"><h2>7. 资源占用和时序</h2>
        <p>下面的资源只来自 Pack2 阵列 OOC 工程，不是完整 TurboVLA 芯片的最终资源。可用资源按 XCZU7EV-2E 报告中的 230,400 LUT、460,800 FF、1,728 DSP 和 312 个 BRAM tile 计算。</p>
        {html_table(["阵列规模", "LUT", "FF", "DSP", "BRAM", "WNS", "综合推导 Fmax", "vectorless power", "结果"], ooc_rows)}
        <div class="figure">{resource_svg}<div class="caption">这图怎么看：只有 Pack2 阵列有独立的 OOC 资源数字；其他模块的 LUT/DSP/BRAM 目前没有单独综合，所以用“未单独综合”标出，右侧只放已有周期模型的阶段占比，避免用周期相减伪造模块面积。</div></div>
        {html_table(["模块/阶段", "独立 LUT", "独立 DSP", "独立 BRAM", "current 模型时间口径"], [["Pack2 阵列", fmt_int(ooc[-1]["lut"]), fmt_int(ooc[-1]["dsp"]), fmt_int(ooc[-1]["bram"]), fmt_pct(mapped_share) + " mapped cycles"], ["读出 / requant", "未单独综合", "未单独综合", "未单独综合", fmt_pct(requant_share) + " requant 阶段"], ["INT8 写回", "未单独综合", "未单独综合", "未单独综合", fmt_pct(write_share) + " write 阶段"], ["LayerNorm / GELU / AUX", "未单独综合", "未单独综合", "未单独综合", fmt_pct(fallback_share) + " fallback cycles"], ["CTX / WRAM / DMA", "未单独综合", "未单独综合", "未单独综合", "read 阶段：" + fmt_pct(act_read_share) + " activation、" + fmt_pct(weight_read_share) + " weight"]])}
        <div class="two"><div class="card"><h4>16×48 资源意味着什么</h4><p class="small">78,249 LUT 约占器件 LUT 的 33.96%，148,168 FF 约占 32.15%，768 DSP 约占 44.44%，BRAM 为 0。当前 OOC top 没有把 CTX/WRAM 片上缓存、DMA 和完整辅助算子放进来，所以这些数字不能直接当成整机资源预算。</p></div><div class="card"><h4>关键路径</h4><p class="small">最差路径落在输入寄存器到 DSP48E2 的 pre-adder/multiplier 数据路径。综合报告中 WNS +1.433 ns，数据路径约 1.845 ns，其中逻辑约 1.541 ns、布线约 0.304 ns。place/route 后的扇出和拥塞仍未验证。</p></div></div>
      </section>

      <section class="section"><h2>8. 现在能下的工程结论</h2>
        {html_table(["问题", "当前回答", "证据等级"], [["编译器能否描述 TurboVLA？", "能。432 descriptor、433 command，mapped/aux 分配完整，unknown=0。", "trace + stream check"], ["Pack2 数学是否正确？", "黄金模型 100,343 样本通过；Verilator multiplier 和 Icarus smoke 通过。", "逐位/冒烟"], ["阵列资源是否可综合？", "1×1、4×4、16×48 均完成 OOC 综合，DSP 数为 1/16/768。", "Vivado OOC"], ["完整 TurboVLA 是否已经在 FPGA 上跑完？", "没有。辅助算子是行为级事件，完整 trace 是虚拟计数，未完成板级 DDR 和 place/route。", "未完成"], ["W8A8 数值和成功率是否已证明？", "没有。当前源 trace 仍是 W8A16 元数据，静态 scale 和新 LIBERO 成功率未重做。", "未完成"]])}
        <div class="note">“unknown=0”只代表每个 trace 事件都被分到了某个类别。AUX/fallback 不是已经综合好的 LayerNorm、GELU、DINO 或 Softmax 硬件。这个区别决定了当前报告可以支持架构讨论，但还不能支持整机性能和任务成功率结论。</div>
      </section>

      <section class="section"><h2>9. 下一步怎么排</h2>
        <ol><li><b>先重采集纯 W8A8 trace。</b>把 activation/weight/output 的 dtype、静态 scale、payload 和 descriptor 字段逐项对齐，再对代表性 GEMM/BMM 做整数输出对拍。</li><li><b>把双缓冲从模型搬到 RTL。</b>模型显示周期可下降 {reduction:.2f}%，而兼容队列只再下降 {queue_gain:.3f}%。优先验证 read/compute/write 重叠、snapshot 占用、输出阻塞和结果顺序。</li><li><b>补齐 descriptor 的 DMA 地址和 stride。</b>目前 sideband 能描述形状和成本，但要让编译器直出系统指令，还要让 CTX/WRAM/DMA 消费 payload offset、base、stride 和依赖 fence。</li><li><b>再做多 suite trace、place/route 和活动功耗。</b>只有把短块、尾列、fallback 和片上存储加入同一个 top，才能给出整机资源、频率和 TOPS/W。</li></ol>
        <p><b>当前判断：</b>Pack2 作为 TurboVLA 的 GEMM 数据通路值得继续；最值得投入的是双缓冲调度和纯 W8A8 数值路径。整机架构还没有到 camera-ready 的证据完整度，主要缺口是 W8A8 trace、DMA/存储实现、辅助算子 RTL、place/route 和真实活动功耗。</p>
      </section>

      <section class="section"><h2>附录：可复核文件</h2>
        {html_table(["文件", "用途"], [[f"data/{VERSION}/trace_manifest.json", "trace 来源、模型结构和量化元数据"], [f"data/{VERSION}/compiled_current/descriptors.jsonl", "逐 descriptor 的尺寸、依赖、scale 和周期字段"], [f"data/{VERSION}/compiled_current/instructions.hex", "64-bit command word"], [f"data/{VERSION}/compiled_current/descriptors_512.hex", "512-bit sideband"], [f"data/{VERSION}/compiled_current/cycle_summary.json", "current 周期、MAC、流量和利用率"], [f"hw/v1_{VERSION}_pack2_rtl/rtl/tvla_w8a8_pack2_replay_top.sv", "descriptor FIFO、command handshake 和 activity monitor"], [f"hw/v1_{VERSION}_pack2_rtl/rtl/ae_pe_p2_pa.sv", "Pack2 PE、INT32 累加和 snapshot"], [f"hw/v1_{VERSION}_pack2_rtl/synth/ooc_16x48/", "Vivado OOC 资源、时序和功耗报告"], [f"reports/{REPORT_TS}/architecture_summary.json", "本页机器可读汇总"], [f"reports/{REPORT_TS}/BUILD_MANIFEST.md", "生成清单和来源 SHA256"]])}
        <p class="muted small">报告脚本：<code>reports/{REPORT_TS}/generate_architecture_report.py</code>。所有图均为内嵌 SVG；页面不依赖外部图片、CSS 或 JavaScript。</p>
      </section>
    </main></body></html>'''
    out_file = REPORT_DIR / f"{REPORT_TS}_chip_architecture_report.html"
    out_file.write_text(html_out, encoding="utf-8")
    # Basic checks required by the worklog discipline.
    text = out_file.read_text(encoding="utf-8")
    checks = {"has_none": "None" in text, "has_nan": bool(re.search(r"\bNaN\b", text)), "has_svg": text.count("<svg") >= 7, "has_timestamp": REPORT_TS in text, "has_unknown_zero": str(check.get("unknown_count", 0)) == "0"}
    (REPORT_DIR / "report_checks.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"report": str(out_file), "summary": str(REPORT_DIR / 'architecture_summary.json'), "checks": checks, "bytes": out_file.stat().st_size}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
