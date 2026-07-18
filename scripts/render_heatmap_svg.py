from __future__ import annotations

import json
from datetime import date

from common import ASSETS, DATA, ensure_dirs, esc, load_profile


def main() -> None:
    ensure_dirs()
    profile = load_profile()
    payload = json.loads((DATA / "contributions.json").read_text(encoding="utf-8"))
    days = sorted(payload["days"], key=lambda item: item["date"])
    first = date.fromisoformat(days[0]["date"])
    cells = []
    palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    for index, item in enumerate(days):
        current = date.fromisoformat(item["date"])
        week = (current - first).days // 7
        weekday = current.weekday()
        # GitHub displays Sunday first; Python displays Monday first.
        row = (weekday + 1) % 7
        x, y = 48 + week * 14, 88 + row * 14
        delay = min(4.2, index * 0.008)
        cells.append(
            f'<rect class="day" x="{x}" y="{y}" width="10" height="10" rx="2" fill="{palette[int(item["level"])]}" '
            f'style="animation-delay:{delay:.3f}s"><title>{esc(item["date"])} · level {int(item["level"])}</title></rect>'
        )
    width = max(860, 70 + ((date.fromisoformat(days[-1]["date"]) - first).days // 7 + 1) * 14)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="235" viewBox="0 0 {width} 235" role="img" aria-labelledby="title desc">
<title id="title">GitHub contributions for {esc(payload['username'])}</title>
<desc id="desc">Contribution activity through {esc(payload['updated_at'])}.</desc>
<style>
  .bg{{fill:{esc(profile['background'])}}}.frame{{fill:none;stroke:#30363d}}text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
  .heading{{fill:{esc(profile['foreground'])};font-size:16px;font-weight:700}}.sub{{fill:{esc(profile['muted'])};font-size:11px}}
  .label{{fill:{esc(profile['muted'])};font-size:9px}}.day{{opacity:0;animation:pop 7s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
  @keyframes pop{{0%,5%{{opacity:0;transform:scale(.3)}}12%,88%{{opacity:1;transform:scale(1)}}96%,100%{{opacity:0}}}}
</style>
<rect class="bg" width="100%" height="100%" rx="12"/><rect class="frame" x=".5" y=".5" width="{width-1}" height="234" rx="11.5"/>
<text class="heading" x="24" y="34">contribution activity</text><text class="sub" x="24" y="55">{esc(payload['username'])} · refreshed {esc(payload['updated_at'])}</text>
<text class="label" x="20" y="102">Mon</text><text class="label" x="20" y="130">Wed</text><text class="label" x="20" y="158">Fri</text>
{''.join(cells)}
<text class="sub" x="24" y="211">Less  ▪ ▪ ▪ ▪ ▪  More</text>
</svg>'''
    (ASSETS / "contrib-heatmap.svg").write_text(svg, encoding="utf-8")
    print(f"Wrote {ASSETS / 'contrib-heatmap.svg'}")


if __name__ == "__main__":
    main()
