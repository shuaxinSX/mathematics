#!/usr/bin/env python3
"""Build the compact badge family from exact, locally installed font outlines.

Requires fontTools, Cinzel Variable and Source Han Serif SC Bold.
The exported SVGs contain paths, not font files or runtime font dependencies.
"""

import argparse
from html import escape
from math import cos, degrees, radians, sin
from pathlib import Path
from shutil import copy2
from subprocess import run

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


ROOT = Path(__file__).resolve().parents[1]
FONT_CACHE = Path.home() / "Library/Caches/math_olympiad_certificate/fonts"
ENGLISH = "HIGH SCHOOL MATHEMATICAL OLYMPIAD · QIHANG ALLIANCE"
CHINESE = "高中数学奥林匹克启航联盟"
COLORS = {
    "Purple": "#2E1065",
    "Prototype": "#2E1065",
    "Crimson": "#9B2034",
    "Navy": "#0F172A",
    "Mono": "#111111",
}
OUTPUT_DIRS = [
    ROOT / "assets",
    ROOT / "qihang-alliance-logo/assets",
    ROOT / "qihang-alliance-logo/vector_exports",
]

# All rings and type share a true geometric centre. Glyph ink is centred at
# r=249.5 rather than aligning mismatched English / Chinese baselines.
CENTER = 300
TEXT_RADIUS = 249.5
OUTER_RADIUS = 286
OUTER_STROKE = 8
INNER_RADIUS = 216
INNER_STROKE = 2
DISC_RADIUS = 209
EN_SIZE, EN_TRACKING = 25, 1.4
CN_SIZE, CN_TRACKING = 35, 8

# Optical centring, plus another 2pt right at the page's 300px badge preview:
# 2pt × 96px/72pt × 600 viewBox units/300px = 5.33333 SVG units.
MOTIF_OFFSET_X = 8 + 2 * 96 / 72 * 600 / 300
MOTIF_OFFSET_Y = -10

# Original approved sail contours, scaled uniformly with the larger core disc.
SAIL = """    <path d="M 30 162 C 55 142 80 182 105 162 C 130 142 155 178 178 152 C 158 172 125 180 102 166 C 82 152 50 178 30 162 Z"/>
    <path d="M 108 153 C 119 133 133 97 147 78 C 140 106 131 134 125 152 C 119 153 113 153 108 153 Z"/>
    <path d="M 52 148 C 65 110 92 60 138 28 C 122 68 110 115 102 156 C 84 156 68 152 52 148 Z"/>
    <circle cx="138" cy="28" r="4.6"/>"""


def number(value):
    return f"{value:.5f}".rstrip("0").rstrip(".") or "0"


def arc_text(text, font_file, font_index, size, tracking, bottom=False, weight=None):
    font = TTFont(font_file, fontNumber=font_index)
    if weight is not None:
        font = instantiateVariableFont(font, {"wght": weight}, inplace=True)
        assert font["OS/2"].usWeightClass == weight
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    records = []
    for char in text:
        glyph_name = cmap[ord(char)]
        bounds = BoundsPen(glyphs)
        glyphs[glyph_name].draw(bounds)
        outline = SVGPathPen(glyphs, ntos=number)
        glyphs[glyph_name].draw(outline)
        records.append((char, font["hmtx"][glyph_name][0], bounds.bounds, outline.getCommands()))

    ink_bounds = [item[2] for item in records if item[2]]
    ink_min = min(bounds[1] for bounds in ink_bounds)
    ink_max = max(bounds[3] for bounds in ink_bounds)
    ink_mid = (ink_min + ink_max) / 2
    length = sum(item[1] * scale for item in records) + tracking * (len(text) - 1)
    span = length / TEXT_RADIUS
    cursor = -length / 2
    family = font["name"].getDebugName(6)
    if weight == 700:
        family = font["name"].getBestFamilyName().replace(" ", "") + "-Bold"
    lines = [f'  <g id="{"chinese" if bottom else "english"}" aria-label="{escape(text)}" data-font="{family}" data-font-weight="{font["OS/2"].usWeightClass}" data-font-size="{size}" data-tracking="{tracking}">']
    for char, advance, bounds, outline in records:
        angle = (cursor + advance * scale / 2) / TEXT_RADIUS
        x = CENTER + TEXT_RADIUS * sin(angle)
        y = CENTER + TEXT_RADIUS * cos(angle) * (1 if bottom else -1)
        rotation = degrees(angle) * (-1 if bottom else 1)
        if outline:
            transform = (
                f"translate({number(x)} {number(y)}) "
                f"rotate({number(rotation)}) "
                f"scale({number(scale)} {number(-scale)}) "
                f"translate({number(-advance / 2)} {number(-ink_mid)})"
            )
            lines.append(f'    <path data-char="{escape(char)}" transform="{transform}" d="{outline}"/>')
        cursor += advance * scale + tracking
    lines.append("  </g>")
    ink_half_height = (ink_max - ink_min) * scale / 2
    assert TEXT_RADIUS - ink_half_height > INNER_RADIUS + INNER_STROKE / 2 + 10
    assert TEXT_RADIUS + ink_half_height < OUTER_RADIUS - OUTER_STROKE / 2 - 10
    return "\n".join(lines), span, family


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--png", action="store_true", help="Also refresh both sets of 1000px PNG exports using macOS sips.")
    parser.add_argument("--english-font", type=Path, default=FONT_CACHE / "Cinzel-Variable.ttf")
    parser.add_argument("--chinese-font", type=Path, default=FONT_CACHE / "SourceHanSerifSC-Bold.otf")
    args = parser.parse_args()
    english, en_span, en_family = arc_text(
        ENGLISH, args.english_font, 0, EN_SIZE, EN_TRACKING, weight=700
    )
    chinese, cn_span, cn_family = arc_text(
        CHINESE, args.chinese_font, 0, CN_SIZE, CN_TRACKING, bottom=True
    )
    # Small bilateral separators occupy the two equal language breaks.
    side_angle = (en_span / 2 + radians(180) - cn_span / 2) / 2
    dot_x = TEXT_RADIUS * sin(side_angle)
    dot_y = CENTER - TEXT_RADIUS * cos(side_angle)
    motif_scale = DISC_RADIUS / 176
    motif_x = CENTER + (112 - CENTER) * motif_scale + MOTIF_OFFSET_X
    motif_y = CENTER + (126 - CENTER) * motif_scale + MOTIF_OFFSET_Y
    for name, color in COLORS.items():
        svg = f'''<svg viewBox="0 0 600 600" width="1200" height="1200" xmlns="http://www.w3.org/2000/svg" fill="{color}" role="img" aria-labelledby="badge-title badge-desc">
  <title id="badge-title">{CHINESE} · {ENGLISH}</title>
  <desc id="badge-desc">紧凑同心圆徽标。中文：思源宋体 Bold；英文：Cinzel Bold（700）。文字已转矢量轮廓。</desc>
  <!-- Generated by scripts/build_canonical_badges.py; all glyphs are font-independent outlines. -->
  <circle cx="300" cy="300" r="{OUTER_RADIUS}" fill="#ffffff" stroke="{color}" stroke-width="{OUTER_STROKE}"/>
  <circle cx="300" cy="300" r="{INNER_RADIUS}" fill="none" stroke="{color}" stroke-width="{INNER_STROKE}"/>
  <circle cx="300" cy="300" r="{DISC_RADIUS}"/>
{english}
{chinese}
  <g id="language-separators" aria-hidden="true">
    <circle cx="{number(CENTER - dot_x)}" cy="{number(dot_y)}" r="3"/>
    <circle cx="{number(CENTER + dot_x)}" cy="{number(dot_y)}" r="3"/>
  </g>
  <g id="sail" transform="translate({number(motif_x)} {number(motif_y)}) scale({number(1.76 * motif_scale)})" fill="#ffffff">
{SAIL}
  </g>
</svg>
'''
        for directory in OUTPUT_DIRS:
            target = directory / f"HSMO_Badge_Canonical_{name}.svg"
            target.write_text(svg, encoding="utf-8")
        if args.png:
            png = OUTPUT_DIRS[0] / f"HSMO_Badge_Canonical_{name}.png"
            run([
                "sips", "-s", "format", "png", "-Z", "1000",
                str(OUTPUT_DIRS[0] / f"HSMO_Badge_Canonical_{name}.svg"),
                "--out", str(png),
            ], check=True, capture_output=True, text=True)
            copy2(png, OUTPUT_DIRS[1] / png.name)
    print(f"Built 15 SVGs; English {en_family}, Chinese {cn_family}.")
    print(f"Text spans: English {degrees(en_span):.1f}°, Chinese {degrees(cn_span):.1f}°.")
    print(f"Clear ring band: {OUTER_RADIUS - OUTER_STROKE / 2 - INNER_RADIUS - INNER_STROKE / 2:g} / 600 units.")
    if args.png:
        print("Refreshed 10 PNGs at 1000 × 1000 with transparency.")


if __name__ == "__main__":
    main()
