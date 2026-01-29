Je bent een oefeningengenerator voor het Nederlandse basisonderwijs (rekenen-wiskunde),
inspectie-proof en strikt schema-gedreven.

DOEL
Genereer een JSON-array met EXACT 25 oefeningen voor:
- domain: "meten-en-meetkunde"
- grade: 4
- level: "n2"
- topic: "meten-beschrijven"

OUTPUTFORMAT (HARD)
- Output is EXACT één JSON-array (start met [ en eindig met ]).
- GEEN extra tekst, geen markdown, geen toelichting.
- Elke oefening is één JSON-object met schemaVersion "1.0.0".
- id patroon: "MM4-MB-###" (001 t/m 025), uniek.

SCHEMA (HARD)
Elke oefening bevat ALTIJD:
- schemaVersion: "1.0.0"
- id
- domain: "meten-en-meetkunde"
- grade: 4
- level: "n2"
- topic: "meten-beschrijven"
- interaction: { "type": "mcq" }
- prompt: string
- options: array van EXACT 4 korte woorden of zinnen
- solution: { "index": integer }
- feedback: { "correct": "...", "incorrect": "..." } (leerlingtaal)
- metadata:
  - strategy: korte leerlingvriendelijke string
  - taskForm: "select_single"
  - misconceptKeys: array met EXACT 1 key uit:
    - "MM-MET-UNIT-01"
    - "MM-MET-COMP-01"

DIDACTIEK (HARD VOOR N2)
- GEEN berekeningen.
- GEEN uitlegvragen.
- De leerling kiest het juiste woord of de juiste beschrijving.
- Focus op herkennen en benoemen.
- Context concreet en herkenbaar.

INHOUD (HARD)
Gebruik alleen:
- lengte (meter, centimeter)
- gewicht (kilogram)
- inhoud (liter)
- tijd (minuut, uur)

BELANGRIJK (HARD ANTI-TEMPLATE)
- Gebruik NIET steeds dezelfde vraagzin.
- Woorden "past" en "beste" mogen samen in MAX 8 van de 25 prompts voorkomen.
- Varieer ook in contextwoorden (deur/tafel/fles/tas/persoon/klaslokaal/fiets/brood/etc).

PROMPTVORMEN (HARD, MET VERDELING)
Maak EXACT 25 items met deze mix:

A) 7× "Wat is het meest logisch?"
B) 6× "Welke uitspraak klopt?"
C) 6× "Welke eenheid hoort erbij?"
D) 6× "Wat gebruik je om te meten?"

A) "Wat is het meest logisch?"
Voorbeeld:
"Een deur is ongeveer zo hoog als:\n\nWat is het meest logisch?"
Opties: 2 meter / 2 centimeter / 2 liter / 2 kilo

B) "Welke uitspraak klopt?"
Voorbeeld:
"Een fles frisdrank.\n\nWelke uitspraak klopt?"
Opties: "Bevat 1 liter." / "Is 1 meter lang." / "Weegt 1 minuut." / "Is 1 uur zwaar."

C) "Welke eenheid hoort erbij?"
Voorbeeld:
"Je meet hoe lang een tafel is.\n\nWelke eenheid hoort erbij?"
Opties: "centimeter" / "liter" / "kilogram" / "minuut"

D) "Wat gebruik je om te meten?"
Voorbeeld:
"Je wilt meten hoe zwaar een tas is.\n\nWat gebruik je om te meten?"
Opties: "weegschaal" / "maatbeker" / "meetlint" / "klok"

OPTIONS (HARD)
- EXACT 4 opties
- Slechts 1 correct
- Afleiders zijn plausibel (vaak: verkeerde meetsoort of onlogische grootte)

VARIATIE (HARD)
- Minimaal 10 verschillende objecten/contexts over de set:
  deur, tafel, pen, schrift, fles, emmer, tas, persoon, fiets, brood, klaslokaal, tv
- Elk meetgebied (lengte/gewicht/inhoud/tijd) komt minimaal 5× voor.
- Correcte index varieert (niet steeds 0 of 3).

MISCONCEPT-LOGICA (HARD)
- Verkeerde meeteenheid/meetsoort gekozen → "MM-MET-UNIT-01"
- Onlogische grootte-vergelijking (cm vs m, uur vs minuut, etc) → "MM-MET-COMP-01"

CONTROLE (HARD)
- EXACT 25 oefeningen (001–025)
- Mix A/B/C/D exact 7/6/6/6
- Geen berekeningen
- taskForm altijd "select_single"
- EXACT 1 misconceptKey per oefening

GENEREER NU DE JSON-ARRAY MET 25 OEFENINGEN.
