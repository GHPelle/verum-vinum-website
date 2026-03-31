#!/usr/bin/env python3
"""
Build wine pages from wines-db.json.
Generates Swedish (sortiment/) and English (en/sortiment/) HTML pages
for each wine where websida=true.
"""

import json
import os
import re
from html import escape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "wines-db.json")
SV_DIR = os.path.join(BASE_DIR, "sortiment")
EN_DIR = os.path.join(BASE_DIR, "en", "sortiment")

# Type color mappings
TYPE_COLORS = {
    "Rött": ("bg-red-900/80", "text-red-100"),
    "Vitt": ("bg-amber-600/80", "text-amber-50"),
    "Rosé": ("bg-pink-400/80", "text-pink-50"),
    "Mousserande": ("bg-yellow-300/80", "text-yellow-900"),
    "Starkvin": ("bg-orange-800/80", "text-orange-100"),
}

# Gradient placeholders by type
TYPE_GRADIENTS = {
    "Rött": "from-red-900/20 to-red-800/10",
    "Vitt": "from-amber-100/40 to-amber-50/20",
    "Rosé": "from-pink-200/30 to-pink-100/10",
    "Mousserande": "from-yellow-100/30 to-yellow-50/10",
    "Starkvin": "from-orange-900/20 to-orange-800/10",
}


def load_existing_images():
    """Scan existing HTML files in sortiment/ for image URLs, keyed by slug."""
    images = {}
    if not os.path.isdir(SV_DIR):
        return images
    for fname in os.listdir(SV_DIR):
        if not fname.endswith(".html"):
            continue
        slug = fname[:-5]
        fpath = os.path.join(SV_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            m = re.search(r'<img src="(\.\./images/viner/[^"]+)"', content)
            if not m:
                m = re.search(r'<img src="(images/viner/[^"]+)"', content)
            if m:
                images[slug] = m.group(1)
        except Exception:
            pass
    return images


def esc(text):
    """HTML-escape a string, handling None."""
    if text is None:
        return ""
    return escape(str(text))


def build_image_html(slug, wine_type, existing_images, db_bild=None):
    """Return the wine visual div HTML."""
    # Prefer database bild field, then existing scan
    img_url = None
    if db_bild:
        img_url = f'../images/viner/{db_bild}'
    if not img_url:
        img_url = existing_images.get(slug)
    if img_url:
        return (
            f'      <div class="bg-gradient-to-b from-stone-100 to-stone-50 rounded-2xl p-8 flex items-center justify-center min-h-[400px]">\n'
            f'        <img src="{esc(img_url)}" alt="{esc(slug)}" class="max-h-[380px] object-contain drop-shadow-xl">\n'
            f'      </div>'
        )
    else:
        gradient = TYPE_GRADIENTS.get(wine_type, "from-stone-200/30 to-stone-100/10")
        return (
            f'      <div class="bg-gradient-to-b {gradient} rounded-2xl p-8 flex items-center justify-center min-h-[400px]">\n'
            f'        <div class="text-stone-300 text-center">\n'
            f'          <svg class="w-24 h-24 mx-auto mb-4 opacity-40" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>\n'
            f'          <p class="text-sm">Bild kommer</p>\n'
            f'        </div>\n'
            f'      </div>'
        )


def build_details_grid(wine, lang):
    """Build the details grid HTML, only including fields with values."""
    if lang == "sv":
        labels = {
            "alkohol": "Alkoholhalt",
            "jordman": "Jordmån",
            "hojd": "Höjd",
            "exponering": "Exponering",
            "alder_vinstockar": "Vinstockarnas ålder",
            "odling": "Odling",
            "serveringstemperatur": "Serverings&shy;temperatur",
            "argang": "Tillgängliga årgångar",
            "forslutningstyp": "Förslutning",
        }
    else:
        labels = {
            "alkohol": "Alcohol",
            "jordman": "Soil",
            "hojd": "Altitude",
            "exponering": "Exposure",
            "alder_vinstockar": "Vine age",
            "odling": "Farming",
            "serveringstemperatur": "Serving temperature",
            "argang": "Available vintages",
            "forslutningstyp": "Closure",
        }

    fields_order = [
        "alkohol", "jordman", "hojd", "exponering",
        "alder_vinstockar", "odling", "serveringstemperatur",
        "argang", "forslutningstyp",
    ]

    items = []
    for key in fields_order:
        val = wine.get(key, "")
        if val is None or str(val).strip() == "":
            continue
        label = labels.get(key, key)
        items.append(
            f'              <div>\n'
            f'                <p class="text-stone-400 text-xs uppercase tracking-wider mb-1 break-words" style="min-height: 2.5em; display: flex; align-items: flex-end;">{label}</p>\n'
            f'                <p class="text-stone-800 font-medium">{esc(str(val))}</p>\n'
            f'              </div>'
        )

    if not items:
        return ""

    return (
        f'            <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mt-6 p-6 bg-stone-50 rounded-xl">\n'
        + "\n".join(items) + "\n"
        f'            </div>'
    )


def build_page(wine, lang, existing_images):
    """Generate the full HTML for a wine page."""
    slug = wine["slug"]
    namn = wine.get("namn", "")
    producent = wine.get("producent", "")
    typ = wine.get("typ", "")
    region = wine.get("region", "")
    druvor = wine.get("druvor", "")
    om_vinet = wine.get("om_vinet", "")
    vinifiering = wine.get("vinifiering", "")
    matforslag = wine.get("matforslag", "")
    betyg = wine.get("betyg", "")

    bg_class, text_class = TYPE_COLORS.get(typ, ("bg-stone-600/80", "text-stone-100"))

    # Labels
    if lang == "sv":
        lbl_back = "&larr; Tillbaka"
        lbl_home = "Hem"
        lbl_region = "Region"
        lbl_grapes = "Druvor"
        lbl_about = "Om vinet"
        lbl_vinification = "Vinifikation"
        lbl_profile = "Vinets profil"
        lbl_pairs = "Passar till"
        lbl_ratings = "Betyg"
        lbl_all_producers = "Alla producenter"
        lbl_selection = "Sortiment"
        lbl_back_btn = "&larr; Tillbaka"
    else:
        lbl_back = "&larr; Back"
        lbl_home = "Home"
        lbl_region = "Region"
        lbl_grapes = "Grapes"
        lbl_about = "About the wine"
        lbl_vinification = "Vinification"
        lbl_profile = "Wine Profile"
        lbl_pairs = "Pairs with"
        lbl_ratings = "Ratings"
        lbl_all_producers = "All producers"
        lbl_selection = "Selection"
        lbl_back_btn = "&larr; Back"

    title = f"{esc(producent)} – {esc(namn)} | Verum Vinum"

    image_html = build_image_html(slug, typ, existing_images, wine.get('bild', ''))
    details_grid = build_details_grid(wine, lang)

    # Build optional sections
    vinification_html = ""
    if vinifiering and vinifiering.strip():
        vinification_html = (
            f'\n            <div class="mt-8">\n'
            f'              <h3 class="font-serif text-lg text-stone-900 mb-3">{lbl_vinification}</h3>\n'
            f'              <p class="text-stone-600 leading-relaxed font-light">{esc(vinifiering)}</p>\n'
            f'            </div>'
        )

    matforslag_html = ""
    if matforslag and matforslag.strip():
        matforslag_html = (
            f'\n            <div class="mt-6">\n'
            f'              <h3 class="font-serif text-lg text-stone-900 mb-3">{lbl_pairs}</h3>\n'
            f'              <p class="text-stone-600 leading-relaxed font-light">{esc(matforslag)}</p>\n'
            f'            </div>'
        )

    betyg_html = ""
    if betyg and betyg.strip():
        betyg_html = (
            f'\n            <div class="mt-6 p-4 bg-wine-50 rounded-lg">\n'
            f'              <h3 class="font-serif text-lg text-wine-900 mb-2">{lbl_ratings}</h3>\n'
            f'              <p class="text-wine-800 font-medium">{esc(betyg)}</p>\n'
            f'            </div>'
        )

    # Region and grapes section
    region_html = ""
    if region and region.strip():
        region_html = (
            f'          <div class="flex items-start gap-3">\n'
            f'            <svg class="w-5 h-5 text-wine-400 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>\n'
            f'            <div>\n'
            f'              <p class="text-stone-500 text-xs uppercase tracking-wider">{lbl_region}</p>\n'
            f'              <p class="text-stone-800">{esc(region)}</p>\n'
            f'            </div>\n'
            f'          </div>'
        )

    grapes_html = ""
    if druvor and druvor.strip():
        grapes_html = (
            f'          <div class="flex items-start gap-3">\n'
            f'            <svg class="w-5 h-5 text-wine-400 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/></svg>\n'
            f'            <div>\n'
            f'              <p class="text-stone-500 text-xs uppercase tracking-wider">{lbl_grapes}</p>\n'
            f'              <p class="text-stone-800">{esc(druvor)}</p>\n'
            f'            </div>\n'
            f'          </div>'
        )

    info_items = "\n".join(filter(None, [region_html, grapes_html]))

    # About section
    about_html = ""
    if om_vinet and om_vinet.strip():
        about_html = (
            f'        <div class="mt-8 pt-8 border-t border-stone-200">\n'
            f'          <h2 class="font-serif text-xl text-stone-900 mb-3">{lbl_about}</h2>\n'
            f'          <p class="text-stone-600 leading-relaxed font-light text-lg">{esc(om_vinet)}</p>\n'
            f'{details_grid}\n'
            f'{vinification_html}\n'
            f'{matforslag_html}\n'
            f'{betyg_html}'
        )
    else:
        # Even without om_vinet, show details grid etc. if they exist
        about_html = (
            f'        <div class="mt-8 pt-8 border-t border-stone-200">\n'
            f'{details_grid}\n'
            f'{vinification_html}\n'
            f'{matforslag_html}\n'
            f'{betyg_html}'
        )

    html = f'''<!DOCTYPE html>
<html lang="{"sv" if lang == "sv" else "en"}" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwindcss.config = {{
      theme: {{
        extend: {{
          colors: {{
            wine: {{ 50:'#fdf2f4', 100:'#fce7eb', 200:'#f9d0d9', 300:'#f5a9ba', 400:'#ee7895', 500:'#e44d73', 600:'#d12a5b', 700:'#b01e49', 800:'#8a1a3d', 900:'#6e1735', 950:'#3f0819' }},
            cream: {{ 50:'#fefdf8', 100:'#fdf9ed' }},
          }},
          fontFamily: {{
            serif: ['"Playfair Display"', 'Georgia', 'serif'],
            sans: ['"Inter"', 'system-ui', 'sans-serif'],
          }}
        }}
      }}
    }}
  </script>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    html {{ -webkit-tap-highlight-color: transparent; }}
    a, button {{ touch-action: manipulation; }}
    @media (max-width: 640px) {{
      .grid.grid-cols-2 {{ grid-template-columns: repeat(2, 1fr) !important; }}
    }}
  </style>
</head>
<body class="bg-cream-50 text-stone-800 font-sans antialiased">

  <!-- Nav -->
  <nav class="bg-wine-950 sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-6 lg:px-8 flex items-center justify-between h-16">
      <a href="../index.html" class="flex items-center gap-3">
        <img src="https://verumvinum.se/static/64/logo-2023.svg" alt="Verum Vinum" class="h-8 brightness-0 invert">
      </a>
      <a href="../index.html#sortiment" class="text-sm text-white/80 hover:text-white tracking-wider uppercase font-medium">{lbl_back}</a>
    </div>
  </nav>

  <main class="max-w-4xl mx-auto px-6 lg:px-8 py-16">
    <!-- Breadcrumb -->
    <nav class="text-sm text-stone-400 mb-8">
      <a href="../index.html" class="hover:text-wine-600 transition-colors">{lbl_home}</a>
      <span class="mx-2">/</span>
      <a href="../index.html#producenter" class="hover:text-wine-600 transition-colors">{esc(producent)}</a>
      <span class="mx-2">/</span>
      <span class="text-stone-600">{esc(namn)}</span>
    </nav>

    <div class="grid grid-cols-1 md:grid-cols-[1fr_1.5fr] gap-12 items-start">
      <!-- Wine visual -->
{image_html}

      <!-- Wine details -->
      <div>
        <span class="{bg_class} {text_class} px-3 py-1 rounded text-xs font-medium uppercase tracking-wider">{esc(typ)}</span>
        <h1 class="font-serif text-2xl sm:text-3xl md:text-4xl lg:text-5xl text-stone-900 mt-4 leading-tight">{esc(namn)}</h1>
        <p class="text-wine-600 text-lg mt-2 font-medium">{esc(producent)}</p>

        <div class="mt-8 space-y-4">
{info_items}
        </div>

{about_html}
        <div class="mt-10 flex flex-col sm:flex-row gap-4">
          <a href="../index.html#producenter" class="px-6 py-3 bg-wine-800 text-white font-medium text-sm uppercase tracking-wider hover:bg-wine-900 transition-colors">{lbl_all_producers}</a>
          <a href="javascript:history.back()" class="px-6 py-3 border border-wine-800 text-wine-800 font-medium text-sm uppercase tracking-wider hover:bg-wine-50 transition-colors cursor-pointer">{lbl_back_btn}</a>
        </div>
      </div>
    </div>
  </main>

  <footer class="bg-stone-900 text-stone-500 py-8 mt-16">
    <div class="max-w-4xl mx-auto px-6 text-center text-xs">
      <p>&copy; 2026 Verum Vinum Sverige AB</p>
    </div>
  </footer>
</body>
</html>'''

    return html


def main():
    # Load database
    with open(DB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    wines = data.get("wines", [])

    # Load existing image URLs from current HTML files
    existing_images = load_existing_images()
    print(f"Found {len(existing_images)} existing image URLs from current pages.")

    # Ensure output directories exist
    os.makedirs(SV_DIR, exist_ok=True)
    os.makedirs(EN_DIR, exist_ok=True)

    generated = 0
    skipped = 0

    for wine in wines:
        slug = wine.get("slug", "")
        websida = wine.get("websida", False)

        if not websida:
            skipped += 1
            continue

        if not slug:
            print(f"  WARNING: Wine '{wine.get('namn', '?')}' has websida=true but no slug, skipping.")
            skipped += 1
            continue

        # Generate Swedish page
        sv_html = build_page(wine, "sv", existing_images)
        sv_path = os.path.join(SV_DIR, f"{slug}.html")
        with open(sv_path, "w", encoding="utf-8") as f:
            f.write(sv_html)

        # Generate English page
        en_html = build_page(wine, "en", existing_images)
        en_path = os.path.join(EN_DIR, f"{slug}.html")
        with open(en_path, "w", encoding="utf-8") as f:
            f.write(en_html)

        generated += 1

    print(f"\n{'='*50}")
    print(f"  Pages generated: {generated} wines x 2 languages = {generated * 2} HTML files")
    print(f"  Wines skipped (websida=false or no slug): {skipped}")
    print(f"  Total wines in database: {len(wines)}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
