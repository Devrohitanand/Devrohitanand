import html
from PIL import Image, ImageOps

SRC = "avatar.png"
OUT = "ascii-portrait.svg"

W, H = 300, 458          # window size (height matches the info card)
ART_X, ART_Y = 15, 44    # where the portrait starts
COLS, ROWS = 75, 56      # character grid
CW, LH = 3.6, 6          # char width / line height (px)
RAMP = " .:1l7I40#8@"    # light -> dense (numbers + symbols)
FILL = "#b6c2cf"

# ---------- image -> grid ----------
raw = Image.open(SRC)
if raw.mode in ("RGBA", "LA", "P"):
    raw = raw.convert("RGBA")
    bg = Image.new("RGBA", raw.size, "white")
    bg.alpha_composite(raw)
    raw = bg
img = raw.convert("L")

iw, ih = img.size
ratio = (COLS * CW) / (ROWS * LH)
cw, ch = int(ih * ratio), ih
if cw > iw:
    cw, ch = iw, int(iw / ratio)
left, top = (iw - cw) // 2, (ih - ch) // 2
img = img.crop((left, top, left + cw, top + ch)).resize((COLS, ROWS), Image.LANCZOS)
img = ImageOps.autocontrast(img, cutoff=2)
px = img.load()

rows = []
for r in range(ROWS):
    line = ""
    for c in range(COLS):
        dark = (1 - px[c, r] / 255) ** 0.8
        if dark < 0.1:
            line += " "
        else:
            line += RAMP[int(dark * (len(RAMP) - 1) + 0.5)]
    rows.append(line)

# ---------- svg ----------
ART_W = COLS * CW
step = 0.035
art_end = round(ROWS * step + 0.6, 2)

css = """
@keyframes in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
@keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }
text { font-family: Consolas, 'Courier New', monospace; }
.art { font-size: 6px; fill: FILL; white-space: pre; }
.cap { opacity: 0; animation: in 0.6s ease-out ART_ENDs forwards; }
.cur { opacity: 0; animation: blink 1s steps(1) ART_ENDs infinite; }
.nm { font-size: 15px; font-weight: bold; fill: #e6edf3; }
.rl { font-size: 12px; fill: #8b949e; }
""".replace("FILL", FILL).replace("ART_END", str(art_end))

p = []
p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
p.append(f"<style>{css}</style>")
p.append("<defs>")
for i, line in enumerate(rows):
    t = round(i * step, 2)
    y = ART_Y + i * LH
    p.append(
        f'<clipPath id="c{i}"><rect x="{ART_X}" y="{y}" width="0" height="{LH + 1}">'
        f'<animate attributeName="width" from="0" to="{ART_W}" begin="{t}s" dur="0.5s" fill="freeze"/>'
        f"</rect></clipPath>"
    )
p.append("</defs>")

p.append(f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>')
p.append('<circle cx="18" cy="16" r="4" fill="#ff5f56"/><circle cx="32" cy="16" r="4" fill="#ffbd2e"/><circle cx="46" cy="16" r="4" fill="#27c93f"/>')
p.append(f'<line x1="0" y1="30" x2="{W}" y2="30" stroke="#21262d"/>')

for i, line in enumerate(rows):
    stripped = line.strip(" ")
    if not stripped:
        continue
    lead = len(line) - len(line.lstrip(" "))
    x = ART_X + lead * CW
    y = ART_Y + (i + 1) * LH - 1
    t = round(i * step, 2)
    p.append(
        f'<text class="art" x="{x:.1f}" y="{y}" textLength="{len(stripped) * CW:.1f}" '
        f'lengthAdjust="spacing" xml:space="preserve" clip-path="url(#c{i})">{html.escape(stripped)}</text>'
    )
    p.append(
        f'<rect x="{ART_X}" y="{ART_Y + i * LH}" width="3" height="{LH}" fill="#58a6ff" opacity="0">'
        f'<animate attributeName="x" from="{ART_X}" to="{ART_X + ART_W}" begin="{t}s" dur="0.5s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.02;0.95;1" begin="{t}s" dur="0.5s" fill="freeze"/>'
        f"</rect>"
    )

cy = ART_Y + ROWS * LH + 34
p.append(f'<g class="cap"><text class="nm" x="{ART_X + 2}" y="{cy}">rohit</text>')
p.append(f'<text class="rl" x="{ART_X + 2}" y="{cy + 20}">Full-Stack Developer</text></g>')
p.append(f'<rect class="cur" x="{ART_X + 2 + 140}" y="{cy + 8}" width="7" height="13" fill="#58a6ff"/>')

p.append("</svg>")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(p))

print("Done:", OUT)