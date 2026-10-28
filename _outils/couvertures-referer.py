"""
LES HÔTES DES COUVERTURES ACCEPTENT-ILS UNE PAGE WEB ? (28 octobre 2026)

Après la bascule du plan B, les couvertures viennent de deux hôtes : les
serveurs d'images de Webtoon (swebtoon-phinf.pstatic.net, le CDN de Naver) et
celui de MangaUpdates (cdn.mangaupdates.com). L'app les charge sans en-tête
Referer ; une page web envoie le sien, et un CDN qui filtre les images liées
depuis un autre site la refuserait. Ce script charge de vraies adresses des
deux hôtes, celles que la bascule écrit en base (toonboxd-scripts,
planb/sortie/chargement.jsonl, relevées le 28 octobre 2026), deux fois chacune :
avec le Referer par défaut du navigateur, puis avec referrerpolicy="no-referrer".

Deux origines, et rien n'est publié pour autant : la page de test est servie
par une interception de Playwright, à http://localhost:4178/ (le Referer est
localhost) et à https://toonboxd.app/ (le vrai Referer du domaine, le cas de la
mise en ligne). Chaque variante a son propre contexte, donc son propre cache :
une image déjà chargée ne repart pas avec l'autre politique.

Pour chaque image : le statut HTTP, le Referer réellement envoyé (lu sur la
requête) et la largeur décodée. Le témoin : une adresse inexistante sur chacun
des deux hôtes doit échouer, sinon le test ne sait pas voir un échec.

Usage : python _outils/couvertures-referer.py   (Playwright, Edge déjà installé)
Une poignée de requêtes d'images vers les deux CDN, aucune vers l'API de MangaUpdates.
"""
import json
from playwright.sync_api import sync_playwright

ADRESSES = [
    ("webtoon", "https://swebtoon-phinf.pstatic.net/20200802_112/1596323433813lDg4V_JPEG/11_EC8DB8EB84A4EC9DBC_mobile.jpg"),
    ("webtoon", "https://swebtoon-phinf.pstatic.net/20220925_233/1664072853907lzhoD_JPEG/6CastleSwimmer_mobile_thumbnail.jpg"),
    ("webtoon", "https://swebtoon-phinf.pstatic.net/20150608_11/1433732704241xoYMT_JPEG/EC8DB8EB84A4EC9DBC_mobile.jpg"),
    ("mangaupdates", "https://cdn.mangaupdates.com/image/i451903.jpg"),
    ("mangaupdates", "https://cdn.mangaupdates.com/image/i198432.jpg"),
    ("mangaupdates", "https://cdn.mangaupdates.com/image/i121274.jpg"),
]
TEMOINS = [
    ("webtoon (témoin)", "https://swebtoon-phinf.pstatic.net/20990101_1/0000000000000aaaaa_JPEG/inexistante.jpg"),
    ("mangaupdates (témoin)", "https://cdn.mangaupdates.com/image/i999999999.jpg"),
]
ORIGINES = ["http://localhost:4178/__test-referer", "https://toonboxd.app/__test-referer"]


def page_de_test(politique):
    attr = ' referrerpolicy="no-referrer"' if politique == "no-referrer" else ""
    imgs = "\n".join(f'<img id="i{n}" src="{u}"{attr} alt="">' for n, (_, u) in enumerate(ADRESSES + TEMOINS))
    return f"<!doctype html><html><head><meta charset=utf-8><title>test</title></head><body>{imgs}</body></html>"


def mesurer(nav, origine, politique):
    ctx = nav.new_context()
    page = ctx.new_page()
    vus = {}

    def reponse(r):
        u = r.url
        if any(u == a for _, a in ADRESSES + TEMOINS):
            vus[u] = {"statut": r.status, "referer": r.request.all_headers().get("referer")}

    page.on("response", reponse)
    page.route(origine, lambda route: route.fulfill(status=200, content_type="text/html; charset=utf-8", body=page_de_test(politique)))
    page.goto(origine, wait_until="load")
    page.wait_for_timeout(1500)
    largeurs = page.evaluate("[...document.images].map(i => i.complete ? i.naturalWidth : -1)")
    ctx.close()
    lignes = []
    for n, (hote, u) in enumerate(ADRESSES + TEMOINS):
        v = vus.get(u, {})
        lignes.append({"hote": hote, "url": u, "statut": v.get("statut"), "referer": v.get("referer"), "largeur": largeurs[n]})
    return lignes


with sync_playwright() as p:
    nav = p.chromium.launch(channel="msedge")
    bilan = {}
    for origine in ORIGINES:
        for politique in ("défaut", "no-referrer"):
            print(f"\n== {origine}  |  Referer : {politique}")
            for l in mesurer(nav, origine, politique):
                ok = bool(l["statut"] and 200 <= l["statut"] < 300 and l["largeur"] and l["largeur"] > 0)
                print(f"  {'OK   ' if ok else 'ÉCHEC'} {l['hote']:<22} statut {l['statut']}  largeur {l['largeur']:>4}  Referer envoyé : {l['referer']}  {l['url'][-46:]}")
                bilan.setdefault((origine, politique, l["hote"]), []).append(ok)
    nav.close()

print("\n== Bilan, hôte par hôte")
for (origine, politique, hote), oks in bilan.items():
    print(f"  {origine:<38} {politique:<12} {hote:<22} {sum(oks)}/{len(oks)} chargées")
temoins_ok = all(not any(v) for (o, pol, h), v in bilan.items() if "témoin" in h)
print("\nTémoins :", "les adresses inexistantes échouent partout, le test sait voir un échec" if temoins_ok else "UN TÉMOIN A CHARGÉ : le test ne tranche pas")
