from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from common import ASSETS, ensure_dirs, esc, load_profile

RAMP = "@%#*+=-:. "


def portrait_to_ascii(path: Path, cols: int = 72, rows: int = 44) -> list[str]:
    image = Image.open(path).convert("RGB")
    width, height = image.size

    # Favor the upper-center of a portrait: face, hair, neck, and shoulders.
    crop_width = min(width, int(height * 0.82))
    left = max(0, (width - crop_width) // 2)
    top = max(0, int(height * 0.01))
    bottom = min(height, top + int(crop_width * 1.06))
    image = image.crop((left, top, left + crop_width, bottom))

    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray = ImageEnhance.Contrast(gray).enhance(1.35)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=3))
    gray = gray.resize((cols, rows), Image.Resampling.LANCZOS)

    pixels = list(gray.getdata())
    lines: list[str] = []
    for y in range(rows):
        line = "".join(RAMP[min(len(RAMP) - 1, pixels[y * cols + x] * len(RAMP) // 256)] for x in range(cols))
        lines.append(line.rstrip())
    return lines


def render_svg(lines: list[str]) -> str:
    p = load_profile()
    width, height = 370, 430
    text_x, text_y, line_height = 20, 38, 8.45
    duration = max(4.5, len(lines) * 0.075 + 1.2)
    text_nodes = []
    for index, line in enumerate(lines):
        delay = index * 0.075
        text_nodes.append(
            f'<text x="{text_x}" y="{text_y + index * line_height:.2f}" '
            f'class="row" style="animation-delay:{delay:.3f}s">{esc(line) or " "}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Animated ASCII portrait of {esc(p['name'])}</title>
<desc id="desc">A monochrome terminal-style portrait drawn one row at a time.</desc>
<style>
  .bg {{ fill: {esc(p['background'])}; }}
  .frame {{ fill: none; stroke: #30363d; }}
  .bar {{ fill: #161b22; }}
  .row {{ fill: {esc(p['foreground'])}; font: 7.2px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; white-space: pre; opacity: 0; animation: reveal {duration:.2f}s linear infinite; }}
  .prompt {{ fill: {esc(p['accent'])}; font: 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  @keyframes reveal {{ 0%, 5% {{ opacity: 0; }} 8%, 86% {{ opacity: 1; }} 94%, 100% {{ opacity: 0; }} }}
</style>
<rect class="bg" width="100%" height="100%" rx="12"/>
<rect class="frame" x=".5" y=".5" width="369" height="429" rx="11.5"/>
<rect class="bar" x="1" y="1" width="368" height="26" rx="11"/>
<circle cx="15" cy="14" r="4" fill="#f85149"/><circle cx="28" cy="14" r="4" fill="#d29922"/><circle cx="41" cy="14" r="4" fill="#3fb950"/>
<text class="prompt" x="55" y="18">portrait.sh --user {esc(p['handle'])}</text>
{''.join(text_nodes)}
<text class="prompt" x="18" y="414">$ <tspan fill="{esc(p['foreground'])}">identity rendered</tspan><tspan class="cursor">▋</tspan></text>
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a portrait to an animated ASCII SVG.")
    parser.add_argument("portrait", type=Path)
    args = parser.parse_args()
    if not args.portrait.is_file():
        raise SystemExit(f"Portrait not found: {args.portrait}")
    ensure_dirs()
    (ASSETS / "nihaal-ascii.svg").write_text(render_svg(portrait_to_ascii(args.portrait)), encoding="utf-8")
    print(f"Wrote {ASSETS / 'nihaal-ascii.svg'}")


if __name__ == "__main__":
    main()
