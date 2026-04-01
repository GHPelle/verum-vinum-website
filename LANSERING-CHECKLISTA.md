# Lanseringsplan: Ny verumvinum.se

## Nuläge
- **Ny sida:** ghpelle.github.io/verum-vinum-website (GitHub Pages)
- **Gammal sida:** www.verumvinum.se (nuvarande live)
- **Admin:** ghpelle.github.io/verum-vinum-website/admin.html (lösenordsskyddad)

---

## Steg 1: Förberedelser (innan lansering)

### 1.1 Innehåll & Data
- [ ] Synka vindatabasen — exportera JSON från admin, uppdatera INITIAL_DATA
- [ ] Kontrollera att alla viner har korrekt data (priser, beskrivningar, bilder)
- [ ] Kontrollera att alla producenter har korrekt data i producentregistret
- [ ] Granska alla texter på samtliga sidor (svenska + engelska)
- [ ] Uppdatera kontaktuppgifter (telefonnummer, e-postadresser)
- [ ] Uppdatera event-tickern med aktuella event
- [ ] Kontrollera att R-listan (prislista) ser korrekt ut

### 1.2 Bilder
- [ ] Ersätt placeholder-bilder ("bild-kommer") med riktiga vinbilder
- [ ] Kontrollera att alla producentbilder visas korrekt
- [ ] Optimera bildstorlekar om någon är onödigt stor (>500KB)
- [ ] Kontrollera att teamfotot (Verumvinum.jpeg) visas under Om oss

### 1.3 Tekniskt
- [ ] Testa alla länkar — inga brutna länkar
- [ ] Testa alla undersidor: Hem, Systembolaget, Privatimport, Mat & Vin, Blogg, Sök
- [ ] Testa mobilversionen på iPhone (alla sidor)
- [ ] Testa språkväxling (Svenska ↔ Engelska)
- [ ] Testa söksidans filter och flerval
- [ ] Testa R-lista utskrift (svensk + engelsk)
- [ ] Kontrollera att admin-sidan fungerar på GitHub Pages
- [ ] Testa att "Prislista Restaurang"-knappen fungerar

### 1.4 SEO & Metadata
- [ ] Kontrollera `<title>` på alla sidor
- [ ] Lägg till meta description på alla sidor
- [ ] Kontrollera att `robots.txt` tillåter indexering (utom admin-sidor)
- [ ] Skapa `sitemap.xml` för sökmotorer
- [ ] Lägg till Open Graph-taggar (för delning på sociala medier)
- [ ] Kontrollera att favicon finns

---

## Steg 2: Domänkoppling

### Vad som behövs från dig (Per):
1. **Tillgång till DNS-inställningar** för verumvinum.se (var är domänen registrerad? Loopia, Binero, One.com, etc.?)
2. **Nuvarande hostingleverantör** — vem hostar www.verumvinum.se idag?

### Alternativ A: Peka domänen till GitHub Pages (rekommenderat)
Enklast och gratis. Steg:

1. **I GitHub-repot:** Skapa filen `CNAME` med innehållet `www.verumvinum.se`
2. **Hos din DNS-leverantör:** Ändra DNS-poster:
   - Ta bort befintlig A-post för verumvinum.se
   - Lägg till dessa A-poster:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```
   - Lägg till CNAME-post: `www` → `ghpelle.github.io`
3. **I GitHub Settings:** Aktivera custom domain + HTTPS

### Alternativ B: Egen hosting (Netlify/Cloudflare Pages)
Mer kontroll, snabbare CDN. Steg:
1. Koppla GitHub-repot till Netlify/Cloudflare Pages
2. Peka DNS dit istället
3. Automatisk deploy vid varje push

---

## Steg 3: Lanseringsdag

### Före (samma dag)
- [ ] Gör en sista synk av vindatabasen
- [ ] Kör `python3 build-from-db.py` för att generera alla sidor
- [ ] Pusha allt till GitHub
- [ ] Ta backup av gamla sidan (exportera/ladda ner allt)

### Under
- [ ] Ändra DNS-poster enligt Steg 2
- [ ] Vänta på DNS-propagering (kan ta 5 min — 48 timmar, oftast <1 timme)
- [ ] Testa www.verumvinum.se — ser du nya sidan?
- [ ] Testa HTTPS — fungerar certifikatet?
- [ ] Testa alla sidor med den riktiga domänen

### Efter
- [ ] Verifiera Google Search Console med nya sidan
- [ ] Skicka in sitemap.xml till Google
- [ ] Testa delning på sociala medier (Open Graph)
- [ ] Meddela kunder/partners om uppdaterad hemsida
- [ ] Övervaka under första veckan — kolla att inget är trasigt

---

## Steg 4: Efter lansering

### Löpande underhåll
1. **Vindata:** Redigera på admin.html → exportera JSON → synka → push
2. **Producenter:** Redigera på admin-producenter.html → exportera → synka → push
3. **Nya viner:** Lägg till i admin → lägg bild i images/viner/ → synka → push
4. **Event:** Uppdatera event-ticker i index.html + event-sektion
5. **Prislista:** Uppdateras automatiskt från vindatabasen via R-lista

### Framtida förbättringar (efter lansering)
- [ ] Koppla producentregistret till producentsidorna (automatisk generering)
- [ ] Bygga SB-lista och PI-lista utskrifter
- [ ] Google Analytics / Plausible Analytics
- [ ] Cookie-banner om analytics används
- [ ] Kontaktformulär
- [ ] Nyhetsbrev-integration

---

## Uppgifter jag behöver från dig

| Uppgift | Status |
|---------|--------|
| Var är domänen verumvinum.se registrerad? | |
| Inloggning till DNS-panelen | |
| Vem hostar gamla sidan? | |
| Vill du använda GitHub Pages eller annan hosting? | |
| Finns Google Search Console uppsatt? | |
| Ska gamla sidan vara tillgänglig som backup? | |
| Önskat lanseringsdatum? | |

---

*Dokument skapat 2026-03-31 — Verum Vinum Website Lansering*
