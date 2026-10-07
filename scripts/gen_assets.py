"""Generates every animated SVG used by the kvcops profile README.
Run from the repo root:  python3 scripts/gen_assets.py   -> rewrites ./assets/*.svg
All SVGs are self-contained (no external fonts/scripts) so GitHub renders them through <img>.
"""
import os, random, math
from xml.sax.saxutils import escape as esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)
random.seed(28)

# ---------- design tokens ----------
BG, PANEL, PANEL2, LINE = "#07090D", "#0E1118", "#131722", "#232A3A"
TEXT, MUTED, DIM = "#ECE8E1", "#9AA0B0", "#5D6475"
AMBER, ORANGE, VIOLET, CYAN, GREEN = "#F5B759", "#FF7A45", "#A78BFA", "#5EEAD4", "#7EE787"
SERIF = "'Fraunces','Iowan Old Style','Palatino Linotype',Georgia,'Times New Roman',serif"
SANS = "'Inter','Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular',ui-monospace,Menlo,Consolas,'Liberation Mono',monospace"

BASE_CSS = f"""
.serif{{font-family:{SERIF}}} .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
@media (prefers-reduced-motion: reduce){{ *{{animation:none!important}} }}
"""

def write(name, w, h, body, css="", defs=""):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img">'
           f'<style>{BASE_CSS}{css}</style><defs>{defs}</defs>{body}</svg>')
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)

def tw(s, size, mono=False):
    """rough text width estimate"""
    return len(s) * size * (0.61 if mono else 0.54)

def card_bg(w, h, r=20, glow=True, gid="g"):
    s = f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="{BG}" stroke="{LINE}"/>'
    if glow:
        s += f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="url(#{gid}glow)"/>'
    return s

def glow_defs(gid="g", cx="12%", cy="0%", color=AMBER, op=0.22, r="70%"):
    return (f'<radialGradient id="{gid}glow" cx="{cx}" cy="{cy}" r="{r}">'
            f'<stop offset="0" stop-color="{color}" stop-opacity="{op}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')

def grain(w, h, n=60, seed=1, cls="tw"):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, y = rnd.uniform(8, w - 8), rnd.uniform(8, h - 8)
        r = rnd.choice([0.6, 0.8, 1.0, 1.3])
        d = rnd.uniform(0, 6)
        out.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{TEXT}" style="animation-delay:{d:.2f}s"/>')
    return "".join(out)

STAR_CSS = ".tw{animation:tw 5s ease-in-out infinite;opacity:.15}@keyframes tw{0%,100%{opacity:.08}50%{opacity:.75}}"

# =====================================================================
# 1. HERO
# =====================================================================
def hero():
    W, H = 1200, 470
    roles = [
        "builds multi-agent systems that actually ship.",
        "turns messy patents & legal docs into structured data.",
        "takes AI pilots out of notebooks and into production.",
        "won 1st place · IKDD Agentic AI Challenge, CODS 2025.",
    ]
    period = 3.2 * len(roles)
    role_svg = ""
    for i, r in enumerate(roles):
        role_svg += (f'<text class="mono role{' role0' if i == 0 else ''}" x="64" y="298" font-size="19" fill="{TEXT}" '
                     f'style="animation-delay:{i*3.2:.1f}s"><tspan fill="{AMBER}">&gt; </tspan>{esc(r)}</text>')
    # agent graph on the right
    nodes = {"in": (790, 120), "plan": (900, 80), "ret": (900, 200), "tool": (1020, 130),
             "eval": (1030, 260), "hitl": (870, 330), "ship": (1120, 205)}
    labels = {"in": "intake", "plan": "planner", "ret": "retriever", "tool": "tools/MCP",
              "eval": "evals", "hitl": "human", "ship": "prod"}
    edges = [("in", "plan"), ("in", "ret"), ("plan", "tool"), ("ret", "tool"), ("tool", "eval"),
             ("ret", "hitl"), ("hitl", "eval"), ("eval", "ship"), ("tool", "ship")]
    g = ""
    for k, (a, b) in enumerate(edges):
        x1, y1 = nodes[a]; x2, y2 = nodes[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 18
        d = f"M{x1},{y1} Q{mx},{my} {x2},{y2}"
        g += f'<path d="{d}" stroke="{LINE}" stroke-width="1.4"/>'
        g += f'<path class="flow" d="{d}" stroke="{AMBER}" stroke-width="1.4" stroke-opacity=".55" style="animation-delay:{k*0.35:.2f}s"/>'
        dur = 2.2 + (k % 3) * 0.5
        g += (f'<circle r="3.2" fill="{AMBER}"><animateMotion dur="{dur}s" begin="{k*0.4:.1f}s" repeatCount="indefinite" path="{d}"/>'
              f'<animate attributeName="opacity" values="0;1;1;0" dur="{dur}s" begin="{k*0.4:.1f}s" repeatCount="indefinite"/></circle>')
    for k, (key, (x, y)) in enumerate(nodes.items()):
        col = CYAN if key == "hitl" else (GREEN if key == "ship" else AMBER)
        g += (f'<circle class="pulse" cx="{x}" cy="{y}" r="16" fill="{col}" fill-opacity=".10" style="animation-delay:{k*0.5:.1f}s"/>'
              f'<circle cx="{x}" cy="{y}" r="7" fill="{PANEL}" stroke="{col}" stroke-width="2"/>'
              f'<circle cx="{x}" cy="{y}" r="2.6" fill="{col}"/>'
              f'<text class="mono" x="{x}" y="{y+30}" text-anchor="middle" font-size="11" fill="{MUTED}" letter-spacing="1">{labels[key]}</text>')
    chips = ["Agentic AI", "Multi-Agent Systems", "Production RAG", "Document Intelligence", "LLM Evals"]
    cx, chip_svg = 64, ""
    for i, c in enumerate(chips):
        wdt = tw(c, 13) + 28
        chip_svg += (f'<g class="rise" style="animation-delay:{1.4+i*0.12:.2f}s">'
                     f'<rect x="{cx}" y="352" width="{wdt:.0f}" height="30" rx="15" fill="{PANEL2}" stroke="{LINE}"/>'
                     f'<text class="sans" x="{cx+wdt/2:.0f}" y="372" text-anchor="middle" font-size="13" fill="{TEXT}">{esc(c)}</text></g>')
        cx += wdt + 10
    css = STAR_CSS + f"""
.role{{opacity:0;animation:role {period}s infinite}} .role0{{opacity:1}}
@keyframes role{{0%{{opacity:0;transform:translateY(10px)}}3%{{opacity:1;transform:none}}22%{{opacity:1;transform:none}}25%,100%{{opacity:0;transform:translateY(-8px)}}}}
.caret{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}
.lamp{{animation:lamp 6s ease-in-out infinite}}@keyframes lamp{{0%,100%{{opacity:1}}45%{{opacity:.82}}48%{{opacity:.55}}50%{{opacity:.95}}70%{{opacity:.88}}}}
.reveal{{animation:reveal 1.3s cubic-bezier(.2,.8,.2,1) both}}@keyframes reveal{{from{{opacity:0;transform:translateY(24px);filter:blur(6px)}}to{{opacity:1;transform:none;filter:none}}}}
.rise{{animation:reveal .9s cubic-bezier(.2,.8,.2,1) both}}
.flow{{stroke-dasharray:14 220;animation:flow 3.2s linear infinite}}@keyframes flow{{to{{stroke-dashoffset:-234}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 3s ease-out infinite}}@keyframes pulse{{0%{{transform:scale(.6);opacity:.9}}100%{{transform:scale(2.1);opacity:0}}}}
.dot{{animation:blink 1.6s ease-in-out infinite}}
.scan{{animation:scan 7s linear infinite}}@keyframes scan{{from{{transform:translateY(-40px)}}to{{transform:translateY(520px)}}}}
"""
    defs = (glow_defs("h", "8%", "0%", AMBER, .28, "75%") +
            f'<radialGradient id="h2glow" cx="85%" cy="45%" r="45%"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".16"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="#FFE3A8"/><stop offset=".45" stop-color="{AMBER}"/><stop offset="1" stop-color="{ORANGE}"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" values="-0.6 0;0.6 0;-0.6 0" dur="8s" repeatCount="indefinite"/></linearGradient>'
            f'<linearGradient id="scanl" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{AMBER}" stop-opacity="0"/><stop offset="1" stop-color="{AMBER}" stop-opacity=".06"/></linearGradient>'
            f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{TEXT}" fill-opacity=".06"/></pattern>'
            f'<clipPath id="hc"><rect width="{W}" height="{H}" rx="22"/></clipPath>')
    body = (f'<g clip-path="url(#hc)">'
            f'<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#dots)"/>'
            f'<rect class="lamp" width="{W}" height="{H}" fill="url(#hglow)"/><rect width="{W}" height="{H}" fill="url(#h2glow)"/>'
            f'{grain(W, H, 80, 3)}'
            f'<rect class="scan" x="0" y="0" width="{W}" height="40" fill="url(#scanl)"/>'
            f'<g>{g}</g>'
            # left text
            f'<g class="rise" style="animation-delay:.1s"><circle class="dot" cx="70" cy="74" r="4.5" fill="{GREEN}"/>'
            f'<text class="mono" x="84" y="79" font-size="13" fill="{MUTED}" letter-spacing="2.2">ONLINE · FORWARD-DEPLOYED AI ENGINEER · HYD/IN</text></g>'
            f'<g class="reveal" style="animation-delay:.25s"><text class="serif" x="60" y="168" font-size="78" font-weight="600" fill="url(#name)" letter-spacing="-1.5">Karri Vamsi</text></g>'
            f'<g class="reveal" style="animation-delay:.45s"><text class="serif" x="60" y="246" font-size="78" font-weight="600" font-style="italic" fill="{TEXT}" letter-spacing="-1.5">Krishna<tspan fill="{AMBER}">.</tspan></text></g>'
            f'{role_svg}'
            f'<rect class="caret" x="64" y="312" width="11" height="3" fill="{AMBER}"/>'
            f'{chip_svg}'
            f'<text class="mono" x="64" y="430" font-size="12" fill="{DIM}" letter-spacing="1.5">AGENTS · LLM SYSTEMS · PRODUCTION RAG · EVIDENCE, NOT CLAIMS</text>'
            f'<text class="mono" x="1136" y="430" text-anchor="end" font-size="12" fill="{DIM}" letter-spacing="1.5">FILE 00 / 07</text>'
            f'</g><rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="22" stroke="{LINE}"/>')
    write("hero.svg", W, H, body, css, defs)

# =====================================================================
# 2. SECTION HEADERS
# =====================================================================
def header(slug, num, title, note, accent=AMBER):
    W, H = 1200, 92
    css = f"""
.in{{animation:in .9s cubic-bezier(.2,.8,.2,1) both}}@keyframes in{{from{{opacity:0;transform:translateX(-18px)}}to{{opacity:1;transform:none}}}}
.ul{{stroke-dasharray:1200;stroke-dashoffset:1200;animation:ul 1.6s .3s cubic-bezier(.6,0,.2,1) forwards}}@keyframes ul{{to{{stroke-dashoffset:0}}}}
.cm{{animation:cm 4s 1.8s linear infinite}}@keyframes cm{{from{{transform:translateX(-80px)}}to{{transform:translateX(1260px)}}}}
"""
    defs = (f'<linearGradient id="cmg" x1="0" x2="1"><stop offset="0" stop-color="{accent}" stop-opacity="0"/><stop offset="1" stop-color="{accent}"/></linearGradient>'
            f'<radialGradient id="hdg" cx="0%" cy="0%" r="60%"><stop offset="0" stop-color="{accent}" stop-opacity=".14"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="hcl"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    body = (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{BG}" stroke="{LINE}"/>'
            f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="url(#hdg)"/>'
            f'<g class="in"><text class="mono" x="30" y="32" font-size="12" fill="{accent}" letter-spacing="2.5">FILE {num} / 07</text>'
            f'<text class="serif" x="28" y="70" font-size="34" font-weight="600" fill="{TEXT}" letter-spacing="-.5">{esc(title)}</text>'
            f'<text class="mono" x="{W-30}" y="68" text-anchor="end" font-size="12" fill="{MUTED}" letter-spacing="1.2">{esc(note)}</text></g>'
            f'<line class="ul" x1="30" y1="{H-1}" x2="{W-30}" y2="{H-1}" stroke="{accent}" stroke-opacity=".5"/>'
            f'<g clip-path="url(#hcl)"><rect class="cm" x="0" y="{H-3}" width="80" height="3" rx="1.5" fill="url(#cmg)"/></g>')
    write(f"h_{slug}.svg", W, H, body, css, defs)

# =====================================================================
# 3. TERMINAL
# =====================================================================
def terminal():
    W = 1200
    lines = [
        ("cmd", "whoami"),
        ("out", [("karri vamsi krishna", TEXT), ("  ·  forward-deployed AI engineer  ·  hyderabad, in", MUTED)]),
        ("cmd", "cat role.txt"),
        ("out", [("junior data scientist", AMBER), (" @ SciTech Patent Art  —  patent & legal document intelligence", MUTED)]),
        ("cmd", "ls ./shipped"),
        ("out", [("patent-extraction/  claim-charts/  legal-rag/  jobhunterx/  referentweave/  atrophy/", CYAN)]),
        ("cmd", "./impact --summary"),
        ("out", [("✔ ", GREEN), ("95%+ accuracy   ", TEXT), ("✔ ", GREEN), ("90–95% lower cost   ", TEXT), ("✔ ", GREEN), ("$0.80 / 1k pages   ", TEXT), ("✔ ", GREEN), ("3–5× cheaper", TEXT)]),
        ("cmd", "cat trophy.txt"),
        ("out", [("★ 1st place", AMBER), ("  —  IKDD Agentic AI Challenge · CODS 2025 · IISER Pune", MUTED)]),
    ]
    top, lh = 74, 31
    H = top + lh * len(lines) + 34
    t, body_lines = 0.6, ""
    for i, (kind, content) in enumerate(lines):
        y = top + i * lh
        if kind == "cmd":
            n = len(content)
            dur = 0.035 * n + 0.12
            body_lines += (f'<g class="ln" style="animation-delay:{t:.2f}s"><text class="mono" x="40" y="{y}" font-size="16" fill="{GREEN}">➜</text>'
                           f'<text class="mono" x="64" y="{y}" font-size="16" fill="{VIOLET}">~</text></g>'
                           f'<text class="mono type" x="88" y="{y}" font-size="16" fill="{TEXT}" style="animation:type {dur:.2f}s steps({n}) {t:.2f}s both">{esc(content)}</text>')
            t += dur + 0.18
        else:
            spans = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in content)
            body_lines += f'<text class="mono ln" x="64" y="{y}" font-size="15" style="animation-delay:{t:.2f}s" xml:space="preserve">{spans}</text>'
            t += 0.32
    cy = top + lh * len(lines)
    body_lines += (f'<g class="ln" style="animation-delay:{t:.2f}s"><text class="mono" x="40" y="{cy}" font-size="16" fill="{GREEN}">➜</text>'
                   f'<text class="mono" x="64" y="{cy}" font-size="16" fill="{VIOLET}">~</text>'
                   f'<rect class="cur" x="88" y="{cy-15}" width="10" height="19" fill="{AMBER}"/></g>')
    css = f"""
.ln{{animation:ln .35s ease-out both}}@keyframes ln{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:none}}}}
@keyframes type{{from{{clip-path:inset(0 100% 0 0)}}to{{clip-path:inset(0 0 0 0)}}}}
.cur{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}
"""
    defs = glow_defs("t", "100%", "0%", VIOLET, .12, "60%")
    body = (card_bg(W, H, 16, True, "t") +
            f'<rect x="0.5" y="0.5" width="{W-1}" height="40" rx="16" fill="{PANEL}"/><rect x="0.5" y="24" width="{W-1}" height="17" fill="{PANEL}"/>'
            f'<line x1="0" y1="41" x2="{W}" y2="41" stroke="{LINE}"/>'
            f'<circle cx="26" cy="21" r="6" fill="#FF5F57"/><circle cx="46" cy="21" r="6" fill="#FEBC2E"/><circle cx="66" cy="21" r="6" fill="#28C840"/>'
            f'<text class="mono" x="{W/2}" y="26" text-anchor="middle" font-size="13" fill="{MUTED}">kvcops@archive: ~ — zsh</text>'
            f'<text class="mono" x="{W-24}" y="26" text-anchor="end" font-size="12" fill="{DIM}">utf-8 · 120×{len(lines)+1}</text>'
            + body_lines)
    write("terminal.svg", W, H, body, css, defs)

# =====================================================================
# 4. IMPACT METERS
# =====================================================================
def impact():
    W, H = 1200, 300
    cards = [
        ("95%+", "claim-chart accuracy", "manual baseline was 30–40%", 0.95, GREEN),
        ("90–95%", "lower processing cost", "vs. manual Acrobat workflow", 0.92, AMBER),
        ("3–5×", "cheaper patent extraction", "US / EP / JP · OCR + non-OCR", 0.78, CYAN),
        ("$0.80", "per 1,000 pages", "per-line coordinate extraction", 0.64, VIOLET),
    ]
    cw, gap, x0 = 276, 12, 18
    s = ""
    for i, (big, lab, sub, frac, col) in enumerate(cards):
        x = x0 + i * (cw + gap)
        d = 0.2 + i * 0.18
        s += (f'<g class="up" style="animation-delay:{d:.2f}s">'
              f'<rect x="{x}" y="20" width="{cw}" height="{H-40}" rx="16" fill="{PANEL}" stroke="{LINE}"/>'
              f'<rect x="{x+22}" y="20" width="{cw-44}" height="2" rx="1" fill="{col}" fill-opacity=".9"/>'
              f'<text class="mono" x="{x+22}" y="56" font-size="11" fill="{DIM}" letter-spacing="2">METRIC 0{i+1}</text>'
              f'<text class="serif" x="{x+20}" y="128" font-size="58" font-weight="600" fill="{col}" letter-spacing="-1">{esc(big)}</text>'
              f'<text class="sans" x="{x+22}" y="164" font-size="17" font-weight="600" fill="{TEXT}">{esc(lab)}</text>'
              f'<text class="sans" x="{x+22}" y="188" font-size="13" fill="{MUTED}">{esc(sub)}</text>'
              f'<rect x="{x+22}" y="222" width="{cw-44}" height="8" rx="4" fill="{PANEL2}" stroke="{LINE}"/>'
              f'<rect class="bar" x="{x+22}" y="222" width="{(cw-44)*frac:.0f}" height="8" rx="4" fill="{col}" style="animation-delay:{d+0.4:.2f}s"/>'
              f'<circle class="spark" cx="{x+22+(cw-44)*frac:.0f}" cy="226" r="5" fill="{col}" style="animation-delay:{d+1.6:.2f}s"/>'
              f'<text class="mono" x="{x+22}" y="254" font-size="11" fill="{DIM}" letter-spacing="1.2">MEASURED IN PRODUCTION</text></g>')
    css = f"""
.up{{animation:up .9s cubic-bezier(.2,.8,.2,1) both}}@keyframes up{{from{{opacity:0;transform:translateY(22px)}}to{{opacity:1;transform:none}}}}
.bar{{transform-box:fill-box;transform-origin:left;animation:bar 1.6s cubic-bezier(.6,0,.2,1) both}}@keyframes bar{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
.spark{{opacity:0;transform-box:fill-box;transform-origin:center;animation:spark 2.4s ease-out infinite}}@keyframes spark{{0%{{opacity:.9;transform:scale(.6)}}100%{{opacity:0;transform:scale(2.6)}}}}
"""
    write("impact.svg", W, H, s, css)

# =====================================================================
# 5. EXPERIENCE TIMELINE
# =====================================================================
def timeline():
    W = 1200
    jobs = [
        ("MAR 2026 — PRESENT", "Junior Data Scientist", "SciTech Patent Art Services · Hyderabad", AMBER, "NOW", [
            "Patent extraction (US/EP/JP): Azure OCR, Docling, PP-DocLayout + Gemini bounding boxes → 3–5× lower cost",
            "Claim charts: OpenCV rectangle-merge + multi-agent spillover detection → 95%+ accuracy, 90–95% cheaper",
            "Non-table claim charts with per-line coordinates at $0.80 / 1,000 pages · fully async auto-matching",
            "Legal RAG chatbot, Selenium web-to-PDF engine, Whisper video pipeline for legal documentation",
        ]),
        ("AUG 2025 — MAR 2026", "AI Software Engineer L1", "Gyan Data · Chennai", CYAN, "PROMOTED", [
            "Telemetry AI dashboard: autonomous agents, natural-language queries, streamed tokens, live Plotly",
            "Graph-RAG backend: FastAPI + LightRAG + Neo4j with domain-constrained graph selection",
            "DB-agnostic chatbot: LangGraph, Google Auth, OpenRouter / Gemini / OpenAI / Ollama, LangSmith",
        ]),
        ("JAN 2025 — JUL 2025", "Data Science Intern", "Gyan Data · Chennai", VIOLET, "CONVERTED", [
            "ERP customization + AI chatbot development → direct full-time conversion offer",
        ]),
    ]
    y, s, items = 40, "", []
    for i, (date, role, org, col, tag, bullets) in enumerate(jobs):
        h = 86 + len(bullets) * 26
        items.append((y, h, date, role, org, col, tag, bullets, i))
        y += h + 22
    H = y + 10
    total = H - 60
    s += f'<line x1="56" y1="40" x2="56" y2="{H-40}" stroke="{LINE}" stroke-width="2"/>'
    s += f'<line class="draw" x1="56" y1="40" x2="56" y2="{H-40}" stroke="{AMBER}" stroke-width="2" style="stroke-dasharray:{total};stroke-dashoffset:{total}"/>'
    s += f'<circle r="4" fill="{AMBER}"><animateMotion dur="5s" repeatCount="indefinite" path="M56,40 L56,{H-40}"/><animate attributeName="opacity" values="0;1;1;0" dur="5s" repeatCount="indefinite"/></circle>'
    for (y, h, date, role, org, col, tag, bullets, i) in items:
        d = 0.3 + i * 0.45
        tagw = tw(tag, 11, True) + 22
        s += (f'<g class="up" style="animation-delay:{d:.2f}s">'
              f'<circle class="ring" cx="56" cy="{y+18}" r="13" fill="{col}" fill-opacity=".15" style="animation-delay:{d:.2f}s"/>'
              f'<circle cx="56" cy="{y+18}" r="7" fill="{BG}" stroke="{col}" stroke-width="2.5"/>'
              f'<rect x="92" y="{y-6}" width="{W-110}" height="{h}" rx="14" fill="{PANEL}" stroke="{LINE}"/>'
              f'<text class="mono" x="116" y="{y+22}" font-size="12" fill="{col}" letter-spacing="2">{date}</text>'
              f'<rect x="{W-40-tagw:.0f}" y="{y+6}" width="{tagw:.0f}" height="24" rx="12" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5"/>'
              f'<text class="mono" x="{W-40-tagw/2:.0f}" y="{y+22}" text-anchor="middle" font-size="11" fill="{col}" letter-spacing="1.5">{tag}</text>'
              f'<text class="serif" x="116" y="{y+54}" font-size="25" font-weight="600" fill="{TEXT}">{esc(role)}'
              f'<tspan class="sans" font-size="15" font-weight="400" fill="{MUTED}">   @ {esc(org)}</tspan></text>')
        for j, b in enumerate(bullets):
            by = y + 86 + j * 26
            s += (f'<g class="ln" style="animation-delay:{d+0.35+j*0.12:.2f}s"><text class="mono" x="118" y="{by}" font-size="13" fill="{col}">▸</text>'
                  f'<text class="sans" x="138" y="{by}" font-size="14.5" fill="{TEXT}" fill-opacity=".88">{esc(b)}</text></g>')
        s += "</g>"
    css = f"""
.draw{{animation:draw 2.6s cubic-bezier(.6,0,.2,1) .2s forwards}}@keyframes draw{{to{{stroke-dashoffset:0}}}}
.up{{animation:up .8s cubic-bezier(.2,.8,.2,1) both}}@keyframes up{{from{{opacity:0;transform:translateX(16px)}}to{{opacity:1;transform:none}}}}
.ln{{animation:ln .5s ease-out both}}@keyframes ln{{from{{opacity:0}}to{{opacity:1}}}}
.ring{{transform-box:fill-box;transform-origin:center;animation:ring 2.8s ease-out infinite}}@keyframes ring{{0%{{transform:scale(.6);opacity:1}}100%{{transform:scale(2);opacity:0}}}}
"""
    write("experience.svg", W, H, s, css)

# =====================================================================
# 6. AGENT PIPELINE (JobHunterX)
# =====================================================================
def agents():
    W, H = 1200, 400
    names = [("Profiler", "resume → profile"), ("Planner", "targeted queries"), ("Scout", "scrapes ATS job boards"),
             ("Gate", "zero-token filter"), ("Evaluator", "score vs profile"), ("Tailor", "PDF per job")]
    n = len(names); bw, bh = 162, 92; gap = (W - 60 - n * bw) / (n - 1); y = 150
    s = ""
    xs = [30 + i * (bw + gap) for i in range(n)]
    # router bar
    s += (f'<g class="up" style="animation-delay:.1s"><rect x="30" y="52" width="{W-60}" height="44" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-dasharray="4 4"/>'
          f'<text class="mono" x="52" y="79" font-size="12" fill="{VIOLET}" letter-spacing="2">MULTI-LLM ROUTER</text>'
          f'<text class="sans" x="230" y="79" font-size="14" fill="{TEXT}">Gemini / Gemma  ·  Groq Llama  ·  Mistral   —   automatic failover · budget caps · disk cache</text></g>')
    for i, x in enumerate(xs):
        s += f'<line x1="{x+bw/2:.0f}" y1="96" x2="{x+bw/2:.0f}" y2="{y}" stroke="{VIOLET}" stroke-opacity=".35" stroke-dasharray="3 5" class="dash"/>'
    # connectors
    for i in range(n - 1):
        x1 = xs[i] + bw; x2 = xs[i + 1]; yy = y + bh / 2
        d = f"M{x1:.0f},{yy} L{x2:.0f},{yy}"
        s += f'<path d="{d}" stroke="{LINE}" stroke-width="2"/>'
        s += (f'<circle r="4" fill="{AMBER}"><animateMotion dur="1.1s" begin="{i*0.55:.2f}s" repeatCount="indefinite" path="{d}"/>'
              f'<animate attributeName="opacity" values="0;1;1;0" dur="1.1s" begin="{i*0.55:.2f}s" repeatCount="indefinite"/></circle>')
        s += f'<path d="M{x2-7:.0f},{yy-5} L{x2-1:.0f},{yy} L{x2-7:.0f},{yy+5}" stroke="{DIM}" stroke-width="1.6" fill="none"/>'
    for i, (nm, sub) in enumerate(names):
        x = xs[i]; d = 0.3 + i * 0.15
        col = GREEN if i == n - 1 else AMBER
        s += (f'<g class="up" style="animation-delay:{d:.2f}s">'
              f'<rect x="{x:.0f}" y="{y}" width="{bw}" height="{bh}" rx="14" fill="{PANEL}" stroke="{LINE}"/>'
              f'<rect class="act" x="{x:.0f}" y="{y}" width="{bw}" height="{bh}" rx="14" fill="none" stroke="{col}" stroke-width="1.6" style="animation-delay:{i*0.55:.2f}s"/>'
              f'<text class="mono" x="{x+16:.0f}" y="{y+26}" font-size="11" fill="{col}" letter-spacing="2">AGENT 0{i+1}</text>'
              f'<text class="serif" x="{x+16:.0f}" y="{y+55}" font-size="21" font-weight="600" fill="{TEXT}">{nm}</text>'
              f'<text class="sans" x="{x+16:.0f}" y="{y+76}" font-size="11.5" fill="{MUTED}">{esc(sub)}</text></g>')
    # HITL under last two
    hx = xs[n - 1] + bw - (bw + 130); hy = 300
    s += (f'<path d="M{xs[n-1]+bw/2:.0f},{y+bh} L{xs[n-1]+bw/2:.0f},{hy}" stroke="{CYAN}" stroke-opacity=".6" stroke-dasharray="4 4" class="dash"/>'
          f'<g class="up" style="animation-delay:1.4s"><rect x="{hx:.0f}" y="{hy}" width="{bw+130}" height="58" rx="12" fill="{PANEL}" stroke="{CYAN}" stroke-opacity=".6"/>'
          f'<circle class="blink" cx="{hx+20:.0f}" cy="{hy+29}" r="5" fill="{CYAN}"/>'
          f'<text class="mono" x="{hx+34:.0f}" y="{hy+25}" font-size="11" fill="{CYAN}" letter-spacing="1.8">BROWSER AGENT · HITL</text>'
          f'<text class="sans" x="{hx+34:.0f}" y="{hy+45}" font-size="12" fill="{MUTED}">human takeover for CAPTCHA / login / MFA</text></g>')
    s += (f'<g class="up" style="animation-delay:1.6s"><text class="mono" x="30" y="316" font-size="12" fill="{DIM}" letter-spacing="1.5">ONE LANGGRAPH STATE MACHINE</text>'
          f'<text class="serif" x="30" y="350" font-size="30" font-weight="600" fill="{TEXT}">6 <tspan fill="{AMBER}">agents</tspan> · 85 <tspan fill="{AMBER}">tests</tspan> · 3 <tspan fill="{AMBER}">LLM houses</tspan></text>'
          f'<text class="sans" x="30" y="378" font-size="13" fill="{MUTED}">Live progress streamed over CDP + WebSockets to a FastAPI dashboard.</text></g>')
    css = f"""
.up{{animation:up .8s cubic-bezier(.2,.8,.2,1) both}}@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.act{{opacity:0;animation:act {0.55*n:.2f}s linear infinite}}@keyframes act{{0%{{opacity:0}}6%{{opacity:1}}22%{{opacity:1}}30%,100%{{opacity:0}}}}
.dash{{animation:dash 1.2s linear infinite}}@keyframes dash{{to{{stroke-dashoffset:-16}}}}
.blink{{animation:bl 1.2s ease-in-out infinite}}@keyframes bl{{50%{{opacity:.2}}}}
"""
    body = card_bg(W, H, 18, True, "a") + f'<text class="mono" x="30" y="34" font-size="12" fill="{AMBER}" letter-spacing="2.5">EXHIBIT · JOBHUNTERX ARCHITECTURE</text>' + s
    write("agents.svg", W, H, body, css, glow_defs("a", "50%", "0%", AMBER, .10, "60%"))

# =====================================================================
# 7. PROJECT CARDS
# =====================================================================
def project(slug, tag, title, lines, metric, metric_lab, stack, url_txt, col, visual=None):
    W, H = 590, 310
    per = 2 * (W + H - 4 * 18) + 2 * math.pi * 18
    chips, cx = "", 28
    for c in stack:
        cw = tw(c, 12, True) + 20
        if cx + cw > W - 28: break
        chips += (f'<rect x="{cx:.0f}" y="232" width="{cw:.0f}" height="26" rx="13" fill="{PANEL2}" stroke="{LINE}"/>'
                  f'<text class="mono" x="{cx+cw/2:.0f}" y="249" text-anchor="middle" font-size="12" fill="{MUTED}">{esc(c)}</text>')
        cx += cw + 8
    desc = "".join(f'<text class="sans" x="28" y="{120+i*21}" font-size="14.5" fill="{TEXT}" fill-opacity=".85">{esc(t)}</text>' for i, t in enumerate(lines))
    vis = visual(W - 200, 70, col) if visual else ""
    css = f"""
.comet{{stroke-dasharray:120 {per-120:.0f};animation:comet 6s linear infinite}}@keyframes comet{{to{{stroke-dashoffset:-{per:.0f}}}}}
.up{{animation:up .9s cubic-bezier(.2,.8,.2,1) both}}@keyframes up{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
.bar{{transform-box:fill-box;transform-origin:left;animation:bar 1.5s .6s cubic-bezier(.6,0,.2,1) both}}@keyframes bar{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
.grow{{transform-box:fill-box;transform-origin:bottom;animation:gr 1.2s cubic-bezier(.6,0,.2,1) both}}@keyframes gr{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
.blink{{animation:bl 1.4s ease-in-out infinite}}@keyframes bl{{50%{{opacity:.25}}}}
.go{{animation:go 1.6s ease-in-out infinite}}@keyframes go{{50%{{transform:translateX(5px)}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2.6s ease-out infinite}}@keyframes pulse{{0%{{transform:scale(.6);opacity:.9}}100%{{transform:scale(2.2);opacity:0}}}}
"""
    defs = glow_defs("p", "100%", "0%", col, .16, "65%")
    body = (f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="{BG}" stroke="{LINE}"/>'
            f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="url(#pglow)"/>'
            f'<rect class="comet" x="1" y="1" width="{W-2}" height="{H-2}" rx="18" stroke="{col}" stroke-width="1.6" stroke-linecap="round"/>'
            f'<g class="up"><text class="mono" x="28" y="42" font-size="11.5" fill="{col}" letter-spacing="2.2">{esc(tag)}</text>'
            f'<text class="serif" x="26" y="88" font-size="36" font-weight="600" fill="{TEXT}" letter-spacing="-.5">{esc(title)}</text>'
            f'{desc}'
            f'<text x="28" y="212"><tspan class="serif" font-size="30" font-weight="600" fill="{col}">{esc(metric)}</tspan>'
            f'<tspan class="sans" dx="10" font-size="13" fill="{MUTED}">{esc(metric_lab)}</tspan></text>'
            f'{chips}'
            f'<text class="mono" x="28" y="290" font-size="12" fill="{DIM}">{esc(url_txt)}</text>'
            f'<g class="go"><text class="mono" x="{W-28}" y="290" text-anchor="end" font-size="13" fill="{col}">open →</text></g></g>'
            f'{vis}')
    write(f"p_{slug}.svg", W, H, body, css, defs)

# every visual lives in a 172x150 box starting at (x0, y0)
def vis_recall(x0, y0, col):
    s = f'<g class="up" style="animation-delay:.3s"><text class="mono" x="{x0}" y="{y0+8}" font-size="10.5" fill="{DIM}" letter-spacing="1.5">RECALL@1 · N=60</text>'
    for i, (lab, v, c) in enumerate([("standard", .183, DIM), ("weave", .633, col)]):
        y = y0 + 26 + i * 48
        s += (f'<text class="mono" x="{x0}" y="{y}" font-size="11" fill="{MUTED}">{lab}</text>'
              f'<rect x="{x0}" y="{y+8}" width="172" height="14" rx="4" fill="{PANEL2}"/>'
              f'<rect class="bar" x="{x0}" y="{y+8}" width="{172*v:.0f}" height="14" rx="4" fill="{c}" style="animation-delay:{.6+i*.3}s"/>'
              f'<text class="mono" x="{x0+172}" y="{y}" text-anchor="end" font-size="11.5" fill="{TEXT}">{v*100:.1f}%</text>')
    s += f'<text class="mono" x="{x0}" y="{y0+136}" font-size="10.5" fill="{DIM}">R@3 98.3% · R@5 100%</text>'
    return s + "</g>"

def vis_nodes(x0, y0, col):
    s = '<g class="up" style="animation-delay:.3s">'
    pts = [(x0+10, y0+20), (x0+86, y0+6), (x0+162, y0+20), (x0+40, y0+90), (x0+120, y0+90), (x0+86, y0+140)]
    eds = [(0, 1), (1, 2), (0, 3), (1, 4), (2, 4), (3, 4), (3, 5), (4, 5)]
    for k, (a, b) in enumerate(eds):
        d = f"M{pts[a][0]},{pts[a][1]} L{pts[b][0]},{pts[b][1]}"
        s += (f'<path d="{d}" stroke="{LINE}" stroke-width="1.4"/>'
              f'<circle r="2.6" fill="{col}"><animateMotion dur="1.8s" begin="{k*0.25:.2f}s" repeatCount="indefinite" path="{d}"/></circle>')
    for i, (x, y) in enumerate(pts):
        s += (f'<circle class="pulse" cx="{x}" cy="{y}" r="9" fill="{col}" fill-opacity=".18" style="animation-delay:{i*0.4:.1f}s"/>'
              f'<circle cx="{x}" cy="{y}" r="5" fill="{BG}" stroke="{col}" stroke-width="2"/>')
    return s + "</g>"

def vis_decay(x0, y0, col):
    s = f'<g class="up" style="animation-delay:.3s"><text class="mono" x="{x0}" y="{y0+8}" font-size="10.5" fill="{DIM}" letter-spacing="1.5">SKILL DECAY · 10 AXES</text>'
    vals = [.9, .8, .72, .65, .5, .62, .4, .35, .55, .3]
    for i, v in enumerate(vals):
        x = x0 + i * 17.5; h = 110 * v; base = y0 + 140
        s += (f'<rect x="{x:.1f}" y="{base-110}" width="11" height="110" rx="3" fill="{PANEL2}"/>'
              f'<rect class="grow" x="{x:.1f}" y="{base-h:.0f}" width="11" height="{h:.0f}" rx="3" fill="{col}" fill-opacity="{0.35+0.6*v:.2f}" style="animation-delay:{.5+i*.08:.2f}s"/>')
    return s + "</g>"

def vis_badge(text, live=False):
    def f(x0, y0, col):
        s = (f'<g class="up" style="animation-delay:.3s"><circle class="pulse" cx="{x0+86}" cy="{y0+70}" r="44" fill="{col}" fill-opacity=".10"/>'
             f'<circle cx="{x0+86}" cy="{y0+70}" r="46" stroke="{col}" stroke-opacity=".35" stroke-dasharray="3 6"/>'
             f'<circle cx="{x0+86}" cy="{y0+70}" r="34" fill="{PANEL}" stroke="{col}" stroke-opacity=".7"/>')
        if live:
            s += (f'<circle class="blink" cx="{x0+66}" cy="{y0+70}" r="5" fill="{col}"/>'
                  f'<text class="mono" x="{x0+76}" y="{y0+75}" font-size="13" fill="{col}" letter-spacing="1.5">LIVE</text>')
        else:
            s += f'<text class="serif" x="{x0+86}" y="{y0+79}" text-anchor="middle" font-size="24" font-weight="600" fill="{col}">{esc(text)}</text>'
        return s + "</g>"
    return f

# =====================================================================
# 8. STACK
# =====================================================================
def stack():
    W = 1200
    groups = [
        ("AGENTS & ORCHESTRATION", AMBER, ["LangGraph", "LangChain", "Multi-Agent Systems", "Tool / Function Calling", "MCP", "Browser Use", "Playwright agents", "Human-in-the-Loop", "Agent Memory"]),
        ("LLM ENGINEERING", VIOLET, ["Prompt & Context Eng.", "Structured Outputs", "Multi-LLM Routing", "Token Streaming", "LangSmith Evals", "Cost / Latency Tuning"]),
        ("RAG & RETRIEVAL", CYAN, ["Production RAG", "Graph-RAG", "LightRAG", "Neo4j", "Hybrid BM25 + Dense", "RRF", "Reranking", "FAISS", "Jina Embeddings"]),
        ("MODELS & APIS", GREEN, ["OpenAI", "Anthropic Claude", "Gemini", "OpenRouter", "Groq", "Mistral", "Ollama", "Hugging Face", "Whisper"]),
        ("DOCUMENT INTELLIGENCE", ORANGE, ["Azure OCR", "Docling", "PP-DocLayout", "OpenCV", "Multimodal Extraction", "Coordinate Mapping"]),
        ("BACKEND & SHIPPING", TEXT, ["Python", "FastAPI", "Flask", "WebSockets", "PostgreSQL", "SQLite", "Docker", "Git", "Selenium", "Streamlit", "GCP", "Render", "Vercel"]),
    ]
    y, s, k = 34, "", 0
    lab_w = 250
    for gi, (lab, col, chips) in enumerate(groups):
        x = lab_w + 20; rows = 1
        s += (f'<g class="up" style="animation-delay:{gi*0.12:.2f}s"><circle cx="34" cy="{y+14}" r="4" fill="{col}"/>'
              f'<text class="mono" x="48" y="{y+18}" font-size="12" fill="{col}" letter-spacing="1.8">{esc(lab)}</text></g>')
        for c in chips:
            cw = tw(c, 13) + 26
            if x + cw > W - 24:
                x = lab_w + 20; y += 38; rows += 1
            s += (f'<g class="chip" style="animation-delay:{0.25+k*0.035:.3f}s"><rect x="{x:.0f}" y="{y}" width="{cw:.0f}" height="28" rx="8" fill="{PANEL}" stroke="{LINE}"/>'
                  f'<rect x="{x:.0f}" y="{y}" width="3" height="28" rx="1.5" fill="{col}" fill-opacity=".8"/>'
                  f'<text class="sans" x="{x+cw/2+1:.0f}" y="{y+19}" text-anchor="middle" font-size="13" fill="{TEXT}">{esc(c)}</text></g>')
            x += cw + 8; k += 1
        y += 38 + 16
        if gi < len(groups) - 1:
            s += f'<line x1="24" y1="{y-8}" x2="{W-24}" y2="{y-8}" stroke="{LINE}" stroke-dasharray="2 6"/>'
    H = y + 14
    css = """
.up{animation:up .7s cubic-bezier(.2,.8,.2,1) both}@keyframes up{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}
.chip{animation:chip .6s cubic-bezier(.2,.8,.2,1) both}@keyframes chip{from{opacity:0;transform:translateY(8px) scale(.96)}to{opacity:1;transform:none}}
"""
    write("stack.svg", W, H, card_bg(W, H, 18, True, "s") + s, css, glow_defs("s", "0%", "0%", AMBER, .10, "55%"))

# =====================================================================
# 9. RECORD (achievements + education)
# =====================================================================
def record():
    W, H = 1200, 470
    s = ""
    # trophy card
    s += (f'<g class="up"><rect x="20" y="20" width="560" height="{H-40}" rx="18" fill="{PANEL}" stroke="{LINE}"/>'
          f'<rect x="20" y="20" width="560" height="{H-40}" rx="18" fill="url(#gold)"/>'
          f'<text class="mono" x="48" y="60" font-size="12" fill="{AMBER}" letter-spacing="2.5">CODS 2025 · IISER PUNE</text>'
          f'<text class="serif shine" x="44" y="200" font-size="150" font-weight="700" fill="url(#goldtxt)" letter-spacing="-6">1st</text>'
          f'<text class="serif" x="48" y="252" font-size="26" font-weight="600" fill="{TEXT}">IKDD Agentic AI Challenge</text>'
          f'<text class="sans" x="48" y="282" font-size="14.5" fill="{MUTED}">AssetOpsBench — multi-agent AI for industrial</text>'
          f'<text class="sans" x="48" y="304" font-size="14.5" fill="{MUTED}">predictive maintenance, fault diagnosis &amp; work orders.</text>'
          f'<rect x="48" y="{H-104}" width="180" height="40" rx="20" fill="{AMBER}" fill-opacity=".12" stroke="{AMBER}" stroke-opacity=".6"/>'
          f'<text class="mono" x="138" y="{H-79}" text-anchor="middle" font-size="13" fill="{AMBER}" letter-spacing="1.5">★ WINNER</text>')
    for i in range(14):
        a = i / 14 * 2 * math.pi; r = 120
        x, y = 470 + r * 0.5 * math.cos(a), 150 + r * 0.5 * math.sin(a)
        s += f'<circle class="orb" cx="{x:.0f}" cy="{y:.0f}" r="2.2" fill="{AMBER}" style="animation-delay:{i*0.15:.2f}s"/>'
    s += f'<g class="spin"><circle cx="470" cy="150" r="44" stroke="{AMBER}" stroke-opacity=".5" stroke-dasharray="3 7"/></g>'
    s += f'<circle cx="470" cy="150" r="24" fill="{AMBER}" fill-opacity=".14" stroke="{AMBER}"/><text class="serif" x="470" y="160" text-anchor="middle" font-size="26" fill="{AMBER}">★</text></g>'
    # right column
    rx = 600
    blocks = [
        ("HACKATHONS & LEADERSHIP", VIOLET, ["2nd Round — Adobe GenSolve Hackathon", "IBC National Hackathon — built & pitched live", "Organizer & Team Lead — IEEE Mystical Code"]),
        ("CERTIFICATIONS", CYAN, ["CCSK Cloud Security (Cohort-5) · Google Cloud Gen AI", "Juniper Networks · Infosys AI · Salesforce Developer"]),
    ]
    y = 20
    for bi, (lab, col, rows) in enumerate(blocks):
        h = 54 + 26 * len(rows)
        s += (f'<g class="up" style="animation-delay:{0.2+bi*0.2:.1f}s"><rect x="{rx}" y="{y}" width="580" height="{h}" rx="16" fill="{PANEL}" stroke="{LINE}"/>'
              f'<text class="mono" x="{rx+26}" y="{y+32}" font-size="12" fill="{col}" letter-spacing="2.2">{esc(lab)}</text>')
        for j, r in enumerate(rows):
            s += (f'<text class="mono" x="{rx+26}" y="{y+60+j*26}" font-size="13" fill="{col}">▸</text>'
                  f'<text class="sans" x="{rx+46}" y="{y+60+j*26}" font-size="14.5" fill="{TEXT}">{esc(r)}</text>')
        s += "</g>"
        y += h + 14
    # education
    eh = H - 20 - y
    s += (f'<g class="up" style="animation-delay:.6s"><rect x="{rx}" y="{y}" width="580" height="{eh}" rx="16" fill="{PANEL}" stroke="{LINE}"/>'
          f'<text class="mono" x="{rx+26}" y="{y+32}" font-size="12" fill="{GREEN}" letter-spacing="2.2">EDUCATION</text>')
    edu = [("B.Tech CSE — Gayatri Vidya Parishad College of Engg. (A)", "2021–25", "8.97 CGPA"),
           ("Intermediate MPC — Sri Chaitanya Jr. College, Steel Plant", "2019–21", "97.7%"),
           ("SSC — Sri Chaitanya EM School, Anakapalle", "2019", "9.8 GPA")]
    for j, (a, b, c) in enumerate(edu):
        yy = y + 62 + j * 28
        s += (f'<text class="sans" x="{rx+26}" y="{yy}" font-size="13.5" fill="{TEXT}">{esc(a)}</text>'
              f'<text class="mono" x="{rx+470}" y="{yy}" text-anchor="end" font-size="12" fill="{DIM}">{b}</text>'
              f'<text class="mono" x="{rx+556}" y="{yy}" text-anchor="end" font-size="13" fill="{GREEN}">{c}</text>')
    s += "</g>"
    css = f"""
.up{{animation:up .8s cubic-bezier(.2,.8,.2,1) both}}@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.spin{{transform-box:fill-box;transform-origin:center;animation:spin 14s linear infinite}}@keyframes spin{{to{{transform:rotate(360deg)}}}}
.orb{{animation:orb 2.1s ease-in-out infinite}}@keyframes orb{{0%,100%{{opacity:.15}}50%{{opacity:1}}}}
"""
    defs = (f'<radialGradient id="gold" cx="85%" cy="15%" r="70%"><stop offset="0" stop-color="{AMBER}" stop-opacity=".20"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="goldtxt" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#FFF1C9"/><stop offset=".4" stop-color="{AMBER}"/><stop offset=".55" stop-color="#FFF6DD"/><stop offset=".7" stop-color="{AMBER}"/><stop offset="1" stop-color="{ORANGE}"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" values="-1 -1;1 1;-1 -1" dur="5s" repeatCount="indefinite"/></linearGradient>')
    write("record.svg", W, H, s, css, defs)

# =====================================================================
# 10. DIVIDER, BUTTONS, FOOTER
# =====================================================================
def divider():
    W, H = 1200, 30
    css = ".cm{animation:cm 5s linear infinite}@keyframes cm{from{transform:translateX(-240px)}to{transform:translateX(1260px)}}"
    defs = f'<linearGradient id="cg" x1="0" x2="1"><stop offset="0" stop-color="{AMBER}" stop-opacity="0"/><stop offset=".85" stop-color="{AMBER}"/><stop offset="1" stop-color="#FFF1C9"/></linearGradient>'
    body = (f'<line x1="0" y1="15" x2="1200" y2="15" stroke="{AMBER}" stroke-opacity=".18"/>'
            f'<g class="cm"><rect x="0" y="14" width="240" height="2" rx="1" fill="url(#cg)"/><circle cx="240" cy="15" r="3" fill="#FFF1C9"/></g>'
            f'<circle cx="600" cy="15" r="3.5" fill="{BG}" stroke="{AMBER}" stroke-opacity=".7"/>')
    write("divider.svg", W, H, body, css, defs)

def button(slug, label, sub, col, icon_path):
    W, H = 280, 64
    css = (".sh{animation:sh 3.6s ease-in-out infinite}@keyframes sh{0%{transform:translateX(-120px)}60%,100%{transform:translateX(420px)}}"
           ".ar{animation:ar 1.6s ease-in-out infinite}@keyframes ar{50%{transform:translateX(4px)}}")
    defs = (f'<linearGradient id="shg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".14"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="bc"><rect width="{W}" height="{H}" rx="14"/></clipPath>')
    body = (f'<g clip-path="url(#bc)"><rect width="{W}" height="{H}" fill="{PANEL}"/>'
            f'<rect width="4" height="{H}" fill="{col}"/>'
            f'<rect class="sh" x="0" y="0" width="90" height="{H}" fill="url(#shg)" transform="skewX(-20)"/></g>'
            f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" stroke="{col}" stroke-opacity=".45"/>'
            f'<g transform="translate(22 20)">{icon_path(col)}</g>'
            f'<text class="sans" x="64" y="29" font-size="16" font-weight="600" fill="{TEXT}">{esc(label)}</text>'
            f'<text class="mono" x="64" y="47" font-size="11" fill="{MUTED}">{esc(sub)}</text>'
            f'<g class="ar"><text class="mono" x="{W-22}" y="38" text-anchor="end" font-size="16" fill="{col}">→</text></g>')
    write(f"btn_{slug}.svg", W, H, body, css, defs)

ICON_GLOBE = lambda c: f'<circle cx="12" cy="12" r="10" stroke="{c}" stroke-width="1.8"/><ellipse cx="12" cy="12" rx="4.5" ry="10" stroke="{c}" stroke-width="1.6"/><line x1="2" y1="12" x2="22" y2="12" stroke="{c}" stroke-width="1.6"/>'
ICON_IN = lambda c: f'<rect x="1" y="1" width="22" height="22" rx="5" stroke="{c}" stroke-width="1.8"/><rect x="5.5" y="9.5" width="2.6" height="8.5" fill="{c}"/><circle cx="6.8" cy="6.4" r="1.6" fill="{c}"/><path d="M11 18v-8.5h2.5v1.3c.6-1 1.6-1.6 3-1.6 2.1 0 3 1.3 3 3.7V18h-2.6v-4.7c0-1.2-.4-1.9-1.5-1.9-1.2 0-1.8.8-1.8 2.1V18Z" fill="{c}"/>'
ICON_MAIL = lambda c: f'<rect x="1" y="4" width="22" height="16" rx="3" stroke="{c}" stroke-width="1.8"/><path d="M2 6l10 7 10-7" stroke="{c}" stroke-width="1.8" fill="none"/>'
ICON_GH = lambda c: f'<path fill="{c}" d="M12 .5A11.5 11.5 0 0 0 8.4 22.9c.6.1.8-.3.8-.6v-2c-3.2.7-3.9-1.5-3.9-1.5-.5-1.3-1.3-1.7-1.3-1.7-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.7-1.6-2.6-.3-5.3-1.3-5.3-5.7 0-1.3.4-2.3 1.2-3.1-.1-.3-.5-1.5.1-3.1 0 0 1-.3 3.2 1.2a11 11 0 0 1 5.8 0c2.2-1.5 3.2-1.2 3.2-1.2.6 1.6.2 2.8.1 3.1.7.8 1.2 1.9 1.2 3.1 0 4.4-2.7 5.4-5.3 5.7.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A11.5 11.5 0 0 0 12 .5Z"/>'

def footer():
    W, H = 1200, 250
    rnd = random.Random(9)
    wave = ""
    for row in range(5):
        for i in range(60):
            x = 10 + i * 20
            y = 190 + row * 11 + 8 * math.sin(i / 5 + row)
            wave += f'<circle class="wv" cx="{x}" cy="{y:.1f}" r="{1.6-row*0.2:.1f}" fill="{AMBER}" style="animation-delay:{(i*0.06+row*0.2)%3:.2f}s;opacity:{0.6-row*0.1:.2f}"/>'
    css = STAR_CSS + """
.wv{animation:wv 3s ease-in-out infinite}@keyframes wv{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
.lamp{animation:lamp 5s ease-in-out infinite}@keyframes lamp{0%,100%{opacity:1}46%{opacity:.6}49%{opacity:.95}}
.up{animation:up 1s cubic-bezier(.2,.8,.2,1) both}@keyframes up{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
"""
    defs = (f'<radialGradient id="fg" cx="50%" cy="10%" r="55%"><stop offset="0" stop-color="{AMBER}" stop-opacity=".26"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="fc"><rect width="{W}" height="{H}" rx="22"/></clipPath>')
    body = (f'<g clip-path="url(#fc)"><rect width="{W}" height="{H}" fill="{BG}"/><rect class="lamp" width="{W}" height="{H}" fill="url(#fg)"/>'
            f'{grain(W, 170, 50, 11)}{wave}'
            f'<g class="up"><text class="mono" x="600" y="54" text-anchor="middle" font-size="12" fill="{AMBER}" letter-spacing="3">CLOSING THE FILE</text>'
            f'<text class="serif" x="600" y="108" text-anchor="middle" font-size="40" font-weight="600" fill="{TEXT}">Have an AI pilot <tspan font-style="italic" fill="{AMBER}">stuck in notebooks?</tspan></text>'
            f'<text class="sans" x="600" y="142" text-anchor="middle" font-size="15.5" fill="{MUTED}">I embed with your team and ship it to production — agents, RAG, automation, proof.</text></g></g>'
            f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" stroke="{LINE}"/>')
    write("footer.svg", W, H, body, css, defs)

if __name__ == "__main__":
    hero(); terminal(); impact(); timeline(); agents(); stack(); record(); divider(); footer()
    for args in [("whoami", "01", "whoami", "who's behind the commits"),
                 ("impact", "02", "Field results", "numbers from real production work"),
                 ("experience", "03", "Field record", "1.5+ years · pilots → production"),
                 ("exhibits", "04", "Exhibits", "shipped, open-source & clickable"),
                 ("stack", "05", "Instruments", "the agentic stack I ship with"),
                 ("activity", "06", "The ledger", "don't trust headlines — read the commits"),
                 ("record", "07", "Record", "trophies, certifications & schooling")]:
        header(*args)
    project("referentweave", "FILE 01 · REFERENCE-AWARE RAG", "ReferentWeave",
            ["Resolves cross-chunk references", "(\"it\" → entity) before retrieval,", "without touching the source text."],
            "+45pp", "Recall@1 over standard RAG", ["Python", "Rust", "FastAPI", "Gemini", "BM25+RRF"], "github.com/kvcops/ReferentWeave", AMBER, vis_recall)
    project("jobhunterx", "FILE 02 · MULTI-AGENT SYSTEM", "JobHunterX",
            ["Six tool-calling agents in one", "LangGraph state machine: resume in,", "tailored applications out."],
            "85", "automated tests · 3 LLM houses", ["LangGraph", "Browser Use", "Playwright", "FastAPI"], "github.com/kvcops/JobHunterX", CYAN, vis_nodes)
    project("atrophy", "FILE 03 · OPEN SOURCE · PyPI", "Atrophy",
            ["Separates human vs AI-written", "commits and tracks skill decay", "across 10 disciplines. Local-first."],
            "pip install atrophy", "", ["Python", "SQLite", "Tree-sitter", "CLI"], "github.com/kvcops/Atrophy", VIOLET, vis_decay)
    project("deepresearch", "FILE 04 · RESEARCH AGENT", "Deep Research",
            ["Plans queries, scrapes many engines", "concurrently, synthesizes with", "Gemini and writes the PDF report."],
            "$0", "paid-API scraping cost", ["Python", "Gemini API", "Scraping", "ReportLab"], "github.com/kvcops/Deep-Research-using-Gemini-api", GREEN, vis_badge("29★"))
    project("neuriq", "FILE 05 · ADAPTIVE LEARNING · LIVE", "NeurIQ AI",
            ["AI tutor with dynamic roadmaps,", "an adaptive learning engine and", "spaced-repetition flashcards."],
            "Live", "deployed on Render", ["FastAPI", "Gemini API", "PostgreSQL"], "neuriq-ai.onrender.com", ORANGE, vis_badge("", True))
    project("kvnexus", "FILE 06 · WHERE IT STARTED", "KV Nexus",
            ["My first website: an AI companion", "for recipes, health, flowcharts", "and mind-maps."],
            "22", "forks · 12 stars", ["Gemini API", "REST", "HTML/CSS/JS"], "kv-nexus.vercel.app", "#F472B6", vis_badge("12★"))
    button("portfolio", "Portfolio", "vamsikrishna28.vercel.app", AMBER, ICON_GLOBE)
    button("linkedin", "LinkedIn", "let's connect", "#4A9EFF", ICON_IN)
    button("email", "Email", "Vamsikv28@gmail.com", ORANGE, ICON_MAIL)
    button("github", "GitHub", "follow the work", TEXT, ICON_GH)
    print("ok", len(os.listdir(OUT)), "files")
