import json
import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL, STEP, LEFT, TOP = 12, 15, 36, 56

with open("data/contributions.json", encoding="utf-8") as f:
    data = json.load(f)

days = data["days"]
stats = data["stats"]

first = datetime.date.fromisoformat(days[0]["date"])
offset = (first.weekday() + 1) % 7  # Sunday = 0
weeks = (len(days) + offset + 6) // 7

WIDTH = LEFT + weeks * STEP + 20
GRID_W = weeks * STEP
GRID_H = 7 * STEP
HEIGHT = TOP + GRID_H + 56

REVEAL_END = round((weeks + 7) * 0.02 + 0.6, 2)

css = """
@keyframes pop {
  0%   { opacity: 0; transform: scale(0); }
  70%  { opacity: 1; transform: scale(1.25); }
  100% { opacity: 1; transform: scale(1); }
}
@keyframes twinkle {
  0%, 100% { opacity: 1; }
  50%      { opacity: 0.45; }
}
@keyframes scan {
  from { transform: translateX(0px); }
  to   { transform: translateX(SCAN_DIST px); }
}
@keyframes blink {
  0%, 49%   { opacity: 1; }
  50%, 100% { opacity: 0; }
}
.c {
  opacity: 0;
  transform-box: fill-box;
  transform-origin: center;
  animation: pop 0.5s ease-out forwards;
}
.beam { animation: scan 4.5s linear 2.2s infinite; opacity: 0; }
.cur  { animation: blink 1s steps(1) infinite; }
text  { font-family: Consolas, 'Courier New', monospace; fill: #8b949e; font-size: 10px; }
.head { fill: #58a6ff; font-size: 12px; }
.foot { fill: #c9d1d9; font-size: 11px; }
""".replace("SCAN_DIST", str(GRID_W + 80))

p = []
p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">')
p.append(f"<style>{css}</style>")
p.append("<defs>")
p.append(f'<clipPath id="grid"><rect x="{LEFT}" y="{TOP}" width="{GRID_W}" height="{GRID_H}"/></clipPath>')
p.append('<linearGradient id="beamg" x1="0" x2="1" y1="0" y2="0">'
         '<stop offset="0" stop-color="#69f0a0" stop-opacity="0"/>'
         '<stop offset="0.5" stop-color="#69f0a0" stop-opacity="0.35"/>'
         '<stop offset="1" stop-color="#69f0a0" stop-opacity="0"/></linearGradient>')
p.append(f'<clipPath id="ft"><rect x="{LEFT}" y="{TOP + GRID_H + 14}" width="0" height="18">'
         f'<animate attributeName="width" from="0" to="760" dur="2.2s" begin="{REVEAL_END}s" fill="freeze"/>'
         '</rect></clipPath>')
p.append("</defs>")

p.append(f'<rect width="{WIDTH}" height="{HEIGHT}" rx="10" fill="#0d1117" stroke="#30363d"/>')

# header prompt
head = "devrohitanand@github ~ $ ./contributions.sh"
p.append(f'<circle cx="18" cy="16" r="4" fill="#ff5f56"/><circle cx="32" cy="16" r="4" fill="#ffbd2e"/><circle cx="46" cy="16" r="4" fill="#27c93f"/>')
p.append(f'<text class="head" x="64" y="20">{head}</text>')
p.append(f'<rect class="cur" x="{64 + int(len(head) * 7.2) + 4}" y="9" width="7" height="13" fill="#58a6ff"/>')

# weekday labels
for r, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    p.append(f'<text x="8" y="{TOP + r * STEP + 10}">{label}</text>')

# cells
last_month = ""
last_w = -10
for i, d in enumerate(days):
    idx = i + offset
    w, r = idx // 7, idx % 7
    month = d["date"][:7]
    if month != last_month and w - last_w >= 3:
        name = datetime.date.fromisoformat(d["date"]).strftime("%b")
        p.append(f'<text x="{LEFT + w * STEP}" y="{TOP - 10}">{name}</text>')
        last_w = w
    last_month = month

    x = LEFT + w * STEP
    y = TOP + r * STEP
    delay = round((w + r) * 0.02, 2)
    level = min(d["level"], 5)
    color = PALETTE[level]
    tip = f'{d["count"]} contributions on {d["date"]}'

    if level >= 3:
        tw_delay = round(delay + 0.8 + (i % 7) * 0.35, 2)
        style = f"animation: pop 0.5s ease-out {delay}s forwards, twinkle 3s ease-in-out {tw_delay}s infinite;"
    else:
        style = f"animation-delay:{delay}s;"

    p.append(
        f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
        f'fill="{color}" style="{style}"><title>{tip}</title></rect>'
    )

# scanner beam
p.append('<g clip-path="url(#grid)">')
p.append(f'<rect class="beam" x="{LEFT - 80}" y="{TOP}" width="80" height="{GRID_H}" fill="url(#beamg)"/>')
p.append("</g>")

# footer (typed)
fy = TOP + GRID_H + 28
footer = f'{stats["total"]:,} contributions in the last year  |  current streak: {stats["current_streak"]}  |  longest streak: {stats["longest_streak"]}'
p.append(f'<g clip-path="url(#ft)"><text class="foot" x="{LEFT}" y="{fy}">{footer}</text></g>')

# legend
lx = WIDTH - 20 - (len(PALETTE) * STEP) - 70
ly = TOP + GRID_H + 28
p.append(f'<text x="{lx}" y="{ly + 20}">Less</text>')
for k, c in enumerate(PALETTE):
    p.append(f'<rect x="{lx + 30 + k * STEP}" y="{ly + 10}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
p.append(f'<text x="{lx + 30 + len(PALETTE) * STEP + 4}" y="{ly + 20}">More</text>')

p.append("</svg>")

with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(p))

print("Done: contrib-heatmap.svg")