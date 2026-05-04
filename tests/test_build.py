"""Tests for build-from-db.py output."""

import json
import os
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "wines-db.json")
SV_DIR = os.path.join(BASE_DIR, "sortiment")
EN_DIR = os.path.join(BASE_DIR, "en", "sortiment")


@pytest.fixture(scope="module")
def db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def websida_wines(db):
    return [w for w in db["wines"] if w.get("websida") and w.get("slug")]


def test_sv_pages_exist(websida_wines):
    missing = []
    for w in websida_wines:
        path = os.path.join(SV_DIR, f"{w['slug']}.html")
        if not os.path.exists(path):
            missing.append(w["slug"])
    assert not missing, f"Saknade SV-sidor: {missing}"


def test_en_pages_exist(websida_wines):
    missing = []
    for w in websida_wines:
        path = os.path.join(EN_DIR, f"{w['slug']}.html")
        if not os.path.exists(path):
            missing.append(w["slug"])
    assert not missing, f"Saknade EN-sidor: {missing}"


def test_page_count_matches(websida_wines):
    expected = len(websida_wines)
    sv_count = len([f for f in os.listdir(SV_DIR) if f.endswith(".html")])
    en_count = len([f for f in os.listdir(EN_DIR) if f.endswith(".html")])
    # Pages should be at least as many as expected (may have stale pages)
    assert sv_count >= expected, f"SV: {sv_count} sidor, förväntat minst {expected}"
    assert en_count >= expected, f"EN: {en_count} sidor, förväntat minst {expected}"


def test_pages_have_valid_html(websida_wines):
    """Check that generated pages have basic HTML structure."""
    for w in websida_wines[:5]:  # Sample first 5
        path = os.path.join(SV_DIR, f"{w['slug']}.html")
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "<!DOCTYPE html>" in content
        assert "<title>" in content
        assert w["namn"] in content or w["producent"] in content


def test_pages_reference_correct_producer(websida_wines):
    """Wine pages should mention the producer name."""
    for w in websida_wines[:5]:
        path = os.path.join(SV_DIR, f"{w['slug']}.html")
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert w["producent"] in content, (
            f"Sidan {w['slug']}.html nämner inte producenten '{w['producent']}'"
        )
