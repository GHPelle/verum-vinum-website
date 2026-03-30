#!/usr/bin/env python3
"""Update wine pages with full content from verumvinum.se"""
import os, re, json, html

wine_data = {
    # === BATCH A - Ettore Germano, Fontanabianca, Diego Morra, Alberto Oggero ===
    "ettore-germano-alta-langa-riserva-blanc-de-blanc-pas-dose": {
        "grapes": "Chardonnay", "alcohol": "12,5%", "soil": "Sand, Stenar", "altitude": "500-580 m ö.h.", "exposure": "Sydost, Sydväst", "vine_age": "13 år", "vintage": "2016",
        "vinification": "Druvorna skördas för hand och pressas i hela klasar. Druvorna jäser sedan en stund vid låg temperatur innan en del placeras i tonneaux och den andra delen i ståltank. Lagras sedan på jästfällningen i minst 65 månader och inget socker tillsätts.",
        "ratings": "James Suckling 92p, Robert Parker 94p, Jancis Robinson 17,5+p"
    },
    "ettore-germano-alta-langa-riserva-blanc-de-noir-pas-dose": {
        "grapes": "Pinot Noir", "alcohol": "12,5%", "soil": "Sand, Stenar", "altitude": "500-580 m ö.h.", "exposure": "Sydost, Sydväst", "vine_age": "15 år", "vintage": "2016",
        "vinification": "Druvorna skördas för hand och pressas i hela klasar. Druvorna jäser sedan en stund vid låg temperatur innan en del placeras i tonneaux och den andra delen i ståltank. Efter jäsning så får vinet vila ett tag tillsammans med sin jäst och kontinuerlig bâtonnage utförs. Lagras sedan på jästfällningen i minst 65 månader och inget socker tillsätts.",
        "ratings": "James Suckling 92p, Robert Parker 94p, Jancis Robinson 17+p"
    },
    "ettore-germano-rosanna-extra-brut-rose-metodo-classico": {
        "grapes": "Nebbiolo", "alcohol": "11,5%", "soil": "Kalksten, marmor och lite sand", "altitude": "300-400 m ö.h.", "vintage": "NV",
        "vinification": "Först pressas hela klasarna för att få ut tillräckligt extrakt till en ljusrosa nyans. Sedan selekterar man ut den bästa musten som sedan ska bli själva vinet. Första jäsningen sker på ståltank och den andra sker på flaska i minst 18 månader på jästfällningen.",
        "ratings": "Robert Parker 90p"
    },
    "ettore-germano-langhe-chardonnay": {
        "grapes": "100% Chardonnay", "alcohol": "12,5%", "soil": "Kalksten och kalkhaltig jord", "altitude": "450-500 m ö.h.",
        "vinification": "Efter druvorna pressats så placeras dom i en ståltank för att undergå jäsning i kontrollerad temperatur, 18°C. Genomgår sedan den malolaktiska jäsningen innan vinet lagras på ståltank i 6 månader."
    },
    "ettore-germano-binel-langhe-bianco": {
        "grapes": "Riesling Renano, Chardonnay", "alcohol": "14%", "soil": "Kalkjord med både kalksten och Langa stenar", "altitude": "450-550 m ö.h.", "vintage": "2017",
        "vinification": "Pressningen sker omedelbart via pneumatisk press för mjuk saftutvinning. Jäsningen påbörjas på ståltank, där en del lagras i medelstora ekfat under 6 månader medan resten stannar på ståltank. Efter blandning lagras vinet 6 månader på flaska före försäljning."
    },
    "ettore-germano-langhe-nascetta": {
        "grapes": "100% Nascetta", "alcohol": "13,5%", "soil": "Kalk, Kalksten, Stenar", "altitude": "500-560 m ö.h.", "exposure": "Sydost", "vine_age": "15 år",
        "vinification": "Druvorna skördas för hand och väl i vineriet så avstjälkas dom och krossas sedan lätt. Alkoholjäsningen sker i ståltank och vinet macererar i 10 dagar. Vinet lagras sedan på amfora i 8-10 månader innan det buteljeras.",
        "ratings": "James Suckling 90p"
    },
    "ettore-germano-barbera-dalba-superiore": {
        "grapes": "100% Barbera", "alcohol": "15%", "soil": "Lera och kalksten",
        "vinification": "Druvorna är handplockade och fraktade i små korgar. Väl i vineriet så avstjälkas dom och pressas lätt för att sedan genomgå jäsningen på ståltank. Macerationstiden är ca 10 dagar för att sedan lagras på medium stora ekfat i ungefär 1 år. Vinet tappas sedan på flaska och lagras på flaska 6 månader innan vinet släpps till försäljning.",
        "ratings": "Robert Parker 90p"
    },
    "ettore-germano-barolo-del-comune-di-serralunga-dalba": {
        "grapes": "100% Nebbiolo", "alcohol": "14,5%", "soil": "Lera, kalksten med vener av sand", "altitude": "330-400 m ö.h.", "exposure": "Syd, Ost", "vintage": "2018, 2019",
        "vinification": "Jäsningen genomförs i ståltank med macerationstid på 20-30 dagar. Vinet lagras sedan i olika storlekar ekfat under 18-24 månader, tappas på flaska och förvaras ytterligare 6 månader innan försäljning.",
        "profile": "Pumpig och energisk Barolo med doft av jordgubbar, körsbär, granatäpple och rosblad. Ljust röd färg med röd frukt och eleganta tanniner. Designad för tidig konsumtion.",
        "food": "Lämpar sig till lättare pastarätter, kyckling eller anka.",
        "ratings": "James Suckling 92p, Robert Parker 93p, Jancis Robinson 17++p, Wine Enthusiast 95p"
    },
    "ettore-germano-barolo-prapo": {
        "grapes": "100% Nebbiolo", "alcohol": "14,5%", "soil": "Lera och kalksten med vener av sand", "altitude": "330-370 m ö.h.", "exposure": "Sydost", "vintage": "2018, 2019",
        "vinification": "Druvorna är handplockade och fraktade i små korgar. Väl i vineriet så avstjälkas dom och pressas lätt för att sedan genomgå jäsningen på ståltank. Macerationstiden är mellan 40-45 dagar för att sedan lagras på \"botti grandi\" (2000-2500L ekfat) i 18-24 månader. Vinet tappas sedan på flaska och lagras på flaska 12 månader innan vinet släpps till försäljning.",
        "profile": "I glaset möts du av en granatröd färg med orangea reflektioner. Intensiva dofter av torkad frukt och vaniljtoner. Tack vare sanden så smyger det även in sig lite underliggande toner av söt röd frukt. Balansen mellan en potent och elegant Barolo är mitt i prick. Eftersmaken tillsammans med dom behagliga tanninerna är den perfekta avslutningen.",
        "food": "Passar väldigt bra ihop med den lokala cusinen eller lagrade ostar och torkad frukt.",
        "ratings": "James Suckling 92p, Robert Parker 94p, Jancis Robinson 17++p, Wine Enthusiast 96p"
    },
    "ettore-germano-barolo-lazzarito-riserva": {
        "grapes": "100% Nebbiolo", "alcohol": "14,5%", "soil": "Kalksten, margel, andel sand och järn", "altitude": "320-360 m ö.h.", "exposure": "Syd, Sydväst", "vine_age": "90 år", "vintage": "2015, 2017",
        "vinification": "Druvorna är handplockade och fraktade i små korgar. Druvorna avstjälkas och pressas för att sedan genomgå jäsningen på ståltank. Macerationstiden är mellan 50-60 dagar för att sedan lagras på botti (2000L ekfat) i 24-36 månader. Vinet tappas sedan på flaska och lagras på flaska innan vinet släpps till försäljning.",
        "profile": "Små röda bär med inslag av söt krydda och lakrits. Mjuk och sammetslent med stor elegans. En liten sötma i avslutet till tanninerna som dröjer sig kvar.",
        "food": "Utmärkt till kött och lagrade ostar.",
        "ratings": "James Suckling 96p, Robert Parker 95p, Jancis Robinson 17+p"
    },
    "ettore-germano-barolo-vignarionda": {
        "grapes": "100% Nebbiolo", "alcohol": "14%", "soil": "Kalkhaltig margel & lite sand", "altitude": "330 m ö.h.", "vintage": "2017",
        "vinification": "Handplockade druvor transporteras i små korgar. Efter pressning tillsammans med stjälken sker jäsning på ståltank med maceration mellan 30-40 dagar. Lagring sker på botti (2000L ekfat) i 18-24 månader, därefter på flaska i 20 månader före försäljning.",
        "profile": "Vinet beskrivs som kraftfullt med utsökt balans och struktur samt aromerna och finessen. Det representerar karaktären av en autentisk Serralunga-Barolo.",
        "food": "Passar till kötträtter, fyllda pastarätter och lagrade ostar.",
        "ratings": "James Suckling 95p, Robert Parker 94p, Jancis Robinson 17++p, Wine Enthusiast 97p"
    },
    "fontanabianca-langhe-arneis-sommo": {
        "grapes": "100% Arneis", "alcohol": "13%", "soil": "Lera och kalksten", "altitude": "300 m ö.h.", "vine_age": "ca 15 år", "serving_temp": "ca 12°C", "vintage": "2023",
        "vinification": "Druvorna pressas hela och man tar sedan bara vara på musten som jäser under lägre temperatur (ca 16 grader). Detta följs av 3 månaders bâtonnage i ståltank och 2 månader på flaska.",
        "profile": "Ett väldigt ungt och fräscht vin fyllt med frukt och blommor. Avnjuts lika väl som aperitif som till lättare rätter.",
        "ratings": "James Suckling 91p, Robert Parker 89p"
    },
    "fontanabianca-dolcetto-dalba": {
        "grapes": "100% Dolcetto", "alcohol": "13%", "soil": "Lera och kalksten", "altitude": "300 m ö.h.", "vine_age": "ca 25 år", "serving_temp": "ca 17-18°C",
        "vinification": "Jäsningen sker i ståltank under kontrollerad temperatur där även lagras i 3 månader. Sedan lagras det 3 månader i betongkar och till slut 6 månader på flaska.",
        "profile": "Ett klart fruktigt vin på doften fyllt med plommon och körsbär. Ett balanserat och harmoniskt vin med medium kropp. Torrt och runt som utan problem dricks väl till pizzan.",
        "ratings": "James Suckling 90p"
    },
    "fontanabianca-barbera-dalba-superiore": {
        "grapes": "100% Barbera", "alcohol": "14%", "soil": "Lera och kalksten", "altitude": "250 m ö.h.", "vine_age": "ca 30 år", "serving_temp": "ca 17-18°C", "vintage": "2021",
        "vinification": "Jäsningen sker i ståltank under kontrollerad temperatur och lagras sedan dels på stora ekfat och dels på barrique i 12-13 månader för att sedan lagras 6-8 månader på flaska.",
        "profile": "Doft av persika, plommon och körsbär. I munnen möts du av en superhärlig mineralitet och balanserad syra. En snygg Barbera helt enkelt.",
        "ratings": "James Suckling 91p, Robert Parker 91p"
    },
    "fontanabianca-langhe-nebbiolo": {
        "grapes": "100% Nebbiolo", "alcohol": "14%", "soil": "Lera och kalksten", "altitude": "300 m ö.h.", "vine_age": "ca 12 år", "serving_temp": "ca 18°C", "vintage": "2022",
        "vinification": "Jäsningen sker i ståltank under kontrollerad temperatur och lagras sedan på stora ekfat i 6 månader för att sedan lagras 6-8 månader på flaska.",
        "profile": "En ung och fräsch Nebbiolo som med fördel kan drickas ung med sina mjuka och härliga tanniner. Snyggt sammansatt med delikat rödfrukt och tydlig viol i doften.",
        "ratings": "James Suckling 90p, Robert Parker 91p"
    },
    "fontanabianca-barbaresco": {
        "grapes": "100% Nebbiolo", "alcohol": "14%", "soil": "Lera & kalksten", "altitude": "300 m ö.h.", "vine_age": "ca 30 år", "serving_temp": "ca 18°C", "vintage": "2020",
        "vinification": "Jäsningen sker i ståltank under kontrollerad temperatur i 30 dagar och lagras sedan dels på stora ekfat och dels på barrique i 15 månader, 2 månader på cementtank för att sedan lagras 8 månader på flaska.",
        "ratings": "James Suckling 93p, Robert Parker 93p, Wine Enthusiast 93p"
    },
    "fontanabianca-barbaresco-serraboella": {
        "grapes": "100% Nebbiolo", "alcohol": "14%", "soil": "Lera & kalksten", "altitude": "300 m ö.h.", "vine_age": "ca 15 år", "serving_temp": "ca 18°C",
        "vinification": "Jäsningen sker i ståltank under kontrollerad temperatur i 30 dagar och lagras sedan i stora ekfat i 15 månader, 2 månader på cementtank för att sedan lagras 8 månader på flaska.",
        "profile": "Ett harmoniskt vin gjort på Nebbiolo med toner av körsbär, kryddighet och viol. Mjuk och elegant med silkeslena tanniner och rödfrukt.",
        "ratings": "James Suckling 93p, Robert Parker 94+p, Wine Enthusiast 95p"
    },
    "diego-morra-langhe-rosato": {
        "grapes": "100% Nebbiolo", "alcohol": "13,5%",
        "vinification": "Handskördad och noggrant manuellt urval. Efter väldigt kort maceration för att få till en perfekt färgton får vinet jäsa på ståltank under temperaturkontroll där det aldrig överstiger 20°C i 25-30 dagar. Vinet lagras sedan i ståltank i 4-5 månader och avslutas med 2 månader på flaska.",
        "profile": "Det fina rosa vinet bjuder på en fantastisk fräschör! Den lilla restsötman som finns ger det en väldigt len känsla tillsammans med pigg rödfrukt och en krispig syra med superfräsch avslutning. Ett väldigt seriöst rosévin!", "vintage": "2022"
    },
    "diego-morra-barolo-del-comune-di-verduno": {
        "grapes": "100% Nebbiolo", "alcohol": "14,5%", "vintage": "2019",
        "vinification": "Druvor är handskördade med manuellt urval. Jäsningen och macerationen genomfördes i ståltank där temperaturen begränsades till högst 26°C under 25 dagar med daglig pumping over. Efter detta lagrades vinet på endast använda tonneauxer i 24 månader.",
        "profile": "Betydligt mer örtiga karaktärer och en liten rökighet med ett otroligt grepp i tanninerna och en otrolig fräschör samt långt avslut."
    },
    "diego-morra-barolo-san-lorenzo": {
        "grapes": "100% Nebbiolo", "alcohol": "14,5%", "vintage": "2019",
        "vinification": "Handskördad och noggrant manuellt urval. Jäsning och maceration sker i ståltank där temperaturen aldrig överstiger 26°C i 25 dagar med daglig pumping over. Vinet lagras sedan på franska ekfat där en del är nya och resten på sin andra passage i 24 månader.",
        "profile": "San Lorenzo visar upp en mer klassisk stil av Barolo. Intensiviteten i doften är lika påtaglig som Monvigliero men har mer struktur och fyllighet men fortfarande den typiska Verduno elegansen och fräschören."
    },
    "diego-morra-barolo-monvigliero": {
        "grapes": "100% Nebbiolo", "alcohol": "14,5%",
        "vinification": "Handskördad och noggrant manuellt urval. Jäsning och maceration i ståltank (max 30°C) under 30-35 dagar. Lagring på använda 25hL botti i 30 månader, sedan minst 6 månader på flaska.",
        "profile": "Intensiv och parfymerad doft med komplexitet från rosor, röda och mörka bär samt kryddighet. Strukturen är elegant med sammetslena tanniner och lång eftersmak.",
        "ratings": "Jancis Robinson 16,5p"
    },
    "alberto-oggero-valle-dei-lunghi": {
        "grapes": "100% Arneis", "alcohol": "13,5%", "soil": "Sand & Lera", "altitude": "320 m ö.h.", "exposure": "Sydväst", "vine_age": "ca 80 år", "serving_temp": "ca 12°C", "vintage": "2020",
        "vinification": "Druvorna handplockas och pressas för att sedan ligga med skalkontakt i 12 dagar. Vinet ligger sedan på cementtank där det genomgår alkohol- och malolaktiskjäsning och lagras sedan i 8-9 månader. Vinet får sedan vila några dagar på ståltank innan buteljering och ligger sedan 2 månader i flaskan.",
        "farming": "Ekologisk"
    },
    "alberto-oggero-roero": {
        "grapes": "100% Arneis", "alcohol": "13,5%", "soil": "Sandig", "altitude": "280 m ö.h.", "exposure": "Ost, Sydost", "vine_age": "ca 20 år", "serving_temp": "ca 12°C", "vintage": "2020",
        "vinification": "Druvorna handplockas och sedan krossas 50% av druvorna och ligger sedan 5 dagar med skalkontakt. Resterande 50% pressas men har ingen skalkontakt. Juicen delas sedan upp där 50% hamnar på använd botti och 50% delas upp på ståltank och cementtank där vinet går igenom alkohol- och malolaktiskjäsning och lagras sedan i 9 månader.",
        "farming": "Ekologisk"
    },
    "alberto-oggero-sandro-dpindeta": {
        "grapes": "100% Nebbiolo", "alcohol": "13,5%", "soil": "Sand", "altitude": "280 m ö.h.", "exposure": "Syd", "vine_age": "ca 20-25 år", "serving_temp": "ca 16°C",
        "vinification": "6-7 dagars maceration i ståltankar, lagring på cementtankar i 8-9 månader och 2 månader på flaska.",
        "farming": "Ekologisk"
    },
    "alberto-oggero-roero-2": {
        "grapes": "100% Nebbiolo", "alcohol": "14,5%", "soil": "Sand & lera", "altitude": "320 m ö.h.", "exposure": "Syd", "vine_age": "ca 30 år", "serving_temp": "ca 18°C",
        "vinification": "25 dagars maceration i ståltankar, lagring 10 månader i slavonska ekfat (tonneaux), 12 månader på flaska.",
        "farming": "Ekologisk"
    },
    # Remaining wines from other batches will be added below
}

# Add all remaining wine data from batches C, D, E
# (continuing with same structure)

more_data = {
    # === CLOS DE LA BONNETTE ===
    "clos-de-la-bonnette-condrieu-legende-bonnetta": {
        "grapes": "Viognier", "soil": "Granit", "farming": "Ekologisk", "vintage": "2023",
        "vinification": "Druvorna pressas direkt och juicen får sedan ligga i kyla i 48h innan vinet överförs via gravitationen till barriquer där vinet spontanjäser och lagras i 11-12 månader. Beroende på årgång utförs ibland bâtonnage och den malolaktiska jäsningen påbörjas direkt efter alkoholjäsningen. Buteljeras med en väldigt lätt filtrering.",
        "profile": "Légende Bonnetta görs av de äldsta rankorna och visar elegant och komplex Viognier med subtila toner av persika, aprikos, vita blommor och ibland exotisk frukt."
    },
    "clos-de-la-bonnette-cisselande-vdf": {
        "grapes": "Syrah, Grenache", "soil": "Granit", "farming": "Ekologisk", "vintage": "2023",
        "vinification": "Druvorna kommer från gården i Condrieu. Efter tre veckors maceration så får vinet jäsa färdigt i barriquer där det även lagras i 12 månader. Endast använda fat. Ingen jäst tillsätts utan jäsning startar spontant. Buteljeras sedan utan filtrering.",
        "profile": "Ett vin där Syrahen skiner igenom i eftersmaken och bjuder på fräsch mörk frukt och gryniga tanniner."
    },
    "clos-de-la-bonnette-collines-rhodaniennes-syrah-vieilles-vignes": {
        "grapes": "Syrah", "soil": "Gnejs, Skiffer", "farming": "Ekologisk", "vine_age": "45 år", "vintage": "2023",
        "vinification": "Druvorna kommer från Côte-Rôtie där vingården ligger högst upp på berget. Efter tre veckors maceration så får vinet jäsa färdigt i barriquer där det även lagras i 12 månader. Endast använda fat. Ingen jäst tillsätts utan jäsning startar spontant. Buteljeras sedan med en väldigt lätt filtrering.",
        "profile": "För att vara ett IGP vin så levererar det på fantastiskt hög nivå! Doft av mald peppar, vilda blommor och hallon. I munnen är vinet generöst genomsyrat av jordnära skogsfrukter, kryddor, torkade blommor och aromatiska örter. Smidiga men strukturerade mogna tanniner ger form åt vinet, medan en läcker mogen syra förde vinet vidare i gommen."
    },
    "clos-de-la-bonnette-coterotie-prenelle": {
        "grapes": "Syrah", "soil": "Gnejs, Skiffer", "farming": "Ekologisk", "vintage": "2022",
        "vinification": "Macerationen sker i ståltank i 3-4 veckor med både pumping over och punch down. I de flesta årgångar så avstjälkas samtliga druvor men vissa årgångar så behövs en del av stammarna. Jäsningen är spontan och efter maceration så flyttas vinet via gravitation till barriquer där vinet lagras i 2 år. Ingen filtrering.",
        "profile": "I doften hittar vi hallon med en ton av björnbär, viol och svartpeppar. I munnen upplevs vinet som väldigt slankt och elegant med en delikat struktur och balans. Frukten är utsökt och ger dig verkligen allt du vill ha från regionen."
    },
    # === VADIO ===
    "vadio-perpetuum-white-sparkling": {
        "grapes": "60% Bical, 30% Baga, 10% Cercial", "alcohol": "12,5%", "soil": "Mestadels lerkalksten", "serving_temp": "ca 8-10°C",
        "vinification": "Solera-metod. Varje del skördas individuellt och manuellt under tidig morgon. Därefter följer en försiktig press av de hela druvklasarna. Jäsningen sker i fat och lagringen på jäsningen pågår i cirka 6 månader. Under de första månaderna av det nya året tas cirka 30% av basvinet bort för att göra den nya 'tirage'. Andra jäsningen sker på flaska med minst 18 månaders lagring före degorgering.",
        "profile": "Doften har stor komplexitet och elegans. Den domineras av nötter, toner av kristalliserad/karamelliserad frukt och en liten härlig saltighet. Smaken är krämig och rik med en balanserad syra och mycket djup.",
        "ratings": "James Suckling 92p, Robert Parker 92p, Jancis Robinson 17p"
    },
    "vadio-rose-sparkling": {
        "grapes": "100% Baga", "alcohol": "11%", "soil": "Mestadels lerkalksten", "serving_temp": "ca 8-10°C", "vintage": "2020",
        "vinification": "Pressning sker av hela klasar med mycket mjuka extraktioner följs av jäsning uppdelat mellan rostfria ståltankar och använda ekfat. I februari görs den sista blandningen och 'tirage' sker. Efter att den andra jäsningen är klar åldras den på flaska i minst 18 månader innan degorgementet.",
        "profile": "Ljus laxfärgad och mycket tunna ihållande bubblor, doften visar massor av färska röda frukter. I munnen finns en fräschör baserat på en balanserad syra och samtidigt en krämig mousse-känsla.",
        "ratings": "James Suckling 92p, Robert Parker 90p, Jancis Robinson 16p"
    },
    "vadio-white": {
        "grapes": "Cercial, Bical", "alcohol": "13,5%", "soil": "Sandjord & lerkalksten", "serving_temp": "ca 8-12°C", "vintage": "2021",
        "vinification": "Druvorna skördas på morgonen, pressas i hela klasar och vinifieras separat. Cercial jäser i ståltankar för att behålla sin aromatiska egenskap, medan Bical-druvorna jäser i använda ekfat för att lägga till komplexitet och textur. Lagring separat i 6 månader innan de blandas och tappas på flaska.",
        "profile": "Doften har en till viss del intensiv citruskaraktär åtföljt av en liten saltig mineralitet. Smaken ger också syran som är typisk för Bical-druvan. Med en lång och behaglig eftersmak visar detta vin konsistensen och friskheten som är karaktäristiken hos de bästa vita vinerna i Bairrada.",
        "ratings": "James Suckling 91p, Robert Parker 91p"
    },
    "vadio-grande": {
        "grapes": "100% Baga", "alcohol": "13%", "soil": "Lerkalksten", "farming": "Ekologisk", "serving_temp": "ca 16-18°C",
        "vinification": "Varje del av skörden från de olika vingårdarna vinifieras i små delar var för sig med manuellt urval. Efter pressningen överförs vinet omedelbart till tidigare använda 500 liters ekfat där den malolaktiska jäsningen äger rum och där vinet sedan åldras i minst 12 månader. Detta vin tappas tidigare än Vadio Red för att bibehålla en högre halt av frukten.",
        "profile": "Doften avslöjar en hög koncentration av frukt där röda frukter och de typiska Baga balsamiska tonerna sticker ut. Smaken är balanserad med en komplexitet och elegans som domineras av mjuka och polerade tanniner och en mycket balanserad syra. Grande Vadio ger maximalt uttryck av Baga från Bairrada.",
        "ratings": "James Suckling 91p, Robert Parker 93+p"
    },
    "vadio-rexarte": {
        "grapes": "100% Baga", "alcohol": "13%", "soil": "Lerkalksten i en övergång till sandig kalkstensjord", "farming": "Ekologisk", "serving_temp": "ca 16-18°C", "exposure": "Norr", "vine_age": "0,3 hektar, ca 1300 flaskor",
        "vinification": "Vinifiering sker i små delar var för sig med manuellt urval, delvis med hela klasar. Strax efter att den alkoholhaltiga jäsningen är klar börjar lagringen i använda 500 liters franska ekfat.",
        "profile": "Doften avslöjar Bagas renhet, visar den mogna frukten och balsamiska toner. Smaken är den perfekta kombinationen av kraft och elegans, med stor balans och lång eftersmak. Rexarte förverkligar Vadios uppdrag att skydda Baga-druvans terroir och rena uttryck.",
        "ratings": "James Suckling 91p, Robert Parker 95p"
    },
    # === QUINTA DO JAVALI ===
    "quinta-do-javali-crazy-branco": {
        "grapes": "Arinto, Viosinho, Rabigato, Encruzado, Gouveio, Cercial", "alcohol": "12%", "soil": "Skiffer och granit", "altitude": "600 m ö.h.", "farming": "Biodynamisk", "vintage": "2023",
        "vinification": "Spontanjäsning med naturlig jäst i ståltank med 1 veckas maceration. Pressas sedan och jäser klart i ståltank för att sedan lagras 6 månader i ståltank med jästfällningen följt av 6 månader i använda franska 500L ekfat."
    },
    "quinta-do-javali-crazy-javali-tinto": {
        "grapes": "Tinta Roriz, Tinta Barroca, Touriga Franca", "alcohol": "12,5%", "soil": "Skiffer och granit", "altitude": "300-500 m ö.h.", "farming": "Biodynamisk", "vintage": "2023",
        "vinification": "Spontanjäsning med naturlig jäst i cementtank och lagras sedan ett år i använda franska 500L ekfat."
    },
    "quinta-do-javali-pet-nat": {
        "grapes": "Tinta Roriz, Tinta Barroca, Touriga Franca", "alcohol": "10,5%", "soil": "Skiffer och granit", "altitude": "300-500 m ö.h.", "farming": "Biodynamisk", "vintage": "2023",
        "vinification": "Spontanjäsning med naturlig jäst i ståltank och buteljeras innan jäsningen är färdig och får sedan jäsa klart på flaska."
    },
    "quinta-do-javali-tinto": {
        "grapes": "Tinta Roriz, Tinta Barroca, Touriga Franca, Touriga Nacional", "alcohol": "12,5%", "soil": "Skiffer och granit", "altitude": "300-500 m ö.h.", "farming": "Biodynamisk", "vintage": "2023",
        "vinification": "Spontanjäsning med naturlig jäst i cementtank och lagras sedan ett år i använda franska ekfat à 500L."
    },
    "quinta-do-javali-clos-bonifata-2": {
        "grapes": "Arinto, Viosinho", "alcohol": "12,5%", "soil": "Skiffer, granit", "altitude": "600 m ö.h.", "farming": "Biodynamisk", "vine_age": "25+ år", "vintage": "2023",
        "vinification": "Spontanjäsning med naturlig jäst i cementtank och lagras sedan ett år i cementtank tillsammans med sin jästfällning."
    },
    "quinta-do-javali-vinhas-dos-lobatos": {
        "grapes": "Field blend", "alcohol": "13,5%", "soil": "Skiffer", "altitude": "380 m ö.h.", "farming": "Biodynamisk", "vine_age": "60+ år", "vintage": "2023",
        "vinification": "Spontanjäsning med naturlig jäst i cementtank och lagras sedan ett år i använda franska 500L ekfat."
    },
    "quinta-do-javali-tawny-port": {
        "grapes": "Tinta Roriz, Touriga Franca, Touriga Nacional, Tinto Cão, Tinta Barroca", "alcohol": "19,5%", "soil": "Skiffer, granit", "farming": "Ekologisk",
        "vinification": "Klasarna avstjälkas inte och pressas genom trampning. Lagras minst 5 år på ekfat."
    },
    "quinta-do-javali-tawny-port-10-year": {
        "grapes": "Tinta Roriz, Touriga Franca, Touriga Nacional, Tinto Cão, Tinta Barroca", "alcohol": "19,5%", "soil": "Skiffer, granit", "farming": "Ekologisk",
        "vinification": "Klasarna avstjälkas inte och pressas genom trampning. Lagras minst 10 år på ekfat."
    },
    # === MARTIN MÜLLEN ===
    "martin-mullen-riesling-revival-trocken": {
        "grapes": "100% Riesling", "alcohol": "12%", "soil": "Skiffer",
        "vinification": "Druvorna skördas i de branta sluttningarna för hand och väljs noggrant ut. Druvorna placeras sedan i en gammal traditionell press där man varsamt pressar druvorna i ca 20 timmar precis som man gjorde för 100 år sedan. Genom att pressa druvorna sakta så låter du druvorna och skalen ge ifrån sig sin totala potential av smak och aromer. Du får även med de fina tanninerna som ger vinet karaktär, längd och lagringspotential. Efter pressningen så får juicen spontanjäsa på stora ekfat med enbart sin naturliga jäst."
    },
    "martin-mullen-nostel-trocken": {
        "grapes": "100% Riesling", "alcohol": "13,5%", "soil": "Skiffer", "vintage": "2019",
        "vinification": "Druvorna skördas i de branta sluttningarna för hand och väljs noggrant ut. Druvorna placeras sedan i en gammal traditionell press där man varsamt pressar druvorna i ca 20 timmar. Efter pressningen så får juicen spontanjäsa på stora ekfat med enbart sin naturliga jäst.",
        "ratings": "James Suckling 97p"
    },
    "martin-mullen-trabener-wurzgarten-kabinett-feinherb": {
        "grapes": "100% Riesling", "alcohol": "10,5%", "soil": "Skiffer",
        "vinification": "Druvorna skördas i de branta sluttningarna för hand och väljs noggrant ut. Druvorna placeras sedan i en gammal traditionell press där man varsamt pressar druvorna i ca 20 timmar. Efter pressningen så får juicen spontanjäsa på stora ekfat med enbart sin naturliga jäst."
    },
    "martin-mullen-krover-paradies-spatlese-trocken": {
        "grapes": "100% Riesling", "alcohol": "12,5%", "soil": "Skiffer", "vintage": "2019",
        "vinification": "Druvorna skördas i de branta sluttningarna för hand och väljs noggrant ut. Druvorna placeras sedan i en gammal traditionell press där man varsamt pressar druvorna i ca 20 timmar. Efter pressningen så får juicen spontanjäsa på stora ekfat med enbart sin naturliga jäst."
    },
    "martin-mullen-krover-letterlay-spatlese-feinherb": {
        "grapes": "100% Riesling", "alcohol": "13,5%", "soil": "Skiffer", "vintage": "2019",
        "vinification": "Druvorna skördas i de branta sluttningarna för hand och väljs noggrant ut. Druvorna placeras sedan i en gammal traditionell press där man varsamt pressar druvorna i ca 20 timmar. Efter pressningen så får juicen spontanjäsa på stora ekfat med enbart sin naturliga jäst.",
        "ratings": "James Suckling 92p"
    },
    "martin-mullen-krover-kirchlay-auslese": {
        "grapes": "100% Riesling", "alcohol": "8,5%", "soil": "Skiffer", "vintage": "2019",
        "vinification": "Druvorna skördas i de branta sluttningarna för hand och väljs noggrant ut. Druvorna placeras sedan i en gammal traditionell press där man varsamt pressar druvorna i ca 20 timmar. Efter pressningen så får juicen spontanjäsa på stora ekfat med enbart sin naturliga jäst.",
        "ratings": "James Suckling 94p, Robert Parker 95p"
    },
    "martin-mullen-trarbacher-huhnerberg-auslese": {
        "grapes": "100% Riesling", "alcohol": "9,5%", "soil": "Skiffer", "vintage": "2019",
        "vinification": "Druvorna skördas i de branta sluttningarna för hand och väljs noggrant ut. Druvorna placeras sedan i en gammal traditionell press där man varsamt pressar druvorna i ca 20 timmar. Efter pressningen så får juicen spontanjäsa på stora ekfat med enbart sin naturliga jäst.",
        "ratings": "James Suckling 95p, Robert Parker 96p"
    },
    # === RUDI PICHLER ===
    "rudi-pichler-gruner-veltliner-kollmutz-smaragd": {
        "grapes": "100% Grüner Veltliner", "alcohol": "13,5%", "soil": "Primära bergarter, gnejs", "vine_age": "40+ år", "vintage": "2022",
        "vinification": "Druvorna skördas för hand och väljs noggrant ut och pressas sedan genom fottrampning för en mjukare pressning som utlöser naturliga enzymer. Vinet macererar i 18 timmar och jäser sedan på ståltank i 18-22°C.",
        "profile": "Vinstockarna är djupt rotade på branta stenterrasser och är mer än 40 år gamla. Detta frambringar viner som kännetecknas av en tydlig mineralitet i kombination med komplexa fruktaromer.",
        "ratings": "James Suckling 97p"
    },
    "rudi-pichler-gruner-veltliner-hochrain-smaragd": {
        "grapes": "100% Grüner Veltliner", "alcohol": "13%", "soil": "Primära bergarter, gnejs, lösjord", "vine_age": "40+ år", "vintage": "2022",
        "vinification": "Druvorna skördas för hand och väljs noggrant ut och pressas sedan genom fottrampning. Vinet macererar i 12 timmar och jäser sedan på ståltank i 18-22°C.",
        "profile": "Vinrankor så gamla som 50 år på jordar av väderbitna urbergarter, delvis täckta med lösjord, ger en extraktrik, djup och arketypisk Veltliner.",
        "ratings": "James Suckling 96p"
    },
    "rudi-pichler-gruner-veltliner-achleithen-smaragd": {
        "grapes": "100% Grüner Veltliner", "alcohol": "13%", "soil": "Primära bergarter, gnejs", "vine_age": "50+ år", "vintage": "2022",
        "vinification": "Druvorna skördas för hand och väljs noggrant ut och pressas sedan genom fottrampning. Vinet macererar i 18 timmar och jäser sedan på ståltank i 18-22°C.",
        "profile": "Dessa mer än 50 år gamla vinstockar växer på branta, sydvästexponerade terrasser, planterade i Gföhler gnejs, och producerar en djupt mineraldriven och puristisk Grüner Veltliner.",
        "ratings": "James Suckling 98p"
    },
    "rudi-pichler-riesling-kirchweg-smaragd": {
        "grapes": "100% Riesling", "alcohol": "13%", "soil": "Primära bergarter, gnejs, sand", "vine_age": "20-40+ år", "vintage": "2022",
        "vinification": "Druvorna skördas för hand och väljs noggrant ut och pressas sedan genom fottrampning. Vinet macererar i 12 timmar och jäser sedan på ståltank i 18-22°C.",
        "profile": "Från en vingård som först officiellt nämndes på 1100-talet. Beläget vid foten av Hochrain, påverkas marken av nedsköljda sediment och stenar från vingården ovan, vilket ger viner med en tät mineraldriven textur och raffinerade fruktaromer.",
        "ratings": "James Suckling 98p"
    },
    "rudi-pichler-riesling-hochrain-smaragd": {
        "grapes": "100% Riesling", "alcohol": "13%", "soil": "Primära bergarter, gnejs, lösjord", "vine_age": "20-40+ år", "vintage": "2022",
        "vinification": "Druvorna skördas för hand och väljs noggrant ut och pressas sedan genom fottrampning. Vinet macererar i 12 timmar och jäser sedan på ståltank i 18-22°C.",
        "profile": "Vinrankor upp till 40 år gamla ger råvaran för denna delikat fruktdrivna och mångfacetterade Riesling, som uppvisar en mineralitet som är typisk för denna topplats i Wösendorf.",
        "ratings": "James Suckling 97p"
    },
    # === COFFINET-DUVERNAY ===
    "coffinetduvernay-chassagnemontrachet-les-blanchots-dessous": {
        "grapes": "Chardonnay", "farming": "Ekologisk", "vine_age": "50+ år", "vintage": "2022",
        "vinification": "Skörden sker för hand och selektering sker redan ute i vingården. Druvorna hålls direkt i en pneumatisk press som försiktigt pressar druvorna i 2 timmar vid ett tryck på 2 bar. Juicen överförs till rostfritt stål första natten före sedimentering. Därefter lagras vinet på ekfat med inhemsk jäst i 12 månader, följt av 2 månader i ståltank före buteljering. Ingen filtrering.",
        "profile": "Vingården ligger på en utmärkt plats där den drar nytta av sin terroir. Vinerna är alltid magnifika och med stor komplexitet."
    },
    "coffinetduvernay-chassagnemontrachet-1er-cru-clos-saint-jean": {
        "grapes": "Chardonnay", "farming": "Ekologisk", "vine_age": "50+ år",
        "vinification": "Handplock och druvselektering i vingården. Druvorna pressas pneumatiskt i 2 timmar vid 2 bar tryck. Lagring i ekfat för jäsning med inhemsk jäst. Lagring på fat i 16-18 månader, sedan 2 månader i ståltank före buteljering. Ingen filtrering.",
        "profile": "Denna 1er Cru ligger högt upp i Chassagne-Montrachet som generellt sett är mer känd för sina röda viner. Men Chardonnay planterad här ger blommiga och lättare vita viner."
    },
    "coffinetduvernay-chassagnemontrachet-1er-cru-dent-de-chien": {
        "grapes": "Chardonnay", "farming": "Ekologisk", "vintage": "2022",
        "vinification": "Skörden sker för hand och selektering sker redan ute i vingården. Druvorna hålls direkt i en pneumatisk press som försiktigt pressar druvorna i 2 timmar vid ett tryck på 2 bar. Lagring på ekfat med inhemsk jäst under 16-18 månader, därefter 2 månader i ståltank före buteljering. Ingen filtrering.",
        "profile": "Vingården ligger i förlängningen av Montrachet, precis ovanför och är på samma nivå som Grand Cru Chevalier-Montrachet. Jorden är grund, och exponeringen mot söder gör att vinstockarna värms snabbt. Detta ger ett mycket mineraliskt och moget vin."
    },
    "coffinetduvernay-chassagnemontrachet-1er-cru-les-caillerets": {
        "grapes": "Chardonnay", "soil": "Stenig jord", "farming": "Ekologisk", "vine_age": "80+ år", "vintage": "2022",
        "vinification": "Manuell skörd med druvor pressade försiktigt i pneumatisk press. Jäsning sker med inhemsk jäst i ekfat. Lagring på fat i 16-18 månader, sedan i ståltank 2 månader före buteljering. Ingen filtrering.",
        "profile": "Denna 1er Cru ligger på höjden av byn, närmare bestämt på platsen som kallas 'Les Combards'. Mycket stenig jord med gamla vinstockar omkring 80 år gamla."
    },
    "coffinetduvernay-chassagnemontrachet-1er-cru-les-grands-clos": {
        "grapes": "Chardonnay", "farming": "Ekologisk",
        "vinification": "Skörden sker för hand och selektering sker redan ute i vingården. Druvorna hålls direkt i en pneumatisk press som försiktigt pressar druvorna i 2 timmar vid ett tryck på 2 bar. Lagring på ekfat under 16-18 månader och sedan i ståltank i 2 månader före buteljering. Ingen filtrering.",
        "profile": "Les Grands Clos är ett något rått, rikt och köttigt vin som kommer kräva sin lagring för att verkligen visa sin fulla potential."
    },
    "coffinetduvernay-btardmontrachet-grand-cru": {
        "grapes": "Chardonnay", "soil": "Mager stenig jord", "farming": "Ekologisk", "vine_age": "30+ år",
        "vinification": "Skörden sker för hand. Druvorna hålls direkt i en pneumatisk press som försiktigt pressar druvorna i 2 timmar vid ett tryck på 2 bar. Jäsning sker i ekfat med inhemsk jäst. Lagring på fat i 16-18 månader, därefter i ståltank 2 månader före buteljering. Ingen filtrering."
    },
    "coffinetduvernay-chassagnemontrachet-rouge": {
        "grapes": "Pinot Noir", "farming": "Ekologisk", "vintage": "2022",
        "vinification": "Skörden sker för hand och selektering sker redan ute i vingården. Druvorna krossas och får sedan macerera i 10 dagar med pump over vid behov men generellt en väldigt lätt extraktion. Vinet jäser sedan på fat där det lagras minst 12 månader. Ingen filtrering sker.",
        "profile": "Vinet är sammansatt med en blandning av druvor från flera olika vingårdar som alla ligger i den nedre delen av byn Chassagne-Montrachet. Med den lätta extraktionen så möts man av en mjuk, fräsch och fruktdriven Pinot."
    },
    "coffinetduvernay-vin-de-france-assemblage": {
        "grapes": "Chardonnay", "farming": "Ekologisk",
        "vinification": "Skörden sker för hand. Druvorna pressas pneumatiskt. Jäsning med inhemsk jäst i ekfat. Ingen filtrering."
    },
    # === MICHEL REBOURGEON ===
    "michel-rebourgeon-beaune-les-epenottes": {
        "grapes": "Pinot Noir", "soil": "Sten, kalksten, lera", "farming": "Ekologisk", "vintage": "2022",
        "vinification": "Efter noggrann selektering så avstjälkas druvorna för att sedan krossas och placeras i temperaturkontrollerade jäskärl där druvorna första får ligga 7 dagar i 'cold soak' innan alkoholjäsningen som normalt pågår i 14 dagar. Ingen jäst tillsätts utan jäsningen sker helt naturligt. Vinet lagras sedan 18 månader i använda fat innan buteljering.",
        "profile": "En lättare Pinot med fullt fokus på frukten där man valt att inte ha någon ny ek. Svårt att inte förföras av redan månader efter buteljering."
    },
    "michel-rebourgeon-pommard-cuvee-william": {
        "grapes": "Pinot Noir", "soil": "Lera, sten, kalksten", "farming": "Ekologisk", "vine_age": "30+ år", "vintage": "2022",
        "vinification": "Efter noggrann selektering så avstjälkas druvorna för att sedan krossas. 7 dagar i 'cold soak' innan alkoholjäsningen i 14 dagar. Ingen jäst tillsätts. Vinet lagras sedan 18 månader i 100% nya stora fat innan buteljering.",
        "profile": "Vinet är en kärleksförklaring till William från sina föräldrar och är det enda vinet som lagras på 100% ny ek och i stora fat. Här fokuserar man mer på den nya eken och kryddan det ger till vinet som är välintegrerat."
    },
    "michel-rebourgeon-pommard-les-noizons": {
        "grapes": "Pinot Noir", "soil": "Kalksten, lera", "farming": "Ekologisk", "vine_age": "80+ år", "vintage": "2022",
        "vinification": "Efter noggrann selektering så avstjälkas 80-95% av druvorna beroende på årgång. 7 dagar i 'cold soak' innan alkoholjäsningen i 14 dagar. Ingen jäst tillsätts. Vinet lagras sedan 18 månader i använda fat.",
        "profile": "Les Noizons är den av village-vingårdarna som ger mest power. Detta tillsammans med en tydlig fräschör från jordmånen, mineralitet och gamla rankor ger vinet en stor helhet."
    },
    "michel-rebourgeon-pommard-trois-terroirs": {
        "grapes": "Pinot Noir", "soil": "Lera, sten, kalksten", "farming": "Ekologisk", "vine_age": "30+ år", "vintage": "2022",
        "vinification": "Efter noggrann selektering så avstjälkas druvorna. 7 dagar i 'cold soak' innan jäsningen utan tillsatt jäst i cirka 14 dagar. Vinet lagras sedan 18 månader i använda fat.",
        "profile": "Även i denna cuvée har man valt att inte ha någon ny ek utan fokusera på en väldigt ren och ung frukt och mineralitet. Tydlig Pommard terroir."
    },
    "michel-rebourgeon-beaune-1er-cru-les-chouacheux": {
        "grapes": "Pinot Noir", "soil": "Jord, kalksten, lera", "farming": "Ekologisk", "vine_age": "65+ år", "vintage": "2022",
        "vinification": "Efter noggrann selektering, 7 dagar i 'cold soak' innan naturlig alkoholjäsning i 14 dagar. Vinet lagras sedan 18 månader i fat varav 20% är nya.",
        "profile": "Vingårdens gamla rankor ger vinet en utsökt koncentration med både kraft och kropp. En djupare färg möter dig i glaset. Men missta dig inte för detta vinet är kanske en av domänens bästa viner för att avnjuta ungt!"
    },
    "michel-rebourgeon-pommard-1er-cru-les-arvelets": {
        "grapes": "Pinot Noir", "soil": "Kalksten, sandsten", "farming": "Ekologisk", "vintage": "2022",
        "vinification": "Efter noggrann selektering, 7 dagar i 'cold soak' innan naturlig alkoholjäsning i 14 dagar. Vinet lagras sedan 18 månader i använda fat.",
        "profile": "Med sin södra exponering ger denna 1er Cru en otroligt finslipad frukt och precision. Inga nya fat som lämnar avtryck utan vinet är väldigt delikat och elegant där man verkligen fångat domänens stil av lägre extraktion och fräschör."
    },
    "michel-rebourgeon-pommard-1er-cru-les-charmots": {
        "grapes": "Pinot Noir", "soil": "Kalksten", "farming": "Ekologisk", "vine_age": "60+ år", "vintage": "2022",
        "vinification": "Efter noggrann selektering, 7 dagar i 'cold soak' innan naturlig alkoholjäsning i 14 dagar. Vinet lagras sedan 18 månader i använda fat.",
        "profile": "En av domänens minsta vingårdar och kanske den som ger mest eleganta viner med fin rundhet och fräschör. På grund av detta så har man valt att endast göra magnum-flaskor och inte använda några nya fat. I vingården används aldrig några maskiner utan allt görs för hand."
    },
    # === LA FAMILLE K ===
    "la-famille-k-lheritiere": {
        "grapes": "100% Gamay", "alcohol": "13%", "soil": "Lera och Kalksten", "farming": "Ekologisk", "vine_age": "50+ år", "vintage": "2022",
        "vinification": "Druvorna skördas för hand och väljs noggrant. Vinet macererar i 7-8 dagar och så fort jäsningen är färdig som sker i cementtank så buteljeras vinet.",
        "profile": "Fyllt med fruktiga toner som jordgubbar och moreller som möts upp av en fin syra."
    },
    "la-famille-k-la-mere": {
        "grapes": "100% Gamay", "alcohol": "13%", "soil": "Lera och Kalksten", "farming": "Ekologisk", "vine_age": "50+ år", "vintage": "2020",
        "vinification": "Druvorna skördas för hand och väljs noggrant. Vinet jäser genom semi-kolsyrejäsning i cementtank med en macerationstid på 10 dagar. Efter jäsning så lagras vinet i 8-12 månader i cement.",
        "profile": "Vinet har tydliga fruktiga karaktärer som hallon och moreller tillsammans med kryddiga inslag. Väldigt behaglig syra."
    },
    "la-famille-k-le-pere": {
        "grapes": "100% Gamay", "alcohol": "13%", "soil": "Lera och Kalksten", "farming": "Ekologisk", "vine_age": "90+ år", "vintage": "2019, 2020",
        "vinification": "Druvorna skördas för hand och väljs noggrant. Vinet jäser genom semi-kolsyrejäsning i cementtank med en macerationstid på 10 dagar. I slutet av jäsningen så flyttas vinet över till franska använda barriquer där de lagras i 8-12 månader.",
        "profile": "Röda bär möter pioner och vissa balsamiska inslag. Vinet visar tydligt att Gamay har ett släktskap till Pinot Noir och tiden på fat har givit vinet väldigt fina polerade tanniner.",
        "ratings": "James Suckling 91p"
    },
    "la-famille-k-le-pere-blanc": {
        "grapes": "100% Chardonnay", "alcohol": "13%", "soil": "Lera och Kalksten", "farming": "Ekologisk", "vine_age": "20+ år", "vintage": "2022",
        "vinification": "Druvorna skördas för hand och väljs noggrant. Druvorna pressas direkt och jäser sedan på franska barriquer. Vinet lagras sedan även på barrique i 10 månader ihop med jästfällningen med kontinuerlig bâtonnage."
    },
    "la-famille-k-le-pere-vdf-pinot-noir": {
        "grapes": "100% Pinot Noir", "alcohol": "12,5%", "soil": "Lera och Kalksten", "farming": "Ekologisk", "vine_age": "4+ år", "vintage": "2022",
        "vinification": "Druvorna skördas för hand och väljs noggrant. Vinet macererar i 10 dagar och efter pressning så flyttas vinet över till franska barriquer där det spontanjäser och även lagras i 10 månader."
    },
    "la-famille-k-loncle": {
        "grapes": "100% Gamaret (Korsning mellan Reichensteiner och Gamay)", "alcohol": "13%", "soil": "Lera och Kalksten", "farming": "Ekologisk", "vine_age": "25+ år", "vintage": "2020",
        "vinification": "Druvorna skördas för hand och väljs noggrant. Druvorna avstjälkas sedan innan det är dags för jäsning i cementtank. Macerationstiden är 10 dagar och den sista delen av jäsningen sker delvis i cementtank och delvis i franska barriquer.",
        "profile": "Vinet har en tydlig rökig karaktär tillsammans med sötare kryddor och fräsch röd frukt."
    },
    # === DOMAINE VILLET (mostly empty on site) ===
    "domaine-villet-chardonnay-elevage-2-an-en-fut": {"grapes": "Chardonnay", "farming": "Ekologisk", "vintage": "2023"},
    "domaine-villet-savagnin-ouille-elevage-24-mois-en-cuve": {"grapes": "Savagnin", "farming": "Ekologisk", "vintage": "2023"},
    "domaine-villet-savagnin-ouille-elevage-30-mois-en-foudre": {"grapes": "Savagnin", "farming": "Ekologisk", "vintage": "2022"},
    "domaine-villet-pinot-noir": {"grapes": "Pinot Noir", "farming": "Ekologisk", "vintage": "2023"},
    "domaine-villet-poulsard": {"grapes": "Poulsard", "farming": "Ekologisk", "vintage": "2023"},
    "domaine-villet-rouge-tradition": {"grapes": "Pinot Noir, Poulsard, Trousseau", "farming": "Ekologisk", "vintage": "2023"},
    # === QUINTA DAS BÁGEIRAS (mostly empty on site) ===
    "quinta-das-bagerias-espumante-colheita": {"grapes": "Maria Gomes, Bical, Cercial", "vintage": "2022"},
    "quinta-das-bagerias-espumante-colheita-rose": {"grapes": "100% Baga", "vintage": "2022"},
    "quinta-das-bagerias-vinho-branco-reserva": {"grapes": "Maria Gomes, Bical", "vintage": "2022"},
    "quinta-das-bagerias-vinho-tinto-reserva": {"grapes": "Baga, Touriga Nacional", "vintage": "2021"},
    "quinta-das-bagerias-garrafeira-tinto": {"grapes": "100% Baga", "vintage": "2018"},
    "quinta-das-bagerias-abafado": {"grapes": "100% Baga"},
}

wine_data.update(more_data)

def build_details_html(data):
    """Build the detailed wine info HTML section."""
    sections = []

    # Details grid
    details = []
    if data.get("alcohol"):
        details.append(("Alkoholhalt", data["alcohol"]))
    if data.get("soil"):
        details.append(("Jordmån", data["soil"]))
    if data.get("altitude"):
        details.append(("Höjd", data["altitude"]))
    if data.get("exposure"):
        details.append(("Exponering", data["exposure"]))
    if data.get("vine_age"):
        details.append(("Ålder på vinstockar", data["vine_age"]))
    if data.get("vintage"):
        details.append(("Tillgängliga årgångar", data["vintage"]))
    if data.get("farming"):
        details.append(("Odling", data["farming"]))
    if data.get("serving_temp"):
        details.append(("Serveringstemperatur", data["serving_temp"]))

    if details:
        grid_items = ""
        for label, value in details:
            grid_items += f'''
              <div>
                <p class="text-stone-400 text-xs uppercase tracking-wider mb-1">{label}</p>
                <p class="text-stone-800 font-medium">{html.escape(value)}</p>
              </div>'''
        sections.append(f'''
            <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mt-6 p-6 bg-stone-50 rounded-xl">
              {grid_items}
            </div>''')

    # Vinification
    if data.get("vinification"):
        sections.append(f'''
            <div class="mt-8">
              <h3 class="font-serif text-lg text-stone-900 mb-3">Vinifikation</h3>
              <p class="text-stone-600 leading-relaxed font-light">{html.escape(data["vinification"])}</p>
            </div>''')

    # Profile/tasting notes
    if data.get("profile"):
        sections.append(f'''
            <div class="mt-6">
              <h3 class="font-serif text-lg text-stone-900 mb-3">Vinets profil</h3>
              <p class="text-stone-600 leading-relaxed font-light">{html.escape(data["profile"])}</p>
            </div>''')

    # Food pairing
    if data.get("food"):
        sections.append(f'''
            <div class="mt-6">
              <h3 class="font-serif text-lg text-stone-900 mb-3">Passar till</h3>
              <p class="text-stone-600 leading-relaxed font-light">{html.escape(data["food"])}</p>
            </div>''')

    # Ratings
    if data.get("ratings"):
        sections.append(f'''
            <div class="mt-6 p-4 bg-wine-50 rounded-lg">
              <h3 class="font-serif text-lg text-wine-900 mb-2">Betyg</h3>
              <p class="text-wine-800 font-medium">{html.escape(data["ratings"])}</p>
            </div>''')

    return "\n".join(sections)

# Update each wine page
count = 0
for slug, data in wine_data.items():
    filepath = f"sortiment/{slug}.html"
    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r') as f:
        content = f.read()

    # Build the new details section
    details_html = build_details_html(data)

    if not details_html.strip():
        continue

    # Replace the "Om vinet" section - find the existing description and add details after it
    # Pattern: find the closing </p> of description and the next div with buttons
    old_section = re.search(
        r'(<div class="mt-8 pt-8 border-t border-stone-200">.*?</p>)(.*?)(<div class="mt-10 flex gap-4">)',
        content, re.DOTALL
    )

    if old_section:
        # Update grapes if available
        if data.get("grapes"):
            grapes_pattern = re.search(r'(<p class="text-stone-500 text-xs uppercase tracking-wider">Druvor</p>\s*<p class="text-stone-800">)(.*?)(</p>)', content, re.DOTALL)
            if grapes_pattern:
                content = content[:grapes_pattern.start()] + grapes_pattern.group(1) + html.escape(data["grapes"]) + grapes_pattern.group(3) + content[grapes_pattern.end():]

        # Re-find after grapes update
        old_section = re.search(
            r'(<div class="mt-8 pt-8 border-t border-stone-200">.*?</p>)(.*?)(<div class="mt-10 flex gap-4">)',
            content, re.DOTALL
        )
        if old_section:
            new_content = old_section.group(1) + details_html + "\n        " + old_section.group(3)
            content = content[:old_section.start()] + new_content + content[old_section.end():]

    with open(filepath, 'w') as f:
        f.write(content)
    count += 1

print(f"Updated {count} wine pages with full details")
