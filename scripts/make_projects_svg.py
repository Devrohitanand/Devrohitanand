import html

W, H = 550, 458
L, R = 18, 532
TOP = 78
HEAD_H = 36
ROW_H = 52
SEPS = [48, 236, 352, 440]

# (name, description, url, status, progress %)   status: "online" or "building"
PROJECTS = [
    ("BrandNewFraud", "Fraud evidence management", "-", "building", 70),
    ("DropKaro", "Secure file & text sharing", "dropkaro.online", "online", 100),
    ("StoleBooks", "Used books marketplace", "-", "building", 55),
    ("KIITGo", "In development", "-", "building", 25),
]
COLOR = {"online": "#3fb950", "building": "#d29922"}

css = """
@keyframes in { from { opacity: 0; } to { opacity: 1; } }
@keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }
@keyframes wait { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
text { font-family: Consolas, 'Courier New', monospace; font-size: 13px; fill: #c9d1d9; }
.r { opacity: 0; animation: in 0.4s ease-out forwards; }
.h { fill: #8b949e; font-weight: bold; font-size: 12px; }
.n { fill: #e6edf3; font-weight: bold; }
.d { fill: #6e7681; font-size: 11px; }
.u { fill: #58a6ff; font-size: 11px; }
.s { font-size: 12px; }
.wait { animation: wait 1.6s ease-in-out infinite; }
.cur { opacity: 0; animation: blink 1s steps(1) 3s infinite; }
"""

p = []
p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
p.append(f"<style>{css}</style>")
p.append(f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>')
p.append('<circle cx="18" cy="16" r="4" fill="#ff5f56"/><circle cx="32" cy="16" r="4" fill="#ffbd2e"/><circle cx="46" cy="16" r="4" fill="#27c93f"/>')
p.append(f'<line x1="0" y1="30" x2="{W}" y2="30" stroke="#21262d"/>')

# typed command
CMD = "./what-am-i-building.sh"
n = len(CMD) + 2
vals = ";".join(f"{i * 7.8:.1f}" for i in range(n + 1))
p.append(
    f'<clipPath id="cmd"><rect x="{L}" y="44" width="0" height="26">'
    f'<animate attributeName="width" values="{vals}" calcMode="discrete" begin="0.3s" dur="{n * 0.05:.2f}s" fill="freeze"/>'
    f"</rect></clipPath>"
)
p.append(f'<g clip-path="url(#cmd)"><text x="{L}" y="64"><tspan style="fill:#7ee787">$</tspan> {html.escape(CMD)}</text></g>')

# table frame
table_h = HEAD_H + len(PROJECTS) * ROW_H
bottom = TOP + table_h
p.append('<g class="r" style="animation-delay:1.1s">')
p.append(f'<rect x="{L}" y="{TOP}" width="{R - L}" height="{HEAD_H}" fill="#161b22"/>')
p.append(f'<rect x="{L}" y="{TOP}" width="{R - L}" height="{table_h}" rx="3" fill="none" stroke="#30363d"/>')
p.append(f'<line x1="{L}" y1="{TOP + HEAD_H}" x2="{R}" y2="{TOP + HEAD_H}" stroke="#30363d"/>')
for sx in SEPS:
    p.append(f'<line x1="{sx}" y1="{TOP}" x2="{sx}" y2="{bottom}" stroke="#30363d"/>')
for i in range(1, len(PROJECTS)):
    ly = TOP + HEAD_H + i * ROW_H
    p.append(f'<line x1="{L}" y1="{ly}" x2="{R}" y2="{ly}" stroke="#21262d"/>')
hy = TOP + 23
p.append(f'<text class="h" x="26" y="{hy}">id</text>')
p.append(f'<text class="h" x="56" y="{hy}">name</text>')
p.append(f'<text class="h" x="244" y="{hy}">url</text>')
p.append(f'<text class="h" x="360" y="{hy}">status</text>')
p.append(f'<text class="h" x="448" y="{hy}">progress</text>')
p.append("</g>")

# rows
for i, (name, desc, url, st, pct) in enumerate(PROJECTS):
    top = TOP + HEAD_H + i * ROW_H
    delay = round(1.4 + i * 0.3, 2)
    c = COLOR[st]
    g = f'<g class="r" style="animation-delay:{delay}s">'
    g += f'<text class="d" x="26" y="{top + 30}" style="font-size:12px">{i}</text>'
    g += f'<text class="n" x="56" y="{top + 23}">{html.escape(name)}</text>'
    g += f'<text class="d" x="56" y="{top + 40}">{html.escape(desc)}</text>'
    if url == "-":
        g += f'<text class="d" x="244" y="{top + 30}" style="font-size:12px">-</text>'
    else:
        g += f'<text class="u" x="244" y="{top + 30}">{html.escape(url)}</text>'
    dot_cls = "wait" if st == "building" else ""
    g += f'<circle class="{dot_cls}" cx="362" cy="{top + 26}" r="3" fill="{c}"/>'
    g += f'<text class="s" x="371" y="{top + 30}" style="fill:{c}">{st}</text>'

    # segmented progress bar
    filled = round(pct / 10)
    for k in range(10):
        bx = 448 + k * 5
        if k < filled:
            b = round(delay + 0.5 + k * 0.1, 2)
            g += (
                f'<rect x="{bx}" y="{top + 22}" width="4" height="9" rx="1" fill="{c}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" begin="{b}s" dur="0.15s" fill="freeze"/>'
            )
            if st == "building" and k == filled - 1:
                g += (
                    f'<animate attributeName="opacity" values="1;0.2;1" dur="1.2s" '
                    f'begin="{round(b + 0.6, 2)}s" repeatCount="indefinite"/>'
                )
            g += "</rect>"
        else:
            g += f'<rect x="{bx}" y="{top + 22}" width="4" height="9" rx="1" fill="#21262d"/>'
    g += f'<text x="448" y="{top + 44}" style="fill:{c};font-size:10px">{pct}%</text>'
    g += "</g>"
    p.append(g)

# summary + prompt
n_on = sum(1 for x in PROJECTS if x[3] == "online")
n_bu = len(PROJECTS) - n_on
p.append(
    f'<g class="r" style="animation-delay:2.8s">'
    f'<text class="d" x="{L}" y="{bottom + 28}" style="font-size:12px"># {n_on} online / {n_bu} building</text>'
    f'<text x="{L}" y="{bottom + 54}" style="fill:#7ee787">$</text></g>'
)
p.append(f'<rect class="cur" x="{L + 14}" y="{bottom + 41}" width="8" height="16" fill="#58a6ff"/>')

p.append("</svg>")

with open("projects.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(p))

print("Done: projects.svg")