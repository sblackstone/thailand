#!/usr/bin/env python3
"""
Build the agent-style travel dossier -- the long-form, printable document.

This is a THIRD document, deliberately unlike the other two. It follows the
layout of the Iceland Offbeat dossier Stephen used in 2024: cover, trip
summary, an information section, a day-by-day timeline with icon badges, and
a voucher block per booking. That format is the point; see DESIGN.md's note
that the print calendar is light "deliberately" -- same reasoning here. A
document you read in a car or hand to a hotel desk should be ink-light and
plainly structured, not the dark web itinerary.

Typography still follows the house rules: Instrument Sans for prose, IBM Plex
Mono for every time, code and confirmation number, Fraunces for display.

Content is transcribed from site/index.html, which remains the source of
truth. If a date or booking changes there, change the DAYS table below too --
same standing hazard as build_calendar.py's `trip` dict.

Run:  python3 scripts/build_dossier.py
Out:  site/Thailand-Dossier-Nov2026.pdf
"""
import html as _html
import pathlib

from fonts import ensure_fonts, font_face_css

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "Thailand-Dossier-Nov2026.pdf"

# ---------------------------------------------------------------- icon badges
# Unicode symbols render as tofu in these fonts (DESIGN.md quirk 6), so every
# glyph here is inline SVG. Colour keys the entry type, as in the template.
STROKE = ('fill="none" stroke="currentColor" stroke-width="1.8" '
          'stroke-linecap="round" stroke-linejoin="round"')

ICONS = {
    "info": f'<svg viewBox="0 0 24 24" {STROKE}><circle cx="12" cy="12" r="8.6"/>'
            f'<path d="M12 11.4v4.9"/><path d="M12 8.1v.01" stroke-width="2.4"/></svg>',
    "stay": f'<svg viewBox="0 0 24 24" {STROKE}><path d="M3 18V7M3 12h13a4 4 0 0 1 4 4v2"/>'
            f'<path d="M3 18h18"/><circle cx="7.5" cy="9.5" r="1.6"/></svg>',
    "fly":  f'<svg viewBox="0 0 24 24" {STROKE}><path d="M17.8 19.2 16 11l3.5-3.5a2.1 2.1 0 0 0-3-3'
            f'L13 8 4.8 6.2l-1.4 1.4 5.9 3.4-2.8 2.8-2.3-.5-1 1 3.4 2 2 3.4 1-1-.5-2.3 2.8-2.8 3.4 5.9z"/></svg>',
    "rail": f'<svg viewBox="0 0 24 24" {STROKE}><rect x="6" y="4" width="12" height="13" rx="2.5"/>'
            f'<path d="M6 11h12"/><path d="M8 21l1.5-3M16 21l-1.5-3"/></svg>',
    "road": f'<svg viewBox="0 0 24 24" {STROKE}><path d="M4 15h16M6 15V9a2 2 0 0 1 2-2h5l3 3"/>'
            f'<circle cx="8" cy="18.5" r="1.3"/><circle cx="16" cy="18.5" r="1.3"/></svg>',
    "boat": f'<svg viewBox="0 0 24 24" {STROKE}><path d="M3 17c1.6 0 1.6 1.4 3.2 1.4S7.8 17 9.4 17s1.6 1.4 3.2 1.4'
            f'S14.2 17 15.8 17s1.6 1.4 3.2 1.4"/><path d="M5 14l1.4-4.6A2 2 0 0 1 8.3 8h7.4a2 2 0 0 1 1.9 1.4L19 14"/>'
            f'<path d="M12 8V4"/></svg>',
    "tour": f'<svg viewBox="0 0 24 24" {STROKE}><rect x="3.5" y="5" width="17" height="15" rx="2.5"/>'
            f'<path d="M3.5 10h17M8 3.5v3M16 3.5v3"/></svg>',
}

# Entry type -> (icon key, accent). Accents are the light-print region tints
# from DESIGN.md plus an ink tone, so this document sits in the same family
# as the calendar without copying the dark itinerary's palette.
KINDS = {
    "info":     ("info", "#7A8F87"),
    "stay":     ("stay", "#C98A1E"),
    "fly":      ("fly",  "#2E9C8D"),
    "rail":     ("rail", "#C2703A"),
    "road":     ("road", "#4E8F46"),
    "boat":     ("boat", "#4E8F46"),
    "tour":     ("tour", "#15332C"),
    "optional": ("info", "#9AA8A2"),
}

# ------------------------------------------------------------------ trip data
# (kind, title, body). Body is HTML; keep times 24-hour and refs in <code>.
DAYS = [
 ("Sunday", "November 1", "Bangkok", [
  ("info", "Sawatdee khrap &mdash; welcome to Thailand",
   "You land at Suvarnabhumi after roughly 21 hours in transit and a 12-hour time shift. "
   "Take it gently; the day is built to be abandoned if you need to sleep."),
  ("fly", "EK374 arrives 07:35",
   "Dubai &rarr; Bangkok Suvarnabhumi (BKK), Airbus A380. Booking reference <code>H2M5FJ</code>."),
  ("info", "Airport to the hotel",
   "Clear immigration, then the <b>Airport Rail Link to Makkasan</b> and the MRT one stop pattern to "
   "<b>Lumphini</b>. That exit is about 300 m from the door &mdash; noticeably better with cases than "
   "walking from Ploen Chit."),
  ("stay", "Check in &mdash; The Ritz-Carlton, Bangkok",
   "Confirmation <code>90034653</code> &middot; 2 nights &middot; Deluxe Room, 1 King, Park View. "
   "Standard check-in is 15:00, but early check-in is one of your Edit benefits &mdash; ask at the desk. "
   "If the room isn't ready, leave the bags and start the day anyway."),
  ("info", "Use The Edit benefits &mdash; this stay only",
   "Booking through The Edit includes <b>breakfast for two daily</b>, a <b>USD 100 property credit</b> "
   "(once per stay, not against room rate, tax or gratuities), a welcome amenity, Wi-Fi, and a room "
   "upgrade plus early check-in and late check-out, all subject to availability. None of it is applied "
   "automatically &mdash; ask for each. U Chiang Mai and Centara were booked through Chase Travel too, "
   "but neither carries these."),
  ("info", "Wat Pho",
   "The reclining Buddha, 46 m of gilded plaster, and the country's oldest centre of massage teaching. "
   "A foot massage at the temple's own school is the correct way to spend the first afternoon."),
  ("info", "Sunset on the Chao Phraya",
   "A boat as the light goes, then a riverside dinner with <b>Wat Arun</b> lit across the water. "
   "Early night &mdash; you'll have earned it."),
 ]),

 ("Monday", "November 2", "Bangkok", [
  ("info", "Grand Palace &amp; Wat Phra Kaew",
   "Be there at opening. The Emerald Buddha sits in the royal chapel; the complex is the single most "
   "crowded thing you will do all fortnight, and the heat compounds it. Shoulders and knees covered."),
  ("info", "Wat Arun",
   "Cross by ferry. Climb the central prang for the view back over the river."),
  ("optional", "Jim Thompson House",
   "Six teak houses assembled by the American who rebuilt the Thai silk trade and then vanished in the "
   "Malaysian jungle in 1967. A cool, shaded hour."),
  ("info", "Yaowarat after dark",
   "Chinatown's street-food stretch. Go hungry and eat standing up."),
  ("stay", "The Ritz-Carlton, Bangkok",
   "Second night. Breakfast for two is included &mdash; it is an Edit benefit, not a room-rate inclusion, "
   "so mention it."),
 ]),

 ("Tuesday", "November 3", "Bangkok &rarr; the night train", [
  ("optional", "Floating market, or a food tour &mdash; not both",
   "The <b>Maeklong railway market</b> and <b>Damnoen Saduak</b> are 80&ndash;100 km southwest and the "
   "market is finished by late morning, so those half-days leave the city around 06:30. If that's too "
   "early after two days of jet lag, take a slow morning and a guided food tour instead."),
  ("info", "Ask for late check-out",
   "An Edit benefit, and worth claiming: a shower before thirteen hours in a sleeper berth is not nothing. "
   "Pack an overnight bag you can actually reach from the berth."),
  ("rail", "Special Express #9 &mdash; 18:40 to Chiang Mai",
   "Krung Thep Aphiwat (KTW) 18:40 &rarr; Chiang Mai (CGM) 07:15 next morning. Roughly 13 hours, 751 km. "
   "Two 2nd-class A/C sleeper berths, reservation <code>34511470</code>, e-tickets issued. "
   "<b>Be at the station by 18:10.</b> Dinner in the dining car, then berths down."),
 ]),

 ("Wednesday", "November 4", "Chiang Mai", [
  ("rail", "Arrive Chiang Mai 07:15",
   "Thirteen hours north and about six degrees cooler."),
  ("stay", "Check in &mdash; U Chiang Mai",
   "Confirmation <code>2535552787</code> &middot; Deluxe with Bathtub, 1 King, inside the moat. "
   "<b>The room is held from the 3rd</b>, the night you were on the train &mdash; paid deliberately so "
   "it is yours the moment you step off the sleeper, whatever the train does. Non-refundable. "
   "Breakfast is extra, about <b>THB 399</b> each."),
  ("info", "The Old City on foot",
   "<b>Wat Chedi Luang</b>, whose 15th-century chedi lost its top thirty metres to an earthquake, and "
   "<b>Wat Phra Singh</b>. The quiet lanes between the two are the actual pleasure."),
  ("info", "Night Bazaar and khao soi",
   "The north's signature dish: egg noodles in a coconut curry broth, crisp noodles on top, pickled "
   "mustard greens and lime alongside."),
 ]),

 ("Thursday", "November 5", "Chiang Mai", [
  ("tour", "Ethical elephant sanctuary &mdash; NOT YET BOOKED",
   "A full day at a genuine sanctuary &mdash; Elephant Nature Park or similar. Feeding and observing, "
   "no riding, no bathing circus. <b>This is the one thing to lock in first:</b> places sell out in "
   "season, and it is the centrepiece of the day."),
  ("info", "Nimman in the evening",
   "The caf&eacute; and craft-beer district west of the moat. Where Chiang Mai goes when it isn't "
   "being a temple town."),
  ("stay", "U Chiang Mai", ""),
 ]),

 ("Friday", "November 6", "Chiang Mai", [
  ("info", "Wat Phra That Doi Suthep",
   "The gold chedi on the mountain above the city, reached by 306 steps flanked by naga balustrades. "
   "Morning, before the haze and the coaches."),
  ("info", "The Old City, slowly",
   "A market, a massage, one more bowl of khao soi."),
  ("optional", "Or swap the whole day for Doi Inthanon",
   "Thailand's highest peak, with waterfalls and the twin royal chedis. But treat it as a <b>full day</b>: "
   "it is 2&ndash;2&frac12; hours each way, in the opposite direction from Doi Suthep. You would leave "
   "about 07:00 and skip the temple. It does not fit as an afternoon."),
  ("info", "Repack tonight",
   "Tomorrow starts early &mdash; you are away from the hotel by about 06:00."),
 ]),

 ("Saturday", "November 7", "Krabi", [
  ("fly", "FD3072 &mdash; Chiang Mai 07:55 &rarr; Krabi 09:55",
   "Thai AirAsia, A320, non-stop. Booking <code>UYTUHF</code>. Roughly two hours in the air."),
  ("road", "Krabi airport to Ao Nang",
   "About 30 minutes."),
  ("stay", "Check in &mdash; Centara Ao Nang Beach Resort &amp; Spa",
   "Confirmation <code>2535573436</code> &middot; 3 nights &middot; Deluxe Room, 1 King, Pool Access. "
   "<b>You land well before check-in at 15:00</b> &mdash; leave the bags at reception and start on the "
   "beach. Two things to ask for on arrival: a room <b>away from the drainage canal</b> that runs "
   "between the wings, which is a recurring smell complaint, and confirmation of the pool-access room "
   "you paid for. Non-refundable; breakfast extra, around <b>THB 325&ndash;650</b> each."),
  ("info", "First Andaman sunset",
   "Afternoon on the sand, then a long seafood dinner."),
 ]),

 ("Sunday", "November 8", "Krabi", [
  ("tour", "Island-hopping &mdash; not booked",
   "A full day by boat: the <b>Hong Islands</b> lagoon, or the classic <b>4-Islands</b> route taking in "
   "Phra Nang cave beach, Tup, Chicken and Poda. Longtails leave from the Ao Nang beach pier, about ten "
   "minutes' walk. Book locally the day before."),
  ("info", "The most weather-dependent day of the trip",
   "Early-November seas are still unsettled and boat trips are the first thing cancelled. If it's rough, "
   "swap with tomorrow and do the inland day instead &mdash; that flexibility is the whole reason these "
   "two days sit next to each other."),
  ("info", "Reef-safe sunscreen",
   "Oxybenzone sunscreens are banned in Thai marine national parks."),
 ]),

 ("Monday", "November 9", "Krabi", [
  ("optional", "Tiger Cave Temple at sunrise",
   "1,260 steps to the summit shrine and a view over the whole Krabi plain. Brutal in the heat, which is "
   "the argument for going at dawn."),
  ("optional", "Emerald Pool &amp; hot springs",
   "Inland, in rainforest &mdash; a spring-fed pool the colour of its name and a set of warm cascades. "
   "The gentler alternative to the steps; easy afternoon back at the beach."),
  ("info", "Long drive tomorrow",
   "Repack tonight and keep one small bag accessible &mdash; you climb down stairs into a boat "
   "tomorrow and the big cases can stay at the pier office."),
 ]),

 ("Tuesday", "November 10", "Khao Sok", [
  ("road", "Leave Krabi by 09:00",
   "About <b>2 hours by road</b> to the 500Rai Pier Office at Chiew Larn. The private car is included in "
   "the resort package. Leave early enough for slack at the pier &mdash; you need to pay the park fee and "
   "get bags down to the boat before it goes, not arrive dead on the hour."),
  ("boat", "Longtail across Cheow Lan Lake &mdash; 12:00",
   "About <b>1.5 hours</b>, sightseeing on the way, and the resort appears like a floating village under "
   "the karsts. Boats out to the resort leave the pier at <b>12:00 or 15:30 only</b>. Miss the 12:00 and "
   "you arrive after the sunset cruise below."),
  ("info", "THB 340 each, in cash",
   "The national park fee, payable on arrival and not included in the package. Bring it in cash."),
  ("stay", "Check in &mdash; 360&deg; Issara Floating Resort",
   "Booking <code>0592406</code> &middot; 3 nights &middot; the 3-Night Essence package, all-in. "
   "Check-in from 14:00. <b>Air-conditioning runs 12:00&ndash;06:00 only</b>, and that applies to all "
   "three nights."),
  ("tour", "Wildlife safari &amp; sunset cruise &mdash; 17:00",
   "Included. Swim off the deck first; set dinner is served over the water."),
 ]),

 ("Wednesday", "November 11", "Khao Sok", [
  ("tour", "Pakarang Cave Trail &mdash; 09:45",
   "The one fixed thing today: a 1.5 km trek plus a bamboo raft. <b>THB 200 each, cash</b>, not included."),
  ("info", "Then nothing at all",
   "Kayak straight off your own balcony &mdash; every room has one. Swim in the fresh water, read, "
   "watch the light move across the karsts. This is the day the trip is built around."),
 ]),

 ("Thursday", "November 12", "Khao Sok", [
  ("info", "Morning on the lake",
   "Sightseeing along the shoreline &mdash; gibbons, hornbills, and elephants if you are lucky."),
  ("tour", "Prakai Petch Cave Trail &mdash; confirm this one",
   "Swamp forest, small waterfalls and a glittering cave. The resort lists it as running "
   "<b>Mon / Wed / Sat</b>, and the 12th is a <b>Thursday</b> &mdash; so confirm it on arrival rather "
   "than counting on it. The morning lake trip above is the fallback."),
  ("tour", "Last sunset cruise &mdash; 17:00", ""),
  ("info", "Pack tonight",
   "<b>Check-out is 10:00</b> and tomorrow is the tightest day of the trip."),
 ]),

 ("Friday", "November 13", "Khao Sok &rarr; Bangkok", [
  ("boat", "Check out 10:00, boat out at 10:30",
   "<b>This is the only scheduled boat back.</b> It feeds a non-refundable flight the same afternoon, so "
   "reconfirm it with the resort the day before and don't plan on arranging something later."),
  ("road", "Chiew Larn to Surat Thani",
   "At the airport (URT) around 13:00, which leaves roughly three and a half hours in hand."),
  ("fly", "SL741 &mdash; Surat Thani 16:40 &rarr; Don Mueang 17:55",
   "Thai Lion Air, arriving <b>Terminal 2</b>. Reservation code <code>OWUPXU</code>. Note this is "
   "<b>Don Mueang, not Suvarnabhumi</b>."),
  ("info", "Into the city by rail, not road",
   "Take the <b>SRT Red Line</b> to Krung Thep Aphiwat, then the MRT to Sukhumvit. It's a Friday and the "
   "roads will be at their worst; the train is elevated and ignores them. Reckon on being checked in "
   "around 19:00&ndash;19:30."),
  ("stay", "Check in &mdash; Grande Centre Point Terminal 21",
   "Travelocity itinerary <code>73523066938869</code> &middot; 1 night &middot; Executive Suite for two. "
   "The hotel sits on top of the Asok interchange, so dinner is downstairs. Non-refundable."),
 ]),

 ("Saturday", "November 14", "Bangkok &rarr; home", [
  ("info", "A half day, not a full one",
   "Check out at 12:00 and leave the bags at the desk. You have about five hours, so keep it central &mdash; "
   "<b>ICONSIAM</b>, Jim Thompson House, a last massage. Not Ayutthaya; it needs the better part of a day."),
  ("info", "Leave by 17:00 &mdash; and mind the airport",
   "You arrived at <b>Don Mueang</b> yesterday but fly home from <b>Suvarnabhumi</b>. They are 50 km "
   "apart. From Asok it is one MRT stop to Phetchaburi and straight onto the <b>Airport Rail Link at "
   "Makkasan</b> &mdash; about 30 minutes, and no traffic to allow for."),
  ("fly", "EK373 &mdash; 20:45 to Dubai, then JFK",
   "Suvarnabhumi 20:45 &rarr; Dubai, connecting to New York JFK at 08:15 Sunday. Booking "
   "<code>H2M5FJ</code>. At the airport by about 17:45."),
  ("info", "Chok dee",
   "Fourteen days, thirteen nights, five bases and four ways of travelling between them. Safe flight home."),
 ]),
]

# --------------------------------------------------------------- booking data
# (label, supplier, reference, when, detail, status)
VOUCHERS = [
 ("Flights &mdash; international", "Emirates", "H2M5FJ",
  "Out 30 Oct &middot; back 14 Nov",
  "EK202 JFK 19:45 &rarr; Dubai &middot; EK374 Dubai &rarr; Bangkok, arrives 07:35 on 1 Nov. "
  "Returning EK373 Bangkok 20:45 on 14 Nov &rarr; Dubai &rarr; JFK 08:15 on the 15th. "
  "Economy, both passengers, A380 on the Bangkok legs.", "Confirmed &middot; seats purchased"),
 ("Hotel &mdash; Bangkok", "The Ritz-Carlton, Bangkok", "90034653",
  "1&ndash;3 Nov &middot; 2 nights",
  "Deluxe Room, 1 King Bed, Park View. Booked through Chase Travel (Trip 1027840438) under The Edit: "
  "breakfast for two daily, USD 100 property credit, welcome amenity, Wi-Fi, and upgrade / early "
  "check-in / late check-out subject to availability.", "Confirmed &middot; paid"),
 ("Rail &mdash; Bangkok to Chiang Mai", "State Railway of Thailand", "34511470",
  "3 Nov &middot; 18:40 &rarr; 07:15",
  "Special Express #9, two 2nd-class A/C sleeper berths. Krung Thep Aphiwat (KTW) to Chiang Mai (CGM), "
  "about 13 hours. E-tickets issued; be at the station by 18:10.", "Ticketed"),
 ("Hotel &mdash; Chiang Mai", "U Chiang Mai", "2535552787",
  "3&ndash;7 Nov &middot; room held from the 3rd",
  "Deluxe with Bathtub, 1 King, two guests. Booked through Chase Travel (Trip 1027896876). The night of "
  "the 3rd is paid deliberately so the room is available on arrival at 07:15 on the 4th. "
  "Breakfast not included, about THB 399 each.", "Confirmed &middot; NON-REFUNDABLE"),
 ("Flight &mdash; Chiang Mai to Krabi", "Thai AirAsia", "UYTUHF",
  "7 Nov &middot; 07:55 &rarr; 09:55",
  "FD3072, Airbus A320, non-stop. Both passengers.", "Confirmed"),
 ("Hotel &mdash; Krabi", "Centara Ao Nang Beach Resort &amp; Spa", "2535573436",
  "7&ndash;10 Nov &middot; 3 nights",
  "Deluxe Room, 1 King Bed, Pool Access. Booked through Chase Travel (Trip 1027898679). Check-in 15:00, "
  "check-out 12:00. Ask for a room away from the drainage canal. Breakfast extra, THB 325&ndash;650 each.",
  "Confirmed &middot; NON-REFUNDABLE"),
 ("Resort &mdash; Khao Sok", "360&deg; Issara Floating Resort", "0592406",
  "10&ndash;13 Nov &middot; 3 nights",
  "3-Night Essence package, all-inclusive. Private car from Krabi and the longtail transfer are both "
  "included. Boats to the resort leave Chiew Larn at 12:00 or 15:30 only; the return boat is 10:30. "
  "THB 340 each in cash for the national park fee. A/C runs 12:00&ndash;06:00.",
  "Confirmed &middot; transfers included"),
 ("Flight &mdash; Surat Thani to Bangkok", "Thai Lion Air", "OWUPXU",
  "13 Nov &middot; 16:40 &rarr; 17:55",
  "SL741, arriving Don Mueang (DMK) Terminal 2 &mdash; not Suvarnabhumi. Both passengers ticketed; "
  "check-in required.", "Confirmed"),
 ("Hotel &mdash; Bangkok", "Grande Centre Point Terminal 21", "73523066938869",
  "13&ndash;14 Nov &middot; 1 night",
  "Executive Suite for two, on the Asok interchange. Booked through Travelocity. Check-in from 14:00, "
  "check-out 12:00. The card used to book must be presented at check-in with matching photo ID.",
  "Confirmed &middot; NON-REFUNDABLE"),
]


def esc(s: str) -> str:
    return _html.escape(s, quote=False)


def badge(kind: str) -> str:
    icon_key, colour = KINDS[kind]
    return (f'<span class="bdg" style="color:{colour};border-color:{colour}">'
            f'{ICONS[icon_key]}</span>')


def entry_html(kind: str, title: str, body: str) -> str:
    prefix = '<span class="opt">Optional &mdash; </span>' if kind == "optional" else ""
    body_html = f'<p>{body}</p>' if body else ""
    return (f'<div class="entry">{badge(kind)}'
            f'<div class="ec"><h4>{prefix}{title}</h4>{body_html}</div></div>')


def summary_html() -> str:
    out = []
    for weekday, date, region, entries in DAYS:
        items = "".join(
            f'<li>{"Optional &mdash; " if k == "optional" else ""}{t}</li>'
            for k, t, _ in entries
        )
        out.append(
            f'<div class="sday"><h3>{date} &mdash; {weekday}'
            f'<span class="sreg">{region}</span></h3><ul>{items}</ul></div>'
        )
    return "".join(out)


def days_html() -> str:
    out = []
    for weekday, date, region, entries in DAYS:
        body = "".join(entry_html(k, t, b) for k, t, b in entries)
        out.append(
            f'<section class="day"><h2 class="dayhead">{date} &mdash; {weekday}'
            f'<span class="dreg">{region}</span></h2>'
            f'<div class="timeline">{body}</div></section>'
        )
    return "".join(out)


def vouchers_html() -> str:
    rows = []
    for label, supplier, ref, when, detail, status in VOUCHERS:
        # Colour the restriction separately from the confirmation.
        parts = [p.strip() for p in status.split("&middot;")]
        marked = " &middot; ".join(
            f'<span class="vwarn">{p}</span>' if "REFUND" in p.upper() else p
            for p in parts
        )
        rows.append(
            f'<div class="vch">'
            f'<div class="vhd"><span class="vlabel">{label}</span>'
            f'<span class="vstatus">{marked}</span></div>'
            f'<h3>{supplier}</h3>'
            f'<div class="vmeta"><span class="vref">{ref}</span>'
            f'<span class="vwhen">{when}</span></div>'
            f'<p>{detail}</p></div>'
        )
    return "".join(rows)


CSS = """
@page{
  size: letter; margin: 18mm 16mm 16mm;
  @bottom-right{
    content: "Page " counter(page) " of " counter(pages);
    font-family:"IBM Plex Mono",monospace; font-size:7.6pt; color:#8C9C96;
  }
  @bottom-left{
    content: "Thailand · 1–14 November 2026";
    font-family:"IBM Plex Mono",monospace; font-size:7.6pt;
    letter-spacing:.06em; color:#8C9C96;
  }
}
@page:first{ @bottom-left{content:""} @bottom-right{content:""} }

html{ background:#fff }
*{ box-sizing:border-box; margin:0; padding:0 }
body{
  font-family:"Instrument Sans",sans-serif; color:#263B35;
  font-size:9.9pt; line-height:1.5;
}
code{
  font-family:"IBM Plex Mono",monospace; font-size:.94em;
  letter-spacing:.02em; color:#15332C; font-weight:500;
  background:#F1F5F3; padding:.5pt 2pt; border-radius:2.5pt;
}
b{ font-weight:600; color:#15332C }

/* ---------------------------------------------------------------- cover */
.cover{ height:23.6cm; display:flex; flex-direction:column }
.cbrand{
  font-family:"IBM Plex Mono",monospace; font-size:8pt; letter-spacing:.22em;
  text-transform:uppercase; color:#7A8F87;
  border-bottom:1px solid #DDE6E2; padding-bottom:9pt;
}
.cmid{ flex:1 1 auto; padding-top:4.6cm }
.cover h1{
  font-family:"Fraunces",serif; font-weight:400; font-size:40pt;
  line-height:1.06; color:#15332C; letter-spacing:-.4pt;
}
.cover h1 em{ font-style:italic; color:#C2703A }
.cdate{
  font-family:"IBM Plex Mono",monospace; font-size:11pt; letter-spacing:.1em;
  color:#4E6660; margin-top:16pt;
}
.cwho{ margin-top:6pt; color:#6B807A; font-size:10.5pt }
.crule{ height:2.5pt; width:88pt; background:#C2703A; margin:26pt 0 0 }
.cfoot{
  border-top:1px solid #DDE6E2; padding-top:10pt;
  font-family:"IBM Plex Mono",monospace; font-size:8pt; letter-spacing:.08em;
  color:#7A8F87; display:flex; justify-content:space-between;
}

/* -------------------------------------------------------------- headings */
.sect{ break-before:page }
h1.page-title{
  font-family:"Fraunces",serif; font-weight:500; font-size:21pt; color:#15332C;
  border-bottom:1px solid #DDE6E2; padding-bottom:7pt; margin-bottom:15pt;
}
h2.dayhead{
  font-family:"Fraunces",serif; font-weight:500; font-size:15.5pt; color:#15332C;
  border-bottom:1px solid #E4EBE8; padding-bottom:5pt; margin:0 0 12pt;
  break-after:avoid;
}
.dreg,.sreg{
  font-family:"IBM Plex Mono",monospace; font-size:7.8pt; letter-spacing:.14em;
  text-transform:uppercase; color:#8C9C96; float:right; padding-top:6pt;
  font-weight:400;
}

/* --------------------------------------------------------- trip summary */
.sday{ break-inside:avoid; margin-bottom:13pt }
.sday h3{
  font-family:"Fraunces",serif; font-weight:500; font-size:12pt; color:#2E4A42;
  margin-bottom:4pt;
}
.sday ul{ list-style:none; border-left:1px solid #E4EBE8; padding-left:11pt }
.sday li{ color:#4E6660; font-size:9.4pt; padding:1.4pt 0 }

/* ------------------------------------------------------------- timeline */
.day{ break-inside:auto; margin-bottom:16pt }
.timeline{ border-left:1px solid #E4EBE8; margin-left:15pt }
.entry{ display:flex; break-inside:avoid; padding-bottom:11pt }
/* The badge is a descendant of .timeline, so it paints over that border --
   which is what makes it sit ON the rail rather than beside it. */
.bdg{
  flex:0 0 21pt; height:21pt; margin-left:-10.5pt; border-radius:50%;
  border:1.4px solid; background:#fff; display:flex;
  align-items:center; justify-content:center;
}
.bdg svg{ width:11.5pt; height:11.5pt; display:block }
.ec{ flex:1 1 auto; min-width:0; padding-left:12pt; padding-top:2.4pt }
.ec h4{
  font-size:10.2pt; font-weight:600; color:#15332C; line-height:1.35;
  margin-bottom:2.5pt;
}
.ec p{ color:#4E6660; font-size:9.5pt }
.opt{ color:#9AA8A2; font-weight:500 }

/* ------------------------------------------------------------- info box */
.ibox{ break-inside:avoid; margin-bottom:13pt }
.ibox h3{
  font-size:10.4pt; font-weight:600; color:#15332C; margin-bottom:3pt;
}
.ibox p{ color:#4E6660; font-size:9.5pt; margin-bottom:4pt }
.nums{ list-style:none; margin:5pt 0 0 }
.nums li{
  font-size:9.4pt; color:#4E6660; padding:2.6pt 0;
  border-bottom:1px dotted #E4EBE8;
}
.nums b{ display:inline-block; min-width:132pt }
.nums code{ font-size:9pt }

/* ------------------------------------------------------------- vouchers */
.vch{
  break-inside:avoid; border:1px solid #E0E8E5; border-radius:4pt;
  padding:11pt 13pt; margin-bottom:9pt;
}
.vhd{ display:flex; justify-content:space-between; margin-bottom:4pt }
.vlabel{
  font-family:"IBM Plex Mono",monospace; font-size:7.4pt; letter-spacing:.14em;
  text-transform:uppercase; color:#8C9C96;
}
.vstatus{
  font-family:"IBM Plex Mono",monospace; font-size:7.4pt; letter-spacing:.09em;
  text-transform:uppercase; color:#4E8F46; font-weight:500;
}
/* A cancellation restriction is a caution, not a reassurance -- it must not
   read in the same green as "confirmed". */
.vwarn{ color:#B0521E; font-weight:500 }
.vch h3{
  font-family:"Fraunces",serif; font-weight:500; font-size:13pt; color:#15332C;
  margin-bottom:4pt;
}
.vmeta{ margin-bottom:5pt }
.vref{
  font-family:"IBM Plex Mono",monospace; font-size:9.6pt; font-weight:500;
  color:#15332C; background:#F1F5F3; padding:1.6pt 5pt; border-radius:2.5pt;
}
.vwhen{
  font-family:"IBM Plex Mono",monospace; font-size:8.4pt; color:#7A8F87;
  margin-left:8pt; letter-spacing:.05em;
}
.vch p{ color:#4E6660; font-size:9.3pt }
.leadin{ color:#4E6660; font-size:9.8pt; margin-bottom:13pt; max-width:34em }
"""


def build() -> pathlib.Path:
    ensure_fonts()

    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="author" content="Trip plan">
<title>Thailand &middot; November 2026 &middot; Dossier</title>
<style>
{font_face_css()}
{CSS}
</style></head><body>

<div class="cover">
  <div class="cbrand">Travel dossier &middot; prepared for Stephen &amp; Doug</div>
  <div class="cmid">
    <h1>Thailand<br><em>November 2026</em></h1>
    <div class="crule"></div>
    <div class="cdate">1 &ndash; 14 NOVEMBER 2026</div>
    <div class="cwho">Bangkok &middot; Chiang Mai &middot; Krabi &middot; Khao Sok &middot; Bangkok<br>
      14 days, 13 nights, two travellers</div>
  </div>
  <div class="cfoot"><span>EK374 in 07:35 &middot; EK373 out 20:45</span><span>REF H2M5FJ</span></div>
</div>

<div class="sect">
  <h1 class="page-title">Trip summary</h1>
  {summary_html()}
</div>

<div class="sect">
  <h1 class="page-title">Information &amp; documents</h1>
  <p class="leadin">Everything below is either a number you might need in a hurry or a thing that is
  easy to forget on the day. The day-by-day pages follow.</p>

  <div class="ibox">
    <h3>Using this document</h3>
    <p>Keep it on your phone; you do not need to print the confirmations. Your name and the confirmation
    number are enough at every hotel. Every booking reference in this document also appears on the
    published itinerary at the download link, so either will do at a desk.</p>
  </div>

  <div class="ibox">
    <h3>Emergency numbers &mdash; Thailand</h3>
    <ul class="nums">
      <li><b>All emergencies</b> <code>191</code></li>
      <li><b>Medical / ambulance</b> <code>1669</code></li>
      <li><b>Tourist police</b> <code>1155</code> &mdash; English-speaking</li>
    </ul>
  </div>

  <div class="ibox">
    <h3>Suppliers</h3>
    <p>For anything urgent on the day, call the operator directly rather than the agent &mdash; it is
    faster.</p>
    <ul class="nums">
      <li><b>360&deg; Issara</b> <code>+66 2 474 0360</code></li>
      <li><b>Thai Lion Air</b> <code>+66 2 529 9999</code></li>
      <li><b>Chase Travel</b> <code>1-855-234-2542</code> &mdash; Ritz-Carlton, U Chiang Mai, Centara</li>
    </ul>
  </div>

  <div class="ibox">
    <h3>Travel insurance</h3>
    <p>A Berkshire Hathaway Travel Protection policy covering this trip is in place; the policy document
    and number are in the trip email thread. Worth having the number to hand before you fly rather than
    hunting for it from a boat.</p>
  </div>

  <div class="ibox">
    <h3>Weather and conditions</h3>
    <p>Early November is the front edge of the cool, dry season, but it is a front edge rather than a
    guarantee. The Andaman is still drying out &mdash; expect a wet afternoon or two around Krabi, and
    treat the island-hopping day as the one to move. Khao Sok is at its lushest precisely because the
    rain has only just stopped. Sea state is the thing that cancels boat trips, so ask at the hotel desk
    the evening before rather than the morning of.</p>
  </div>

  <div class="ibox">
    <h3>Cash</h3>
    <p>Card works nearly everywhere, but two things on this trip are cash-only and both are at Khao Sok:
    the national park fee of <b>THB 340 per person</b> on arrival, and <b>THB 200 each</b> for the
    Pakarang cave trail. Draw that before you leave Krabi &mdash; there is no ATM on the lake.</p>
  </div>

  <div class="ibox">
    <h3>Still to book</h3>
    <p>Every night and every flight is confirmed. No activity is: the elephant sanctuary on the 5th is
    the one to arrange first, as places sell out in season. The island-hopping boat on the 8th, Tiger
    Cave or the Emerald Pool on the 9th, and the two cave trails at Khao Sok can all be arranged locally
    &mdash; but the cave trails have fixed departure times and run only on certain days.</p>
  </div>
</div>

<div class="sect">
  <h1 class="page-title">Day by day</h1>
  {days_html()}
</div>

<div class="sect">
  <h1 class="page-title">Bookings &amp; references</h1>
  <p class="leadin">Every confirmed booking, in trip order. Name and reference are sufficient at
  check-in.</p>
  {vouchers_html()}
</div>

</body></html>"""

    from weasyprint import HTML

    HTML(string=doc).write_pdf(OUT)
    return OUT


if __name__ == "__main__":
    print(f"Wrote {build()}")
