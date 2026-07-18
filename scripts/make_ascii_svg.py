from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from common import ASSETS, ensure_dirs, esc, load_profile

RAMP = "@%#*+=-:. "


def portrait_to_ascii(
    path: Path,
    cols: int = 78,
    rows: int = 44,
) -> list[str]:
    image = Image.open(path).convert("RGB")
    width, height = image.size

    # Tight head-and-shoulders crop
    crop_width = int(width * 0.62)
    crop_height = int(height * 0.68)

    left = (width - crop_width) // 2
    top = int(height * 0.01)

    image = image.crop(
        (
            left,
            top,
            left + crop_width,
            min(height, top + crop_height),
        )
    )

    gray = ImageOps.grayscale(image)

    # Improve facial separation without crushing everything into black
    gray = ImageOps.autocontrast(gray, cutoff=(2, 3))
    gray = ImageEnhance.Contrast(gray).enhance(1.18)
    gray = ImageEnhance.Brightness(gray).enhance(1.06)

    gray = gray.filter(
        ImageFilter.UnsharpMask(
            radius=1.0,
            percent=135,
            threshold=3,
        )
    )

    gray = gray.resize(
        (cols, rows),
        Image.Resampling.LANCZOS,
    )

    ramp = "@%#*+=-:. "
    pixels = list(gray.getdata())
    lines: list[str] = []

    for y in range(rows):
        line = ""

        for x in range(cols):
            value = pixels[y * cols + x]
            index = min(
                len(ramp) - 1,
                value * len(ramp) // 256,
            )
            line += ramp[index]

        lines.append(line.rstrip())

    return lines


def render_svg(lines: list[str]) -> str:
    p = load_profile()
    width, height = 370, 430
    text_x, text_y, line_height = 20, 38, 8.0
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
  .row {{ fill: {esc(p['foreground'])}; font: 6.3px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; white-space: pre; opacity: 0; animation: reveal {duration:.2f}s linear infinite; }}
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
