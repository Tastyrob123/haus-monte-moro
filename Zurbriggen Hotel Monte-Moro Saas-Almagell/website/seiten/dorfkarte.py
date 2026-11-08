"""Gezeichnete Dorfkarte für den Schluss des Flugs auf anreise.html (Robert 24.10.2026: «statt den 2. mal mit den Füssen eine echt im Stil des Hauses
gezeichnete Karte die den Weg beschreibt»). Aus echten OpenStreetMap-Daten (_quelle/monte-moro/karte-2026-10-24/osm-dorf.json, ODbL, Nennung auf der
Karte und im Impressum): Strassen, Wege, Bäche und Häuser von Saas-Almagell rund um das Hotel, gezeichnet in den Farben des Hauses auf einem Blatt Papier.
Der Fussweg von der Bushaltestelle Dorfplatz bis vor das Hotel ist der kürzeste Weg auf dem Strassennetz; er erscheint Strich für Strich (nur Deckkraft),
sobald die Kamera beim Haus ist. Daneben, was zu Fuss nah ist: die Sesselbahn Furggstalden und das Spa im Wellness & Spa Pirmin Zurbriggen.
Koordinaten: das Hotel liegt bei (HX, HY) der Flugkarte, Massstab M Einheiten je Meter, Norden oben."""
import heapq, json, math, os

QUELLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '_quelle', 'karte-2026-10-24')
LAT0, LON0 = 46.09343, 7.95778            # Hotel Monte-Moro (OSM-Punkt «Monte-Moro», tourism=hotel)
HX, HY, M = 575, 318, .26                 # Lage des Hauses auf der Flugkarte, Einheiten je Meter
BLATT = (512, 252, 645, 372)              # x0 y0 x1 y1 des Papiers
ORTE = {'bus': (46.0943752, 7.9575889), 'lift': (46.0922228, 7.9579601), 'spa': (46.09235, 7.9575677)}


def _xy(la, lo):
    return (HX + (lo - LON0) * math.cos(math.radians(LAT0)) * 111320 * M, HY - (la - LAT0) * 110540 * M)


def _innen(p, rand=0):
    x0, y0, x1, y1 = BLATT
    return x0 - rand <= p[0] <= x1 + rand and y0 - rand <= p[1] <= y1 + rand


def _clip(pts):
    """Linie auf das Blatt kürzen (Liang-Barsky je Strecke), Teilstücke zurückgeben."""
    x0, y0, x1, y1 = BLATT
    teile, cur = [], []
    for a, b in zip(pts, pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        t0, t1, ok = 0.0, 1.0, True
        for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
            if p == 0:
                if q < 0: ok = False; break
            else:
                r = q / p
                if p < 0: t0 = max(t0, r)
                else: t1 = min(t1, r)
        if not ok or t0 > t1:
            if cur: teile.append(cur); cur = []
            continue
        A = (a[0] + t0 * dx, a[1] + t0 * dy); Bp = (a[0] + t1 * dx, a[1] + t1 * dy)
        if not cur: cur = [A]
        cur.append(Bp)
        if t1 < 1: teile.append(cur); cur = []
    if cur: teile.append(cur)
    return [t for t in teile if len(t) > 1]


def _d(pts):
    return 'M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in pts)


def karte(e=lambda s: s):
    d = json.load(open(os.path.join(QUELLE, 'osm-dorf.json')))
    strassen, wege, baeche, haeuser, graph = [], [], [], [], {}
    for el in d['elements']:
        t = el.get('tags', {}); g = el.get('geometry')
        if el['type'] != 'way' or not g: continue
        pts = [_xy(p['lat'], p['lon']) for p in g]
        if 'building' in t:
            if any(_innen(p) for p in pts) and all(_innen(p, 2) for p in pts):
                haeuser.append((pts, t.get('name') or t.get('tourism') or ''))
        elif 'waterway' in t:
            baeche += _clip(pts)
        elif 'highway' in t:
            art = t['highway']
            (wege if art in ('footway', 'path', 'steps', 'track', 'cycleway', 'pedestrian') else strassen).extend(_clip(pts))
            for a, b, pa, pb in zip(el['nodes'], el['nodes'][1:], pts, pts[1:]):
                w = math.dist(pa, pb)
                graph.setdefault(a, [pa, []])[1].append((b, w)); graph.setdefault(b, [pb, []])[1].append((a, w))

    def nah(p): return min(graph, key=lambda n: math.dist(graph[n][0], p))
    def weg(a, b):
        s, z = nah(a), nah(b); D, P, q = {s: 0}, {}, [(0, s)]
        while q:
            c, u = heapq.heappop(q)
            if u == z: break
            if c > D[u]: continue
            for v, w in graph[u][1]:
                if c + w < D.get(v, 1e18): D[v] = c + w; P[v] = u; heapq.heappush(q, (c + w, v))
        r = [z]
        while r[-1] != s: r.append(P[r[-1]])
        return [graph[n][0] for n in r[::-1]]

    bus, lift, spa = (_xy(*ORTE[k]) for k in ('bus', 'lift', 'spa'))
    route = [bus] + weg(bus, (HX, HY)) + [(HX, HY)]
    # Strich für Strich: gleich lange Stücke entlang des Wegs
    laenge = sum(math.dist(a, b) for a, b in zip(route, route[1:])); n = max(8, int(laenge / 1.6))
    def punkt(s):
        for a, b in zip(route, route[1:]):
            l = math.dist(a, b)
            if s <= l: return (a[0] + (b[0] - a[0]) * s / l, a[1] + (b[1] - a[1]) * s / l)
            s -= l
        return route[-1]
    striche = ''.join(f'<line x1="{punkt(i * laenge / n)[0]:.2f}" y1="{punkt(i * laenge / n)[1]:.2f}" x2="{punkt((i + .62) * laenge / n)[0]:.2f}" y2="{punkt((i + .62) * laenge / n)[1]:.2f}" style="--k:{i}"/>' for i in range(n))

    # das Hotel: das Haus, in dem der Punkt liegt (sonst das nächste)
    def drin(p, poly):
        c = False
        for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
            if (y1 > p[1]) != (y2 > p[1]) and p[0] < (x2 - x1) * (p[1] - y1) / (y2 - y1 or 1e-9) + x1: c = not c
        return c
    hotel = next((i for i, (h, _) in enumerate(haeuser) if drin((HX, HY), h)), None)
    if hotel is None and haeuser:
        hotel = min(range(len(haeuser)), key=lambda i: math.dist((HX, HY), (sum(p[0] for p in haeuser[i][0]) / len(haeuser[i][0]), sum(p[1] for p in haeuser[i][0]) / len(haeuser[i][0]))))
    hs = ''.join(f'<path class="dk-haus{" dk-haus--hotel" if i == hotel else ""}" d="{_d(h)}Z"/>' for i, (h, _) in enumerate(haeuser))

    x0, y0, x1, y1 = BLATT
    def marke(p, kl, name, sub, dx=2.2, anker='start'):
        return (f'<g class="dk-ort dk-ort--{kl}" transform="translate({p[0]:.2f} {p[1]:.2f})"><rect x="-1" y="-1" width="2" height="2"/>'
                f'<text class="dk-n" x="{dx}" y="-.3" text-anchor="{anker}">{e(name)}</text><text class="dk-s" x="{dx}" y="1.9" text-anchor="{anker}">{e(sub)}</text></g>')
    return (f'<g class="dorfkarte">'
            f'<rect class="dk-blatt" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/>'
            f'<rect class="dk-rahmen" x="{x0 + 1.4}" y="{y0 + 1.4}" width="{x1 - x0 - 2.8}" height="{y1 - y0 - 2.8}"/>'
            + ''.join(f'<path class="dk-bach" d="{_d(t)}"/>' for t in baeche)
            + ''.join(f'<path class="dk-weg" d="{_d(t)}"/>' for t in wege)
            + ''.join(f'<path class="dk-str" d="{_d(t)}"/>' for t in strassen)
            + hs
            + f'<g class="dk-route">{striche}</g>'
            + marke(bus, 'bus', 'Bushaltestelle Dorfplatz', 'Hier hält das Postauto', -2.2, 'end')
            + marke(lift, 'lift', 'Sesselbahn Furggstalden', 'Skigebiet Saas-Almagell')
            + marke(spa, 'spa', 'Spa nebenan', 'Wellness & Spa Pirmin Zurbriggen', -2.2, 'end')
            + f'<g class="dk-ort dk-ort--hotel" transform="translate({HX} {HY})"><rect x="-1.4" y="-1.4" width="2.8" height="2.8"/><text class="dk-n dk-n--hotel" x="3.4" y=".8">Hotel Monte-Moro</text></g>'
            + f'<g class="dk-nord" transform="translate({x1 - 6} {y0 + 7})"><path d="M0 -3.2 L1.1 1.4 L0 .6 L-1.1 1.4 Z"/><text y="3.8" text-anchor="middle">N</text></g>'
            + f'<text class="dk-quelle" x="531" y="355.2">Karte: © OpenStreetMap-Mitwirkende</text>'
            + '</g>')
