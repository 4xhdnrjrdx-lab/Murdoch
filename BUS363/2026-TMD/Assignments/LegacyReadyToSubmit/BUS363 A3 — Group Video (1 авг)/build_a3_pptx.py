#!/usr/bin/env python3
"""Сборка колоды BUS363 A3 «From Bean to Bar» (13 слайдов, 16:9).

Источник содержания — BUS363_A3_Slides_Plan.md (тот же порядок и тот же текст).
Всё построено НАТИВНЫМИ фигурами python-pptx, без картинок-растров: команда сможет
подвинуть любой блок прямо в PowerPoint, ничего не пересобирая кодом.

Правила оформления взяты из плана (они из брифа, не вкусовые): одна мысль на слайд,
максимум 6 строк, кегль от 24pt, палитра шоколада, футер в левом нижнем углу.
Скрипт лежит рядом с колодой намеренно: генератор сдаваемого артефакта не должен
жить во временной папке (урок 21.07).
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUT = "/Users/king1/Documents/Murdoch/К сдаче/BUS363 A3 — Group Video (1 авг)/BUS363_A3_Slides_Team1.pptx"

# ── палитра: тёмный шоколад / крем / медный акцент ──────────────────────────
BG      = RGBColor(0x2B, 0x1D, 0x14)   # тёмный шоколад — фон
CREAM   = RGBColor(0xF2, 0xE6, 0xD5)   # основной текст
COPPER  = RGBColor(0xC8, 0x86, 0x2B)   # акцент: заголовки, подсветка
MUTED   = RGBColor(0x9C, 0x8A, 0x78)   # второстепенное, футер
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
DIM     = RGBColor(0x4A, 0x35, 0x26)   # заливка блоков
FONT    = "Arial"

W, H = Inches(13.333), Inches(7.5)
prs = Presentation()
prs.slide_width, prs.slide_height = W, H
BLANK = prs.slide_layouts[6]


def slide(title=None, sub=None):
    s = prs.slides.add_slide(BLANK)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    bg.fill.solid(); bg.fill.fore_color.rgb = BG; bg.line.fill.background()
    bg.shadow.inherit = False
    if title:
        tb = s.shapes.add_textbox(Inches(0.7), Inches(0.45), Inches(12), Inches(0.9))
        p = tb.text_frame.paragraphs[0]; p.text = title
        p.font.size, p.font.bold, p.font.name = Pt(34), True, FONT
        p.font.color.rgb = COPPER
        if sub:
            p2 = tb.text_frame.add_paragraph(); p2.text = sub
            p2.font.size, p2.font.name = Pt(15), FONT
            p2.font.color.rgb = MUTED
        ln_y = 1.62 if sub else 1.45          # подзаголовок занимает вторую строку, линия уходит ниже
        ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(ln_y), Inches(2.2), Pt(3))
        ln.fill.solid(); ln.fill.fore_color.rgb = COPPER; ln.line.fill.background()
        ln.shadow.inherit = False
    ft = s.shapes.add_textbox(Inches(0.7), Inches(6.95), Inches(6), Inches(0.35))
    fp = ft.text_frame.paragraphs[0]; fp.text = "BUS363 · Team 1 · Scaling Your Venture"
    fp.font.size, fp.font.name = Pt(10), FONT; fp.font.color.rgb = MUTED
    return s


def text(s, txt, x, y, w, h, size=24, color=CREAM, bold=False, align=PP_ALIGN.LEFT,
         space=10, italic=False):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    for i, line in enumerate(txt.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size, p.font.name, p.font.bold, p.font.italic = Pt(size), FONT, bold, italic
        p.font.color.rgb = color; p.alignment = align
        p.space_after = Pt(space)
    return tb


def rows(s, data, x, y, w1, w2, size=22, gap=0.62, c1=CREAM, c2=MUTED, bold1=False):
    """Двухколоночные строки: слева ярлык, справа значение. Выравнивание держат
    два текстбокса, а не пробелы, иначе на другом шрифте всё разъедется."""
    for i, (a, b) in enumerate(data):
        yy = y + i * gap
        text(s, a, x, yy, w1, gap, size=size, color=c1, bold=bold1, space=0)
        if b:
            text(s, b, x + w1, yy, w2, gap, size=size, color=c2, space=0)


def chip(s, txt, x, y, w, h, fill=DIM, color=CREAM, size=20, bold=False):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill; sh.line.fill.background()
    sh.shadow.inherit = False
    tf = sh.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.text = txt; p.alignment = PP_ALIGN.CENTER
    p.font.size, p.font.name, p.font.bold = Pt(size), FONT, bold
    p.font.color.rgb = color
    return sh


# ── 1 · титул ───────────────────────────────────────────────────────────────
s = slide()
text(s, "FROM BEAN TO BAR", 0.9, 2.35, 11.5, 1.1, size=54, color=COPPER, bold=True)
text(s, "Scaling a Perth craft chocolate brand into the UAE", 0.9, 3.45, 11.5, 0.6, size=26)
ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.95), Inches(4.35), Inches(3.4), Pt(3))
ln.fill.solid(); ln.fill.fore_color.rgb = COPPER; ln.line.fill.background(); ln.shadow.inherit = False
text(s, "BUS363 Assessment 3 · Team 1", 0.9, 4.65, 11.5, 0.4, size=18, color=MUTED)
text(s, "Faiaz Dzhafarov (35553299) · Uliana Komarova · Artem Baranov",
     0.9, 5.05, 11.5, 0.4, size=18, color=MUTED)

# ── 2 · где бизнес сейчас ───────────────────────────────────────────────────
s = slide("TODAY: ONE POSTCODE")
rows(s, [("120 bars / day", "A$18.7k / month revenue"),
         ("1 workshop, Perth", "A$6–10k / month running cost")],
     0.9, 2.2, 4.6, 6.5, size=26, gap=0.85, c1=CREAM, c2=COPPER, bold1=True)
text(s, "Proven recipe. No reach.", 0.9, 4.35, 11, 0.7, size=30, color=COPPER, bold=True)

# ── 3 · growth ≠ scale ──────────────────────────────────────────────────────
s = slide("GROWTH ≠ SCALE")
text(s, "“A business model's ability to increase revenues\nfaster than the corresponding cost base”",
     0.9, 2.0, 11, 1.4, size=26, italic=True)
text(s, "Hallowell (2001)", 0.9, 3.25, 11, 0.4, size=17, color=MUTED)
chip(s, "Second workshop\ncosts rise with sales", 0.9, 4.05, 5.4, 1.5, size=21)
chip(s, "Brand + recipe + storefront\nthey don't", 6.9, 4.05, 5.4, 1.5, fill=COPPER, color=BG,
     size=21, bold=True)

# ── 4 · пять рычагов Stampfl ────────────────────────────────────────────────
s = slide("FIVE DESIGN LEVERS", "Stampfl et al. (2013)")
rows(s, [("Technology", "←  our weakest link"),
         ("Cost & revenue structure", ""),
         ("Adaptability to legal regimes", "←  decides everything"),
         ("Network effects", "←  thin for a physical product"),
         ("User orientation", "←  where we compete")],
     0.9, 2.05, 5.9, 5.4, size=23, gap=0.66, c2=COPPER)
text(s, "→  Scalability  →  Growth + investor attractiveness",
     0.9, 5.65, 11.5, 0.6, size=22, color=COPPER, bold=True)

# ── 5 · выбор рынка ─────────────────────────────────────────────────────────
s = slide("WHY THE UAE")
rows(s, [("Japan", "best palate, most crowded shelf, slowest cycle"),
         ("Singapore", "easy to enter, small")],
     0.9, 2.05, 2.6, 9.0, size=22, gap=0.6, c2=CREAM)
box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.75), Inches(3.3),
                         Inches(11.8), Inches(1.95))
box.fill.solid(); box.fill.fore_color.rgb = DIM; box.line.color.rgb = COPPER
box.line.width = Pt(2); box.shadow.inherit = False
text(s, "UAE", 1.05, 3.5, 2.4, 0.6, size=26, color=COPPER, bold=True)
text(s, "gifting economy · premium import shelf already exists\n"
        "Ramadan + Eid = two forecastable peaks\n"
        "Australian origin is an asset here",
     3.4, 3.5, 9.0, 1.9, size=22, space=6)

# ── 6 · айсберг Шейна ───────────────────────────────────────────────────────
s = slide("THE PERTH BAR IS NOT THE PRODUCT")
tip = s.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(4.6), Inches(2.05),
                         Inches(4.2), Inches(1.5))
tip.fill.solid(); tip.fill.fore_color.rgb = COPPER; tip.line.fill.background(); tip.shadow.inherit = False
water = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(3.6), Inches(11), Pt(2))
water.fill.solid(); water.fill.fore_color.rgb = CREAM; water.line.fill.background(); water.shadow.inherit = False
body = s.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(3.1), Inches(3.62),
                          Inches(7.2), Inches(2.7))
body.rotation = 180
body.fill.solid(); body.fill.fore_color.rgb = DIM; body.line.fill.background(); body.shadow.inherit = False
text(s, "packaging, advertising", 9.0, 2.45, 3.6, 0.5, size=19, color=COPPER)
text(s, "what you see", 9.0, 2.85, 3.6, 0.4, size=14, color=MUTED)
text(s, "values and norms", 1.0, 4.15, 3.4, 0.5, size=19)
text(s, "underlying assumptions", 1.0, 5.0, 3.6, 0.5, size=19)
text(s, "Schein (1985)", 10.2, 5.45, 2.4, 0.4, size=15, color=MUTED)

# ── 7 · культурное чтение рынка ─────────────────────────────────────────────
s = slide("READING THE MARKET")
rows(s, [("Hall", "high-context · polychronic"),
         ("", "packaging whispers, not shouts"),
         ("", "a six-week conversation is not a “no”"),
         ("Hofstede", "high power distance"),
         ("", "the gift box leads, not the single bar"),
         ("Trompenaars", "particularist"),
         ("", "contracts follow relationships"),
         ("", "two buying trips before one advert")],
     0.9, 1.95, 3.0, 8.6, size=20, gap=0.58, c1=COPPER, c2=CREAM, bold1=True)

# ── 8 · редизайн продукта (ключевой слайд рубрики) ──────────────────────────
s = slide("FIVE CHANGES TO THE PRODUCT")
data = [("1  Formulation", "heat-stable temper, 65% dark summer range"),
        ("2  Compliance", "halal certification · Arabic + English label"),
        ("3  Flavour", "date & sea salt · pistachio & tahini · camel milk"),
        ("4  Format", "6-bar gift box, A$55"),
        ("5  Calendar", "Ramadan & Eid editions, planned 6 months out")]
rows(s, data, 0.9, 2.0, 3.3, 8.3, size=22, gap=0.72, c1=COPPER, c2=CREAM, bold1=True)
hero = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.55), Inches(4.05),
                          Inches(2.9), Inches(0.62))
hero.fill.solid(); hero.fill.fore_color.rgb = COPPER; hero.line.fill.background(); hero.shadow.inherit = False
hp = hero.text_frame.paragraphs[0]; hp.text = "hero SKU"; hp.alignment = PP_ALIGN.CENTER
hp.font.size, hp.font.bold, hp.font.name = Pt(19), True, FONT; hp.font.color.rgb = BG

# ── 9 · позиционирование и канал ────────────────────────────────────────────
s = slide("POSITIONING")
rows(s, [("Perth", "craft"),
         ("UAE", "a considered gift with a traceable story")],
     0.9, 1.95, 2.0, 9.6, size=24, gap=0.62, c1=COPPER, c2=CREAM, bold1=True)
text(s, "CHANNEL, IN ORDER", 0.9, 3.35, 6.0, 0.5, size=20, color=MUTED, bold=True)
for i, (n, t) in enumerate([("1", "cross-border D2C, bilingual store, temp-controlled courier"),
                            ("2", "one UAE distributor for hotels & corporate gifting"),
                            ("3", "retail shelf")]):
    chip(s, n, 0.9, 3.95 + i * 0.72, 0.55, 0.55, size=18, bold=True)
    text(s, t, 1.65, 4.02 + i * 0.72, 10.4, 0.55, size=21, space=0)
text(s, "Sell online → learn → sign.", 0.9, 6.05, 11, 0.6, size=24, color=COPPER, bold=True)

# ── 10 · партнёры ───────────────────────────────────────────────────────────
s = slide("CHOOSING A PARTNER", "shared market & buyer persona · complementary identity · "
                                "similar goals · and not a competitor")
hdr = [("", "market"), ("", "identity"), ("", "goals")]
for i, (a, b) in enumerate([("Specialty coffee roaster", "✓   ✓   ✓"),
                            ("Five-star hotel group", "✓   –   ✓"),
                            ("Supermarket private label", "✓   ✗   ✓")]):
    y = 2.25 + i * 0.85
    text(s, a, 0.9, y, 6.0, 0.7, size=23, space=0)
    text(s, b, 7.0, y, 2.6, 0.7, size=23, color=COPPER, bold=True, space=0)
text(s, "makes our story invisible", 9.6, 4.02, 3.2, 0.5, size=17, color=MUTED, space=0)
text(s, "First two deals:  co-branded box  ·  hotel amenity placement",
     0.9, 5.55, 11.5, 0.6, size=22, color=COPPER, bold=True)

# ── 11 · деньги ─────────────────────────────────────────────────────────────
s = slide("A$250,000 OVER 18 MONTHS")
# Две колонки рядом, а не друг под другом: в один столбец нижняя строка налезала на футер,
# а длинные подписи переносились и ломали сетку (поймано на рендере первой сборки).
text(s, "WHERE IT GOES", 0.9, 1.95, 5.0, 0.45, size=17, color=MUTED, bold=True)
rows(s, [("90k", "tempering line + cold packing"),
         ("70k", "certification, labelling, container"),
         ("50k", "brand & digital"),
         ("40k", "runway")],
     0.9, 2.55, 1.2, 4.6, size=21, gap=0.75, c1=COPPER, c2=CREAM, bold1=True)
text(s, "WHERE IT COMES FROM", 7.0, 1.95, 5.4, 0.45, size=17, color=MUTED, bold=True)
rows(s, [("40k", "bootstrap"),
         ("60k", "Kickstarter, all-or-nothing"),
         ("100k", "angel (~12%)"),
         ("50k", "co-marketing + export grant")],
     7.0, 2.55, 1.2, 4.4, size=21, gap=0.75, c1=COPPER, c2=CREAM, bold1=True)
chip(s, "across the valley of death, still holding the company",
     0.9, 5.75, 11.5, 0.8, fill=DIM, size=21)

# ── 12 · три гейта ──────────────────────────────────────────────────────────
s = slide("THREE GATES", "no gate opens until the numbers clear")
for i, (g, m, t) in enumerate([
        ("Gate 1", "months 1–6", "certification · bilingual store · 100 online orders"),
        ("Gate 2", "months 7–12", "1 distributor · 25 stockists · 2nd tempering line"),
        ("Gate 3", "months 13–18", "UAE line profitable · ready for Saudi")]):
    y = 2.15 + i * 0.95
    chip(s, g, 0.9, y, 1.6, 0.68, fill=COPPER, color=BG, size=19, bold=True)
    text(s, m, 2.7, y + 0.08, 2.0, 0.5, size=19, color=MUTED, space=0)
    text(s, t, 4.7, y + 0.08, 8.0, 0.5, size=20, space=0)
text(s, "PMBOK 7: tailor the process, judge by value delivered", 0.9, 5.35, 11.5, 0.5, size=20,
     color=CREAM)
text(s, "Top risk: cocoa price → two suppliers, forward-buy one season",
     0.9, 5.9, 11.5, 0.5, size=20, color=COPPER)

# ── 13 · финал ──────────────────────────────────────────────────────────────
s = slide("WHAT WE WON'T DROP")
rows(s, [("Leadership", "strataplex: one workshop ≠ two countries"),
         ("", "add the business & strategic layer at Gate 2"),
         ("Hubris", "Theranos: nobody could say no"),
         ("", "monthly review, outside mentor can stop a gate"),
         ("Ethics", "fair-trade sourcing · recyclable packaging"),
         ("", "same beans, same farmers, bigger order")],
     0.9, 1.95, 2.9, 8.8, size=21, gap=0.6, c1=COPPER, c2=CREAM, bold1=True)
text(s, "One workshop in Perth. One country at a time.",
     0.9, 5.85, 11.5, 0.7, size=28, color=COPPER, bold=True)

prs.save(OUT)
print(f"сохранено: {OUT}")
print(f"слайдов: {len(prs.slides.__iter__.__self__._sldIdLst)}")
