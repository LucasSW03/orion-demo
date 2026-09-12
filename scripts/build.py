"""Build the static demo site into dist/.

mockup/index.html is written in "artifact" form (no <html>/<head>/<body> skeleton)
so it can be published as a Claude artifact as-is. This script wraps it into a
standalone HTML document and copies the images, robots.txt and CNAME next to it.
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "mockup" / "index.html"
IMG = ROOT / "mockup" / "img"
DIST = ROOT / "dist"
DEMO_DOMAIN = "orion.krimisa.com.ar"


def wrap_document(fragment: str) -> str:
    """Split the artifact fragment into head (meta, title, fonts, style) and body."""
    style_start = fragment.index("<style>")
    style_end = fragment.index("</style>", style_start) + len("</style>")
    head = fragment[:style_end]
    body = fragment[style_end:]
    return (
        "<!doctype html>\n<html lang=\"es\">\n<head>\n"
        + head
        + "\n</head>\n<body>\n"
        + body
        + "\n</body>\n</html>\n"
    )


def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    (DIST / "index.html").write_text(wrap_document(SRC.read_text(encoding="utf-8")), encoding="utf-8")
    shutil.copytree(IMG, DIST / "img")
    # Demo must never be indexed (it would compete with the real site later),
    # but link unfurlers need access so the URL previews well in LinkedIn and WhatsApp.
    (DIST / "robots.txt").write_text(
        "User-agent: LinkedInBot\nAllow: /\n\n"
        "User-agent: WhatsApp\nAllow: /\n\n"
        "User-agent: facebookexternalhit\nAllow: /\n\n"
        "User-agent: Twitterbot\nAllow: /\n\n"
        "User-agent: *\nDisallow: /\n",
        encoding="utf-8",
    )
    (DIST / "CNAME").write_text(DEMO_DOMAIN + "\n", encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    files = sorted(p.relative_to(DIST).as_posix() for p in DIST.rglob("*") if p.is_file())
    print(f"built {len(files)} files into {DIST}")
    for f in files:
        print("  ", f)


if __name__ == "__main__":
    build()
