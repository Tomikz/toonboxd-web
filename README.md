# Publier le site de `toonboxd.app`

Ce dossier est la **source** des pages web du produit. Il se copie tel quel dans un dépôt public séparé, servi par GitHub Pages sur le domaine apex `toonboxd.app`. Ouvert le 4 septembre 2026 avec l'étape 7.6, le partage des listes.

Aujourd'hui il ne porte qu'une page, `l/index.html`, la consultation publique d'une liste. Le site de la Phase 10 et la migration de `legal/` le rejoindront ici : `constants/Handle.ts` réserve déjà `confidentialite` et `cgu`, et un domaine se sert d'un seul dépôt.

**Le sens est source vers copie, et il n'y en a qu'un.** Une correction faite directement dans le dépôt public se transcrit ici **avant** tout autre changement, sinon la source ment et la recopie suivante écrase la correction. C'est la règle de `legal/README.md`, née d'une divergence réelle le 3 septembre 2026, et elle vaut d'autant plus ici que la page porte des valeurs substituées.

**Cette règle ne couvre qu'un sens, et le second est arrivé le 5 septembre 2026.** La copie servie était **en retard d'un commit** sur la source : publiée le 4 septembre à 16h17, elle a été modifiée après par le commit de titres 4, et la page rendait donc une liste sans le titre de son auteur. La règle du 3 septembre vise la copie **plus récente** que la source ; celle-ci était **plus ancienne**. **La condition qui rend ce sens probable est nommée** : tout commit qui touche `web/` après une copie la périme, et rien dans le dépôt ne le signale, un commit ne sachant pas ce qui a été publié.

**La parade est une comparaison et non une discipline, et c'est ce qui la rend meilleure que la règle qu'elle complète.** Une discipline demande de la vigilance et **échoue en silence quand elle manque** ; le contrôle de fraîcheur ci-dessous ne raisonne pas sur qui a écrit en dernier, donc **il ne peut pas se tromper de sens** et il est indifférent à celui du défaut. La discipline est reconduite, la comparaison est ce qui la garde honnête.

## Ce que la page contient, et pourquoi ce n'est pas une variable d'environnement

`l/index.html` porte en clair l'URL Supabase et la **clé anon**. Les deux sont substituées depuis `.env` au moment d'écrire le fichier, jamais lues à l'exécution : une page statique n'a pas d'environnement, et surtout **l'adresse et la clé de la page déployée doivent être vérifiables contre la source**, ce qu'un remplacement au moment de la copie interdirait.

**Sur la clé, l'argument est écrit dans le fichier et il se résume ici** : elle est déjà dans le bundle de l'app, donc rien de neuf ; ce qui change est qu'elle passe d'un binaire à dépaqueter à un « voir la source ». **La RLS est ce qui protège, jamais la clé.** Ce qu'elle donne : le catalogue, déjà ouvert en lecture par policy, et `liste_publique`, qui rend une liste publiée contre son code. Les contrôles ci-dessous le prouvent au lieu de l'affirmer.

## Publication

1. Un dépôt public, le **contenu** de ce dossier à sa racine (`l/`, `robots.txt`, `CNAME`, et ce `README.md`).
2. Settings, Pages, source « Deploy from a branch », branche `main`, dossier `/ (root)`.
3. Chez OVH, les quatre `A` de l'apex vers `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, et un `AAAA` si l'IPv6 est voulue. Le `CNAME` du dépôt porte déjà `toonboxd.app`.
4. Attendre le certificat (Settings, Pages, « Enforce HTTPS » devient cochable). Compter quelques minutes, parfois une heure.
5. Ce README est publié aussi, **servi brut à `/README.md`**. Sans conséquence, et sans secret : la clé qu'il commente est publique par conception. *(Cette ligne annonçait `/README.html` en supposant que Jekyll rendrait le Markdown. Mesuré le 5 septembre 2026 : `/README.html` rend `404` et `/README.md` rend `200` avec le fichier tel quel, ce dossier n'ayant pas de `_config.yml` et le fichier pas de front matter. **La correction vient du même instrument que le reste** : la supposition tenait depuis la première publication, et il a suffi de demander l'URL.)*

**Le jour où l'adresse change**, `constants/Sharing.ts` et la page déployée changent le même jour. Contrairement à la politique de confidentialité, **une adresse de partage est déjà dans les messages des lecteurs** : elle ne se change pas, elle se casse.

## Ce qui se vérifie avant de publier

- La bannière `TOONBOXD : la lecture publique d'une liste` est **jouée** dans `toonboxd-scripts/toonboxd-schema.sql`. Sans elle, `liste_publique` n'existe pas et la page rend « Cette liste n'est pas publique » sur un lien valide.
- Aucun `__SUPABASE` ne reste dans `l/index.html` : `grep -c '__SUPABASE' web/l/index.html` rend `0`.
- La clé substituée est bien l'**anon** et pas la `service_role` : son corps décodé porte `"role":"anon"`. La `service_role` contourne la RLS, donc la publier annulerait tout ce que cette étape a fermé. C'est le seul contrôle de ce fichier qui puisse causer un dommage irréversible s'il est sauté.
- La bannière `TOONBOXD : le titre de l'auteur sur la page publique` est **jouée** (titres 4, 4 septembre 2026). Sans elle, `liste_publique` ne rend pas `auteur_titre` et la page rend la liste **sans le titre**, silencieusement : c'est le cas dégradé que la prédiction de la bannière annonce, et il ne se voit que sur un auteur qui en porte un.
- Le **contrôle croisé des titres** ci-dessous rend zéro écart.

## Le contrôle de fraîcheur, à jouer APRÈS avoir copié

C'est le seul contrôle de ce fichier qui se joue **après** la publication, parce que c'est la copie qu'il mesure et non la source. Il est aussi le plus fort que ce dossier puisse porter : tout y est copié **tel quel**, donc l'artefact et la source sont le même fichier et un `diff` d'octets tranche sans interprétation.

**Il parcourt les fichiers, il ne les nomme pas**, et c'est la même leçon que ci-dessus d'un cran plus bas : une énumération oublie, un parcours non. La première version de ce contrôle ne regardait que `l/index.html`, et c'est précisément le fichier qui allait bien.

```bash
cd web
for f in $(find . -type f | sed 's|^\./||'); do
  code=$(curl -s -o /tmp/s.tmp -w '%{http_code}' "https://toonboxd.app/$f")
  if   [ "$code" != "200" ];        then echo "$f : HTTP $code"
  elif diff -q "$f" /tmp/s.tmp >/dev/null; then echo "$f : ok"
  else echo "$f : ECART $(diff "$f" /tmp/s.tmp | grep -c '^[<>]') lignes"; fi
done
```

**Une seule exemption, et elle est nommée plutôt que silencieuse** : `CNAME` rend `404`, et c'est correct. GitHub Pages le **consomme** comme configuration du domaine au lieu de le servir. Toute autre ligne qui n'est pas `ok` est un défaut.

**Relevé du 5 septembre 2026** : `l/index.html` ok (15 766 octets des deux côtés), `robots.txt` ok, `CNAME` 404 attendu, et **`README.md` en écart de 60 lignes, 5 604 octets servis contre 13 262 en source**. La copie de ce fichier-ci était donc périmée de **deux** commits, et personne ne l'avait vu.

**Son témoin, et sans lui un `diff` vide ne prouve rien** : il pourrait venir d'une commande qui ne compare rien, d'un fichier local vide, d'une URL qui rend une 404 de GitHub. Le témoin est le défaut réel, rejoué depuis l'historique :

```bash
git show 6eb6330~1:web/l/index.html > /tmp/avant.html   # la page avant le commit de titres 4
diff /tmp/avant.html /tmp/servie.html                    # DOIT etre non vide
```

**Relevé du 5 septembre 2026** : 10 495 octets contre 15 766, **101 lignes différentes**. Le contrôle aurait dit non au premier coup. Un témoin pris sur une vraie révision plutôt que sur un fichier forgé, parce qu'il en existait une.

**Quand le rejouer** : après chaque copie, et après tout commit qui touche `web/`. Le second cas est celui qui a mordu, deux fois.

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

Les quatre `diff` doivent être **vides**, et les cinq extractions doivent rendre **six lignes chacune** : une extraction qui rend zéro ou une ligne est un `diff` qui parle d'autre chose que d'une divergence. Le cas s'est produit à l'écriture, la dernière entrée d'un bloc JSON n'ayant pas de virgule finale, et le contrôle a rendu un écart pour un fichier juste. **Compter les lignes avant de lire les `diff`.**

**Les témoins, joués le 4 septembre 2026 avant de croire le zéro**, sur une copie du dépôt et sur trois forges d'une seule variation chacune : une teinte de la page passée de `#FF7C9B` à `#FF7C9C` fait tomber le premier `diff` ; un libellé passé de « Critique » à « Critiques » fait tomber le quatrième ; un code passé de `finisseur` à `finisseurs` fait tomber le premier et le deuxième. Chacun tombe sur la comparaison qui le vise, et la copie intacte rend zéro. **Sans ces trois, un zéro ne dit rien de plus qu'un `sed` qui ne trouve rien.**

## Ce que le rendu du bloc auteur a éprouvé, le 4 septembre 2026

**Ni `tsc` ni `lint` ne regardent ce fichier** (`tsconfig.json` n'inclut que `**/*.ts` et `**/*.tsx`), donc ils restent verts par construction et ne mesurent rien ici. Avec titres 4, `rendre()` a été exercé **hors navigateur**, en évaluant le `<script>` de la page sous un DOM de substitution en Node, sur les quatre cas que l'étape introduit : un auteur qui porte un titre (le libellé et sa classe sont posés), un auteur qui n'en porte pas (aucun élément de titre, pas de place creuse), un auteur sans pseudo (aucun bloc auteur, et le titre ne fuit nulle part), et quatre codes qui ne sont pas des clés propres, `constructor`, `toString`, `__proto__` et `eclaireur` (rien n'est rendu). Dix contrôles, tous passés.

**Deux témoins, parce qu'un harnais qui n'a jamais échoué ne mesure rien.** La garde ramenée à un test de vérité fait tomber trois des quatre cas de prototype, `__proto__` rendant même un objet comme texte ; et le titre déplacé hors du bloc auteur fait tomber le cas « sans pseudo ». *(Une première forme du second témoin cassait la garde de l'auteur au lieu de déplacer le titre : elle a levé une `TypeError` au lieu d'échouer sur un contrôle, ce qui ne prouvait rien. Une forge qui plante n'est pas un témoin.)*

**Sa limite, écrite comme une limite** : ce harnais n'a **pas de domicile permanent**, le dépôt n'ayant aucune infrastructure de test, donc c'est un relevé daté et non un instrument qui se rejouera tout seul. Ce qu'il ne couvre pas non plus : la mise en page réelle, qui se regarde en servant `web/` en local, et le déploiement, que rien n'éprouve tant que le domaine n'est pas pointé.

## Les deux instruments des caractères bannis

Le cadratin et le point médian sont bannis du projet (`CLAUDE.md`, *Critical Rules*). Ici la page n'est pas rendue par kramdown mais **par notre propre JavaScript**, donc le défaut peut naître au rendu comme il naissait à la conversion : la source serait propre et la page ne le serait pas. Les deux instruments restent, et le second porte sur l'artefact.

**Sur la source :**

```
printf '\xe2\x80\x94\n\xc2\xb7\n' > /tmp/bannis.txt
grep -rn -F -f /tmp/bannis.txt web/            # attendu : rien
grep -c  -F -f /tmp/bannis.txt CLAUDE.md       # témoin positif : > 0
```

**Sur la page publiée**, après déploiement, et **sur une liste réellement publiée** pour que le contenu rendu par le script soit dans la sortie :

```
URL='https://toonboxd.app/l/#<code d une liste publiee>'
printf 'a\xe2\x80\x94b\n' | grep -c -F -f /tmp/bannis.txt   # témoin forcé : 1
curl -sL 'https://toonboxd.app/l/' | grep -c -F 'Toonboxd'  # la page est la nôtre : > 0
curl -sL 'https://toonboxd.app/l/' | grep -n -F -f /tmp/bannis.txt   # attendu : rien
```

**Ce que `curl` ne voit pas, et il faut le dire** : le fragment n'est pas envoyé au serveur, donc `curl` rend toujours la page vide de contenu, avant l'appel. Le contenu rendu par le script se contrôle **dans le navigateur**, sur l'inspecteur, sur une liste dont le titre et la description contiennent les caractères cherchés, forgés exprès. Un `curl` seul sur cette page est un contrôle qui ne peut pas tomber, donc qui ne mesure rien.

## Ce que le contrôle de l'URL doit dire en premier

La règle du README de `toonboxd-scripts`, née le 3 septembre 2026 : **un contrôle qui interroge une URL dit d'abord d'où vient sa réponse.** Le contrôle de lecture fermée des listes a été joué une fois contre la page 404 de GitHub, qui porte un cadratin dans son pied : faux positif d'un côté, et de l'autre n'importe quelle recherche d'absence aurait rendu « conforme » sur une page qui ne contient rien de nous. D'où le `grep -c -F 'Toonboxd'` avant toute autre chose.
