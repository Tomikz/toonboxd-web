# Publier le site de `toonboxd.app`

Ce dossier est la **source** des pages web du produit. Il se copie tel quel dans un dépôt public séparé, servi par GitHub Pages sur le domaine apex `toonboxd.app`. Ouvert le 4 septembre 2026 avec l'étape 7.6, le partage des listes.

Aujourd'hui il ne porte qu'une page, `l/index.html`, la consultation publique d'une liste. Le site de la Phase 10 et la migration de `legal/` le rejoindront ici : `constants/Handle.ts` réserve déjà `confidentialite` et `cgu`, et un domaine se sert d'un seul dépôt.

**Le sens est source vers copie, et il n'y en a qu'un.** Une correction faite directement dans le dépôt public se transcrit ici **avant** tout autre changement, sinon la source ment et la recopie suivante écrase la correction. C'est la règle de `legal/README.md`, née d'une divergence réelle le 3 septembre 2026, et elle vaut d'autant plus ici que la page porte des valeurs substituées.

## Ce que la page contient, et pourquoi ce n'est pas une variable d'environnement

`l/index.html` porte en clair l'URL Supabase et la **clé anon**. Les deux sont substituées depuis `.env` au moment d'écrire le fichier, jamais lues à l'exécution : une page statique n'a pas d'environnement, et surtout **l'adresse et la clé de la page déployée doivent être vérifiables contre la source**, ce qu'un remplacement au moment de la copie interdirait.

**Sur la clé, l'argument est écrit dans le fichier et il se résume ici** : elle est déjà dans le bundle de l'app, donc rien de neuf ; ce qui change est qu'elle passe d'un binaire à dépaqueter à un « voir la source ». **La RLS est ce qui protège, jamais la clé.** Ce qu'elle donne : le catalogue, déjà ouvert en lecture par policy, et `liste_publique`, qui rend une liste publiée contre son code. Les contrôles ci-dessous le prouvent au lieu de l'affirmer.

## Publication

1. Un dépôt public, le **contenu** de ce dossier à sa racine (`l/`, `robots.txt`, `CNAME`).
2. Settings, Pages, source « Deploy from a branch », branche `main`, dossier `/ (root)`.
3. Chez OVH, les quatre `A` de l'apex vers `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, et un `AAAA` si l'IPv6 est voulue. Le `CNAME` du dépôt porte déjà `toonboxd.app`.
4. Attendre le certificat (Settings, Pages, « Enforce HTTPS » devient cochable). Compter quelques minutes, parfois une heure.
5. Ce README est publié aussi (Jekyll rend tout `.md`), à `/README.html`. Sans conséquence, et sans secret : la clé qu'il commente est publique par conception.

**Le jour où l'adresse change**, `constants/Sharing.ts` et la page déployée changent le même jour. Contrairement à la politique de confidentialité, **une adresse de partage est déjà dans les messages des lecteurs** : elle ne se change pas, elle se casse.

## Ce qui se vérifie avant de publier

- La bannière `TOONBOXD : la lecture publique d'une liste` est **jouée** dans `toonboxd-scripts/toonboxd-schema.sql`. Sans elle, `liste_publique` n'existe pas et la page rend « Cette liste n'est pas publique » sur un lien valide.
- Aucun `__SUPABASE` ne reste dans `l/index.html` : `grep -c '__SUPABASE' web/l/index.html` rend `0`.
- La clé substituée est bien l'**anon** et pas la `service_role` : son corps décodé porte `"role":"anon"`. La `service_role` contourne la RLS, donc la publier annulerait tout ce que cette étape a fermé. C'est le seul contrôle de ce fichier qui puisse causer un dommage irréversible s'il est sauté.

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
