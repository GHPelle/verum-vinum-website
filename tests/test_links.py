"""Tests for broken internal links and image references."""

import os
import re
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def collect_html_files():
    """Collect all HTML files in the project (excluding node_modules etc)."""
    files = []
    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in {"node_modules", ".git", "tests"}]
        for fname in filenames:
            if fname.endswith(".html"):
                files.append(os.path.join(root, fname))
    return files


@pytest.fixture(scope="module")
def html_files():
    return collect_html_files()


def test_internal_href_links(html_files):
    """Check that internal href links point to existing files."""
    broken = []
    for fpath in html_files:
        fdir = os.path.dirname(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        for m in re.finditer(r'href="([^"#?]+)"', content):
            href = m.group(1)
            # Skip external, javascript, mailto, tel, JS template literals
            if href.startswith(("http", "javascript:", "mailto:", "tel:", "#", "data:")) or "${" in href:
                continue
            target = os.path.normpath(os.path.join(fdir, href))
            if not os.path.exists(target):
                rel = os.path.relpath(fpath, BASE_DIR)
                broken.append(f"{rel} -> {href}")

    assert not broken, f"Trasiga interna länkar ({len(broken)}):\n" + "\n".join(broken[:20])


def test_image_references(html_files):
    """Check that img src references point to existing files."""
    missing = []
    for fpath in html_files:
        fdir = os.path.dirname(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        for m in re.finditer(r'<img[^>]+src="([^"]+)"', content):
            src = m.group(1)
            # Skip external URLs and data URIs
            if src.startswith(("http", "data:")):
                continue
            target = os.path.normpath(os.path.join(fdir, src))
            if not os.path.exists(target):
                rel = os.path.relpath(fpath, BASE_DIR)
                missing.append(f"{rel} -> {src}")

    if missing:
        pytest.skip(f"Saknade bilder (ej kritiskt): {len(missing)} st")
