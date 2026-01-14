#!/usr/bin/env python3
"""
WOORDENSCHAT VALIDATOR v3.0 - Enhanced Validator voor Woordenschat Items

Valideert woordenschat items voor Groep 3-8, Midden/Eind niveau.
Gebaseerd op prompt-woordenschat-v2.md specificaties.

Features:
- Volledige G3-G8 M/E niveauregels (12 varianten)
- Receptief vs. productief validatie
- Woordfrequentie checks (hoogfrequent → laagfrequent)
- Woordcategorie validatie (concreet → abstract)
- Woordrelaties validatie (synoniemen, antoniemen, etc.)
- Item type validatie
- Strategie validatie (plaatje, context, woorddelen, relaties)
- G3-specifieke checks (concreet, visueel, hoogfrequent)
- Figuurlijk taalgebruik checks (G4-E+)
- Strategic distractor validation
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


class WoordenschatValidatorEnhanced:
    """Enhanced validator for vocabulary items"""

    # NIVEAU REGELS per (groep, niveau)
    NIVEAU_REGELS = {
        # GROEP 3
        (3, 'M'): {
            'woordenschat_omvang_receptief': (800, 1500),
            'woordenschat_omvang_productief': (500, 1000),
            'woordfrequentie': 'hoogfrequent_500',
            'woordcategorieen': ['concreet_znw', 'werkwoord_actie', 'bijvoeglijk_basis', 'voorzetsels'],
            'item_types': ['meerkeuze_plaatje', 'plaatje_woord', 'categoriseren'],
            'strategieen': ['plaatje', 'ervaring'],
            'abstract': False,
            'figuurlijk': False,
            'moeilijkheid': (0.10, 0.30),
            'tijd_per_item': (15, 30),
        },
        (3, 'E'): {
            'woordenschat_omvang_receptief': (1200, 1500),
            'woordenschat_omvang_productief': (800, 1000),
            'woordfrequentie': 'hoogfrequent_1000',
            'woordcategorieen': ['concreet_znw', 'emoties_basis', 'tijd', 'samenstellingen_2delig'],
            'item_types': ['synoniemen_basis', 'categoriseren', 'context_zinsvervollend'],
            'strategieen': ['plaatje', 'context', 'woorddelen_herkennen'],
            'abstract': False,
            'figuurlijk': False,
            'moeilijkheid': (0.25, 0.45),
            'tijd_per_item': (20, 40),
        },

        # GROEP 4
        (4, 'M'): {
            'woordenschat_omvang_receptief': (2500, 3000),
            'woordenschat_omvang_productief': (1500, 2000),
            'woordfrequentie': 'top_2000',
            'woordcategorieen': ['abstract_introductie', 'vaktaal_basis', 'samenstellingen_3delig', 'afleidingen'],
            'item_types': ['synoniemen', 'antoniemen', 'woorddelen', 'vaktaal', 'meerdere_betekenissen'],
            'strategieen': ['woorddelen_herkennen', 'context', 'vervangen'],
            'abstract': 'introductie',
            'figuurlijk': False,
            'moeilijkheid': (0.35, 0.60),
            'tijd_per_item': (30, 50),
        },
        (4, 'E'): {
            'woordenschat_omvang_receptief': (3500, 4000),
            'woordenschat_omvang_productief': (2500, 3000),
            'woordfrequentie': 'top_3000',
            'woordcategorieen': ['figuurlijk_introductie', 'vaktaal_uitgebreid', 'leenwoorden_introductie'],
            'item_types': ['figuurlijk_letterlijk', 'meerdere_betekenissen_context', 'vaktaal'],
            'strategieen': ['context', 'woorddelen', 'relaties'],
            'abstract': 'basis',
            'figuurlijk': 'introductie',
            'moeilijkheid': (0.50, 0.70),
            'tijd_per_item': (40, 60),
        },

        # GROEP 5
        (5, 'M'): {
            'woordenschat_omvang_receptief': (5000, 6000),
            'woordenschat_omvang_productief': (3500, 4500),
            'woordfrequentie': 'top_5000',
            'woordcategorieen': ['abstract_complex', 'vaktaal_gevorderd', 'figuurlijk', 'woordvorming_complex'],
            'item_types': ['connotatie', 'figuurlijk_uitleggen', 'vaktaal_definieren', 'register'],
            'strategieen': ['etymologie_basis', 'morfologische_analyse', 'context_woorddelen'],
            'abstract': 'gevorderd',
            'figuurlijk': 'gevorderd',
            'moeilijkheid': (0.55, 0.75),
            'tijd_per_item': (50, 70),
        },
        (5, 'E'): {
            'woordenschat_omvang_receptief': (7000, 8000),
            'woordenschat_omvang_productief': (5000, 6000),
            'woordfrequentie': 'top_7000',
            'woordcategorieen': ['wetenschappelijk', 'klassiek', 'technisch'],
            'moeilijkheid': (0.65, 0.82),
            'tijd_per_item': (60, 80),
        },

        # GROEP 6
        (6, 'M'): {
            'woordenschat_omvang_receptief': (10000, 12000),
            'woordenschat_omvang_productief': (7000, 8000),
            'woordfrequentie': 'top_10000',
            'woordcategorieen': ['academisch', 'retorisch', 'idiomatisch'],
            'item_types': ['retorisch_middel', 'academisch', 'register', 'betekenisnuances'],
            'abstract': 'volledig',
            'figuurlijk': 'volledig',
            'moeilijkheid': (0.70, 0.87),
            'tijd_per_item': (60, 90),
        },
        (6, 'E'): {
            'woordenschat_omvang_receptief': (13000, 15000),
            'woordenschat_omvang_productief': (9000, 11000),
            'moeilijkheid': (0.75, 0.90),
            'tijd_per_item': (70, 100),
        },

        # GROEP 7
        (7, 'M'): {
            'woordenschat_omvang_receptief': (16000, 18000),
            'woordenschat_omvang_productief': (12000, 14000),
            'woordcategorieen': ['specialistisch', 'filosofisch', 'maatschappelijk'],
            'moeilijkheid': (0.78, 0.92),
            'tijd_per_item': (70, 100),
        },
        (7, 'E'): {
            'woordenschat_omvang_receptief': (20000, 999999),
            'woordenschat_omvang_productief': (15000, 999999),
            'moeilijkheid': (0.82, 0.95),
            'tijd_per_item': (80, 110),
        },

        # GROEP 8
        (8, 'M'): {
            'referentieniveau': '1F',
            'moeilijkheid': (0.85, 0.96),
            'tijd_per_item': (80, 120),
        },
        (8, 'E'): {
            'referentieniveau': '1S',
            'moeilijkheid': (0.88, 1.0),
            'tijd_per_item': (90, 130),
        },
    }

    # Hoogfrequente woorden G3 (top 100)
    HOOGFREQUENT_G3 = {
        'de', 'het', 'een', 'en', 'van', 'in', 'is', 'op', 'te', 'dat',
        'ik', 'jij', 'hij', 'zij', 'wij', 'ze', 'hun',
        'mama', 'papa', 'oma', 'opa', 'kind', 'school', 'huis',
        'kat', 'hond', 'vis', 'muis', 'boom', 'auto', 'bal', 'boek',
        'appel', 'peer', 'rood', 'blauw', 'groen', 'geel', 'groot', 'klein',
        'spelen', 'eten', 'drinken', 'slapen', 'lopen', 'zitten', 'staan',
    }

    # Geldige woordcategorieën
    WOORDCATEGORIEEN = {
        'concreet_znw', 'abstract_znw', 'werkwoord', 'werkwoord_actie',
        'bijvoeglijk', 'bijvoeglijk_basis', 'voorzetsels', 'voornaamwoorden',
        'emoties_basis', 'emoties_complex', 'tijd', 'verhoudingen',
        'samenstellingen_2delig', 'samenstellingen_3delig',
        'afleidingen', 'vaktaal', 'vaktaal_basis', 'vaktaal_uitgebreid', 'vaktaal_gevorderd',
        'figuurlijk', 'figuurlijk_introductie',
        'leenwoorden', 'leenwoorden_introductie',
        'abstract_introductie', 'abstract_complex',
        'woordvorming_complex', 'wetenschappelijk', 'klassiek', 'technisch',
        'academisch', 'retorisch', 'idiomatisch',
        'specialistisch', 'filosofisch', 'maatschappelijk'
    }

    # Geldige item types
    ITEM_TYPES = {
        'meerkeuze', 'meerkeuze_plaatje', 'invullen', 'plaatje_woord',
        'synoniemen', 'synoniemen_basis', 'antoniemen',
        'context', 'context_zinsvervollend',
        'woorddelen', 'categoriseren',
        'figuurlijk_letterlijk', 'figuurlijk_uitleggen', 'uitdrukking',
        'meerdere_betekenissen', 'meerdere_betekenissen_context',
        'vaktaal', 'vaktaal_definieren',
        'connotatie', 'register',
        'retorisch_middel', 'academisch', 'betekenisnuances'
    }

    # Geldige strategieën
    STRATEGIEEN = {
        'plaatje', 'context', 'woorddelen', 'relaties', 'ervaring',
        'woorddelen_herkennen', 'vervangen',
        'etymologie_basis', 'morfologische_analyse', 'context_woorddelen',
        'figuurlijk', 'figuurlijk_context'
    }

    # Woordfrequentie niveaus
    WOORDFREQUENTIE = {
        'hoogfrequent', 'hoogfrequent_500', 'hoogfrequent_1000',
        'middenfrequent', 'top_2000', 'top_3000', 'top_5000', 'top_7000', 'top_10000',
        'laagfrequent', 'specialistisch'
    }


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

        # 3. Doelwoord validatie
        self._check_doelwoord_kwaliteit(item)

        # 4. Woordfrequentie validatie
        self._check_woordfrequentie(item)

        # 5. Item type validatie
        self._check_item_type(item)

        # 6. Vraag validatie
        self._check_vraag_kwaliteit(item)

        # 7. Afleiders validatie
        self._check_afleiders(item)

        # 8. G3-specifieke checks
        if item.get('groep') == 3:
            self._check_g3_specifiek(item)

        # 9. Figuurlijk taalgebruik (G4-E+)
        if item.get('groep') >= 4:
            self._check_figuurlijk_taalgebruik(item)

        # 10. Woordrelaties validatie
        self._check_woordrelaties(item)

        # 11. Context validatie
        self._check_context(item)

        # 12. Metadata checks
        self._check_metadata(item)

        # 13. Cross-validation
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
            'id', 'groep', 'niveau', 'woordenschat_type',
            'woordcategorie', 'item_type', 'doelwoord',
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

        # Check woordenschat_type
        ws_type = item.get('woordenschat_type')
        if ws_type not in ['receptief', 'productief']:
            self.errors.append(
                f"❌ Ongeldig woordenschat_type: {ws_type} (moet receptief of productief zijn)"
            )

        # Check woordcategorie
        categorie = item.get('woordcategorie')
        if categorie and categorie not in self.WOORDCATEGORIEEN:
            self.warnings.append(f"⚠️  Ongebruikelijke woordcategorie: {categorie}")

        # Check item_type
        item_type = item.get('item_type')
        if item_type and item_type not in self.ITEM_TYPES:
            self.warnings.append(f"⚠️  Ongebruikelijk item_type: {item_type}")


    def _check_niveau_regels(self, item: Dict[str, Any]):
        """Check niveau-specific rules"""
        groep = item.get('groep')
        niveau = item.get('niveau')

        regels = self.NIVEAU_REGELS.get((groep, niveau))
        if not regels:
            self.errors.append(f"❌ Geen regels voor G{groep}-{niveau}")
            return

        # 1. Woordfrequentie
        woordfrequentie = item.get('woordfrequentie')
        verwachte_frequentie = regels.get('woordfrequentie')
        if verwachte_frequentie and woordfrequentie:
            if woordfrequentie != verwachte_frequentie:
                # Check if it's within acceptable range
                if 'hoogfrequent' in verwachte_frequentie and 'laagfrequent' in woordfrequentie:
                    self.warnings.append(
                        f"⚠️  Woordfrequentie '{woordfrequentie}' niet passend voor G{groep}-{niveau}. "
                        f"Verwacht: {verwachte_frequentie}"
                    )

        # 2. Item types
        item_type = item.get('item_type')
        toegestane_types = regels.get('item_types', [])
        if toegestane_types and item_type:
            if item_type not in toegestane_types:
                self.info.append(
                    f"ℹ️  Item type '{item_type}' niet standaard voor G{groep}-{niveau}. "
                    f"Standaard: {', '.join(toegestane_types[:3])}..."
                )

        # 3. Abstract toegestaan?
        categorie = item.get('woordcategorie', '')
        abstract_niveau = regels.get('abstract', False)
        if 'abstract' in categorie:
            if abstract_niveau == False:
                self.errors.append(
                    f"❌ G{groep}-{niveau}: Abstract woorden NIET toegestaan. "
                    f"Gebruik concreet_znw."
                )
            elif abstract_niveau == 'introductie':
                self.info.append(
                    f"ℹ️  G{groep}-{niveau}: Abstract alleen bij introductie "
                    f"(eenvoudige abstracte begrippen)"
                )

        # 4. Figuurlijk toegestaan?
        figuurlijk_niveau = regels.get('figuurlijk', False)
        if 'figuurlijk' in categorie or item_type in ['figuurlijk_letterlijk', 'figuurlijk_uitleggen', 'uitdrukking']:
            if figuurlijk_niveau == False:
                self.errors.append(
                    f"❌ G{groep}-{niveau}: Figuurlijk taalgebruik NIET toegestaan"
                )

        # 5. Moeilijkheidsgraad
        moeilijkheid = item.get('moeilijkheidsgraad')
        if moeilijkheid:
            min_m, max_m = regels.get('moeilijkheid', (0, 1))
            if not (min_m <= moeilijkheid <= max_m):
                self.warnings.append(
                    f"⚠️  Moeilijkheidsgraad {moeilijkheid:.2f} buiten range "
                    f"({min_m:.2f}-{max_m:.2f}) voor G{groep}-{niveau}"
                )


    def _check_doelwoord_kwaliteit(self, item: Dict[str, Any]):
        """Check target word quality"""
        doelwoord = item.get('doelwoord', '').strip()

        if not doelwoord:
            self.errors.append("❌ Doelwoord is leeg")
            return

        # 1. Spelling check (basic)
        if not doelwoord.replace(' ', '').replace('-', '').isalpha():
            # Contains non-letter characters (except space and hyphen)
            self.info.append(
                f"ℹ️  Doelwoord '{doelwoord}' bevat speciale tekens (check spelling)"
            )

        # 2. Lengte check
        if len(doelwoord) > 30:
            self.warnings.append(
                f"⚠️  Doelwoord '{doelwoord}' is erg lang ({len(doelwoord)} karakters)"
            )

        # 3. Check of doelwoord in vraag voorkomt
        hoofdvraag = item.get('hoofdvraag', '').lower()
        if doelwoord.lower() in hoofdvraag:
            # This is OK for some types (e.g., "Wat betekent 'enthousiast'?")
            item_type = item.get('item_type', '')
            if item_type not in ['synoniemen', 'antoniemen', 'figuurlijk_uitleggen', 'uitdrukking']:
                self.info.append(
                    f"ℹ️  Doelwoord '{doelwoord}' komt voor in hoofdvraag "
                    f"(kan correct zijn bij betekenis-vragen)"
                )


    def _check_woordfrequentie(self, item: Dict[str, Any]):
        """Check word frequency appropriateness"""
        doelwoord = item.get('doelwoord', '').lower()
        frequentie = item.get('woordfrequentie', '')
        groep = item.get('groep')

        # 1. Check hoogfrequent voor G3
        if groep == 3:
            if doelwoord in self.HOOGFREQUENT_G3:
                self.info.append(
                    f"ℹ️  ✅ '{doelwoord}' is hoogfrequent woord (goed voor G3)"
                )
            else:
                self.warnings.append(
                    f"⚠️  G3: '{doelwoord}' mogelijk niet hoogfrequent genoeg"
                )

        # 2. Frequency level check
        if frequentie:
            if frequentie not in self.WOORDFREQUENTIE:
                self.warnings.append(
                    f"⚠️  Onbekende woordfrequentie: '{frequentie}'"
                )


    def _check_item_type(self, item: Dict[str, Any]):
        """Check item type appropriateness"""
        item_type = item.get('item_type', '')
        groep = item.get('groep')
        categorie = item.get('woordcategorie', '')

        # 1. Plaatje types (G3 vooral)
        if item_type in ['meerkeuze_plaatje', 'plaatje_woord']:
            if groep > 5:
                self.info.append(
                    f"ℹ️  G{groep}: Plaatje-items zijn gebruikelijker voor G3-4"
                )
            # Check if plaatje is mentioned
            if 'plaatje' not in str(item.get('hoofdvraag', '')).lower():
                if not item.get('plaatje') and not item.get('plaatje_beschrijving'):
                    self.warnings.append(
                        "⚠️  Item type met 'plaatje' maar geen plaatje/beschrijving aanwezig"
                    )

        # 2. Figuurlijk types (G4-E+)
        if item_type in ['figuurlijk_letterlijk', 'figuurlijk_uitleggen', 'uitdrukking']:
            if groep < 4 or (groep == 4 and item.get('niveau') == 'M'):
                self.errors.append(
                    f"❌ G{groep}-{item.get('niveau')}: Figuurlijk taalgebruik pas vanaf G4-E"
                )

        # 3. Academische types (G6+)
        if item_type in ['academisch', 'retorisch_middel', 'betekenisnuances']:
            if groep < 6:
                self.warnings.append(
                    f"⚠️  G{groep}: '{item_type}' is complex, gebruikelijk vanaf G6"
                )


    def _check_vraag_kwaliteit(self, item: Dict[str, Any]):
        """Check question quality"""
        hoofdvraag = item.get('hoofdvraag', '').strip()

        if not hoofdvraag:
            self.errors.append("❌ Hoofdvraag is leeg")
            return

        # 1. Vraag eindigt met vraagteken (meestal)
        item_type = item.get('item_type', '')
        if item_type not in ['invullen']:  # Invullen kan zonder vraagteken
            if not hoofdvraag.endswith('?'):
                self.warnings.append(
                    "⚠️  Hoofdvraag eindigt niet met vraagteken"
                )

        # 2. Check vraagwoord
        vraagwoorden = ['wat', 'welke', 'welk', 'hoe', 'waarom', 'waar', 'wie', 'wanneer']
        heeft_vraagwoord = any(hoofdvraag.lower().startswith(vw) for vw in vraagwoorden)
        if not heeft_vraagwoord and '?' in hoofdvraag:
            self.info.append(
                "ℹ️  Vraag heeft geen standaard vraagwoord (kan correct zijn)"
            )


    def _check_afleiders(self, item: Dict[str, Any]):
        """Check distractor quality"""
        afleiders = item.get('afleiders', [])
        correct = str(item.get('correct_antwoord', '')).strip()
        groep = item.get('groep')
        categorie = item.get('woordcategorie', '')

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

        # 5. Type-specifieke afleider checks
        item_type = item.get('item_type', '')

        if item_type in ['synoniemen', 'synoniemen_basis']:
            # Afleiders should not be antonyms
            self.info.append(
                "ℹ️  Synoniemen: check dat afleiders GEEN antoniemen zijn (veelvoorkomende fout)"
            )

        elif item_type in ['antoniemen']:
            # Afleiders should not be synonyms
            self.info.append(
                "ℹ️  Antoniemen: check dat afleiders GEEN synoniemen zijn"
            )

        elif item_type in ['categoriseren']:
            # Afleiders should be from different categories
            self.info.append(
                "ℹ️  Categoriseren: afleiders moeten uit andere categorieën zijn"
            )

        # 6. G3: visueel vergelijkbaar
        if groep == 3:
            # Afleiders should be plausible for young children
            self.info.append(
                "ℹ️  G3: check dat afleiders visueel/klankelijk vergelijkbaar zijn"
            )


    def _check_g3_specifiek(self, item: Dict[str, Any]):
        """Extra checks specific for Groep 3"""
        niveau = item.get('niveau')
        doelwoord = item.get('doelwoord', '').lower()
        categorie = item.get('woordcategorie', '')

        regels = self.NIVEAU_REGELS.get((3, niveau), {})

        # 1. Alleen concreet (GEEN abstract)
        if 'abstract' in categorie:
            self.errors.append(
                f"❌ G3: Alleen concrete woorden. '{categorie}' is abstract!"
            )

        # 2. Hoogfrequent check
        if doelwoord not in self.HOOGFREQUENT_G3:
            # Check if it's at least a simple word
            if len(doelwoord) > 7:
                self.warnings.append(
                    f"⚠️  G3: '{doelwoord}' is lang en mogelijk niet hoogfrequent genoeg"
                )

        # 3. Plaatje ondersteuning (vooral M3)
        if niveau == 'M':
            item_type = item.get('item_type', '')
            if 'plaatje' not in item_type:
                self.warnings.append(
                    "⚠️  G3-M: Plaatje-ondersteuning sterk aanbevolen"
                )

        # 4. GEEN figuurlijk
        if 'figuurlijk' in categorie:
            self.errors.append(
                "❌ G3: Figuurlijk taalgebruik NIET toegestaan (te abstract)"
            )

        # 5. GEEN meerdere betekenissen
        item_type = item.get('item_type', '')
        if 'meerdere_betekenissen' in item_type:
            self.errors.append(
                "❌ G3: Meerdere betekenissen te complex (komt vanaf G4-M)"
            )


    def _check_figuurlijk_taalgebruik(self, item: Dict[str, Any]):
        """Check figurative language (G4-E+)"""
        item_type = item.get('item_type', '')
        categorie = item.get('woordcategorie', '')
        groep = item.get('groep')
        niveau = item.get('niveau')

        if 'figuurlijk' not in categorie and item_type not in ['figuurlijk_letterlijk', 'figuurlijk_uitleggen', 'uitdrukking']:
            return  # Not a figurative item

        # Check if it's allowed
        if groep < 4 or (groep == 4 and niveau == 'M'):
            self.errors.append(
                f"❌ G{groep}-{niveau}: Figuurlijk taalgebruik pas vanaf G4-E"
            )
            return

        # Check if context is provided
        context = item.get('context_zin') or item.get('context_tekst')
        if not context:
            self.warnings.append(
                "⚠️  Figuurlijk: context_zin aanbevolen om betekenis te verduidelijken"
            )

        # Check if toelichting explains figurative vs literal
        toelichting = item.get('toelichting', '').lower()
        if toelichting:
            if 'figuurlijk' not in toelichting and 'letterlijk' not in toelichting:
                self.warnings.append(
                    "⚠️  Figuurlijk: toelichting zou 'figuurlijk' vs 'letterlijk' moeten uitleggen"
                )

        # Check afleiders include literal interpretation
        afleiders = item.get('afleiders', [])
        has_literal = False
        for afleider in afleiders:
            afleider_str = str(afleider).lower()
            if any(word in afleider_str for word in ['letterlijk', 'echt', 'daadwerkelijk']):
                has_literal = True
                break

        if not has_literal and item_type == 'figuurlijk_letterlijk':
            self.info.append(
                "ℹ️  Figuurlijk: overweeg een letterlijke interpretatie als afleider"
            )


    def _check_woordrelaties(self, item: Dict[str, Any]):
        """Check word relations validation"""
        item_type = item.get('item_type', '')

        if item_type in ['synoniemen', 'synoniemen_basis']:
            # Check correct answer is indeed a synonym
            doelwoord = item.get('doelwoord', '').lower()
            correct = str(item.get('correct_antwoord', '')).lower()

            # Basic check: should not be same word
            if doelwoord == correct:
                self.warnings.append(
                    f"⚠️  Synoniem '{correct}' is hetzelfde woord als doelwoord '{doelwoord}'"
                )

            # Check toelichting mentions "synoniem" or "zelfde betekenis"
            toelichting = item.get('toelichting', '').lower()
            if toelichting and 'synoniem' not in toelichting and 'zelfde betekenis' not in toelichting:
                self.info.append(
                    "ℹ️  Synoniemen: vermeld 'synoniem' of 'zelfde betekenis' in toelichting"
                )

        elif item_type in ['antoniemen']:
            # Check toelichting mentions "antoniem" or "tegenovergesteld"
            toelichting = item.get('toelichting', '').lower()
            if toelichting and 'antoniem' not in toelichting and 'tegenover' not in toelichting:
                self.info.append(
                    "ℹ️  Antoniemen: vermeld 'antoniem' of 'tegenovergesteld' in toelichting"
                )

        elif item_type in ['categoriseren']:
            # Should mention category in toelichting
            toelichting = item.get('toelichting', '').lower()
            categorie_woorden = ['categorie', 'groep', 'soort', 'type']
            if toelichting and not any(woord in toelichting for woord in categorie_woorden):
                self.info.append(
                    "ℹ️  Categoriseren: vermeld categorie/groep in toelichting"
                )


    def _check_context(self, item: Dict[str, Any]):
        """Check context provision"""
        item_type = item.get('item_type', '')

        # Items that should have context
        context_items = ['context', 'context_zinsvervollend', 'meerdere_betekenissen_context',
                        'figuurlijk_letterlijk', 'figuurlijk_uitleggen']

        if item_type in context_items:
            context_zin = item.get('context_zin')
            context_tekst = item.get('context_tekst')

            if not context_zin and not context_tekst:
                self.errors.append(
                    f"❌ Item type '{item_type}' vereist context_zin of context_tekst"
                )

            # Check if doelwoord appears in context
            doelwoord = item.get('doelwoord', '').lower()
            context = str(context_zin or context_tekst or '').lower()

            if doelwoord and context:
                if doelwoord not in context:
                    self.warnings.append(
                        f"⚠️  Doelwoord '{doelwoord}' komt niet voor in context"
                    )


    def _check_metadata(self, item: Dict[str, Any]):
        """Check metadata completeness"""

        # 1. ID format
        item_id = item.get('id', '')
        expected_pattern = r'^W_G[3-8]_[ME]_\d{3}$'
        if not re.match(expected_pattern, item_id):
            self.warnings.append(
                f"⚠️  ID '{item_id}' volgt niet verwacht patroon: W_G[3-8]_[ME]_###"
            )

        # 2. Toelichting aanwezig
        if not item.get('toelichting'):
            self.warnings.append(
                "⚠️  Geen toelichting aanwezig (sterk aanbevolen)"
            )

        # 3. Strategie aanwezig
        strategie = item.get('strategie')
        if not strategie:
            self.warnings.append(
                "⚠️  Geen strategie vermeld (aanbevolen)"
            )
        elif strategie not in self.STRATEGIEEN:
            self.warnings.append(
                f"⚠️  Ongebruikelijke strategie: '{strategie}'"
            )

        # 4. Woordenschat_omvang_niveau
        ws_niveau = item.get('woordenschat_omvang_niveau')
        if ws_niveau:
            geldige_niveaus = ['basis_500', 'uitgebreid_2000', 'gevorderd_5000', 'academisch_10000+']
            if ws_niveau not in geldige_niveaus:
                self.info.append(
                    f"ℹ️  Woordenschat_omvang_niveau '{ws_niveau}' niet standaard"
                )


    def _check_cross_validation(self, item: Dict[str, Any]):
        """Cross-validation checks"""

        # 1. Receptief vs. productief consistency
        ws_type = item.get('woordenschat_type')
        item_type = item.get('item_type', '')

        # Receptief: herkennen, begrijpen
        receptief_types = ['meerkeuze', 'meerkeuze_plaatje', 'synoniemen', 'antoniemen',
                           'categoriseren', 'context']
        # Productief: zelf gebruiken
        productief_types = ['invullen']

        if ws_type == 'receptief' and item_type in productief_types:
            self.warnings.append(
                f"⚠️  Receptief type maar item_type '{item_type}' is productief"
            )
        elif ws_type == 'productief' and item_type in receptief_types:
            self.info.append(
                f"ℹ️  Productief type maar item_type '{item_type}' is vaak receptief"
            )

        # 2. Woordcategorie vs. doelgroep
        groep = item.get('groep')
        categorie = item.get('woordcategorie', '')

        if groep <= 4:
            if categorie in ['academisch', 'retorisch', 'filosofisch']:
                self.warnings.append(
                    f"⚠️  G{groep}: Categorie '{categorie}' is te complex (pas G6+)"
                )

        # 3. Moeilijkheid vs. tijd consistency
        moeilijkheid = item.get('moeilijkheidsgraad')
        tijd = item.get('geschatte_tijd_sec')

        if moeilijkheid and tijd:
            # Moeilijker items zouden meer tijd moeten kosten
            if moeilijkheid > 0.7 and tijd < 40:
                self.warnings.append(
                    f"⚠️  Hoge moeilijkheid ({moeilijkheid:.2f}) maar korte tijd ({tijd}s)"
                )
            if moeilijkheid < 0.3 and tijd > 60:
                self.warnings.append(
                    f"⚠️  Lage moeilijkheid ({moeilijkheid:.2f}) maar lange tijd ({tijd}s)"
                )


    def _calculate_score(self) -> float:
        """Calculate quality score"""
        error_penalty = len(self.errors) * 0.15
        warning_penalty = len(self.warnings) * 0.05

        score = max(0.0, 1.0 - error_penalty - warning_penalty)
        return round(score, 2)


def valideer_woordenschat_items(filepath: str) -> None:
    """Validate vocabulary items from JSON file"""

    print("=" * 80)
    print("WOORDENSCHAT VALIDATOR v3.0 - Enhanced Validation")
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

    validator = WoordenschatValidatorEnhanced()

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
        print("Usage: python woordenschat-validator-v3.py <test-file.json>")
        print("\nExample:")
        print("  python woordenschat-validator-v3.py test-woordenschat-g3.json")
        sys.exit(1)

    valideer_woordenschat_items(sys.argv[1])
