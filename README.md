# Giordano Paoletti — Personal Website

Static personal site (GitHub Pages) presenting my CV, with publications auto-synced
daily from Google Scholar via GitHub Actions.

## Structure

```
index.html                       # the site (CV content)
assets/style.css                 # styles
assets/main.js                   # loads publications.json
data/publications.json           # publications (auto-updated)
scripts/update_publications.py   # Scholar -> publications.json
.github/workflows/update-scholar.yml  # daily cron
```

## One-time setup

### 1. Push to GitHub
For a personal site at `https://<username>.github.io`, name the repo
`<username>.github.io`. Then:

```bash
git init
git add .
git commit -m "Initial site"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

### 2. Enable GitHub Pages
Repo → **Settings → Pages** → Source: **Deploy from a branch** → Branch: `main` / root.

### 3. Scholar auto-update
The Scholar ID is already set in `.github/workflows/update-scholar.yml`
(`SCHOLAR_ID: "Nm7mot8AAAAJ"`). Just run the workflow once manually:
**Actions → "Update publications from Google Scholar" → Run workflow**.
After that it runs daily at 05:30 UTC.

> Note: Google Scholar has no official API. The job scrapes the public profile
> and occasionally gets rate-limited; on those days it simply skips and retries
> the next day. Until the first run, the site shows the seed list from the CV.

## Run locally

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

To refresh publications locally:

```bash
pip install -r requirements.txt
SCHOLAR_ID=XXXXXXXXXXXX python scripts/update_publications.py
```
