# Pedagogische Review: Groep 8 Prompt Templates
## Educatieve Expert Analyse

**Datum:** 31 december 2025
**Beoordelaar:** Senior Onderwijsexpert Basisonderwijs
**Scope:** Alle Groep 8 leerdoelen getoetst tegen SLO Kerndoelen en CITO eindtoetsniveau

---

## ❌ KRITIEKE BEVINDINGEN: Inhoud Te Moeilijk voor Groep 8

### 1. **PYTHAGORAS** - NIET GESCHIKT VOOR BASISONDERWIJS

**Locatie:**
- `rekenen-meten-meetkunde.csv` regel 37: **7MM2** - "Kennismaken met stelling van Pythagoras"
- `rekenen-meten-meetkunde.csv` regel 43: **8MM2** - "Stelling van Pythagoras toepassen"

**Probleem:**
- De stelling van Pythagoras (a² + b² = c²) wordt **NIET** onderwezen in het Nederlandse basisonderwijs
- Dit is stof uit het **voortgezet onderwijs** (typisch VMBO/HAVO/VWO klas 2-3)
- SLO Kerndoel K33 (Meetkunde) omvat dit **NIET**

**Kerndoel K33 (Meetkunde) voor groep 8:**
- Vlakke figuren: eigenschappen, omtrek, oppervlakte (vierkant, rechthoek, driehoek, cirkel)
- Ruimtelijke figuren: volume van kubus, balk, cilinder
- Symmetrie, coördinaten, transformaties
- **GEEN** geavanceerde stellingen zoals Pythagoras

**Aanbeveling:** **VERWIJDEREN** uit Groep 7 en Groep 8

---

### 2. **VIERKANTSWORTELS** - NIET GESCHIKT VOOR BASISONDERWIJS

**Locatie:**
- `rekenen-getallen.csv` regel 42: **8G2** - "Vierkantswortels van eenvoudige getallen"

**Probleem:**
- Worteltrekken (√64, √144) wordt **NIET** onderwezen in groep 8
- Dit is stof uit het **voortgezet onderwijs**
- SLO Kerndoel K29 (Hoofdrekenen) omvat alleen de vier basisbewerkingen (+, -, ×, :)

**Kerndoel K29 (Hoofdrekenen) voor groep 8:**
- Optellen, aftrekken, vermenigvuldigen, delen
- Strategieën voor hoofdrekenen
- **GEEN** worteltrekken of machtsverheffen

**Aanbeveling:** **VERWIJDEREN** uit Groep 8

---

### 3. **WETENSCHAPPELIJKE NOTATIE** - TE GEAVANCEERD

**Locatie:**
- `rekenen-getallen.csv` regel 41: **8G1** - "Kennismaken met wetenschappelijke notatie (machten van 10)"

**Probleem:**
- Wetenschappelijke notatie (4,5 × 10⁴) is **niet passend** voor groep 8
- Machtsverheffen wordt beperkt behandeld (hoogstens in context van vierkante getallen)
- Dit is typisch **VO-stof** (natuurkunde, wiskunde onderbouw)

**Kerndoel K28 (Getalsysteem) voor groep 8:**
- Gehele getallen, decimalen, breuken
- Negatieve getallen (basis)
- Getalsysteem begrijpen (tientallen, honderdtallen, duizendtallen)
- **GEEN** wetenschappelijke notatie met machten

**Aanbeveling:** **VERVANGEN** door:
- Grote getallen lezen en schrijven (tot miljoenen)
- Afronden op tientallen, honderdtallen, duizendtallen
- Getallenlijnen met grote getallen

---

## ✅ CORRECTE INHOUD VOOR GROEP 8

### Verhoudingen Domein (rekenen-verhoudingen.csv)

**Passend en goed:**
- 8V1: Rente berekenen (enkelvoudig) ✓
- 8V2: BTW berekenen (21%, 9%) ✓
- 8V3: Gemiddelde en verhoudingen ✓
- 8V4: Complexe schaalberekeningen ✓
- 8V5: Verhoudingen in woordproblemen ✓
- 8V6: Referentieniveau 1F/1S ✓

**Toelichting:**
- Financiële geletterdheid (rente, BTW) is passend voor groep 8
- Sluit aan bij maatschappelijke oriëntatie
- Voorbereiding op praktische situaties in VO en het dagelijks leven

### Meten & Meetkunde Domein (gedeeltelijk)

**Passend:**
- 8MM1: Complexe oppervlaktes (samengestelde figuren) ✓
- 8MM3: Schaalmodellen maken ✓
- 8MM4: Alle meeteenheden beheersen ✓
- 8MM5: Alle figuren (omtrek, oppervlakte, volume) ✓
- 8MM6: Referentieniveau 1F/1S meetkunde ✓

**Niet passend:**
- 8MM2: Pythagoras ❌ (zie eerder)

---

## AANBEVELINGEN VOOR CORRECTIES

### Te Verwijderen Leerdoelen:

1. **7MM2** - Pythagoras kennismaken (Groep 7)
2. **8MM2** - Pythagoras toepassen (Groep 8)
3. **8G2** - Vierkantswortels

### Te Vervangen Leerdoel:

4. **8G1** - Wetenschappelijke notatie → Vervang door "Grote getallen tot miljoenen"

### Vervangingsvoorstel voor 8G1:

**Oud:**
```
8G1: Wetenschappelijke notatie - machten van 10
```

**Nieuw:**
```
8G1: Grote getallen lezen, schrijven en afronden
Beschrijving: Getallen tot miljoenen lezen, schrijven, ordenen en afronden op verschillende posities
Niveau: M (midden groep 8)
Kerndoel: K28 (Getalsysteem)
Vraagtypen:
- Schrijf 4.567.890 in woorden
- Rond 8.734.521 af op duizendtallen
- Orden getallen van klein naar groot
- Welk getal is 100.000 meer dan 3.456.789?
- Lees en schrijf grote getallen van de getallenlijn
```

### Vervangingsvoorstel voor 8G2:

**Oud:**
```
8G2: Vierkantswortels
```

**Nieuw:**
```
8G2: Kwadraten van getallen tot 20
Beschrijving: Kwadraten van getallen 1-20 kennen en toepassen (in context van oppervlakte)
Niveau: M (midden groep 8)
Kerndoel: K29 (Hoofdrekenen)
Vraagtypen:
- Bereken 12² (vierkant met zijde 12 cm, oppervlakte?)
- Welk getal × zichzelf = 64?
- Een vierkant speelveld met zijde 15 meter, oppervlakte?
- 8 × 8 = ?
- Kwadraat van 20 = ?
Context: Altijd in relatie tot oppervlakteberekeningen, niet abstract
```

### Vervangingsvoorstel voor 7MM2 en 8MM2:

**Oud:**
```
7MM2: Pythagoras kennismaken
8MM2: Pythagoras toepassen
```

**Nieuw voor 7MM2:**
```
7MM2: Diagonaal schatten en meten
Beschrijving: Diagonalen in rechthoeken meten en schatten (zonder Pythagoras)
Niveau: M (midden groep 7)
Kerndoel: K33 (Meetkunde)
Vraagtypen:
- Meet de diagonaal van deze rechthoek met een liniaal
- Schat de diagonaal van een voetbalveld 100×60 meter
- Welke rechthoek heeft de langste diagonaal?
- Teken en meet de diagonalen in deze rechthoek
```

**Nieuw voor 8MM2:**
```
8MM2: Vlakke en ruimtelijke figuren eigenschappen
Beschrijving: Alle eigenschappen van figuren beheersen (hoeken, zijden, vlakken, ribben)
Niveau: M (midden groep 8)
Kerndoel: K33 (Meetkunde)
Vraagtypen:
- Hoeveel ribben heeft een kubus?
- Som van hoeken in driehoek = ?
- Hoeveel vlakken heeft een cilinder?
- Welke eigenschappen heeft een rechthoek?
- Vergelijk kubus en balk (overeenkomsten en verschillen)
```

---

## SAMENVATTING KERNDOELEN GROEP 8

### Wat WEL in kerndoelen zit (en dus mag):

**K23 - Automatiseren:**
- Alle tafels en sommen tot 100 automatisch

**K28 - Getalsysteem:**
- Gehele getallen tot miljoenen
- Decimalen tot drie cijfers achter de komma
- Breuken (stambreuken en eenvoudige niet-stambreuken)
- Negatieve getallen (basis: temperatuur, rekening)
- Procenten

**K29 - Hoofdrekenen:**
- Alle vier basisbewerkingen
- Strategieën (splitsing, compensatie)
- Schatten en afronden
- **GEEN worteltrekken of geavanceerde machten**

**K30 - Cijferend rekenen:**
- Standaardalgoritmen voor +, -, ×, :
- Rekenen met kommagetallen
- **GEEN algebraïsche bewerkingen**

**K32 - Meten:**
- Alle meeteenheden (lengte, gewicht, inhoud, tijd)
- Omrekenen tussen eenheden
- Tijd en tijdsduur
- Geld (inclusief BTW begrip)

**K33 - Meetkunde:**
- Vlakke figuren: omtrek en oppervlakte (vierkant, rechthoek, driehoek, cirkel met π)
- Ruimtelijke figuren: volume (kubus, balk, cilinder met π)
- Symmetrie, spiegeling, rotatie
- Coördinatenstelsel (4 kwadranten)
- Schaal op kaarten en tekeningen
- **GEEN Pythagoras of geavanceerde stellingen**

### Wat NIET in kerndoelen zit (en dus moet weg):

❌ Stelling van Pythagoras
❌ Vierkantswortels
❌ Wetenschappelijke notatie met machten
❌ Geavanceerde algebra
❌ Goniometrische verhoudingen
❌ Derdemachten of hogere machten

---

## CITO EINDTOETS REFERENTIE

### Referentieniveau 1F (Fundamenteel):
- Basale rekenvaardigheden die iedereen moet kunnen
- Eenvoudige bewerkingen, meten, meetkunde
- Herkennen en toepassen in standaardsituaties

### Referentieniveau 1S (Streefniveau groep 8):
- Gevorderde rekenvaardigheden
- Complexe woordproblemen
- Strategisch denken en meerstapsopgaven
- **MAAR GEEN VO-stof zoals Pythagoras of wortels!**

### Referentieniveau 2F (Basis VO):
- Dit is NIET voor groep 8
- Soms als uitdaging voor hoogbegaafden
- Maar NIET in standaard curriculum

---

## CONCLUSIE

De Groep 8 prompt templates bevatten **drie substantiële fouten** waarbij VO-stof (voortgezet onderwijs) ten onrechte is opgenomen in het basisschoolcurriculum:

1. **Pythagoras** (7MM2, 8MM2) - Te moeilijk, past niet bij kerndoelen
2. **Vierkantswortels** (8G2) - Te moeilijk, pas bij kerndoelen
3. **Wetenschappelijke notatie** (8G1) - Te geavanceerd voor deze leeftijd

Deze moeten worden **verwijderd of vervangen** door passende leerdoelen die wél aansluiten bij de SLO Kerndoelen K23, K28, K29, K30, K32, K33 voor groep 8.

De overige Groep 8 leerdoelen zijn **pedagogisch verantwoord** en sluiten goed aan bij:
- CITO eindtoetsniveau 1F/1S
- Nederlandse onderwijsstandaarden
- Leeftijdsadequaat leren
- Voorbereiding op voortgezet onderwijs (zonder VO-stof te anticiperen)

---

## ACTIE VEREIST

☐ Verwijder 7MM2 (Pythagoras kennismaken)
☐ Verwijder 8MM2 (Pythagoras toepassen)
☐ Verwijder 8G2 (Vierkantswortels)
☐ Vervang 8G1 (Wetenschappelijke notatie) door "Grote getallen"
☐ Voeg nieuwe leerdoelen toe zoals voorgesteld
☐ Regenereer alle betreffende oefeningen
☐ Update prompt templates in CSV-bestanden

**Prioriteit:** HOOG - Deze fouten kunnen leiden tot frustratie bij leerlingen en onjuiste voorbereiding op CITO eindtoets.
