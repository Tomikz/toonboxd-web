"""
REND og-en.png DEPUIS _outils/og-en.html (16 octobre 2026).

Le modèle est servi par le site lui-même, pour que la police et l'icône soient
celles qu'il sert : lancer d'abord un serveur à la racine du dépôt,
    py -3 -m http.server 4178 --bind 127.0.0.1
puis :
    python _outils/og.py
Il faut Playwright (pip install playwright) ; le navigateur est Microsoft Edge,
déjà installé sous Windows (channel="msedge"), donc rien d'autre à télécharger.
Le rendu attend que les trois polices soient chargées : une capture prise
avant tomberait sur la police de repli, et elle ne le dirait pas.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

RACINE = Path(__file__).resolve().parent.parent
ADRESSE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:4178/_outils/og-en.html"

with sync_playwright() as p:
    navigateur = p.chromium.launch(channel="msedge")
    page = navigateur.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
    page.goto(ADRESSE, wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    chargees = page.evaluate("[...document.fonts].filter(f => f.status === 'loaded').length")
    if chargees < 3:
        raise SystemExit(f"{chargees} police(s) chargée(s) sur 3 : la capture tomberait sur la police de repli")
    page.screenshot(path=str(RACINE / "og-en.png"), clip={"x": 0, "y": 0, "width": 1200, "height": 630})
    navigateur.close()
print("og-en.png écrit,", (RACINE / "og-en.png").stat().st_size, "octets")
