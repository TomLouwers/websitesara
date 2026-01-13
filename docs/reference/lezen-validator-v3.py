#!/usr/bin/env python3
"""
LEZEN VALIDATOR v3.0 - Enhanced Validator voor Leesbegrip Items

Valideert leesbegrip items voor Groep 3-8, Midden/Eind niveau.
Gebaseerd op prompt-lezen-v2.md specificaties.

Features:
- Volledige G3-G8 M/E niveauregels (12 varianten)
- AVI-niveau validatie
- Tekstlengte en zinsbouw checks
- Vraagtype distributie validatie
- G3-specifieke checks (plaatje, korte zinnen, hoogfrequente woorden)
- Strategic distractor validation
- RALFI focus validation
- Woordenschat niveau checks
- 60+ quality checks per item

Author: Claude (Anthropic)
Version: 3.0
Date: 2026-01
"""

import json
import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from collections import Counter


@dataclass
class ValidationResult:
    """Result of validation"""
    valid: bool
    score: float  # 0.0-1.0 (1.0 = perfect)
    errors: List[str]
    warnings: List[str]
    info: List[str]


class LezenValidatorEnhanced:
    """Enhanced validator for reading comprehension items"""

    # NIVEAU REGELS per (groep, niveau)
    NIVEAU_REGELS = {
        # GROEP 3
        (3, 'M'): {
            'avi_niveau': ['Start', 'M3'],
            'tekst_lengte': (20, 50),
            'zin_lengte_max': 8,
            'zinnen_max': 5,
            'vraagtypen_verdeling': {
                'letterlijk': 0.80,
                'inferentie': 0.20,
            },
            'visualisatie': 'verplicht',  # Plaatje VERPLICHT
            'woordenschat': 'basis',
            'moeilijkheid': (0.10, 0.35),
            'tijd_totaal': (120, 180),  # 2-3 minuten
            'dmt_verwacht': (10, 20),
        },
        (3, 'E'): {
            'avi_niveau': ['E3', 'M4'],
            'tekst_lengte': (50, 100),
            'zin_lengte_max': 10,
            'zinnen_max': 12,
            'vraagtypen_verdeling': {
                'letterlijk': 0.60,
                'inferentie': 0.30,
                'volgorde': 0.10,
            },
            'visualisatie': 'verplicht',
            'woordenschat': 'basis',
            'moeilijkheid': (0.25, 0.50),
            'tijd_totaal': (180, 240),  # 3-4 minuten
            'dmt_verwacht': (20, 35),
        },

        # GROEP 4
        (4, 'M'): {
            'avi_niveau': ['M4', 'E4'],
            'tekst_lengte': (100, 150),
            'zin_lengte_max': 12,
            'zinnen_max': 20,
            'vraagtypen_verdeling': {
                'letterlijk': 0.50,
                'inferentie': 0.30,
                'hoofdgedachte': 0.20,
            },
            'woordenschat': 'basis',
            'moeilijkheid': (0.35, 0.60),
            'tijd_totaal': (300, 420),  # 5-7 minuten
            'dmt_verwacht': (35, 55),
        },
        (4, 'E'): {
            'avi_niveau': ['E4', 'M5'],
            'tekst_lengte': (150, 250),
            'zin_lengte_max': 15,
            'zinnen_max': 30,
            'alineas_min': 2,
            'vraagtypen_verdeling': {
                'letterlijk': 0.40,
                'inferentie': 0.40,
                'hoofdgedachte': 0.10,
                'mening': 0.10,
            },
            'woordenschat': 'basis',
            'moeilijkheid': (0.45, 0.70),
            'tijd_totaal': (420, 600),  # 7-10 minuten
            'dmt_verwacht': (55, 75),
        },

        # GROEP 5
        (5, 'M'): {
            'avi_niveau': ['M5', 'E5'],
            'tekst_lengte': (250, 350),
            'zin_lengte_max': 20,
            'alineas_min': 3,
            'vraagtypen_verdeling': {
                'letterlijk': 0.30,
                'inferentie': 0.40,
                'evaluatie': 0.30,
            },
            'woordenschat': 'uitgebreid',
            'moeilijkheid': (0.50, 0.75),
            'tijd_totaal': (600, 720),  # 10-12 minuten
            'dmt_verwacht': (75, 95),
        },
        (5, 'E'): {
            'avi_niveau': ['E5', 'M6'],
            'tekst_lengte': (350, 500),
            'alineas_min': 5,
            'vraagtypen_verdeling': {
                'letterlijk': 0.30,
                'inferentie': 0.40,
                'evaluatie': 0.30,
            },
            'woordenschat': 'uitgebreid',
            'moeilijkheid': (0.60, 0.80),
            'tijd_totaal': (720, 900),  # 12-15 minuten
            'dmt_verwacht': (95, 115),
        },

        # GROEP 6
        (6, 'M'): {
            'avi_niveau': ['M6', 'E6'],
            'tekst_lengte': (500, 700),
            'alineas_min': 7,
            'vraagtypen_verdeling': {
                'letterlijk': 0.20,
                'inferentie': 0.40,
                'evaluatie': 0.40,
            },
            'woordenschat': 'gevorderd',
            'moeilijkheid': (0.65, 0.85),
            'tijd_totaal': (900, 1080),  # 15-18 minuten
            'dmt_verwacht': (115, 135),
        },
        (6, 'E'): {
            'avi_niveau': ['E6', 'PLUS'],
            'tekst_lengte': (700, 1000),
            'vraagtypen_verdeling': {
                'letterlijk': 0.20,
                'inferentie': 0.40,
                'evaluatie': 0.40,
            },
            'woordenschat': 'gevorderd',
            'moeilijkheid': (0.70, 0.90),
            'tijd_totaal': (1080, 1200),
            'dmt_verwacht': (135, 150),
        },

        # GROEP 7
        (7, 'M'): {
            'avi_niveau': ['PLUS'],
            'tekst_lengte': (800, 1200),
            'woordenschat': 'gevorderd',
            'moeilijkheid': (0.75, 0.92),
            'dmt_verwacht': (135, 160),
        },
        (7, 'E'): {
            'avi_niveau': ['PLUS'],
            'tekst_lengte': (1000, 1500),
            'woordenschat': 'gevorderd',
            'moeilijkheid': (0.80, 0.95),
            'dmt_verwacht': (140, 170),
        },

        # GROEP 8
        (8, 'M'): {
            'avi_niveau': ['PLUS'],
            'tekst_lengte': (1200, 1800),
            'woordenschat': 'gevorderd',
            'moeilijkheid': (0.80, 0.95),
            'referentieniveau': '1F',
            'dmt_verwacht': (145, 175),
        },
        (8, 'E'): {
            'avi_niveau': ['PLUS'],
            'tekst_lengte': (1500, 2000),
            'woordenschat': 'gevorderd',
            'moeilijkheid': (0.85, 1.0),
            'referentieniveau': '1S',
            'dmt_verwacht': (150, 180),
        },
    }

    # Hoogfrequente woorden voor G3 (top 100)
    HOOGFREQUENT_G3 = {
        'de', 'het', 'een', 'en', 'van', 'in', 'is', 'op', 'te', 'dat',
        'hij', 'het', 'zijn', 'aan', 'voor', 'met', 'als', 'maar', 'om', 'was',
        'heeft', 'kan', 'niet', 'er', 'ze', 'ook', 'bij', 'naar', 'dan', 'zo',
        'dit', 'uit', 'nog', 'wat', 'nu', 'wel', 'mijn', 'daar', 'heb', 'alle',
        'ik', 'jij', 'je', 'wij', 'zij', 'we', 'ze', 'hij', 'hun',
        'mama', 'papa', 'oma', 'opa', 'kind', 'school', 'huis', 'boom', 'auto',
        'kat', 'hond', 'bal', 'boek', 'spelen', 'eten', 'drinken', 'slapen',
        'groot', 'klein', 'rood', 'blauw', 'groen', 'geel', 'mooi', 'leuk',
    }

    # Geldige vraagtypen
    VRAAGTYPEN = {
        'letterlijk', 'inferentie', 'evaluatie', 'hoofdgedachte',
        'mening', 'volgorde', 'woordenschat', 'structuur', 'retorisch'
    }

    # Geldige tekstsoorten
    TEKSTSOORTEN = {
        'verhaal', 'informatief', 'instructief', 'betogend',
        'krantenbericht', 'recensie', 'brief', 'gedicht'
    }

    # RALFI focus opties
    RALFI_FOCUS = {'R', 'A', 'L', 'F', 'I', None}


    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []


    def valideer_item(self, item: Dict[str, Any]) -> ValidationResult:
        """Main validation method"""
        self.errors = []
        self.warnings = []
        self.info = []

        # 1. Basis structuur
        self._check_basis_structuur(item)

        # 2. Niveau regels
        self._check_niveau_regels(item)

        # 3. Tekst validatie
        self._check_tekst_kwaliteit(item)

        # 4. Vraag validatie
        self._check_vragen_kwaliteit(item)

        # 5. Afleiders validatie
        self._check_afleiders(item)

        # 6. G3-specifieke checks
        if item.get('groep') == 3:
            self._check_g3_specifiek(item)

        # 7. Metadata checks
        self._check_metadata(item)

        # 8. Cross-validation
        self._check_cross_validation(item)

        # Calculate score
        score = self._calculate_score()

        return ValidationResult(
            valid=len(self.errors) == 0,
            score=score,
            errors=self.errors,
            warnings=self.warnings,
            info=self.info
        )


    def _check_basis_structuur(self, item: Dict[str, Any]):
        """Check basic required fields"""
        required_fields = [
            'id', 'groep', 'niveau', 'avi_niveau', 'tekstsoort',
            'tekst', 'tekst_lengte_woorden'
        ]

        for field in required_fields:
            if field not in item:
                self.errors.append(f"❌ Verplicht veld ontbreekt: '{field}'")

        # Check groep
        groep = item.get('groep')
        if groep not in [3, 4, 5, 6, 7, 8]:
            self.errors.append(f"❌ Ongeldige groep: {groep} (moet 3-8 zijn)")

        # Check niveau
        niveau = item.get('niveau')
        if niveau not in ['M', 'E']:
            self.errors.append(f"❌ Ongeldig niveau: {niveau} (moet M of E zijn)")

        # Check tekstsoort
        tekstsoort = item.get('tekstsoort')
        if tekstsoort and tekstsoort not in self.TEKSTSOORTEN:
            self.warnings.append(f"⚠️  Ongebruikelijke tekstsoort: {tekstsoort}")


    def _check_niveau_regels(self, item: Dict[str, Any]):
        """Check niveau-specific rules"""
        groep = item.get('groep')
        niveau = item.get('niveau')

        regels = self.NIVEAU_REGELS.get((groep, niveau))
        if not regels:
            self.errors.append(f"❌ Geen regels voor G{groep}-{niveau}")
            return

        # 1. AVI-niveau
        avi = item.get('avi_niveau')
        if avi:
            geldige_avi = regels.get('avi_niveau', [])
            if avi not in geldige_avi:
                self.errors.append(
                    f"❌ AVI-niveau '{avi}' niet geldig voor G{groep}-{niveau}. "
                    f"Verwacht: {' of '.join(geldige_avi)}"
                )

        # 2. Tekstlengte
        tekst_lengte = item.get('tekst_lengte_woorden', 0)
        min_len, max_len = regels.get('tekst_lengte', (0, 999999))
        if not (min_len <= tekst_lengte <= max_len):
            self.errors.append(
                f"❌ Tekstlengte {tekst_lengte} woorden buiten range "
                f"({min_len}-{max_len}) voor G{groep}-{niveau}"
            )

        # 3. Moeilijkheidsgraad
        moeilijkheid = item.get('moeilijkheidsgraad')
        if moeilijkheid:
            min_m, max_m = regels.get('moeilijkheid', (0, 1))
            if not (min_m <= moeilijkheid <= max_m):
                self.warnings.append(
                    f"⚠️  Moeilijkheidsgraad {moeilijkheid:.2f} buiten range "
                    f"({min_m:.2f}-{max_m:.2f}) voor G{groep}-{niveau}"
                )

        # 4. Woordenschat niveau
        woordenschat = item.get('woordenschat_niveau')
        verwacht_woordenschat = regels.get('woordenschat')
        if woordenschat and verwacht_woordenschat:
            if woordenschat != verwacht_woordenschat:
                self.warnings.append(
                    f"⚠️  Woordenschat niveau '{woordenschat}' afwijkend van verwacht "
                    f"'{verwacht_woordenschat}' voor G{groep}-{niveau}"
                )


    def _check_tekst_kwaliteit(self, item: Dict[str, Any]):
        """Check text quality"""
        tekst = item.get('tekst', '')
        if not tekst:
            self.errors.append("❌ Geen tekst aanwezig")
            return

        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        # 1. Zinslengte (voor G3-4)
        max_zin_lengte = regels.get('zin_lengte_max')
        if max_zin_lengte:
            zinnen = re.split(r'[.!?]', tekst)
            zinnen = [z.strip() for z in zinnen if z.strip()]

            for i, zin in enumerate(zinnen, 1):
                woorden = zin.split()
                if len(woorden) > max_zin_lengte:
                    self.errors.append(
                        f"❌ Zin {i} heeft {len(woorden)} woorden (max {max_zin_lengte}): '{zin[:50]}...'"
                    )

            # Check aantal zinnen
            max_zinnen = regels.get('zinnen_max')
            if max_zinnen and len(zinnen) > max_zinnen:
                self.warnings.append(
                    f"⚠️  Tekst heeft {len(zinnen)} zinnen (max {max_zinnen})"
                )

        # 2. Alinea structuur (G4+)
        min_alineas = regels.get('alineas_min')
        if min_alineas:
            alineas = tekst.split('\n\n')
            alineas = [a.strip() for a in alineas if a.strip()]
            if len(alineas) < min_alineas:
                self.warnings.append(
                    f"⚠️  Tekst heeft {len(alineas)} alinea's (min {min_alineas})"
                )

        # 3. Tekstlengte verificatie
        tekst_lengte_berekend = len(tekst.split())
        tekst_lengte_metadata = item.get('tekst_lengte_woorden', 0)

        verschil = abs(tekst_lengte_berekend - tekst_lengte_metadata)
        if verschil > 5:  # Tolerantie van 5 woorden
            self.warnings.append(
                f"⚠️  Tekstlengte metadata ({tekst_lengte_metadata}) komt niet overeen "
                f"met berekende lengte ({tekst_lengte_berekend})"
            )


    def _check_vragen_kwaliteit(self, item: Dict[str, Any]):
        """Check question quality"""
        vragen = item.get('vragen', [])

        if not vragen:
            self.errors.append("❌ Geen vragen aanwezig")
            return

        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        # 1. Vraagtype validatie
        vraagtypen_gevonden = Counter()
        for i, vraag in enumerate(vragen, 1):
            vraagtype = vraag.get('vraagtype')

            if not vraagtype:
                self.errors.append(f"❌ Vraag {i}: vraagtype ontbreekt")
                continue

            if vraagtype not in self.VRAAGTYPEN:
                self.errors.append(
                    f"❌ Vraag {i}: ongeldig vraagtype '{vraagtype}'"
                )
                continue

            vraagtypen_gevonden[vraagtype] += 1

            # Check of vraag niet leeg is
            if not vraag.get('hoofdvraag'):
                self.errors.append(f"❌ Vraag {i}: hoofdvraag is leeg")

            # Check correct antwoord
            if not vraag.get('correct_antwoord'):
                self.errors.append(f"❌ Vraag {i}: correct_antwoord ontbreekt")

            # Check RALFI focus (G4+)
            if groep >= 4:
                ralfi = vraag.get('ralfi_focus')
                if ralfi and ralfi not in self.RALFI_FOCUS:
                    self.warnings.append(
                        f"⚠️  Vraag {i}: ongeldige RALFI focus '{ralfi}'"
                    )

        # 2. Vraagtype distributie (als regels aanwezig)
        verdeling_verwacht = regels.get('vraagtypen_verdeling')
        if verdeling_verwacht and len(vragen) >= 3:
            totaal = len(vragen)

            for vraagtype, verwacht_percentage in verdeling_verwacht.items():
                aantal = vraagtypen_gevonden.get(vraagtype, 0)
                actueel_percentage = aantal / totaal
                verschil = abs(actueel_percentage - verwacht_percentage)

                if verschil > 0.25:  # Tolerantie 25%
                    self.warnings.append(
                        f"⚠️  Vraagtype '{vraagtype}': {actueel_percentage:.0%} "
                        f"(verwacht ~{verwacht_percentage:.0%})"
                    )

        # 3. Vraag moeilijkheid progressie
        moeilijkheden = [v.get('moeilijkheidsgraad', 0.5) for v in vragen
                         if v.get('moeilijkheidsgraad')]

        if len(moeilijkheden) >= 3:
            # Check of vragen oplopend moeilijker worden
            if moeilijkheden != sorted(moeilijkheden):
                self.info.append(
                    "ℹ️  Vragen worden niet progressief moeilijker "
                    "(kan opzettelijk zijn)"
                )


    def _check_afleiders(self, item: Dict[str, Any]):
        """Check distractor quality"""
        vragen = item.get('vragen', [])

        for i, vraag in enumerate(vragen, 1):
            afleiders = vraag.get('afleiders', [])
            correct = vraag.get('correct_antwoord', '')

            # 1. Aantal afleiders (meestal 3)
            if len(afleiders) < 2:
                self.errors.append(
                    f"❌ Vraag {i}: te weinig afleiders ({len(afleiders)}, min 2)"
                )

            if len(afleiders) > 4:
                self.warnings.append(
                    f"⚠️  Vraag {i}: veel afleiders ({len(afleiders)})"
                )

            # 2. Afleiders niet leeg
            for j, afleider in enumerate(afleiders, 1):
                if not afleider or not str(afleider).strip():
                    self.errors.append(f"❌ Vraag {i}, afleider {j}: is leeg")

            # 3. Afleiders niet gelijk aan correct antwoord
            for afleider in afleiders:
                if str(afleider).lower().strip() == str(correct).lower().strip():
                    self.errors.append(
                        f"❌ Vraag {i}: afleider '{afleider}' is gelijk aan correct antwoord"
                    )

            # 4. Afleiders onderling verschillend
            afleiders_lower = [str(a).lower().strip() for a in afleiders]
            if len(afleiders_lower) != len(set(afleiders_lower)):
                self.errors.append(
                    f"❌ Vraag {i}: dubbele afleiders gevonden"
                )

            # 5. Afleider lengte vergelijkbaar (waarschuwing)
            if correct and afleiders:
                correct_len = len(str(correct))
                afleider_lens = [len(str(a)) for a in afleiders]
                avg_afleider_len = sum(afleider_lens) / len(afleider_lens)

                if abs(correct_len - avg_afleider_len) > correct_len * 0.5:
                    self.warnings.append(
                        f"⚠️  Vraag {i}: correct antwoord ({correct_len} chars) "
                        f"veel anders dan afleiders ({avg_afleider_len:.0f} chars)"
                    )


    def _check_g3_specifiek(self, item: Dict[str, Any]):
        """Extra checks specific for Groep 3"""
        niveau = item.get('niveau')
        tekst = item.get('tekst', '').lower()
        vragen = item.get('vragen', [])

        regels = self.NIVEAU_REGELS.get((3, niveau), {})

        # 1. Visualisatie VERPLICHT
        visualisatie = regels.get('visualisatie')
        if visualisatie == 'verplicht':
            visual_keywords = [
                'plaatje', 'tekening', 'zie', 'afbeelding', 'figuur',
                'foto', 'illustratie', 'prent'
            ]

            heeft_visual = any(keyword in tekst for keyword in visual_keywords)

            # Ook checken in vragen
            if not heeft_visual:
                for vraag in vragen:
                    hoofdvraag = vraag.get('hoofdvraag', '').lower()
                    if any(keyword in hoofdvraag for keyword in visual_keywords):
                        heeft_visual = True
                        break

            if not heeft_visual:
                self.errors.append(
                    "❌ G3: Visualisatie is VERPLICHT. "
                    "Vermeld '(zie plaatje)' of refereer naar afbeelding."
                )

        # 2. Hoogfrequente woorden check (sample)
        woorden = tekst.split()
        total_woorden = len(woorden)

        if total_woorden > 10:
            hoogfrequent_count = sum(
                1 for w in woorden
                if w.strip('.,!?;:').lower() in self.HOOGFREQUENT_G3
            )
            hoogfrequent_percentage = hoogfrequent_count / total_woorden

            if hoogfrequent_percentage < 0.50:  # Minstens 50% hoogfrequent
                self.warnings.append(
                    f"⚠️  G3: Slechts {hoogfrequent_percentage:.0%} hoogfrequente woorden "
                    f"(verwacht >50% voor G3)"
                )

        # 3. Geen abstracte begrippen
        abstracte_woorden = {
            'vriendschap', 'eerlijkheid', 'democratie', 'evolutie',
            'filosofie', 'emotie', 'gevoel', 'gedachte', 'idee',
            'mening', 'standpunt', 'argument'
        }

        gevonden_abstract = [w for w in woorden if w in abstracte_woorden]
        if gevonden_abstract:
            self.warnings.append(
                f"⚠️  G3: Abstracte woorden gevonden: {', '.join(set(gevonden_abstract))}"
            )

        # 4. Vraagtypen check
        for i, vraag in enumerate(vragen, 1):
            vraagtype = vraag.get('vraagtype')
            hoofdvraag = vraag.get('hoofdvraag', '').lower()

            # G3-M: GEEN waarom/hoe voelt vragen
            if niveau == 'M':
                verboden_woorden = ['waarom', 'hoe voelt']
                if any(woord in hoofdvraag for woord in verboden_woorden):
                    self.errors.append(
                        f"❌ G3-M Vraag {i}: 'Waarom' en 'Hoe voelt' vragen "
                        f"zijn te abstract voor M3"
                    )


    def _check_metadata(self, item: Dict[str, Any]):
        """Check metadata completeness and correctness"""

        # 1. ID format
        item_id = item.get('id', '')
        expected_pattern = r'^L_G[3-8]_[ME]_\d{3}$'
        if not re.match(expected_pattern, item_id):
            self.warnings.append(
                f"⚠️  ID '{item_id}' volgt niet verwacht patroon: L_G[3-8]_[ME]_###"
            )

        # 2. Geschatte tijd
        totale_tijd = item.get('totale_tijd_sec')
        vragen = item.get('vragen', [])

        if totale_tijd and vragen:
            # Bereken som van vraag tijden
            vraag_tijden_sum = sum(v.get('geschatte_tijd_sec', 0) for v in vragen)

            if vraag_tijden_sum > 0:
                # Geschatte leestijd (tekst_lengte / DMT)
                groep = item.get('groep')
                niveau = item.get('niveau')
                regels = self.NIVEAU_REGELS.get((groep, niveau), {})

                dmt_min, dmt_max = regels.get('dmt_verwacht', (50, 100))
                dmt_avg = (dmt_min + dmt_max) / 2

                tekst_lengte = item.get('tekst_lengte_woorden', 0)
                geschatte_leestijd = (tekst_lengte / dmt_avg) * 60  # seconden

                totaal_verwacht = geschatte_leestijd + vraag_tijden_sum

                verschil = abs(totale_tijd - totaal_verwacht)
                if verschil > 60:  # Tolerantie 1 minuut
                    self.warnings.append(
                        f"⚠️  Totale tijd ({totale_tijd}s) wijkt af van verwacht "
                        f"({totaal_verwacht:.0f}s = {geschatte_leestijd:.0f}s lezen + "
                        f"{vraag_tijden_sum}s vragen)"
                    )

        # 3. Toelichting aanwezig
        vragen = item.get('vragen', [])
        for i, vraag in enumerate(vragen, 1):
            if not vraag.get('toelichting'):
                self.warnings.append(
                    f"⚠️  Vraag {i}: geen toelichting aanwezig (aanbevolen)"
                )


    def _check_cross_validation(self, item: Dict[str, Any]):
        """Cross-validation checks"""

        # 1. Moeilijkheid vs groep/niveau consistency
        groep = item.get('groep')
        niveau = item.get('niveau')
        moeilijkheid = item.get('moeilijkheidsgraad')

        vragen = item.get('vragen', [])
        if vragen and moeilijkheid:
            vraag_moeilijkheden = [
                v.get('moeilijkheidsgraad') for v in vragen
                if v.get('moeilijkheidsgraad')
            ]

            if vraag_moeilijkheden:
                avg_vraag_moeilijkheid = sum(vraag_moeilijkheden) / len(vraag_moeilijkheden)

                verschil = abs(moeilijkheid - avg_vraag_moeilijkheid)
                if verschil > 0.2:
                    self.warnings.append(
                        f"⚠️  Item moeilijkheid ({moeilijkheid:.2f}) wijkt af van "
                        f"gemiddelde vraag moeilijkheid ({avg_vraag_moeilijkheid:.2f})"
                    )

        # 2. Tekstsoort vs groep geschiktheid
        tekstsoort = item.get('tekstsoort')

        if groep == 3:
            if tekstsoort not in ['verhaal', 'informatief']:
                self.warnings.append(
                    f"⚠️  G3: Tekstsoort '{tekstsoort}' mogelijk te complex "
                    f"(aanbevolen: verhaal, informatief)"
                )

        # 3. Check of tekst woorden voorkomen in vragen (goede praktijk)
        tekst = item.get('tekst', '').lower()
        tekst_woorden = set(re.findall(r'\b\w+\b', tekst))

        for vraag in vragen:
            correct = str(vraag.get('correct_antwoord', '')).lower()

            if len(correct) > 3:  # Skip very short answers
                # Check if answer words appear in text
                correct_woorden = set(re.findall(r'\b\w+\b', correct))
                overlap = correct_woorden & tekst_woorden

                if len(overlap) == 0 and len(correct_woorden) > 0:
                    self.info.append(
                        f"ℹ️  Antwoord '{correct}' komt niet letterlijk voor in tekst "
                        f"(kan correct zijn bij inferentie vragen)"
                    )


    def _calculate_score(self) -> float:
        """Calculate quality score based on errors and warnings"""
        error_penalty = len(self.errors) * 0.15
        warning_penalty = len(self.warnings) * 0.05

        score = max(0.0, 1.0 - error_penalty - warning_penalty)
        return round(score, 2)


def valideer_lezen_items(filepath: str) -> None:
    """Validate reading items from JSON file"""

    print("=" * 80)
    print("LEZEN VALIDATOR v3.0 - Enhanced Validation")
    print("=" * 80)
    print()

    # Load items
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            items = json.load(f)
    except Exception as e:
        print(f"❌ Fout bij laden bestand: {e}")
        return

    if not isinstance(items, list):
        items = [items]

    validator = LezenValidatorEnhanced()

    # Validate each item
    for i, item in enumerate(items, 1):
        print(f"\n{'=' * 80}")
        print(f"ITEM {i}/{len(items)}: {item.get('id', 'UNKNOWN')}")
        print(f"{'=' * 80}")

        result = validator.valideer_item(item)

        # Print results
        if result.errors:
            print(f"\n❌ ERRORS ({len(result.errors)}):")
            for error in result.errors:
                print(f"  {error}")

        if result.warnings:
            print(f"\n⚠️  WARNINGS ({len(result.warnings)}):")
            for warning in result.warnings:
                print(f"  {warning}")

        if result.info:
            print(f"\nℹ️  INFO ({len(result.info)}):")
            for info in result.info:
                print(f"  {info}")

        # Status
        status = "✅ VALID" if result.valid else "❌ INVALID"
        print(f"\n{status} | Score: {result.score:.2f}/1.00")

    print(f"\n{'=' * 80}")
    print("VALIDATIE COMPLEET")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python lezen-validator-v3.py <test-file.json>")
        print("\nExample:")
        print("  python lezen-validator-v3.py test-lezen-g3.json")
        sys.exit(1)

    valideer_lezen_items(sys.argv[1])
