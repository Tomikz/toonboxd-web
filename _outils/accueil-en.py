"""
LA PAGE D'ACCUEIL ANGLAISE, en/index.html, GÉNÉRÉE DEPUIS index.html.

Depuis le 16 octobre 2026. Elle ne s'édite jamais à la main : ce script part de
la page française et remplace chaque texte par son anglais, si bien que les
balises, les classes, le style et le script restent ceux de la française par
construction (le contrôle des jumeaux le vérifie quand même, plus bas).

LES MOTS SONT CEUX DE L'APP. Le lexique et la forme anglaise sont ceux de
DECISIONS.md §5 (« L'anglais : le lexique et la forme ») du dépôt de l'app, et
toute chaîne qui recopie un écran vient de locales/en.json, comme la française
vient de locales/fr.json. Les règles de la page sont celles du §2 point 10 de
docs/PLAN-ANGLAIS.md : aucun montant (six devises), un lien vers l'autre langue,
une invitation sans redirection, l'inscription inchangée.

CHAQUE REMPLACEMENT DIT COMBIEN DE FOIS IL DOIT S'APPLIQUER, et le script
s'arrête au premier écart : un texte français changé sans que sa traduction
suive ne passe pas en silence. Puis trois contrôles sur la page produite :
  - les jumeaux : la suite des balises et de leurs classes est la même des
    deux côtés (son témoin retire une section et doit tomber) ;
  - le reste de français : aucun texte visible, aucun attribut lu (aria-label,
    alt, placeholder, content) ni aucune chaîne du script n'en garde, hors des
    deux libellés de l'autre langue ;
  - les deux caractères bannis du projet, absents.

Usage, depuis la racine du dépôt :  py -3 _outils/accueil-en.py
                                     py -3 _outils/accueil-en.py --temoins
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "index.html"
CIBLE = RACINE / "en" / "index.html"

SUJET_FR = "Pr%C3%A9viens-moi%20du%20lancement%20de%20Toonboxd"
SUJET_EN = "Let%20me%20know%20when%20Toonboxd%20launches"

# (français tel qu'il est dans index.html, anglais, nombre d'occurrences)
TABLE = [
    # ---------- La tête ----------
    ('<html lang="fr" class="no-js">', '<html lang="en" class="no-js">', 1),
    ('<title>Toonboxd : manhwa tracker et webtoon tracker en français</title>',
     '<title>Toonboxd: manhwa tracker and webtoon tracker for iPhone</title>', 1),
    ('<meta name="description" content="Toonboxd, le manhwa tracker et webtoon tracker sur iPhone : suis tes séries au chapitre près et reçois une alerte quand un manhwa en pause reprend. Gratuit, sans pub.">',
     '<meta name="description" content="Toonboxd is the manhwa tracker and webtoon tracker for iPhone: track every series down to the chapter, and get an alert when a manhwa on hold is back. Free, no ads.">', 1),
    ('<link rel="canonical" href="https://toonboxd.app/">', '<link rel="canonical" href="https://toonboxd.app/en/">', 1),
    ('<meta property="og:locale" content="fr_FR">', '<meta property="og:locale" content="en_US">', 1),
    ('<meta property="og:locale:alternate" content="en_US">', '<meta property="og:locale:alternate" content="fr_FR">', 1),
    ('<meta property="og:url" content="https://toonboxd.app/">', '<meta property="og:url" content="https://toonboxd.app/en/">', 1),
    ('<meta property="og:title" content="Toonboxd : manhwa tracker et webtoon tracker en français">',
     '<meta property="og:title" content="Toonboxd: manhwa tracker and webtoon tracker for iPhone">', 1),
    ('<meta property="og:description" content="Suis tes manhwas et webtoons au chapitre près, et sache quand une série en pause reprend.">',
     '<meta property="og:description" content="Track your manhwa and webtoons down to the chapter, and know when a series on hold is back.">', 1),
    ('<meta property="og:image" content="https://toonboxd.app/og.png">', '<meta property="og:image" content="https://toonboxd.app/og-en.png">', 1),
    ('<meta property="og:image:alt" content="Toonboxd, manhwa tracker et webtoon tracker : ne perds plus jamais le fil.">',
     '<meta property="og:image:alt" content="Toonboxd, manhwa tracker and webtoon tracker: never lose your place again.">', 1),
    ('<meta name="twitter:title" content="Toonboxd : manhwa tracker et webtoon tracker en français">',
     '<meta name="twitter:title" content="Toonboxd: manhwa tracker and webtoon tracker for iPhone">', 1),
    ('<meta name="twitter:description" content="Suis tes manhwas et webtoons au chapitre près, et sache quand une série en pause reprend.">',
     '<meta name="twitter:description" content="Track your manhwa and webtoons down to the chapter, and know when a series on hold is back.">', 1),
    ('<meta name="twitter:image" content="https://toonboxd.app/og.png">', '<meta name="twitter:image" content="https://toonboxd.app/og-en.png">', 1),

    # ---------- Les données structurées ----------
    ('      "url": "https://toonboxd.app/",\n      "description": "Manhwa tracker et webtoon tracker sur iPhone, en français : progression chapitre par chapitre, note de reprise, et une notification quand une série en pause reprend.",\n      "offers": { "@type": "Offer", "price": "0", "priceCurrency": "EUR" },',
     '      "url": "https://toonboxd.app/en/",\n      "description": "Manhwa tracker and webtoon tracker for iPhone: chapter-by-chapter progress, a pause note, and a notification when a series on hold is back.",\n      "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },', 1),
    ('"@id": "https://toonboxd.app/#faq",', '"@id": "https://toonboxd.app/en/#faq",', 1),
    ('{ "@type": "Question", "name": "C’est quoi, Toonboxd ?", "acceptedAnswer": { "@type": "Answer", "text": "Toonboxd est un manhwa tracker et un webtoon tracker sur iPhone, entièrement en français. Tu ranges tes séries par statut, tu avances chapitre par chapitre, tu écris une note quand tu mets une série en pause, et l’app te prévient quand elle reprend. L’idée tient en une image : un Letterboxd des manhwas." } },',
     '{ "@type": "Question", "name": "What is Toonboxd?", "acceptedAnswer": { "@type": "Answer", "text": "Toonboxd is a manhwa tracker and webtoon tracker for iPhone, in English and French. You sort your series by status, move forward chapter by chapter, write a note when you put a series on hold, and the app lets you know when it’s back. The idea fits in a few words: Letterboxd for manhwa." } },', 1),
    ('{ "@type": "Question", "name": "Qu’est-ce qu’un manhwa tracker ?", "acceptedAnswer": { "@type": "Answer", "text": "Un manhwa tracker est une app qui retient où tu en es dans chacune de tes séries : le dernier chapitre lu, son statut, ta note. Tu n’as plus à tenir une liste dans tes notes ni à relire des chapitres pour retrouver ta place. Toonboxd fait la même chose pour les manhuas et les webtoons." } },',
     '{ "@type": "Question", "name": "What is a manhwa tracker?", "acceptedAnswer": { "@type": "Answer", "text": "A manhwa tracker is an app that remembers where you are in each of your manhwa (Korean comics): the last chapter you read, its status, your rating. No more keeping a list in your notes or rereading chapters to find your place. Toonboxd does the same for manhua and webtoons." } },', 1),
    ('{ "@type": "Question", "name": "Existe-t-il un webtoon tracker en français ?", "acceptedAnswer": { "@type": "Answer", "text": "Oui : Toonboxd est un webtoon tracker entièrement en français, lancé d’abord en France. Son catalogue compte près de 9 700 manhwas, manhuas et webtoons verticaux." } },',
     '{ "@type": "Question", "name": "Is there a webtoon tracker in English?", "acceptedAnswer": { "@type": "Answer", "text": "Yes: Toonboxd is a webtoon tracker in English and French, coming to iPhone in the United States, the United Kingdom, Canada, Australia, Ireland, New Zealand and France. It lists nearly 9,700 vertical manhwa, manhua and webtoons." } },', 1),
    ('{ "@type": "Question", "name": "Comment savoir quand un manhwa en pause reprend ?", "acceptedAnswer": { "@type": "Answer", "text": "Mets-le en pause dans Toonboxd. Quand un lecteur signale sa reprise et que le signalement est validé, tous ceux qui l’avaient en pause reçoivent une notification dans les cinq minutes, et un tap ouvre sa fiche." } },',
     '{ "@type": "Question", "name": "How do I know when a manhwa on hiatus is back?", "acceptedAnswer": { "@type": "Answer", "text": "Put it on hold in Toonboxd. When a reader reports that it’s back and the report is confirmed, everyone who had it on hold gets a notification within five minutes, and one tap opens its page." } },', 1),
    ('{ "@type": "Question", "name": "Comment montrer son top 5 manhwa ?", "acceptedAnswer": { "@type": "Answer", "text": "Compose ton top 5 dans Toonboxd : l’œil de ton top 5, sur ton profil, ouvre ta carte. Ta série numéro 1 en grand avec ta note et ton chapitre, les quatre suivantes dessous, ton total de chapitres lus, au format story. Le libellé « Mon top 5 manhwa » se remplace par le tien, gratuitement." } },',
     '{ "@type": "Question", "name": "How do I share my top 5 manhwa?", "acceptedAnswer": { "@type": "Answer", "text": "Put together your top 5 in Toonboxd: the eye on your top 5, in your profile, opens your card. Your #1 series up front with your rating and your chapter, the next four below, your total chapters read, in story format. You can swap the “My top 5 manhwa” label for your own, for free." } },', 1),
    ('{ "@type": "Question", "name": "Toonboxd est-il gratuit ?", "acceptedAnswer": { "@type": "Answer", "text": "Oui, et sans publicité. La version gratuite suit jusqu’à 30 séries en cours, sans limite pour les séries prévues, en pause, terminées ou abandonnées, avec trois listes modifiables. Toonboxd Pro coûte 17,99 € par an ou 2,99 € par mois, avec 7 jours d’essai sur les deux formules à un premier abonnement." } },',
     '{ "@type": "Question", "name": "Is Toonboxd free?", "acceptedAnswer": { "@type": "Answer", "text": "Yes, with no ads. The free version tracks up to 30 series you’re reading, with no limit on series in Plan to Read, On Hold, Completed or Dropped, and three editable lists. Toonboxd Pro is yearly or monthly, with 7 days free on both plans with a first subscription. The App Store shows the price in your currency." } },', 1),
    ('{ "@type": "Question", "name": "Peut-on lire des chapitres dans l’app ?", "acceptedAnswer": { "@type": "Answer", "text": "Non. Toonboxd n’héberge aucun chapitre. Le bouton « Lire sur… » de chaque fiche ouvre la plateforme officielle où lire la série." } },',
     '{ "@type": "Question", "name": "Can I read chapters in the app?", "acceptedAnswer": { "@type": "Answer", "text": "No. Toonboxd hosts no chapters. The “Read on…” button on every series page opens the official platform where you can read it." } },', 1),
    ('{ "@type": "Question", "name": "Faut-il créer un compte ?", "acceptedAnswer": { "@type": "Answer", "text": "Non. L’app crée un compte anonyme, sans email ni mot de passe. Tu peux le lier à ton identifiant Apple pour retrouver ta bibliothèque sur un autre iPhone, et le supprimer entièrement depuis les réglages." } },',
     '{ "@type": "Question", "name": "Do I need to create an account?", "acceptedAnswer": { "@type": "Answer", "text": "No. The app creates an anonymous account, with no email or password. You can link it to your Apple Account to get your library back on another iPhone, and delete it entirely from Settings." } },', 1),
    ('{ "@type": "Question", "name": "Les mangas japonais sont-ils au catalogue ?", "acceptedAnswer": { "@type": "Answer", "text": "Non, et c’est voulu : Toonboxd suit les manhwas, les manhuas et les webtoons. Si une série de ce genre manque, tu peux la suggérer depuis la recherche, gratuitement." } },',
     '{ "@type": "Question", "name": "Does Toonboxd have Japanese manga?", "acceptedAnswer": { "@type": "Answer", "text": "No, and that’s on purpose: Toonboxd tracks manhwa, manhua and webtoons. No Japanese manga. If a series like these is missing, you can suggest it from Search, for free." } },', 1),
    ('{ "@type": "Question", "name": "Toonboxd existe-t-il sur Android ?", "acceptedAnswer": { "@type": "Answer", "text": "Android ensuite : Toonboxd sort d’abord sur iPhone, en France, et la version Android suit. Choisis Android en t’inscrivant au lancement sur toonboxd.app : on t’écrit pour la bêta, puis le jour où elle arrive sur ton téléphone." } },',
     '{ "@type": "Question", "name": "Is Toonboxd on Android?", "acceptedAnswer": { "@type": "Answer", "text": "Android is next: Toonboxd comes to iPhone first, and the Android version follows. Choose Android when you sign up for the launch on toonboxd.app: we’ll write to you for the beta, then on the day it arrives on your phone." } },', 1),
    ('{ "@type": "Question", "name": "Quand sort Toonboxd ?", "acceptedAnswer": { "@type": "Answer", "text": "Toonboxd arrive bientôt sur l’App Store, et sur Android ensuite. Pour être prévenu, laisse ton email sur toonboxd.app et choisis ton téléphone : on t’écrit pour la bêta, puis le jour où Toonboxd arrive sur ton téléphone. Rien d’autre." } }',
     '{ "@type": "Question", "name": "When does Toonboxd come out?", "acceptedAnswer": { "@type": "Answer", "text": "Toonboxd is coming soon to the App Store, and to Android after that. To hear about it, leave your email on toonboxd.app and choose your phone: we’ll write to you for the beta, then on the day Toonboxd arrives on your phone. Nothing else." } }', 1),

    # ---------- L'en-tête et l'autre langue ----------
    ('<a class="skip" href="#contenu">Aller au contenu</a>', '<a class="skip" href="#contenu">Skip to content</a>', 1),
    ('<a class="brand" href="/" aria-label="Toonboxd, accueil">', '<a class="brand" href="/en/" aria-label="Toonboxd, home">', 1),
    ('<a href="#fonctionnalites">Fonctionnalités</a>', '<a href="#fonctionnalites">Features</a>', 1),
    ('<a href="#tarifs">Tarifs</a>', '<a href="#tarifs">Pricing</a>', 1),
    ('<a class="langue" href="/en/" hreflang="en" lang="en">English</a>', '<a class="langue" href="/" hreflang="fr" lang="fr">Français</a>', 1),
    ('<p class="autre-langue" data-autre-langue="en" hidden><a href="/en/" hreflang="en" lang="en">Read in English<svg',
     '<p class="autre-langue" data-autre-langue="fr" hidden><a href="/" hreflang="fr" lang="fr">Lire en français<svg', 1),
    (SUJET_FR, SUJET_EN, 5),
    ('data-prevenir>Me prévenir du lancement</a>', 'data-prevenir>Notify Me at Launch</a>', 3),

    # ---------- L'accroche ----------
    ('</svg>Manhwa tracker et webtoon tracker</span>', '</svg>Manhwa tracker and webtoon tracker</span>', 1),
    ('<span class="h1-main">Ne perds plus jamais le fil.</span>', '<span class="h1-main">Never lose your place again.</span>', 1),
    ('<p class="lead">Avance chaque série d’un chapitre en un tap. Et quand un manhwa en pause reprend, Toonboxd te prévient.</p>',
     '<p class="lead">Move any series forward a chapter with one tap. And when a manhwa on hold is back, Toonboxd lets you know.</p>', 1),
    ('<span class="store-badge">Bientôt sur l’App Store</span>', '<span class="store-badge">Coming soon to the App Store</span>', 1),
    ('aria-label="Démonstration de l’écran Reprendre de Toonboxd"', 'aria-label="Demo of the Toonboxd Continue screen"', 1),
    ('<p class="app-title">Tes lectures</p>', '<p class="app-title">Currently Reading</p>', 1),
    ('<p class="app-sub">4 séries en cours</p>', '<p class="app-sub">4 series you’re reading</p>', 1),
    ('</svg>Cherche dans tes lectures</div>', '</svg>Search what you’re reading</div>', 2),
    ('aria-label="Épinglée"', 'aria-label="Pinned"', 1),
    ('aria-label="Retirer un chapitre, ', 'aria-label="Previous chapter, ', 4),
    ('aria-label="Chapitre suivant, ', 'aria-label="Next chapter, ', 4),
    # Les onglets des deux téléphones, et l'étiquette de la cellule du même nom.
    ('</svg>Reprendre</span>', '</svg>Continue</span>', 3),
    ('</svg>Recherche</span>', '</svg>Search</span>', 3),
    ('</svg>Bibliothèque</span>', '</svg>Library</span>', 3),
    ('</svg>Profil</span>', '</svg>Profile</span>', 2),
    ('aria-label="Notification Toonboxd : Nano Machine est de retour. Tu l\'avais mise en pause. Elle a repris."',
     'aria-label="Toonboxd notification: Nano Machine is back. You put it on hold. It’s updating again."', 1),
    ('<span class="notif-when">maintenant</span>', '<span class="notif-when">now</span>', 2),
    ('<p class="notif-title">Nano Machine est de retour</p>', '<p class="notif-title">Nano Machine is back</p>', 2),
    ('<p class="notif-body">Tu l\'avais mise en pause. Elle a repris.</p>', '<p class="notif-body">You put it on hold. It’s updating again.</p>', 2),

    # ---------- La carte du top 5 ----------
    ('aria-label="Carte de partage du top 5 de @toi : numéro 1, Return of the Blossoming Blade, cinq étoiles, 174 chapitres ; puis Eleceed, Solo Leveling, Omniscient Reader et Nano Machine ; 6 214 chapitres lus. Signée Toonboxd."',
     'aria-label="Top 5 share card for @you: number 1, Return of the Blossoming Blade, five stars, 174 chapters; then Eleceed, Solo Leveling, Omniscient Reader and Nano Machine; 6,214 chapters read. Signed Toonboxd."', 1),
    ('<p class="sc-handle">@toi</p><p class="sc-label">Mon top 5 manhwa</p>', '<p class="sc-handle">@you</p><p class="sc-label">My top 5 manhwa</p>', 1),
    ('<p class="sc-label sc-hero-ch">174 chapitres</p>', '<p class="sc-label sc-hero-ch">174 chapters</p>', 1),
    ('<div class="sc-total"><b>6&#8239;214</b><span class="sc-label">chapitres lus</span></div>',
     '<div class="sc-total"><b>6,214</b><span class="sc-label">chapters read</span></div>', 1),
    ('<span class="eyebrow" data-reveal>La carte du top 5</span>', '<span class="eyebrow" data-reveal>The top 5 card</span>', 1),
    ('<h2 class="h2" id="t-carte" data-reveal>Ton top 5, en une image.</h2>', '<h2 class="h2" id="t-carte" data-reveal>Your top 5, in one image.</h2>', 1),
    ('<p class="lead" data-reveal style="--d:1">Ta série numéro 1 en grand, les quatre suivantes dessous, et ton total de chapitres lus. Une image au format story, faite pour être partagée.</p>',
     '<p class="lead" data-reveal style="--d:1">Your #1 series up front, the next four below, and your total chapters read. A story-format image, made to be shared.</p>', 1),
    ('<p>Ta note et ton chapitre <span>sur ta série numéro 1, mise en avant.</span></p>', '<p>Your rating and your chapter <span>on your #1 series, front and center.</span></p>', 1),
    ('<p>Ton propre libellé <span>à la place de « Mon top 5 manhwa », gratuitement.</span></p>', '<p>Your own label <span>instead of “My top 5 manhwa”, for free.</span></p>', 1),
    ('<p>Toujours à portée, <span>depuis l’œil de ton top 5 sur ton profil.</span></p>', '<p>Always within reach, <span>from the eye on your top 5, in your profile.</span></p>', 1),
    ('<p>Au format story, <span>1080 sur 1920 pixels.</span></p>', '<p>Story format, <span>1080 by 1920 pixels.</span></p>', 1),

    # ---------- Les fonctionnalités ----------
    ('<h2 class="h2" id="t-fonctions" data-reveal>Un webtoon tracker complet, en quatre onglets.</h2>',
     '<h2 class="h2" id="t-fonctions" data-reveal>A complete webtoon tracker, in four tabs.</h2>', 1),
    ('<p class="lead" data-reveal style="--d:1">Reprendre, Recherche, Bibliothèque, Profil&nbsp;: de quoi suivre des dizaines de manhwas, manhuas et webtoons sans rien noter ailleurs.</p>',
     '<p class="lead" data-reveal style="--d:1">Continue, Search, Library, Profile: everything you need to follow dozens of manhwa, manhua and webtoons without writing anything down elsewhere.</p>', 1),
    ('<h3 class="h3">Chaque série a son statut.</h3>', '<h3 class="h3">Every series has its status.</h3>', 1),
    ('<p class="p">Des carrousels par statut, une grille complète, un tri, un filtre par genre, et une recherche dans toute ta bibliothèque.</p>',
     '<p class="p">Carousels by status, a full grid, sorting, a genre filter, and search across your whole library.</p>', 1),
    ('aria-label="Les cinq statuts"', 'aria-label="The five statuses"', 1),
    ('<span class="chip">Prévu</span><span class="chip on">En cours</span><span class="chip">En pause</span><span class="chip">Terminé</span><span class="chip">Abandonné</span>',
     '<span class="chip">Plan to Read</span><span class="chip on">Reading</span><span class="chip">On Hold</span><span class="chip">Completed</span><span class="chip">Dropped</span>', 1),
    ('<p class="shelf-head">En cours <span>12</span></p>', '<p class="shelf-head">Reading <span>12</span></p>', 1),
    ('<p class="shelf-head">En pause <span>4</span></p>', '<p class="shelf-head">On Hold <span>4</span></p>', 1),
    ('</svg>La fiche</span>', '</svg>The series page</span>', 1),
    ('<h3 class="h3">Note ce que tu lis.</h3>', '<h3 class="h3">Rate what you read.</h3>', 1),
    ('<p class="p">Ta note rejoint une moyenne communautaire anonyme.</p>', '<p class="p">Your rating joins an anonymous community average.</p>', 1),
    ('<p class="fiche-line">Terminé - 201 chapitres</p>', '<p class="fiche-line">Finished - 201 chapters</p>', 1),
    ('</svg>Sources officielles</span>', '</svg>Official sources</span>', 1),
    ('<h3 class="h3">Toonboxd n’héberge aucun chapitre.</h3>', '<h3 class="h3">Toonboxd hosts no chapters.</h3>', 1),
    ('<p class="p">«&nbsp;Lire sur…&nbsp;» t’emmène sur la plateforme officielle, et un second bouton cherche le chapitre où tu en es.</p>',
     '<p class="p">“Read on…” takes you to the official platform, and a second button searches for the chapter you’re on.</p>', 1),
    ('<span class="readon" aria-hidden="true">Lire sur…<svg', '<span class="readon" aria-hidden="true">Read on…<svg', 1),
    ('<h3 class="h3">Tes épinglées, dans ton ordre.</h3>', '<h3 class="h3">Your pinned series, in your order.</h3>', 1),
    ('<p class="p">Glisse tes séries épinglées pour les ranger comme tu veux, et retrouve une lecture en tapant son nom.</p>',
     '<p class="p">Drag your pinned series to arrange them however you like, and find any series you’re reading by typing its name.</p>', 1),
    ('<h3 class="h3">Près de 9&#8239;700 séries. Il manque la tienne&nbsp;? Suggère-la.</h3>', '<h3 class="h3">Nearly 9,700 series. Missing yours? Suggest it.</h3>', 1),
    ('<p class="p">La recherche couvre tout le catalogue de manhwas, manhuas et webtoons. Si ton titre n’y est pas, propose-le&nbsp;: c’est gratuit, et on te prévient si on l’ajoute.</p>',
     '<p class="p">Search covers every manhwa, manhua and webtoon in Toonboxd. If your title isn’t there, suggest it: it’s free, and we’ll let you know if we add it.</p>', 1),
    ('</svg>Cherche un titre</div>', '</svg>Search for a title</div>', 1),
    ('</svg>Suggérer un titre</span>', '</svg>Suggest a Title</span>', 1),

    # ---------- Le retour de hiatus ----------
    ('<span class="eyebrow" data-reveal>Le retour de hiatus</span>', '<span class="eyebrow" data-reveal>Hiatus returns</span>', 1),
    ('<h2 class="h2" id="t-hiatus" data-reveal>Les longues pauses&nbsp;? Gérées.</h2>', '<h2 class="h2" id="t-hiatus" data-reveal>Long hiatuses? Handled.</h2>', 1),
    ('<p class="lead" data-reveal style="--d:1">Un manhwa part en hiatus pendant des mois, tu passes à autre chose. Le jour où il reprend, Toonboxd te prévient, et ta note t’attend.</p>',
     '<p class="lead" data-reveal style="--d:1">A manhwa goes on hiatus for months, and you move on. The day it’s back, Toonboxd lets you know, and your note will be waiting.</p>', 1),
    ('<p class="sheet-line">En pause&nbsp;: chapitre 147</p>', '<p class="sheet-line">On Hold: chapter 147</p>', 1),
    ('<p class="memo-label">Ta note de reprise</p>', '<p class="memo-label">Your pause note</p>', 1),
    ('<p class="memo-text">Il vient de rentrer au clan. Relire la fin du 146 avant de reprendre.</p>',
     '<p class="memo-text">He just made it back to the clan. Reread the end of 146 before picking it up.</p>', 1),
    ('<h3 class="h3">Tu la mets en pause</h3>', '<h3 class="h3">You put it on hold</h3>', 1),
    ('<p class="p">Tu écris ta note de reprise&nbsp;: où tu t’étais arrêté, ce que tu attendais. Elle est privée et ne quitte jamais notre base.</p>',
     '<p class="p">You write your pause note: where you stopped, what you were waiting for. It’s private and never leaves our database.</p>', 1),
    ('<p class="alert-title">Cette série a repris&nbsp;?</p>', '<p class="alert-title">Is this series back?</p>', 1),
    ('<p class="alert-msg">Tu signales qu\'un nouveau chapitre est sorti après une longue pause. C\'est relu à la main avant d\'être pris en compte.</p>',
     '<p class="alert-msg">You’re reporting that a new chapter came out after a long hiatus. We check it by hand before it counts.</p>', 1),
    ('<div class="alert-actions"><span>Annuler</span><span>Signaler</span></div>', '<div class="alert-actions"><span>Cancel</span><span>Report</span></div>', 1),
    ('<h3 class="h3">Un lecteur signale son retour</h3>', '<h3 class="h3">A reader reports its comeback</h3>', 1),
    ('<p class="p">Chaque signalement est relu à la main avant d’être pris en compte. Pas de fausse alerte.</p>',
     '<p class="p">Every report is checked by hand before it counts. No false alarms.</p>', 1),
    ('<h3 class="h3">Tu es prévenu</h3>', '<h3 class="h3">You get notified</h3>', 1),
    ('<p class="p">Dans les cinq minutes qui suivent la validation, que l’app soit ouverte ou fermée. Un tap t’amène sur la fiche.</p>',
     '<p class="p">Within five minutes of the check, whether the app is open or closed. One tap takes you to the series page.</p>', 1),
    ('<span>Toonboxd ne te demande pas d’accepter les notifications à l’installation. La question arrive à ta première mise en pause, au moment où tu comprends à quoi elles servent.</span>',
     '<span>Toonboxd doesn’t ask you to allow notifications when you install it. The question comes the first time you put a series on hold, when you can see what they’re for.</span>', 1),

    # ---------- Le profil ----------
    ('<h2 class="h2" id="t-profil" data-reveal>Ton profil, ta vitrine.</h2>', '<h2 class="h2" id="t-profil" data-reveal>Your profile, your showcase.</h2>', 1),
    ('<p class="lead" data-reveal style="--d:1">Un top 5 que tu composes, des titres qui se débloquent en lisant, et un profil à ton image&nbsp;: bannière, cadre et animation.</p>',
     '<p class="lead" data-reveal style="--d:1">A top 5 you put together, titles you unlock by reading, and a profile that’s yours: banner, frame and animation.</p>', 1),
    ('aria-label="L’écran Profil de Toonboxd : la bannière Nuit étoilée, l’avatar dans le cadre Roses, une pluie de pétales à l’ouverture, @toi, le titre Bêta-testeur, 86 séries, 6 214 chapitres lus, et un top 5 : Return of the Blossoming Blade, Eleceed, Solo Leveling, Omniscient Reader, Nano Machine."',
     'aria-label="The Toonboxd Profile screen: the Starry Night banner, the avatar in the Roses frame, falling petals when it opens, @you, the Beta Tester title, 86 series, 6,214 chapters read, and a top 5: Return of the Blossoming Blade, Eleceed, Solo Leveling, Omniscient Reader, Nano Machine."', 1),
    ('<p class="pf-handle">@toi</p>', '<p class="pf-handle">@you</p>', 1),
    ('<p class="pf-title titre-beta_testeur">Bêta-testeur</p>', '<p class="pf-title titre-beta_testeur">Beta Tester</p>', 1),
    ('<p><b>86</b><span>séries</span></p>', '<p><b>86</b><span>series</span></p>', 1),
    ('<p><b>6&#8239;214</b><span>chapitres lus</span></p>', '<p><b>6,214</b><span>chapters read</span></p>', 1),
    ('<div class="pf-edit">Modifier le profil</div>', '<div class="pf-edit">Edit Profile</div>', 1),
    ('<p class="pf-lists">Listes<svg', '<p class="pf-lists">Lists<svg', 1),
    ('</svg>Titres</span>', '</svg>Titles</span>', 1),
    ('<h3 class="h3">Des titres qui se gagnent en lisant.</h3>', '<h3 class="h3">Titles you earn by reading.</h3>', 1),
    ('<p class="p">Tu en portes un sous ton pseudo. Six pour commencer, tous gratuits&nbsp;: personne ne paie pour un titre.</p>',
     '<p class="p">You wear one under your username. Six to start with, all free: nobody pays for a title.</p>', 1),
    ('<b class="titre-lecteur">Lecteur</b><span class="num">1&#8239;000 chapitres lus</span>', '<b class="titre-lecteur">Reader</b><span class="num">1,000 chapters read</span>', 1),
    ('<b class="titre-devoreur">Dévoreur</b><span class="num">5&#8239;000 chapitres lus</span>', '<b class="titre-devoreur">Devourer</b><span class="num">5,000 chapters read</span>', 1),
    ('<b class="titre-insatiable">Insatiable</b><span class="num">20&#8239;000 chapitres lus</span>', '<b class="titre-insatiable">Insatiable</b><span class="num">20,000 chapters read</span>', 1),
    ('<b class="titre-finisseur">Finisseur</b><span class="num">25 séries terminées</span>', '<b class="titre-finisseur">Completionist</b><span class="num">25 series completed</span>', 1),
    ('<b class="titre-critique">Critique</b><span class="num">20 séries notées</span>', '<b class="titre-critique">Critic</b><span class="num">20 series rated</span>', 1),
    ('<b class="titre-beta_testeur">Bêta-testeur</b><span>Réservé aux premiers lecteurs.</span>', '<b class="titre-beta_testeur">Beta Tester</b><span>Reserved for our first readers.</span>', 1),
    ('<b>Et bien d’autres à venir</b><span>La galerie s’agrandit avec les mises à jour de l’app.</span>', '<b>And many more to come</b><span>The gallery grows with every app update.</span>', 1),
    ('<p class="titles-foot">Une galerie te montre où tu en es pour chacun.</p>', '<p class="titles-foot">A gallery shows where you stand on each one.</p>', 1),

    # ---------- Les listes ----------
    ('<h2 class="h2" id="t-listes" data-reveal>Tes listes, lisibles par tous.</h2>', '<h2 class="h2" id="t-listes" data-reveal>Your lists, open to everyone.</h2>', 1),
    ('<p class="lead" data-reveal style="--d:1">Compose des listes avec un titre, une description et ton ordre. Partage-en une&nbsp;: elle devient une page sur toonboxd.app, lisible sans compte ni app.</p>',
     '<p class="lead" data-reveal style="--d:1">Make lists with a title, a description and your order. Share one: it becomes a page on toonboxd.app that anyone can read, no account or app needed.</p>', 1),
    ('<p>Tes statuts de lecture, tes notes de reprise et tes évaluations <span>n’y apparaissent jamais.</span></p>',
     '<p>Your reading statuses, pause notes and ratings <span>never show up there.</span></p>', 1),
    ('<p>Visible par qui a le lien, <span>et la page ne mesure rien de ses visiteurs.</span></p>', '<p>Visible to anyone with the link, <span>and the page measures nothing about its visitors.</span></p>', 1),
    ('<p>Trois listes gratuites, <span>illimitées avec le Pro.</span></p>', '<p>Three free lists, <span>unlimited with Pro.</span></p>', 1),
    ('aria-label="Exemple de liste partagée sur toonboxd.app : Murim, mes indispensables, par @toi, 7 séries."',
     'aria-label="Example of a list shared on toonboxd.app: Murim, my must-reads, by @you, 7 series."', 1),
    ('<p class="who">@toi<b class="titre-devoreur">Dévoreur</b></p>', '<p class="who">@you<b class="titre-devoreur">Devourer</b></p>', 1),
    ('<p class="page-title">Murim, mes indispensables</p>', '<p class="page-title">Murim, my must-reads</p>', 1),
    ('<p class="page-desc">Les séries d’arts martiaux que je fais lire à tout le monde.</p>', '<p class="page-desc">The martial arts series I get everyone to read.</p>', 1),
    ('<p class="page-count">7 séries</p>', '<p class="page-count">7 series</p>', 1),

    # ---------- Les tarifs, sans aucun montant ----------
    ('<h2 class="h2" id="t-tarifs" data-reveal>Gratuit et sans pub. Pro si tu en veux plus.</h2>', '<h2 class="h2" id="t-tarifs" data-reveal>Free with no ads. Pro if you want more.</h2>', 1),
    ('<p class="plan-name">Gratuit</p>\n          <p class="price">0&nbsp;€</p>\n          <p class="price-sub">Sans limite de durée, sans publicité.</p>',
     '<p class="plan-name">Toonboxd</p>\n          <p class="price">Free</p>\n          <p class="price-sub">No time limit, no ads.</p>', 1),
    ('</svg>Jusqu’à 30 séries en cours</li>', '</svg>Up to 30 series you’re reading</li>', 1),
    ('</svg>Séries prévues, en pause, terminées ou abandonnées sans limite</li>', '</svg>Unlimited series in Plan to Read, On Hold, Completed or Dropped</li>', 1),
    ('</svg>Le retour de hiatus et la note de reprise</li>', '</svg>Hiatus returns and the pause note</li>', 1),
    ('</svg>3 listes modifiables et partageables</li>', '</svg>3 lists you can edit and share</li>', 1),
    ('</svg>Tous les titres du profil</li>', '</svg>Every profile title</li>', 1),
    ('<p class="plan-name">Pro <span class="trial">7 jours d’essai</span></p>\n          <p class="price">17,99&nbsp;€<small>&nbsp;/an</small></p>\n          <p class="price-sub">Soit 1,50&nbsp;€ par mois. Ou 2,99&nbsp;€ au mois, sans engagement.</p>',
     '<p class="plan-name">Toonboxd Pro <span class="trial">7 days free</span></p>\n          <p class="price">Yearly<small> or monthly</small></p>\n          <p class="price-sub">Monthly with no commitment. The App Store shows the price in your currency.</p>', 1),
    ('</svg>Tout ce que fait la version gratuite</li>', '</svg>Everything the free version does</li>', 1),
    ('</svg>Séries en cours illimitées</li>', '</svg>Unlimited series you’re reading</li>', 1),
    ('</svg>Listes illimitées</li>', '</svg>Unlimited lists</li>', 1),
    ('</svg>Bannières illustrées et animées, animations et cadres de profil</li>', '</svg>Illustrated and animated banners, profile animations and frames</li>', 1),
    ('<p class="plans-note" data-reveal>7 jours offerts sur les deux formules à ton premier abonnement, annulable à tout moment. Si tu arrêtes le Pro, ta bannière reste et toutes tes listes restent visibles&nbsp;: Toonboxd ne verrouille jamais ce que tu as construit.</p>',
     '<p class="plans-note" data-reveal>7 days free on both plans with your first subscription, cancel anytime. If you stop Pro, your banner stays and all your lists stay visible: Toonboxd never locks what you’ve built.</p>', 1),

    # ---------- La vie privée ----------
    ('<span>Pas de pub.</span>\n        <span>Pas de suivi publicitaire.</span>\n        <span>Pas de compte à créer.</span>',
     '<span>No ads.</span>\n        <span>No ad tracking.</span>\n        <span>No account to create.</span>', 1),
    ('<b>Aucun outil publicitaire</b><p>L’app ne te demande jamais l’autorisation de suivi d’Apple&nbsp;: il n’y a rien dedans qui en aurait besoin.</p>',
     '<b>No ad tools</b><p>The app never shows Apple’s tracking prompt: there’s nothing in it that would need one.</p>', 1),
    ('<b>Hébergée à Paris</b><p>Ta bibliothèque est stockée en France.</p>', '<b>Hosted in Paris</b><p>Your library is stored in France.</p>', 1),
    ('<b>Ni email, ni mot de passe</b><p>Un compte anonyme se crée tout seul. Lie-le à Apple si tu changes d’iPhone.</p>',
     '<b>No email, no password</b><p>An anonymous account is created for you. Link it to Apple if you switch iPhones.</p>', 1),
    ('<b>Supprimable en entier</b><p>Ton compte s’efface depuis les réglages, avec tout ce qu’il contient.</p>',
     '<b>Fully deletable</b><p>Your account is erased from Settings, with everything in it.</p>', 1),
    ('<a class="link" href="/confidentialite/">Lire la politique de confidentialité<svg', '<a class="link" href="/privacy/">Read the privacy policy<svg', 1),
    ('<p class="privacy-site">Ce site non plus ne mesure rien&nbsp;: ni cookie, ni statistique de visite.</p>',
     '<p class="privacy-site">This site doesn’t measure anything either: no cookies, no visit stats.</p>', 1),

    # ---------- Les questions ----------
    ('<h2 class="h2" id="t-faq" data-reveal>Questions fréquentes</h2>', '<h2 class="h2" id="t-faq" data-reveal>Frequently asked questions</h2>', 1),
    ('<p class="lead" data-reveal style="--d:1">Une autre question&nbsp;? Écris à <a href="mailto:contact@toonboxd.app">contact@toonboxd.app</a>.</p>',
     '<p class="lead" data-reveal style="--d:1">Another question? Write to <a href="mailto:contact@toonboxd.app">contact@toonboxd.app</a>.</p>', 1),
    ('<summary>C’est quoi, Toonboxd&nbsp;?<svg', '<summary>What is Toonboxd?<svg', 1),
    ('<p>Toonboxd est un manhwa tracker et un webtoon tracker sur iPhone, entièrement en français. Tu ranges tes séries par statut, tu avances chapitre par chapitre, tu écris une note quand tu mets une série en pause, et l’app te prévient quand elle reprend. L’idée tient en une image&nbsp;: un Letterboxd des manhwas.</p>',
     '<p>Toonboxd is a manhwa tracker and webtoon tracker for iPhone, in English and French. You sort your series by status, move forward chapter by chapter, write a note when you put a series on hold, and the app lets you know when it’s back. The idea fits in a few words: Letterboxd for manhwa.</p>', 1),
    ('<summary>Qu’est-ce qu’un manhwa tracker&nbsp;?<svg', '<summary>What is a manhwa tracker?<svg', 1),
    ('<p>Un manhwa tracker est une app qui retient où tu en es dans chacune de tes séries&nbsp;: le dernier chapitre lu, son statut, ta note. Tu n’as plus à tenir une liste dans tes notes ni à relire des chapitres pour retrouver ta place. Toonboxd fait la même chose pour les manhuas et les webtoons.</p>',
     '<p>A manhwa tracker is an app that remembers where you are in each of your manhwa (Korean comics): the last chapter you read, its status, your rating. No more keeping a list in your notes or rereading chapters to find your place. Toonboxd does the same for manhua and webtoons.</p>', 1),
    ('<summary>Existe-t-il un webtoon tracker en français&nbsp;?<svg', '<summary>Is there a webtoon tracker in English?<svg', 1),
    ('<p>Oui&nbsp;: Toonboxd est un webtoon tracker entièrement en français, lancé d’abord en France. Son catalogue compte près de 9&#8239;700 manhwas, manhuas et webtoons verticaux.</p>',
     '<p>Yes: Toonboxd is a webtoon tracker in English and French, coming to iPhone in the United States, the United Kingdom, Canada, Australia, Ireland, New Zealand and France. It lists nearly 9,700 vertical manhwa, manhua and webtoons.</p>', 1),
    ('<summary>Comment savoir quand un manhwa en pause reprend&nbsp;?<svg', '<summary>How do I know when a manhwa on hiatus is back?<svg', 1),
    ('<p>Mets-le en pause dans Toonboxd. Quand un lecteur signale sa reprise et que le signalement est validé, tous ceux qui l’avaient en pause reçoivent une notification dans les cinq minutes, et un tap ouvre sa fiche.</p>',
     '<p>Put it on hold in Toonboxd. When a reader reports that it’s back and the report is confirmed, everyone who had it on hold gets a notification within five minutes, and one tap opens its page.</p>', 1),
    ('<summary>Comment montrer son top 5 manhwa&nbsp;?<svg', '<summary>How do I share my top 5 manhwa?<svg', 1),
    ('<p>Compose ton top 5 dans Toonboxd&nbsp;: l’œil de ton top 5, sur ton profil, ouvre ta carte. Ta série numéro 1 en grand avec ta note et ton chapitre, les quatre suivantes dessous, ton total de chapitres lus, au format story. Le libellé «&nbsp;Mon top 5 manhwa&nbsp;» se remplace par le tien, gratuitement.</p>',
     '<p>Put together your top 5 in Toonboxd: the eye on your top 5, in your profile, opens your card. Your #1 series up front with your rating and your chapter, the next four below, your total chapters read, in story format. You can swap the “My top 5 manhwa” label for your own, for free.</p>', 1),
    ('<summary>Toonboxd est-il gratuit&nbsp;?<svg', '<summary>Is Toonboxd free?<svg', 1),
    ('<p>Oui, et sans publicité. La version gratuite suit jusqu’à 30 séries en cours, sans limite pour les séries prévues, en pause, terminées ou abandonnées, avec trois listes modifiables. Toonboxd Pro coûte 17,99&nbsp;€ par an ou 2,99&nbsp;€ par mois, avec 7 jours d’essai sur les deux formules à un premier abonnement.</p>',
     '<p>Yes, with no ads. The free version tracks up to 30 series you’re reading, with no limit on series in Plan to Read, On Hold, Completed or Dropped, and three editable lists. Toonboxd Pro is yearly or monthly, with 7 days free on both plans with a first subscription. The App Store shows the price in your currency.</p>', 1),
    ('<summary>Peut-on lire des chapitres dans l’app&nbsp;?<svg', '<summary>Can I read chapters in the app?<svg', 1),
    ('<p>Non. Toonboxd n’héberge aucun chapitre. Le bouton «&nbsp;Lire sur…&nbsp;» de chaque fiche ouvre la plateforme officielle où lire la série.</p>',
     '<p>No. Toonboxd hosts no chapters. The “Read on…” button on every series page opens the official platform where you can read it.</p>', 1),
    ('<summary>Faut-il créer un compte&nbsp;?<svg', '<summary>Do I need to create an account?<svg', 1),
    ('<p>Non. L’app crée un compte anonyme, sans email ni mot de passe. Tu peux le lier à ton identifiant Apple pour retrouver ta bibliothèque sur un autre iPhone, et le supprimer entièrement depuis les réglages.</p>',
     '<p>No. The app creates an anonymous account, with no email or password. You can link it to your Apple Account to get your library back on another iPhone, and delete it entirely from Settings.</p>', 1),
    ('<summary>Les mangas japonais sont-ils au catalogue&nbsp;?<svg', '<summary>Does Toonboxd have Japanese manga?<svg', 1),
    ('<p>Non, et c’est voulu&nbsp;: Toonboxd suit les manhwas, les manhuas et les webtoons. Si une série de ce genre manque, tu peux la suggérer depuis la recherche, gratuitement.</p>',
     '<p>No, and that’s on purpose: Toonboxd tracks manhwa, manhua and webtoons. No Japanese manga. If a series like these is missing, you can suggest it from Search, for free.</p>', 1),
    ('<summary>Toonboxd existe-t-il sur Android&nbsp;?<svg', '<summary>Is Toonboxd on Android?<svg', 1),
    ('<p>Android ensuite&nbsp;: Toonboxd sort d’abord sur iPhone, en France, et la version Android suit. Choisis Android en <a href="mailto:contact@toonboxd.app?subject=' + SUJET_EN + '" data-prevenir>t’inscrivant au lancement</a>&nbsp;: on t’écrit pour la bêta, puis le jour où elle arrive sur ton téléphone.</p>',
     '<p>Android is next: Toonboxd comes to iPhone first, and the Android version follows. Choose Android when you <a href="mailto:contact@toonboxd.app?subject=' + SUJET_EN + '" data-prevenir>sign up for the launch</a>: we’ll write to you for the beta, then on the day it arrives on your phone.</p>', 1),
    ('<summary>Quand sort Toonboxd&nbsp;?<svg', '<summary>When does Toonboxd come out?<svg', 1),
    ('<p>Toonboxd arrive bientôt sur l’App Store, et sur Android ensuite. Pour être prévenu, <a href="mailto:contact@toonboxd.app?subject=' + SUJET_EN + '" data-prevenir>laisse ton email</a> et choisis ton téléphone&nbsp;: on t’écrit pour la bêta, puis le jour où Toonboxd arrive sur ton téléphone. Rien d’autre.</p>',
     '<p>Toonboxd is coming soon to the App Store, and to Android after that. To hear about it, <a href="mailto:contact@toonboxd.app?subject=' + SUJET_EN + '" data-prevenir>leave your email</a> and choose your phone: we’ll write to you for the beta, then on the day Toonboxd arrives on your phone. Nothing else.</p>', 1),

    # ---------- L'appel final et le pied ----------
    ('<h2 class="h2" id="t-final"><span>Tous tes manhwas et webtoons.</span> <span>Un seul endroit.</span></h2>',
     '<h2 class="h2" id="t-final"><span>All your manhwa and webtoons.</span> <span>One place.</span></h2>', 1),
    ('<p class="lead">Toonboxd arrive bientôt sur l’App Store, en France. Android ensuite.</p>', '<p class="lead">Toonboxd is coming soon to the App Store. Android after that.</p>', 1),
    ('<a class="brand" href="/"><img', '<a class="brand" href="/en/"><img', 1),
    ('<p class="foot-tag">Le manhwa tracker et webtoon tracker en français, sur iPhone.</p>', '<p class="foot-tag">The manhwa tracker and webtoon tracker for iPhone.</p>', 1),
    ('<nav class="foot-links" aria-label="Liens utiles">\n        <a href="/confidentialite/">Confidentialité</a>\n        <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Conditions d’utilisation</a>',
     '<nav class="foot-links" aria-label="Useful links">\n        <a href="/privacy/">Privacy</a>\n        <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Terms of Use</a>', 1),
    # Le pied d'après la bascule du plan B (29 octobre 2026) : l'anglais du message
    # de docs/PLAN-B-CATALOGUE.md, dépôt de l'app.
    ('<p class="foot-small">Données des séries&nbsp;: MangaUpdates. Couvertures&nbsp;: la plateforme officielle de chaque série ou MangaUpdates&nbsp;; elles restent la propriété de leurs auteurs, studios et éditeurs. Toonboxd n’héberge aucun chapitre et renvoie toujours vers les sources officielles.</p>',
     '<p class="foot-small">Series data: MangaUpdates. Covers: each series’ official platform or MangaUpdates; they remain the property of their authors, studios and publishers. Toonboxd hosts no chapters and always points to official sources.</p>', 1),

    # ---------- La fenêtre d'inscription : les mêmes champs, la même fonction ----------
    ('data-fermer aria-label="Fermer">', 'data-fermer aria-label="Close">', 1),
    ('<h2 class="modal-titre" id="prevenir-titre">Sois prévenu du lancement</h2>', '<h2 class="modal-titre" id="prevenir-titre">Hear about the launch</h2>', 1),
    ('<p class="modal-texte">Laisse ton email&nbsp;: on t’écrit pour la bêta, puis le jour où Toonboxd arrive sur ton téléphone. Rien d’autre.</p>',
     '<p class="modal-texte">Leave your email: we’ll write to you for the beta, then on the day Toonboxd arrives on your phone. Nothing else.</p>', 1),
    ('<label class="modal-label" for="prevenir-email">Ton email</label>', '<label class="modal-label" for="prevenir-email">Your email</label>', 1),
    ('placeholder="toi@exemple.fr"', 'placeholder="you@example.com"', 1),
    ('<legend>Ton téléphone</legend>', '<legend>Your phone</legend>', 1),
    ('hidden>Toonboxd sort d’abord sur iPhone, Android ensuite&nbsp;: pour toi, le lancement, c’est le jour où il arrive sur Android.</p>',
     'hidden>Toonboxd comes to iPhone first, Android after that: for you, the launch is the day it arrives on Android.</p>', 1),
    ('<label for="prevenir-site">Laisse ce champ vide</label>', '<label for="prevenir-site">Leave this field empty</label>', 1),
    ('<button class="btn btn-primary modal-envoyer" type="submit">Me prévenir</button>', '<button class="btn btn-primary modal-envoyer" type="submit">Notify Me</button>', 1),
    ('id="prevenir-aide">Ton email et ton téléphone sont stockés à Paris et ne servent qu’à ces deux messages&nbsp;: la bêta, puis l’arrivée de Toonboxd sur ton téléphone. Ils sont effacés une fois le second parti, au plus tard 12 mois après ton inscription. Pour les retirer avant, écris à <a href="mailto:contact@toonboxd.app">contact@toonboxd.app</a>. <a href="/confidentialite/">Confidentialité</a></p>',
     'id="prevenir-aide">Your email and phone type are stored in Paris and used only for these two messages: the beta, then Toonboxd arriving on your phone. They’re erased once the second one goes out, and at the latest 12 months after you sign up. To remove them sooner, write to <a href="mailto:contact@toonboxd.app">contact@toonboxd.app</a>. <a href="/privacy/">Privacy</a></p>', 1),
    ('<h2 class="modal-titre">C’est noté.</h2>', '<h2 class="modal-titre">Got it.</h2>', 1),
    ('id="prevenir-merci">On t’écrit pour la bêta, puis le jour où Toonboxd arrive sur l’App Store.</p>',
     'id="prevenir-merci">We’ll write to you for the beta, then on the day Toonboxd arrives on the App Store.</p>', 1),
    ('<button class="btn btn-ghost modal-fin" type="button" data-fermer>Fermer</button>', '<button class="btn btn-ghost modal-fin" type="button" data-fermer>Close</button>', 1),
    ("var ECHEC = 'L’inscription n’a pas abouti. Réessaie, ou écris à contact@toonboxd.app.';",
     "var ECHEC = 'The sign-up didn’t go through. Try again, or write to contact@toonboxd.app.';", 1),
    ("var MERCI_IPHONE = 'On t’écrit pour la bêta, puis le jour où Toonboxd arrive sur l’App Store.';",
     "var MERCI_IPHONE = 'We’ll write to you for the beta, then on the day Toonboxd arrives on the App Store.';", 1),
    ("var MERCI_ANDROID = 'On t’écrit pour la bêta, puis le jour où Toonboxd arrive sur Android.';",
     "var MERCI_ANDROID = 'We’ll write to you for the beta, then on the day Toonboxd arrives on Android.';", 1),
    ("'Cette adresse n’a pas l’air valide.'", "'This email address doesn’t look right.'", 2),
    ("'Choisis ton téléphone : iPhone ou Android.'", "'Choose your phone: iPhone or Android.'", 1),
]

# Ce qui reste légitimement en français dans la page anglaise : le libellé et
# l'invitation qui mènent à la page française, dans sa langue.
FRANCAIS_PERMIS = {"Français", "Lire en français"}
MARQUES = re.compile(
    r"[éèêëàâùûçôîïœÉÈÊÀÇ]|\b(?:le|la|les|des|du|tu|ton|ta|tes|une|est|et|pour|avec|sans|dans|sur|pas|ce|cette|chapitres?|séries?|notre|votre)\b",
    re.I)


def generer(source):
    texte = source
    for fr, en, n in TABLE:
        trouve = texte.count(fr)
        if trouve != n:
            raise SystemExit(f"ÉCART : {trouve} occurrence(s) au lieu de {n} pour :\n  {fr[:160]}")
        texte = texte.replace(fr, en)
    return texte


class Squelette(HTMLParser):
    """La suite des balises ouvrantes et de leurs classes, sans texte ni autre attribut."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.suite = []

    def handle_starttag(self, balise, attrs):
        self.suite.append((balise, dict(attrs).get("class") or ""))


def squelette(html):
    s = Squelette(); s.feed(html); return s.suite


class Lu(HTMLParser):
    """Ce qu'un lecteur ou un moteur lit : textes visibles, attributs lus, JSON-LD et chaînes du script."""
    ATTRIBUTS = ("aria-label", "alt", "placeholder", "title")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.morceaux = []
        self.pile = []

    def handle_starttag(self, balise, attrs):
        a = dict(attrs)
        self.pile.append((balise, a.get("type")))
        for nom in self.ATTRIBUTS:
            if a.get(nom):
                self.morceaux.append(a[nom])
        if balise == "meta" and a.get("content") and (a.get("name") in ("description", "twitter:title", "twitter:description") or (a.get("property") or "").startswith("og:")):
            self.morceaux.append(a["content"])

    def handle_endtag(self, balise):
        while self.pile:
            if self.pile.pop()[0] == balise:
                break

    def handle_data(self, data):
        haut = self.pile[-1] if self.pile else (None, None)
        if haut[0] == "style":
            return
        if haut[0] == "script":
            if haut[1] == "application/ld+json":
                def valeurs(o):
                    if isinstance(o, dict):
                        for v in o.values(): yield from valeurs(v)
                    elif isinstance(o, list):
                        for v in o: yield from valeurs(v)
                    elif isinstance(o, str):
                        yield o
                self.morceaux.extend(valeurs(json.loads(data)))
            else:
                # Les commentaires restent en français, ce sont des notes de travail ;
                # seules les chaînes du script peuvent s'afficher.
                code = re.sub(r"/\*.*?\*/", "", data, flags=re.S)
                code = re.sub(r"(?<![:'\"])//[^\n]*", "", code)
                # Une chaîne sans espace est un sélecteur ou une valeur machine
                # ('data-pas', 'android'), jamais une phrase.
                self.morceaux.extend(s for s in re.findall(r"'([^'\n]*[A-Za-zÀ-ÿ][^'\n]*)'", code) if " " in s)
            return
        if data.strip():
            self.morceaux.append(data.strip())


def reste_de_francais(html):
    l = Lu(); l.feed(html)
    return [m for m in l.morceaux if m not in FRANCAIS_PERMIS and MARQUES.search(m)]


def controler(fr, en):
    defauts = []
    if squelette(fr) != squelette(en):
        a, b = squelette(fr), squelette(en)
        i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
        defauts.append(f"JUMEAUX : les squelettes divergent à la balise {i} ({a[i] if i < len(a) else 'fin'} contre {b[i] if i < len(b) else 'fin'})")
    for m in reste_de_francais(en):
        defauts.append(f"FRANÇAIS RESTANT : {m[:120]}")
    for c in (chr(0x2014), chr(0xB7)):  # le cadratin et le point médian, jamais écrits en clair
        if c in en:
            defauts.append(f"CARACTÈRE BANNI : U+{ord(c):04X}")
    return defauts


def main():
    fr = SOURCE.read_text(encoding="utf-8")
    en = generer(fr)
    if "--temoins" in sys.argv:
        # Trois forges, chacune doit faire tomber le contrôle qui la vise.
        sans_section = re.sub(r'<section class="section" id="listes".*?</section>', "", en, count=1, flags=re.S)
        assert any(d.startswith("JUMEAUX") for d in controler(fr, sans_section)), "le témoin des jumeaux ne tombe pas"
        oubli = en.replace("Your lists, open to everyone.", "Tes listes, lisibles par tous.", 1)
        assert any(d.startswith("FRANÇAIS") for d in controler(fr, oubli)), "le témoin du français restant ne tombe pas"
        banni = en.replace("One place.", "One place " + chr(0x2014) + " yours.", 1)
        assert any(d.startswith("CARACTÈRE") for d in controler(fr, banni)), "le témoin des caractères bannis ne tombe pas"
        print("témoins : les trois contrôles tombent sur leur forge")
    defauts = controler(fr, en)
    if defauts:
        raise SystemExit("\n".join(defauts))
    CIBLE.parent.mkdir(exist_ok=True)
    CIBLE.write_text(en, encoding="utf-8", newline="\n")
    print(f"en/index.html écrit : {len(TABLE)} remplacements, {len(squelette(en))} balises jumelles, aucun reste de français")


if __name__ == "__main__":
    main()
