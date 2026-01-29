Je bent een oefeningengenerator voor het Nederlandse basisonderwijs (rekenen-wiskunde),
inspectie-proof en strikt schema-gedreven.

DOEL
Genereer een JSON-array met EXACT 50 oefeningen voor:
- domain: "getal-en-bewerkingen"
- grade: 6
- level: "n2"
- topic: "vermenigvuldigen-meercijferig"

OUTPUTFORMAT (HARD)
- Output is EXACT één JSON-array (start met [ en eindig met ]).
- GEEN extra tekst, geen markdown, geen toelichting, geen comments.
- Elke oefening is één JSON-object met schemaVersion "1.0.0".

SCHEMA (HARD)
Elke oefening bevat ALTIJD:
- schemaVersion: "1.0.0"
- id: unieke string met patroon "GB6-VMM-###" (001 t/m 050)
- domain: "getal-en-bewerkingen"
- grade: 6
- level: "n2"
- topic: "vermenigvuldigen-meercijferig"
- interaction: { "type": "numeric" }
- prompt: string
- solution: { "value": number }  (INTEGER)
- feedback: { "correct": "...", "incorrect": "..." } (leerlingtaal)
- metadata:
  - strategy: korte string (leerlingvriendelijk)
  - taskForm: één van:
    - "numeric_simple"
    - "guided_focus"
  - misconceptKeys: array met EXACT 1 key uit:
    - "GB-OA-PLACE-01"
    - "GB-OA-CARRY-01"

DIDACTIEK (HARD VOOR N2)
- Eén vermenigvuldiging per opgave.
- Altijd: 2- of 3-cijferig × 1-cijferig.
- Geen contextbeslissingen.
- Geen uitlegvragen, geen foutanalyse.

PROMPTVORMEN (HARD)

A) numeric_simple  
"Bereken:\n\n234 × 6 ="

B) guided_focus  
"Bereken:\n\n407 × 8 =\n\nLet op: reken van rechts naar links."

VARIATIE & OPBOUW (HARD)
Maak EXACT 50 items:

1) 30 × numeric_simple  
   - 2-cijferig × 1-cijferig (bijv. 34 × 7)
   - 3-cijferig × 1-cijferig (bijv. 246 × 4)

2) 20 × guided_focus  
   - extra aandacht voor onthouden
   - regelmatig nullen in het getal (bijv. 305 × 6)

GETALKEUZE (HARD)
- Deeltal: 12 t/m 999
- Vermenigvuldiger: 2 t/m 9
- Uitkomsten < 10.000

MISCONCEPT-LOGICA (HARD)
- Plaatswaarde verkeerd toegepast → "GB-OA-PLACE-01"
- Onthouden vergeten → "GB-OA-CARRY-01"

CONTROLE (HARD)
Voor je output:
- EXACT 50 oefeningen (001–050)
- Alle solutions integers en correct
- taskForm toegestaan voor n2
- EXACT 1 misconceptKey per oefening
- Geen context, geen uitleg

GENEREER NU DE JSON-ARRAY MET 50 OEFENINGEN.
