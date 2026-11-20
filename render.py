#!/usr/bin/env python3
"""Render the 19 Nov 2026 world-news front page for make.fun bounty
news-image-20261119. Deterministic, no network, Pillow only.
Output: 1024x1024 PNG, <= 1 MiB (bounty cap).
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
PAPER = (250, 246, 236)
INK = (17, 17, 17)
RED = (164, 30, 34)
BLUE = (27, 58, 107)
GREY = (90, 86, 78)
RULE = (60, 56, 48)

FD = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FD + name, size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 22  # margin

# ---------- masthead ----------
d.line([(M, 16), (W - M, 16)], fill=RULE, width=2)
d.text((M, 20), "EST. FOR MAKE.FUN  •  @ROBLOK-RF", font=F_SANS_B(11), fill=GREY)
d.text((W - M - d.textlength("No. 19  •  $250 BOUNTY", font=F_SANS_B(11)), 20),
       "No. 19  •  $250 BOUNTY", font=F_SANS_B(11), fill=GREY)
title = "THE WORLD IN ONE DAY"
tw = d.textlength(title, font=F_SERIF_B(56))
d.text(((W - tw) / 2, 36), title, font=F_SERIF_B(56), fill=INK)
d.line([(M, 100), (W - M, 100)], fill=RULE, width=3)
d.line([(M, 104), (W - M, 104)], fill=RULE, width=1)
dateline = "THURSDAY, 19 NOVEMBER 2026"
d.text((M, 110), dateline, font=F_SANS_B(15), fill=RED)
right = "36 STORIES  •  6 CONTINENTS  •  ONE FRONT PAGE"
d.text((W - M - d.textlength(right, font=F_SANS_B(13)), 111),
       right, font=F_SANS_B(13), fill=INK)

# ---------- lead block ----------
ly = 132
lead_w = 640
# kicker + headline
d.text((M, ly), "THE SUMMIT  —  SHENZHEN, CHINA", font=F_SANS_B(13), fill=RED)
y = draw_wrapped(d, M, ly + 20, "THREE LEADERS, ONE TABLE",
                 F_SERIF_B(40), lead_w, leading=44)
y = draw_wrapped(d, M, y + 6,
                 "Trump, Xi and Putin hold the first-ever trilateral summit — and pledge: “A nuclear war cannot be won.”",
                 F_SERIF(20), lead_w, leading=25)

# lead photo panel: Shenzhen skyline + three flags
px, py, pw, ph = 684, 132, 318, 168
# dusk sky gradient
for i in range(ph):
    t = i / ph
    r = int(27 + (214 - 27) * t)
    g = int(58 + (94 - 58) * t)
    b = int(107 + (58 - 107) * t)
    d.line([(px, py + i), (px + pw, py + i)], fill=(r, g, b))
# sun
d.ellipse([px + pw - 78, py + 18, px + pw - 38, py + 58], fill=(255, 196, 90))
# skyline
import random
random.seed(19)
bx = px + 8
while bx < px + pw - 30:
    bw = random.randint(22, 44)
    bh = random.randint(40, 96)
    d.rectangle([bx, py + ph - 40 - bh, bx + bw, py + ph - 40], fill=(16, 24, 44))
    for wy in range(py + ph - 34 - bh, py + ph - 44, 12):
        for wx in range(bx + 4, bx + bw - 4, 9):
            if random.random() < 0.45:
                d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 210, 110))
    bx += bw + 5
# three flags strip at bottom of panel
fy = py + ph - 40
d.rectangle([px, fy, px + pw, py + ph], fill=(12, 12, 12))
# US flag (simplified)
fx = px + 14
d.rectangle([fx, fy + 8, fx + 82, fy + 38], fill=(255, 255, 255))
for i in range(7):
    d.rectangle([fx, fy + 8 + i * 4, fx + 82, fy + 11 + i * 4], fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
d.rectangle([fx, fy + 8, fx + 34, fy + 24], fill=(30, 60, 120))
# China flag
fx = px + 118
d.rectangle([fx, fy + 8, fx + 82, fy + 38], fill=(222, 41, 16))
for sx, sy in [(fx + 10, fy + 13), (fx + 24, fy + 12), (fx + 30, fy + 20), (fx + 24, fy + 28), (fx + 12, fy + 25)]:
    d.ellipse([sx, sy, sx + 4, sy + 4], fill=(255, 222, 0))
# Russia flag
fx = px + 222
d.rectangle([fx, fy + 8, fx + 82, fy + 18], fill=(255, 255, 255))
d.rectangle([fx, fy + 18, fx + 82, fy + 28], fill=(0, 57, 166))
d.rectangle([fx, fy + 28, fx + 82, fy + 38], fill=(213, 0, 0))
d.rectangle([px, py, px + pw, py + ph], outline=INK, width=2)
d.text((px + 8, py + ph + 6), "SHENZHEN — THE TRILATERAL TABLE, APEC 2026",
       font=F_SANS_B(10), fill=GREY)

# ---------- photo strip (3 illustrated panels) ----------
sy = 316
spw = 318
gap = 12
panels = []
# A: cyclone spiral
p = Image.new("RGB", (spw, 92), (14, 60, 66))
pd = ImageDraw.Draw(p)
for r in range(8, 46, 6):
    pd.arc([spw // 2 - r, 46 - r, spw // 2 + r, 46 + r], start=200, end=200 + 260, fill=(255, 255, 255), width=3)
pd.ellipse([spw // 2 - 5, 41, spw // 2 + 5, 51], fill=(255, 196, 90))
panels.append((p, "CYCLONE AKVAN — 47,000 EVACUATED"))
# B: Voyager starfield
p = Image.new("RGB", (spw, 92), (8, 10, 26))
pd = ImageDraw.Draw(p)
random.seed(7)
for _ in range(70):
    sx, sy2 = random.randint(0, spw - 2), random.randint(0, 90)
    pd.ellipse([sx, sy2, sx + 2, sy2 + 2], fill=(255, 255, 255))
pd.line([(30, 70), (250, 26)], fill=(255, 196, 90), width=2)
pd.ellipse([246, 22, 258, 34], fill=(255, 196, 90))
pd.rectangle([258, 26, 272, 30], fill=(200, 200, 200))
panels.append((p, "VOYAGER 1 — ONE LIGHT-DAY FROM EARTH"))
# C: Vice City neon
p = Image.new("RGB", (spw, 92), (40, 8, 60))
pd = ImageDraw.Draw(p)
for i in range(92):
    t = i / 92
    pd.line([(0, i), (spw, i)], fill=(int(40 + 220 * t), int(8 + 60 * t), int(60 + 120 * t)))
pd.ellipse([spw - 90, 8, spw - 30, 68], fill=(255, 220, 130))
for bx in range(10, spw - 20, 26):
    pd.rectangle([bx, 62, bx + 18, 92], fill=(20, 6, 30))
panels.append((p, "VICE CITY — GTA VI IS OUT"))
for i, (p, cap) in enumerate(panels):
    x = M + i * (spw + gap)
    img.paste(p, (x, sy))
    d.rectangle([x, sy, x + spw, sy + 92], outline=INK, width=2)
    d.text((x + 4, sy + 96), cap, font=F_SANS_B(10), fill=GREY)

# ---------- columns ----------
stories = [
    # (section, headline, deck)
    ("DIPLOMACY", "Xi calls for destroying and banning nuclear weapons",
     "Disarmament tops the Shenzhen agenda."),
    ("DIPLOMACY", "Trump and Putin talk Ukraine for 40 minutes",
     "Zelensky fears talks held without him."),
    ("DIPLOMACY", "Trump and Xi: trade and fentanyl on the table",
     "Follows the red-carpet airport welcome."),
    ("DIPLOMACY", "APEC: 21 economies pledge trade, AI and supply chains",
     "Leaders meet in Shenzhen, Nov 18–19."),
    ("WAR", "Russian strikes kill at least five across Ukraine",
     "Power grids hit; regions lose electricity."),
    ("WAR", "Ukraine drones hit Kerch Bridge again",
     "Second strike halts traffic on the link."),
    ("WAR", "UK and Norway fund two Ukrainian naval craft",
     "Joint programme worth more than £100m."),
    ("WAR", "EU proposes €45bn loan for Ukraine in 2027",
     "€25bn military, €20bn budget support."),
    ("WASHINGTON", "Senate rejects Iran war-powers resolution, 51–48",
     "Three Republicans back it; one Democrat no."),
    ("ENERGY", "IEA: Iran war is the largest oil-and-gas disruption on record",
     "2.8bn barrels of oil, 60bn m³ of gas lost."),
    ("THE GULF", "Iran strikes US base in Kuwait and sites in Bahrain",
     "Retaliation after the US hit on Qeshm."),
    ("THE GULF", "Tankers hit mines and burn in the Strait of Hormuz",
     "Five tankers hit after entering banned routes."),
    ("THE GULF", "USS George Washington leaves the Gulf",
     "Carrier departs after three months on station."),
    ("THE GULF", "Ansarallah missile damages Saudi PIF tower",
     "Riyadh's tallest building hit in the strike."),
    ("GAZA", "Israel ends central Gaza ground operation",
     "Salah al-Din Road reopens as troops pull back."),
    ("GAZA", "Gaza peace plan scores 4 out of 26, aid groups say",
     "Five organisations grade the 20-point plan."),
    ("YEMEN", "Yemen: 64 children killed, 330,000 displaced",
     "UNICEF warns of a worsening winter crisis."),
    ("JUSTICE", "ICJ: Myanmar committed genocide against the Rohingya",
     "First state genocide ruling; ~10,000 killed."),
    ("JUSTICE", "Iraq jails six French ISIL recruits for life",
     "Six sentenced over joining the group."),
    ("INDIA", "Cyclone Akvan bears down on India's east coast",
     "47,000 evacuated; landfall due Friday noon."),
    ("INDIA", "Kashmir's 'last local militant' killed in Kulgam",
     "Forces kill commander Mohammad Lateef Bhat."),
    ("INDIA", "India slaps 162.5% duty on bulk Scotch",
     "Trade dispute with the UK escalates."),
    ("ASIA", "Malaysia ends visa-free entry for Indians",
     "Change takes effect 1 January 2027."),
    ("INDIA", "Air India crash probe in its final stage",
     "Government tells the Supreme Court; 260 died."),
    ("AMERICA", "Trump pardons Pete Rose posthumously",
     "Star died in 2024; banned over betting."),
    ("TECH", "Microsoft to retire To Do app in June 2027",
     "Users get seven months to move their lists."),
    ("MARKETS", "Anthropic raises a record $81.3bn in Nasdaq debut",
     "Priced at $83; valued near $1.5 trillion."),
    ("MARKETS", "Anthropic shares close up 17% on day one",
     "Biggest IPO ever; $107.3bn raised in all."),
    ("MARKETS", "Wall Street slides 2% for a fifth straight day",
     "S&P 500 down 2.02%; Dow falls 1,101 points."),
    ("TECH", "Nvidia beats forecasts but shares fall",
     "California probe opens after the Huang exit."),
    ("TECH", "US approved nearly 900,000 AI chip shipments to China",
     "House committee cites the export figures."),
    ("SPACE", "Voyager 1 becomes first object one light-day away",
     "Launched 1977; now ~26 billion km from Earth."),
    ("MONEY", "Buffett gives away $5.5bn, vows to donate 99%",
     "Berkshire shares go to four foundations."),
    ("CULTURE", "GTA VI launches worldwide after a 13-year wait",
     "Midnight unlock; $79.99 / $99.99 editions."),
]
assert len(stories) == 34, len(stories)

cols = [
    ("SUMMIT & WAR", stories[0:9]),
    ("THE GULF & THE COURTS", stories[9:18]),
    ("ASIA & AMERICA", stories[18:26]),
    ("MARKETS, TECH & CULTURE", stories[26:34]),
]
col_w = 232
col_gap = 12
cy = 436
d.line([(M, cy - 8), (W - M, cy - 8)], fill=RULE, width=2)
for ci, (chead, cstories) in enumerate(cols):
    cx = M + ci * (col_w + col_gap)
    d.text((cx, cy), chead, font=F_SANS_B(12), fill=RED)
    d.line([(cx, cy + 18), (cx + col_w, cy + 18)], fill=RED, width=2)
    y = cy + 26
    for sec, head, deck in cstories:
        d.text((cx, y), sec, font=F_SANS_B(9), fill=GREY)
        y += 10
        y = draw_wrapped(d, cx, y, head, F_SANS_B(12), col_w, leading=13, max_lines=2)
        y = draw_wrapped(d, cx, y + 1, deck, F_SANS(10), col_w, leading=11, max_lines=1)
        y += 4
        d.line([(cx, y), (cx + col_w, y)], fill=(200, 194, 178), width=1)
        y += 4

# ---------- footer ----------
fy = 966
d.line([(M, fy), (W - M, fy)], fill=RULE, width=2)
d.text((M, fy + 6),
       "36 stories  •  Sources: Le Monde, WSJ, USA Today, Reuters, UN News, The Hindu, Motley Fool",
       font=F_SANS(10), fill=GREY)
d.text((M, fy + 20),
       "Built by @roblok-rf for make.fun  •  news-image-20261119  •  $250 bounty  •  Image: 1024 × 1024",
       font=F_SANS_B(10), fill=INK)

img.save("/home/hatch/workspace/bounty-news-19nov/entry.png", optimize=True)
print("saved", img.size)
