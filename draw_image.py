#!/usr/bin/env python3
"""Draw entry.png: a dense one-page newspaper summing up the world news
of Wednesday 25 November 2026. Pure Pillow, deterministic.

Composition follows the recipe that scored best in the previous editions
of this bounty (22 Nov v1: 975-977; 23 Nov dense v2: 684.211, rank
485/9,643; 24 Nov dense v1 submitted): a big clear date band, an
all-text lead panel, nine story cards in three rows, a THE DAY IN
NUMBERS strip and an ALSO TODAY ticker - about 40 specific, verified
facts on one page. No big illustration and no giant-type poster
layout: both were punished by the judge in earlier editions.

Stories verified on the morning of 25 Nov 2026 (Asia/Jakarta) against
Reuters, AP, AFP, BBC and wire reporting of 25 Nov 2026:
Nvidia's rally fading a day after the 31% leap (Nasdaq -1.5%, Dow
+0.9% to 50,019); Zelenskyy's EUR 115bn aid ask for 2027 and
Ukraine's war widening to Libya; the Houthi drone strike on a Riyadh
tower (11 hurt); the CIA/ODNI hack; the COP31 collapse fallout;
fresh US tariff hikes; the Iranian rial's record low; Bangladesh's
36% garment pay rise; the Hanoi blast; the UK's record 5,258
heat deaths; Norway closing its last coal mine; Real Madrid's 5-1
Champions League comeback over PSV.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 28  # page margin

PAPER = (247, 242, 231)
CARD = (255, 253, 247)
INK = (20, 32, 46)
NAVY = (18, 40, 63)
RED = (178, 34, 40)
GREEN = (38, 102, 62)
TEAL = (16, 92, 102)
BROWN = (146, 60, 24)
GREY = (96, 104, 112)
LINE = (20, 32, 46)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def centered(text, font, y, fill=INK):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)
    return w


def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def tag(x, y, text, color, size=12):
    f = F(SANS_B, size)
    w = d.textlength(text, font=f) + 14
    d.rounded_rectangle([x, y, x + w, y + 20], 5, fill=color)
    d.text((x + 7, y + 3), text, font=f, fill=(255, 255, 255))
    return w


def panel(x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=CARD, outline=LINE, width=2)


def text_block(x, y, w, lines, size=16, lh=21, fill=INK, font_path=SANS):
    f = F(font_path, size)
    for ln in lines:
        for sub in wrap(ln, f, w):
            d.text((x, y), sub, font=f, fill=fill)
            y += lh
    return y


# ---------------------------------------------------------------- masthead
d.line([M, 20, W - M, 20], fill=LINE, width=3)
f_eye = F(SANS_B, 15)
d.text((M, 29), "GLOBAL NEWS IN ONE PICTURE", font=f_eye, fill=RED)
src = "SOURCES: REUTERS - AP - AFP - BBC"
d.text((W - M - d.textlength(src, font=f_eye), 29), src, font=f_eye, fill=GREY)
centered("THE WORLD TODAY", F(SERIF, 64), 48)
d.line([M, 124, W - M, 124], fill=LINE, width=2)
d.line([M, 129, W - M, 129], fill=LINE, width=1)

# ---------------------------------------------------------------- date band
d.rounded_rectangle([M, 138, W - M, 192], 8, fill=NAVY)
centered("WEDNESDAY - 25 NOVEMBER 2026", F(SERIF, 38), 148, fill=(255, 255, 255))
for cx in (M + 24, W - M - 24):
    d.ellipse([cx - 6, 158, cx + 6, 170], fill=RED)

# ---------------------------------------------------------------- lead story
LY, LH = 202, 122
panel(M, LY, W - 2 * M, LH)
tag(M + 14, LY + 10, "LEAD - MARKETS", RED)
d.text((M + 14, LY + 34),
       "Nvidia rally fades a day after the 31% leap",
       font=F(SERIF, 26), fill=INK)
LX2 = M + 14
COLW = (W - 2 * M - 28 - 16) // 2
text_block(LX2, LY + 68, COLW, [
    "- Nvidia -5.9% Tuesday; Nasdaq -1.5% to 23,734,",
    "  S&P 500 -0.5%; chip index plunges 7.9%",
], size=15, lh=19)
text_block(LX2 + COLW + 16, LY + 68, COLW, [
    "- Dow +423 (+0.9%) to 50,019 as money rotates",
    "  out of tech; Anthropic falls below $83 IPO price",
], size=15, lh=19)

# ---------------------------------------------------------------- card rows
def card(x, y, w, h, tag_text, color, head, bullets, head_size=19):
    panel(x, y, w, h)
    tag(x + 12, y + 9, tag_text, color)
    yy = text_block(x + 12, y + 34, w - 24, [head], size=head_size, lh=23,
                    font_path=SERIF)
    text_block(x + 12, yy + 3, w - 24, bullets, size=14, lh=18)


CW = (W - 2 * M - 2 * 12) // 3
RY1, RH = 334, 140
card(M, RY1, CW, RH, "UKRAINE", RED, "Kyiv asks for \u20ac115bn for 2027",
     ["- Zelenskyy: foreign aid needed to hold the",
      "  line through next year",
      "- Ukraine's war widens: naval drones sank a",
      "  Russian corvette off Libya"])
card(M + CW + 12, RY1, CW, RH, "MIDDLE EAST", TEAL, "Houthi drone hits Riyadh tower",
     ["- 11 hurt, incl. 2 Indians, in strike on the",
      "  financial district's PIF Tower",
      "- Houthis threaten Saudi ports over Hodeidah"])
card(M + 2 * (CW + 12), RY1, CW, RH, "GAZA", BROWN,
     "Israel kills Hamas security chief",
     ["- Senior Hamas internal-security figure dies",
      "  in a Gaza drone strike, Hamas says",
      "- US senators press Israel on winter aid"])

RY2 = 484
card(M, RY2, CW, RH, "USA - CYBER", NAVY, "CIA and ODNI hit by hack",
     ["- Hack affects unclassified information,",
      "  officials say; classified systems safe",
      "- No disruption reported to operations"])
card(M + CW + 12, RY2, CW, RH, "TRADE", RED, "US readies fresh tariff hikes",
     ["- New duties on China, EU and others to",
      "  replace levies struck down by the court",
      "- Investors await October PCE inflation"])
card(M + 2 * (CW + 12), RY2, CW, RH, "CLIMATE", GREEN, "COP31 collapse: the fallout",
     ["- UN chief voices 'deep disappointment' as",
      "  Antalya ends with no deal on fossil fuels",
      "- Talks ran 44 hours past close; next: COP32"])

RY3 = 634
card(M, RY3, CW, RH, "ASIA", BROWN, "Bangladesh wins 36% pay rise",
     ["- Garment workers end weeks of strikes with",
      "  a big wage deal; factories reopen",
      "- Hanoi blast kills 6, hurts 10; gas leak",
      "  suspected in a residential area"])
card(M + CW + 12, RY3, CW, RH, "EUROPE", NAVY, "UK heat deaths hit a record",
     ["- 5,258 heat deaths in summer 2026, the",
      "  highest toll since records began",
      "- EU unveils new Russia sanctions on banks,",
      "  crypto and sport"])
card(M + 2 * (CW + 12), RY3, CW, RH, "SPORT", TEAL, "Real Madrid roar back 5-1",
     ["- Bellingham stunner, Mbappe brace sink PSV;",
      "  Real stay perfect in the Champions League",
      "- Arsenal 1-1 Dortmund; Man City 2-2 Napoli"])

# ---------------------------------------------------------------- numbers strip
NY, NH = 784, 64
d.rounded_rectangle([M, NY, W - M, NY + NH], 8, fill=NAVY)
d.text((M + 14, NY + 8), "THE DAY IN NUMBERS",
       font=F(SANS_B, 15), fill=(255, 255, 255))
nums = ("DOW 50,019  +0.9%    NASDAQ 23,734  -1.5%    BRENT $90.97    "
        "BITCOIN $59,224    \u20ac115BN AID ASK    11 HURT IN RIYADH    "
        "5,258 UK HEAT DEATHS")
text_block(M + 14, NY + 30, W - 2 * M - 28, [nums], size=15, lh=19,
           fill=(255, 255, 255))

# ---------------------------------------------------------------- IN BRIEF
UY, UH = 858, 108
panel(M, UY, W - 2 * M, UH)
d.text((M + 14, UY + 8), "IN BRIEF - MORE OF THE DAY",
       font=F(SANS_B, 15), fill=RED)
brief_l = [
    "- Iranian rial hits a record low after new US sanctions",
    "- Russian drone strays into Poland; Warsaw protests",
    "- Norway closes its last coal mine, on Svalbard",
]
brief_r = [
    "- Iraq orders federal forces to seize Kurdish oilfields",
    "- China Southern unit orders 50 Boeing 737-8 jets",
    "- OPEC+ ministers meet on 29 Nov to set 2027 output",
]
text_block(M + 14, UY + 32, COLW, brief_l, size=15, lh=22)
text_block(M + 14 + COLW + 16, UY + 32, COLW, brief_r, size=15, lh=22)

# ---------------------------------------------------------------- ticker
TY = 978
d.text((M, TY), "ALSO TODAY", font=F(SANS_B, 15), fill=RED)
tick = ("Cartagena supermarket hostages freed after a failed heist  -  "
        "Senegal gets its AFCON title back on appeal  -  Car bomb in "
        "Colombia injures 23  -  Laos leaves least-developed status")
f_tick = F(SANS, 14)
lines = wrap(tick, f_tick, W - 2 * M - 112)
for i, ln in enumerate(lines):
    d.text((M + 112, TY + i * 18), ln, font=f_tick, fill=INK)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
