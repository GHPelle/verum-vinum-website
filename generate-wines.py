#!/usr/bin/env python3
"""Generate individual wine pages for all wines."""
import os, re, json

# Wine data: slug -> { name, producer, region, country, type, grapes, description }
wines = {
    # === ETTORE GERMANO ===
    "ettore-germano-alta-langa-extra-brut": {
        "name": "Alta Langa Extra Brut 2019",
        "producer": "Ettore Germano",
        "region": "Alta Langa, Piemonte",
        "country": "Italien",
        "type": "Mousserande",
        "grapes": "Pinot Noir, Chardonnay",
        "description": "En elegant mousserande från Alta Langa, framställd enligt metodo classico. Vinet vilar minst 36 månader på jästen vilket ger en komplex karaktär med fina bubblor, noter av brioche, citrus och gröna äpplen."
    },
    "ettore-germano-alta-langa-riserva-blanc-de-blanc-pas-dose": {
        "name": "Alta Langa Riserva Blanc de Blanc Pas Dosé",
        "producer": "Ettore Germano",
        "region": "Alta Langa, Piemonte",
        "country": "Italien",
        "type": "Mousserande",
        "grapes": "Chardonnay",
        "description": "En ren Chardonnay-baserad mousserande utan dosage. Lång lagring på jästen ger minerala toner, frisk syra och elegant komplexitet."
    },
    "ettore-germano-alta-langa-riserva-blanc-de-noir-pas-dose": {
        "name": "Alta Langa Riserva Blanc de Noir Pas Dosé",
        "producer": "Ettore Germano",
        "region": "Alta Langa, Piemonte",
        "country": "Italien",
        "type": "Mousserande",
        "grapes": "Pinot Noir",
        "description": "100% Pinot Noir framställd som blanc de noir utan dosage. Vinös karaktär med struktur och djup, fina bubblor och lång eftersmak."
    },
    "ettore-germano-rosanna-extra-brut-rose-metodo-classico": {
        "name": "Rosanna Extra Brut Rosé Metodo Classico",
        "producer": "Ettore Germano",
        "region": "Piemonte",
        "country": "Italien",
        "type": "Mousserande",
        "grapes": "Pinot Noir",
        "description": "En charmig rosé mousserande med vacker laxrosa färg, fina bubblor och smaker av jordgubbar, hallon och blodapelsin."
    },
    "ettore-germano-langhe-chardonnay": {
        "name": "Langhe Chardonnay 2023",
        "producer": "Ettore Germano",
        "region": "Langhe, Piemonte",
        "country": "Italien",
        "type": "Vitt",
        "grapes": "Chardonnay",
        "description": "En frisk och elegant Chardonnay från Langhe. Odlad på kalkrika jordar i Serralunga d'Alba med smaker av vit persika, citrus och en fin mineralitet."
    },
    "ettore-germano-binel-langhe-bianco": {
        "name": "Binel Langhe Bianco",
        "producer": "Ettore Germano",
        "region": "Langhe, Piemonte",
        "country": "Italien",
        "type": "Vitt",
        "grapes": "Chardonnay, Riesling",
        "description": "En unik blend av Chardonnay och Riesling som kombinerar fyllig frukt med frisk mineralitet. Lagras delvis på ekfat."
    },
    "ettore-germano-langhe-nascetta": {
        "name": "Langhe Nascetta 2021",
        "producer": "Ettore Germano",
        "region": "Langhe, Piemonte",
        "country": "Italien",
        "type": "Vitt",
        "grapes": "Nascetta",
        "description": "Nascetta är en sällsynt vit druva från Piemonte. Vinet visar aromatisk komplexitet med noter av vita blommor, örter och honung."
    },
    "ettore-germano-herzu-langhe-riesling": {
        "name": "Hérzu Langhe Riesling 2023",
        "producer": "Ettore Germano",
        "region": "Langhe, Piemonte",
        "country": "Italien",
        "type": "Vitt",
        "grapes": "Riesling",
        "description": "En av Italiens mest hyllade Riesling. Hérzu betyder 'sällsynt' på piemontesisk dialekt. Kristallklar mineralitet, eleganta citrusnyanser och lång eftersmak."
    },
    "ettore-germano-barbera-dalba-superiore": {
        "name": "Barbera d'Alba Superiore",
        "producer": "Ettore Germano",
        "region": "Alba, Piemonte",
        "country": "Italien",
        "type": "Rött",
        "grapes": "Barbera",
        "description": "En generös Barbera med rik fruktighet, mjuka tanniner och livlig syra. Lagras på stora ekfat vilket ger extra djup och komplexitet."
    },
    "ettore-germano-barolo-del-comune-di-serralunga-dalba": {
        "name": "Barolo del Comune di Serralunga d'Alba",
        "producer": "Ettore Germano",
        "region": "Serralunga d'Alba, Piemonte",
        "country": "Italien",
        "type": "Rött",
        "grapes": "Nebbiolo",
        "description": "En klassisk Barolo från Serralunga d'Alba, känd för sina kraftfulla och strukturerade viner. Doft av rosor, tjära och körsbär med fast tanninstruktur."
    },
    "ettore-germano-barolo-cerretta": {
        "name": "Barolo Cerretta 2019",
        "producer": "Ettore Germano",
        "region": "Serralunga d'Alba, Piemonte",
        "country": "Italien",
        "type": "Rött",
        "grapes": "Nebbiolo",
        "description": "Från den berömda vingården Cerretta i Serralunga d'Alba. Ett kraftfullt och elegant vin med djup fruktighet, komplexa kryddtoner och lång lagringskapacitet."
    },
    "ettore-germano-barolo-prapo": {
        "name": "Barolo Prapò",
        "producer": "Ettore Germano",
        "region": "Serralunga d'Alba, Piemonte",
        "country": "Italien",
        "type": "Rött",
        "grapes": "Nebbiolo",
        "description": "Prapò är en av Serralungas mest klassiska vingårdar. Vinet är elegant och strukturerat med noter av körsbär, lakrits, rosor och mineraler."
    },
    "ettore-germano-barolo-lazzarito-riserva": {
        "name": "Barolo Lazzarito Riserva",
        "producer": "Ettore Germano",
        "region": "Serralunga d'Alba, Piemonte",
        "country": "Italien",
        "type": "Rött",
        "grapes": "Nebbiolo",
        "description": "En Riserva från vingården Lazzarito med minst 5 års lagring. Majestetisk Barolo med enormt djup, komplexa aromor och exceptionell lagringskapacitet."
    },
    "ettore-germano-barolo-vignarionda": {
        "name": "Barolo Vigna Rionda",
        "producer": "Ettore Germano",
        "region": "Serralunga d'Alba, Piemonte",
        "country": "Italien",
        "type": "Rött",
        "grapes": "Nebbiolo",
        "description": "Vigna Rionda anses vara en av Barolos absolut finaste vingårdar. Ett monumentalt vin med oerhörd koncentration, elegans och lagringskapacitet på decennier."
    },

    # === FONTANABIANCA ===
    "fontanabianca-langhe-arneis-sommo": {
        "name": "Langhe Arneis \"Sommo\" 2023",
        "producer": "Fontanabianca",
        "region": "Neive, Piemonte",
        "country": "Italien",
        "type": "Vitt",
        "grapes": "Arneis",
        "description": "En frisk och aromatisk Arneis med noter av vita blommor, persika och mandel. Perfekt som aperitif eller till lätta fishrätter."
    },
    "fontanabianca-dolcetto-dalba": {
        "name": "Dolcetto d'Alba 2023",
        "producer": "Fontanabianca",
        "region": "Neive, Piemonte",
        "country": "Italien",
        "type": "Rött",
        "grapes": "Dolcetto",
        "description": "En fruktig och lättdrucken Dolcetto med smaker av mörka bär, plommon och en antydan av mandelbitterhet i avslutningen."
    },
    "fontanabianca-barbera-dalba-superiore": {
        "name": "Barbera d'Alba Superiore 2021",
        "producer": "Fontanabianca",
        "region": "Neive, Piemonte",
        "country": "Italien",
        "type": "Rött",
        "grapes": "Barbera",
        "description": "En Barbera med generös fruktighet och frisk syra. Lagras på ekfat vilket ger extra komplexitet och djup."
    },
    "fontanabianca-langhe-nebbiolo": {
        "name": "Langhe Nebbiolo",
        "producer": "Fontanabianca",
        "region": "Neive, Piemonte",
        "country": "Italien",
        "type": "Rött",
        "grapes": "Nebbiolo",
        "description": "En elegant och tillgänglig Nebbiolo med klassiska noter av rosor, körsbär och kryddor. Ett utmärkt insteg till Nebbiolons värld."
    },
    "fontanabianca-barbaresco": {
        "name": "Barbaresco",
        "producer": "Fontanabianca",
        "region": "Neive, Piemonte",
        "country": "Italien",
        "type": "Rött",
        "grapes": "Nebbiolo",
        "description": "Fontanabiancas klassiska Barbaresco från Neive. Elegant och parfymerad med fina tanniner och lång eftersmak."
    },
    "fontanabianca-barbaresco-bordini": {
        "name": "Barbaresco Bordini 2021",
        "producer": "Fontanabianca",
        "region": "Neive, Piemonte",
        "country": "Italien",
        "type": "Rött",
        "grapes": "Nebbiolo",
        "description": "Från den utvalda vingården Bordini i Neive. Mer komplex och djup än deras klassiska Barbaresco med noter av rosor, körsbär, lakrits och kryddor."
    },
    "fontanabianca-barbaresco-serraboella": {
        "name": "Barbaresco Serraboella 2020",
        "producer": "Fontanabianca",
        "region": "Neive, Piemonte",
        "country": "Italien",
        "type": "Rött",
        "grapes": "Nebbiolo",
        "description": "Serraboella är Fontanabiancas toppcru. Ett kraftfullt och elegant vin med komplexa aromor av rosor, violer, tjära och kryddor. Utomordentlig lagringskapacitet."
    },

    # === DIEGO MORRA ===
    "diego-morra-langhe-rosato": {
        "name": "Langhe Rosato 2022", "producer": "Diego Morra", "region": "Verduno, Piemonte", "country": "Italien", "type": "Rosé", "grapes": "Nebbiolo",
        "description": "En elegant rosé på Nebbiolo med vacker laxrosa färg och smaker av jordgubbar, citrus och örter."
    },
    "diego-morra-verduno-pelaverga": {
        "name": "Verduno Pelaverga 2023", "producer": "Diego Morra", "region": "Verduno, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Pelaverga",
        "description": "Pelaverga är en sällsynt druva som odlas nästan uteslutande i Verduno. Lätt och aromatisk med pepprighet och röda bär. Ett unikt vin."
    },
    "diego-morra-barolo-del-comune-di-verduno": {
        "name": "Barolo del Comune di Verduno", "producer": "Diego Morra", "region": "Verduno, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Nebbiolo",
        "description": "En elegant Barolo från Verduno med mjukare tanniner och floral elegans. Tillgänglig ung men med god lagringskapacitet."
    },
    "diego-morra-barolo-san-lorenzo": {
        "name": "Barolo San Lorenzo", "producer": "Diego Morra", "region": "Verduno, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Nebbiolo",
        "description": "Från den utvalda vingården San Lorenzo i Verduno. Komplex och djup med fina tanniner och lång eftersmak av rosor och kryddor."
    },
    "diego-morra-barolo-monvigliero": {
        "name": "Barolo Monvigliero", "producer": "Diego Morra", "region": "Verduno, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Nebbiolo",
        "description": "Monvigliero är en av Barolos mest hyllade vingårdar. Diegos kronjuvel – raffinerad, komplex och med otrolig elegans och djup."
    },

    # === ALBERTO OGGERO ===
    "alberto-oggero-valle-dei-lunghi": {"name": "Valle dei Lunghi", "producer": "Alberto Oggero", "region": "Roero, Piemonte", "country": "Italien", "type": "Vitt", "grapes": "Arneis", "description": "En frisk och mineralisk Arneis från Roero med noter av vita blommor, citrus och mandel."},
    "alberto-oggero-roero": {"name": "Roero Arneis", "producer": "Alberto Oggero", "region": "Roero, Piemonte", "country": "Italien", "type": "Vitt", "grapes": "Arneis", "description": "Klassisk Roero Arneis med elegant fruktighet och mineralitet som tydligt avspeglar terroiren."},
    "alberto-oggero-sandro-dpindeta": {"name": "Sandro d'Pindeta 2023", "producer": "Alberto Oggero", "region": "Roero, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Nebbiolo", "description": "En karaktärsfull Nebbiolo från Roero. Fruktdriven med mjuka tanniner, perfekt för vardagsdrickande."},
    "alberto-oggero-roero-2": {"name": "Roero", "producer": "Alberto Oggero", "region": "Roero, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Nebbiolo", "description": "Albertos Roero Nebbiolo – elegant och terroir-driven med klassiska noter av rosor, körsbär och kryddor."},

    # === RÉVA ===
    "reva-langhe-bianco-grey": {"name": "Langhe Bianco Grey", "producer": "Réva", "region": "Monforte d'Alba, Piemonte", "country": "Italien", "type": "Vitt", "grapes": "70% Sauvignon Gris, 30% Sauvignon Blanc", "description": "En väldigt unik vit blend för Piemonte. Aromatisk och komplex med exotisk frukt och mineraler."},
    "reva-dolcetto-dalba": {"name": "Dolcetto d'Alba", "producer": "Réva", "region": "Monforte d'Alba, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Dolcetto", "description": "Fruktdriven och lättdrucken Dolcetto med mörka bär och en fin bitterhet i avslutningen."},
    "reva-barbera-dalba-superiore": {"name": "Barbera d'Alba Superiore", "producer": "Réva", "region": "Monforte d'Alba, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Barbera", "description": "Generös Barbera med rik frukt, frisk syra och ekfatskaraktär."},
    "reva-nebbiolo-dalba": {"name": "Nebbiolo d'Alba", "producer": "Réva", "region": "Monforte d'Alba, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Nebbiolo", "description": "Drickbar direkt men klarar även lagring. Elegant Nebbiolo med rosor och körsbär."},
    "reva-barolo": {"name": "Barolo 2021", "producer": "Réva", "region": "Monforte d'Alba, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Nebbiolo", "description": "Révas klassiska Barolo – unik, exakt och tillverkad med respekt för druvorna och sin terroir. Drickbar direkt men klarar flera års lagring."},
    "reva-barolo-ravera": {"name": "Barolo Ravera", "producer": "Réva", "region": "Monforte d'Alba, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Nebbiolo", "description": "Från den eftertraktade vingården Ravera. Elegant och komplex med mineraler och lång eftersmak."},
    "reva-barolo-cannubi": {"name": "Barolo Cannubi", "producer": "Réva", "region": "Barolo, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Nebbiolo", "description": "Cannubi är kanske Barolos mest ikoniska vingård. Raffinerad, komplex och med fantastisk elegans."},

    # === LAPO BERTI ===
    "lapo-berti-langhe-nebbiolo": {"name": "Langhe Nebbiolo", "producer": "Lapo Berti", "region": "La Morra, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Nebbiolo", "description": "Lapos Langhe Nebbiolo – ren, ofiltrerad och med minimalt svavel. Elegant och terroir-driven."},
    "lapo-berti-barolo-del-comune-di-la-morra": {"name": "Barolo del Comune di La Morra", "producer": "Lapo Berti", "region": "La Morra, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Nebbiolo", "description": "En hantverksmässig Barolo från La Morra. Cirka 3500 flaskor produceras totalt. Ren och ofiltrerad."},
    "lapo-berti-barolo-fossati": {"name": "Barolo Fossati", "producer": "Lapo Berti", "region": "La Morra, Piemonte", "country": "Italien", "type": "Rött", "grapes": "Nebbiolo", "description": "Kronjuvelen – Barolo från den arrenderade vingården Fossati. Exceptionellt vin med enorm komplexitet och djup. Extremt begränsad produktion."},

    # === CIGLIANO DI SOPRA ===
    "cigliano-di-sopra-chianti-classico": {"name": "Chianti Classico 2022", "producer": "Cigliano di Sopra", "region": "San Casciano in Val di Pesa, Toscana", "country": "Italien", "type": "Rött", "grapes": "Sangiovese", "description": "Ekologisk Chianti Classico från unga vinmakare Matteo och Maddalena. Handskördad, naturlig jäst, 30% hela klasar. Ofiltrerat med minimalt svavel."},

    # === MORI CONCETTA ===
    "mori-concetta-morino-chianti-classico": {"name": "Morino Chianti Classico 2021", "producer": "Mori Concetta", "region": "San Casciano in Val di Pesa, Toscana", "country": "Italien", "type": "Rött", "grapes": "Sangiovese", "description": "Ekologiskt certifierad Chianti Classico i världsklass från en liten 1,2 hektars vingård. Noggrant utvalda rankor anpassade efter jordmån, klimat och vindar."},

    # === VILLA I CIPRESSI ===
    "villa-i-cipressi-rosso-di-montalcino": {"name": "Rosso di Montalcino", "producer": "Villa i Cipressi", "region": "Montalcino, Toscana", "country": "Italien", "type": "Rött", "grapes": "Sangiovese", "description": "Yngre brodern till Brunello. Fruktigare och mer tillgänglig men med samma kvalitativa grund. Sangiovese från två vingårdar i syd och väst Montalcino."},
    "villa-i-cipressi-brunello-di-montalcino": {"name": "Brunello di Montalcino", "producer": "Villa i Cipressi", "region": "Montalcino, Toscana", "country": "Italien", "type": "Rött", "grapes": "Sangiovese", "description": "Klassisk Brunello di Montalcino. Druvor från två vingårdar med helt annorlunda jordmån och mikroklimat blandas för att skapa ett rikare vin."},
    "villa-i-cipressi-zebras-brunello-di-montalcino": {"name": "Zebras Brunello di Montalcino", "producer": "Villa i Cipressi", "region": "Montalcino, Toscana", "country": "Italien", "type": "Rött", "grapes": "Sangiovese", "description": "Toppvinet – gjord på vingårdarnas allra bästa druvor. Koncentrerad och komplex med enorm lagringskapacitet."},

    # === VICTOR CHARLOT ===
    "victor-charlot-instinct-premier-5050": {"name": "Instinct Premier 50-50 NV", "producer": "Victor Charlot", "region": "Moussy, Champagne", "country": "Frankrike", "type": "Mousserande", "grapes": "50% Pinot Meunier, 50% Chardonnay", "description": "En balanserad Champagne med lika delar Pinot Meunier och Chardonnay. Jäst på ståltank utan malolaktisk jäsning. Frisk, elegant och terroir-driven."},
    "victor-charlot-instinct-premier-7525": {"name": "Instinct Premier 75-25 NV", "producer": "Victor Charlot", "region": "Moussy, Champagne", "country": "Frankrike", "type": "Mousserande", "grapes": "75% Pinot Meunier, 25% Chardonnay", "description": "Mer Meunier-dominerad med vinös karaktär och struktur, balanserad av Chardonnays elegans. Utan malolaktisk jäsning."},
    "victor-charlot-noirs-de-jais": {"name": "Noirs de Jais", "producer": "Victor Charlot", "region": "Moussy, Champagne", "country": "Frankrike", "type": "Mousserande", "grapes": "Pinot Meunier", "description": "100% Pinot Meunier blanc de noirs. Vinös och komplex med djup och karaktär."},
    "victor-charlot-les-terres-de-la-greve": {"name": "Les Terres de la Grève", "producer": "Victor Charlot", "region": "Moussy, Champagne", "country": "Frankrike", "type": "Mousserande", "grapes": "Pinot Meunier, Chardonnay", "description": "En platsspecifik Champagne som speglar terroiren i Les Terres de la Grève."},
    "victor-charlot-lapprivoisee": {"name": "L'Apprivoisée", "producer": "Victor Charlot", "region": "Moussy, Champagne", "country": "Frankrike", "type": "Mousserande", "grapes": "Pinot Meunier, Chardonnay", "description": "En unik cuvée med extra lagring och komplexitet. Victors nytänkande uttryck."},
    "victor-charlot-lart-de-la-ruse": {"name": "L'Art de la Ruse", "producer": "Victor Charlot", "region": "Moussy, Champagne", "country": "Frankrike", "type": "Mousserande", "grapes": "Pinot Meunier, Chardonnay", "description": "Victors senaste skapelse – en Champagne med karaktär och djup."},

    # === CHRISTIAN CLERGET ===
    "christian-clerget-bourgogne-rouge": {"name": "Bourgogne Rouge", "producer": "Domaine Christian Clerget", "region": "Vougeot, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Ekologisk Bourgogne Rouge. Ren Pinot Noir vinifierad utan tillsatt jäst. 18 månader på ekfat."},
    "christian-clerget-moreysaintdenis": {"name": "Morey-Saint-Denis", "producer": "Domaine Christian Clerget", "region": "Morey-Saint-Denis, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Eleganta Pinot Noir från Morey-Saint-Denis. Strukturerad och komplex med mörka bär och kryddor."},
    "christian-clerget-chambollemusigny": {"name": "Chambolle-Musigny", "producer": "Domaine Christian Clerget", "region": "Chambolle-Musigny, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Typisk Chambolle-Musigny med blommig elegans, silkiga tanniner och röda bär."},
    "christian-clerget-chambollemusigny-aux-croix": {"name": "Chambolle-Musigny Aux Croix", "producer": "Domaine Christian Clerget", "region": "Chambolle-Musigny, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Från lieu-dit Aux Croix. Mer djup och komplexitet än villages-nivån."},
    "christian-clerget-vosneromanee-les-violettes": {"name": "Vosne-Romanée Les Violettes", "producer": "Domaine Christian Clerget", "region": "Vosne-Romanée, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Från den poetiskt namngivna vingården Les Violettes. Vacker doft av violer, körsbär och kryddor."},
    "christian-clerget-chambollemusigny-1er-cru-les-charmes": {"name": "Chambolle-Musigny 1er Cru Les Charmes", "producer": "Domaine Christian Clerget", "region": "Chambolle-Musigny, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Premier Cru från Les Charmes – en av Chambolles finaste lägen. Silkig, komplex och med lång eftersmak."},
    "christian-clerget-vougeot-1er-cru-les-petits-vougeots": {"name": "Vougeot 1er Cru Les Petits Vougeots", "producer": "Domaine Christian Clerget", "region": "Vougeot, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Premier Cru från Vougeot. Strukturerad och djup med mörk frukt och jordiga toner."},
    "christian-clerget-echezeaux-grand-cru-en-orveaux": {"name": "Échezeaux Grand Cru En Orveaux", "producer": "Domaine Christian Clerget", "region": "Vosne-Romanée, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Grand Cru Échezeaux – familjens stolthet. Majestetisk Pinot Noir med enorm komplexitet, djup och lagringskapacitet."},

    # === COFFINET-DUVERNAY ===
    "coffinetduvernay-vin-de-france-assemblage": {"name": "Vin de France Assemblage", "producer": "Domaine Coffinet-Duvernay", "region": "Chassagne-Montrachet, Bourgogne", "country": "Frankrike", "type": "Vitt", "grapes": "Chardonnay", "description": "En tillgänglig och charmig Chardonnay-assemblage."},
    "coffinetduvernay-chassagnemontrachet-les-blanchots-dessous": {"name": "Chassagne-Montrachet Les Blanchots Dessous", "producer": "Domaine Coffinet-Duvernay", "region": "Chassagne-Montrachet, Bourgogne", "country": "Frankrike", "type": "Vitt", "grapes": "Chardonnay", "description": "Elegant Chassagne-Montrachet med mineralitet och citrusfrukt."},
    "coffinetduvernay-chassagnemontrachet-1er-cru-clos-saint-jean": {"name": "Chassagne-Montrachet 1er Cru Clos Saint Jean", "producer": "Domaine Coffinet-Duvernay", "region": "Chassagne-Montrachet, Bourgogne", "country": "Frankrike", "type": "Vitt", "grapes": "Chardonnay", "description": "Premier Cru med djup och komplexitet. Rik frukt balanserad av frisk syra."},
    "coffinetduvernay-chassagnemontrachet-1er-cru-dent-de-chien": {"name": "Chassagne-Montrachet 1er Cru Dent de Chien", "producer": "Domaine Coffinet-Duvernay", "region": "Chassagne-Montrachet, Bourgogne", "country": "Frankrike", "type": "Vitt", "grapes": "Chardonnay", "description": "Dent de Chien gränsar till Bâtard-Montrachet. Exceptionellt läge med koncentration och mineralitet."},
    "coffinetduvernay-chassagnemontrachet-1er-cru-les-caillerets": {"name": "Chassagne-Montrachet 1er Cru Les Caillerets", "producer": "Domaine Coffinet-Duvernay", "region": "Chassagne-Montrachet, Bourgogne", "country": "Frankrike", "type": "Vitt", "grapes": "Chardonnay", "description": "Les Caillerets – ett av Chassagnes mest hyllade lägen. Elegant och komplex."},
    "coffinetduvernay-chassagnemontrachet-1er-cru-les-grands-clos": {"name": "Chassagne-Montrachet 1er Cru Les Grands Clos", "producer": "Domaine Coffinet-Duvernay", "region": "Chassagne-Montrachet, Bourgogne", "country": "Frankrike", "type": "Vitt", "grapes": "Chardonnay", "description": "Generöst och rikt Premier Cru med bredare karaktär."},
    "coffinetduvernay-btardmontrachet-grand-cru": {"name": "Bâtard-Montrachet Grand Cru", "producer": "Domaine Coffinet-Duvernay", "region": "Chassagne-Montrachet, Bourgogne", "country": "Frankrike", "type": "Vitt", "grapes": "Chardonnay", "description": "Grand Cru Bâtard-Montrachet – en av världens finaste vita viner. Majestetisk koncentration, komplexitet och lagringskapacitet."},
    "coffinetduvernay-chassagnemontrachet-rouge": {"name": "Chassagne-Montrachet Rouge", "producer": "Domaine Coffinet-Duvernay", "region": "Chassagne-Montrachet, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Röd Chassagne-Montrachet – en ovanlig pärla. Elegant Pinot Noir med jordiga toner."},

    # === MICHEL REBOURGEON ===
    "michel-rebourgeon-beaune-les-epenottes": {"name": "Beaune Les Epenottes", "producer": "Domaine Michel Rebourgeon", "region": "Pommard, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Ekologisk Pinot Noir från Beaune. Elegant och fruktig med mjuka tanniner."},
    "michel-rebourgeon-pommard-cuvee-william": {"name": "Pommard Cuvée William", "producer": "Domaine Michel Rebourgeon", "region": "Pommard, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Williams personliga cuvée – elegant Pommard med fräschör och djup."},
    "michel-rebourgeon-pommard-les-noizons": {"name": "Pommard Les Noizons", "producer": "Domaine Michel Rebourgeon", "region": "Pommard, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Från lieu-dit Les Noizons i Pommard. Strukturerad och terroir-driven."},
    "michel-rebourgeon-pommard-trois-terroirs": {"name": "Pommard Trois Terroirs", "producer": "Domaine Michel Rebourgeon", "region": "Pommard, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "En assemblage av tre olika terroir i Pommard. Komplex och balanserad."},
    "michel-rebourgeon-beaune-1er-cru-les-chouacheux": {"name": "Beaune 1er Cru Les Chouacheux", "producer": "Domaine Michel Rebourgeon", "region": "Beaune, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Premier Cru från Beaune med fin elegans och silkiga tanniner."},
    "michel-rebourgeon-pommard-1er-cru-les-arvelets": {"name": "Pommard 1er Cru Les Arvelets", "producer": "Domaine Michel Rebourgeon", "region": "Pommard, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Premier Cru Les Arvelets – kraftfull och strukturerad Pommard."},
    "michel-rebourgeon-pommard-1er-cru-les-charmots": {"name": "Pommard 1er Cru Les Charmots", "producer": "Domaine Michel Rebourgeon", "region": "Pommard, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Les Charmots ger en mer charmig och elegant Pommard. Silkiga tanniner och lång eftersmak."},
    "michel-rebourgeon-pommard-1er-cru-les-rugiens": {"name": "Pommard 1er Cru Les Rugiens", "producer": "Domaine Michel Rebourgeon", "region": "Pommard, Bourgogne", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Les Rugiens är Pommards mest hyllade Premier Cru. Toppvinet – koncentrerat, djupt och med enorm lagringskapacitet."},

    # === LA FAMILLE K ===
    "la-famille-k-lheritiere": {"name": "L'Héritière Rouge 2024", "producer": "Domaine La Famille K", "region": "Morancé, Beaujolais", "country": "Frankrike", "type": "Rött", "grapes": "Gamay", "description": "Instegsvinet – fruktig och lättdrucken Gamay. Ekologiskt certifierad sedan 2022."},
    "la-famille-k-la-mere": {"name": "La Mère", "producer": "Domaine La Famille K", "region": "Morancé, Beaujolais", "country": "Frankrike", "type": "Rött", "grapes": "Gamay", "description": "Mellannivån i familjen. Mer struktur och djup än L'Héritière."},
    "la-famille-k-le-pere": {"name": "Le Père Rouge 2020", "producer": "Domaine La Famille K", "region": "Morancé, Beaujolais", "country": "Frankrike", "type": "Rött", "grapes": "Gamay", "description": "Mer komplex och lagringsduglig Gamay med extra djup och karaktär."},
    "la-famille-k-le-pere-blanc": {"name": "Le Père Blanc", "producer": "Domaine La Famille K", "region": "Morancé, Beaujolais", "country": "Frankrike", "type": "Vitt", "grapes": "Chardonnay", "description": "100% Chardonnay från Beaujolais. Frisk och elegant med citrusfrukt och mineralitet."},
    "la-famille-k-le-pere-vdf-pinot-noir": {"name": "Le Père VdF Pinot Noir 2022", "producer": "Domaine La Famille K", "region": "Morancé, Beaujolais", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "En ovanlig Pinot Noir från Beaujolais. Elegant och burgundisk i stilen."},
    "la-famille-k-loncle": {"name": "L'Oncle", "producer": "Domaine La Famille K", "region": "Morancé, Beaujolais", "country": "Frankrike", "type": "Rött", "grapes": "Gamaret", "description": "Den ovanliga druvan Gamaret – en korsning av Reichensteiner och Gamay. Unikt vin som bara finns som rött."},

    # === DOMAINE VILLET ===
    "domaine-villet-chardonnay-elevage-2-an-en-fut": {"name": "Chardonnay (élevage 2 an en fût)", "producer": "Domaine Villet", "region": "Arbois, Jura", "country": "Frankrike", "type": "Vitt", "grapes": "Chardonnay", "description": "Chardonnay lagrat 2 år på fat i Jura-tradition. Ekologiskt certifierad. Komplex med nötiga och fruktiga toner."},
    "domaine-villet-savagnin-ouille-elevage-24-mois-en-cuve": {"name": "Savagnin Ouillé (24 mois en cuve)", "producer": "Domaine Villet", "region": "Arbois, Jura", "country": "Frankrike", "type": "Vitt", "grapes": "Savagnin", "description": "Savagnin vinifierad ouillé (utan florhinna) i 24 månader på tank. Frisk och mineralisk."},
    "domaine-villet-savagnin-ouille-elevage-30-mois-en-foudre": {"name": "Savagnin Ouillé (30 mois en Foudre)", "producer": "Domaine Villet", "region": "Arbois, Jura", "country": "Frankrike", "type": "Vitt", "grapes": "Savagnin", "description": "Savagnin lagrat 30 månader på stor ek (foudre). Mer komplexitet och djup."},
    "domaine-villet-pinot-noir": {"name": "Pinot Noir", "producer": "Domaine Villet", "region": "Arbois, Jura", "country": "Frankrike", "type": "Rött", "grapes": "Pinot Noir", "description": "Elegant Pinot Noir från Jura. Ekologisk med lätt och fruktig karaktär."},
    "domaine-villet-poulsard": {"name": "Poulsard", "producer": "Domaine Villet", "region": "Arbois, Jura", "country": "Frankrike", "type": "Rött", "grapes": "Poulsard", "description": "Poulsard – Juras signaturduva. Ljus, delikat och transparent med röda bär och kryddor."},
    "domaine-villet-rouge-tradition": {"name": "Rouge Tradition", "producer": "Domaine Villet", "region": "Arbois, Jura", "country": "Frankrike", "type": "Rött", "grapes": "Poulsard, Pinot Noir, Trousseau", "description": "Traditionell Jura-blend av tre druvor. Komplex och terroir-driven."},

    # === CLOS DE LA BONNETTE ===
    "clos-de-la-bonnette-condrieu-legende-bonnetta": {"name": "Condrieu Légende Bonnetta", "producer": "Clos de la Bonnette", "region": "Condrieu, Norra Rhône", "country": "Frankrike", "type": "Vitt", "grapes": "Viognier", "description": "Condrieu från terrasser med utsikt över Rhône. Rik och aromatisk Viognier med aprikoser och blommor. Ekologisk."},
    "clos-de-la-bonnette-cisselande-vdf": {"name": "Cisselande VdF 2023", "producer": "Clos de la Bonnette", "region": "Norra Rhône", "country": "Frankrike", "type": "Rött", "grapes": "Syrah", "description": "En lättare Syrah från Norra Rhône. Fruktig och kryddig med fina tanniner."},
    "clos-de-la-bonnette-collines-rhodaniennes-syrah-vieilles-vignes": {"name": "Syrah Vieilles Vignes 2023", "producer": "Clos de la Bonnette", "region": "Norra Rhône", "country": "Frankrike", "type": "Rött", "grapes": "Syrah", "description": "Gamla rankor högst upp på berget. Koncentrerad Syrah med djup och komplexitet. Allt handskördat pga branta sluttningar."},
    "clos-de-la-bonnette-coterotie-prenelle": {"name": "Côte-Rôtie Prenelle", "producer": "Clos de la Bonnette", "region": "Côte-Rôtie, Norra Rhône", "country": "Frankrike", "type": "Rött", "grapes": "Syrah", "description": "Côte-Rôtie – en av Rhônedalens finaste appellationer. Komplex och elegant Syrah med enorm lagringskapacitet."},

    # === QUINTA DAS BÁGEIRAS ===
    "quinta-das-bagerias-espumante-colheita": {"name": "Espumante Colheita", "producer": "Quinta das Bágeiras", "region": "Sangalhos, Bairrada", "country": "Portugal", "type": "Mousserande", "grapes": "Baga", "description": "Traditionell mousserande utan restsocker. Handplockade druvor, producerat med traditionella metoder."},
    "quinta-das-bagerias-espumante-colheita-rose": {"name": "Espumante Colheita Rosé 2022", "producer": "Quinta das Bágeiras", "region": "Sangalhos, Bairrada", "country": "Portugal", "type": "Mousserande", "grapes": "Baga", "description": "Rosé mousserande utan restsocker. Elegant med röda bär och frisk syra."},
    "quinta-das-bagerias-vinho-branco-reserva": {"name": "Branco Reserva 2022", "producer": "Quinta das Bágeiras", "region": "Sangalhos, Bairrada", "country": "Portugal", "type": "Vitt", "grapes": "Bical, Maria Gomes", "description": "Vit Reserva från Bairrada med traditionella lokala druvor. Mineraler och citrusfrukt."},
    "quinta-das-bagerias-vinho-tinto-reserva": {"name": "Tinto Reserva 2021", "producer": "Quinta das Bágeiras", "region": "Sangalhos, Bairrada", "country": "Portugal", "type": "Rött", "grapes": "Baga", "description": "Kraftfull röd Reserva producerad i lagares utan tillsatt jäst. Traditionell Bairrada."},
    "quinta-das-bagerias-garrafeira-tinto": {"name": "Garrafeira Tinto 2018", "producer": "Quinta das Bágeiras", "region": "Sangalhos, Bairrada", "country": "Portugal", "type": "Rött", "grapes": "Baga", "description": "Toppvinet – Garrafeira med extra lagring. Komplex och djup med enorm lagringskapacitet."},
    "quinta-das-bagerias-abafado": {"name": "Abafado", "producer": "Quinta das Bágeiras", "region": "Sangalhos, Bairrada", "country": "Portugal", "type": "Starkvin", "grapes": "Baga", "description": "Traditionellt starkvin från Bairrada. Rikt och komplext med mörk frukt och kryddor."},

    # === VADIO ===
    "vadio-perpetuum-white-sparkling": {"name": "Perpetuum Sparkling NV", "producer": "Vadio", "region": "Poutena, Bairrada", "country": "Portugal", "type": "Mousserande", "grapes": "Cercial, Bical", "description": "Mousserande från Bairrada med traditionella druvor. Frisk och elegant med fina bubblor."},
    "vadio-rose-sparkling": {"name": "Rosé Sparkling Bruto 2020", "producer": "Vadio", "region": "Poutena, Bairrada", "country": "Portugal", "type": "Mousserande", "grapes": "Baga", "description": "Rosé mousserande på Baga-druvan. Elegant och fruktig."},
    "vadio-white": {"name": "White 2023", "producer": "Vadio", "region": "Poutena, Bairrada", "country": "Portugal", "type": "Vitt", "grapes": "Cercial, Bical", "description": "Friskt och mineraliskt vitt vin som tydligt avspeglar Bairradas terroir."},
    "vadio-red": {"name": "Red 2020", "producer": "Vadio", "region": "Poutena, Bairrada", "country": "Portugal", "type": "Rött", "grapes": "Baga", "description": "Klassisk röd Bairrada på Baga-druvan. Fruktdriven med kryddiga toner och fast tanninstruktur."},
    "vadio-grande": {"name": "Grande", "producer": "Vadio", "region": "Poutena, Bairrada", "country": "Portugal", "type": "Rött", "grapes": "Baga", "description": "Vadios toppvin. Koncentrerad Baga med enorm djup och komplexitet."},
    "vadio-rexarte": {"name": "Rexarte", "producer": "Vadio", "region": "Poutena, Bairrada", "country": "Portugal", "type": "Rött", "grapes": "Baga", "description": "Från gamla rankor. Komplex och terroir-driven med exceptionell lagringskapacitet."},

    # === QUINTA DO JAVALI ===
    "quinta-do-javali-crazy-branco": {"name": "Crazy Javali Branco", "producer": "Quinta do Javali", "region": "São João da Pesqueira, Douro", "country": "Portugal", "type": "Vitt", "grapes": "Fältblend", "description": "Lättsam och frisk vit från Douro. Syradriven med stor fräschör."},
    "quinta-do-javali-crazy-javali-tinto": {"name": "Crazy Javali Tinto", "producer": "Quinta do Javali", "region": "São João da Pesqueira, Douro", "country": "Portugal", "type": "Rött", "grapes": "Fältblend", "description": "Lättsamt rött – tillgängligt och fruktigt. Biodynamiskt odlat."},
    "quinta-do-javali-pet-nat": {"name": "Javali Pet Nat", "producer": "Quinta do Javali", "region": "São João da Pesqueira, Douro", "country": "Portugal", "type": "Mousserande", "grapes": "Fältblend", "description": "Naturlig mousserande pétillant naturel. Lekfull och ofiltrerad."},
    "quinta-do-javali-tinto": {"name": "Javali Tinto", "producer": "Quinta do Javali", "region": "São João da Pesqueira, Douro", "country": "Portugal", "type": "Rött", "grapes": "Fältblend", "description": "Elegant och syradriven röd Douro. Antonios filosofi – man ska känna växtplatsen."},
    "quinta-do-javali-clos-bonifata-2": {"name": "Clos Bonifata", "producer": "Quinta do Javali", "region": "São João da Pesqueira, Douro", "country": "Portugal", "type": "Rött", "grapes": "Fältblend", "description": "Från den enskilda vingården Clos Bonifata. Komplex och terroir-driven."},
    "quinta-do-javali-vinhas-dos-lobatos": {"name": "Vinhas dos Lobatos", "producer": "Quinta do Javali", "region": "São João da Pesqueira, Douro", "country": "Portugal", "type": "Rött", "grapes": "Fältblend", "description": "Från vingården Vinhas dos Lobatos. Djup och koncentrerad med stor fräschör."},
    "quinta-do-javali-clos-fonte-do-santo": {"name": "Clos Fonte do Santo", "producer": "Quinta do Javali", "region": "São João da Pesqueira, Douro", "country": "Portugal", "type": "Rött", "grapes": "Fältblend (30+ druvor)", "description": "Toppvinet – från den äldsta biodynamiska vingården med rankor upp till 90 år gamla och ett 30-tal olika druvor. Exceptionellt."},
    "quinta-do-javali-tawny-port": {"name": "Tawny Port", "producer": "Quinta do Javali", "region": "São João da Pesqueira, Douro", "country": "Portugal", "type": "Starkvin", "grapes": "Fältblend", "description": "Världens minsta producent av portvin. Lagrad uppe i Douro istället för Porto, vilket ger en mer utvecklad och knäckig karaktär."},
    "quinta-do-javali-tawny-port-10-year": {"name": "Tawny Port 10 Year", "producer": "Quinta do Javali", "region": "São João da Pesqueira, Douro", "country": "Portugal", "type": "Starkvin", "grapes": "Fältblend", "description": "10-årig Tawny från världens minsta portvinproducent. Komplex med nötter, torkad frukt och karamell."},

    # === MARTIN MÜLLEN ===
    "martin-mullen-riesling-revival-trocken": {"name": "Riesling Revival Trocken", "producer": "Weingut Martin Müllen", "region": "Traben-Trarbach, Mosel", "country": "Tyskland", "type": "Vitt", "grapes": "Riesling", "description": "Torr Riesling – frisk och mineralisk med citrus och gröna äpplen. Manuellt skördad."},
    "martin-mullen-nostel-trocken": {"name": "Nostel Trocken", "producer": "Weingut Martin Müllen", "region": "Traben-Trarbach, Mosel", "country": "Tyskland", "type": "Vitt", "grapes": "Riesling", "description": "Platsspecifik torr Riesling med mineralisk karaktär."},
    "martin-mullen-trabener-wurzgarten-spatlese-trocken": {"name": "Trabener Würzgarten Spätlese Trocken 2021", "producer": "Weingut Martin Müllen", "region": "Traben-Trarbach, Mosel", "country": "Tyskland", "type": "Vitt", "grapes": "Riesling", "description": "Spätlese-nivå Riesling från Würzgarten – torr med koncentrerad frukt och finess."},
    "martin-mullen-krover-paradies-spatlese-trocken": {"name": "Kröver Paradies Spätlese Trocken", "producer": "Weingut Martin Müllen", "region": "Traben-Trarbach, Mosel", "country": "Tyskland", "type": "Vitt", "grapes": "Riesling", "description": "Från vingården Kröver Paradies – torr Riesling med rik smakpalett och mineralitet."},
    "martin-mullen-trabener-wurzgarten-kabinett-feinherb": {"name": "Trabener Würzgarten Kabinett Feinherb", "producer": "Weingut Martin Müllen", "region": "Traben-Trarbach, Mosel", "country": "Tyskland", "type": "Vitt", "grapes": "Riesling", "description": "Halvtorr Kabinett med elegant balans mellan frukt och syra."},
    "martin-mullen-krover-letterlay-spatlese-feinherb": {"name": "Kröver Letterlay Spätlese Feinherb", "producer": "Weingut Martin Müllen", "region": "Traben-Trarbach, Mosel", "country": "Tyskland", "type": "Vitt", "grapes": "Riesling", "description": "Halvtorr Spätlese från Kröver Letterlay. Rik och komplex."},
    "martin-mullen-krover-kirchlay-auslese": {"name": "Kröver Kirchlay Auslese", "producer": "Weingut Martin Müllen", "region": "Traben-Trarbach, Mosel", "country": "Tyskland", "type": "Vitt", "grapes": "Riesling", "description": "Söt Auslese med koncentrerad frukt, honung och elegant syra."},
    "martin-mullen-trarbacher-huhnerberg-auslese": {"name": "Trarbacher Hühnerberg Auslese", "producer": "Weingut Martin Müllen", "region": "Traben-Trarbach, Mosel", "country": "Tyskland", "type": "Vitt", "grapes": "Riesling", "description": "Auslese från Hühnerberg – rik, komplex och med fantastisk balans mellan sötma och syra."},

    # === RUDI PICHLER ===
    "rudi-pichler-gruner-veltliner-terrassen-smaragd": {"name": "Grüner Veltliner Terrassen Smaragd 2023", "producer": "Rudi Pichler", "region": "Wosendorf, Wachau", "country": "Österrike", "type": "Vitt", "grapes": "Grüner Veltliner", "description": "Smaragd-nivå Grüner Veltliner – fyllig och komplex med vitpeppar, citrus och mineralitet."},
    "rudi-pichler-gruner-veltliner-kollmutz-smaragd": {"name": "Grüner Veltliner Kollmutz Smaragd", "producer": "Rudi Pichler", "region": "Wosendorf, Wachau", "country": "Österrike", "type": "Vitt", "grapes": "Grüner Veltliner", "description": "Från den enskilda vingården Kollmutz. Djup och koncentrerad med exceptionell mineralitet."},
    "rudi-pichler-gruner-veltliner-hochrain-smaragd": {"name": "Grüner Veltliner Hochrain Smaragd", "producer": "Rudi Pichler", "region": "Wosendorf, Wachau", "country": "Österrike", "type": "Vitt", "grapes": "Grüner Veltliner", "description": "Hochrain ger en mer kraftfull GV med djup och komplexitet."},
    "rudi-pichler-gruner-veltliner-achleithen-smaragd": {"name": "Grüner Veltliner Achleithen Smaragd", "producer": "Rudi Pichler", "region": "Wosendorf, Wachau", "country": "Österrike", "type": "Vitt", "grapes": "Grüner Veltliner", "description": "Achleithen – en av Wachaus grands crus. Majestetisk GV med enormt djup och precision."},
    "rudi-pichler-riesling-kirchweg-smaragd": {"name": "Riesling Kirchweg Smaragd", "producer": "Rudi Pichler", "region": "Wosendorf, Wachau", "country": "Österrike", "type": "Vitt", "grapes": "Riesling", "description": "Elegant Riesling från Kirchweg. Mineraler, citrus och stenfrukt med lång eftersmak."},
    "rudi-pichler-riesling-hochrain-smaragd": {"name": "Riesling Hochrain Smaragd", "producer": "Rudi Pichler", "region": "Wosendorf, Wachau", "country": "Österrike", "type": "Vitt", "grapes": "Riesling", "description": "Kraftfull Riesling från Hochrain med koncentration och djup."},
    "rudi-pichler-riesling-achleithen-smaragd": {"name": "Riesling Achleithen Smaragd", "producer": "Rudi Pichler", "region": "Wosendorf, Wachau", "country": "Österrike", "type": "Vitt", "grapes": "Riesling", "description": "Toppvinet – Achleithen Riesling. Precis, komplex och med enorm lagringskapacitet. Rudi vill alltid komplexitet framför koncentration."},
}

# Type colors
type_colors = {
    "Rött": ("bg-red-900/80", "text-red-100"),
    "Vitt": ("bg-amber-600/80", "text-amber-50"),
    "Rosé": ("bg-pink-400/80", "text-pink-50"),
    "Mousserande": ("bg-yellow-300/80", "text-yellow-900"),
    "Starkvin": ("bg-orange-800/80", "text-orange-100"),
}

template = '''<!DOCTYPE html>
<html lang="sv" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{producer} – {name} | Verum Vinum</title>
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
</head>
<body class="bg-cream-50 text-stone-800 font-sans antialiased">

  <!-- Nav -->
  <nav class="bg-wine-950 sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-6 lg:px-8 flex items-center justify-between h-16">
      <a href="../index.html" class="flex items-center gap-3">
        <img src="https://verumvinum.se/static/64/logo-2023.svg" alt="Verum Vinum" class="h-8 brightness-0 invert">
      </a>
      <a href="../index.html#sortiment" class="text-sm text-white/80 hover:text-white tracking-wider uppercase font-medium">&larr; Tillbaka</a>
    </div>
  </nav>

  <main class="max-w-4xl mx-auto px-6 lg:px-8 py-16">
    <!-- Breadcrumb -->
    <nav class="text-sm text-stone-400 mb-8">
      <a href="../index.html" class="hover:text-wine-600 transition-colors">Hem</a>
      <span class="mx-2">/</span>
      <a href="../index.html#producenter" class="hover:text-wine-600 transition-colors">{producer}</a>
      <span class="mx-2">/</span>
      <span class="text-stone-600">{name}</span>
    </nav>

    <div class="grid md:grid-cols-[1fr_1.5fr] gap-12 items-start">
      <!-- Wine visual -->
      <div class="bg-gradient-to-b from-stone-100 to-stone-50 rounded-2xl p-12 flex items-center justify-center min-h-[400px]">
        <div class="text-center">
          <div class="w-20 h-56 bg-gradient-to-b {bottle_gradient} rounded-t-full mx-auto shadow-lg"></div>
          <div class="w-12 h-3 bg-stone-400 mx-auto rounded-b"></div>
        </div>
      </div>

      <!-- Wine details -->
      <div>
        <span class="{type_bg} {type_text} px-3 py-1 rounded text-xs font-medium uppercase tracking-wider">{type}</span>
        <h1 class="font-serif text-4xl lg:text-5xl text-stone-900 mt-4 leading-tight">{name}</h1>
        <p class="text-wine-600 text-lg mt-2 font-medium">{producer}</p>

        <div class="mt-8 space-y-4">
          <div class="flex items-start gap-3">
            <svg class="w-5 h-5 text-wine-400 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            <div>
              <p class="text-stone-500 text-xs uppercase tracking-wider">Region</p>
              <p class="text-stone-800">{region}, {country}</p>
            </div>
          </div>
          <div class="flex items-start gap-3">
            <svg class="w-5 h-5 text-wine-400 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/></svg>
            <div>
              <p class="text-stone-500 text-xs uppercase tracking-wider">Druvor</p>
              <p class="text-stone-800">{grapes}</p>
            </div>
          </div>
        </div>

        <div class="mt-8 pt-8 border-t border-stone-200">
          <h2 class="font-serif text-xl text-stone-900 mb-3">Om vinet</h2>
          <p class="text-stone-600 leading-relaxed font-light text-lg">{description}</p>
        </div>

        <div class="mt-10 flex gap-4">
          <a href="../index.html#producenter" class="px-6 py-3 bg-wine-800 text-white font-medium text-sm uppercase tracking-wider hover:bg-wine-900 transition-colors">Alla producenter</a>
          <a href="../index.html#sortiment" class="px-6 py-3 border border-wine-800 text-wine-800 font-medium text-sm uppercase tracking-wider hover:bg-wine-50 transition-colors">Sortiment</a>
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

bottle_gradients = {
    "Rött": "from-red-900 to-red-950",
    "Vitt": "from-amber-200 to-amber-300",
    "Rosé": "from-pink-300 to-pink-400",
    "Mousserande": "from-amber-100 to-amber-200",
    "Starkvin": "from-amber-800 to-amber-900",
}

os.makedirs("sortiment", exist_ok=True)
count = 0
for slug, w in wines.items():
    tc = type_colors.get(w["type"], ("bg-stone-600", "text-stone-100"))
    bg = bottle_gradients.get(w["type"], "from-stone-400 to-stone-500")
    html = template.format(
        name=w["name"],
        producer=w["producer"],
        region=w["region"],
        country=w["country"],
        type=w["type"],
        grapes=w["grapes"],
        description=w["description"],
        type_bg=tc[0],
        type_text=tc[1],
        bottle_gradient=bg,
    )
    with open(f"sortiment/{slug}.html", "w") as f:
        f.write(html)
    count += 1

print(f"Generated {count} wine pages")
