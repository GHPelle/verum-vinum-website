#!/usr/bin/env python3
"""
Build-all: Single script that regenerates all derived files from wines-db.json.

Steps:
1. Load wines-db.json (master data)
2. Generate wine pages (sortiment/ + en/sortiment/) via build-from-db.py logic
3. Update sok.html + en/sok.html with wine data for search
4. Update r-lista.js with restaurant wines
5. Update INITIAL_DATA in admin.html
6. Validate: check for broken internal links and missing images
7. Print report
"""

import json
import os
import re
import sys
import importlib.util
from html import escape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "wines-db.json")


def load_db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ── Step 1: Generate wine pages ──────────────────────────────────
def step_generate_pages(data):
    """Run the build-from-db logic to generate wine HTML pages."""
    spec = importlib.util.spec_from_file_location(
        "build_from_db", os.path.join(BASE_DIR, "build-from-db.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    sv_dir = os.path.join(BASE_DIR, "sortiment")
    en_dir = os.path.join(BASE_DIR, "en", "sortiment")
    os.makedirs(sv_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)

    existing_images = mod.load_existing_images()
    wines = data.get("wines", [])
    generated = 0

    for wine in wines:
        if not wine.get("websida", False):
            continue
        slug = wine.get("slug", "")
        if not slug:
            continue

        sv_html = mod.build_page(wine, "sv", existing_images)
        with open(os.path.join(sv_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(sv_html)

        en_html = mod.build_page(wine, "en", existing_images)
        with open(os.path.join(en_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(en_html)

        generated += 1

    return generated


# ── Step 2: Update sok.html search data ──────────────────────────
def build_search_wine(wine):
    """Build the search-page wine object from db wine."""
    return {
        "slug": wine.get("slug", ""),
        "name": wine.get("namn", ""),
        "producer": wine.get("producent", ""),
        "type": wine.get("typ", ""),
        "country": wine.get("land", ""),
        "region": wine.get("region", ""),
        "price": wine.get("pris_restaurang"),
        "grape_type": wine.get("druvor", ""),
        "grapes_raw": wine.get("druvor", ""),
    }


def step_update_sok(data):
    """Update the inline wines array in sok.html and en/sok.html."""
    wines = [
        build_search_wine(w)
        for w in data.get("wines", [])
        if w.get("websida", False) and w.get("slug")
    ]
    wines_json = json.dumps(wines, ensure_ascii=False)

    updated = 0
    for path in [
        os.path.join(BASE_DIR, "sok.html"),
        os.path.join(BASE_DIR, "en", "sok.html"),
    ]:
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = re.sub(
            r"const wines = \[.*?\];",
            f"const wines = {wines_json};",
            content,
            count=1,
        )
        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated += 1

    return updated


# ── Step 3: Update r-lista.js ────────────────────────────────────
def step_update_rlista(data):
    """Update the rWines array in r-lista.js with wines where r_prislista=true."""
    r_wines = []
    for w in data.get("wines", []):
        if not w.get("r_prislista", False):
            continue
        r_wines.append({
            "slug": w.get("slug", ""),
            "namn": w.get("namn", ""),
            "producent": w.get("producent", ""),
            "typ": w.get("typ", ""),
            "land": w.get("land", ""),
            "region": w.get("region", ""),
            "druvor": w.get("druvor", ""),
            "alkohol": w.get("alkohol", ""),
            "pris_restaurang": w.get("pris_restaurang"),
            "volym": w.get("volym", 750),
            "argang": w.get("argang", ""),
            "allokering": w.get("allokering", False),
            "allokeringstext": w.get("allokeringstext", ""),
            "tillfalligt_slut": w.get("tillfalligt_slut", False),
            "antal_per_kolli": w.get("antal_per_kolli", ""),
        })

    r_json = json.dumps(r_wines, ensure_ascii=False)
    rlista_path = os.path.join(BASE_DIR, "r-lista.js")

    with open(rlista_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(
        r"const rWines = \[.*?\];",
        f"const rWines = {r_json};",
        content,
        count=1,
    )

    with open(rlista_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return len(r_wines)


# ── Step 4: Update INITIAL_DATA in admin.html ────────────────────
def step_update_admin(data):
    """Update the INITIAL_DATA constant in admin.html with current db data."""
    admin_path = os.path.join(BASE_DIR, "admin.html")
    with open(admin_path, "r", encoding="utf-8") as f:
        content = f.read()

    initial_json = json.dumps(data, ensure_ascii=False)
    new_content = re.sub(
        r"const INITIAL_DATA = \{.*?\};",
        f"const INITIAL_DATA = {initial_json};",
        content,
        count=1,
    )

    with open(admin_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


# ── Step 5: Validate ─────────────────────────────────────────────
def step_validate(data):
    """Check for broken internal links and missing images."""
    errors = []
    warnings = []

    sv_dir = os.path.join(BASE_DIR, "sortiment")
    en_dir = os.path.join(BASE_DIR, "en", "sortiment")

    # Check that all websida=true wines have HTML files
    for w in data.get("wines", []):
        if not w.get("websida", False):
            continue
        slug = w.get("slug", "")
        if not slug:
            errors.append(f"Vin '{w.get('namn', '?')}' har websida=true men ingen slug")
            continue
        sv_path = os.path.join(sv_dir, f"{slug}.html")
        en_path = os.path.join(en_dir, f"{slug}.html")
        if not os.path.exists(sv_path):
            errors.append(f"Saknad SV-sida: sortiment/{slug}.html")
        if not os.path.exists(en_path):
            errors.append(f"Saknad EN-sida: en/sortiment/{slug}.html")

    # Check image references in generated pages
    img_dir = os.path.join(BASE_DIR, "images", "viner")
    for html_dir in [sv_dir, en_dir]:
        if not os.path.isdir(html_dir):
            continue
        for fname in os.listdir(html_dir):
            if not fname.endswith(".html"):
                continue
            fpath = os.path.join(html_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                html_content = f.read()
            for m in re.finditer(r'src="\.\.\/images\/viner\/([^"]+)"', html_content):
                img_file = m.group(1)
                if not os.path.exists(os.path.join(img_dir, img_file)):
                    warnings.append(f"Saknad bild: images/viner/{img_file} (refererad i {fname})")

    # Check expected file count
    expected = sum(
        1 for w in data.get("wines", [])
        if w.get("websida", False) and w.get("slug")
    )
    sv_count = len([f for f in os.listdir(sv_dir) if f.endswith(".html")]) if os.path.isdir(sv_dir) else 0
    en_count = len([f for f in os.listdir(en_dir) if f.endswith(".html")]) if os.path.isdir(en_dir) else 0

    return errors, warnings, expected, sv_count, en_count


# ── Main ─────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  VERUM VINUM – BUILD ALL")
    print("=" * 60)

    if not os.path.exists(DB_PATH):
        print(f"\nFEL: wines-db.json hittades inte: {DB_PATH}")
        sys.exit(1)

    data = load_db()
    total_wines = len(data.get("wines", []))
    print(f"\nLaddade wines-db.json: {total_wines} viner")

    # Step 1: Generate pages
    print("\n[1/5] Genererar vinsidor...")
    pages = step_generate_pages(data)
    print(f"      {pages} viner x 2 språk = {pages * 2} HTML-filer")

    # Step 2: Update search pages
    print("\n[2/5] Uppdaterar söksidor (sok.html + en/sok.html)...")
    sok_updated = step_update_sok(data)
    print(f"      {sok_updated} söksidor uppdaterade")

    # Step 3: Update r-lista
    print("\n[3/5] Uppdaterar r-lista.js...")
    r_count = step_update_rlista(data)
    print(f"      {r_count} restaurangviner")

    # Step 4: Update admin INITIAL_DATA
    print("\n[4/5] Uppdaterar INITIAL_DATA i admin.html...")
    step_update_admin(data)
    print("      OK")

    # Step 5: Validate
    print("\n[5/5] Validerar...")
    errors, warnings, expected, sv_count, en_count = step_validate(data)

    if errors:
        print(f"\n  FEL ({len(errors)}):")
        for e in errors:
            print(f"    - {e}")

    if warnings:
        print(f"\n  VARNINGAR ({len(warnings)}):")
        for w in warnings[:10]:
            print(f"    - {w}")
        if len(warnings) > 10:
            print(f"    ... och {len(warnings) - 10} till")

    # Report
    print(f"\n{'=' * 60}")
    print(f"  RAPPORT")
    print(f"  Viner i databas:     {total_wines}")
    print(f"  Vinsidor (SV):       {sv_count}")
    print(f"  Vinsidor (EN):       {en_count}")
    print(f"  Förväntat:           {expected}")
    print(f"  Restaurangviner:     {r_count}")
    print(f"  Söksidor:            {sok_updated} uppdaterade")
    if errors:
        print(f"  FEL:                 {len(errors)}")
    if warnings:
        print(f"  VARNINGAR:           {len(warnings)}")
    if not errors:
        print(f"  Status:              OK")
    print(f"{'=' * 60}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
