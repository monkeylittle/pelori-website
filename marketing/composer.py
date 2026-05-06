"""Compose App Store marketing screenshots, per locale.

Reads raw simulator captures from
`marketing/screenshots/raw/6.9-inch/<lang>/`, mats each on a
1290×2796 brand-coloured canvas with a translated caption (one accent
word in hi-vis lime), and writes the result to
`marketing/screenshots/composed-6.9/<lang>/`.

Run from anywhere:

    python3 marketing/composer.py            # composes every locale
                                             # whose raw/ dir has files
    python3 marketing/composer.py fr         # just that one locale

Fonts auto-download into `marketing/fonts/` on first run (gitignored —
~250KB of TTFs we don't want bloating the repo). Subsequent runs reuse
the cache.

Edit the `CAPTIONS_BY_LOCALE` dict below to change captions / accent
words / order. Each locale should carry the same number of panels in
the same order so the composed sets stay parallel.
"""
from __future__ import annotations

import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:
    sys.exit('Missing dependency: pip install --user Pillow')


# ─── Paths ────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent
RAW_BASE = ROOT / 'screenshots' / 'raw' / '6.9-inch'
OUT_BASE = ROOT / 'screenshots' / 'composed-6.9'
FONT_DIR = ROOT / 'fonts'


# ─── Brand tokens (mirror lib/main.dart's theme) ──────────────────────

ELECTRIC_BLUE = (0x00, 0x66, 0xFF)
NEAR_BLACK = (0x0E, 0x0E, 0x0C)
HIVIS_LIME = (0xD4, 0xFF, 0x3A)
WHITE = (0xFF, 0xFF, 0xFF)
WHITE_DIM = (0xFF, 0xFF, 0xFF, 0xCC)

# 6.9" canvas — Apple requires this for new submissions.
CANVAS_W, CANVAS_H = 1290, 2796


# ─── Per-panel content ────────────────────────────────────────────────

@dataclass
class Panel:
    src: str
    out: str
    background: tuple[int, int, int]
    # Two lines max — Bricolage 800 at the size we use eats the canvas.
    headline_lines: list[str]
    # Single substring of the headline to render in hi-vis lime. Pass
    # None to keep everything white. Match is case-sensitive and only
    # the first occurrence is coloured.
    accent_word: str | None
    subhead: str | None


# Per-locale caption sets. Source filenames stay the same across
# languages — the raw simulator capture for panel 02 in French lives
# at raw/6.9-inch/fr/02-my-rides.png, etc.
CAPTIONS_BY_LOCALE: dict[str, list[Panel]] = {
    'en': [
        Panel(
            src='01-onboarding-hero.png', out='01-onboarding-hero.png',
            background=ELECTRIC_BLUE,
            headline_lines=['Ride together.', "We've got the rest."],
            accent_word='together', subhead=None,
        ),
        Panel(
            src='02-my-rides.png', out='02-my-rides.png',
            background=NEAR_BLACK,
            headline_lines=['One place', 'for every ride.'],
            accent_word='every', subhead='Plan, RSVP, chat — all sorted.',
        ),
        Panel(
            src='03-chat.png', out='03-chat.png',
            background=NEAR_BLACK,
            headline_lines=['One thread', 'per ride.'],
            accent_word='thread', subhead='Beats five overlapping group chats.',
        ),
        Panel(
            src='04-going-list.png', out='04-going-list.png',
            background=NEAR_BLACK,
            headline_lines=["Know who's", 'actually riding.'],
            accent_word='actually', subhead='Tap the count to see who said yes.',
        ),
        Panel(
            src='05-discover.png', out='05-discover.png',
            background=NEAR_BLACK,
            headline_lines=['Find rides', 'nearby.'],
            accent_word='nearby',
            subhead='Cycling clubs, shop rides, weekend rollouts.',
        ),
        Panel(
            src='06-where-tab.png', out='06-where-tab.png',
            background=NEAR_BLACK,
            headline_lines=['Meeting points,', 'made obvious.'],
            accent_word='obvious',
            subhead='One pin, on the map, for the whole crew.',
        ),
        Panel(
            src='07-public-preview.png', out='07-public-preview.png',
            background=NEAR_BLACK,
            headline_lines=['Browse first.', "Join when you're sure."],
            accent_word='Browse',
            subhead='See the schedule, route, and crew before you commit.',
        ),
    ],
    'nl': [
        Panel(
            src='01-onboarding-hero.png', out='01-onboarding-hero.png',
            background=ELECTRIC_BLUE,
            headline_lines=['Rijd samen.', 'De rest doen wij.'],
            accent_word='samen', subhead=None,
        ),
        Panel(
            src='02-my-rides.png', out='02-my-rides.png',
            background=NEAR_BLACK,
            headline_lines=['Eén plek', 'voor elke rit.'],
            accent_word='elke', subhead='Plan, RSVP, chat — alles op orde.',
        ),
        Panel(
            src='03-chat.png', out='03-chat.png',
            background=NEAR_BLACK,
            headline_lines=['Eén gesprek', 'per rit.'],
            accent_word='gesprek',
            subhead='Beter dan vijf overlappende appgroepen.',
        ),
        Panel(
            src='04-going-list.png', out='04-going-list.png',
            background=NEAR_BLACK,
            headline_lines=['Weet wie', 'écht meerijdt.'],
            accent_word='écht',
            subhead='Tik op het aantal om te zien wie ja zei.',
        ),
        Panel(
            src='05-discover.png', out='05-discover.png',
            background=NEAR_BLACK,
            headline_lines=['Vind ritten', 'in de buurt.'],
            accent_word='in de buurt',
            subhead='Wielerclubs, fietswinkels, weekendritten.',
        ),
        Panel(
            src='06-where-tab.png', out='06-where-tab.png',
            background=NEAR_BLACK,
            headline_lines=['Verzamelpunten,', 'glashelder.'],
            accent_word='glashelder',
            subhead='Eén pin, op de kaart, voor de hele crew.',
        ),
        Panel(
            src='07-public-preview.png', out='07-public-preview.png',
            background=NEAR_BLACK,
            headline_lines=['Eerst kijken.', 'Daarna meedoen.'],
            accent_word='Eerst',
            subhead='Bekijk schema, route en crew voor je je aanmeldt.',
        ),
    ],
    'fr': [
        Panel(
            src='01-onboarding-hero.png', out='01-onboarding-hero.png',
            background=ELECTRIC_BLUE,
            headline_lines=['Roule ensemble.', "On s'occupe du reste."],
            accent_word='ensemble', subhead=None,
        ),
        Panel(
            src='02-my-rides.png', out='02-my-rides.png',
            background=NEAR_BLACK,
            headline_lines=['Un seul endroit', 'pour chaque sortie.'],
            accent_word='chaque',
            subhead='Planifier, RSVP, discuter — tout est rangé.',
        ),
        Panel(
            src='03-chat.png', out='03-chat.png',
            background=NEAR_BLACK,
            headline_lines=['Un seul fil', 'par sortie.'],
            accent_word='fil',
            subhead='Mieux que cinq groupes WhatsApp qui se chevauchent.',
        ),
        Panel(
            src='04-going-list.png', out='04-going-list.png',
            background=NEAR_BLACK,
            headline_lines=['Sache qui', 'roule vraiment.'],
            accent_word='vraiment',
            subhead='Tape le compteur pour voir qui a dit oui.',
        ),
        Panel(
            src='05-discover.png', out='05-discover.png',
            background=NEAR_BLACK,
            headline_lines=['Trouve des sorties', 'à côté.'],
            accent_word='à côté',
            subhead='Clubs cyclistes, magasins de vélo, sorties du week-end.',
        ),
        Panel(
            src='06-where-tab.png', out='06-where-tab.png',
            background=NEAR_BLACK,
            headline_lines=['Points de rendez-vous,', 'évidents.'],
            accent_word='évidents',
            subhead='Un seul point, sur la carte, pour toute la team.',
        ),
        Panel(
            src='07-public-preview.png', out='07-public-preview.png',
            background=NEAR_BLACK,
            headline_lines=["Regarde d'abord.", 'Rejoins quand tu es sûr.'],
            accent_word="d'abord",
            subhead="Vois le programme, le parcours et la team avant de t'engager.",
        ),
    ],
    'es': [
        Panel(
            src='01-onboarding-hero.png', out='01-onboarding-hero.png',
            background=ELECTRIC_BLUE,
            headline_lines=['Rueda con los tuyos.', 'Nosotros ponemos el resto.'],
            accent_word='los tuyos', subhead=None,
        ),
        Panel(
            src='02-my-rides.png', out='02-my-rides.png',
            background=NEAR_BLACK,
            headline_lines=['Un solo lugar', 'para cada ruta.'],
            accent_word='cada',
            subhead='Planifica, confirma, chatea — todo ordenado.',
        ),
        Panel(
            src='03-chat.png', out='03-chat.png',
            background=NEAR_BLACK,
            headline_lines=['Un hilo', 'por ruta.'],
            accent_word='hilo', subhead='Mejor que cinco grupos solapados.',
        ),
        Panel(
            src='04-going-list.png', out='04-going-list.png',
            background=NEAR_BLACK,
            headline_lines=['Sabe quién', 'rueda de verdad.'],
            accent_word='de verdad',
            subhead='Toca el contador para ver quién dijo que sí.',
        ),
        Panel(
            src='05-discover.png', out='05-discover.png',
            background=NEAR_BLACK,
            headline_lines=['Encuentra rutas', 'cerca.'],
            accent_word='cerca',
            subhead='Clubs ciclistas, tiendas de bici, salidas de fin de semana.',
        ),
        Panel(
            src='06-where-tab.png', out='06-where-tab.png',
            background=NEAR_BLACK,
            headline_lines=['Puntos de encuentro,', 'claros.'],
            accent_word='claros',
            subhead='Un solo pin, en el mapa, para todo el grupo.',
        ),
        Panel(
            src='07-public-preview.png', out='07-public-preview.png',
            background=NEAR_BLACK,
            headline_lines=['Mira primero.', 'Únete cuando lo tengas claro.'],
            accent_word='primero',
            subhead='Mira el horario, la ruta y el grupo antes de apuntarte.',
        ),
    ],
    'it': [
        Panel(
            src='01-onboarding-hero.png', out='01-onboarding-hero.png',
            background=ELECTRIC_BLUE,
            headline_lines=['Pedala insieme.', 'Al resto pensiamo noi.'],
            accent_word='insieme', subhead=None,
        ),
        Panel(
            src='02-my-rides.png', out='02-my-rides.png',
            background=NEAR_BLACK,
            headline_lines=['Un solo posto', 'per ogni uscita.'],
            accent_word='ogni',
            subhead='Pianifica, conferma, chatta — tutto in ordine.',
        ),
        Panel(
            src='03-chat.png', out='03-chat.png',
            background=NEAR_BLACK,
            headline_lines=['Un filo', 'per uscita.'],
            accent_word='filo', subhead='Meglio di cinque chat sovrapposte.',
        ),
        Panel(
            src='04-going-list.png', out='04-going-list.png',
            background=NEAR_BLACK,
            headline_lines=['Scopri chi', 'pedala davvero.'],
            accent_word='davvero',
            subhead='Tocca il contatore per vedere chi ha detto sì.',
        ),
        Panel(
            src='05-discover.png', out='05-discover.png',
            background=NEAR_BLACK,
            headline_lines=['Trova uscite', 'vicino a te.'],
            accent_word='vicino a te',
            subhead='Club ciclistici, negozi di bici, uscite del weekend.',
        ),
        Panel(
            src='06-where-tab.png', out='06-where-tab.png',
            background=NEAR_BLACK,
            headline_lines=['Punti di ritrovo,', 'chiari.'],
            accent_word='chiari',
            subhead='Un solo pin, sulla mappa, per tutta la squadra.',
        ),
        Panel(
            src='07-public-preview.png', out='07-public-preview.png',
            background=NEAR_BLACK,
            headline_lines=['Guarda prima.', 'Unisciti quando sei sicuro.'],
            accent_word='prima',
            subhead='Vedi orario, percorso e squadra prima di impegnarti.',
        ),
    ],
}


# ─── Fonts (variable axes from upstream Google Fonts) ─────────────────

# Variable fonts — Pillow 10+ supports these. We pick weights via
# set_variation_by_axes after load. URLs resolve through Google Fonts'
# raw GitHub mirror; both files are stable releases.
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


def load_headline_font(size: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(str(ensure_font('BricolageGrotesque.ttf')), size)
    # Named instance "96pt ExtraBold" pins opsz=96 + wght=800 + the
    # default width — mirrors the .h-display CSS in the design system.
    try:
        font.set_variation_by_name(b'96pt ExtraBold')
    except Exception:
        try:
            font.set_variation_by_name(b'ExtraBold')
        except Exception:
            pass
    return font


def load_subhead_font(size: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(str(ensure_font('DMSans.ttf')), size)
    try:
        font.set_variation_by_name(b'Medium')
    except Exception:
        pass
    return font


# ─── Layout constants ─────────────────────────────────────────────────

CAPTION_TOP_PAD = 200
HEADLINE_PT = 132
HEADLINE_LINE_GAP = 14
SUBHEAD_PT = 44
SUBHEAD_TOP_GAP = 36
DEVICE_TOP_GAP = 96
# Mounted device width — leaves a comfortable mat on the brand colour.
DEVICE_TARGET_W = 1000
DEVICE_CORNER_R = 60
SHADOW_BLUR = 28
SHADOW_OFFSET = 12
SHADOW_OPACITY = 90  # alpha 0-255


# ─── Drawing ──────────────────────────────────────────────────────────

def render_panel(
    panel: Panel,
    raw_dir: Path,
    headline_font: ImageFont.FreeTypeFont,
    subhead_font: ImageFont.FreeTypeFont,
) -> Image.Image:
    canvas = Image.new('RGB', (CANVAS_W, CANVAS_H), panel.background)
    draw = ImageDraw.Draw(canvas)

    cursor_y = CAPTION_TOP_PAD
    for line in panel.headline_lines:
        cursor_y = _draw_headline_line(
            draw, line, panel.accent_word, headline_font, cursor_y,
        )
        cursor_y += HEADLINE_LINE_GAP

    if panel.subhead:
        cursor_y += SUBHEAD_TOP_GAP - HEADLINE_LINE_GAP
        _draw_centered(draw, panel.subhead, subhead_font, cursor_y, WHITE_DIM)
        cursor_y += SUBHEAD_PT

    device_y = cursor_y + DEVICE_TOP_GAP
    _paste_device(canvas, raw_dir / panel.src, device_y)
    return canvas


def _draw_headline_line(
    draw: ImageDraw.ImageDraw,
    text: str,
    accent: str | None,
    font: ImageFont.FreeTypeFont,
    y: int,
) -> int:
    """Centre the headline line on the canvas. If `accent` exists in
    `text`, render it in HIVIS_LIME and the rest in WHITE; otherwise
    the whole line goes WHITE. Returns the y position of the next line.
    """
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    start_x = (CANVAS_W - text_w) // 2

    if accent and accent in text:
        idx = text.index(accent)
        before = text[:idx]
        after = text[idx + len(accent):]
        x = start_x
        for segment, colour in (
            (before, WHITE),
            (accent, HIVIS_LIME),
            (after, WHITE),
        ):
            if not segment:
                continue
            draw.text((x, y), segment, font=font, fill=colour)
            seg_bbox = draw.textbbox((0, 0), segment, font=font)
            x += seg_bbox[2] - seg_bbox[0]
    else:
        draw.text((start_x, y), text, font=font, fill=WHITE)

    return y + HEADLINE_PT


def _draw_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    y: int,
    colour: tuple,
) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (CANVAS_W - w) // 2
    if len(colour) == 4:
        colour = colour[:3]
    draw.text((x, y), text, font=font, fill=colour)


def _paste_device(canvas: Image.Image, src_path: Path, y: int) -> None:
    src = Image.open(src_path).convert('RGBA')
    sw, sh = src.size
    new_w = DEVICE_TARGET_W
    new_h = round(sh * (new_w / sw))
    src = src.resize((new_w, new_h), Image.LANCZOS)

    # Round-corner mask matches the iPhone screen radius proportionally.
    mask = Image.new('L', (new_w, new_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, new_w, new_h), DEVICE_CORNER_R, fill=255,
    )
    rounded = Image.new('RGBA', (new_w, new_h), (0, 0, 0, 0))
    rounded.paste(src, (0, 0), mask)

    # Drop shadow — a softer mask blurred behind the device.
    shadow_pad = SHADOW_BLUR * 2 + abs(SHADOW_OFFSET)
    shadow = Image.new(
        'RGBA',
        (new_w + shadow_pad * 2, new_h + shadow_pad * 2),
        (0, 0, 0, 0),
    )
    shadow_mask = Image.new('L', (new_w, new_h), 0)
    ImageDraw.Draw(shadow_mask).rounded_rectangle(
        (0, 0, new_w, new_h), DEVICE_CORNER_R, fill=SHADOW_OPACITY,
    )
    shadow_block = Image.new(
        'RGBA', (new_w, new_h), (0, 0, 0, SHADOW_OPACITY),
    )
    shadow.paste(
        shadow_block,
        (shadow_pad, shadow_pad + SHADOW_OFFSET),
        shadow_mask,
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(SHADOW_BLUR))

    x = (CANVAS_W - new_w) // 2
    canvas.paste(shadow, (x - shadow_pad, y - shadow_pad), shadow)
    canvas.paste(rounded, (x, y), rounded)


def compose_locale(
    locale: str,
    panels: list[Panel],
    headline_font: ImageFont.FreeTypeFont,
    subhead_font: ImageFont.FreeTypeFont,
) -> int:
    """Compose every panel for one locale. Returns the count of panels
    actually written; raw PNGs that haven't been captured yet are
    skipped with a notice so an incomplete locale doesn't abort the
    whole run."""
    raw_dir = RAW_BASE / locale
    out_dir = OUT_BASE / locale
    if not raw_dir.exists():
        print(f'  ! {locale}: no raw dir at {raw_dir.relative_to(ROOT.parent)}')
        return 0
    out_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    for panel in panels:
        src_path = raw_dir / panel.src
        if not src_path.exists():
            print(f'  · {locale}/{panel.src} (raw not captured yet — skipping)')
            continue
        img = render_panel(panel, raw_dir, headline_font, subhead_font)
        out_path = out_dir / panel.out
        img.save(out_path, 'PNG', optimize=True)
        print(f'  wrote {out_path.relative_to(ROOT.parent)}')
        written += 1
    return written


def main() -> None:
    requested = sys.argv[1:]
    if requested:
        unknown = [c for c in requested if c not in CAPTIONS_BY_LOCALE]
        if unknown:
            sys.exit(
                f'Unknown locale(s): {unknown}. '
                f'Known: {sorted(CAPTIONS_BY_LOCALE.keys())}'
            )
        locales = requested
    else:
        locales = sorted(CAPTIONS_BY_LOCALE.keys())

    headline_font = load_headline_font(HEADLINE_PT)
    subhead_font = load_subhead_font(SUBHEAD_PT)

    total = 0
    for locale in locales:
        panels = CAPTIONS_BY_LOCALE[locale]
        total += compose_locale(locale, panels, headline_font, subhead_font)
    print(f'\n  {total} panel(s) written across {len(locales)} locale(s).')


if __name__ == '__main__':
    main()
