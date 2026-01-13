# VERHOUDINGEN - Praktisch Gebruiksvoorbeeld

## Overzicht
Dit document toont concrete voorbeelden van hoe de Verhoudingen prompt v2.0 gebruikt wordt en wat de verwachte output is.

---

## VOORBEELD 1: Groep 4 Midden - Basis Breuken

### INPUT:
```
GROEP: 4
NIVEAU: M
AANTAL: 3
```

### VERWACHT GEDRAG:
De generator moet automatisch toepassen:
- ✅ Alleen stambreuken 1/2 en 1/4
- ✅ Visualisatie VERPLICHT
- ✅ Maximaal 1 stap
- ✅ Context: speelgoed, snoep, taart
- ✅ Getallen tot 20
- ✅ Taalcomplexiteit: 1-3 zinnen

### VERWACHTE OUTPUT:

```json
{
  "items": [
    {
      "id": "V_G4_M_001",
      "domein": "Verhoudingen",
      "subdomein": "Breuken",
      "groep": 4,
      "niveau": "M",
      "slo_code": "4V1",
      "kerndoel": "K28",
      "referentieniveau": "nvt",

      "vraag": {
        "context": "Een appeltaart is in 4 gelijke stukken gesneden.",
        "hoofdvraag": "Hoeveel is 1 stuk van de taart?",
        "visualisatie": "cirkel_4_delen_1_gekleurd.svg",
        "visualisatie_beschrijving": "Cirkel verdeeld in 4 gelijke stukken, 1 stuk is rood gekleurd"
      },

      "antwoorden": [
        {
          "id": "A",
          "tekst": "1/4",
          "waarde": "1/4",
          "correct": true,
          "fouttype": null
        },
        {
          "id": "B",
          "tekst": "1/2",
          "waarde": "1/2",
          "correct": false,
          "fouttype": "verkeerde_breuk"
        },
        {
          "id": "C",
          "tekst": "4",
          "waarde": "4",
          "correct": false,
          "fouttype": "geheel_ipv_deel"
        },
        {
          "id": "D",
          "tekst": "4/1",
          "waarde": "4/1",
          "correct": false,
          "fouttype": "omgedraaid"
        }
      ],

      "metadata": {
        "moeilijkheidsgraad": 0.25,
        "adaptief_niveau": 1,
        "geschatte_tijd_sec": 30,
        "stappen_aantal": 1,
        "stappen_beschrijving": ["1 stuk van 4 delen herkennen als 1/4"],
        "cognitieve_complexiteit": "herkennen",
        "taalcomplexiteit_avi": "E3",
        "visuele_ondersteuning": "hoog"
      },

      "didactiek": {
        "conceptuitleg": "Als je iets in 4 gelijke stukken verdeelt, is 1 stuk een kwart. Je schrijft dit als 1/4.",

        "berekening_stappen": [
          "De taart is in 4 gelijke stukken verdeeld",
          "Je wilt weten wat 1 stuk is",
          "1 stuk van 4 is 1/4 (een kwart)"
        ],

        "lova": {
          "lezen": "Taart in 4 gelijke stukken. Vraag: hoeveel is 1 stuk?",
          "ordenen": "Geheel: 4 stukken. Deel: 1 stuk. Gevraagd: breuk.",
          "vormen": "1 stuk van 4 stukken = 1/4",
          "antwoorden": "1/4 (een kwart)"
        },

        "feedback": {
          "correct": "Heel goed! 1 stuk van 4 is inderdaad 1/4. Dit heet een kwart.",
          "fout_verkeerde_breuk": "Let op: de taart is in 4 stukken verdeeld, niet in 2. Dus het is 1/4 in plaats van 1/2.",
          "fout_geheel_ipv_deel": "Je hebt het aantal stukken geteld (4). De vraag is: wat is 1 stuk? Dat is 1/4.",
          "fout_omgedraaid": "Bij een breuk komt eerst hoeveel je hebt (1), dan in hoeveel stukken het verdeeld is (4). Dus 1/4.",
          "algemeen": "Tip: Tel het aantal stukken. Je hebt 1 stuk. Hoeveel stukken zijn er in totaal?"
        },

        "hulp_strategie": "Kijk naar het plaatje. Tel hoeveel stukken er zijn (4). Het gekleurde stuk is er maar één. Dus 1 van de 4 = 1/4.",
        "veelvoorkomende_fout": "Kinderen verwarren vaak teller en noemer, of geven het totaal aantal in plaats van de breuk."
      },

      "tags": ["breuken", "stambreuk", "1/4", "visueel", "herkennen", "introductie"],
      "bronverwijzing": "SLO K28 - Verhoudingen G4 Midden",
      "cito_itemtype": "meerkeuzevraag_visueel",
      "datum_aangemaakt": "2026-01-13",
      "versie": "2.0"
    },

    {
      "id": "V_G4_M_002",
      "domein": "Verhoudingen",
      "subdomein": "Breuken",
      "groep": 4,
      "niveau": "M",
      "vraag": {
        "context": "Lisa heeft 6 snoepjes. Ze geeft de helft aan haar broer.",
        "hoofdvraag": "Hoeveel snoepjes krijgt haar broer?",
        "visualisatie": "6_snoepjes_helft_gekleurd.svg"
      },
      "antwoorden": [
        {"id": "A", "tekst": "3", "correct": true, "fouttype": null},
        {"id": "B", "tekst": "6", "correct": false, "fouttype": "geheel"},
        {"id": "C", "tekst": "2", "correct": false, "fouttype": "verkeerde_deling"},
        {"id": "D", "tekst": "4", "correct": false, "fouttype": "verkeerde_deling"}
      ],
      "metadata": {
        "moeilijkheidsgraad": 0.3,
        "stappen_aantal": 1,
        "stappen_beschrijving": ["De helft van 6 berekenen: 6 : 2 = 3"]
      },
      "didactiek": {
        "conceptuitleg": "De helft betekent in 2 gelijke delen verdelen. De helft van 6 is 3.",
        "berekening_stappen": ["6 snoepjes delen door 2 = 3 snoepjes"]
      }
    },

    {
      "id": "V_G4_M_003",
      "domein": "Verhoudingen",
      "subdomein": "Breuken",
      "groep": 4,
      "niveau": "M",
      "vraag": {
        "context": "Een pizza is in 4 stukken gesneden. Tim eet 2 stukken.",
        "hoofdvraag": "Hoeveel pizza heeft Tim opgegeten?",
        "visualisatie": "pizza_4_delen_2_gekleurd.svg"
      },
      "antwoorden": [
        {"id": "A", "tekst": "2/4", "correct": true, "fouttype": null},
        {"id": "B", "tekst": "1/2", "correct": false, "fouttype": "vereenvoudigd_niet_gevraagd"},
        {"id": "C", "tekst": "4/2", "correct": false, "fouttype": "omgedraaid"},
        {"id": "D", "tekst": "2", "correct": false, "fouttype": "geen_breuk"}
      ],
      "metadata": {
        "moeilijkheidsgraad": 0.35,
        "stappen_aantal": 1
      }
    }
  ],

  "metadata_set": {
    "domein": "Verhoudingen",
    "aantal_items": 3,
    "groep": 4,
    "niveau": "M",
    "gegenereerd_op": "2026-01-13T11:00:00Z",
    "generator_versie": "v2.0",
    "moeilijkheidsgraad_gemiddeld": 0.30,
    "verdeling_subdomeinen": {
      "Breuken": 3
    }
  }
}
```

---

## VOORBEELD 2: Groep 6 Eind - Conversies

### INPUT:
```
GROEP: 6
NIVEAU: E
AANTAL: 2
FOCUS: Conversies
```

### VERWACHT GEDRAG:
- ✅ Breuk ↔ Decimaal ↔ Procent conversies
- ✅ Maximaal 3-4 stappen
- ✅ Vergelijken verschillende notaties
- ✅ Context: praktische situaties

### VERWACHTE OUTPUT:

```json
{
  "items": [
    {
      "id": "V_G6_E_001",
      "domein": "Verhoudingen",
      "subdomein": "Conversies",
      "groep": 6,
      "niveau": "E",
      "slo_code": "6V6",
      "kerndoel": "K28",
      "referentieniveau": "nvt",

      "vraag": {
        "context": "In de klas heeft 3/4 van de leerlingen hun huiswerk gemaakt. De juf wil dit als percentage noteren.",
        "hoofdvraag": "Hoeveel procent van de leerlingen heeft het huiswerk gemaakt?",
        "visualisatie": null
      },

      "antwoorden": [
        {
          "id": "A",
          "tekst": "75%",
          "waarde": "75",
          "correct": true,
          "fouttype": null
        },
        {
          "id": "B",
          "tekst": "34%",
          "waarde": "34",
          "correct": false,
          "fouttype": "decimaal_verwarring"
        },
        {
          "id": "C",
          "tekst": "0,75%",
          "waarde": "0.75",
          "correct": false,
          "fouttype": "decimaal_ipv_percentage"
        },
        {
          "id": "D",
          "tekst": "25%",
          "waarde": "25",
          "correct": false,
          "fouttype": "complement_berekend"
        }
      ],

      "metadata": {
        "moeilijkheidsgraad": 0.52,
        "adaptief_niveau": 3,
        "geschatte_tijd_sec": 60,
        "stappen_aantal": 2,
        "stappen_beschrijving": [
          "3/4 omzetten naar decimaal: 3 : 4 = 0,75",
          "Decimaal naar percentage: 0,75 × 100 = 75%"
        ],
        "cognitieve_complexiteit": "toepassen",
        "taalcomplexiteit_avi": "M5"
      },

      "didactiek": {
        "conceptuitleg": "Om een breuk om te zetten naar een percentage, kun je eerst naar een decimaal getal gaan (teller : noemer) en dan × 100 doen. Of direct: 3/4 = 75/100 = 75%.",

        "berekening_stappen": [
          "Stap 1: 3/4 naar decimaal: 3 : 4 = 0,75",
          "Stap 2: Decimaal naar percentage: 0,75 × 100 = 75%",
          "Alternatief: 3/4 = 75/100 = 75%"
        ],

        "lova": {
          "lezen": "3/4 van leerlingen heeft huiswerk. Vraag: hoeveel procent?",
          "ordenen": "Gegeven: breuk 3/4. Gevraagd: percentage. Conversie nodig: breuk → percentage.",
          "vormen": "Methode 1: 3/4 = 0,75 = 75%. Methode 2: 3/4 = 75/100 = 75%.",
          "antwoorden": "75%"
        },

        "feedback": {
          "correct": "Perfect! 3/4 is inderdaad 75%. Je hebt de conversie goed uitgevoerd.",
          "fout_decimaal_verwarring": "Let op: 3/4 is 0,75 als decimaal. Dit is niet hetzelfde als 34%.",
          "fout_decimaal_ipv_percentage": "Je hebt 3/4 correct naar decimaal omgezet (0,75), maar de vraag is naar een percentage. Vermenigvuldig met 100: 0,75 × 100 = 75%.",
          "fout_complement_berekend": "Je hebt 25% berekend, dat is het deel dat het huiswerk NIET heeft gemaakt (1/4). De vraag gaat over het deel dat het WEL heeft gemaakt: 3/4 = 75%.",
          "algemeen": "Tip: Breuk → Decimaal (teller : noemer) → Percentage (× 100)"
        },

        "hulp_strategie": "Maak een conversietabel:\n3/4 = ? (als decimaal)\n3 : 4 = 0,75\n0,75 × 100 = 75%\n\nOf: 3/4 = ?/100. Als je 4 × 25 = 100, dan ook 3 × 25 = 75. Dus 3/4 = 75/100 = 75%",

        "veelvoorkomende_fout": "Leerlingen vergeten vaak de × 100 stap bij conversie naar percentage, of verwarren 0,75 met 75."
      },

      "tags": ["conversie", "breuk_naar_percentage", "3/4", "75%", "meerstaps"],
      "bronverwijzing": "SLO K28 - Verhoudingen G6 Eind",
      "cito_itemtype": "meerkeuzevraag_context",
      "datum_aangemaakt": "2026-01-13",
      "versie": "2.0"
    },

    {
      "id": "V_G6_E_002",
      "domein": "Verhoudingen",
      "subdomein": "Conversies",
      "groep": 6,
      "niveau": "E",
      "vraag": {
        "context": "Een winkel geeft korting. Op het bordje staat: '0,6 korting op alle jassen'. Emma's moeder vraagt: 'Hoeveel procent korting is dat?'",
        "hoofdvraag": "Welk antwoord klopt?",
        "visualisatie": null
      },
      "antwoorden": [
        {"id": "A", "tekst": "60%", "correct": true, "fouttype": null},
        {"id": "B", "tekst": "6%", "correct": false, "fouttype": "factor_10_vergeten"},
        {"id": "C", "tekst": "0,6%", "correct": false, "fouttype": "niet_omgezet"},
        {"id": "D", "tekst": "40%", "correct": false, "fouttype": "complement"}
      ],
      "metadata": {
        "moeilijkheidsgraad": 0.48,
        "stappen_aantal": 1,
        "stappen_beschrijving": ["Decimaal naar percentage: 0,6 × 100 = 60%"]
      },
      "didactiek": {
        "conceptuitleg": "Een decimaal getal naar percentage: vermenigvuldig met 100. Dus 0,6 × 100 = 60%."
      }
    }
  ],

  "metadata_set": {
    "domein": "Verhoudingen",
    "aantal_items": 2,
    "groep": 6,
    "niveau": "E",
    "focus": "Conversies",
    "gegenereerd_op": "2026-01-13T11:15:00Z",
    "moeilijkheidsgraad_gemiddeld": 0.50
  }
}
```

---

## VOORBEELD 3: Groep 8 Eind - Complexe Woordproblemen (1S niveau)

### INPUT:
```
GROEP: 8
NIVEAU: E
AANTAL: 1
```

### VERWACHT GEDRAG:
- ✅ Meerstaps (max 5)
- ✅ Combinatie verhoudingen + percentages + schaal
- ✅ CITO eindtoets niveau 1S
- ✅ Kritisch redeneren

### VERWACHTE OUTPUT:

```json
{
  "items": [
    {
      "id": "V_G8_E_001",
      "domein": "Verhoudingen",
      "subdomein": "Integraal",
      "groep": 8,
      "niveau": "E",
      "slo_code": "8V6",
      "kerndoel": "K28, K29, K30",
      "referentieniveau": "1S",

      "vraag": {
        "context": "Een school organiseert een schoolreisje naar een pretpark. Op de plattegrond met schaal 1:2000 is de afstand van de ingang naar de achtbaan 12 cm. Tickets kosten normaal €35 per leerling, maar de school krijgt 15% groepskorting. Er gaan 78 leerlingen mee. De reisleider wil weten: (1) wat is de werkelijke afstand naar de achtbaan, en (2) hoeveel betaalt de school in totaal voor alle tickets na korting?",
        "hoofdvraag": "Wat is de werkelijke afstand in meters EN wat zijn de totale ticketkosten?",
        "visualisatie": null
      },

      "antwoorden": [
        {
          "id": "A",
          "tekst": "240 meter en €2.457",
          "waarde": {"afstand": 240, "kosten": 2457},
          "correct": true,
          "fouttype": null
        },
        {
          "id": "B",
          "tekst": "24 meter en €2.457",
          "waarde": {"afstand": 24, "kosten": 2457},
          "correct": false,
          "fouttype": "schaal_factor_fout"
        },
        {
          "id": "C",
          "tekst": "240 meter en €2.730",
          "waarde": {"afstand": 240, "kosten": 2730},
          "correct": false,
          "fouttype": "korting_vergeten"
        },
        {
          "id": "D",
          "tekst": "2.400 meter en €2.457",
          "waarde": {"afstand": 2400, "kosten": 2457},
          "correct": false,
          "fouttype": "schaal_factor_verkeerd_en_eenheid"
        }
      ],

      "metadata": {
        "moeilijkheidsgraad": 0.78,
        "adaptief_niveau": 5,
        "geschatte_tijd_sec": 180,
        "stappen_aantal": 5,
        "stappen_beschrijving": [
          "Schaalberekening: 12 cm × 2000 = 24.000 cm",
          "Eenheid conversie: 24.000 cm = 240 m",
          "Percentage berekenen: 15% van €35 = €5,25",
          "Prijs na korting: €35 - €5,25 = €29,75",
          "Totaalprijs: €29,75 × 78 = €2.457"
        ],
        "cognitieve_complexiteit": "analyseren_en_evalueren",
        "taalcomplexiteit_avi": "PLUS",
        "visuele_ondersteuning": "geen",
        "ruis_aantal": 1
      },

      "didactiek": {
        "conceptuitleg": "Dit is een complexe opgave die schaalberekening, percentages en vermenigvuldiging combineert. Je moet systematisch stap voor stap werken en tussen verschillende eenheden converteren.",

        "berekening_stappen": [
          "DEEL 1 - Afstand berekenen:",
          "  Schaal 1:2000 betekent: 1 cm op kaart = 2000 cm in werkelijkheid",
          "  12 cm × 2000 = 24.000 cm",
          "  Omzetten: 24.000 cm ÷ 100 = 240 meter",
          "",
          "DEEL 2 - Ticketkosten:",
          "  Oorspronkelijke prijs: €35 per leerling",
          "  Korting: 15% van €35 = 0,15 × €35 = €5,25",
          "  Prijs na korting: €35 - €5,25 = €29,75 per leerling",
          "  Totaal: €29,75 × 78 leerlingen = €2.321,50",
          "  Afgerond: €2.322 (of exact: €2.321,50)",
          "",
          "Let op: Som vraagt beide antwoorden!"
        ],

        "lova": {
          "lezen": "Schoolreisje, plattegrond schaal 1:2000, 12 cm op kaart, tickets €35 met 15% korting, 78 leerlingen. Vraag: werkelijke afstand EN totale kosten.",

          "ordenen": "Twee deelvragen: (1) Schaalberekening → afstand. (2) Percentagekorting → prijs per leerling → totaalprijs. Gegeven: schaal, afstand kaart, prijs, korting%, aantal leerlingen. Gevraagd: werkelijke afstand in meters + totale ticketkosten.",

          "vormen": "Deel 1: 12 × 2000 = 24.000 cm = 240 m. Deel 2: 15% van 35 = 5,25. Nieuwe prijs: 35 - 5,25 = 29,75. Totaal: 29,75 × 78 = 2.321,50 ≈ 2.322 euro.",

          "antwoorden": "240 meter en €2.322 (exact: €2.321,50, afhankelijk van afrondingsinstructie)"
        },

        "feedback": {
          "correct": "Uitstekend! Je hebt beide berekeningen correct uitgevoerd. Je past schaalberekening én percentages goed toe in een complexe context. Dit is 1S-niveau!",

          "fout_schaal_factor_fout": "De ticketberekening klopt, maar let op bij de schaalberekening: 1:2000 betekent dat je × 2000 moet doen. 12 × 2000 = 24.000 cm = 240 meter (niet 24 meter).",

          "fout_korting_vergeten": "De afstand klopt! Maar bij de ticketprijs ben je vergeten de 15% korting toe te passen. €35 × 78 = €2.730 is de prijs ZONDER korting. Met 15% korting betaal je minder.",

          "fout_schaal_factor_verkeerd_en_eenheid": "De ticketberekening is goed! Bij de schaal: 12 × 2000 = 24.000 cm. Je moet dit nog omrekenen naar meters: 24.000 cm = 240 m (niet 2.400 m!).",

          "algemeen": "Tip: Maak twee aparte berekeningen: eerst de afstand (let op eenheden!), dan de ticketprijs (vergeet korting niet!). Controleer of je beide antwoorden hebt."
        },

        "hulp_strategie": "Aanpak voor complexe opgaven:\n1. Lees zorgvuldig en onderstreep de vragen\n2. Maak een lijstje: wat is gegeven, wat is gevraagd\n3. Los elke deelvraag apart op\n4. Check eenheden (cm→m, korting toepassen)\n5. Controleer of je alle gevraagde antwoorden hebt gegeven",

        "veelvoorkomende_fout": "Leerlingen vergeten vaak: (1) eenheid conversie (cm naar m), (2) korting toepassen, (3) één van de twee deelvragen beantwoorden. Ook: schaalfactor verkeerd toepassen (delen i.p.v. vermenigvuldigen)."
      },

      "tags": [
        "integraal", "meerstaps", "schaalberekening", "percentages",
        "korting", "verhoudingstabel", "eenheid_conversie",
        "1S_niveau", "cito_eindtoets", "complex_woordprobleem"
      ],

      "bronverwijzing": "SLO K28/K29/K30 - Verhoudingen G8 Eind - Referentieniveau 1S",
      "cito_itemtype": "meerkeuzevraag_complex_context",
      "datum_aangemaakt": "2026-01-13",
      "versie": "2.0"
    }
  ],

  "metadata_set": {
    "domein": "Verhoudingen",
    "aantal_items": 1,
    "groep": 8,
    "niveau": "E",
    "referentieniveau": "1S",
    "gegenereerd_op": "2026-01-13T11:30:00Z",
    "moeilijkheidsgraad_gemiddeld": 0.78
  }
}
```

**LET OP bij dit voorbeeld:**
- ✅ 5 stappen (maximaal voor G8-E)
- ✅ Combinatie van subdomeinen (Schaal + Procenten + Verhoudingen)
- ✅ Ruis aanwezig (informatie over pretpark/achtbaan niet direct nodig)
- ✅ Eenheid conversie (cm → m)
- ✅ CITO 1S complexiteit
- ✅ Meervoudige vraag (afstand ÉN kosten)

---

## VALIDATIE CHECKLIST

Voor elk gegenereerd item, check:

### ✅ Structuur
- [ ] Alle verplichte velden aanwezig
- [ ] JSON valide en parseerbaar
- [ ] ID uniek en volgens format: `V_G{groep}_{niveau}_{volgnummer}`

### ✅ Niveauregels
- [ ] Groep en niveau correct (4-8, M/E)
- [ ] Subdomein toegestaan voor dit niveau
- [ ] Stappenaantal binnen maximum
- [ ] Getallen binnen toegestane ruimte
- [ ] Bewerkingen toegestaan voor niveau

### ✅ Taal
- [ ] Zinsaantal binnen maximum
- [ ] Geen te lange woorden voor groep
- [ ] Eenduidige hoofdvraag
- [ ] Context passend bij leeftijd

### ✅ Afleiders
- [ ] Exact 4 antwoordopties
- [ ] Exact 1 correct antwoord
- [ ] 3 strategische afleiders
- [ ] Verschillende fouttypes
- [ ] Plausibele waarden

### ✅ Didactiek
- [ ] LOVA volledig ingevuld
- [ ] Conceptuitleg aanwezig
- [ ] Stappen beschreven
- [ ] Feedback per fouttype
- [ ] Hulpstrategie aanwezig

---

## GEBRUIK VALIDATOR

```bash
python verhoudingen-validator.py
```

Of in code:
```python
from verhoudingen_validator import VerhoudingenValidator
import json

# Laad gegenereerde items
with open('gegenereerde_items.json') as f:
    data = json.load(f)

# Valideer
validator = VerhoudingenValidator()
resultaat = validator.valideer_set(data['items'])

print(f"Valide: {resultaat['percentage_valide']:.1f}%")
print(f"Gemiddelde score: {resultaat['gemiddelde_score']:.2f}")
```

---

## BESTE PRACTICES

### DO's ✅
1. **Volg niveauregels STRICT** - Geen uitzonderingen
2. **Gebruik realistische contexten** - Herkenbaar voor Nederlandse kinderen
3. **Maak plausibele afleiders** - Gebaseerd op empirische foutpatronen
4. **Geef volledige feedback** - Per fouttype specifieke uitleg
5. **Check eenheden** - Altijd conversies expliciet maken
6. **Test met validator** - Voor elke batch items

### DON'TS ❌
1. **Geen willekeurige afleiders** - Altijd gebaseerd op foutpatronen
2. **Geen te complexe taal** - Houd rekening met AVI-niveau
3. **Geen stappen overslaan** - In uitleg alles expliciet
4. **Geen onduidelijke vragen** - "dit", "dat" vermijden
5. **Geen inconsistente notatie** - Kies 1/2 of ½, niet mixen
6. **Geen visualisatie vergeten** - Voor jonge groepen verplicht bij breuken

---

## VOLGENDE STAPPEN

1. **Test de prompt** met een LLM (Claude, GPT-4, etc.)
2. **Valideer output** met het validator script
3. **Verzamel feedback** van leerkrachten
4. **Itereer op afleiders** als blijkt dat bepaalde fouttypes niet herkenbaar zijn
5. **Schaal op** naar volledige itembank

---

**EINDE GEBRUIKSVOORBEELD**
