#!/usr/bin/env python3
"""Generate an RSS 2.0 feed from Zine blog posts.

Parses the .smd frontmatter from content/blog/ and writes zig-out/feed.xml.
Invoked by .github/workflows/website.yml after `zig build`.

Usage:
    python3 tools/gen_rss.py
"""

import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from xml.sax.saxutils import escape

HOST = "https://kassane.github.io"
SITE_TITLE = "Kassane Website"
SITE_DESCRIPTION = "Systems programming blog by Matheus Catarino (@kassane)"


def parse_smd(path: Path) -> dict | None:
    """Extract frontmatter fields from a .smd file.

    Returns None for draft pages or files without valid frontmatter.
    """
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    front = m.group(1)

    def get(key: str) -> str:
        hit = re.search(rf'\.{key}\s*=\s*"([^"]*)"', front)
        return hit.group(1) if hit else ""

    def get_bool(key: str) -> bool:
        hit = re.search(rf'\.{key}\s*=\s*(true|false)', front)
        return bool(hit and hit.group(1) == "true")

    def get_date(key: str) -> str:
        hit = re.search(rf'\.{key}\s*=\s*@date\("([^"]+)"\)', front)
        return hit.group(1) if hit else ""

    if get_bool("draft"):
        return None

    return {
        "title": get("title"),
        "description": get("description"),
        "author": get("author"),
        "date_iso": get_date("date"),
        "layout": get("layout"),
    }


def to_rfc822(iso: str) -> str:
    """Convert an ISO 8601 datetime string to RFC 822 format for RSS."""
    try:
        dt = datetime.fromisoformat(iso).replace(tzinfo=timezone.utc)
        return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
    except (ValueError, AttributeError):
        return ""


def build_feed(posts: list[dict]) -> str:
    """Render the complete RSS 2.0 XML string."""
    last_build = to_rfc822(posts[0]["date_iso"]) if posts else ""

    items = ""
    for p in posts:
        items += (
            "\n    <item>"
            f"\n      <title>{escape(p['title'])}</title>"
            f"\n      <link>{p['url']}</link>"
            f"\n      <guid isPermaLink=\"true\">{p['url']}</guid>"
            f"\n      <description>{escape(p['description'])}</description>"
            f"\n      <author>{escape(p['author'])}</author>"
            f"\n      <pubDate>{to_rfc822(p['date_iso'])}</pubDate>"
            "\n    </item>"
        )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        f"    <title>{escape(SITE_TITLE)}</title>\n"
        f"    <link>{HOST}</link>\n"
        f"    <description>{escape(SITE_DESCRIPTION)}</description>\n"
        "    <language>en-us</language>\n"
        f'    <atom:link href="{HOST}/feed.xml" rel="self" type="application/rss+xml"/>\n'
        f"    <lastBuildDate>{last_build}</lastBuildDate>"
        f"{items}\n"
        "  </channel>\n"
        "</rss>\n"
    )


def main() -> int:
    content_dir = Path("content/blog")
    out_path = Path("zig-out/feed.xml")

    if not content_dir.is_dir():
        print(f"ERROR: {content_dir} does not exist", file=sys.stderr)
        return 1

    posts = []
    for smd in content_dir.glob("*.smd"):
        meta = parse_smd(smd)
        if meta is None or not meta["title"]:
            continue
        meta["slug"] = smd.stem
        meta["url"] = f"{HOST}/blog/{smd.stem}/"
        posts.append(meta)

    # Newest first
    posts.sort(key=lambda p: p["date_iso"], reverse=True)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_feed(posts), encoding="utf-8")
    print(f"feed.xml: {len(posts)} item(s) → {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
