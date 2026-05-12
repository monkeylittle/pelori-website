"""Render the Play Console feature graphic (1024 × 500).

Composes the lime equalizer mark + the "pelori" wordmark + a one-line
tagline on the brand Electric Blue. Output:

    pelori_website/marketing/feature_graphic.png

Run: `python3 marketing/feature_graphic.py`. No CLI args. Re-run any
time the source artwork or wordmark conventions change; the output
PNG is what gets uploaded to Play Console → Main store listing →
Feature graphic.

Reuses composer.py's font and colour conventions but is intentionally
self-contained — single output, no incremental compositing pipeline,
not worth importing across files.
"""

import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONT_DIR = ROOT / 'fonts'
ICON_FG = ROOT.parent.parent / 'pelori_app' / 'assets' / 'icon_foreground.png'
OUT = ROOT / 'feature_graphic.png'

# Brand tokens — mirror composer.py + the in-app design system.
ELECTRIC_BLUE = (0x00, 0x66, 0xFF)
HIVIS_LIME = (0xD4, 0xFF, 0x3A)
WHITE = (0xFF, 0xFF, 0xFF)

# Play Console feature graphic spec.
CANVAS_W = 1024
CANVAS_H = 500

FONT_URLS = {
    'BricolageGrotesque.ttf': (
        'https://raw.githubusercontent.com/google/fonts/main/'
        'ofl/bricolagegrotesque/'
        'BricolageGrotesque%5Bopsz%2Cwdth%2Cwght%5D.ttf'
    ),
    'DMSans.ttf': (
        'https://raw.githubusercontent.com/google/fonts/main/'
        'ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf'
    ),
}


def ensure_font(name: str) -> Path:
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    path = FONT_DIR / name
    if path.exists() and path.stat().st_size > 0:
        return path
    url = FONT_URLS[name]
    print(f'  downloading {name}')
    urllib.request.urlretrieve(url, path)
    return path


def load_wordmark_font(size: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(str(ensure_font('BricolageGrotesque.ttf')), size)
    try:
        font.set_variation_by_name(b'96pt ExtraBold')
    except Exception:
        try:
            font.set_variation_by_name(b'ExtraBold')
        except Exception:
            pass
    return font


def load_tagline_font(size: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(str(ensure_font('DMSans.ttf')), size)
    try:
        font.set_variation_by_name(b'Medium')
    except Exception:
        pass
    return font


def render():
    canvas = Image.new('RGB', (CANVAS_W, CANVAS_H), ELECTRIC_BLUE)
    draw = ImageDraw.Draw(canvas)

    # Mark on the left. icon_foreground is the lime equalizer alone
    # (no blue background) — paste it directly so the brand colour
    # bleeds underneath.
    if not ICON_FG.exists():
        raise SystemExit(f'icon_foreground.png not found at {ICON_FG}')
    mark = Image.open(ICON_FG).convert('RGBA')
    target_h = 280
    aspect = mark.width / mark.height
    target_w = int(target_h * aspect)
    mark = mark.resize((target_w, target_h), Image.LANCZOS)
    mark_x = 90
    mark_y = (CANVAS_H - target_h) // 2
    canvas.paste(mark, (mark_x, mark_y), mark)

    # Wordmark + tagline on the right.
    text_x = mark_x + target_w + 60
    wordmark_font = load_wordmark_font(170)
    tagline_font = load_tagline_font(38)

    # Vertical centre the two lines as a block. Use textbbox for
    # accurate sizing; PIL's metrics are otherwise font-internal and
    # leave inconsistent leading.
    wordmark_text = 'pelori'
    tagline_text = 'Group cycling, planned together.'
    wm_box = draw.textbbox((0, 0), wordmark_text, font=wordmark_font)
    tg_box = draw.textbbox((0, 0), tagline_text, font=tagline_font)
    wm_h = wm_box[3] - wm_box[1]
    tg_h = tg_box[3] - tg_box[1]
    line_gap = 18
    block_h = wm_h + line_gap + tg_h
    block_top = (CANVAS_H - block_h) // 2

    # Bricolage's optical baseline sits below the bbox top — subtract
    # the bbox y-offset so the visual top of the glyphs aligns with
    # block_top rather than the bbox-reported top edge.
    draw.text(
        (text_x, block_top - wm_box[1]),
        wordmark_text,
        font=wordmark_font,
        fill=WHITE,
    )
    draw.text(
        (text_x, block_top + wm_h + line_gap - tg_box[1]),
        tagline_text,
        font=tagline_font,
        fill=WHITE,
    )

    canvas.save(OUT, 'PNG', optimize=True)
    print(f'  wrote {OUT.relative_to(ROOT.parent)} ({CANVAS_W}×{CANVAS_H})')


if __name__ == '__main__':
    render()
