# VERHOUDINGEN VALIDATOR - VERGELIJKING & KEUZEWIJZER

## 📊 Overzicht Versies

Dit document helpt je kiezen tussen validator v2.0 en v3.0.

---

## 🔍 Quick Comparison

| **Aspect** | **v2.0 (Basic)** | **v3.0 (Enhanced)** |
|------------|------------------|---------------------|
| **Totaal checks** | ~15 | **60+** |
| **Execution time** | ~5ms/item | ~15ms/item |
| **False positives** | Laag | Iets hoger (strict checks) |
| **Code size** | 450 regels | 1,100 regels |
| **Dependencies** | `json`, `typing` | `json`, `typing`, `re`, `fractions`, `decimal` |
| **Best for** | Rapid development | Production quality |
| **Complexity** | Low | Medium |

---

## ✅ Wanneer v2.0 Gebruiken

### **Development Fase**
- Snel itereren over nieuwe items
- Prototyping en experimenten
- Eerste draft van items

### **Eenvoudige Validatie**
- Alleen basis structuur checks nodig
- Geen strenge kwaliteitseisen (nog)
- Team is ervaren (weinig fouten)

### **Performance Kritisch**
- Validatie van 1000+ items per seconde
- Real-time validatie in UI
- Resource-beperkte omgeving

### **Voorbeeld Use Case**
```python
# Snelle check tijdens development
validator = VerhoudingenValidator()
result = validator.valideer_item(draft_item)

if result.valid:
    print("✓ Basis structuur OK, ga door met ontwikkelen")
else:
    print("✗ Fix eerst deze errors:", result.errors[:3])
```

---

## 🚀 Wanneer v3.0 Gebruiken

### **Pre-Productie Validatie**
- Items klaar voor publicatie
- CITO-compliance vereist
- Kwaliteitsborging

### **Nieuwe Teams / Generatoren**
- Onervaren content creators
- Nieuwe AI-generators trainen
- Externe leveranciers

### **Kwaliteitsanalyse**
- Bestaande itembank reviewen
- Kwaliteitstrends analyseren
- Rapportage voor stakeholders

### **Stricte Requirements**
- Leeftijd-geschikte content verplicht
- Rekenkundige correctheid critical
- Didactische kwaliteit belangrijk

### **Voorbeeld Use Case**
```python
# Complete validatie voor productie
validator = VerhoudingenValidatorEnhanced(strict_mode=True)
resultaten = validator.valideer_set(production_items)

rapport = validator.genereer_rapport(resultaten)
print(rapport)

if resultaten['percentage_valide'] >= 95:
    print("✅ Kwaliteit voldoende, deploy naar productie")
else:
    print("❌ Items verbeteren eerst")
```

---

## 📋 Feature Matrix

### **Basisvalidatie** (beide versies)

| Feature | v2.0 | v3.0 | Notes |
|---------|------|------|-------|
| Structuur checks | ✅ | ✅ | Verplichte velden |
| Groep/niveau checks | ✅ | ✅ | 4-8, M/E |
| Stappenlogica | ✅ | ✅ | Max stappen per niveau |
| Subdomein validatie | ✅ | ✅ | Toegestane subdomeinen |
| Afleiders count | ✅ | ✅ | Exact 4 opties |
| Correct antwoord | ✅ | ✅ | Exact 1 correct |
| Taalcomplexiteit basic | ✅ | ✅ | Zinsaantal, woordlengte |
| Metadata presence | ✅ | ✅ | Verplichte velden |
| LOVA presence | ✅ | ✅ | 4 onderdelen |

### **Geavanceerde Validatie** (alleen v3.0)

| Feature | v2.0 | v3.0 | Impact |
|---------|------|------|--------|
| **Inhoudelijke Validatie** | | | |
| Breuk correctheid | ❌ | ✅ | Detecteert 1/3 in G4-M |
| Decimaal notatie | ❌ | ✅ | Consistentie check |
| Percentage bereiken | ❌ | ✅ | G5-M: alleen 50/100% |
| Schaal validatie | ❌ | ✅ | Standaard schalen |
| **Context Validatie** | | | |
| Leeftijd-geschikt | ❌ | ✅ | Geen hypotheek G4 |
| Context suggesties | ❌ | ✅ | Passende onderwerpen |
| Realistische getallen | ❌ | ✅ | €1-20 zakgeld |
| **Afleider Kwaliteit** | | | |
| Numerieke plausibiliteit | ❌ | ✅ | Niet 100× te ver |
| Antwoord spreiding | ❌ | ✅ | Varieer positie |
| Fouttype uitgebreid | ✅ Basic | ✅ 15+ types | |
| **Rekencontrole** | | | |
| Breuk berekeningen | ❌ | ✅ | 1/2 + 1/4 check |
| Percentage berekeningen | ❌ | ✅ | 25% × 120 check |
| **Taal Extended** | | | |
| Gemiddelde zinslengte | ❌ | ✅ | Max 15 woorden G4 |
| Dubbelzinnige woorden | ❌ | ✅ | "dit", "dat" detect |
| **Metadata Extended** | | | |
| Moeilijkheid ranges | ❌ | ✅ | Per niveau bereik |
| Tijd validatie | ❌ | ✅ | 20-45s voor G4-M |
| **Didactiek** | | | |
| LOVA lengte | ❌ | ✅ | Min 10 karakters |
| Feedback specificiteit | ❌ | ✅ | Per fouttype |
| Stappen consistentie | ❌ | ✅ | Match metadata |
| **Visualisatie** | | | |
| Verplichte vis check | ❌ | ✅ | G4 breuken |
| Type specificatie | ❌ | ✅ | Cirkel/rechthoek |
| **Cross-Validatie** | | | |
| Moeilijkheid vs stappen | ❌ | ✅ | Logische relatie |
| Moeilijkheid vs tijd | ❌ | ✅ | Correlatie |
| Tijd per stap | ❌ | ✅ | Min 15s/stap |

---

## 🎯 Use Case Scenarios

### **Scenario 1: Nieuwe AI Generator Trainen**

**Keuze:** ✅ **v3.0 Enhanced**

**Waarom:**
- Generator maakt veel fouten in begin
- Strikte checks helpen training
- Quality breakdown toont zwakke punten
- Rapport voor iteratie

**Voorbeeld workflow:**
```python
validator = VerhoudingenValidatorEnhanced(strict_mode=False)

for epoch in range(10):
    items = generator.generate(prompt)
    results = validator.valideer_set(items)

    print(f"Epoch {epoch}: {results['gemiddelde_score']:.2f}")

    # Train op errors
    for item, res in zip(items, results['individuele_resultaten']):
        if not res.valid:
            generator.add_negative_example(item, res.errors)
```

---

### **Scenario 2: Rapid Prototyping**

**Keuze:** ✅ **v2.0 Basic**

**Waarom:**
- Snelheid belangrijker dan perfectie
- Team weet wat ze doen
- Iteratie cycle < 5 minuten

**Voorbeeld workflow:**
```python
validator = VerhoudingenValidator()

while not done:
    item = create_draft_item()
    result = validator.valideer_item(item)

    if not result.valid:
        print("Quick fix needed:", result.errors[0])
        fix_immediately(item)
    else:
        commit_to_batch(item)
```

---

### **Scenario 3: Bestaande Itembank Review**

**Keuze:** ✅ **v3.0 Enhanced**

**Waarom:**
- Volledige analyse nodig
- Identificeer patronen
- Prioriteer verbeteringen
- Rapportage voor management

**Voorbeeld workflow:**
```python
validator = VerhoudingenValidatorEnhanced()

# Valideer hele bank
results = validator.valideer_set(all_items)
rapport = validator.genereer_rapport(results)

# Analyseer per categorie
for cat, score in results['quality_breakdown'].items():
    if score < 0.8:
        print(f"Verbeterpunt: {cat} (score: {score:.2f})")

# Top errors -> action items
for error, count in results['top_errors'][:5]:
    create_improvement_ticket(error, count)
```

---

### **Scenario 4: CI/CD Pipeline**

**Keuze:** 🔀 **Beide**

**Waarom:**
- v2.0 voor snelle pre-commit check
- v3.0 voor pre-productie gate

**Voorbeeld workflow:**
```bash
# Pre-commit hook (snel)
python verhoudingen-validator.py new_items.json --fast

# Pre-production (grondig)
python verhoudingen-validator-v3.py new_items.json --strict --report
```

---

## 📊 Performance Comparison

### **Benchmark (1000 items)**

| Metric | v2.0 | v3.0 | Verschil |
|--------|------|------|----------|
| Total time | 5.2s | 15.8s | +3× |
| Per item | 5.2ms | 15.8ms | +3× |
| Memory | 45MB | 72MB | +60% |
| CPU usage | Low | Medium | |

### **Wanneer Performance Belangrijk Is**

**v2.0 kiezen als:**
- Real-time validatie in UI (< 10ms response)
- Validatie van 10.000+ items per run
- Resource-beperkte omgeving (embedded, mobile)

**v3.0 is OK als:**
- Batch validatie (niet real-time)
- Max 1.000 items per run
- Server-side processing

---

## 🔄 Migratiestrategie

### **Gefaseerde Aanpak (aanbevolen)**

#### **Fase 1: Parallel Draaien (Week 1-2)**
```python
# Beide validators parallel
v2_validator = VerhoudingenValidator()
v3_validator = VerhoudingenValidatorEnhanced(strict_mode=False)

v2_result = v2_validator.valideer_item(item)
v3_result = v3_validator.valideer_item(item)

# Vergelijk
if v2_result.valid != v3_result.valid:
    log_difference(item, v2_result, v3_result)
```

#### **Fase 2: v3.0 Warnings Alleen (Week 3-4)**
```python
# v3.0 gebruikt, maar alleen errors blokkeren
validator = VerhoudingenValidatorEnhanced(strict_mode=False)
result = validator.valideer_item(item)

if result.errors:
    reject_item(item)
if result.warnings:
    log_for_improvement(item)  # Niet blokkeren
```

#### **Fase 3: v3.0 Strict Mode (Week 5+)**
```python
# Volledige v3.0 met strict mode
validator = VerhoudingenValidatorEnhanced(strict_mode=True)
result = validator.valideer_item(item)

if not result.valid:  # Errors + warnings
    reject_item(item)
```

---

## 💡 Aanbevelingen per Team

### **Kleine Teams (1-3 personen)**
- **Advies:** Start met **v2.0**
- Upgrade naar v3.0 bij:
  - Externe stakeholders (CITO review)
  - Publicatie naar eindgebruikers
  - Kwaliteitsproblemen in productie

### **Middelgrote Teams (4-10 personen)**
- **Advies:** **v2.0** voor development, **v3.0** voor staging
- Pipeline:
  1. Dev: v2.0 basic checks
  2. Staging: v3.0 warnings
  3. Production: v3.0 strict

### **Grote Teams (10+ personen, externe leveranciers)**
- **Advies:** **v3.0 altijd**
- Waarom:
  - Inconsistente kwaliteit zonder strenge checks
  - Rapportage voor coordinatie nodig
  - Quality gates essentieel

---

## 🎓 Conclusie

### **Vuistregel**

```
v2.0 = "Is het item technisch correct?"
v3.0 = "Is het item production-ready?"
```

### **Decision Tree**

```
Items voor productie?
├─ JA
│  ├─ Hoge kwaliteitseisen? → v3.0 STRICT
│  └─ Normale eisen? → v3.0 NORMAL
└─ NEE (development)
   ├─ Ervaren team? → v2.0
   └─ Nieuw team/generator? → v3.0 NORMAL
```

### **Combinatie Strategie (Best of Both)**

```python
class HybridValidator:
    def __init__(self):
        self.fast = VerhoudingenValidator()
        self.thorough = VerhoudingenValidatorEnhanced()

    def validate(self, item, mode='auto'):
        if mode == 'fast':
            return self.fast.valideer_item(item)
        elif mode == 'thorough':
            return self.thorough.valideer_item(item)
        else:  # auto
            # Eerst snelle check
            fast_result = self.fast.valideer_item(item)
            if not fast_result.valid:
                return fast_result  # Fail fast

            # Dan grondige check
            return self.thorough.valideer_item(item)
```

---

**Beide validators hebben hun plek. Kies verstandig!** 🎯
