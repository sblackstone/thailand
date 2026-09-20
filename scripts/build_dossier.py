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
  ("rail", "Airport to the hotel by rail",
   "Clear immigration, then follow the signs down to the <b>Airport Rail Link</b> on the basement level "
   "of the terminal. Three steps, about 45&ndash;50 minutes in total, roughly THB 65 each:<br>"
   "<b>1.</b> City Line towards Phaya Thai, alighting at <b>Makkasan</b> (A6) &mdash; about 25 minutes, "
   "THB 35. Buy a token at the machine or tap a contactless card.<br>"
   "<b>2.</b> Follow the <b>166 m covered skywalk</b> from Makkasan to <b>MRT Phetchaburi</b> &mdash; "
   "five minutes, longer with cases.<br>"
   "<b>3.</b> MRT Blue Line towards <b>Hua Lamphong</b>, four stops: Sukhumvit, Queen Sirikit, "
   "Khlong Toei, <b>Lumphini</b>. Leave by <b>Exit 1</b>, which feeds a walkway into One Bangkok; the "
   "hotel is inside it, about 300 m from the door &mdash; noticeably better with cases than walking "
   "from Ploen Chit. A taxi is 45 to 90 minutes depending on the expressway."),
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
  ("boat", "Manohra dining cruise &mdash; 20:00, booked",
   "Reservation <code>YQGNYS</code> &middot; two people &middot; prepaid THB 11,000, "
   "<b>non-refundable</b>. A converted teak rice barge from the Anantara Riverside pier on the Thonburi "
   "bank, up the Chao Phraya past <b>Wat Arun</b> and the Grand Palace lit from the water. Premium set "
   "menu with free-flow wine and beer. Getting there: MRT Lumphini &rarr; Si Lom, cross to BTS "
   "Sala Daeng &rarr; Saphan Taksin, then the free Anantara shuttle boat from Sathorn pier every 15 "
   "minutes &mdash; about an hour door to door, so leave by 18:00 and be at the pier by 19:00."),
  ("info", "Confirm the boarding time &mdash; and it is a late night",
   "The reservation reads 20:00, but Manohra's published cruise departs 19:30 with check-in from 19:15; "
   "you are booked on the &ldquo;Third Round&rdquo; seating, so the times may differ. Settle it when you "
   "call about dietary requirements &mdash; <code>riversidedining@anantara.com</code> or 02 476 0022. "
   "Back at the hotel around 23:00, after 21 hours of travelling across a 12-hour shift. Keep the "
   "afternoon soft; this is the one fixed point of the day."),
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
  ("tour", "Ayutthaya, a private full day &mdash; 09:00, booked",
   "GetYourGuide reference <code>GYG996VK39Z9</code> &middot; two adults &middot; USD 299.42 paid in "
   "full. Ten hours, private car and English-speaking guide, operated by TripGuru Thailand. It is a "
   "<b>customise-your-own</b> product &mdash; TripGuru will help you pick the temples if you ask. "
   "Pick-up from the Ritz-Carlton lobby; they confirm the time one or two days ahead. Free cancellation "
   "until 09:00 on 2 November."),
  ("info", "Check out before you leave &mdash; you are not coming back",
   "The tour collects you at 09:00 and the day ends at a railway station 80 km north. Check-out is "
   "12:00, so settle it on the way out. <b>Late check-out is worthless to you now</b>, whatever The "
   "Edit entitles you to. You have asked TripGuru to keep two backpacks in the car for the day."),
  ("rail", "Special Express #9 &mdash; boarding at Ayutthaya, 19:45",
   "The ticket reads Krung Thep Aphiwat (KTW) 18:40 &rarr; Chiang Mai (CGM) 07:15, reservation "
   "<code>34511470</code>, two 2nd-class A/C berths. <b>You are joining it at Ayutthaya instead</b>, "
   "which Thai Railways confirmed by email on 7 September: <i>&ldquo;Yes, absolutely&hellip; the train "
   "is scheduled to depart from Ayutthaya at 19:45.&rdquo;</i> The ticket stays valid; you forfeit the "
   "first 63 minutes you already paid for. <b>Be on the platform by 19:15</b> &mdash; the booked stop "
   "is about two minutes, so know which end of the platform your coach stops at before the train "
   "appears. Ask at the Ayutthaya ticket window when you arrive."),
  ("info", "The whole evening rests on the drop-off, which is NOT yet agreed",
   "The tour as sold ends where it began &mdash; back at the Ritz-Carlton. <b>A ten-hour day starting "
   "at 09:00 finishes at 19:00, which cannot reach the 18:40 out of Bangkok under any circumstances.</b> "
   "So the Ayutthaya drop-off is not a convenience, it is load-bearing. You emailed "
   "<code>reservations@thetripguru.com</code> on 20 September asking for exactly that, plus luggage "
   "storage in the car. <b>Get a written yes before 2 November</b>, which is when free cancellation "
   "ends and your last cheap exit closes. If they refuse, the tour has to be cut short by mid-afternoon "
   "and you go back for the Bangkok departure instead."),
  ("info", "Dress code and cash",
   "The ruins enforce a temple dress code: no exposed shoulders, underarms, back or knees, so carry a "
   "scarf or long-sleeved shirt. Site entry fees are not included in the tour price &mdash; bring cash. "
   "A combined pass covering six of the temples is sold at the gates and is worth it from about four "
   "sites onward."),
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
  ("info", "Wat Phra That Doi Suthep &mdash; this afternoon or not at all",
   "The gold chedi on the mountain above the city, reached by 306 steps flanked by naga balustrades. "
   "An hour up, an hour back. <b>The 5th and 6th are now both full-day booked tours</b>, so this "
   "afternoon is the only slot it has left."),
  ("info", "Night Bazaar and khao soi",
   "The north's signature dish: egg noodles in a coconut curry broth, crisp noodles on top, pickled "
   "mustard greens and lime alongside."),
 ]),

 ("Thursday", "November 5", "Chiang Mai", [
  ("tour", "Doi Inthanon private tour &mdash; 08:30, booked",
   "Tripadvisor reference <code>1444673351</code>, TripGuru reference <code>7E51T410N0DP</code> "
   "&middot; two adults &middot; USD 250 paid in full. Thailand's highest peak, the waterfalls and the "
   "twin royal chedis, as a private full-day tour with an English-speaking guide. Hotel pick-up and "
   "drop-off, air-conditioned vehicle, drinking water and the entrance fees (Doi Inthanon THB 300, "
   "Twin Pagoda THB 100) are all included. <b>Lunch is not.</b> Free cancellation up to 24 hours before."),
  ("info", "Two things TripGuru needs from you first",
   "<b>1.</b> Your WhatsApp number and the hotel name, sent before <b>18:00 the day before</b> &mdash; "
   "miss that and they collect you at a meeting point rather than the hotel. They email between 19:00 "
   "and 21:00 the night before with the details. <b>2.</b> Passport name, number and date of birth for "
   "both of you on their insurance form, which is required before the tour runs. Do both now. "
   "<code>reservations@thetripguru.com</code>."),
  ("info", "Nimman in the evening",
   "The caf&eacute; and craft-beer district west of the moat. Where Chiang Mai goes when it isn't "
   "being a temple town."),
  ("stay", "U Chiang Mai", ""),
 ]),

 ("Friday", "November 6", "Chiang Mai", [
  ("tour", "Elephant Nature Park &mdash; Elephant Highlands, booked",
   "Booking <code>55796</code> &middot; two adults &middot; THB 12,000 total. A genuine sanctuary: "
   "feeding and observing, no riding. <b>Hotel pick-up from U Chiang Mai between 08:00 and 08:45</b> "
   "&mdash; wait in the lobby, and check your name with the driver, because not every pick-up vehicle "
   "carries the park's logo. Vegan lunch, transport, admission, insurance and an English-speaking "
   "guide are included."),
  ("info", "THB 8,400 in cash, on the morning",
   "Only the <b>THB 3,600</b> deposit has been paid. The <b>THB 8,400 balance must be settled in Thai "
   "baht at the start of the trip</b> &mdash; not by card, not in advance. Draw it in Chiang Mai on the "
   "5th. This is the largest cash requirement of the fortnight."),
  ("info", "Confirm the pick-up point 72 hours ahead",
   "If the park has not been told your pick-up point within 72 hours of the trip, you are expected to "
   "start from their office at 1 Ratmakka Road instead. <code>info@elephantnaturepark.org</code> "
   "or +66 53 272855."),
  ("info", "It is a walking day, and a muddy one",
   "Moderate to fit: mountainsides and slopes, up to <b>3&frac12; hours</b> of walking, often muddy. "
   "A change of clothes and footwear is essential, plus a towel, hat, sunscreen, repellent and a "
   "refillable bottle &mdash; in <b>one small day pack each</b>, which is the whole baggage allowance."),
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
  ("boat", "9 Islands private longtail &mdash; booked",
   "GetYourGuide reference <code>GYGVN22MBRVZ</code> &middot; eight hours &middot; USD 299.43 paid in "
   "full. Operated by <b>krabiteerapongtour</b>. The booking is for a <b>private boat</b> (priced as a "
   "group of up to five, so it is just the two of you) &mdash; the route and the pace are yours to "
   "settle with the boatman rather than a fixed shared-seat circuit."),
  ("info", "Pick-up from the Centara lobby &mdash; time still to be confirmed",
   "The operator collects you from the hotel lobby and returns you to the same place. <b>They contact "
   "you to fix the pick-up time within 48 hours of booking</b> &mdash; booked 20 September, so expect "
   "that by the 22nd, and chase them if it does not come: <code>+66 81 078 5454</code>."),
  ("info", "Confirm the date when they call",
   "The confirmation email does not print the activity date. <b>8 November is inferred</b> from the "
   "cancellation deadline &mdash; GetYourGuide allows free cancellation until 24 hours before the "
   "start, and the stated deadline is 09:00 on the 7th. It matches the plan, but have them say the "
   "date out loud when they ring."),
  ("info", "No guide, no meals",
   "Neither is included. Carry cash for a beach lunch and plenty of water. Bring swimwear, sunglasses "
   "and <b>reef-safe sunscreen</b> &mdash; oxybenzone sunscreens are banned in Thai marine national "
   "parks. National park rules apply on the islands: no touching or handling marine life."),
  ("info", "The weather call now has a deadline",
   "Early-November seas are still unsettled and boat trips are the first thing cancelled. You can still "
   "cancel for a <b>full refund until 09:00 on 7 November</b> &mdash; which is the morning you fly into "
   "Krabi. Check the forecast and the sea state as soon as you land, because after that the money is "
   "spent whatever the weather does. <b>The 9th is no longer a free swap</b> &mdash; the Emerald Pool "
   "tour is booked too, and its own deadline is 08:00 on the 8th. Two consecutive mornings, two "
   "decisions; make them both when you land on the 7th."),
 ]),

 ("Monday", "November 9", "Krabi", [
  ("tour", "Emerald Pool, Hot Springs and Tiger Cave &mdash; 08:00, booked",
   "GetYourGuide reference <code>GYGN6BWWFQFY</code> &middot; two adults &middot; USD 115.82 paid in "
   "full. A small-group tour running <b>nine and a half hours</b>, operated by TripGuru Thailand. "
   "The order of the day: a swim in the <b>Emerald Pool</b>, a walk along the <b>Blue Lagoon</b>, "
   "lunch, the <b>Hot Springs Waterfall</b>, and finally the climb to <b>Tiger Cave Temple</b>. "
   "English-speaking guide, hotel pick-up and drop-off, drinking water and <b>every entrance fee</b> "
   "are included. Free cancellation until 08:00 on 8 November."),
  ("info", "The 1,260 steps are the last thing you do, not the first",
   "The old plan had Tiger Cave at dawn precisely because the climb is brutal in the heat. This tour "
   "puts it at the <b>end</b> of a nine-and-a-half-hour day, in the afternoon. Nothing to be done about "
   "the running order &mdash; just know it is coming and keep something in reserve. The summit view "
   "over the whole Krabi plain is the reward."),
  ("info", "Dress code, and what to carry",
   "Some sites on this tour <b>enforce a temple dress code</b>: no sleeveless shirts, and shoulders, "
   "underarms, back and knees covered. Carry a sarong or scarf to throw on. Also swimwear, a towel, a "
   "change of clothes, hat, sunscreen, insect repellent and <b>cash</b> &mdash; lunch is not listed "
   "among the inclusions."),
  ("info", "Pick-up: they email the night before",
   "TripGuru confirm the exact pick-up time and meeting point by email the evening before, and the "
   "booking portal carries it from 19:00&ndash;21:00. <b>Be in the Centara lobby ten minutes early.</b> "
   "The guide carries a TripGuru sign and will wait a maximum of ten minutes. Morning traffic in Ao "
   "Nang runs heavier than the map apps predict."),
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
   "<b>ICONSIAM</b>, Jim Thompson House, a last massage. Nothing that needs the better part of a day "
   "&mdash; and Ayutthaya is already behind you, done properly on the 3rd."),
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
  "<b>Out:</b> EK202 JFK <b>23:00</b> on 30 Oct &rarr; Dubai 19:45 on the 31st; 2 h 50 m in Dubai; "
  "EK374 Dubai 22:35 &rarr; Bangkok <b>07:35</b> on 1 Nov. Twenty-one and a half hours door to door. "
  "<b>Back:</b> EK373 Bangkok 20:45 on 14 Nov &rarr; Dubai 01:00; 1 h 35 m in Dubai; EK203 Dubai 02:35 "
  "&rarr; JFK <b>08:15</b> on the 15th. Economy, both passengers, A380 on the JFK legs. One checked bag "
  "each, up to 50 lb.", "Confirmed &middot; seats purchased"),
 ("Hotel &mdash; Bangkok", "The Ritz-Carlton, Bangkok", "90034653",
  "1&ndash;3 Nov &middot; 2 nights",
  "Deluxe Room, 1 King Bed, Park View. Booked through Chase Travel (Trip 1027840438) under The Edit: "
  "breakfast for two daily, USD 100 property credit, welcome amenity, Wi-Fi, and upgrade / early "
  "check-in / late check-out subject to availability.", "Confirmed &middot; paid"),
 ("Dining &mdash; Bangkok", "Manohra Dining Cruises &middot; Anantara Riverside", "YQGNYS",
  "1 Nov &middot; 20:00 &middot; 2 people",
  "Premium set menu with free-flow wine and beer, THB 5,500 each. Booked through TableCheck; "
  "THB 11,000 charged in full. Departs the Anantara Riverside pier &mdash; free shuttle boat from "
  "Sathorn pier every 15 minutes. No dietary restrictions were advised. Confirm the boarding time: "
  "the published cruise leaves 19:30 with check-in 19:15.",
  "Confirmed &middot; PREPAID, NON-REFUNDABLE"),
 ("Tour &mdash; Bangkok", "TripGuru Thailand &middot; via GetYourGuide", "GYG996VK39Z9",
  "3 Nov &middot; 09:00 &middot; 2 adults",
  "Customise-your-own full-day Ayutthaya tour, ten hours, private car and English-speaking guide. "
  "USD 299.42 paid in full. Pick-up from the Ritz-Carlton lobby. <b>The drop-off at Ayutthaya railway "
  "station is requested but not yet confirmed</b> &mdash; as sold, the tour returns to Bangkok. "
  "Site entry fees not included. Operator <code>+1 254 454 4878</code>.",
  "Confirmed &middot; free cancellation to 09:00 on 2 Nov"),
 ("Rail &mdash; Bangkok to Chiang Mai", "State Railway of Thailand", "34511470",
  "3 Nov &middot; board Ayutthaya 19:45 &rarr; 07:15",
  "Special Express #9, two 2nd-class A/C sleeper berths, ticketed Krung Thep Aphiwat (KTW) to Chiang "
  "Mai (CGM). <b>Boarding downline at Ayutthaya at 19:45</b>, confirmed by Thai Railways on 7 September; "
  "the ticket stays valid and the berths are held for the whole run. Be on the platform by 19:15 "
  "&mdash; the stop is about two minutes.", "Ticketed &middot; boarding at Ayutthaya"),
 ("Hotel &mdash; Chiang Mai", "U Chiang Mai", "2535552787",
  "3&ndash;7 Nov &middot; room held from the 3rd",
  "Deluxe with Bathtub, 1 King, two guests. Booked through Chase Travel (Trip 1027896876). The night of "
  "the 3rd is paid deliberately so the room is available on arrival at 07:15 on the 4th. "
  "Breakfast not included, about THB 399 each.", "Confirmed &middot; NON-REFUNDABLE"),
 ("Tour &mdash; Chiang Mai", "TripGuru Thailand &middot; via Tripadvisor", "1444673351",
  "5 Nov &middot; 08:30 &middot; 2 adults",
  "Doi Inthanon National Park, private full-day tour with an English-speaking guide. USD 250 paid in "
  "full. Includes hotel pick-up and drop-off, air-conditioned vehicle, water and entrance fees "
  "(park THB 300, Twin Pagoda THB 100); excludes lunch. TripGuru reference 7E51T410N0DP. "
  "Send them your WhatsApp number and hotel before 18:00 the previous day, and passport details for "
  "both travellers on their insurance form before the tour.",
  "Confirmed &middot; free cancellation to 24 h before"),
 ("Tour &mdash; Chiang Mai", "Elephant Nature Park", "55796",
  "6 Nov &middot; pick-up 08:00&ndash;08:45 &middot; 2 adults",
  "Elephant Highlands, single-day visit. THB 12,000 total: THB 3,600 deposit paid, "
  "<b>THB 8,400 balance due in cash, in Thai baht, at the start of the trip</b>. Hotel pick-up from "
  "U Chiang Mai; confirm the pick-up point at least 72 hours ahead or start from their office at "
  "1 Ratmakka Road. Vegan lunch, transport, admission, insurance and guide included. "
  "One small day pack per person.", "Confirmed &middot; PART-PAID, balance in cash"),
 ("Flight &mdash; Chiang Mai to Krabi", "Thai AirAsia", "UYTUHF",
  "7 Nov &middot; 07:55 &rarr; 09:55",
  "FD3072, Airbus A320, non-stop. Both passengers.", "Confirmed"),
 ("Hotel &mdash; Krabi", "Centara Ao Nang Beach Resort &amp; Spa", "2535573436",
  "7&ndash;10 Nov &middot; 3 nights",
  "Deluxe Room, 1 King Bed, Pool Access. Booked through Chase Travel (Trip 1027898679). Check-in 15:00, "
  "check-out 12:00. Ask for a room away from the drainage canal. Breakfast extra, THB 325&ndash;650 each.",
  "Confirmed &middot; NON-REFUNDABLE"),
 ("Boat &mdash; Krabi", "krabiteerapongtour &middot; via GetYourGuide", "GYGVN22MBRVZ",
  "8 Nov &middot; 8 hours &middot; private boat",
  "9 Islands private longtail. USD 299.43 paid in full; booked as a group of up to five, so the boat is "
  "yours. Pick-up and drop-off at the Centara Ao Nang lobby &mdash; <b>pick-up time to be confirmed by "
  "the operator</b>. No guide and no meals included. Date inferred from the cancellation deadline; "
  "confirm it when they call. Operator <code>+66 81 078 5454</code>.",
  "Confirmed &middot; free cancellation to 09:00 on 7 Nov"),
 ("Tour &mdash; Krabi", "TripGuru Thailand &middot; via GetYourGuide", "GYGN6BWWFQFY",
  "9 Nov &middot; 08:00 &middot; 2 adults",
  "Emerald Pool, Blue Lagoon, Hot Springs Waterfall and Tiger Cave Temple. Small-group tour, 9.5 hours, "
  "English-speaking guide. USD 115.82 paid in full. Hotel pick-up and drop-off at the Centara Ao Nang "
  "lobby, all entrance fees and drinking water included; lunch is not. Pick-up time confirmed by email "
  "the evening before &mdash; be in the lobby ten minutes early, the guide waits ten minutes. "
  "Temple dress code enforced. Operator <code>+1 254 454 4878</code>.",
  "Confirmed &middot; free cancellation to 08:00 on 8 Nov"),
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
      <li><b>Elephant Nature Park</b> <code>+66 53 272855</code> &mdash; 07:00&ndash;17:00 daily</li>
      <li><b>TripGuru</b> <code>+1 254 454 4878</code> &mdash; WhatsApp chat; Doi Inthanon on the 5th
        and Emerald Pool / Tiger Cave on the 9th</li>
      <li><b>Manohra Cruises</b> <code>+66 2 476 0022</code></li>
      <li><b>krabiteerapongtour</b> <code>+66 81 078 5454</code> &mdash; the 9 Islands longtail</li>
    </ul>
  </div>

  <div class="ibox">
    <h3>Travel insurance</h3>
    <p>Berkshire Hathaway Travel Protection, policy <code>201350715</code>, purchased 21 July 2026 and
    covering this trip. This is the replacement policy issued with the correct number of flight
    segments, so it is the one to quote. The full document is in the trip email thread.</p>
  </div>

  <div class="ibox">
    <h3>Weather and conditions</h3>
    <p>Early November is the front edge of the cool, dry season, but it is a front edge rather than a
    guarantee. The Andaman is still drying out &mdash; expect a wet afternoon or two around Krabi. The
    island day used to be the one to move freely; now that the longtail is booked, the decision has a
    deadline: <b>09:00 on 7 November</b>, while cancellation is still free. Khao Sok is at its lushest
    precisely because the rain has only just stopped. Sea state is the thing that cancels boat trips, so
    ask at the hotel desk the evening before rather than the morning of.</p>
  </div>

  <div class="ibox">
    <h3>Cash</h3>
    <p>Card works nearly everywhere, but three things on this trip are cash-only. The big one is in
    Chiang Mai: the <b>THB 8,400 balance for Elephant Nature Park</b>, payable in Thai baht on the
    morning of the 6th. Draw it on the 5th. The other two are at Khao Sok: the national park fee of
    <b>THB 340 per person</b> on arrival and <b>THB 200 each</b> for the Pakarang cave trail &mdash;
    draw those before you leave Krabi, as there is no ATM on the lake.</p>
  </div>

  <div class="ibox">
    <h3>Still to book</h3>
    <p>Every night, every flight and six activities are now confirmed: the Manohra dinner cruise on the
    1st, Ayutthaya on the 3rd, Doi Inthanon on the 5th, Elephant Nature Park on the 6th, the 9 Islands
    longtail on the 8th and the Emerald Pool / Tiger Cave tour on the 9th. <b>One thing is left to
    book</b>: the two cave trails at Khao Sok, arranged at the resort &mdash; they have fixed departure
    times and run only on certain days, so ask on arrival rather than the morning of. <b>One thing is
    left to confirm</b>, and it matters more: the Ayutthaya station drop-off on the 3rd.</p>
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
