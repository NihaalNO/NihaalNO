# Setup

## Publish the profile

1. On GitHub, create a **public** repository named exactly `NihaalNO`.
2. Copy this package into the repository root.
3. Edit `profile.json` and the links in `README.md` if needed.
4. Run the commands below, then commit and push.

```bash
python -m pip install -r scripts/requirements.txt
python scripts/generate_all.py
git add README.md assets scripts profile.json .github .gitignore SETUP.md
git commit -m "Add animated profile README"
git push
```

GitHub recognizes a repository as a profile README only when its name exactly matches your username.

## Regenerate the portrait locally

The original photograph is intentionally not included. Keep it outside the public repository and run:

```bash
python scripts/make_ascii_svg.py "/path/to/portrait.jpeg"
```

Only `assets/nihaal-ascii.svg` needs to be committed. Files placed under `local-input/` are ignored.

## Customize

- Change profile text and colors in `profile.json`.
- Re-run `python scripts/make_info_card.py` after editing the profile.
- The scheduled workflow refreshes contribution data daily and can also be run manually from the Actions tab.
- If your repository uses protected branches, let the workflow open/update through your normal branch policy instead of granting direct writes.

## Troubleshooting

- **Workflow cannot push:** Settings → Actions → General → Workflow permissions → select **Read and write permissions**.
- **Images appear stale:** GitHub caches images. Wait a few minutes or commit a regenerated SVG.
- **No contribution data:** confirm `handle` in `profile.json` matches the GitHub username exactly.
