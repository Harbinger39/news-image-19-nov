#!/usr/bin/env python3
"""Build the dense newspaper front page for 19 Nov 2026 (make.fun news-image-20261119).
All visuals are flat illustrations drawn in code; all text is drawn with real fonts.
Output: ~/workspace/makefun/news19-entry/entry.png (1024x1024, PNG)."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.expanduser("~/workspace/makefun/news19-entry/entry.png")
W, H = 1024, 1024
PAPER = (248, 244, 235)
INK = (18, 18, 18)
GREY = (96, 94, 88)
LGREY = (150, 147, 138)
RED = (178, 24, 24)
GREEN = (22, 110, 52)
BLUE = (28, 68, 160)
ORANGE = (176, 96, 8)
SKY = (214, 230, 242)
SAND = (238, 228, 205)
SEA = (52, 110, 165)

FB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
text(d, W // 2, 2, "THE WORLD TODAY", f(FB, 58), anchor="ma")
# black date bar
d.rectangle([16, 62, 1008, 86], fill=INK)
text(d, 28, 67, "THURSDAY 19 NOVEMBER 2026", f(SB, 14), fill=(255, 255, 255))
text(d, 996, 68, "33 STORIES  ·  7 REGIONS  ·  ALL FROM THIS THURSDAY", f(SB, 11),
     fill=(255, 255, 255), anchor="ra")

# ---------------------------------------------------------------- numbers strip
nums = [
    ("3", "PRESIDENTS AT ONE TABLE", "Trump · Xi · Putin"),
    ("9–6", "WORLD COURT VOTE", "Myanmar: genocide"),
    ("$81bn", "ANTHROPIC IPO", "largest ever"),
    ("$97.17", "ANT CLOSE, +17%", "priced at $83"),
    ("109–0", "DENMARK VOTES YES", "Greenland deal"),
    ("4.9%", "AUSTRALIA JOBLESS", "5-year high"),
]
y0, y1 = 92, 132
d.line([16, y0, 1008, y0], fill=INK, width=2)
cw = 992 / 6
for i, (n, lab, sub) in enumerate(nums):
    cx = 16 + cw * i + cw / 2
    text(d, cx, y0 + 3, n, f(FB, 24), anchor="ma")
    text(d, cx, y0 + 31, lab, f(SB, 8), anchor="ma")
    if i < 5:
        d.line([16 + cw * (i + 1), y0 + 4, 16 + cw * (i + 1), y1 - 4], fill=LGREY, width=1)
d.line([16, y1, 1008, y1], fill=INK, width=2)

# ---------------------------------------------------------------- timeline strip
text(d, 16, 138, "THE DAY, HOUR BY HOUR  —  TIMES UTC", f(SB, 9), fill=GREY)
tl = [
    ("00:30", "Australia: jobless hits 4.9%"),
    ("MORNING", "Three presidents meet in Shenzhen"),
    ("05:21", "Three tankers on fire off Hormuz"),
    ("10:22", "Two more supertankers explode"),
    ("14:30", "Blast outside Austria's Kyiv embassy"),
    ("16:50", "Anthropic opens at $111.50"),
    ("21:00", "Dow closes down 1,101"),
]
tw = 992 / 7
for i, (t, s) in enumerate(tl):
    x = 16 + tw * i + 4
    text(d, x, 150, t, f(SB, 11), fill=RED)
    for j, ln in enumerate(wrap(d, s, f(SR, 10), tw - 10)):
        text(d, x, 164 + j * 11, ln, f(SR, 10))
    if i < 6:
        d.line([16 + tw * (i + 1), 150, 16 + tw * (i + 1), 184], fill=LGREY, width=1)
d.line([16, 188, 1008, 188], fill=INK, width=2)

# ---------------------------------------------------------------- flat illustrations
def flag_trio(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # table
    d.ellipse([x + w * 0.18, y + h * 0.72, x + w * 0.82, y + h * 0.92], fill=(120, 72, 40))
    d.rectangle([x + w * 0.15, y + h * 0.70, x + w * 0.85, y + h * 0.78], fill=(150, 95, 55))
    flags = [
        # US: red/white stripes + blue canton
        (0.10, [(255, 255, 255), (178, 24, 24)]),
        # China: red + star
        (0.42, None),
        # Russia: white/blue/red tricolour
        (0.74, None),
    ]
    for fx, kind in flags:
        px = x + w * fx
        d.line([px, y + 8, px, y + h * 0.68], fill=INK, width=2)
        fw, fh = w * 0.22, h * 0.30
        if kind is not None:  # US
            for s in range(5):
                d.rectangle([px, y + 8 + s * fh / 5, px + fw, y + 8 + (s + 1) * fh / 5],
                            fill=(178, 24, 24) if s % 2 == 0 else (255, 255, 255))
            d.rectangle([px, y + 8, px + fw * 0.45, y + 8 + fh * 0.55], fill=(28, 68, 160))
        elif fx < 0.5:  # China
            d.rectangle([px, y + 8, px + fw, y + 8 + fh], fill=(222, 32, 32))
            d.text((px + fw * 0.22, y + 8 + fh * 0.18), "\u2605", font=f(SB, 12), fill=(255, 220, 60))
        else:  # Russia
            d.rectangle([px, y + 8, px + fw, y + 8 + fh / 3], fill=(255, 255, 255))
            d.rectangle([px, y + 8 + fh / 3, px + fw, y + 8 + 2 * fh / 3], fill=(28, 68, 160))
            d.rectangle([px, y + 8 + 2 * fh / 3, px + fw, y + 8 + fh], fill=(200, 30, 30))


def scales(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    cx, top = x + w / 2, y + 10
    d.line([cx, top, cx, y + h - 12], fill=INK, width=3)
    d.line([cx - w * 0.34, top + 8, cx + w * 0.34, top + 8], fill=INK, width=3)
    d.ellipse([cx - 5, top - 4, cx + 5, top + 6], fill=RED)
    for sgn in (-1, 1):
        px = cx + sgn * w * 0.34
        d.line([px, top + 8, px - 14, y + h * 0.52], fill=INK, width=2)
        d.line([px, top + 8, px + 14, y + h * 0.52], fill=INK, width=2)
        d.arc([px - 15, y + h * 0.50, px + 15, y + h * 0.72], 0, 180, fill=INK, width=3)
    d.rectangle([cx - 22, y + h - 12, cx + 22, y + h - 6], fill=INK)


def factory(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 226))
    # factory block + sawtooth roof
    d.rectangle([x + w * 0.08, y + h * 0.48, x + w * 0.62, y + h * 0.88], fill=(120, 122, 118))
    d.polygon([(x + w * 0.08, y + h * 0.48), (x + w * 0.20, y + h * 0.34),
               (x + w * 0.32, y + h * 0.48), (x + w * 0.44, y + h * 0.34),
               (x + w * 0.56, y + h * 0.48), (x + w * 0.62, y + h * 0.42),
               (x + w * 0.62, y + h * 0.48)], fill=(96, 98, 94))
    d.rectangle([x + w * 0.66, y + h * 0.18, x + w * 0.76, y + h * 0.88], fill=(96, 98, 94))
    for i in range(3):
        d.ellipse([x + w * 0.67 + i * 3, y + h * 0.06 + i * 2, x + w * 0.75 - i * 2,
                   y + h * 0.16 + i * 2], fill=(200, 200, 196))
    # red down arrow
    ax = x + w * 0.86
    d.line([ax, y + h * 0.22, ax, y + h * 0.72], fill=RED, width=4)
    d.polygon([(ax - 8, y + h * 0.62), (ax + 8, y + h * 0.62), (ax, y + h * 0.80)], fill=RED)


def chart_line(x, y, w, h, pts, colour=INK):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.line([x + 6, y + h - 6, x + w - 4, y + h - 6], fill=LGREY, width=1)
    d.line([x + 6, y + 6, x + 6, y + h - 6], fill=LGREY, width=1)
    xs = [x + 8 + i * (w - 16) / (len(pts) - 1) for i in range(len(pts))]
    lo, hi = min(pts), max(pts)
    ys = [y + h - 8 - (p - lo) / (hi - lo + 1e-9) * (h - 16) for p in pts]
    d.line(list(zip(xs, ys)), fill=colour, width=3)
    for px, py in zip(xs, ys):
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=colour)


def tanker(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    d.rectangle([x + w * 0.12, y + h * 0.44, x + w * 0.88, y + h * 0.64], fill=(40, 40, 40))
    d.rectangle([x + w * 0.66, y + h * 0.26, x + w * 0.82, y + h * 0.44], fill=(240, 240, 240))
    for fx in (0.24, 0.48):
        px = x + w * fx
        d.polygon([(px, y + h * 0.46), (px + 7, y + h * 0.14), (px + 14, y + h * 0.46)],
                  fill=(230, 120, 20))
        d.polygon([(px + 4, y + h * 0.40), (px + 9, y + h * 0.24), (px + 14, y + h * 0.40)],
                  fill=(255, 200, 40))


def building_crack(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    bx, bw = x + w * 0.18, w * 0.64
    d.rectangle([bx, y + h * 0.22, bx + bw, y + h * 0.92], fill=(196, 178, 150))
    d.polygon([(bx - 4, y + h * 0.22), (bx + bw / 2, y + h * 0.08), (bx + bw + 4, y + h * 0.22)],
              fill=(150, 130, 105))
    for r in range(3):
        for c in range(4):
            d.rectangle([bx + 8 + c * (bw - 16) / 4, y + h * 0.30 + r * h * 0.20,
                         bx + 8 + (c + 0.6) * (bw - 16) / 4, y + h * 0.30 + r * h * 0.20 + 8],
                        fill=(60, 70, 90))
    d.line([(bx + bw * 0.55, y + h * 0.10), (bx + bw * 0.45, y + h * 0.35),
            (bx + bw * 0.60, y + h * 0.55), (bx + bw * 0.48, y + h * 0.80)],
           fill=INK, width=2)


def controller(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 248))
    cx, cy = x + w / 2, y + h * 0.52
    d.rounded_rectangle([cx - w * 0.38, cy - h * 0.22, cx + w * 0.38, cy + h * 0.26],
                        radius=12, fill=(90, 50, 160))
    d.ellipse([cx - w * 0.24, cy - 4, cx - w * 0.24 + 12, cy + 8], fill=(40, 40, 40))
    d.ellipse([cx + w * 0.24 - 12, cy - 4, cx + w * 0.24, cy + 8], fill=(40, 40, 40))
    for dx, dy, col in ((0.16, -0.10, (255, 220, 60)), (0.24, -0.02, (255, 120, 120)),
                        (0.16, 0.06, (120, 220, 120)), (0.08, -0.02, (140, 200, 255))):
        d.ellipse([cx + w * dx - 3, cy + h * dy - 3, cx + w * dx + 3, cy + h * dy + 3], fill=col)
    d.line([cx - w * 0.30, cy - h * 0.08, cx - w * 0.22, cy - h * 0.08], fill=(255, 255, 255), width=2)
    d.line([cx - w * 0.26, cy - h * 0.14, cx - w * 0.26, cy - h * 0.02], fill=(255, 255, 255), width=2)


def bridge(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h * 0.66, x + w, y + h], fill=SEA)
    for tx in (0.22, 0.72):
        d.rectangle([x + w * tx, y + h * 0.18, x + w * tx + 5, y + h * 0.66], fill=(90, 90, 90))
    d.rectangle([x + w * 0.06, y + h * 0.52, x + w * 0.44, y + h * 0.58], fill=(60, 60, 60))
    d.rectangle([x + w * 0.62, y + h * 0.52, x + w * 0.94, y + h * 0.58], fill=(60, 60, 60))
    d.polygon([(x + w * 0.44, y + h * 0.52), (x + w * 0.53, y + h * 0.70),
               (x + w * 0.62, y + h * 0.52)], fill=(60, 60, 60))
    d.line([x + w * 0.24, y + h * 0.18, x + w * 0.44, y + h * 0.52], fill=LGREY, width=1)
    d.line([x + w * 0.74, y + h * 0.18, x + w * 0.62, y + h * 0.52], fill=LGREY, width=1)


def parliament(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    d.polygon([(x + w * 0.15, y + h * 0.30), (x + w * 0.50, y + h * 0.10),
               (x + w * 0.85, y + h * 0.30)], fill=(120, 100, 80))
    d.rectangle([x + w * 0.15, y + h * 0.30, x + w * 0.85, y + h * 0.88], fill=(210, 196, 168))
    for i in range(5):
        cx = x + w * (0.24 + i * 0.13)
        d.rectangle([cx - 3, y + h * 0.38, cx + 3, y + h * 0.82], fill=(255, 255, 255))
    d.ellipse([x + w * 0.80, y + h * 0.55, x + w * 0.98, y + h * 0.73], outline=GREEN, width=4)
    d.line([x + w * 0.83, y + h * 0.65, x + w * 0.87, y + h * 0.69, x + w * 0.95, y + h * 0.58],
           fill=GREEN, width=4)


def cyclone(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cx, cy = x + w * 0.5, y + h * 0.52
    for r in range(6, 30, 6):
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], 20 + r * 8, 200 + r * 8,
              fill=(30, 90, 160), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(30, 90, 160))
    for dx in (-0.32, -0.10, 0.14, 0.34):
        d.line([x + w * (0.5 + dx), y + h * 0.82, x + w * (0.5 + dx) - 2, y + h * 0.94],
               fill=(60, 120, 200), width=2)


def dotgrid(x, y, w, h, red=4, total=26):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    cols, rows = 13, 2
    cw, ch = w / cols, h / rows
    for i in range(total):
        c, r = i % cols, i // cols
        cx, cy = x + cw * (c + 0.5), y + ch * (r + 0.5)
        col = RED if i < red else (190, 190, 190)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=col)


def bars_up(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    vals = [0.62, 0.78, 1.0]
    bw = w / 5
    for i, v in enumerate(vals):
        bx = x + bw * (0.6 + i * 1.4)
        d.rectangle([bx, y + h - 6 - v * (h - 16), bx + bw * 0.9, y + h - 6],
                    fill=(28, 68, 160) if i < 2 else RED)
    d.line([x + 6, y + h - 6, x + w - 4, y + h - 6], fill=LGREY, width=1)

# ---------------------------------------------------------------- leads
LEADS = [
    ("1 · ASIA · DIPLOMACY", "TRUMP, XI AND PUTIN HOLD FIRST THREE-WAY SUMMIT",
     "The three leaders meet in Shenzhen and sign a four-point “Declaration toward Peace”, "
     "pledging further talks on cutting nuclear risks.",
     "CONFIRMED", "White House · Al Jazeera", flag_trio),
    ("2 · JUSTICE · THE HAGUE", "WORLD COURT: MYANMAR COMMITTED GENOCIDE",
     "The ICJ rules 9–6 that Myanmar committed genocide against the Rohingya in 2017 — the "
     "first time the court has held a state responsible.",
     "CONFIRMED", "Al Jazeera · Le Monde", scales),
    ("3 · CLIMATE · ANTALYA", "COP31 DRAFT DROPS FOSSIL FUELS",
     "The new draft deal removes all mention of moving away from coal, oil and gas, but keeps "
     "a target of 35% clean electricity by 2035. Final deal due Friday.",
     "CONFIRMED", "Reuters · UN News", factory),
]
TAGCOL = {"CONFIRMED": GREEN, "REPORTED": ORANGE, "CLAIM": RED}
for i, (lab, head, summ, tag, src, ill) in enumerate(LEADS):
    x = 16 + i * 334
    lw = 322
    ill(x, 194, lw, 92)
    text(d, x, 292, lab, f(SB, 10), fill=RED)
    y = 306
    for ln in wrap(d, head, f(FB, 20), lw):
        text(d, x, y, ln, f(FB, 20))
        y += 23
    y += 2
    for ln in wrap(d, summ, f(SR, 11), lw):
        text(d, x, y, ln, f(SR, 11))
        y += 14
    text(d, x, 402, tag, f(SB, 9), fill=TAGCOL[tag])
    text(d, x + d.textlength(tag, font=f(SB, 9)) + 6, 402, "· " + src, f(SR, 9), fill=GREY)
d.line([16, 418, 1008, 418], fill=INK, width=2)

# ---------------------------------------------------------------- cards (5 x 2)
CARDS = [
    ("4 · MARKETS · NEW YORK", "ANTHROPIC SOARS ON DEBUT",
     "Priced at $83, it opens at $111.50 and closes at $97.17 — up 17%.",
     "CONFIRMED", "WSJ · Al Jazeera", lambda x, y, w, h: chart_line(x, y, w, h, [83, 111.5, 97.17], BLUE)),
    ("5 · ENERGY · GULF", "TANKERS BURN AFTER MINE STRIKES",
     "Three tankers catch fire east of Hormuz; two more supertankers explode later.",
     "REPORTED", "IRNA · Al Arabiya", tanker),
    ("6 · WAR · UKRAINE", "TWO EMBASSIES HIT IN KYIV",
     "Russian strikes hit the Austrian and Dutch embassies. One person is killed.",
     "CONFIRMED", "CNA · Kyiv Independent", building_crack),
    ("7 · GAMING · WORLDWIDE", "GTA VI ARRIVES AFTER 13 YEARS",
     "Rockstar's sequel launches to a 99/100 Metacritic score after a 13-year wait.",
     "CONFIRMED", "Al Jazeera · Rockstar", controller),
    ("8 · WAR · CRIMEA", "KERCH BRIDGE HIT A THIRD TIME",
     "A midnight strike halts rail traffic — the third attack in four days.",
     "REPORTED", "One Turn · Reuters", bridge),
    ("9 · EUROPE · COPENHAGEN", "DENMARK VOTES 109–0 ON GREENLAND",
     "Parliament unanimously approves the US–Greenland security deal.",
     "CONFIRMED", "Al Jazeera · AP", parliament),
    ("10 · WEATHER · INDIA", "300,000 FLEE CYCLONE AKVAN",
     "A severe cyclone nears India's east coast; landfall is due Friday at noon.",
     "CONFIRMED", "IMD · The Hindu", cyclone),
    ("11 · MARKETS · NEW YORK", "DOW DROPS 1,101 POINTS",
     "The Dow closes below 50,000 as US stocks fall for a fifth straight day.",
     "CONFIRMED", "AP · Morningstar", lambda x, y, w, h: chart_line(x, y, w, h, [100, 96, 88, 80], RED)),
    ("12 · MIDDLE EAST · GAZA", "GAZA PEACE PLAN SCORES 4 OUT OF 26",
     "Aid groups score the plan 4/26, down from 5 in April.",
     "CONFIRMED", "ReliefWeb · Al Jazeera", lambda x, y, w, h: dotgrid(x, y, w, h, 4, 26)),
    ("13 · ECONOMY · AUSTRALIA", "AUSTRALIA'S JOBLESS HITS 4.9%",
     "Unemployment hits a five-year high as 43,500 jobs are lost in October.",
     "CONFIRMED", "ABS · FXStreet", bars_up),
]
for i, (lab, head, summ, tag, src, ill) in enumerate(CARDS):
    col, row = i % 5, i // 5
    x = 16 + col * 200
    y = 426 + row * 141
    cw = 192
    ill(x, y, cw, 44)
    text(d, x, y + 48, lab, f(SB, 8), fill=RED)
    yy = y + 60
    for ln in wrap(d, head, f(FB, 13), cw):
        text(d, x, yy, ln, f(FB, 13))
        yy += 16
    yy = y + 94
    for ln in wrap(d, summ, f(SR, 10), cw):
        text(d, x, yy, ln, f(SR, 10))
        yy += 11
    text(d, x, y + 128, tag, f(SB, 8), fill=TAGCOL[tag])
    text(d, x + d.textlength(tag, font=f(SB, 8)) + 5, y + 128, "· " + src, f(SR, 8), fill=GREY)
d.line([16, 708, 1008, 708], fill=INK, width=2)

# ---------------------------------------------------------------- bottom third headers
text(d, 16, 714, "WHERE IT HAPPENED", f(SB, 12))
text(d, 416, 714, "ALSO ON THURSDAY — 20 MORE STORIES", f(SB, 12))

# ---------------------------------------------------------------- dotted world map
LAND = [
    (0, [(16, 16), (21, 26), (32, 34), (45, 48)]),
    (1, [(2, 27), (42, 58)]),
    (2, [(2, 26), (31, 59)]),
    (3, [(2, 25), (31, 59)]),
    (4, [(4, 21), (29, 59)]),
    (5, [(8, 22), (29, 59)]),
    (6, [(9, 24), (30, 59)]),
    (7, [(10, 25), (29, 55)]),
    (8, [(11, 25), (30, 53)]),
    (9, [(12, 25), (29, 52)]),
    (10, [(13, 25), (29, 52)]),
    (11, [(16, 20), (28, 46), (48, 52)]),
    (12, [(17, 19), (27, 46), (48, 51)]),
    (13, [(18, 20), (27, 40), (43, 45), (49, 55)]),
    (14, [(18, 22), (28, 40), (49, 58)]),
    (15, [(19, 24), (29, 40), (50, 58)]),
    (16, [(19, 26), (30, 40), (51, 58)]),
    (17, [(20, 27), (31, 39), (52, 55)]),
    (18, [(20, 27), (31, 38), (49, 56)]),
    (19, [(21, 27), (31, 38), (49, 56)]),
    (20, [(21, 27), (31, 36), (49, 55)]),
    (21, [(22, 26), (32, 35), (50, 55)]),
    (22, [(22, 25), (32, 34), (50, 54), (57, 58)]),
    (23, [(23, 25), (51, 54), (57, 58)]),
    (24, [(23, 24), (54, 54), (57, 58)]),
    (25, [(23, 24), (57, 57)]),
    (26, [(23, 24)]),
    (27, [(23, 23)]),
]
MX0, MY0, MW, MH = 16, 732, 384, 150
for r, spans in LAND:
    for c0, c1 in spans:
        for c in range(c0, c1 + 1):
            cx = MX0 + (c + 0.5) * MW / 60
            cy = MY0 + (r + 0.5) * MH / 28
            d.ellipse([cx - 1.7, cy - 1.7, cx + 1.7, cy + 1.7], fill=(70, 70, 66))

PINS = [  # number, lon, lat, dx, dy
    (1, 114.1, 22.5, 0, 0),
    (2, 4.3, 52.1, 0, 0),
    (3, 30.7, 36.9, -4, 8),
    (4, -74.0, 40.7, 0, 0),
    (5, 56.5, 26.5, 0, -6),
    (6, 30.5, 50.5, -12, -8),
    (7, -80.2, 25.8, 0, 0),
    (8, 36.4, 45.3, 12, -8),
    (9, 12.6, 55.7, 0, -14),
    (10, 85.0, 18.0, 0, 0),
    (11, -74.0, 40.7, 16, -12),
    (12, 34.5, 31.5, 10, 8),
    (13, 151.2, -33.9, 0, 0),
]
for n, lon, lat, dx, dy in PINS:
    px = MX0 + (lon + 180) / 360 * MW
    py = MY0 + (80 - lat) / 140 * MH
    cx, cy = px + dx, py + dy
    d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)
    if dx or dy:
        d.line([px, py, cx, cy], fill=GREY, width=1)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255), width=1)
    text(d, cx, cy - 5, str(n), f(SB, 9), fill=(255, 255, 255), anchor="ma")
# ---------------------------------------------------------------- DATE CHECK box
bx0, by0, bx1, by1 = 16, 890, 400, 962
d.rectangle([bx0, by0, bx1, by1], outline=RED, width=2)
text(d, bx0 + 8, by0 + 5, "DATE CHECK — WHAT WE LEFT OUT", f(SB, 11), fill=RED)
yy = by0 + 21
text(d, bx0 + 8, yy, "NOT THURSDAY:", f(SB, 10))
yy += 12
for ln in wrap(d, "EU €45bn Ukraine loan (Wed) · Jeffries as Speaker (Wed) · Nvidia earnings (Tue) · Iran/Kuwait drones (Wed)",
               f(SR, 10), bx1 - bx0 - 16):
    text(d, bx0 + 8, yy, ln, f(SR, 10))
    yy += 12
yy += 2
text(d, bx0 + 8, yy, "NOT YET:  COP31 final deal (due Fri) · Akvan landfall (due Fri noon)",
     f(SR, 10))

# ---------------------------------------------------------------- ALSO list
ALSO = [
    ("EUROPE", [
        "Berlin: allies meet; Zelensky urges faster €45bn rollout",
        "EU summons Russia's envoy over the Kyiv strikes",
        "Dutch summon Russia's ambassador over Kyiv",
        "France jails three women for joining ISIS in Syria",
    ]),
    ("MIDDLE EAST & AFRICA", [
        "Houthi missiles damage Riyadh's PIF tower",
        "Iraq: government and militia end Jurf al-Sakhar standoff",
        "Taiz water output nearly halved; 800,000 cut off from aid",
        "Houthi media: Saudi strikes kill 11 in Yemen",
        "IDF's Nuseirat operation in Gaza ends",
    ]),
    ("SCIENCE & CULTURE", [
        "NASA confirms Voyager 1 is one light-day from Earth",
        "“Human” is Cambridge Dictionary's Word of the Year",
    ]),
    ("ASIA", [
        "Mongolia's parliament accepts the president's resignation",
        "Pakistan army says 22 militants killed in raids",
        "Bangladesh deploys paramilitary amid Hasina unrest",
        "Pakistan FM reveals role in US–Iran June deal",
    ]),
    ("AMERICAS", [
        "US arrests alleged Russian agent spying on a tech firm",
        "US reissues warnings for citizens in Bahrain, Saudi",
        "Hegseth lands in Ecuador on anti-narcotics tour",
        "Pakistani gets 27 years over plot to kill Trump",
        "US outage wave blamed on old systems, AI fixes",
    ]),
]
cols = [ALSO[:3], ALSO[3:]]
for ci, groups in enumerate(cols):
    x = 416 + ci * 302
    y = 732
    for gname, items in groups:
        text(d, x, y, gname, f(SB, 9), fill=RED)
        y += 14
        for it in items:
            for j, ln in enumerate(wrap(d, "·  " + it, f(SR, 10), 290)):
                text(d, x, y, ln, f(SR, 10))
                y += 12
        y += 6

# ---------------------------------------------------------------- footer
d.line([16, 970, 1008, 970], fill=INK, width=2)
text(d, 16, 976,
     "SOURCES: Reuters · AP · Al Jazeera · White House · UN News · WSJ · IRNA · CNA · Kyiv Independent · IMD · ABS · The Hindu · Dawn · NDTV · Rockstar · NASA",
     f(SR, 9), fill=GREY)
text(d, 16, 990,
     "All 33 stories are from Thursday 19 November 2026. CONFIRMED means verified by more than one source; REPORTED means the claim is attributed to the source named.",
     f(SR, 9), fill=GREY)
text(d, W // 2, 1004, "THE WORLD TODAY  ·  THURSDAY 19 NOVEMBER 2026", f(SB, 9), fill=GREY,
     anchor="ma")

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes", img.size)
