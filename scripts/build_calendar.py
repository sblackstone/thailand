#!/usr/bin/env python3
"""
Build the one-page printable November 2026 calendar.

Design notes (see DESIGN.md for the full system):
  - LIGHT background here, unlike the dark web itinerary. A dark calendar
    is unprintable -- it drains a cartridge and the region colours muddy.
  - Landscape Letter. Two week-rows cover the trip (Nov 1 is a Sunday, so
    the grid starts flush in column one and needs no leading pad).
  - Region-transition days get a diagonal two-colour split: origin region
    upper-left, destination lower-right, so direction of travel reads
    without the legend.

Run:  python3 scripts/build_calendar.py
Out:  site/Thailand-Calendar-Nov2026.pdf
"""
import pathlib
from fonts import ensure_fonts, font_face_css

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "Thailand-Calendar-Nov2026.pdf"

ensure_fonts()
faces = font_face_css()



# Nov 2026: Nov 1 = Sunday. Grid starts col 1, no leading pad.
# Region key: bkk / cnx / krb / kks
trip = {
 1:('bkk','Land BKK 07:35','EK374 · Ritz-Carlton · Wat Pho','plane',''),
 2:('bkk','Bangkok','Grand Palace · Wat Arun · Yaowarat','',''),
 3:('bkk','Night train 18:40','Bangkok → Chiang Mai · Sleeper #9','train','s-bkk-cnx'),
 4:('cnx','Chiang Mai · arr 07:15','U Chiang Mai · Old City temples','',''),
 5:('cnx','U Chiang Mai','Elephant sanctuary day','',''),
 6:('cnx','U Chiang Mai','Doi Suthep · Inthanon falls','',''),
 7:('krb','Fly CNX → KBV','Check out 12:00 → Centara Ao Nang','plane','s-cnx-krb'),
 8:('krb','Centara Ao Nang','Island-hop: Hong or 4-Islands','',''),
 9:('krb','Centara Ao Nang','Tiger Cave / Emerald Pool','',''),
 10:('kks','Transfer in','Krabi ~2h → Chiew Larn → boat 1.5h','car','s-krb-kks'),
 11:('kks','360 Issara','Kayak off the balcony · swim','',''),
 12:('kks','360 Issara','Cave trail · sunset safari 17:00','',''),
 13:('bkk','Boat out · SL741 16:40','Check out 10:00 → URT → DMK 17:55','plane','s-kks-bkk'),
 14:('bkk','Fly home 20:45','Full day · leave city ~17:00','plane',''),
}
fest={}

ICON={
 'plane':'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17.8 19.2 16 11l3.5-3.5a2.1 2.1 0 0 0-3-3L13 8 4.8 6.2l-1.4 1.4 5.9 3.4-2.8 2.8-2.3-.5-1 1 3.4 2 2 3.4 1-1-.5-2.3 2.8-2.8 3.4 5.9z"/></svg>',
 'train':'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="12" height="13" rx="2.5"/><path d="M6 11h12"/><path d="M8 21l1.5-3M16 21l-1.5-3"/></svg>',
 'car':'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15h16M6 15V9a2 2 0 0 1 2-2h5l3 3"/><circle cx="8" cy="18.5" r="1.3"/><circle cx="16" cy="18.5" r="1.3"/></svg>',
 '':''}

cells=[]
for d in range(1,15):
    if d in trip:
        reg,title,sub,ic,sp=trip[d]
        cls = f'cell split {sp}' if sp else f'cell {reg}'
        rule = ''
        cells.append(
          f'<div class="{cls}">{rule}'
          f'<div class="top"><span class="num">{d}</span>{ICON[ic]}</div>'
          f'<div class="ttl">{title}</div>'
          f'<div class="sub">{sub}</div>'
          f'</div>')
    elif d in fest:
        cells.append(f'<div class="cell off"><div class="top"><span class="num">{d}</span></div>'
                     f'<div class="fest">✦ {fest[d]}</div></div>')
    else:
        cells.append(f'<div class="cell off"><div class="top"><span class="num">{d}</span></div></div>')


heads=''.join(f'<div class="hd">{x}</div>' for x in ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'])

html=f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Thailand · November 2026 Calendar</title><style>
{faces}
@page{{size: letter landscape; margin: 11mm 11mm 9mm;}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"Instrument Sans",sans-serif;color:#15332C;background:#fff;line-height:1.35}}
.head{{display:flex;align-items:flex-end;gap:14px;border-bottom:2px solid #15332C;padding-bottom:8px;margin-bottom:11px}}
h1{{font-family:"Fraunces",serif;font-weight:500;font-size:26px;letter-spacing:-.01em;white-space:nowrap}}
h1 em{{font-style:italic;color:#B77A1E}}
.meta{{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:#5C7168;margin-left:auto;text-align:right;line-height:1.5}}
.grid{{display:grid;grid-template-columns:repeat(7,1fr);gap:5px}}
.hd{{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:#5C7168;text-align:center;padding-bottom:3px}}
.cell{{min-height:78px;border:1px solid #D8DED9;border-radius:7px;padding:6px 7px;display:flex;flex-direction:column;break-inside:avoid}}
.top{{display:flex;align-items:flex-start;justify-content:space-between;gap:4px}}
.num{{font-family:"Fraunces",serif;font-size:17px;line-height:1;color:#15332C}}
.ic{{width:12px;height:12px;flex:0 0 12px;opacity:.95}}
.ttl{{margin-top:5px;font-size:9.6px;font-weight:600;line-height:1.28}}
.sub{{margin-top:2px;font-size:8.6px;color:#2E3B33;line-height:1.3}}
.off{{background:#FAFBFA;border-color:#E8EDE9}}
.off .num{{color:#93A49C;font-size:14px}}
.pad{{border:none;background:none;min-height:0}}
.fest{{margin-top:auto;font-family:"IBM Plex Mono",monospace;font-size:7.6px;letter-spacing:.02em;color:#8A5FA8;text-transform:uppercase}}
.bkk{{background:#F6CE85;border-color:#C08A26}} .bkk .ic{{color:#6B4406}} .bkk .ttl{{color:#5E3B05}}
.cnx{{background:#F0A876;border-color:#B4652C}} .cnx .ic{{color:#7A3D12}} .cnx .ttl{{color:#6B350F}}
.krb{{background:#7ED8CB;border-color:#1F8477}} .krb .ic{{color:#0E5148}} .krb .ttl{{color:#0C453E}}
.kks{{background:#9BCE91;border-color:#3F7C38}} .kks .ic{{color:#25501F}} .kks .ttl{{color:#1F441A}}
.cell.split{{position:relative;border-color:#6E7C74}}
.cell.split .ttl,.cell.split .sub,.cell.split .num,.cell.split .ic{{position:relative;z-index:1}}
.s-bkk-cnx{{background:linear-gradient(135deg,#F6CE85 0%,#F6CE85 49.4%,#FFFFFF 49.4%,#FFFFFF 50.6%,#F0A876 50.6%,#F0A876 100%)}}
.s-cnx-krb{{background:linear-gradient(135deg,#F0A876 0%,#F0A876 49.4%,#FFFFFF 49.4%,#FFFFFF 50.6%,#7ED8CB 50.6%,#7ED8CB 100%)}}
.s-krb-kks{{background:linear-gradient(135deg,#7ED8CB 0%,#7ED8CB 49.4%,#FFFFFF 49.4%,#FFFFFF 50.6%,#9BCE91 50.6%,#9BCE91 100%)}}
.s-kks-bkk{{background:linear-gradient(135deg,#9BCE91 0%,#9BCE91 49.4%,#FFFFFF 49.4%,#FFFFFF 50.6%,#F6CE85 50.6%,#F6CE85 100%)}}
.cell.split .rule{{position:absolute;inset:0;z-index:0}}
.cell.split .rule svg{{width:100%;height:100%;display:block}}
.s-bkk-cnx .ic,.s-bkk-cnx .ttl{{color:#3D2A08}}
.s-cnx-krb .ic,.s-cnx-krb .ttl{{color:#2C2A18}}
.s-krb-kks .ic,.s-krb-kks .ttl{{color:#123B2E}}
.s-kks-bkk .ic,.s-kks-bkk .ttl{{color:#2A3A12}}

.legs{{margin-top:13px}}
.legs h2{{font-family:"Fraunces",serif;font-weight:500;font-size:15px;margin-bottom:2px}}
.legs .lead{{font-family:"IBM Plex Mono",monospace;font-size:8.6px;letter-spacing:.1em;text-transform:uppercase;color:#5C7168;margin-bottom:7px}}
.legrid{{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}}
.leg{{border:1px solid #D8DED9;border-radius:7px;padding:7px 8px;display:flex;flex-direction:column;break-inside:avoid}}
.leg .lhd{{display:flex;align-items:baseline;gap:5px;padding-bottom:4px;margin-bottom:5px;border-bottom:1px solid #E4E9E5}}
.leg .ldate{{font-family:"IBM Plex Mono",monospace;font-size:8.4px;letter-spacing:.1em;color:#fff;background:#3E5850;border-radius:3px;padding:1.5px 5px}}
.leg .lroute{{font-size:9.6px;font-weight:600;color:#15332C}}
.leg .lmode{{font-family:"IBM Plex Mono",monospace;font-size:7.6px;letter-spacing:.08em;text-transform:uppercase;color:#5C7168;margin-left:auto}}
table{{width:100%;border-collapse:collapse}}
td{{font-family:"IBM Plex Mono",monospace;font-size:8.2px;padding:2.1px 0;vertical-align:top;color:#2E3B33}}
td.t{{white-space:nowrap;font-weight:500}}
td.p{{text-align:right;white-space:nowrap;color:#15332C}}
td.n{{color:#6B7C74;padding-left:6px}}
tr.pick td{{color:#0C453E;font-weight:500}}
tr.pick td{{background:#FBF0D8}}
tr.pick td.t{{border-left:2px solid #C08A26;padding-left:4px}}
.leg .foot{{margin-top:auto;padding-top:5px;font-size:7.8px;color:#5C7168;line-height:1.3}}
.leg.tbd{{background:#FAFBFA}}
.legend{{display:flex;flex-wrap:nowrap;gap:8px 15px;margin-top:10px;padding-top:8px;border-top:1px solid #D8DED9;
 font-family:"IBM Plex Mono",monospace;font-size:9.5px;color:#4A5F57;letter-spacing:.03em;align-items:center}}
.lg{{display:flex;align-items:center;gap:6px;white-space:nowrap}}
.sw{{width:11px;height:11px;border-radius:3px;border:1px solid rgba(0,0,0,.15)}}
.sw-bkk{{background:#E0A94A}}.sw-cnx{{background:#DE8A4C}}.sw-krb{{background:#46BFB0}}.sw-kks{{background:#69AB60}}
.note{{margin-left:auto;color:#5C7168}}
</style></head><body>
<div class="head">
  <h1>Thailand — <em>November 2026</em></h1>
  <div class="meta">Sun 1 Nov &rarr; Sat 14 Nov · 13 nights · 2 travellers<br>EK374 in 07:35 · EK373 out 20:45 · ref H2M5FJ</div>
</div>
<div class="grid">{heads}{''.join(cells)}</div>

<div class="legs">
  <h2>Getting between them</h2>
  <div class="lead">Four inter-region legs · times to confirm at booking · shaded row = current pick</div>
  <div class="legrid">

    <div class="leg">
      <div class="lhd"><span class="ldate">TUE 3</span><span class="lroute">Bangkok &rarr; Chiang Mai</span><span class="lmode">Rail</span></div>
      <table>
        <tr><td class="t">14:15 &rarr; 04:05</td><td class="n">#109 · 2nd only</td><td class="p">13h50</td></tr>
        <tr class="pick"><td class="t">18:40 &rarr; 07:15</td><td class="n">#9 · 2nd A/C · BOOKED</td><td class="p">12h35</td></tr>
        <tr><td class="t">20:05 &rarr; 08:40</td><td class="n">#13 · 1st + 2nd</td><td class="p">12h35</td></tr>
        <tr><td class="t">22:30 &rarr; 12:10</td><td class="n">#51 · 2nd only</td><td class="p">13h40</td></tr>
      </table>
      <div class="foot">Krung Thep Aphiwat (KTW → CGM). <strong>Ticketed — 2 berths, 2nd Class Sleeping A/C.</strong> Board 20 min before; arrive 30 min early.</div>
    </div>

    <div class="leg">
      <div class="lhd"><span class="ldate">SAT 7</span><span class="lroute">Chiang Mai &rarr; Krabi</span><span class="lmode">Air</span></div>
      <table>
        <tr class="pick"><td class="t">07:55 &rarr; 09:55</td><td class="n">FD3072 &middot; BOOKED</td><td class="p">$258</td></tr>
        <tr><td class="t">12:55 &rarr; 14:55</td><td class="n">FD3076</td><td class="p">$306</td></tr>
        <tr><td class="t">17:05 &rarr; 19:05</td><td class="n">FD3074</td><td class="p">$221</td></tr>
      </table>
      <div class="foot">AirAsia · A320 · 2h00 non-stop. Morning flight buys a full first beach afternoon; 17:05 saves $37 but costs the day.</div>
    </div>

    <div class="leg tbd">
      <div class="lhd"><span class="ldate">TUE 10</span><span class="lroute">Krabi &rarr; 360 Issara</span><span class="lmode">Included</span></div>
      <table>
        <tr class="pick"><td class="t">Krabi &rarr; Chiew Larn</td><td class="n">private car</td><td class="p">~2h00</td></tr>
        <tr class="pick"><td class="t">Pier 12:00 or 15:30</td><td class="n">longtail boat</td><td class="p">~1h30</td></tr>
      </table>
      <div class="foot"><strong>Transfer is included in the package.</strong> Meet at 500Rai Pier Office, Chiew Larn. Boats leave pier 12:00 / 15:30 only. Small bags — you climb down to the boat.</div>
    </div>

    <div class="leg">
      <div class="lhd"><span class="ldate">FRI 13</span><span class="lroute">Khao Sok &rarr; Bangkok</span><span class="lmode">Road + Air</span></div>
      <table>
        <tr><td class="t">Resort boat 10:30</td><td class="n">scheduled</td><td class="p">URT ~13:00</td></tr>
        <tr class="pick"><td class="t">16:40 &rarr; 17:55</td><td class="n">SL741 &rarr; DMK · BOOKED</td><td class="p">OWUPXU</td></tr>
        <tr><td class="t">18:50 &rarr; 20:05</td><td class="n">VZ353 &rarr; BKK · not taken</td><td class="p">$110</td></tr>
      </table>
      <div class="foot"><strong>Lands at Don Mueang</strong>, not Suvarnabhumi — but Saturday's flight home leaves from Suvarnabhumi. Red Line to Krung Thep Aphiwat, then MRT to Asok.</div>
    </div>

  </div>
</div>
<div class="legend">
  <span class="lg"><span class="sw sw-bkk"></span>Bangkok</span>
  <span class="lg"><span class="sw sw-cnx"></span>Chiang Mai</span>
  <span class="lg"><span class="sw sw-krb"></span>Krabi</span>
  <span class="lg"><span class="sw sw-kks"></span>Khao Sok</span>
  <span class="lg"><span class="sw" style="background:linear-gradient(135deg,#7ED8CB 0%,#7ED8CB 49.4%,#FFFFFF 49.4%,#FFFFFF 50.6%,#9BCE91 50.6%,#9BCE91 100%)"></span>split = region change</span>
  <span class="lg note" style="margin-left:auto">Prices indicative · confirm at booking</span>
</div>
</body></html>"""

pathlib.Path(ROOT / 'scripts' / '_calendar.html').write_text(html)
from weasyprint import HTML
HTML(str(ROOT / 'scripts' / '_calendar.html')).write_pdf(str(OUT))
print(f"Wrote {OUT}")
