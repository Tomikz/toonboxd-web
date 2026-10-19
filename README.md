# Publier le site de `toonboxd.app`

**Ce dépôt, `Tomikz/toonboxd-web`, est la source du site depuis le 16 octobre 2026** (décision de l'utilisateur ; `DECISIONS.md` §8 bis du dépôt de l'app, « Le site hors du dépôt »). Il est servi tel quel par GitHub Pages sur le domaine apex `toonboxd.app`. Jusque-là, il était la copie de `web/` du dépôt de l'app, ouvert le 4 septembre 2026 avec l'étape 7.6, le partage des listes ; `web/` reste figé à `963bcd4` et plus rien ne s'y écrit. **Ce qui vient encore du dépôt de l'app** : les deux politiques, dont la source reste `legal/`, et ce que l'app décide (le lexique, les libellés, les seuils, les couleurs), qu'elle relaie (`docs/PLAN-ANGLAIS.md`, commit 7). Ce fichier garde son histoire : là où il dit `web/`, il parle de ce qui est désormais ici.

Il porte deux pages. `l/index.html`, la consultation publique d'une liste, depuis le 4 septembre 2026 ; et depuis le 30 septembre 2026 `index.html`, la page d'accueil du domaine, avec ce qu'elle charge (`assets/fonts/`, `assets/img/` : l'icône, la bannière Nuit étoilée, l'avatar du Profil d'exemple et le logo de la signature de la carte, et depuis le 9 octobre 2026 `assets/img/profil/`, le cadre Roses et les pétales de son animation ; `favicon.png`, `apple-touch-icon.png`, `og.png`) et ce qui la fait trouver (`sitemap.xml`, et `robots.txt`, qui n'interdit plus que `/l/`). **La politique de confidentialité l'a rejoint le 16 octobre 2026**, à `/confidentialite/` en français et `/privacy/` en anglais (section suivante), deux mots que `constants/Handle.ts` réserve comme pseudos ; un domaine se sert d'un seul dépôt. **Et depuis le même jour, l'anglais** : `en/index.html`, la page d'accueil anglaise, générée depuis la française, son image de partage `og-en.png`, et `_outils/`, ce qui la génère et la contrôle, que Jekyll ne publie pas (section « La page anglaise »).

**Le sens est source vers copie, et il n'y en a qu'un.** Une correction faite directement dans le dépôt public se transcrit ici **avant** tout autre changement, sinon la source ment et la recopie suivante écrase la correction. C'est la règle de `legal/README.md`, née d'une divergence réelle le 3 septembre 2026, et elle vaut d'autant plus ici que la page porte des valeurs substituées.

**Cette règle ne couvre qu'un sens, et le second est arrivé le 5 septembre 2026.** La copie servie était **en retard d'un commit** sur la source : publiée le 4 septembre à 16h17, elle a été modifiée après par le commit de titres 4, et la page rendait donc une liste sans le titre de son auteur. La règle du 3 septembre vise la copie **plus récente** que la source ; celle-ci était **plus ancienne**. **La condition qui rend ce sens probable est nommée** : tout commit qui touche `web/` après une copie la périme, et rien dans le dépôt ne le signale, un commit ne sachant pas ce qui a été publié.

**La parade est une comparaison et non une discipline, et c'est ce qui la rend meilleure que la règle qu'elle complète.** Une discipline demande de la vigilance et **échoue en silence quand elle manque** ; le contrôle de fraîcheur ci-dessous ne raisonne pas sur qui a écrit en dernier, donc **il ne peut pas se tromper de sens** et il est indifférent à celui du défaut. La discipline est reconduite, la comparaison est ce qui la garde honnête.

**Depuis le 16 octobre 2026, le dépôt public EST la source** : il n'y a plus de copie à transcrire, et le contrôle de fraîcheur mesure ce que Pages sert contre ce que ce dépôt porte. La règle du sens unique vaut encore pour les deux politiques, dont la source est `legal/` du dépôt de l'app : une correction ne se fait jamais ici, elle se fait là-bas et se recopie.

## Les deux politiques de confidentialité, seul contenu que Jekyll rend

**Leur source n'est pas ce dossier, c'est `legal/`** (`legal/README.md`, Publication) : `legal/index.md` se recopie tel quel en `confidentialite/index.md` et `legal/en/index.md` en `privacy/index.md`, **directement dans le dépôt public**, jamais ici, pour qu'une politique n'ait qu'une source dans le dépôt de l'app. Ce dossier porte ce qui les met en page : `_config.yml`, qui donne aux deux dossiers le gabarit et la langue, et `_layouts/politique.html`, le gabarit, aux couleurs et à la police de la page d'accueil, avec le lien vers l'autre langue et les `hreflang` des deux. **Le gabarit ne charge rien d'ailleurs et n'a aucun script** : la politique dit que le site ne dépose aucun cookie et ne mesure rien, et ces deux pages en font partie. Tout le reste de ce dossier n'a pas de front matter et sort de Jekyll octet pour octet, comme avant.

## La page anglaise, sa jumelle générée, et la page de liste dans la langue du lecteur

**Depuis le 16 octobre 2026**, avec les règles du §2 point 10 de `docs/PLAN-ANGLAIS.md` (dépôt de l'app) : la 1.0 sort en France et dans six pays anglophones.

**`en/index.html` ne s'édite jamais à la main : `_outils/accueil-en.py` la génère depuis `index.html`.** Le script remplace chaque texte français par son anglais, une table de quelque deux cents remplacements dont chacun dit combien de fois il doit s'appliquer ; un texte changé dans la page française sans que sa traduction suive arrête le script. Les balises, les classes, le style et le script de la page restent donc ceux de la française par construction, et trois contrôles le vérifient sur la page produite : **les jumeaux** (la suite des balises et de leurs classes est la même des deux côtés), **le reste de français** (aucun texte visible, attribut lu, valeur des données structurées ni phrase du script, hors des deux libellés qui mènent au français) et **les deux caractères bannis**. `--temoins` forge un défaut par contrôle et vérifie que chacun tombe. **Les mots sont ceux de l'app** : le lexique et la forme de `DECISIONS.md` §5 (« L'anglais : le lexique et la forme »), et toute chaîne qui recopie un écran vient de `locales/en.json` (Currently Reading, Search what you’re reading, Plan to Read, On Hold, la notification « Nano Machine is back », les six titres…). Les noms des séries affichées sont leur `titre` du catalogue, identiques dans les deux langues pour celles de la page.

**Ce que la page anglaise ne fait pas** : afficher un montant (six devises ; la section des tarifs dit « The App Store shows the price in your currency. », et le JSON-LD garde seulement le prix nul du téléchargement) ; rediriger qui que ce soit. **Les deux pages se désignent** par `hreflang` (`fr`, `en`, et `x-default` vers l'anglaise), portent dans l'en-tête un lien vers l'autre langue (« English », « Français »), et une invitation (« Read in English », « Lire en français ») que le script ne montre que si la langue du navigateur n'est pas celle de la page, par la règle de l'app : la première des langues préférées que le site sait servir, l'anglais si aucune ne l'est. **L'inscription reste la même** : la même fonction, les mêmes champs, sans colonne de langue, le courriel de lancement devant être bilingue.

**`og-en.png`** se rend depuis `_outils/og-en.html` par `_outils/og.py` (Playwright, avec Edge déjà installé), sur le modèle de `og.png` : l'accroche anglaise et la notification de `en.json`.

**La page de liste suit la langue du navigateur**, par la même règle, un texte par langue posé par `textContent` : le compte, les messages de refus, le lien « Report This List » et son courriel, le pied, et les six titres (`TITRE_LIBELLE_EN`, recopiés de `en.json`, sous le contrôle croisé). Le titre d'une série suit `utils/serieAffichee.ts` : l'alias français en français, le `titre` du catalogue en anglais. Le titre et la description d'une liste, écrits par son auteur, ne se traduisent pas. **Une conséquence à porter côté app** : la politique anglaise cite le lien de signalement en français (« Signaler cette liste »), et un navigateur anglais lit désormais « Report This List ».

**Relevé du 16 octobre 2026, en local** (Edge piloté par Playwright, quatre langues de navigateur : `fr-FR`, `en-US`, `es-ES`, et `es-ES` puis `fr`) : l'invitation de chaque page d'accueil paraît exactement quand la langue servie n'est pas la sienne, et la page de liste, sur une réponse simulée de `liste_publique` (aucune requête vers la base), rend sa langue, son titre d'auteur (« Finisseur » ou « Completionist »), son compte, l'alias français ou le titre selon la langue, son lien et son sujet de courriel ; seize contrôles conformes. **Témoin** : le même script contre le site servi d'avant rend quatorze échecs. Aucun débordement horizontal à 1280 et à 375 px.

## Ce que la page contient, et pourquoi ce n'est pas une variable d'environnement

`l/index.html` porte en clair l'URL Supabase et la **clé anon**, et depuis le 30 septembre 2026 `index.html` porte **les mêmes**, pour lire les couvertures du catalogue. Les deux sont substituées depuis `.env` au moment d'écrire le fichier, jamais lues à l'exécution : une page statique n'a pas d'environnement, et surtout **l'adresse et la clé de la page déployée doivent être vérifiables contre la source**, ce qu'un remplacement au moment de la copie interdirait.

**Sur la clé, l'argument est écrit dans le fichier et il se résume ici** : elle est déjà dans le bundle de l'app, donc rien de neuf ; ce qui change est qu'elle passe d'un binaire à dépaqueter à un « voir la source ». **La RLS est ce qui protège, jamais la clé.** Ce qu'elle donne : le catalogue, déjà ouvert en lecture par policy, et `liste_publique`, qui rend une liste publiée contre son code. Les contrôles ci-dessous le prouvent au lieu de l'affirmer.

## La page d'accueil, et ce qu'elle refuse de charger

`index.html` est une page statique écrite à la main : pas de build, pas de framework, donc **l'artefact et la source restent le même fichier** et le contrôle de fraîcheur ci-dessous la couvre par un `diff` d'octets, comme `l/`. Ses sections : l'accroche (le suivi et le retour de hiatus réunis sur un écran Reprendre), la carte du top 5, les fonctionnalités, le retour de hiatus, le profil, les listes, les tarifs, la vie privée, les questions ; ses couleurs, sa police et ses textes sont ceux de l'app.

**Ce que la page charge, et d'où**, avec la même règle que `l/` pour la même raison, une page lue par des gens qui n'ont rien accepté : ni cookie, ni mesure d'audience, ni police d'un CDN. La police est Pretendard, les trois `.otf` de `assets/fonts/` du dépôt de l'app réduits au latin et convertis en woff2 (14 Ko chacun) ; le point médian et le cadratin ont été **laissés hors du sous-ensemble**. Les icônes sont celles de Phosphor (MIT), recopiées en symboles dans la page.

**Les couvertures passent par le chemin de l'app, et jamais par ce dossier.** La page lit la table `series` avec la clé anon, sur les colonnes de `LIST_COLUMNS` (`services/seriesService.ts`), de deux façons qui sont celles de l'app : par identifiant pour les séries désignées (`fetchSeriesByIds`, associées par `id` puisque `in` n'ordonne rien), et par popularité puis `id` pour les murs de couvertures (`fetchPopularSeries`, le collage de l'accueil de l'onboarding). L'image vient de l'adresse que porte `cover_url`, chez AniList, en variante `medium` (230 px de large, un tiers du poids de `large`) ; une adresse qui n'est pas celle d'AniList passe telle quelle. **Le repli n'est pas une branche** : le fond de chaque emplacement est le placeholder, la règle de `components/SeriesCover.tsx`, et un réseau mort laisse la page lisible. **Conséquence à connaître** : le visiteur contacte Supabase et AniList, comme sur une liste partagée ; rien n'y est mesuré, mais ce n'est plus une page qui ne parle qu'à son hébergeur.

**Une seule bannière illustrée, et à un seul endroit** (décisions de l'utilisateur, 30 septembre 2026) : la première version en portait six en décor, retirées ; la section Profil montre ensuite l'écran Profil de l'app dans un téléphone, avec la bannière Nuit étoilée, l'avatar du clan Hwasan (`assets/images/User-avatar.png` du dépôt de l'app, réduit à 144 px) et le titre porté Bêta-testeur. Les deux images sont copiées dans `assets/img/`. L'image de partage `og.png` ne porte ni bannière ni couverture.

**La carte du top 5 est une recopie, datée du 1er octobre 2026** (l'objet que les publicités montreront, décision de l'utilisateur) : sa géométrie vient de `constants/ShareCard.ts` (le cadre de 360 x 640, la carte à 16 du bord au rayon 23, le héros de 112 x 168 incliné à -4° avec sa lueur ambre, la rangée de quatre colonnes de 70 en creux `[0, 12, 12, 0]`, le total, la signature au logo de 22), ses couleurs de `components/Top5ShareCard.tsx`, ses textes de `shareCard.*` dans `locales/fr.json`, et ses séries de la vitrine de l'onboarding. **Le jour où la carte bouge dans l'app, cette section bouge le même jour** : une image de marque qui ne ressemble plus à celle que l'app exporte promettrait autre chose. Deux écarts, voulus : la pastille reprend l'avatar du Profil d'exemple plutôt que celle d'`Avatar`, pour qu'une page ne montre pas deux visages au même pseudo, et le cadre est arrondi, l'image exportée ayant des coins droits. L'iPhone du Profil porte l'oeil violet de la vitrine (`components/Top5Showcase.tsx`) à la place de « Modifier ».

**Le Profil d'exemple porte un cadre et une animation de Pro, recopiés le 9 octobre 2026** (demande de l'utilisateur : la page vendait les cadres et les animations sans en montrer un). Le cadre Roses vient de `components/CadreRoses.tsx` et de `constants/CadresGeometrie.ts` (la couronne de feuillage, cinq roses posées par angle et distance, six étoiles à quatre branches, sur l'avatar de 56 dans une boîte de 100), la pluie de pétales de `components/PluieDePetales.tsx`, à l'échelle 0,8 de l'écran : elle tombe quand l'écran Profil entre dans la page, comme à l'ouverture du profil, et se rejoue d'un toucher sur l'avatar. Les neuf images sont celles de l'app (`assets/images/cadres/roses/`, `assets/images/petales/`), réduites à environ trois fois leur taille affichée, la densité d'un écran d'iPhone : la couronne de 600 à 260 px, les roses à 64 px de large, les pétales à 96 px de haut, 53 Ko pour les neuf contre 245 Ko. Sous « Réduire les animations », le cadre reste immobile et la pluie ne tombe pas, comme dans l'app. **Le jour où le cadre ou la pluie bouge dans l'app, cette recopie bouge le même jour**, pour la raison de la carte.

**La page écrit une chose, et une seule** : l'email qu'un visiteur donne dans la fenêtre « Me prévenir du lancement », avec le téléphone qu'il choisit dans deux onglets (iPhone ou Android, `ios` ou `android` en base, depuis le 7 octobre 2026), par `inscrire_lancement` (bannière « les inscriptions au lancement » de `toonboxd-schema.sql`), avec la même clé anon. La table est fermée au client, lecture comprise, et une adresse déjà inscrite répond comme une nouvelle. Sans JavaScript, ou sans `<dialog>`, les boutons gardent leur lien `mailto:` vers `contact@toonboxd.app`. L'inventaire est `docs/COLLECTE.md` (section 2, `inscriptions_lancement`) et la politique porte une section « Sur le site toonboxd.app ». **Depuis le 9 octobre 2026, le téléphone choisit le message** (« Android ensuite » : le lancement sur iPhone d'abord, la sortie Android ensuite), et une adresse est effacée une fois son message parti, **au plus tard douze mois après l'inscription**, par une tâche `pg_cron` quotidienne (bannière « la durée des inscriptions au lancement »). **Depuis le 13 octobre 2026, la fenêtre promet deux messages et rien d'autre** (« On t'écrit pour la bêta, puis le jour où Toonboxd arrive sur ton téléphone. Rien d'autre. », demande de l'utilisateur) ; une inscription d'avant cette promesse reçoit aussi le message de la bêta, une seule fois, dans une version qui reconnaît l'exception et offre une désinscription par une réponse « STOP » (décision de l'utilisateur, sa raison dans `docs/COLLECTE.md`).

**Les textes qui ressemblent à l'app sont ceux de l'app** : la notification vient de `supabase/functions/envoyer-notifications/chaines.ts`, apostrophe droite comprise ; la boîte « Cette série a repris ? », la note de reprise, les deux recherches (« Cherche dans tes lectures » sur Reprendre, « Cherche un titre » dans le catalogue) et les titres viennent de `locales/fr.json`. **Depuis le 9 octobre 2026, la notification de l'accroche arrive, repart comme une bannière d'iOS et revient**, sur onze secondes : posée pour de bon, elle cachait l'en-tête et le champ de recherche de Reprendre. Sous « Réduire les animations », elle reste. Les seuils des titres (1 000, 5 000, 20 000 chapitres, 25 séries terminées, 20 notées) ont été relus dans `titres_profil` le 30 septembre 2026 ; **un seuil qui bouge est une migration, et cette page bouge avec elle**.

**Le prix par mois de la section des tarifs est celui de l'app, à l'identique** (13 octobre 2026, décision de l'utilisateur, dette 43 de `DECISIONS.md`) : « Soit 1,50 € par mois » doit être la ligne « soit … /mois » que la carte annuelle de l'app rend en euros. Le SDK de RevenueCat arrondissait vers le bas (17,99 / 12 = 1,4992, donc « 1,49 € » prédit, non mesuré) ; **le build 4 a tranché le 13 octobre 2026** : l'app calcule la ligne elle-même, au centime le plus proche, donc « 1,50 € », et cette page ne change pas. Elle suivrait, republiée sous le contrôle de fraîcheur, le jour où l'app dirait autre chose. Le 2,99 € mensuel et le 17,99 € annuel suivent le §3 de la même façon.

**Le bouton principal envoie un email à `contact@toonboxd.app`** (« Me prévenir du lancement »), et le badge « Bientôt sur l'App Store » n'est pas un lien : la fiche n'existe pas, et le §5 interdit de nommer une destination avant qu'elle existe. **Le commit qui a l'adresse de la fiche** remplace les trois boutons et le badge par le badge officiel d'Apple et son lien, et ajoute `downloadUrl` au JSON-LD de la page.

## Publication

1. Ce dépôt public, servi tel quel depuis sa racine (`index.html`, `en/`, `assets/`, `l/`, `favicon.png`, `apple-touch-icon.png`, `og.png`, `og-en.png`, `robots.txt`, `sitemap.xml`, `CNAME`, `_config.yml`, `_layouts/`, et ce `README.md`), **plus les deux politiques venues de `legal/` du dépôt de l'app** : `confidentialite/index.md` et `privacy/index.md`. `_outils/` n'est pas publié, Jekyll écartant les dossiers dont le nom commence par `_`. **Avant chaque commit qui touche `index.html`**, `py -3 _outils/accueil-en.py` régénère la jumelle, dans le même commit.
2. Settings, Pages, source « Deploy from a branch », branche `main`, dossier `/ (root)`.
3. Chez OVH, les quatre `A` de l'apex vers `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, et un `AAAA` si l'IPv6 est voulue. Le `CNAME` du dépôt porte déjà `toonboxd.app`.
4. Attendre le certificat (Settings, Pages, « Enforce HTTPS » devient cochable). Compter quelques minutes, parfois une heure.
5. Ce README est publié aussi, **servi brut à `/README.md`**. Sans conséquence, et sans secret : la clé qu'il commente est publique par conception. *(Cette ligne annonçait `/README.html` en supposant que Jekyll rendrait le Markdown. Mesuré le 5 septembre 2026 : `/README.html` rend `404` et `/README.md` rend `200` avec le fichier tel quel, ce dossier n'ayant pas de `_config.yml` et le fichier pas de front matter. **La correction vient du même instrument que le reste** : la supposition tenait depuis la première publication, et il a suffi de demander l'URL.)*

**Le jour où l'adresse change**, `constants/Sharing.ts` et la page déployée changent le même jour. Contrairement à la politique de confidentialité, **une adresse de partage est déjà dans les messages des lecteurs** : elle ne se change pas, elle se casse.

## Ce qui se vérifie avant de publier

- La bannière `TOONBOXD : la lecture publique d'une liste` est **jouée** dans `toonboxd-scripts/toonboxd-schema.sql`. Sans elle, `liste_publique` n'existe pas et la page rend « Cette liste n'est pas publique » sur un lien valide.
- La bannière `TOONBOXD : le téléphone des inscriptions au lancement` est **jouée AVANT de publier la page qui envoie le téléphone**. Sans elle, la page neuve appelle `inscrire_lancement` avec deux paramètres que l'ancienne signature ne connaît pas, PostgREST rend `404`, et chaque inscription échoue ; dans l'autre ordre rien ne casse, la signature neuve acceptant l'appel sans téléphone de la page d'avant.
- La bannière `TOONBOXD : les inscriptions au lancement` est **jouée**. Sans elle, `inscrire_lancement` n'existe pas, PostgREST rend `404`, et la fenêtre répond « L'inscription n'a pas abouti » à chaque envoi : rien ne se perd, mais rien ne s'inscrit.
- La bannière `TOONBOXD : la durée des inscriptions au lancement` est **jouée avant le 30 septembre 2027**, un an après la première inscription. Rien sur la page n'en dépend et son ordre avec la publication est libre ; mais la politique du 9 octobre 2026 promet l'effacement à douze mois, et c'est la tâche de cette bannière qui tient la promesse, pas une mémoire.
- `legal/` est **republiée avec sa section « Sur le site toonboxd.app »**, AVANT cette page : la fenêtre renvoie à la politique au moment où elle demande l'adresse, et une politique qui ne dit rien du site ferait de ce renvoi une promesse vide.
- `py -3 _outils/accueil-en.py --temoins` rend ses trois témoins tombés puis « aucun reste de français », et `git status` ne montre pas `en/index.html` modifié après lui : la jumelle publiée est celle de la page française publiée.
- Aucun `__SUPABASE` ne reste dans les pages : `grep -c '__SUPABASE' l/index.html index.html en/index.html` rend `0` pour les trois.
- **Les pages portent la même adresse et la même clé** : `diff <(sed -n "s/^const CLE_ANON = '\(.*\)';/\1/p" l/index.html) <(sed -n "s/^ *var CLE_ANON = '\(.*\)';/\1/p" index.html)` est vide, et la même forme sur `URL_BASE` ; la page anglaise les porte par construction. Relevé du 30 septembre 2026 : identiques.
- La clé substituée est bien l'**anon** et pas la `service_role`, dans les deux pages : son corps décodé porte `"role":"anon"`. La `service_role` contourne la RLS, donc la publier annulerait tout ce que cette étape a fermé. C'est le seul contrôle de ce fichier qui puisse causer un dommage irréversible s'il est sauté.
- La bannière `TOONBOXD : le titre de l'auteur sur la page publique` est **jouée** (titres 4, 4 septembre 2026). Sans elle, `liste_publique` ne rend pas `auteur_titre` et la page rend la liste **sans le titre**, silencieusement : c'est le cas dégradé que la prédiction de la bannière annonce, et il ne se voit que sur un auteur qui en porte un.
- Le **contrôle croisé des titres** ci-dessous rend zéro écart.

## Le contrôle de fraîcheur, à jouer APRÈS avoir copié

C'est le seul contrôle de ce fichier qui se joue **après** la publication, parce que c'est la copie qu'il mesure et non la source. Il est aussi le plus fort que ce dossier puisse porter : tout y est copié **tel quel**, donc l'artefact et la source sont le même fichier et un `diff` d'octets tranche sans interprétation.

**Il parcourt les fichiers, il ne les nomme pas**, et c'est la même leçon que ci-dessus d'un cran plus bas : une énumération oublie, un parcours non. La première version de ce contrôle ne regardait que `l/index.html`, et c'est précisément le fichier qui allait bien.

```bash
# À la racine de ce dépôt, depuis le 16 octobre 2026
for f in $(git ls-files); do
  case "$f" in CNAME|_config.yml|_layouts/*|_outils/*|confidentialite/index.md|privacy/index.md) echo "$f : exempté"; continue;; esac
  code=$(curl -s -o /tmp/s.tmp -w '%{http_code}' "https://toonboxd.app/$f")
  if   [ "$code" != "200" ];        then echo "$f : HTTP $code"
  elif git show "HEAD:$f" | cmp -s - /tmp/s.tmp; then echo "$f : ok"
  else echo "$f : ECART"; fi
done
```

**Les exemptions sont nommées plutôt que silencieuses** : `CNAME` rend `404`, et c'est correct, GitHub Pages le **consomme** comme configuration du domaine au lieu de le servir ; depuis le 16 octobre 2026, `_config.yml` et `_layouts/politique.html` rendent `404` pour la même raison, Jekyll les consommant, et `_outils/` n'est pas publié ; la boucle les nomme comme exemptés au lieu de les taire. `en/index.html` et `og-en.png` sont dans la boucle comme les autres. Toute autre ligne qui n'est pas `ok` est un défaut. **Les deux politiques ne sont pas dans cette boucle**, leurs sources étant dans `legal/` et leur page servie du HTML rendu : elles se contrôlent par les phrases de `legal/README.md` sous leur témoin, et par l'absence de tout script et de toute ressource d'un autre domaine sur la page servie (`grep -c '<script'` à 0, sous le témoin de la page d'accueil, qui en a).

**La source est le contenu enregistré, `git show HEAD:web/$f`, et non le fichier du dossier** (depuis le 9 octobre 2026). Sous Windows, `core.autocrlf` met des fins de ligne CRLF dans la copie de travail, et `git archive` en met autant : la boucle d'avant, qui comparait le fichier du dossier, rendait un écart sur chaque fichier texte d'une page servie juste, un octet par ligne. C'est la leçon du 1er octobre 2026 sur le clone public, portée ici sur la source ; `HEAD` doit être le commit copié.

**Relevé du 5 septembre 2026** : `l/index.html` ok (15 766 octets des deux côtés), `robots.txt` ok, `CNAME` 404 attendu, et **`README.md` en écart de 60 lignes, 5 604 octets servis contre 13 262 en source**. La copie de ce fichier-ci était donc périmée de **deux** commits, et personne ne l'avait vu.

**Relevé du 30 septembre 2026**, à la publication de la page d'accueil (la copie du commit `dddc17b`) : quinze fichiers, tous `ok` octet pour octet, sauf `CNAME` (`404`, l'exemption attendue) ; témoin pris sur le `robots.txt` d'avant la page (`HEAD~1`), qui rend un écart. **Avant la copie, les deux sens ont été comparés** : `l/index.html` et `robots.txt` servis étaient identiques à leur source, et le `README.md` servi était celui du commit `9e939e8` (5 septembre 2026), une copie en retard et non une correction faite en ligne ; il est recopié, ce relevé compris. Côté `legal/`, le même jour : `index.md` servi déjà identique à la source, section « Sur le site toonboxd.app » comprise, `README.md` en retard et recopié. **Depuis le domaine réel** : les 56 emplacements de couverture reçoivent leur image, aucune en erreur ; `inscrire_lancement` répond `400` (22023) à une adresse mal formée, donc la fonction existe et la requête passe depuis `toonboxd.app`, sans rien écrire ; `/l/` répond `200`, porte `noindex`, et est la nôtre.

**Relevé du 1er octobre 2026**, à la publication de la carte du top 5 (la copie du commit `b097cc0`) : la copie servie était identique, contenu enregistré contre contenu enregistré, à la source publiée la veille ; **une comparaison sur la copie de travail du clone rendait cinq faux écarts**, les fins de ligne que Git convertit sous Windows, et c'est la comparaison des contenus enregistrés (`git show`) qui tranche. Après la copie : seize fichiers `ok` octet pour octet, `CNAME` à `404` ; témoin pris sur l'`index.html` de la veille, qui rend un écart. Depuis le domaine réel, les cinq couvertures de la carte, son avatar et son logo chargés, aucune erreur.

**Relevé du 7 octobre 2026**, à la publication du téléphone dans la fenêtre d'inscription, dans l'ordre que la page exige : la bannière du téléphone jouée d'abord, puis contrôlée de l'extérieur par trois appels qui n'écrivent rien (un téléphone `windows` refusé en 400, l'appel sans téléphone de la page d'avant résolu, un paramètre inconnu rendu en 404 pour témoin) ; la politique republiée ensuite et relue en ligne (« iPhone ou Android » présent, date du 7 octobre, aucun caractère banni ni entité) ; la page enfin. Avant chaque copie, les deux sens comparés sur les contenus enregistrés : aucune correction en ligne, le `README.md` de `legal/` seulement en retard. Après la copie de la page, quinze fichiers `ok` et `CNAME` à `404`, sous témoin. **Sur le domaine réel, une barre de défilement horizontale de 15 px restait sous la fenêtre** sans que rien ne déborde (`scrollWidth` égal à `clientWidth`), et disparaissait au premier recalcul : la fenêtre interdit désormais le défilement horizontal, et la page est republiée avec ce remède.

**Relevé du 9 octobre 2026**, à la publication de « Android ensuite », des tarifs Pro de l'app, de la recherche, des épinglées, du cadre et de la pluie (la copie du commit `53e8c6b`) : avant chaque copie, les deux sens comparés sur les contenus enregistrés, la politique et la page servies identiques à la source d'avant (`53e8c6b~1`), donc ni correction en ligne ni copie en retard, sous deux témoins (la page de `91d3e88` et la politique neuve rendent chacune un écart). La politique publiée d'abord et relue en ligne (date du 9 octobre, « douze mois après ton inscription », aucun caractère banni), la page ensuite. Après la copie : vingt-cinq fichiers, vingt-quatre `ok` et `CNAME` à `404` ; témoin pris sur l'`index.html` de `aab7953`, qui rend un écart de 167 lignes. **La première boucle, sur un `git archive` du commit, a rendu cinq faux écarts**, les cinq fichiers texte, chacun plus long d'un octet par ligne (682 octets contre 668 pour les 14 lignes de `robots.txt`) : la même page comparée aux contenus enregistrés est `ok` partout, et la boucle ci-dessus compare désormais ceux-là. Depuis le domaine réel : `inscrire_lancement` rend toujours `400` (22023) à une adresse mal formée, sans rien écrire ; les sept images du cadre et les pétales répondent `200` en `image/webp` et se décodent ; aucune erreur dans la console. **La bannière « la durée des inscriptions au lancement » n'est pas encore jouée**, et rien n'en dépend avant le 30 septembre 2027.

**Relevé du 16 octobre 2026**, à la publication des deux politiques sur le site (la copie du commit `99f1d45`, `legal/` comprise) : avant la copie, la page servie identique à la source d'avant, sauf `README.md`, en retard (la source de `18d6c38`) ; `l/index.html` avait été publié à la main sur GitHub le 14 octobre et était identique à sa source. Après la copie : vingt-quatre fichiers `ok`, `CNAME`, `_config.yml` et `_layouts/politique.html` à `404`, témoin pris sur l'`index.html` de `36a902c`, qui rend un écart de 6 lignes ; les trois liens de la page d'accueil vers la politique pointent `/confidentialite/`, et plus aucun vers l'ancienne adresse. Les deux politiques rendues se contrôlent dans `legal/README.md` (relevé du déménagement).

**Relevé du 19 octobre 2026**, à la recopie des deux politiques datées du 19 octobre (`957837b` du dépôt de l'app, publiée ici par `e70c3d0`) : avant la copie, les deux pages servies étaient la source de `99f1d45`, donc ni correction en ligne ni rien à reporter ; après, les deux fichiers enregistrés identiques à leur source. Sur les pages rendues, sous leurs témoins (2 et 2) : « 19 octobre 2026 » et « October 19, 2026 » à 2 chacune (la date en tête et la ligne datée), « ou en anglais » et « or in French » à 2, « les notifications arrivent dans la langue » et « notifications arrive in the language » à 1, plus aucune date du 16 en tête ; aucun caractère banni ni entité (témoin tiers 5, témoin forcé 1), aucun script. Le reste du site : vingt-six fichiers `ok`. L'ancienne adresse conduit toujours aux deux pages.

**Relevé du 13 octobre 2026**, à la publication de la promesse « On t'écrit pour la bêta, puis le jour où Toonboxd arrive sur ton téléphone. Rien d'autre. » (la copie du commit `5da1f73`) : avant chaque copie, les deux sens comparés sur les contenus enregistrés, la page servie identique à la source d'avant (`5da1f73~1`) et la politique à celle de `fb1eb86`, republiée le matin même par une autre session ; témoin, la politique neuve rend un écart. La politique publiée d'abord (07:24 UTC) et relue en ligne, la page ensuite (poussée à 07:25:19 UTC, **vue servie à 07:26:13 UTC**). Après la copie : vingt-quatre fichiers `ok` et `CNAME` à `404` ; témoin pris sur l'`index.html` de `3d2444c`, qui rend un écart de 20 lignes ; « une seule fois » absent de la page servie, « Rien d’autre » présent trois fois, aucun caractère banni. **L'heure vue servie est la borne des deux versions du message de la bêta** (d'abord écrite comme la borne de ses destinataires, une exclusion que l'utilisateur a remplacée le même jour) : une inscription d'avant n'avait accepté que le message de lancement, et reçoit la version qui le dit ; le bloc 4 de la bannière « la durée des inscriptions au lancement » rend toutes les adresses, avec la version à envoyer.

**Son témoin, et sans lui un `diff` vide ne prouve rien** : il pourrait venir d'une commande qui ne compare rien, d'un fichier local vide, d'une URL qui rend une 404 de GitHub. Le témoin est le défaut réel, rejoué depuis l'historique :

```bash
git show 6eb6330~1:web/l/index.html > /tmp/avant.html   # la page avant le commit de titres 4
diff /tmp/avant.html /tmp/servie.html                    # DOIT etre non vide
```

**Relevé du 5 septembre 2026** : 10 495 octets contre 15 766, **101 lignes différentes**. Le contrôle aurait dit non au premier coup. Un témoin pris sur une vraie révision plutôt que sur un fichier forgé, parce qu'il en existait une.

**Quand le rejouer** : après chaque copie, et après tout commit qui touche `web/`. Le second cas est celui qui a mordu, deux fois. Depuis le 16 octobre 2026 : après chaque `push` de ce dépôt.

## Le contrôle croisé des titres

La page recopie **six teintes** de `components/TitreText.tsx` et **six libellés** de `locales/fr.json` (`profile.title.*`), pour la raison que le fichier porte : elle vit dans un autre dépôt et ne peut rien importer. C'est la même recopie assumée que les jetons de charte de `constants/Colors.tsx`, avec une conséquence qui n'est pas la même des deux côtés : **un libellé qui diverge ment, une couleur qui diverge décore mal.** La seule parade à une recopie est un instrument qui la compare, jamais une note, et c'est celui-ci.

Il compare quatre choses : les codes et les teintes de la page contre le record privé de `TitreText.tsx` ; les codes de la page contre `ROSTER` de `constants/Titres.ts`, dans l'ordre ; les codes de la table des libellés contre ce même `ROSTER` ; et les six libellés de la page contre les six valeurs de `locales/fr.json`. Les clés du fichier de locales sont en anglais là où les codes sont français, donc la comparaison porte sur les **valeurs en ordre de roster**, et c'est ce que `ROSTER` et le `switch` de `titreLabel` garantissent des deux côtés.

```bash
P=web/l/index.html
sed -n "s/^ *\.titre-auteur\.\([a-z_]*\) *{ color: \(#[0-9A-Fa-f]*\); }/\1 \2/p" "$P"                      > /tmp/page-teintes
sed -n "s/^  \([a-z_]*\): '\(#[0-9A-Fa-f]*\)',$/\1 \2/p" components/TitreText.tsx                          > /tmp/app-teintes
sed -n "/^export const ROSTER/,/^];/s/^  '\([a-z_]*\)',$/\1/p" constants/Titres.ts                         > /tmp/roster
sed -n "/^const TITRE_LIBELLE/,/^};/s/^  \([a-z_]*\): '\(.*\)',$/\1 \2/p" "$P"                             > /tmp/page-libelles
sed -n '/^    "title": {$/,/^    },$/s/^      "[a-zA-Z]*": "\(.*\)",\?$/\1/p' locales/fr.json              > /tmp/loc-libelles

diff /tmp/page-teintes /tmp/app-teintes
diff <(cut -d' ' -f1 /tmp/page-teintes)  /tmp/roster
diff <(cut -d' ' -f1 /tmp/page-libelles) /tmp/roster
diff <(cut -d' ' -f2- /tmp/page-libelles) /tmp/loc-libelles
```

**La page d'accueil recopie les mêmes six teintes et les mêmes six libellés** (la galerie du profil), et depuis le 30 septembre 2026 le contrôle la couvre aussi. Ses deux extractions, qui remplacent les deux premières ci-dessus avant de rejouer les quatre `diff` :

```bash
P=web/index.html
sed -n "s/^ *\.titre-\([a-z_]*\) *{ color: \(#[0-9A-Fa-f]*\); }/\1 \2/p" "$P"                              > /tmp/page-teintes
sed -n 's/.*data-titre="\([a-z_]*\)"><b class="titre-[a-z_]*">\([^<]*\)<\/b>.*/\1 \2/p' "$P"                > /tmp/page-libelles
```

L'attribut `data-titre` n'est porté que par les six entrées de la galerie : le même nom de titre apparaît ailleurs dans la page (sous le pseudo des deux exemples), et une extraction sur la seule classe rendrait sept lignes. **Joué le 30 septembre 2026** : six lignes par extraction, quatre `diff` vides ; témoins, une teinte passée de `#FF7C9B` à `#FF7C9C` et « Critique » passé à « Critiques » font tomber chacun la comparaison qui le vise.

Les quatre `diff` doivent être **vides**, et les cinq extractions doivent rendre **six lignes chacune** : une extraction qui rend zéro ou une ligne est un `diff` qui parle d'autre chose que d'une divergence. Le cas s'est produit à l'écriture, la dernière entrée d'un bloc JSON n'ayant pas de virgule finale, et le contrôle a rendu un écart pour un fichier juste. **Compter les lignes avant de lire les `diff`.**

**L'anglais, depuis le 16 octobre 2026.** La page de liste porte les six libellés anglais dans `TITRE_LIBELLE_EN`, et la page anglaise sa galerie : les mêmes quatre `diff`, contre `locales/en.json`. Les commandes se lancent **depuis la racine du dépôt de l'app**, ce dépôt-ci à côté (`S`), puisque les fichiers de l'app y sont :

```bash
S=../toonboxd-web
sed -n '/^    "title": {$/,/^    },$/s/^      "[a-zA-Z]*": "\(.*\)",\?$/\1/p' locales/en.json                    > /tmp/loc-libelles
sed -n "/^const TITRE_LIBELLE_EN = {/,/^};/s/^  \([a-z_]*\): '\(.*\)',$/\1 \2/p" "$S/l/index.html"            > /tmp/page-libelles
# puis, pour la page anglaise :
sed -n 's/.*data-titre="\([a-z_]*\)"><b class="titre-[a-z_]*">\([^<]*\)<\/b>.*/\1 \2/p' "$S/en/index.html"     > /tmp/page-libelles
```

**Joué le 16 octobre 2026** sur les quatre pages (la liste en français et en anglais, les deux accueils) : six lignes par extraction, seize `diff` vides ; témoin, les libellés anglais de la page comparés à `fr.json` rendent dix lignes d'écart.

**Les témoins, joués le 4 septembre 2026 avant de croire le zéro**, sur une copie du dépôt et sur trois forges d'une seule variation chacune : une teinte de la page passée de `#FF7C9B` à `#FF7C9C` fait tomber le premier `diff` ; un libellé passé de « Critique » à « Critiques » fait tomber le quatrième ; un code passé de `finisseur` à `finisseurs` fait tomber le premier et le deuxième. Chacun tombe sur la comparaison qui le vise, et la copie intacte rend zéro. **Sans ces trois, un zéro ne dit rien de plus qu'un `sed` qui ne trouve rien.**

## Ce que le rendu du bloc auteur a éprouvé, le 4 septembre 2026

**Ni `tsc` ni `lint` ne regardent ce fichier** (`tsconfig.json` n'inclut que `**/*.ts` et `**/*.tsx`), donc ils restent verts par construction et ne mesurent rien ici. Avec titres 4, `rendre()` a été exercé **hors navigateur**, en évaluant le `<script>` de la page sous un DOM de substitution en Node, sur les quatre cas que l'étape introduit : un auteur qui porte un titre (le libellé et sa classe sont posés), un auteur qui n'en porte pas (aucun élément de titre, pas de place creuse), un auteur sans pseudo (aucun bloc auteur, et le titre ne fuit nulle part), et quatre codes qui ne sont pas des clés propres, `constructor`, `toString`, `__proto__` et `eclaireur` (rien n'est rendu). Dix contrôles, tous passés.

**Deux témoins, parce qu'un harnais qui n'a jamais échoué ne mesure rien.** La garde ramenée à un test de vérité fait tomber trois des quatre cas de prototype, `__proto__` rendant même un objet comme texte ; et le titre déplacé hors du bloc auteur fait tomber le cas « sans pseudo ». *(Une première forme du second témoin cassait la garde de l'auteur au lieu de déplacer le titre : elle a levé une `TypeError` au lieu d'échouer sur un contrôle, ce qui ne prouvait rien. Une forge qui plante n'est pas un témoin.)*

**Sa limite, écrite comme une limite** : ce harnais n'a **pas de domicile permanent**, le dépôt n'ayant aucune infrastructure de test, donc c'est un relevé daté et non un instrument qui se rejouera tout seul. Ce qu'il ne couvre pas non plus : la mise en page réelle, qui se regarde en servant `web/` en local, et le déploiement, que rien n'éprouve tant que le domaine n'est pas pointé.

## Les deux instruments des caractères bannis

Le cadratin et le point médian sont bannis du projet (`CLAUDE.md`, *Critical Rules*). Ici la page n'est pas rendue par kramdown mais **par notre propre JavaScript**, donc le défaut peut naître au rendu comme il naissait à la conversion : la source serait propre et la page ne le serait pas. Les deux instruments restent, et le second porte sur l'artefact.

**Sur la source :**

Le fichier de motifs `/tmp/bannis.txt` se construit par la forme des *Critical Rules* de `CLAUDE.md`, son seul domicile, jamais par un `printf` à échappements, qui a menti le 5 septembre 2026 et survivait dans ce fichier jusqu'au 29 septembre 2026 (`DECISIONS.md` §5). La recopier ici mettrait les deux caractères dans `web/`, dont le balayage attend « rien ».

```
od -An -tx1 /tmp/bannis.txt                                          # attendu : e2 80 94 0a c2 b7 0a
grep -c -F -f /tmp/bannis.txt node_modules/react-native/README.md   # témoin tiers, AVANT : 5
git ls-files -z --cached --others --exclude-standard web/ | xargs -0 grep -n -I -F -f /tmp/bannis.txt   # attendu : rien
```

**Le `-I` est né le 30 septembre 2026 avec la page d'accueil, et il n'est pas une tolérance.** Sa première version portait six illustrations, et le balayage sans lui rendait « Binary file ... matches » sur quatre fichiers (trois `.webp` et `og.png`) : des octets compressés qui forment la séquence par hasard, deux octets sur des dizaines de milliers, et aucun texte. Ces illustrations sont parties le jour même et plus aucun binaire ne matche, **mais le suivant le pourra** : `-I` écarte les binaires et garde tout le texte. **Son témoin, joué ce jour-là** : un fichier texte forgé dans `web/` avec un cadratin est trouvé par `grep -rnI`, puis retiré.

**Sur la page publiée**, après déploiement, et **sur une liste réellement publiée** pour que le contenu rendu par le script soit dans la sortie :

```
URL='https://toonboxd.app/l/#<code d une liste publiee>'
grep -c -F -f /tmp/bannis.txt node_modules/react-native/README.md   # témoin tiers : 5
curl -sL 'https://toonboxd.app/l/' | grep -c -F 'Toonboxd'  # la page est la nôtre : > 0
curl -sL 'https://toonboxd.app/l/' | grep -n -F -f /tmp/bannis.txt   # attendu : rien
```

**Ce que `curl` ne voit pas, et il faut le dire** : le fragment n'est pas envoyé au serveur, donc `curl` rend toujours la page vide de contenu, avant l'appel. Le contenu rendu par le script se contrôle **dans le navigateur**, sur l'inspecteur, sur une liste dont le titre et la description contiennent les caractères cherchés, forgés exprès. Un `curl` seul sur cette page est un contrôle qui ne peut pas tomber, donc qui ne mesure rien.

## Ce que le contrôle de l'URL doit dire en premier

La règle du README de `toonboxd-scripts`, née le 3 septembre 2026 : **un contrôle qui interroge une URL dit d'abord d'où vient sa réponse.** Le contrôle de lecture fermée des listes a été joué une fois contre la page 404 de GitHub, qui porte un cadratin dans son pied : faux positif d'un côté, et de l'autre n'importe quelle recherche d'absence aurait rendu « conforme » sur une page qui ne contient rien de nous. D'où le `grep -c -F 'Toonboxd'` avant toute autre chose.
