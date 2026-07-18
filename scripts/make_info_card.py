from __future__ import annotations

from common import ASSETS, ensure_dirs, esc, load_profile


def main() -> None:
    ensure_dirs()
    p = load_profile()
    rows = [
        ("name", p["name"]),
        ("role", p["title"]),
        ("location", p["location"]),
        ("education", p["education"]),
        ("focus", p["focus"]),
        ("stack", p["stack"]),
        ("projects", p["projects"]),
        ("status", p["status"]),
    ]
    body = []
    for i, (key, value) in enumerate(rows):
        y = 119 + i * 30
        delay = 0.45 + i * 0.22
        body.append(
            f'<g class="line" style="animation-delay:{delay:.2f}s">'
            f'<text class="key" x="26" y="{y}">{esc(key.ljust(9))}</text>'
            f'<text class="sep" x="121" y="{y}">:</text>'
            f'<text class="value" x="140" y="{y}">{esc(value)}</text></g>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="490" height="430" viewBox="0 0 490 430" role="img" aria-labelledby="title desc">
<title id="title">Profile information for {esc(p['name'])}</title>
<desc id="desc">A terminal-style developer profile card.</desc>
<style>
  .bg {{ fill: {esc(p['background'])}; }} .frame {{ fill:none; stroke:#30363d; }} .bar {{ fill:#161b22; }}
  text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  .header {{ fill:{esc(p['foreground'])}; font-size:20px; font-weight:700; }}
  .handle,.key,.sep {{ fill:{esc(p['accent'])}; }} .handle {{ font-size:12px; }}
  .key,.sep,.value {{ font-size:12px; }} .value {{ fill:{esc(p['foreground'])}; }}
  .line {{ opacity:0; animation:show 6.4s ease-in-out infinite; }}
  .footer {{ fill:{esc(p['muted'])}; font-size:11px; }} .cursor {{ fill:{esc(p['accent'])}; animation:blink 1s step-end infinite; }}
  @keyframes show {{ 0%,7% {{opacity:0;transform:translateY(4px)}} 13%,87% {{opacity:1;transform:none}} 95%,100% {{opacity:0}} }}
  @keyframes blink {{ 50% {{opacity:0}} }}
</style>
<rect class="bg" width="100%" height="100%" rx="12"/><rect class="frame" x=".5" y=".5" width="489" height="429" rx="11.5"/>
<rect class="bar" x="1" y="1" width="488" height="30" rx="11"/>
<circle cx="16" cy="16" r="4" fill="#f85149"/><circle cx="29" cy="16" r="4" fill="#d29922"/><circle cx="42" cy="16" r="4" fill="#3fb950"/>
<text class="header" x="26" y="66">{esc(p['name'])}</text><text class="handle" x="26" y="88">github.com/{esc(p['handle'])}</text>
{''.join(body)}
<line x1="26" y1="370" x2="464" y2="370" stroke="#21262d"/>
<text class="footer" x="26" y="399">$ open to collaboration <tspan class="cursor">▋</tspan></text>
</svg>'''
    (ASSETS / "info-card.svg").write_text(svg, encoding="utf-8")
    print(f"Wrote {ASSETS / 'info-card.svg'}")


if __name__ == "__main__":
    main()
