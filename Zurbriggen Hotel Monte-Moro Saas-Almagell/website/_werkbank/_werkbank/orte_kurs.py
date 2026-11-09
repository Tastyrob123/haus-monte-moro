#!/usr/bin/env python3
"""Werkbank Monte-Moro: «Meine drei Orte», das Kursblatt mit Hamburg, Koh Phangan und Siargao (Robert 29.10.2026: «meine hamburg siargao koh phangan
animation einfügen wie wir sie mal hatte»). Block und Animation kommen unverändert aus dem Werkbank-Kit (bau.py › orte, Brief-Art «lang»; werkbank.css ›
.karte3, .kurs, @keyframes welle, beides lädt die Werkbank ohnehin); hier steht nur das Kleid des Stamm: Nacht statt Marineblau, Warmweiss und Orange.
Gebraucht im Brief (brief_blatt.py, neben der Unterschrift) und im Schluss (wb_kapitel.py › schluss, unter der Unterschrift)."""
import os
import re

_KIT = os.path.join(os.environ.get('WERKBANK_KIT') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '_Werkbank-Kit'), 'bau.py')


def block(art):
    """Robert 09.11.2026 (KORREKTUR-ROBERT.md 1): kein Ticket, kein Billett, keine Reiseroute. Der Block fällt in Brief und Schluss weg.
    Früher: Der Block «orte» aus dem Kit, Wort für Wort; art = 'brief' oder 'schluss' für die Lage im Kleid."""
    return ''
    h = re.search(r"orte = '''(.*?)'''", open(_KIT, encoding='utf-8').read(), re.S).group(1).strip()
    # Robert 1.11.2026: «soll mehr wie ein Ticket sein, kein Kasten». Inhalt (Titel, Satz, Kursblatt) bleibt aus dem Kit, die Form wird ein Billett:
    # Kopfzeile, Hauptteil, Perforation mit zwei ausgeschnittenen Kerben (Maske, Website-Master 13: nie Kreise über die Kante), Abriss in Creme.
    innen = h[h.index('>') + 1:h.rindex('</div>')].strip()
    return (f'<div class="tk ok ok--{art}" data-a="kipp" style="--i:2"><div class="tk__f">'
            f'<div class="tk__h"><p class="tk__kopf"><span>Kursblatt</span><span>Robert Reff · Tasty Studios</span></p>{innen}</div>'
            '<div class="tk__a" aria-hidden="true"><span class="tk__nr">N° 3</span><b>3</b><small>Orte</small>'
            '<span class="tk__l">Hamburg<br>Koh Phangan<br>Siargao</span></div>'
            '</div></div>')


CSS = """
/* ---------- «Meine drei Orte» im Kleid des Hauses (orte_kurs.py, 29.10.2026): Block und Animation aus dem Kit, Farben des Hauses ---------- */
.karte3.ok{background:var(--navy);color:#fbf5ea;text-align:left;box-shadow:inset 0 1px 0 rgba(255,255,255,.08),inset 0 0 0 1px rgba(239,118,73,.26),0 30px 40px -26px rgba(8,7,10,.8)}
.karte3.ok h3{color:#fbf5ea}
.karte3.ok p{color:rgba(251,245,234,.76)}
.ok .kurs text{fill:rgba(251,245,234,.72)}
.ok .kurs .ort{fill:#fbf5ea}
.ok .kurs .weg,.ok .kurs .welle{stroke:var(--gold)}
.ok .kurs .pkt{fill:#fbf5ea}.ok .kurs .da0{fill:var(--gold)}
.ok--schluss{width:min(100%,560px);margin:clamp(22px,2.6vw,36px) auto 0}
/* Ticket (Robert 1.11.2026): Schatten an der Hülle (drop-shadow folgt der Maske), Fläche mit Kerben an der Naht, Abriss in Creme */
.tk{--ab:clamp(112px,22%,168px);--k:12px;color:#f8f3eb;text-align:left;filter:drop-shadow(0 22px 26px rgba(8,6,5,.5)) drop-shadow(0 3px 6px rgba(8,6,5,.35))}
.tk__f{display:grid;grid-template-columns:minmax(0,1fr) var(--ab);border-radius:20px;overflow:hidden;background:linear-gradient(180deg,#2b211c,#1c1513);
  -webkit-mask:radial-gradient(circle at calc(100% - var(--ab)) 0,#0000 var(--k),#000 calc(var(--k) + .6px)) top/100% 51% no-repeat,radial-gradient(circle at calc(100% - var(--ab)) 100%,#0000 var(--k),#000 calc(var(--k) + .6px)) bottom/100% 51% no-repeat;
  mask:radial-gradient(circle at calc(100% - var(--ab)) 0,#0000 var(--k),#000 calc(var(--k) + .6px)) top/100% 51% no-repeat,radial-gradient(circle at calc(100% - var(--ab)) 100%,#0000 var(--k),#000 calc(var(--k) + .6px)) bottom/100% 51% no-repeat}
.tk__h{padding:clamp(20px,2.4vw,32px);min-width:0}
.tk__kopf{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:0 0 16px;padding-bottom:11px;border-bottom:1px solid rgba(216,178,100,.3);font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}
.tk h3{font-family:var(--serif);font-weight:400;font-size:1.5rem;line-height:1.14;margin:0 0 6px;color:#f8f3eb}
.tk h3+p{color:rgba(248,243,235,.76);font-size:1rem;margin:0}
.tk__a{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:22px 12px;text-align:center;background:linear-gradient(180deg,#f7f1e7,#ece2d2);color:#1b1512}
.tk__a::before{content:'';position:absolute;left:0;top:calc(var(--k) + 6px);bottom:calc(var(--k) + 6px);border-left:2px dashed rgba(27,21,18,.32)}
.tk__nr{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:#7a5c24}
.tk__a b{font-family:var(--serif);font-weight:400;font-size:clamp(46px,5vw,64px);line-height:1;margin-top:6px}
.tk__a small{font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase}
.tk__l{margin-top:10px;padding-top:10px;border-top:1px solid rgba(27,21,18,.18);font-family:var(--mono);font-size:9.5px;line-height:1.7;letter-spacing:.12em;text-transform:uppercase;color:rgba(27,21,18,.72)}
@media (max-width:620px){
  .tk{--abh:96px}
  .tk__f{grid-template-columns:1fr;
    -webkit-mask:radial-gradient(circle at 0 calc(100% - var(--abh)),#0000 var(--k),#000 calc(var(--k) + .6px)) left/51% 100% no-repeat,radial-gradient(circle at 100% calc(100% - var(--abh)),#0000 var(--k),#000 calc(var(--k) + .6px)) right/51% 100% no-repeat;
    mask:radial-gradient(circle at 0 calc(100% - var(--abh)),#0000 var(--k),#000 calc(var(--k) + .6px)) left/51% 100% no-repeat,radial-gradient(circle at 100% calc(100% - var(--abh)),#0000 var(--k),#000 calc(var(--k) + .6px)) right/51% 100% no-repeat}
  .tk__a{height:var(--abh);box-sizing:border-box;flex-direction:row;flex-wrap:wrap;gap:4px 14px;padding:12px 20px}
  .tk__a::before{left:calc(var(--k) + 6px);right:calc(var(--k) + 6px);top:0;bottom:auto;border-left:0;border-top:2px dashed rgba(27,21,18,.32)}
  .tk__a b{font-size:40px;margin:0}.tk__nr{width:100%}.tk__l{margin:0;padding:0 0 0 14px;border-top:0;border-left:1px solid rgba(27,21,18,.18)}
}
"""
