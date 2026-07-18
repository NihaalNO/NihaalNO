from __future__ import annotations

import json
from datetime import date

import requests
from bs4 import BeautifulSoup

from common import DATA, ensure_dirs, load_profile


def main() -> None:
    ensure_dirs()
    username = load_profile()["handle"]
    url = f"https://github.com/users/{username}/contributions"
    response = requests.get(url, headers={"User-Agent": "github-profile-readme-generator/1.0"}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    for cell in soup.select("[data-date][data-level]"):
        raw_date = cell.get("data-date", "")
        try:
            date.fromisoformat(raw_date)
            level = max(0, min(4, int(cell.get("data-level", 0))))
        except (TypeError, ValueError):
            continue
        days.append({"date": raw_date, "level": level})
    if len(days) < 300:
        raise RuntimeError(f"Expected a contribution year, found only {len(days)} cells")
    payload = {"username": username, "updated_at": date.today().isoformat(), "days": days}
    (DATA / "contributions.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Fetched {len(days)} contribution cells for {username}")


if __name__ == "__main__":
    main()
