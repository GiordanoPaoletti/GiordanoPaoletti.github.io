#!/usr/bin/env python3
"""Fetch publications from a Google Scholar profile and write data/publications.json.

Usage:
    SCHOLAR_ID=XXXXXXXXXXXX python scripts/update_publications.py

The Scholar ID is the value of the `user=` query parameter in your profile URL,
e.g. https://scholar.google.com/citations?user=XXXXXXXXXXXX
"""
import json
import os
import sys
from datetime import date
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "publications.json"
SCHOLAR_ID = os.environ.get("SCHOLAR_ID", "").strip()


def main() -> int:
    if not SCHOLAR_ID:
        print("ERROR: set the SCHOLAR_ID environment variable.", file=sys.stderr)
        return 2

    try:
        from scholarly import scholarly
    except ImportError:
        print("ERROR: run `pip install scholarly` first.", file=sys.stderr)
        return 2

    print(f"Fetching Scholar profile {SCHOLAR_ID} ...")
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author, sections=["publications"])

    pubs = []
    for p in author.get("publications", []):
        bib = p.get("bib", {}) or {}
        title = (bib.get("title") or "").strip()
        if not title:
            continue
        year = bib.get("pub_year")
        try:
            year = int(year) if year else None
        except (TypeError, ValueError):
            year = None
        venue = (bib.get("venue") or bib.get("journal") or bib.get("citation") or "").strip()
        pub_id = p.get("author_pub_id")
        url = (
            f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={SCHOLAR_ID}&citation_for_view={pub_id}"
            if pub_id else ""
        )
        pubs.append({"title": title, "venue": venue, "year": year, "url": url})

    # Newest first; undated entries go last
    pubs.sort(key=lambda x: (x["year"] is None, -(x["year"] or 0)))

    out = {
        "last_updated": date.today().isoformat(),
        "source": "Google Scholar",
        "scholar_profile": f"https://scholar.google.com/citations?user={SCHOLAR_ID}",
        "publications": pubs,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(pubs)} publications to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
