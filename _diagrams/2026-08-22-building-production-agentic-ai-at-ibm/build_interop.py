#!/usr/bin/env python3
"""
Companion figure: Ecosystem Interoperability.

Reuses the palette and A2A/MCP link colours from build_diagram.py so the two
figures read as a set and the reader arrives already knowing the legend.

Structure is the 2x2 hiding in the prose: {A2A, MCP} x {inbound, outbound}.
Left = callers in, right = things the platform calls, so the figure reads
left-to-right as "callers -> platform -> callees".
"""
import html, os
import build_diagram as bd

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1230, 500
TOP_CROP = 92        # title/subtitle removed; caption in the post carries them

# rows: the two protocol surfaces
Y_A2A, Y_MCP, BH = 150, 310, 96
X_L, X_C, X_R, CW_S, CW_C = 70, 472, 860, 300, 236

NODES, EDGES = [], []
def N(nid, label, x, y, w, h, kind, fs=11.5, shape="box"):
    NODES.append(dict(id=nid, label=label, x=x, y=y, w=w, h=h,
                      kind=kind, shape=shape, fs=fs))
def E(s, t, kind):
    EDGES.append(dict(s=s, t=t, kind=kind))

# --- the platform, abstracted to its two boundaries -------------------------
N("grp", "TLS Agentic Platform", 450, 102, 280, 350, "grp", 13, "group")
N("agents", "Supervisor &\nSpecialist Agents", X_C, Y_A2A, CW_C, BH, "agent", 13)
N("tools",  "MCP Tool Servers",   X_C, Y_MCP, CW_C, BH, "mcp", 13)

# --- inbound: the platform as a provider -----------------------------------
N("in_a2a", "TLS Concierge BFF\nOther IBM assistants & apps\nAny A2A-compliant client",
  X_L, Y_A2A, CW_S, BH, "ext")
N("in_mcp", "Systems that speak MCP —\nreach tool servers directly,\nbypassing the agent layer",
  X_L, Y_MCP, CW_S, BH, "ext")

# --- outbound: the platform as an orchestrator ------------------------------
N("out_a2a", "Salesforce Agentforce\nIBM watsonx Orchestrate\nAny A2A-compliant agent",
  X_R, Y_A2A, CW_S, BH, "ext")
N("out_mcp", "MCP servers hosted\non other platforms",
  X_R, Y_MCP, CW_S, BH, "ext")

E("in_a2a", "agents", "a2a")
E("in_mcp", "tools",  "mcp")
E("agents", "out_a2a", "a2a")
E("agents", "out_mcp", "mcp")

HEADERS = [(X_L + CW_S / 2, "Inbound  ·  as a provider"),
           (X_R + CW_S / 2, "Outbound  ·  as an orchestrator")]

def build_svg():
    P, EK = bd.P, bd.EK
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {TOP_CROP} {W} {H-TOP_CROP}" '
         f'width="{W}" height="{H-TOP_CROP}">',
         f'<defs><filter id="sh" x="-20%" y="-20%" width="140%" height="150%">'
         f'<feDropShadow dx="0" dy="1" stdDeviation="1.2" flood-color="#0B1F3A" '
         f'flood-opacity="{bd.SHADOW_OP}"/></filter></defs>']

    for x, lbl in HEADERS:
        o.append(f'<text x="{x}" y="128" text-anchor="middle" font-family="{bd.FONT}" '
                 f'font-size="12" font-weight="700" fill="{bd.BAND_COLOR}" '
                 f'letter-spacing="0.6">{html.escape(lbl.upper())}</text>')

    for n in [x for x in NODES if x["shape"] == "group"]:
        p = P[n["kind"]]
        o.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" rx="10" '
                 f'fill="{p["fill"]}" stroke="{p["stroke"]}" stroke-width="1.2"/>')
        o.append(f'<text x="{n["x"]+n["w"]/2}" y="{n["y"]+26}" font-family="{bd.FONT}" '
                 f'font-size="{n["fs"]}" font-weight="700" fill="{p["font"]}" '
                 f'text-anchor="middle" letter-spacing="0.3">{html.escape(n["label"])}</text>')

    by = {n["id"]: n for n in NODES}
    for e in EDGES:
        s, t = by[e["s"]], by[e["t"]]
        col, wdt = EK[e["kind"]]
        ys, yt = s["y"] + s["h"] / 2, t["y"] + t["h"] / 2
        x0, x1 = s["x"] + s["w"], t["x"]
        if abs(ys - yt) < 0.5:
            d = f'M {x0} {ys} L {x1-8} {ys}'
            lx, ly, anch = (x0 + x1) / 2, ys - 12, "middle"
        else:
            bx, r = (x0 + x1) / 2, 10
            sgn = 1 if yt > ys else -1
            # leave the source box offset from its centre so this path doesn't
            # run collinear with the straight edge on the same row
            ye = ys + sgn * 26
            d = (f'M {x0} {ye} L {bx-r} {ye} Q {bx} {ye} {bx} {ye+sgn*r} '
                 f'L {bx} {yt-sgn*r} Q {bx} {yt} {bx+r} {yt} L {x1-8} {yt}')
            lx, ly, anch = bx - 14, (ye + yt) / 2 + 4, "end"
        o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{wdt}"/>')
        o.append(f'<path d="M {x1} {yt} L {x1-9} {yt-4.5} L {x1-9} {yt+4.5} Z" fill="{col}"/>')
        o.append(f'<text x="{lx:.0f}" y="{ly:.0f}" font-family="{bd.FONT}" '
                 f'font-size="12" font-weight="700" fill="{col}" text-anchor="{anch}">'
                 f'{e["kind"].upper()}</text>')

    for n in [x for x in NODES if x["shape"] != "group"]:
        p = P[n["kind"]]
        nd = ' stroke-dasharray="4 3"' if p.get("dash") else ''
        o.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" rx="7" '
                 f'fill="{p["fill"]}" stroke="{p["stroke"]}" stroke-width="1.3"{nd} '
                 f'filter="url(#sh)"/>')
        o.append(bd.svg_text(n["label"].split("\n"), n["x"] + n["w"] / 2,
                             n["y"] + n["h"] / 2, n["fs"], p["font"], "600"))

    o.append('</svg>')
    return "\n".join(o)

if __name__ == "__main__":
    for theme, suffix in (("light", ""), ("dark", "-dark")):
        bd.apply_theme(theme)
        open(os.path.join(OUT, f"ecosystem-interoperability{suffix}.svg"), "w",
             encoding="utf-8").write(build_svg())
    bd.apply_theme("light")
    print("wrote ecosystem-interoperability svg (light + dark)")
