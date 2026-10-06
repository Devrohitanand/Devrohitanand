import html

WIDTH = 850
LINE_H = 27
TOP = 66
LEFT = 30
KEY_W = 130

NAME = "rohit"
HOST = "github"

ROWS = [
    ("Role", "B.Tech CSE (AI & ML) Student"),
    ("Building", "BrandNewFraud  /  DropKaro  /  StoleBooks  /  KIITGo"),
    ("Languages", "C++, JavaScript, TypeScript, Python, SQL, HTML, CSS"),
    ("Frontend", "React, Next.js, Tailwind CSS, shadcn/ui, Framer Motion"),
    ("Backend", "Node.js, Express, REST APIs, JWT Auth, Middleware"),
    ("Database", "MongoDB, PostgreSQL + PostGIS, Firebase, Redis"),
    ("Mobile", "React Native, Expo, NativeWind, Reanimated"),
    ("DSA", "C++, Trees, AVL, Recursion, LeetCode / HackerRank"),
    ("DevOps", "Git, Docker, WSL 2, Linux, Cursor, VS Code"),
    ("Cloud", "Vercel, Railway, Hostinger, GitHub Pages"),
    ("Integrations", "Razorpay, Shiprocket, Cloudinary"),
    ("GitHub", "github.com/Devrohitanand"),
]

HEIGHT = TOP + (len(ROWS) + 2) * LINE_H + 14

css = """
@keyframes in {
  from { opacity: 0; transform: translateX(-10px); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes blink {
  0%, 49%   { opacity: 1; }
  50%, 100% { opacity: 0; }
}
.l { opacity: 0; animation: in 0.5s ease-out forwards; }
.cur { animation: blink 1s steps(1) infinite; }
text { font-family: Consolas, 'Courier New', monospace; font-size: 14px; fill: #c9d1d9; }
.k { fill: #58a6ff; font-weight: bold; }
.dim { fill: #6e7681; }
.head { fill: #8b949e; font-size: 12px; }
.name { fill: #e6edf3; font-weight: bold; }
"""

p = []
p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">')
p.append(f"<style>{css}</style>")
p.append(f'<rect width="{WIDTH}" height="{HEIGHT}" rx="10" fill="#0d1117" stroke="#30363d"/>')
p.append('<circle cx="18" cy="16" r="4" fill="#ff5f56"/><circle cx="32" cy="16" r="4" fill="#ffbd2e"/><circle cx="46" cy="16" r="4" fill="#27c93f"/>')
p.append(f'<line x1="0" y1="30" x2="{WIDTH}" y2="30" stroke="#21262d"/>')

t = 0.2
y = TOP

p.append(
    f'<g class="l" style="animation-delay:{t}s"><text x="{LEFT}" y="{y}">'
    f'<tspan class="name">{html.escape(NAME)}</tspan><tspan class="dim">@</tspan><tspan class="k">{HOST}</tspan>'
    f'</text></g>'
)
t += 0.25
y += LINE_H - 8

p.append(f'<g class="l" style="animation-delay:{t}s"><line x1="{LEFT}" y1="{y}" x2="{WIDTH - LEFT}" y2="{y}" stroke="#30363d"/></g>')
t += 0.25
y += LINE_H - 2

for key, val in ROWS:
    p.append(
        f'<g class="l" style="animation-delay:{round(t, 2)}s">'
        f'<text class="k" x="{LEFT}" y="{y}">{html.escape(key)}</text>'
        f'<text class="dim" x="{LEFT + KEY_W - 14}" y="{y}">:</text>'
        f'<text x="{LEFT + KEY_W}" y="{y}">{html.escape(val)}</text></g>'
    )
    t += 0.22
    y += LINE_H

y += 2
p.append(f'<g class="l" style="animation-delay:{round(t, 2)}s"><text x="{LEFT}" y="{y}" style="fill:#7ee787">$</text></g>')
p.append(f'<rect class="cur" x="{LEFT + 14}" y="{y - 13}" width="8" height="16" fill="#58a6ff"/>')

# ---------- pixel cat on laptop (right side) ----------
cat_css = """
@keyframes eyeblink { 0%, 92%, 100% { transform: scaleY(1); } 96% { transform: scaleY(0.1); } }
@keyframes tap { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
@keyframes floatup {
  0%   { opacity: 0; transform: translateY(0); }
  25%  { opacity: 1; }
  100% { opacity: 0; transform: translateY(-26px); }
}
@keyframes glow { 0%, 100% { opacity: 1; } 50% { opacity: 0.55; } }
.eye { transform-box: fill-box; transform-origin: center; animation: eyeblink 4s infinite; }
.paw1 { animation: tap 0.6s ease-in-out infinite; }
.paw2 { animation: tap 0.6s ease-in-out 0.3s infinite; }
.heart { opacity: 0; animation: floatup 3.5s ease-out 1s infinite; }
.logo { animation: glow 3s ease-in-out infinite; }
"""
p.append(f"<style>{cat_css}</style>")

S = 7
CX = WIDTH - 130
BASE_Y = HEIGHT // 2 + 55
LID_W, LID_H = 140, 90
LT = BASE_Y - LID_H

CAT = [
    ".XX......XX.",
    ".XXX....XXX.",
    ".XXXXXXXXXX.",
    "XXXXXXXXXXXX",
    "XXXXXXXXXXXX",
    "XXXXXXXXXXXX",
    ".XXXXXXXXXX.",
    "..XXXXXXXX..",
]
X0 = CX - 6 * S
Y0 = LT - 6 * S


def px(c, r, color, w=1, h=1, extra=""):
    return (f'<rect x="{X0 + c * S}" y="{Y0 + r * S}" width="{w * S}" height="{h * S}" '
            f'fill="{color}" {extra}/>')


# shadow
p.append(f'<ellipse cx="{CX}" cy="{BASE_Y + 14}" rx="76" ry="4" fill="#000" opacity="0.35"/>')

# cat head (drawn first, lid covers the lower rows)
p.append('<g shape-rendering="crispEdges">')
for r, row in enumerate(CAT):
    for c, ch in enumerate(row):
        if ch == "X":
            p.append(px(c, r, "#f0883e"))
p.append(px(2, 1, "#ff9ebc"))
p.append(px(9, 1, "#ff9ebc"))
p.append(px(4, 2, "#c2691f"))
p.append(px(7, 2, "#c2691f"))
p.append(px(5, 3, "#c2691f", 2, 1))
p.append(px(2, 5, "#ff9ebc", 1, 1, 'opacity="0.6"'))
p.append(px(9, 5, "#ff9ebc", 1, 1, 'opacity="0.6"'))
p.append(px(5, 5, "#ff7eb0", 2, 1))
for ex in (3, 8):
    p.append(
        f'<g class="eye">{px(ex, 3, "#0d1117", 1, 2)}'
        f'<rect x="{X0 + ex * S}" y="{Y0 + 3 * S}" width="3" height="3" fill="#ffffff"/></g>'
    )
p.append("</g>")

# whiskers
wy = Y0 + 5 * S + 3
for dy in (-3, 3):
    p.append(f'<line x1="{X0 - 12}" y1="{wy + dy * 2}" x2="{X0 + 4}" y2="{wy + dy}" stroke="#c9d1d9" stroke-opacity="0.5"/>')
    p.append(f'<line x1="{X0 + 12 * S + 12}" y1="{wy + dy * 2}" x2="{X0 + 12 * S - 4}" y2="{wy + dy}" stroke="#c9d1d9" stroke-opacity="0.5"/>')

# laptop lid + base
p.append(f'<rect x="{CX - LID_W // 2}" y="{LT}" width="{LID_W}" height="{LID_H}" rx="6" fill="#161b22" stroke="#484f58"/>')
p.append(f'<text class="logo" x="{CX}" y="{LT + 52}" text-anchor="middle" style="fill:#58a6ff;font-size:24px;font-weight:bold">&lt;/&gt;</text>')
p.append(f'<circle cx="{CX - 48}" cy="{LT + 74}" r="5" fill="#7ee787"/>')
p.append(f'<rect x="{CX + 34}" y="{LT + 68}" width="16" height="11" rx="3" fill="#d2a8ff"/>')
p.append(f'<circle cx="{CX + 20}" cy="{LT + 76}" r="4" fill="#ffa657"/>')
p.append(f'<rect x="{CX - 82}" y="{BASE_Y}" width="164" height="8" rx="4" fill="#30363d"/>')
p.append(f'<rect x="{CX - 14}" y="{BASE_Y}" width="28" height="3" rx="1.5" fill="#21262d"/>')

# paws on the lid
p.append(f'<rect class="paw1" x="{CX - 62}" y="{LT - 6}" width="14" height="12" rx="4" fill="#f5e6d3"/>')
p.append(f'<rect class="paw2" x="{CX + 48}" y="{LT - 6}" width="14" height="12" rx="4" fill="#f5e6d3"/>')

# floating pixel heart
HEART = [".X.X.", "XXXXX", ".XXX.", "..X.."]
hx = CX + 52
hy = Y0 - 6
p.append('<g class="heart" shape-rendering="crispEdges">')
for r, row in enumerate(HEART):
    for c, ch in enumerate(row):
        if ch == "X":
            p.append(f'<rect x="{hx + c * 3}" y="{hy + r * 3}" width="3" height="3" fill="#ff7b72"/>')
p.append("</g>")

# caption
caption = html.escape('$ git commit -m "meow"')
p.append(f'<text class="dim" x="{CX}" y="{BASE_Y + 36}" text-anchor="middle" style="font-size:11px">{caption}</text>')
# ------------------------------------------------------

p.append("</svg>")

with open("info-card.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(p))

print("Done: info-card.svg")