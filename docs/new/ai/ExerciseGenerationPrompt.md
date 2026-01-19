# AI Prompt-Contract — Oefeningen Genereren (Rekenen-Wiskunde PO)

## Status
**Bindend prompt-contract**  
Dit document beschrijft de verplichte regels voor het genereren van rekenoefeningen voor het primair onderwijs.  
Afwijkingen leiden tot **ongeldige output** en worden door validatie geblokkeerd.

---

## 1. Doel

Genereer **didactisch correcte**, **SLO-conforme** rekenoefeningen die:

- exact passen binnen de vastgestelde **leerlijnen**
- voldoen aan `docs/schemas/ExerciseSchema.json`
- automatisch door **alle validators** komen
- geschikt zijn voor **direct gebruik** in een leerplatform

De output is **uitsluitend** een JSON-array met oefeningen.

---

## 2. Invoerparameters (worden vooraf gegeven)

- `domain` (string) — bijv. `verhoudingen`
- `grade` (integer) — 4 t/m 8
- `level` (string) — `n1`, `n2`, `n3`, `n4`
- `topic` (string) — exact zoals in `topic-canon.json`
- `count` (integer) — aantal oefeningen
- `allowedTaskForms` (array) — toegestane taskvormen voor dit niveau
- `misconceptKeys` (array) — toegestane misconcept-keys voor dit topic

---

## 3. Algemene harde regels (ALTIJD)

Deze regels gelden **voor alle niveaus**.

- Output is **alleen** een JSON-array  
- Geen markdown, uitleg, commentaar of extra tekst  
- Elk object voldoet exact aan `ExerciseSchema.json`  
- Gebruik **uitsluitend** de opgegeven `domain`, `grade`, `level`, `topic`  
- Voeg **geen** nieuwe topics, niveaus of domeinen toe  
- Gebruik **alleen** misconcept-keys uit `misconceptKeys`  
- Elk item bevat:
  - `schemaVersion`
  - `interaction`
  - `solution`
  - `feedback.correct`
  - `feedback.incorrect`
  - `metadata.taskForm`
  - `metadata.misconceptKeys`
- Taalgebruik is **leerlingtaal**, kort en concreet  
- Geen vakjargon of meta-taal (zoals *strategie*, *analyse*, *redeneer*)

---

## 4. Interactie- en antwoordregels

### Numeric
- `interaction.type = "numeric"` ⇒ `solution.value` is **numeriek**
  - toegestaan: `12`, `0.5`, `"0.5"`
  - verboden: `"evenveel"`, `"meer"`, `"minder"`, `"ja"`, `"nee"`

### MCQ
- `interaction.type = "mcq"` ⇒
  - `options[]` aanwezig (minstens 2)
  - `solution.index` is een integer ≥ 0

---

## 5. Verboden per niveau (STRIKT)

### 🔵 Niveau n1 — Kennismaken
**Verboden in n1:**
- contextopgaven
- meerstapsopgaven
- vergelijkingen
- reflectie- of uitlegvragen
- keuzes tussen antwoorden

---

### 🟢 Niveau n2 — Toepassen (standaardniveau PO)
**Verboden in n2:**
- foutanalyse-opgaven  
  (bijv. “wat gaat hier mis?”)
- verklarende vragen  
  (bijv. “leg uit waarom”)
- strategie- of aanpakvergelijkingen  
  (bijv. “welke is slimmer?”)
- meerstapsopgaven
- opgaven met keuzes vóór het rekenen
- categorische antwoorden bij numeric
- abstracte of formele taal

**Vereisten voor n2:**
- maximaal **één rekenhandeling**
- standaard, eenduidige context
- eventuele sturing alleen via korte aandachtszinnen  
  (bijv. “Let op de eenheden”)

---

### 🟡 Niveau n3 — Verdiepen
**Verboden in n3:**
- formele bewijzen
- abstracte generalisaties zonder context
- VO-wiskundetaal

---

### 🔴 Niveau n4 — Transfer
**Verboden in n4:**
- algebraïsche notatie
- formele bewijsvoering
- terminologie uit het voortgezet onderwijs

---

## 6. Domein- en groepgebonden verboden (SLO-gebonden)

- Procenttaal of procentnotatie vóór **groep 6**
- Procentberekeningen vóór **groep 7**
- Breukbewerkingen vóór **groep 6**
- Formele schaalnotatie (bijv. `1 : 100`) vóór **groep 7**

---

## 7. Taskvormen

- Elke oefening heeft **exact één** `metadata.taskForm`
- `metadata.taskForm` ∈ `allowedTaskForms`
- Verboden taskvormen voor het niveau **niet gebruiken**
- Geen impliciete taskvormen

---

## 8. Feedbackregels

- Feedback is:
  - kort
  - concreet
  - direct helpend
- Geen nieuwe concepten introduceren
- Geen uitleg die buiten het niveau valt

---

## 9. Zelfcontrole (verplicht vóór output)

Controleer intern dat:

- alle `numeric` antwoorden numeriek zijn
- alle `taskForm`s toegestaan zijn
- alle `misconceptKeys` geldig zijn
- geen verboden niveauelementen zijn gebruikt
- het schema volledig klopt

**Lever daarna direct de JSON-array op.**

---

## 10. Outputformaat (ABSOLUUT)

- Eén JSON-array
- Geen extra tekst
- Geen markdown
- Geen toelichting
