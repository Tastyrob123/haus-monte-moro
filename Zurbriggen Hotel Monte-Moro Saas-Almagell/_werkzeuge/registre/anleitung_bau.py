#!/usr/bin/env python3
"""Baut anleitung.html (Anleitung Besucher · Hotel Monte-Moro, Saas-Almagell) aus den Texten unten. Vorlage: die Anleitung Besucher
im Stamm der Häuser (zehn Kapitel in vier Themen), Bild gross mit Klick und Esc, «Gut zu wissen» je Kapitel, im Kleid des Hotel Monte-Moro.
Bilder: node anleitung_bilder.js (anleitung/k01.jpg …). python3 anleitung_bau.py"""
import html, os, re
HIER = os.path.dirname(os.path.abspath(__file__))
# Namen der Werkzeuge nur aus dem Kleid des Hauses (_werkzeuge/oberflaeche/kleid/montemoro.js, WO_HAUS.namen, gepflegt vom Chat der Zentrale), nie abgetippt.
_KLEID = open(os.path.join(os.path.dirname(HIER), 'oberflaeche', 'kleid', 'montemoro.js'), encoding='utf-8').read()
def _name(k):
    m = re.search(k + r":\s*'([^']+)'", re.search(r'namen:\s*\{([^}]*)\}', _KLEID).group(1))
    return m.group(1)
NAME, STUBE = _name('besuche'), _name('zentrale')
KLEIN = re.sub(r'^(Die|Das|Der) ', lambda m: m.group(0).lower(), NAME)
THEMEN = [
 ('Grundlagen', 'So geht ' + KLEIN, [
  ('k01', 'Übersicht', 'So ist ' + KLEIN + ' aufgebaut.', NAME + ' zeigt, wer Ihre Website besucht: woher die Gäste kommen, was sie sich ansehen, wie lange sie bleiben und wie oft daraus eine Zimmer-Anfrage oder eine Buchung wird. Sie ändern hier nichts, Sie lesen.',
   ['Links die Bereiche: «Übersicht», darunter «Besuche», «Herkunft» und «Zeit» für die Gäste, «Seiten», «Verlauf» und «Zur Buchung» für die Website, zuletzt «So wird gezählt».',
    'Unter dem Titel jeder Ansicht wählen Sie den Zeitraum: 7, 30 oder 90 Tage. Alle Zahlen der Ansicht gelten für diesen Zeitraum.',
    'Oben im Kopf stehen Titel und Stand der Ansicht, rechts der Weg zu allen Werkzeugen (' + STUBE + '), die Anleitung und «Website ansehen». Unten nennt die Leiste die Besuche von heute.',
    'Beim ersten Mal zeigt ein kleines Schild unten rechts «Kurzer Rundgang». Er lässt sich jederzeit über den Rand wieder öffnen.'],
   'Die Bilder dieser Anleitung zeigen Beispielwerte. Sie sind erfunden und im Bild so beschriftet. Ihre echten Besuche erscheinen, sobald die Website zählt.'),
  ('k02', 'Übersicht', 'Die Übersicht lesen.', 'Oben vier Zahlen: Besuche (mit dem Vergleich zum Zeitraum davor), angesehene Seiten, Minuten je Besuch und wie viele zur Buchung kamen, also im Fenster «Anfrage» ein Zimmer anfragten oder auf «Zimmer buchen» gingen. Darunter die Besuche je Tag als Säulen.',
   ['Mit der Maus über eine Säule fahren: Tag und Zahl der Besuche erscheinen.',
    '«Woher die Gäste kommen» und «Am meisten angesehen» zeigen je die ersten Plätze. Der Link daneben führt zur ganzen Liste.',
    'Ganz unten stehen die letzten fünf Besuche. Ein Klick öffnet den Besuch.'],
   'Ein Besuch ist ein Gast an einem Tag. Kommt derselbe Gast nach mehr als einer halben Stunde Pause wieder, zählt das als neuer Besuch.')]),
 ('Die Gäste', 'Besuche, Herkunft und Zeit', [
  ('k03', 'Besuche', 'Einen Besuch lesen.', 'Unter «Besuche» steht jeder einzelne Besuch: links die Liste nach Tagen, rechts der gewählte Besuch.',
   ['Links einen Besuch anklicken. Das Bild zeigt die erste Seite, die der Gast nach der Startseite öffnete, das Land steht klein darauf; daneben Ort, Uhrzeit, Zahl der Seiten und Dauer. Die Seite bleibt, wo sie ist, nur die Karte rechts wechselt.',
    'Rechts oben sechs Angaben: wann der Gast kam, wie lange er blieb, wie viele Seiten, mit welchem Gerät, in welcher Sprache und über welche Website er zu Ihnen fand.',
    'Darunter «Der Weg durch die Website»: Seite für Seite in der Reihenfolge des Besuchs, mit der Zeit je Seite. Unter einer Seite steht, was der Gast dort getan hat, etwa eine Zimmer-Anfrage begonnen, «Zimmer buchen» angeklickt oder einen Tisch im Röstihüs angefragt.'],
   'Ein Name steht nie da. ' + NAME + ' kennt Ort, Uhrzeit und Weg, aber nicht, wer der Gast ist.'),
  ('k04', 'Besuche', 'Wer buchen oder anfragen wollte.', 'Über der Liste grenzen Sie ein: alle Besuche, nur die zur Buchung, nur die, in denen eine Anfrage begonnen wurde, nur die mit Anruf oder E-Mail, oder nur die am Handy.',
   ['Auf «Zur Buchung» klicken. Die Liste zeigt nur noch Besuche, bei denen der Gast ein Zimmer anfragte oder auf «Zimmer buchen» ging. Ihr Kreis steht in Lärche.',
    'Einen dieser Besuche öffnen und den Weg lesen: Welche Seiten hat der Gast vorher angesehen, wie lange, und hat er angefragt oder ist er zur Buchung bei seekda gegangen?',
    '«Anfrage begonnen» zeigt, wer das Fenster «Anfrage» für ein Zimmer oder einen Tisch im Röstihüs geöffnet hat. «Anruf oder E-Mail» zeigt, wer die Nummer oder die E-Mail-Adresse des Hauses angeklickt hat, «Am Handy» die Besuche vom Telefon.'],
   'So sehen Sie, welche Seiten Gäste zur Buchung führen. Lesen viele vorher «Zimmer» oder «Preise», lohnt es sich, gerade diese Seiten mit Fotos und Preisen der neuen Saison aktuell zu halten.'),
  ('k05', 'Herkunft', 'Woher die Gäste kommen.', 'Unter «Herkunft» stehen Länder und Orte, wie viele aus der Schweiz und aus dem Wallis kommen, die Sprache des Browsers und das Gerät.',
   ['«Länder» und «Orte» nennt die Verbindung des Gastes. Der Ort ist der seines Anschlusses und kann einige Kilometer danebenliegen.',
    '«Gekommen über» zeigt, von welcher Website der Gast zu Ihnen fand: Google, Booking.com, Schweiz Tourismus, die Ferienregion Saas-Fee/Saastal oder Instagram. «Direkt aufgerufen» heisst: Adresse eingetippt, Lesezeichen oder Link aus einer Nachricht.',
    '«Sprache des Browsers» ist die Sprache, in der der Gast seinen Browser eingestellt hat (die Website selbst ist deutsch), «Gerät» unterscheidet Handy, Tablet und Rechner.'],
   'Planen Gäste aus Deutschland, Italien oder den Niederlanden ihre Ferien im Saastal, sehen Sie es hier zuerst.'),
  ('k06', 'Zeit', 'Wann Gäste vorbeischauen.', 'Unter «Zeit» steht, zu welcher Stunde und an welchem Wochentag die Besuche beginnen. Uhrzeit in Saas-Almagell.',
   ['Oben vier Spitzen: wann die meisten kommen, welcher Tag am stärksten ist, wie viele ab 18 Uhr und wie viele am Wochenende.',
    '«Zu welcher Uhrzeit» zeigt 24 Säulen, eine je Stunde. Mit der Maus darüber erscheint die Zahl.',
    '«Wochentag und Stunde» legt beides übereinander: Je dunkler ein Feld, desto mehr Besuche.'],
   'So sehen Sie, wann Gäste ihre Ferien planen und wann sich ein Beitrag zur neuen Saison am ehesten lohnt: Dann sind die Gäste ohnehin auf der Seite.')]),
 ('Die Website', 'Seiten, Verlauf und der Weg zur Buchung', [
  ('k07', 'Seiten', 'Was am meisten angesehen wird.', 'Unter «Seiten» steht jede Seite der Website mit ihren Aufrufen, der Zeit, die Gäste im Schnitt darauf bleiben, und wie oft sie auf dem Weg eines Gastes lag, der danach ein Zimmer anfragte oder auf «Zimmer buchen» ging.',
   ['Die Liste ist nach Aufrufen geordnet, die meistbesuchte Seite steht oben, jede mit ihrem Bild.',
    '«Zeit im Schnitt» zählt nur, solange die Seite im Vordergrund war. Liegt sie in einem Reiter im Hintergrund, läuft die Zeit nicht.',
    '«Zur Buchung» nennt, wie oft die Seite in einem Besuch angesehen wurde, der danach zu einer Anfrage oder Buchung führte.'],
   'Eine Seite mit vielen Aufrufen und wenig Zeit wird oft nur überflogen. Eine Seite mit wenigen Aufrufen und viel Zeit wird gelesen, aber selten gefunden.'),
  ('k08', 'Verlauf', 'Wie sich die Besuche entwickeln.', 'Unter «Verlauf» steht der gewählte Zeitraum neben dem Zeitraum davor: Geht es aufwärts oder abwärts?',
   ['Die Säulen zeigen die Besuche je Tag, dahinter hell derselbe Tag im Zeitraum davor.',
    '«Neben dem Zeitraum davor» vergleicht Besuche, Seiten, Zeit, den Weg zur Buchung, die begonnenen Anfragen, Anrufe und E-Mails sowie den Weg zur Familie Zurbriggen, mit dem Unterschied in Prozent.',
    '«Woche für Woche» fasst von Montag bis Sonntag zusammen, darunter die wichtigsten Länder als kleine Verlaufslinien.'],
   'Ein einzelner Tag sagt wenig. Achten Sie auf Wochen und auf die Richtung der Linien, besonders vor dem Beginn der Sommer- und der Wintersaison.'),
  ('k09', 'Zur Buchung', 'Wie oft die Website zur Buchung führt.', 'Ein Zimmer fragen Gäste im Fenster «Anfrage» an, gebucht wird über «Zimmer buchen» bei seekda. Neun Werte zeigen, wie oft ein Besuch dahin führt: von der Startseite, von «Preise», über «Zimmer buchen», die Anfrage ohne Abschicken, der Tisch im Röstihüs (begonnen und angefragt), Anruf oder E-Mail, der Chat der Rezeption und der Weg zur Familie Zurbriggen.',
   ['Jeder Wert steht als Anteil in Prozent, darunter die gezählten Zahlen, also wie viele von allen Aufrufen der Startseite in einem Besuch lagen, der danach zur Buchung führte.',
    '«Anfrage ohne Abschicken» zählt, wie oft jemand das Fenster «Anfrage» für ein Zimmer öffnet und dann nicht abschickt.',
    'Darunter «Welche Seiten vor der Buchung lagen» und «Der Weg zur Buchung» vom Besuch über «Zimmer» oder «Preise» bis zur Anfrage oder zu «Zimmer buchen».'],
   'Gezählt wird, dass eine Anfrage abgeschickt oder «Zimmer buchen» angeklickt wurde, nie Name oder Telefonnummer. Wer angefragt oder gebucht hat, sehen Sie in Ihrem Eingang und bei seekda.')]),
 ('Gut zu wissen', 'Die Zählung', [
  ('k10', 'Gut zu wissen', 'Was gezählt wird und was nicht.', NAME + ' zählt so wenig wie möglich und so viel wie nötig. «So wird gezählt» im Rand sagt es in einem Blick.',
   ['Gezählt werden Seite, Zeit, Land und Ort, Gerät, Sprache des Browsers, die Herkunft (nur der Name der Website) und die Schritte zu Zimmer-Anfrage, «Zimmer buchen», Tisch im Röstihüs, Telefon, E-Mail, Chat der Rezeption und Familie Zurbriggen.',
    'Nie gezählt werden Namen, Mailadressen, Eingaben, die Adresse der Verbindung und Cookies. Am nächsten Tag erkennt ' + KLEIN + ' denselben Gast nicht wieder.',
    'Die Daten liegen nur in Ihrem Speicher, getrennt von jedem anderen Haus, und werden nach 400 Tagen gelöscht.'],
   'Sobald die Zählung auf der Website läuft, steht sie auch in der Datenschutzerklärung.')])]

def e(s): return html.escape(s, quote=False)
def fest(s):   # Tor 30.10.2026: die letzten zwei Wörter bleiben zusammen (Safari bricht im ausgewogenen Umbruch auch am geschützten Leerzeichen)
    t = s.rsplit(' ', 2)
    return e(s) if len(t) < 3 else e(t[0]) + ' <span class="nw">' + e(t[1]) + ' ' + e(t[2]) + '</span>'
n = 0
inhalt, kapitel = [], []
for kz, tz, ks in THEMEN:
    zeilen = []
    for (bild, bereich, titel, einl, schritte, wissen) in ks:
        n += 1; nr = '%02d' % n
        zeilen.append(f'<li><a href="#k{nr}"><b>{nr}</b><span>{fest(titel)}</span><i>{e(bereich)}</i></a></li>')
        li = ''.join(f'<li><span>{i}</span><p>{e(s)}</p></li>' for i, s in enumerate(schritte, 1))
        kapitel.append(f'''<article class="kap" id="k{nr}">
  <div class="kap__t"><span class="mono">{nr} · {e(bereich)}</span><h2>{fest(titel)}</h2><p class="einl">{e(einl)}</p>
    <ol class="schritte">{li}</ol>
    <p class="wissen"><b>Gut zu wissen</b>{e(wissen)}</p></div>
  <figure class="kap__b"><button type="button" class="bild" aria-label="Bild gross ansehen: {e(titel)}"><img src="anleitung/{bild}.jpg" width="1200" height="750" decoding="async" alt="{e(NAME)}, {e(bereich)}: {e(titel)} (Beispielwerte)"></button>
    <figcaption><span>{e(NAME.lower())} · {e(bereich.lower())}</span><span>Beispielwerte · Grösser ansehen</span></figcaption></figure>
</article>''')
    inhalt.append(f'<section class="thema"><h3><small>{e(kz)}</small>{e(tz)}<em>{len(ks)} Kapitel</em></h3><ol>{"".join(zeilen)}</ol></section>')
seite = open(os.path.join(HIER, 'anleitung.vorlage.html'), encoding='utf-8').read()
seite = seite.replace('%%NAME%%', e(NAME)).replace('%%ANZAHL_WORT%%', ['Null', 'Ein', 'Zwei', 'Drei', 'Vier', 'Fünf', 'Sechs', 'Sieben', 'Acht', 'Neun', 'Zehn', 'Elf', 'Zwölf'][n] if n < 13 else str(n)).replace('%%ANZAHL%%', str(n)).replace('%%INHALT%%', ''.join(inhalt)).replace('%%KAPITEL%%', '\n'.join(kapitel))   # Titel mit Wort: eine grosse Zahl stünde lose (oberflaeche_pruefen Regel 4)
open(os.path.join(HIER, 'anleitung.html'), 'w', encoding='utf-8').write(seite)
print('anleitung.html:', n, 'Kapitel')
