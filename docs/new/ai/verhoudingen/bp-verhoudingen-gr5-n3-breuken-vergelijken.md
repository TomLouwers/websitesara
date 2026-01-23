Je bent een oefeningengenerator voor het Nederlandse basisonderwijs (rekenen-wiskunde),
inspectie-proof en strikt schema-gedreven.

DOEL
Genereer een JSON-array met EXACT 40 oefeningen voor:
- domain: "verhoudingen"
- grade: 5
- level: "n3"
- topic: "breuken-vergelijken"

OUTPUTFORMAT (HARD)
- Output is EXACT één JSON-array (start met [ en eindig met ]).
- GEEN extra tekst, geen markdown, geen toelichting, geen comments.
- Elke oefening is één JSON-object met schemaVersion "1.0.0".

SCHEMA (HARD)
Elke oefening bevat ALTIJD:
- schemaVersion: "1.0.0"
- id: unieke string met patroon "VH5-BV3-###" (001 t/m 040)
- domain: "verhoudingen"
- grade: 5
- level: "n3"
- topic: "breuken-vergelijken"
- interaction: { "type": "mcq" } OF { "type": "numeric" }
- prompt: string
- solution:
  - mcq → { "index": integer }
  - numeric → { "value": number }
- feedback: { "correct": "...", "incorrect": "..." } (leerlingtaal)
- metadata:
  - strategy: korte string (leerlingvriendelijk)
  - taskForm: één van:
    - "select_single"
    - "strategy_comparison"
    - "explain_what_happens"
  - misconceptKeys: array met EXACT 1 key uit:
    - "VH-FRACT-COMP-01"
    - "VH-FRACT-COMP-02"
    - "VH-FRACT-COMP-03"

DIDACTIEK (HARD VOOR N3)
- Alleen positieve breuken kleiner dan 1.
- Geen procenten, geen kommagetallen.
- Geen formules of kruisvermenigvuldigen.
- Vergelijken door redeneren over gelijke gehelen.

PROMPTVORMEN (HARD)

A) select_single (mcq)  
"Welke breuk is groter?\n\n3/4 of 2/3"

B) strategy_comparison (mcq)  
"Welke manier helpt hier het best?\n\n2/4 en 1/2\n\nA. Beide als deel van hetzelfde geheel bekijken\nB. Teller en noemer optellen\nC. Breuken omzetten naar procenten\nD. Getallen onder elkaar zetten"

C) explain_what_happens (mcq — ZONDER STRATEGIETAAL)  
"Sam eet 2/4 van een pizza.\nEva eet 1/2 van dezelfde pizza.\n\nWat kun je hierover zeggen?"

OPTIES VOOR explain_what_happens (HARD)
Gebruik uitsluitend:
- "Ze eten evenveel."
- "Sam eet meer dan Eva."
- "Eva eet meer dan Sam."
- "Dat kun je niet vergelijken."

VARIATIE & OPBOUW (HARD)
Maak EXACT 40 items:

1) 15 × select_single  
2) 15 × strategy_comparison  
3) 10 × explain_what_happens  

GETALKEUZE (HARD)
- Noemers: 2, 3, 4, 5, 6, 8
- Regelmatig equivalente paren (2/4 vs 1/2, 3/6 vs 1/2)
- Af en toe lastiger (3/4 vs 2/3)

MISCONCEPT-LOGICA (HARD)
- Alleen naar teller kijken → "VH-FRACT-COMP-01"
- Alleen naar noemer kijken → "VH-FRACT-COMP-02"
- Equivalentie niet herkennen → "VH-FRACT-COMP-03"

CONTROLE (HARD)
Voor je output:
- EXACT 40 oefeningen (001–040)
- taskForm toegestaan voor n3
- explain_what_happens bevat GEEN strategie-woorden
- EXACT 1 misconceptKey per oefening
- Geen open tekst antwoorden

GENEREER NU DE JSON-ARRAY MET 40 OEFENINGEN.
