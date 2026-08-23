#!/usr/bin/env python3
"""
Single source of truth for the Multi-Agent Platform Architecture diagram.
Emits:
  - agent-platform-architecture.drawio       (editable in draw.io / diagrams.net)
  - agent-platform-architecture.svg          (light, for the blog)
  - agent-platform-architecture-dark.svg     (dark, for Chirpy's dark mode)
Edit NODES / EDGES below, re-run, and all outputs regenerate.

This is a deliberately trimmed, external-facing subset of the platform:
one agent per pattern rather than the full inventory.
"""
import html, os

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1376, 985
TOP_CROP = 86        # title/subtitle removed; caption in the post carries them

# ---------------------------------------------------------------- palette ----
# Layers are encoded by tint, not by hue. Only the agent tier carries real
# colour, so the eye lands on the Supervisor and fans out from there.
P = {
    "sup":   dict(fill="#3B6FB6", stroke="#2C568F", font="#FFFFFF"),   # focal point
    "agent": dict(fill="#E3ECFA", stroke="#3B6FB6", font="#14365E"),   # agents (accent)
    "ghost": dict(fill="#EEF3FB", stroke="#A9C0E0", font="#5E7CA3"),   # "and more agents"
    "mcp":   dict(fill="#DCE3EC", stroke="#93A0B1", font="#38414D"),   # MCP tool servers
    "api":   dict(fill="#FFFFFF", stroke="#BFC6D1", font="#454F5D"),   # APIs / services
    "data":  dict(fill="#FFFFFF", stroke="#BFC6D1", font="#454F5D"),   # datastores
    "ext":   dict(fill="#FFFFFF", stroke="#BFC6D1", font="#78818E",
                  dash=True),                                          # external (dashed)
    "grp":   dict(fill="#F8FAFC", stroke="#D5DBE3", font="#69727E"),   # container
    "grpg":  dict(fill="#F2F5F8", stroke="#D5DBE3", font="#69727E"),   # data zone
    "grpn":  dict(fill="none",    stroke="#D5DBE3", font="#69727E"),   # open container
}
EDGE_COLOR, TITLE_COLOR = "#A2ABB8", "#1A1F26"
# Link types. Two protocols carry the whole story: A2A between agents,
# MCP from agents to tool servers. Everything else is internal plumbing.
EK = {"a2a": ("#3B6FB6", 2.0), "mcp": ("#6E8299", 1.8), None: ("#A2ABB8", 1.5)}
EK_DARK = {"a2a": ("#6BA6E8", 2.0), "mcp": ("#8A94A3", 1.8), None: ("#6E7681", 1.5)}
BAND_COLOR, SUB_COLOR = "#8A93A1", "#6B7280"
LABEL_BG, SHADOW_OP = "#FFFFFF", "0.055"
FONT = "Helvetica, Arial, sans-serif"

# Dark variant, tuned for Chirpy's dark mode (page background #1b1b1e).
# The accent tracks Chirpy's dark link blue so the diagram reads as part of the site.
DARK = {
    "sup":   dict(fill="#4A85D6", stroke="#6BA6E8", font="#0F1114"),
    "agent": dict(fill="#1E3050", stroke="#5A8FD4", font="#CBDCF6"),
    "ghost": dict(fill="#19202B", stroke="#3D5570", font="#7E97BC"),
    "mcp":   dict(fill="#2A2F37", stroke="#535C69", font="#B9C0C9"),
    "api":   dict(fill="#1D1E22", stroke="#434952", font="#AFB6BF"),
    "data":  dict(fill="#1D1E22", stroke="#434952", font="#AFB6BF"),
    "ext":   dict(fill="#1D1E22", stroke="#434952", font="#868D96", dash=True),
    "grp":   dict(fill="#202125", stroke="#34383F", font="#7E858F"),
    "grpg":  dict(fill="#1E1F23", stroke="#34383F", font="#7E858F"),
    "grpn":  dict(fill="none",    stroke="#34383F", font="#7E858F"),
}

def apply_theme(name):
    """Swap the module-level palette between 'light' and 'dark'."""
    global EDGE_COLOR, TITLE_COLOR, BAND_COLOR, SUB_COLOR, LABEL_BG, SHADOW_OP, P
    if name == "dark":
        P.update(DARK)
        EDGE_COLOR, TITLE_COLOR = "#6E7681", "#E8E9EA"
        BAND_COLOR, SUB_COLOR = "#767D87", "#8B929B"
        LABEL_BG, SHADOW_OP = "#1B1B1E", "0"
        EK.update(EK_DARK)
    else:
        P.update(LIGHT)
        EDGE_COLOR, TITLE_COLOR = "#A2ABB8", "#1A1F26"
        BAND_COLOR, SUB_COLOR = "#8A93A1", "#6B7280"
        LABEL_BG, SHADOW_OP = "#FFFFFF", "0.055"
        EK.update(EK_LIGHT)

LIGHT = {k: dict(v) for k, v in P.items()}
EK_LIGHT = dict(EK)

# ------------------------------------------------------------------ layout ---
R_UI, R_BFF, R_SUP, R_AGT, R_MCP, R_API, R_DB = 110, 214, 300, 398, 498, 586, 682
H_STD, H_MCP, H_AGT, H_DB = 54, 44, 60, 58
CW = 124
COL = [60 + 136 * i for i in range(7)]      # 60,196,332,468,604,740,876
SI = 1144                                    # Support Insights column

def c(x, w=CW):
    return x + w / 2

NODES = []
def N(nid, label, x, y, w, h, kind, shape="box", fs=12, **kw):
    NODES.append(dict(id=nid, label=label, x=x, y=y, w=w, h=h,
                      kind=kind, shape=shape, fs=fs, **kw))
    return nid

# --- containers (drawn first, behind everything) ---
N("grp_core", "TLS Core Platform  ·  IBM Cloud", 40, 186, 1006, 576, "grp", "group", fs=13)
N("grp_si",   "Support Insights\n(separate environment)", 1086, 306, 240, 456, "grpn", "group",
  fs=11, align="center")
N("grp_plat", "Platform Services", 866, 200, 164, 134, "grpn", "group", fs=12, align="center")

# --- application ---
N("ui_concierge", "Concierge UI", 455, R_UI, 150, H_STD, "api")
N("ui_si",        "Support Insights UI", SI, R_UI, CW, H_STD, "api", fs=11)

# --- orchestration ---
N("bff", "Backend for Frontend\n(Next.js)", 455, R_BFF, 150, H_STD, "api", fs=11)
N("sup", "Supervisor Agent",     455, R_SUP, 150, H_STD, "sup", fs=13)
N("langfuse", "Langfuse", 882, 228, 132, 42, "api", fs=11)
N("litellm",  "LiteLLM",  882, 280, 132, 42, "api", fs=11)

# --- agents ---
N("ag_case",  "Case Agent",               128, R_AGT, CW, H_AGT, "agent")
N("ag_clnt",  "Client Management\nAgent", 468, R_AGT, CW, H_AGT, "agent", fs=11)
N("ag_doc",   "Doc Agent",                740, R_AGT, CW, H_AGT, "agent")
N("ag_asset", "Asset Agent", SI,  R_AGT, CW, H_AGT, "agent")
# Not exhaustive: shows the supervisor fanning out to agents not drawn individually
N("ag_more",  "+ Contract Agent,\nHACoC Agent,\nand others in the future", COL[6], R_AGT, CW, H_AGT,
  "ghost", fs=9.5)

# --- MCP tool servers ---
for i, (nid, lbl) in enumerate([
        ("mcp_case",   "Case\nMCP Server"),
        ("mcp_aa",     "Agent Assist\nMCP Server"),
        ("mcp_ca",     "Case Analytics\nMCP Server"),
        ("mcp_ppt",    "PowerPoint Builder\nMCP Server"),
        ("mcp_carbon", "Carbon Charts\nMCP Server"),
        ("mcp_docs",   "Documentation\nMCP Server")]):
    N(nid, lbl, COL[i], R_MCP, CW, H_MCP, "mcp", fs=10)
N("mcp_asset", "Asset\nMCP Server", SI, R_MCP, CW, H_MCP, "mcp", fs=10)

# --- APIs / services ---
N("api_csp", "Salesforce\nProxy API",       COL[0], R_API, CW, H_STD, "api", fs=11)
N("api_aa",  "Agent Assist API",           COL[1], R_API, CW, H_STD, "api", fs=11)
N("api_doc", "Documentation API",          COL[5], R_API, CW, H_STD, "api", fs=11)
N("api_si",  "Support Insights\nAPI",     SI,     R_API, CW, H_STD, "api", fs=11)

# --- datastores ---
N("db_aa",     "Agent Assist DB", COL[1], R_DB, CW, H_DB, "data", "cyl", fs=11)
N("db_cos",    "Cloud Object\nStorage", COL[4], R_DB, CW, H_DB, "data", "cyl", fs=10.5)
N("db_milvus", "Milvus",          COL[5], R_DB, CW, H_DB, "data", "cyl", fs=11)
N("db_si",     "Support Insights\nDB", SI, R_DB, CW, H_DB, "data", "cyl", fs=11)

# --- external systems (dashed: outside the platform boundary) ---
N("ext_csp", "Salesforce API", COL[0], 812, CW, H_STD, "ext", fs=11)

LEGEND = [("sup", "Supervisor"), ("agent", "Agents"), ("mcp", "MCP tool servers"),
          ("api", "APIs, services & data stores"), ("ext", "External systems")]
LINK_LEGEND = [("a2a", "A2A  (agent to agent)"), ("mcp", "MCP  (agent to tool server)"),
               (None,  "Internal service & data calls")]
BANDS = []   # left-hand band labels removed

# ------------------------------------------------------------------- edges ---
EDGES = []
def E(s, t, mode="v", label="", dashed=False, sside=None, tside=None, wp=None, kind=None):
    EDGES.append(dict(s=s, t=t, mode=mode, label=label, dashed=dashed,
                      sside=sside, tside=tside, wp=wp or [], kind=kind))

E("ui_concierge", "bff")
E("bff", "sup", kind="a2a")                 # BFF speaks A2A, so any agent can plug in
for a in ("ag_case", "ag_clnt", "ag_doc", "ag_more", "ag_asset"):
    E("sup", a, kind="a2a")

E("ag_case", "mcp_case", kind="mcp")
E("ag_case", "mcp_aa", kind="mcp")
for m in ("mcp_ca", "mcp_ppt", "mcp_carbon"):
    E("ag_clnt", m, kind="mcp")
E("ag_doc", "mcp_docs", kind="mcp")
E("ag_asset", "mcp_asset", kind="mcp")

E("mcp_case", "api_csp")
E("api_csp", "ext_csp")
E("mcp_aa", "api_aa")
E("api_aa", "db_aa")
E("mcp_carbon", "db_cos")
E("mcp_docs", "api_doc")
E("api_doc", "db_milvus")

E("mcp_ca", "api_si", "h", sside="b", tside="l", wp=[(c(COL[2]), 562), (1058, 562)])
E("api_si", "db_si")
E("mcp_asset", "db_si", "h", sside="r", tside="r", wp=[(1294, 520), (1294, 711)])
E("ui_si", "grp_si", "v", sside="b", tside="t")

# ----------------------------------------------------------------- helpers ---
BY_ID = {}

def anchor(n, side):
    x, y, w, h = n["x"], n["y"], n["w"], n["h"]
    return {"t": (x + w / 2, y), "b": (x + w / 2, y + h),
            "l": (x, y + h / 2), "r": (x + w, y + h / 2)}[side]

def route(e):
    s, t = BY_ID[e["s"]], BY_ID[e["t"]]
    if e["mode"] == "v":
        ss, ts = e["sside"] or "b", e["tside"] or "t"
    else:
        ss, ts = e["sside"] or "r", e["tside"] or "l"
    p0, p1 = anchor(s, ss), anchor(t, ts)
    pts = [p0] + e["wp"] + [p1]
    out = [pts[0]]
    for i in range(1, len(pts)):
        a, b = out[-1], pts[i]
        if abs(a[0] - b[0]) < 0.5 or abs(a[1] - b[1]) < 0.5:
            out.append(b); continue
        vertical_first = (ss in "tb") if i == 1 else (abs(out[-1][1] - out[-2][1]) > 0.5)
        if i == len(pts) - 1 and ts in "tb":
            if vertical_first:
                mid = (a[1] + b[1]) / 2
                out += [(a[0], mid), (b[0], mid), b]
            else:
                out += [(b[0], a[1]), b]
        elif i == len(pts) - 1 and ts in "lr":
            if vertical_first:
                out += [(a[0], b[1]), b]
            else:
                mid = (a[0] + b[0]) / 2
                out += [(mid, a[1]), (mid, b[1]), b]
        else:
            out += [((a[0], b[1]) if vertical_first else (b[0], a[1])), b]
    ded = [out[0]]
    for p in out[1:]:
        if abs(p[0] - ded[-1][0]) > 0.5 or abs(p[1] - ded[-1][1]) > 0.5:
            ded.append(p)
    return ded

# --------------------------------------------------------------- SVG output --
def rounded_path(pts, r=8):
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(pts) - 1):
        p, cpt, n = pts[i - 1], pts[i], pts[i + 1]
        def trim(a, b, dist):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = (dx * dx + dy * dy) ** .5 or 1
            k = min(dist, L / 2)
            return (a[0] + dx / L * k, a[1] + dy / L * k)
        a, b = trim(cpt, p, r), trim(cpt, n, r)
        d += f" L {a[0]:.1f} {a[1]:.1f} Q {cpt[0]:.1f} {cpt[1]:.1f} {b[0]:.1f} {b[1]:.1f}"
    return d + f" L {pts[-1][0]:.1f} {pts[-1][1]:.1f}"

def arrowhead(pts, size=7.5, w=4.2, col=None):
    (x1, y1), (x0, y0) = pts[-1], pts[-2]
    dx, dy = x1 - x0, y1 - y0
    L = (dx * dx + dy * dy) ** .5 or 1
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    bx, by = x1 - ux * size, y1 - uy * size
    return (f'<path d="M {x1:.1f} {y1:.1f} L {bx+px*w:.1f} {by+py*w:.1f} '
            f'L {bx-px*w:.1f} {by-py*w:.1f} Z" fill="{col or EDGE_COLOR}"/>')

def mid_of(pts):
    best, bl = (pts[0], pts[-1]), -1
    for a, b in zip(pts, pts[1:]):
        L = abs(a[0] - b[0]) + abs(a[1] - b[1])
        if L > bl:
            bl, best = L, (a, b)
    a, b = best
    return (a[0] + b[0]) / 2, (a[1] + b[1]) / 2

def svg_text(lines, cx, cy, fs, color, weight="500"):
    n = len(lines); lh = fs * 1.22
    y0 = cy - (n - 1) * lh / 2 + fs * 0.35
    return "".join(
        f'<text x="{cx:.1f}" y="{y0 + i*lh:.1f}" font-family="{FONT}" font-size="{fs}" '
        f'font-weight="{weight}" fill="{color}" text-anchor="middle">{html.escape(ln)}</text>\n'
        for i, ln in enumerate(lines))

def build_svg():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {TOP_CROP} {W} {H-TOP_CROP}" '
         f'width="{W}" height="{H-TOP_CROP}">',
         f'<defs><filter id="sh" x="-20%" y="-20%" width="140%" height="150%">'
         f'<feDropShadow dx="0" dy="1" stdDeviation="1.2" flood-color="#0B1F3A" '
         f'flood-opacity="{SHADOW_OP}"/></filter></defs>']

    for lbl, y in BANDS:
        o.append(f'<text x="{COL[0]-18}" y="{y}" font-family="{FONT}" font-size="12.5" '
                 f'font-weight="700" fill="{BAND_COLOR}" text-anchor="end" '
                 f'letter-spacing="0.6">{lbl.upper()}</text>')

    for n in [x for x in NODES if x["shape"] == "group"]:
        p = P[n["kind"]]
        o.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" rx="10" '
                 f'fill="{p["fill"]}" stroke="{p["stroke"]}" stroke-width="1.2"/>')
        ctr = n.get("align") == "center"
        tx, anch = (n["x"] + n["w"] / 2, "middle") if ctr else (n["x"] + 14, "start")
        for i, ln in enumerate(n["label"].split("\n")):
            o.append(f'<text x="{tx}" y="{n["y"] + 21 + i * (n["fs"] * 1.32):.1f}" '
                     f'text-anchor="{anch}" font-family="{FONT}" '
                     f'font-size="{n["fs"]}" font-weight="700" fill="{p["font"]}" '
                     f'letter-spacing="0.3">{html.escape(ln)}</text>')

    for e in EDGES:
        pts = route(e)
        col, wdt = EK[e["kind"]]
        dash = ' stroke-dasharray="5 4"' if e["dashed"] else ''
        o.append(f'<path d="{rounded_path(pts)}" fill="none" stroke="{col}" '
                 f'stroke-width="{wdt}"{dash}/>')
        o.append(arrowhead(pts, col=col))
        if e["label"]:
            mx, my = mid_of(pts)
            o.append(f'<rect x="{mx-24:.1f}" y="{my-9:.1f}" width="48" height="18" rx="4" '
                     f'fill="{LABEL_BG}" stroke="{LABEL_BG}"/>')
            o.append(svg_text([e["label"]], mx, my, 10.5, SUB_COLOR, "700"))

    for n in [x for x in NODES if x["shape"] != "group"]:
        p = P[n["kind"]]; x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        nd = ' stroke-dasharray="4 3"' if p.get("dash") else ''
        if n["shape"] == "cyl":
            ry = 8
            o.append(f'<g filter="url(#sh)"><path d="M {x} {y+ry} A {w/2} {ry} 0 0 1 {x+w} {y+ry} '
                     f'L {x+w} {y+h-ry} A {w/2} {ry} 0 0 1 {x} {y+h-ry} Z" fill="{p["fill"]}" '
                     f'stroke="{p["stroke"]}" stroke-width="1.3"{nd}/>'
                     f'<path d="M {x} {y+ry} A {w/2} {ry} 0 0 0 {x+w} {y+ry}" fill="none" '
                     f'stroke="{p["stroke"]}" stroke-width="1.3"{nd}/></g>')
            cy = y + h / 2 + 4
        else:
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{p["fill"]}" '
                     f'stroke="{p["stroke"]}" stroke-width="1.3"{nd} filter="url(#sh)"/>')
            cy = y + h / 2
        o.append(svg_text(n["label"].split("\n"), x + w / 2, cy, n["fs"], p["font"], "600"))

    ly = 905
    o.append(f'<text x="40" y="{ly-16}" font-family="{FONT}" font-size="12" font-weight="700" '
             f'fill="{BAND_COLOR}" letter-spacing="0.6">LEGEND</text>')
    lx = 40
    for kind, lbl in LEGEND:
        p = P[kind]
        nd = ' stroke-dasharray="3 2"' if p.get("dash") else ''
        o.append(f'<rect x="{lx}" y="{ly-11}" width="22" height="15" rx="4" fill="{p["fill"]}" '
                 f'stroke="{p["stroke"]}" stroke-width="1.2"{nd}/>')
        o.append(f'<text x="{lx+30}" y="{ly+1}" font-family="{FONT}" font-size="12.5" '
                 f'fill="{SUB_COLOR}">{html.escape(lbl)}</text>')
        lx += int(40 + len(lbl) * 7.2)
    ly2, lx = ly + 30, 40
    for kind, lbl in LINK_LEGEND:
        col, wdt = EK[kind]
        o.append(f'<path d="M {lx} {ly2-4} L {lx+24} {ly2-4}" stroke="{col}" stroke-width="{wdt}"/>')
        o.append(f'<path d="M {lx+24} {ly2-4} l -5 -3 l 0 6 z" fill="{col}"/>')
        o.append(f'<text x="{lx+32}" y="{ly2}" font-family="{FONT}" font-size="12.5" '
                 f'fill="{SUB_COLOR}">{html.escape(lbl)}</text>')
        lx += int(42 + len(lbl) * 7.2)
    o.append('</svg>')
    return "\n".join(o)

# ------------------------------------------------------------ draw.io output -
def dstyle(n):
    p = P[n["kind"]]
    if n["shape"] == "group":
        ctr = n.get("align") == "center"
        return (f'rounded=1;arcSize=4;whiteSpace=wrap;html=1;verticalAlign=top;'
                f'align={"center" if ctr else "left"};spacingLeft={0 if ctr else 8};'
                f'spacingTop=2;fillColor={p["fill"]};strokeColor={p["stroke"]};'
                f'fontColor={p["font"]};fontStyle=1;fontSize={n["fs"]};fontFamily=Helvetica;')
    if n["shape"] == "cyl":
        return (f'shape=cylinder3;boundedLbl=1;backgroundOutline=1;size=8;whiteSpace=wrap;html=1;'
                f'fillColor={p["fill"]};strokeColor={p["stroke"]};fontColor={p["font"]};'
                f'fontSize={n["fs"]};fontFamily=Helvetica;fontStyle=1;')
    return (f'rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor={p["fill"]};'
            f'strokeColor={p["stroke"]};fontColor={p["font"]};fontSize={n["fs"]};'
            f'fontFamily=Helvetica;fontStyle=1;shadow=0;'
            + ('dashed=1;dashPattern=4 3;' if p.get("dash") else ''))

SIDE = {"t": (0.5, 0), "b": (0.5, 1), "l": (0, 0.5), "r": (1, 0.5)}

def build_drawio():
    x = ['<mxfile host="app.diagrams.net" version="26.0.0">',
         '  <diagram name="Multi-Agent Platform Architecture" id="mapa1">',
         f'    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" '
         f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" '
         f'pageHeight="{H}" math="0" shadow="0">', '      <root>',
         '        <mxCell id="0" /><mxCell id="1" parent="0" />']

    def cell(i, val, style, gx, gy, gw, gh):
        x.append(f'        <mxCell id="{i}" value="{html.escape(val)}" style="{style}" '
                 f'vertex="1" parent="1"><mxGeometry x="{gx}" y="{gy}" width="{gw}" '
                 f'height="{gh}" as="geometry" /></mxCell>')

    ts = "text;html=1;align=left;verticalAlign=middle;fontFamily=Helvetica;"

    for n in sorted(NODES, key=lambda n: 0 if n["shape"] == "group" else 1):
        lbl = n["label"].replace("\n", "<br>" if n["shape"] == "group" else " ")
        cell(n["id"], lbl, dstyle(n), n["x"], n["y"], n["w"], n["h"])

    for k, e in enumerate(EDGES):
        ss = e["sside"] or ("b" if e["mode"] == "v" else "r")
        tsd = e["tside"] or ("t" if e["mode"] == "v" else "l")
        ex, ey = SIDE[ss]; nx, ny = SIDE[tsd]
        st = (f'edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;jettySize=auto;orthogonalLoop=1;'
              f'exitX={ex};exitY={ey};exitDx=0;exitDy=0;entryX={nx};entryY={ny};entryDx=0;'
              f'entryDy=0;strokeColor={EDGE_COLOR};strokeWidth=1.5;endArrow=block;endFill=1;'
              f'endSize=6;fontFamily=Helvetica;fontSize=10;fontStyle=1;fontColor={SUB_COLOR};'
              + ('dashed=1;' if e["dashed"] else ''))
        pts = ''.join(f'<mxPoint x="{p[0]}" y="{p[1]}" />' for p in e["wp"])
        arr = f'<Array as="points">{pts}</Array>' if pts else ''
        x.append(f'        <mxCell id="e{k}" value="{html.escape(e["label"])}" style="{st}" '
                 f'edge="1" parent="1" source="{e["s"]}" target="{e["t"]}">'
                 f'<mxGeometry relative="1" as="geometry">{arr}</mxGeometry></mxCell>')

    ly = 905
    cell("legt", "LEGEND", ts + f"fontSize=12;fontStyle=1;fontColor={BAND_COLOR};",
         40, ly - 30, 120, 20)
    lx = 40
    for j, (kind, lbl) in enumerate(LEGEND):
        p = P[kind]
        cell(f"lg{j}", "", f"rounded=1;arcSize=25;html=1;fillColor={p['fill']};"
             f"strokeColor={p['stroke']};" + ("dashed=1;dashPattern=3 2;" if p.get("dash") else ""),
             lx, ly - 11, 22, 15)
        cell(f"lgt{j}", lbl, ts + f"fontSize=12;fontColor={SUB_COLOR};",
             lx + 28, ly - 12, len(lbl) * 7 + 10, 18)
        lx += int(40 + len(lbl) * 7.2)

    x += ['      </root>', '    </mxGraphModel>', '  </diagram>', '</mxfile>']
    return "\n".join(x)

# --------------------------------------------------------------------- main --
if __name__ == "__main__":
    BY_ID.update({n["id"]: n for n in NODES})
    for theme, suffix in (("light", ""), ("dark", "-dark")):
        apply_theme(theme)
        open(os.path.join(OUT, f"agent-platform-architecture{suffix}.svg"), "w",
             encoding="utf-8").write(build_svg())
    apply_theme("light")
    open(os.path.join(OUT, "agent-platform-architecture.drawio"), "w",
         encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n' + build_drawio())
    print("wrote light svg + dark svg + drawio")
