"""Hotel Monte-Moro, Saas-Almagell: Haken für das Werkbank-Kit, nur für die Dokumente der Kette (Befund Station 2, Material Station 3).
Keine Markenentscheidung: Farben und Zeichen sind am 17.10.2026 aus dem Logo (allgem_logo.png, Blau #115595) und den Fotos der Stube
(restau_*.jpg, Lärchenholz gemessen #b77f49) abgelesen. Die Designidentität legt erst Station 5 fest."""
import os
import hilfen as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = 'Hotel Monte-Moro'
KURZ = 'monte-moro'
LEISTE = ''
PORT = 8978
RECHTE = 'dem Hotel Monte-Moro und den jeweiligen Fotografen.'

FARBEN = dict(nacht='#0b1626', tief='#08111d', navy='#11294a', blau='#174070', papier='#f6f1e7', creme='#ede3d1', weiss='#fdfaf4',
              gold='#cfa26c', messing='#b77f49', taupe='#9a7a5c', tinte='#15202e', punkt='#b77f49', rot='#b0342c')
SCHRIFT = dict(titel=('Gelasio', 'gelasio-500.woff2'), titel_folge="Georgia,'Times New Roman',serif", ersatz="local('Georgia');size-adjust:97%")

ZEICHEN = K.svg_innen(os.path.join(ROOT, 'assets/logo/zeichen.svg'))   # die zwei Gipfel aus dem Logo, mit potrace gezogen
WORT = K.svg_innen(os.path.join(ROOT, 'assets/logo/logo.svg'))

# Tapete: feines Gitter, im Kreuzungspunkt die zwei Gipfel als Medaillon (Rapport 180 px)
_vb, _in = ZEICHEN
_tile = ('<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 180 180">'
         '<g fill="none" stroke="%23cfa26c" stroke-opacity=".10" stroke-width="1"><path d="M0 90H180M90 0V180"/><circle cx="90" cy="90" r="22"/></g>'
         f'<svg x="76" y="82" width="28" height="16" viewBox="{_vb}"><g fill="%23cfa26c" fill-opacity=".16">{_in.replace(chr(34), chr(39))}</g></svg></svg>')
MUSTER = 'url("data:image/svg+xml;utf8,' + _tile.replace('#', '%23').replace('%2523', '%23') + '")'
MUSTER_B = '180px'

SEITEN = []
ETIKETTEN = dict(ordner='etiketten', name='Etiketten', einzahl='Etikett')
