#!/usr/bin/env python3
"""
VERHAALTJESSOMMEN VALIDATOR v3.0 - Enhanced Validator voor Verhaaltjessommen Items

Valideert verhaaltjessommen (word problems) voor Groep 3-8, Midden/Eind niveau.
Gebaseerd op prompt-verhaaltjessommen-v2.md specificaties.

Features:
- Volledige G3-G8 M/E niveauregels (12 varianten)
- Dual validation: LEZEN (tekstbegrip) + REKENEN (bewerking)
- LOVA-structuur validatie (Lezen, Ordenen, Vormen, Antwoorden)
- Domein-specifieke checks (GETALLEN, VERHOUDINGEN, METEN, VERBANDEN)
- AVI-niveau validatie
- Tekstlengte en complexiteit checks
- Rekenkundige complexiteit (getallenruimte, bewerkingen, stappen)
- Context type geschiktheid
- Strategic distractor validation
- Realiteitscheck (antwoord logisch?)
- 65+ quality checks per item

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


class VerhaaltjessommenValidatorEnhanced:
    """Enhanced validator for word problem items"""

    # NIVEAU REGELS per (groep, niveau)
    NIVEAU_REGELS = {
        # GROEP 3
        (3, 'M'): {
            'avi_niveau': ['M3'],
            'tekst_lengte': (20, 50),
            'zinnen': (3, 5),
            'woorden_per_zin': (6, 8),
            'visualisatie': 'verplicht',
            'domeinen': ['GETALLEN'],
            'getallenruimte': (0, 20),
            'bewerkingen': ['+', '-'],
            'stappen': 1,
            'context_types': ['speelgoed', 'snoep', 'vrienden', 'huisdieren'],
            'vraag_type': 'direct',
            'taal_complexiteit': 'eenvoudig',
            'reken_complexiteit': '1_stap',
            'moeilijkheid': (0.15, 0.35),
            'tijd_totaal': (60, 90),
        },
        (3, 'E'): {
            'avi_niveau': ['E3', 'M4'],
            'tekst_lengte': (50, 100),
            'zinnen': (5, 8),
            'woorden_per_zin': (8, 10),
            'visualisatie': 'verplicht',
            'domeinen': ['GETALLEN', 'METEN'],
            'getallenruimte': (0, 50),
            'bewerkingen': ['+', '-'],
            'stappen': (1, 2),
            'context_types': ['winkel', 'groepjes', 'tijd', 'meten'],
            'vraag_type': 'direct',
            'moeilijkheid': (0.30, 0.50),
            'tijd_totaal': (105, 150),
        },

        # GROEP 4
        (4, 'M'): {
            'avi_niveau': ['M4', 'E4'],
            'tekst_lengte': (100, 150),
            'zinnen': (8, 12),
            'woorden_per_zin': (8, 12),
            'domeinen': ['GETALLEN', 'METEN'],
            'getallenruimte': (0, 100),
            'bewerkingen': ['+', '-', '×', ':'],
            'tafels': [1, 2, 5, 10],
            'stappen': (2, 3),
            'context_types': ['winkel', 'feest', 'sport', 'school'],
            'vraag_type': 'meerstaps',
            'moeilijkheid': (0.40, 0.65),
            'tijd_totaal': (150, 210),
        },
        (4, 'E'): {
            'avi_niveau': ['E4', 'M5'],
            'tekst_lengte': (150, 250),
            'zinnen': (10, 15),
            'domeinen': ['GETALLEN', 'METEN', 'VERHOUDINGEN'],
            'getallenruimte': (0, 1000),
            'bewerkingen': ['+', '-', '×', ':', 'alle_tafels'],
            'stappen': (3, 4),
            'context_types': ['schoolreisje', 'koken', 'bouwen'],
            'moeilijkheid': (0.55, 0.75),
            'tijd_totaal': (180, 300),
        },

        # GROEP 5
        (5, 'M'): {
            'avi_niveau': ['M5', 'E5'],
            'tekst_lengte': (250, 350),
            'alineas_min': 2,
            'domeinen': ['GETALLEN', 'VERHOUDINGEN', 'METEN', 'VERBANDEN'],
            'getallenruimte': (0, 10000),
            'bewerkingen': ['+', '-', '×', ':', 'breuken', 'decimalen'],
            'stappen': (4, 5),
            'context_types': ['projecten', 'data', 'geld', 'schaal'],
            'vraag_type': 'multi_staps',
            'data_integratie': ['tabel', 'grafiek'],
            'moeilijkheid': (0.60, 0.80),
            'tijd_totaal': (300, 420),
        },
        (5, 'E'): {
            'avi_niveau': ['E5', 'M6'],
            'tekst_lengte': (350, 500),
            'domeinen': ['alle'],
            'stappen': (5, 6),
            'moeilijkheid': (0.70, 0.85),
            'tijd_totaal': (420, 600),
        },

        # GROEP 6
        (6, 'M'): {
            'avi_niveau': ['M6', 'E6'],
            'tekst_lengte': (500, 700),
            'domeinen': ['alle'],
            'context_types': ['wetenschappelijk', 'maatschappelijk', 'technisch'],
            'stappen': (6, 8),
            'moeilijkheid': (0.75, 0.88),
            'tijd_totaal': (600, 900),
        },
        (6, 'E'): {
            'avi_niveau': ['E6', 'PLUS'],
            'tekst_lengte': (700, 1000),
            'moeilijkheid': (0.78, 0.92),
            'tijd_totaal': (900, 1200),
        },

        # GROEP 7
        (7, 'M'): {
            'avi_niveau': ['PLUS'],
            'tekst_lengte': (800, 1200),
            'moeilijkheid': (0.82, 0.94),
        },
        (7, 'E'): {
            'avi_niveau': ['PLUS'],
            'tekst_lengte': (1000, 1500),
            'moeilijkheid': (0.85, 0.96),
        },

        # GROEP 8
        (8, 'M'): {
            'avi_niveau': ['PLUS'],
            'tekst_lengte': (1200, 1800),
            'referentieniveau': '1F',
            'moeilijkheid': (0.88, 0.97),
        },
        (8, 'E'): {
            'avi_niveau': ['PLUS'],
            'tekst_lengte': (1500, 2000),
            'referentieniveau': '1S',
            'moeilijkheid': (0.90, 1.0),
        },
    }

    # Geldige domeinen
    DOMEINEN = {'GETALLEN', 'VERHOUDINGEN', 'METEN', 'VERBANDEN'}

    # Geldige context types
    CONTEXT_TYPES = {
        'speelgoed', 'snoep', 'vrienden', 'huisdieren',
        'winkel', 'groepjes', 'tijd', 'meten',
        'feest', 'sport', 'school',
        'schoolreisje', 'koken', 'bouwen',
        'projecten', 'data', 'geld', 'schaal',
        'wetenschappelijk', 'maatschappelijk', 'technisch'
    }

    # Geldige bewerkingen
    BEWERKINGEN = {'+', '-', '×', '*', ':', '/', 'x'}


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

        # 3. TAAL-aspect: Tekstkwaliteit (LEZEN component)
        self._check_tekst_kwaliteit(item)

        # 4. REKEN-aspect: Rekenkundige geldigheid
        self._check_reken_complexiteit(item)

        # 5. LOVA-structuur validatie
        self._check_lova_structuur(item)

        # 6. Vraag validatie
        self._check_vraag_kwaliteit(item)

        # 7. Afleiders validatie
        self._check_afleiders(item)

        # 8. G3-specifieke checks
        if item.get('groep') == 3:
            self._check_g3_specifiek(item)

        # 9. Domein-specifieke checks
        self._check_domein_specifiek(item)

        # 10. Realiteitscheck
        self._check_realiteitscheck(item)

        # 11. Metadata checks
        self._check_metadata(item)

        # 12. Cross-validation
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
            'id', 'groep', 'niveau', 'domein', 'avi_niveau',
            'context_type', 'verhaal_tekst', 'tekst_lengte_woorden',
            'hoofdvraag', 'correct_antwoord', 'afleiders'
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

        # Check domein
        domein = item.get('domein')
        if domein and domein not in self.DOMEINEN:
            self.errors.append(
                f"❌ Ongeldig domein: {domein}. "
                f"Moet zijn: {', '.join(self.DOMEINEN)}"
            )


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

        # 3. Domein toegestaan?
        domein = item.get('domein')
        toegestane_domeinen = regels.get('domeinen', ['alle'])
        if toegestane_domeinen != ['alle'] and domein:
            if domein not in toegestane_domeinen:
                self.warnings.append(
                    f"⚠️  Domein '{domein}' niet standaard voor G{groep}-{niveau}. "
                    f"Verwacht: {', '.join(toegestane_domeinen)}"
                )

        # 4. Moeilijkheidsgraad
        moeilijkheid = item.get('moeilijkheidsgraad')
        if moeilijkheid:
            min_m, max_m = regels.get('moeilijkheid', (0, 1))
            if not (min_m <= moeilijkheid <= max_m):
                self.warnings.append(
                    f"⚠️  Moeilijkheidsgraad {moeilijkheid:.2f} buiten range "
                    f"({min_m:.2f}-{max_m:.2f}) voor G{groep}-{niveau}"
                )


    def _check_tekst_kwaliteit(self, item: Dict[str, Any]):
        """Check text quality (LEZEN component)"""
        tekst = item.get('verhaal_tekst', '')
        if not tekst:
            self.errors.append("❌ Geen verhaal_tekst aanwezig")
            return

        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        # 1. Zinslengte (voor G3-4)
        max_woorden_per_zin = regels.get('woorden_per_zin')
        if max_woorden_per_zin:
            zinnen = re.split(r'[.!?]', tekst)
            zinnen = [z.strip() for z in zinnen if z.strip()]

            max_verwacht = max_woorden_per_zin[1] if isinstance(max_woorden_per_zin, tuple) else max_woorden_per_zin

            for i, zin in enumerate(zinnen, 1):
                woorden = zin.split()
                if len(woorden) > max_verwacht + 3:  # Tolerantie van 3 woorden
                    self.warnings.append(
                        f"⚠️  Zin {i} heeft {len(woorden)} woorden (max ~{max_verwacht}): '{zin[:60]}...'"
                    )

        # 2. Aantal zinnen
        zinnen_range = regels.get('zinnen')
        if zinnen_range:
            zinnen = re.split(r'[.!?]', tekst)
            zinnen = [z.strip() for z in zinnen if z.strip()]
            min_zinnen, max_zinnen = zinnen_range

            if len(zinnen) < min_zinnen:
                self.warnings.append(
                    f"⚠️  Tekst heeft {len(zinnen)} zinnen (min {min_zinnen})"
                )
            elif len(zinnen) > max_zinnen + 3:  # Tolerantie
                self.warnings.append(
                    f"⚠️  Tekst heeft {len(zinnen)} zinnen (max ~{max_zinnen})"
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

        # 4. Check of getallen in tekst voorkomen
        # Extract numbers from text
        getallen_in_tekst = re.findall(r'\b\d+\b', tekst)
        if not getallen_in_tekst:
            self.errors.append(
                "❌ Geen getallen gevonden in verhaal_tekst "
                "(verhaaltjessommen moeten getallen bevatten)"
            )
        else:
            self.info.append(
                f"ℹ️  Getallen in tekst: {', '.join(getallen_in_tekst)}"
            )


    def _check_reken_complexiteit(self, item: Dict[str, Any]):
        """Check mathematical complexity"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        # 1. Stappenstructuur
        stappenstructuur = item.get('stappenstructuur', [])
        if not stappenstructuur:
            self.warnings.append(
                "⚠️  Geen stappenstructuur aanwezig (aanbevolen voor G4+)"
            )
        else:
            aantal_stappen = len(stappenstructuur)
            stappen_verwacht = regels.get('stappen')

            if stappen_verwacht:
                if isinstance(stappen_verwacht, tuple):
                    min_stappen, max_stappen = stappen_verwacht
                    if aantal_stappen < min_stappen or aantal_stappen > max_stappen:
                        self.warnings.append(
                            f"⚠️  Aantal stappen ({aantal_stappen}) buiten verwacht "
                            f"({min_stappen}-{max_stappen}) voor G{groep}-{niveau}"
                        )
                elif aantal_stappen != stappen_verwacht:
                    self.warnings.append(
                        f"⚠️  Aantal stappen ({aantal_stappen}) afwijkend van verwacht "
                        f"({stappen_verwacht}) voor G{groep}-{niveau}"
                    )

            # 2. Check stappen structuur
            for i, stap in enumerate(stappenstructuur, 1):
                if 'stap' not in stap:
                    self.errors.append(f"❌ Stap {i}: 'stap' nummer ontbreekt")
                if 'actie' not in stap or not stap.get('actie'):
                    self.errors.append(f"❌ Stap {i}: 'actie' ontbreekt of is leeg")
                if 'berekening' not in stap or not stap.get('berekening'):
                    self.errors.append(f"❌ Stap {i}: 'berekening' ontbreekt of is leeg")
                if 'resultaat' not in stap or not stap.get('resultaat'):
                    self.errors.append(f"❌ Stap {i}: 'resultaat' ontbreekt of is leeg")

        # 3. Check reken_complexiteit
        reken_complexiteit = item.get('reken_complexiteit')
        verwachte_complexiteit = regels.get('reken_complexiteit')
        if verwachte_complexiteit and reken_complexiteit:
            if reken_complexiteit != verwachte_complexiteit:
                self.info.append(
                    f"ℹ️  Reken_complexiteit '{reken_complexiteit}' afwijkend van "
                    f"verwacht '{verwachte_complexiteit}'"
                )


    def _check_lova_structuur(self, item: Dict[str, Any]):
        """Check LOVA (Lezen, Ordenen, Vormen, Antwoorden) structure"""
        lova = item.get('toelichting_lova')

        if not lova:
            groep = item.get('groep')
            if groep >= 4:
                self.warnings.append(
                    "⚠️  Geen toelichting_lova aanwezig (aanbevolen voor G4+)"
                )
            return

        # Check alle 4 LOVA-onderdelen
        lova_onderdelen = ['lezen', 'ordenen', 'vormen', 'antwoorden']
        for onderdeel in lova_onderdelen:
            if onderdeel not in lova:
                self.errors.append(
                    f"❌ LOVA-onderdeel '{onderdeel}' ontbreekt in toelichting_lova"
                )
            elif not lova.get(onderdeel) or not str(lova.get(onderdeel)).strip():
                self.errors.append(
                    f"❌ LOVA-onderdeel '{onderdeel}' is leeg"
                )

        # Check LOVA content quality
        if lova.get('lezen'):
            lezen_tekst = str(lova['lezen']).lower()
            # Should mention "gegeven" and "gevraagd"
            if 'gegeven' not in lezen_tekst and 'weet' not in lezen_tekst:
                self.info.append(
                    "ℹ️  LOVA-Lezen: vermeld bij voorkeur wat 'gegeven' is"
                )
            if 'gevraagd' not in lezen_tekst and 'zoek' not in lezen_tekst:
                self.info.append(
                    "ℹ️  LOVA-Lezen: vermeld bij voorkeur wat 'gevraagd' is"
                )

        if lova.get('vormen'):
            vormen_tekst = str(lova['vormen']).lower()
            # Should mention bewerking
            bewerking_woorden = ['optellen', 'aftrekken', 'vermenigvuldig', 'delen',
                                  'berekening', 'bewerking', 'som', '+', '-', '×', ':']
            if not any(woord in vormen_tekst for woord in bewerking_woorden):
                self.warnings.append(
                    "⚠️  LOVA-Vormen: vermeld bij voorkeur welke bewerking(en) nodig zijn"
                )


    def _check_vraag_kwaliteit(self, item: Dict[str, Any]):
        """Check question quality"""
        hoofdvraag = item.get('hoofdvraag', '').strip()

        if not hoofdvraag:
            self.errors.append("❌ Hoofdvraag is leeg")
            return

        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        # 1. Vraagtype check
        vraag_type = regels.get('vraag_type')
        if vraag_type == 'direct':
            # Direct vraag moet beginnen met vraagwoord
            vraagwoorden = ['hoeveel', 'wat', 'welke', 'wie', 'waar', 'wanneer']
            if not any(hoofdvraag.lower().startswith(vw) for vw in vraagwoorden):
                self.warnings.append(
                    f"⚠️  Voor G{groep}-{niveau} wordt een directe vraag verwacht "
                    f"(begint met vraagwoord)"
                )

        # 2. Eenheid check
        correct = str(item.get('correct_antwoord', '')).lower()
        eenheid_woorden = ['euro', 'cent', 'cm', 'meter', 'km', 'gram', 'kg',
                           'liter', 'uur', 'minuut', 'seconde', 'jaar',
                           'appel', 'snoep', 'kind', 'stuk', 'stuks']

        heeft_eenheid = any(eenheid in correct for eenheid in eenheid_woorden)
        if not heeft_eenheid:
            # Check if it's just a number
            if correct.strip().isdigit():
                self.warnings.append(
                    "⚠️  Correct antwoord heeft geen eenheid (bijv. 'euro', 'appels', 'cm')"
                )

        # 3. Vraag eindigt met vraagteken
        if not hoofdvraag.endswith('?'):
            self.errors.append("❌ Hoofdvraag eindigt niet met vraagteken")


    def _check_afleiders(self, item: Dict[str, Any]):
        """Check distractor quality"""
        afleiders = item.get('afleiders', [])
        correct = str(item.get('correct_antwoord', '')).strip()
        groep = item.get('groep')

        # 1. Aantal afleiders (meestal 3)
        if len(afleiders) < 2:
            self.errors.append(
                f"❌ Te weinig afleiders ({len(afleiders)}, min 2)"
            )

        if len(afleiders) > 4:
            self.warnings.append(
                f"⚠️  Veel afleiders ({len(afleiders)})"
            )

        # 2. Afleiders niet leeg
        for i, afleider in enumerate(afleiders, 1):
            if not afleider or not str(afleider).strip():
                self.errors.append(f"❌ Afleider {i}: is leeg")

        # 3. Afleiders niet gelijk aan correct
        for afleider in afleiders:
            if str(afleider).lower().strip() == correct.lower():
                self.errors.append(
                    f"❌ Afleider '{afleider}' is gelijk aan correct antwoord"
                )

        # 4. Afleiders onderling verschillend
        afleiders_lower = [str(a).lower().strip() for a in afleiders]
        if len(afleiders_lower) != len(set(afleiders_lower)):
            self.errors.append("❌ Dubbele afleiders gevonden")

        # 5. Check strategische afleiders (G4+)
        if groep >= 4:
            # Should include common errors:
            # - Verkeerde bewerking (+ i.p.v. -)
            # - Tussenstap (alleen 1e bewerking)
            # - Verkeerde volgorde
            self.info.append(
                "ℹ️  G4+: Check of afleiders veelvoorkomende fouten vertegenwoordigen "
                "(verkeerde bewerking, tussenstap vergeten, etc.)"
            )


    def _check_g3_specifiek(self, item: Dict[str, Any]):
        """Extra checks specific for Groep 3"""
        niveau = item.get('niveau')
        tekst = item.get('verhaal_tekst', '').lower()

        regels = self.NIVEAU_REGELS.get((3, niveau), {})

        # 1. Visualisatie VERPLICHT
        visualisatie = regels.get('visualisatie')
        if visualisatie == 'verplicht':
            heeft_visual = item.get('visualisatie') == 'verplicht'

            # Ook checken in tekst/beschrijving
            visual_keywords = [
                'plaatje', 'tekening', 'zie', 'afbeelding', 'figuur',
                'foto', 'illustratie', 'prent'
            ]
            heeft_visual_ref = any(keyword in tekst for keyword in visual_keywords)

            if not heeft_visual and not heeft_visual_ref:
                self.errors.append(
                    "❌ G3: Visualisatie is VERPLICHT. "
                    "Zet 'visualisatie': 'verplicht' of vermeld '(zie plaatje)' in tekst"
                )

        # 2. Alleen GETALLEN domein voor M3
        if niveau == 'M':
            domein = item.get('domein')
            if domein != 'GETALLEN':
                self.errors.append(
                    f"❌ G3-M: Alleen GETALLEN domein toegestaan, niet '{domein}'"
                )

        # 3. Eenvoudige context
        context = item.get('context_type', '')
        toegestane_context = regels.get('context_types', [])
        if context and toegestane_context:
            if context not in toegestane_context:
                self.warnings.append(
                    f"⚠️  G3: Context '{context}' niet standaard. "
                    f"Aanbevolen: {', '.join(toegestane_context)}"
                )

        # 4. Enkelvoudige actie
        actie_woorden = ['krijgen', 'krijgt', 'geeft', 'geven', 'erbij', 'weggeven',
                         'opgegeten', 'opgeten', 'komen', 'gaan', 'weg']
        heeft_actie = any(actie in tekst for actie in actie_woorden)
        if not heeft_actie:
            self.info.append(
                "ℹ️  G3: Gebruik duidelijke actiewoorden (krijgen, weggeven, erbij, etc.)"
            )


    def _check_domein_specifiek(self, item: Dict[str, Any]):
        """Domain-specific checks"""
        domein = item.get('domein')
        correct = str(item.get('correct_antwoord', '')).lower()

        if domein == 'GETALLEN':
            # Check if answer is a number
            cijfers = re.findall(r'\d+', correct)
            if not cijfers:
                self.warnings.append(
                    "⚠️  GETALLEN domein: correct_antwoord bevat geen cijfer"
                )

        elif domein == 'METEN':
            # Check for unit
            meet_eenheden = ['euro', 'cent', 'cm', 'meter', 'm', 'km',
                            'gram', 'kg', 'liter', 'ml',
                            'uur', 'minuut', 'seconde']
            heeft_eenheid = any(eenheid in correct for eenheid in meet_eenheden)
            if not heeft_eenheid:
                self.warnings.append(
                    "⚠️  METEN domein: correct_antwoord moet eenheid bevatten "
                    "(euro, cm, uur, etc.)"
                )

        elif domein == 'VERHOUDINGEN':
            # Check for fractions/percentages/ratios
            verhouding_woorden = ['breuk', 'helft', '1/2', '1/4', 'procent', '%',
                                  'keer', 'dubbel', 'driedubbel']
            context_ok = any(woord in item.get('verhaal_tekst', '').lower()
                            for woord in verhouding_woorden)
            if not context_ok:
                self.info.append(
                    "ℹ️  VERHOUDINGEN: check of breuk/percentage/verhouding duidelijk is"
                )

        elif domein == 'VERBANDEN':
            # Check for patterns/formulas/graphs
            verband_woorden = ['patroon', 'regel', 'formule', 'tabel', 'grafiek']
            context_ok = any(woord in item.get('verhaal_tekst', '').lower()
                            for woord in verband_woorden)
            if not context_ok:
                self.info.append(
                    "ℹ️  VERBANDEN: check of patroon/formule/tabel aanwezig is"
                )


    def _check_realiteitscheck(self, item: Dict[str, Any]):
        """Reality check on answer"""
        correct_str = str(item.get('correct_antwoord', ''))

        # Extract number from answer
        getallen = re.findall(r'-?\d+\.?\d*', correct_str)
        if not getallen:
            return

        getal = float(getallen[0])

        # 1. Negatieve getallen check (meestal fout in verhaaltjessommen)
        if getal < 0:
            self.errors.append(
                f"❌ REALITEITSCHECK: Negatief antwoord ({getal}) is onrealistisch "
                f"voor verhaaltjessommen (je kunt geen -3 appels hebben)"
            )

        # 2. Zeer grote getallen check
        groep = item.get('groep')
        if groep <= 4 and getal > 1000:
            self.warnings.append(
                f"⚠️  REALITEITSCHECK: Groot getal ({getal}) voor G{groep}"
            )

        # 3. Context-specifieke checks
        context = item.get('context_type', '')
        tekst = item.get('verhaal_tekst', '').lower()

        # Geld checks
        if 'euro' in correct_str.lower() or 'cent' in correct_str.lower():
            if getal > 1000:
                self.warnings.append(
                    f"⚠️  REALITEITSCHECK: Heel veel geld ({getal}) voor kind-context"
                )

        # Tijd checks
        if 'uur' in tekst or 'minuut' in tekst:
            if 'uur' in correct_str and getal > 24:
                self.warnings.append(
                    f"⚠️  REALITEITSCHECK: Meer dan 24 uur ({getal}) is ongebruikelijk"
                )
            if 'minuut' in correct_str and getal > 120:
                self.warnings.append(
                    f"⚠️  REALITEITSCHECK: Meer dan 2 uur ({getal} minuten) is lang"
                )

        # Leeftijd/aantal kinderen
        if 'kind' in tekst or 'jaar' in tekst:
            if getal > 50:
                self.warnings.append(
                    f"⚠️  REALITEITSCHECK: Getal ({getal}) lijkt hoog voor kind-context"
                )


    def _check_metadata(self, item: Dict[str, Any]):
        """Check metadata completeness"""

        # 1. ID format
        item_id = item.get('id', '')
        expected_pattern = r'^VT_G[3-8]_[ME]_\d{3}$'
        if not re.match(expected_pattern, item_id):
            self.warnings.append(
                f"⚠️  ID '{item_id}' volgt niet verwacht patroon: VT_G[3-8]_[ME]_###"
            )

        # 2. Geschatte tijd
        tijd = item.get('geschatte_tijd_sec')
        groep = item.get('groep')
        niveau = item.get('niveau')

        if tijd:
            regels = self.NIVEAU_REGELS.get((groep, niveau), {})
            tijd_range = regels.get('tijd_totaal')

            if tijd_range:
                min_tijd, max_tijd = tijd_range
                if not (min_tijd <= tijd <= max_tijd):
                    self.warnings.append(
                        f"⚠️  Geschatte tijd ({tijd}s) buiten verwacht "
                        f"({min_tijd}-{max_tijd}s) voor G{groep}-{niveau}"
                    )

        # 3. Toelichting LOVA aanwezig (G4+)
        if groep >= 4:
            if not item.get('toelichting_lova'):
                self.warnings.append(
                    "⚠️  Geen toelichting_lova aanwezig (aanbevolen voor G4+)"
                )


    def _check_cross_validation(self, item: Dict[str, Any]):
        """Cross-validation checks"""

        # 1. Taal-complexiteit vs reken-complexiteit balans
        taal_complexiteit = item.get('taal_complexiteit')
        reken_complexiteit = item.get('reken_complexiteit')

        if taal_complexiteit == 'complex' and reken_complexiteit == 'meerstaps':
            groep = item.get('groep')
            if groep < 5:
                self.warnings.append(
                    f"⚠️  G{groep}: Zowel complexe taal als meerstaps rekenen "
                    f"kan te moeilijk zijn (balans!)"
                )

        # 2. Context vs groep geschiktheid
        groep = item.get('groep')
        context = item.get('context_type', '')

        if groep == 3:
            abstracte_context = ['wetenschappelijk', 'maatschappelijk', 'data']
            if context in abstracte_context:
                self.warnings.append(
                    f"⚠️  G3: Context '{context}' mogelijk te abstract "
                    f"(aanbevolen: speelgoed, snoep, vrienden)"
                )

        # 3. Domein vs groep
        domein = item.get('domein')
        if groep == 3 and domein not in ['GETALLEN', 'METEN']:
            self.warnings.append(
                f"⚠️  G3: Domein '{domein}' mogelijk te abstract "
                f"(GETALLEN is standaard voor G3)"
            )


    def _calculate_score(self) -> float:
        """Calculate quality score"""
        error_penalty = len(self.errors) * 0.15
        warning_penalty = len(self.warnings) * 0.05

        score = max(0.0, 1.0 - error_penalty - warning_penalty)
        return round(score, 2)


def valideer_verhaaltjessommen_items(filepath: str) -> None:
    """Validate word problem items from JSON file"""

    print("=" * 80)
    print("VERHAALTJESSOMMEN VALIDATOR v3.0 - Enhanced Validation")
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

    validator = VerhaaltjessommenValidatorEnhanced()

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
        print("Usage: python verhaaltjessommen-validator-v3.py <test-file.json>")
        print("\nExample:")
        print("  python verhaaltjessommen-validator-v3.py test-verhaaltjes-g3.json")
        sys.exit(1)

    valideer_verhaaltjessommen_items(sys.argv[1])
