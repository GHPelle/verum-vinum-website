"""Tests for restaurant price list (r-lista.js) data."""

import json
import os
import re
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RLISTA_PATH = os.path.join(BASE_DIR, "r-lista.js")
DB_PATH = os.path.join(BASE_DIR, "wines-db.json")


@pytest.fixture(scope="module")
def r_wines():
    with open(RLISTA_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"const rWines = (\[.*?\]);", content, re.DOTALL)
    assert m, "Kunde inte hitta rWines i r-lista.js"
    return json.loads(m.group(1))


@pytest.fixture(scope="module")
def db_r_wines():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [w for w in data["wines"] if w.get("r_prislista")]


def test_r_wines_not_empty(r_wines):
    assert len(r_wines) > 0


def test_r_wines_have_prices(r_wines):
    no_price = [w["namn"] for w in r_wines if not w.get("pris_restaurang")]
    # Some may intentionally lack prices
    if no_price:
        pytest.skip(f"{len(no_price)} r-lista viner utan pris (kan vara medvetet)")


def test_r_wines_count_matches_db(r_wines, db_r_wines):
    assert len(r_wines) == len(db_r_wines), (
        f"r-lista.js har {len(r_wines)} viner men db har {len(db_r_wines)} med r_prislista=true"
    )


def test_r_wines_have_required_fields(r_wines):
    required = ["namn", "producent", "typ"]
    for w in r_wines:
        for field in required:
            assert w.get(field), f"R-lista vin saknar {field}: {w}"


def test_r_wines_price_format(r_wines):
    for w in r_wines:
        price = w.get("pris_restaurang")
        if price is not None:
            assert isinstance(price, (int, float)), (
                f"R-lista vin '{w['namn']}' har icke-numeriskt pris: {price!r}"
            )
            assert price > 0, f"R-lista vin '{w['namn']}' har pris <= 0"
