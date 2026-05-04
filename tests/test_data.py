"""Tests for wines-db.json data integrity."""

import json
import os
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "wines-db.json")


@pytest.fixture(scope="module")
def db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def wines(db):
    return db["wines"]


def test_db_has_wines(db):
    assert "wines" in db
    assert len(db["wines"]) > 0


def test_no_empty_slugs(wines):
    for w in wines:
        assert w.get("slug"), f"Vin '{w.get('namn', '?')}' saknar slug"


def test_unique_slugs(wines):
    slugs = [w["slug"] for w in wines]
    dupes = [s for s in slugs if slugs.count(s) > 1]
    assert len(dupes) == 0, f"Duplicerade slugs: {set(dupes)}"


def test_required_fields(wines):
    required = ["slug", "namn", "producent", "typ"]
    for w in wines:
        for field in required:
            assert field in w and w[field], (
                f"Vin '{w.get('slug', '?')}' saknar obligatoriskt fält: {field}"
            )


def test_valid_types(wines):
    valid_types = {"Rött", "Vitt", "Rosé", "Mousserande", "Starkvin", "Vinlåda"}
    for w in wines:
        assert w.get("typ") in valid_types, (
            f"Vin '{w['slug']}' har ogiltig typ: '{w.get('typ')}'"
        )


def test_prices_are_numeric_or_null(wines):
    price_fields = ["pris_restaurang", "pris_sb", "pris_privatimport"]
    for w in wines:
        for field in price_fields:
            val = w.get(field)
            if val is not None:
                assert isinstance(val, (int, float)), (
                    f"Vin '{w['slug']}' har icke-numeriskt {field}: {val!r}"
                )


def test_websida_wines_have_slugs(wines):
    for w in wines:
        if w.get("websida", False):
            assert w.get("slug"), (
                f"Vin '{w.get('namn', '?')}' har websida=true men ingen slug"
            )


def test_volym_is_positive(wines):
    for w in wines:
        vol = w.get("volym")
        if vol is not None:
            assert isinstance(vol, (int, float)) and vol > 0, (
                f"Vin '{w['slug']}' har ogiltig volym: {vol!r}"
            )
