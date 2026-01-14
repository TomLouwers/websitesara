#!/usr/bin/env python3
"""
SCHRIJVEN VALIDATOR v3.0 - Enhanced Validator voor Schrijven Items

Valideert schrijfopdrachten voor Groep 3-8, Midden/Eind niveau.
Gebaseerd op prompt-schrijven-v2.md specificaties.

Features:
- Volledige G3-G8 M/E niveauregels (12 varianten)
- Drie domeinen: Technisch schrijven, Spelling, Stellen (compositie)
- Tekstsoort validatie (verhaal, verslag, brief, instructie, betoog, etc.)
- Schrijfproces validatie (plannen, schrijven, reviseren)
- Schrijfdoel checks (informeren, instrueren, vermaken, overtuigen)
- Doelgroep validatie
- Beoordelingscriteria checks (inhoud, structuur, taal, doelgroep/doel)
- Structuur eisen validatie (lengte, alineas, onderdelen)
- Ondersteuning niveau checks (geleid, semi-geleid, vrij)
- G3-specifieke checks (technisch dominant, klankzuiver)
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


class SchrijvenValidatorEnhanced:
    """Enhanced validator for writing assignment items"""

    # NIVEAU REGELS per (groep, niveau)
    NIVEAU_REGELS = {
        # GROEP 3
        (3, 'M'): {
            'schrijf_domein': 'technisch+spelling',
            'schrijftempo': (5, 10),  # letters/minuut
            'tekstsoorten': ['losse_woorden', 'losse_zinnen'],
            'zinnen_lengte': (3, 5),  # woorden per zin
            'spelling_focus': 'klankzuiver',
            'ondersteuning': 'geleid',
            'structuur': None,  # Nog geen tekststructuur
            'moeilijkheid': (0.15, 0.35),
            'tijd_per_item': (2, 5),  # minuten
        },
        (3, 'E'): {
            'schrijf_domein': 'technisch+spelling',
            'schrijftempo': (10, 15),
            'tekstsoorten': ['losse_zinnen', 'verhaal_eenvoudig'],
            'zinnen_aantal': (2, 3),
            'zinnen_lengte': (5, 8),
            'samenhang': ['en', 'toen', 'daarna'],
            'spelling_focus': 'klankzuiver+tweeklanken',
            'ondersteuning': 'geleid',
            'structuur': 'begin_eind',
            'moeilijkheid': (0.30, 0.50),
            'tijd_per_item': (5, 10),
        },

        # GROEP 4
        (4, 'M'): {
            'schrijf_domein': 'spelling+stellen',
            'schrijftempo': (15, 25),
            'tekstsoorten': ['verhaal', 'verslag', 'brief_persoonlijk'],
            'tekst_lengte': (80, 120),  # woorden
            'zinnen_aantal': (8, 12),
            'spelling_focus': 'regelgebonden',
            'ondersteuning': 'semi-geleid',
            'structuur': 'begin_midden_eind',
            'alineas': 'introductie',
            'schrijfproces': ['plannen', 'schrijven', 'reviseren'],
            'beoordelingscriteria': ['spelling', 'zinsbouw', 'tekststructuur', 'samenhang', 'inhoud'],
            'moeilijkheid': (0.40, 0.65),
            'tijd_per_item': (15, 25),
        },
        (4, 'E'): {
            'schrijf_domein': 'spelling+stellen',
            'schrijftempo': (25, 35),
            'tekstsoorten': ['verhaal', 'verslag', 'brief_persoonlijk', 'instructie', 'beschrijving'],
            'tekst_lengte': (120, 200),
            'alineas': (2, 3),
            'spelling_focus': 'dt_regel',  # KERN!
            'ondersteuning': 'semi-geleid',
            'structuur': 'inleiding_kern_slot',
            'signaalwoorden': True,
            'schrijfproces': ['plannen', 'schrijven', 'reviseren', 'herschrijven'],
            'moeilijkheid': (0.55, 0.75),
            'tijd_per_item': (25, 35),
        },

        # GROEP 5
        (5, 'M'): {
            'schrijf_domein': 'stellen',
            'schrijftempo': (35, 45),
            'typen': (10, 20),  # woorden/minuut (optioneel)
            'tekstsoorten': ['verhaal', 'verslag_formeel', 'brief', 'instructie', 'mening', 'samenvatting'],
            'tekst_lengte': (150, 250),
            'alineas': (4, 6),
            'tussenkopjes': True,
            'spelling_focus': 'samenstellingen+tussen_n',
            'ondersteuning': 'semi-geleid',
            'schrijfproces': ['plannen_doel_doelgroep', 'schrijven_alinea', 'reviseren_inhoud_structuur_taal'],
            'doelgroep_doel': True,
            'moeilijkheid': (0.60, 0.78),
            'tijd_per_item': (30, 45),
        },
        (5, 'E'): {
            'schrijf_domein': 'stellen',
            'tekstsoorten': ['verslag_formeel', 'betoog', 'recensie', 'samenvatting'],
            'tekst_lengte': (200, 300),
            'structuur': 'argumentatie',
            'schrijfproces': ['onderzoeken', 'plannen', 'schrijven', 'reviseren', 'herschrijven'],
            'moeilijkheid': (0.68, 0.85),
            'tijd_per_item': (45, 60),
        },

        # GROEP 6
        (6, 'M'): {
            'schrijf_domein': 'stellen',
            'schrijftempo': (45, 55),
            'typen': (20, 30),
            'tekstsoorten': ['werkstuk', 'formele_brief', 'betoog', 'verslag'],
            'tekst_lengte': (400, 600),
            'structuur': 'academisch',  # voorblad, inhoudsopgave, etc.
            'bronvermelding': True,
            'schrijfproces': ['oriënteren', 'onderzoeken', 'plannen', 'schrijven', 'reviseren', 'presenteren'],
            'register': True,  # formeel vs. informeel
            'moeilijkheid': (0.72, 0.88),
            'tijd_per_item': (60, 90),
        },
        (6, 'E'): {
            'schrijf_domein': 'stellen',
            'tekstsoorten': ['werkstuk', 'betoog_uitgebreid', 'column', 'recensie'],
            'tekst_lengte': (500, 800),
            'retorisch': True,  # ethos, pathos, logos
            'moeilijkheid': (0.78, 0.92),
            'tijd_per_item': (60, 120),
        },

        # GROEP 7
        (7, 'M'): {
            'schrijf_domein': 'stellen',
            'typen': (30, 40),
            'tekstsoorten': ['essay', 'toespraak', 'betoog_complex', 'werkstuk'],
            'tekst_lengte': (500, 800),
            'moeilijkheid': (0.82, 0.94),
            'tijd_per_item': (60, 120),
        },
        (7, 'E'): {
            'schrijf_domein': 'stellen',
            'moeilijkheid': (0.85, 0.96),
            'tijd_per_item': (90, 150),
        },

        # GROEP 8
        (8, 'M'): {
            'schrijf_domein': 'stellen',
            'referentieniveau': '1F',
            'tekstsoorten': ['alle'],
            'moeilijkheid': (0.88, 0.97),
            'tijd_per_item': (60, 180),
        },
        (8, 'E'): {
            'schrijf_domein': 'stellen',
            'referentieniveau': '1S',
            'moeilijkheid': (0.90, 1.0),
            'tijd_per_item': (90, 240),
        },
    }

    # Geldige schrijfdomeinen
    SCHRIJF_DOMEINEN = {'technisch', 'spelling', 'stellen',
                        'technisch+spelling', 'spelling+stellen'}

    # Geldige tekstsoorten
    TEKSTSOORTEN = {
        'losse_woorden', 'losse_zinnen', 'verhaal_eenvoudig', 'verhaal',
        'verslag', 'verslag_formeel',
        'brief', 'brief_persoonlijk', 'formele_brief',
        'instructie', 'beschrijving',
        'mening', 'betoog', 'betoog_uitgebreid', 'betoog_complex',
        'samenvatting', 'recensie',
        'werkstuk', 'column', 'essay', 'toespraak'
    }

    # Geldige schrijfdoelen
    SCHRIJFDOELEN = {
        'informeren', 'instrueren', 'vermaken', 'overtuigen',
        'documenteren', 'reflecteren', 'analyseren'
    }

    # Geldige ondersteuningsniveaus
    ONDERSTEUNING = {'geleid', 'semi-geleid', 'vrij'}


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

        # 3. Tekstsoort validatie
        self._check_tekstsoort(item)

        # 4. Schrijfopdracht validatie
        self._check_schrijfopdracht(item)

        # 5. Structuur eisen validatie
        self._check_structuur_eisen(item)

        # 6. Beoordelingscriteria validatie
        self._check_beoordelingscriteria(item)

        # 7. Schrijfproces validatie
        self._check_schrijfproces(item)

        # 8. G3-specifieke checks
        if item.get('groep') == 3:
            self._check_g3_specifiek(item)

        # 9. Domein-specifieke checks
        self._check_domein_specifiek(item)

        # 10. Doelgroep/doel validatie (G5+)
        if item.get('groep') >= 5:
            self._check_doelgroep_doel(item)

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
            'id', 'groep', 'niveau', 'schrijf_domein',
            'tekstsoort', 'schrijfopdracht'
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

        # Check schrijf_domein
        domein = item.get('schrijf_domein')
        if domein and domein not in self.SCHRIJF_DOMEINEN:
            self.errors.append(
                f"❌ Ongeldig schrijf_domein: {domein}. "
                f"Moet zijn: {', '.join(self.SCHRIJF_DOMEINEN)}"
            )

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

        # 1. Tekstsoort toegestaan?
        tekstsoort = item.get('tekstsoort')
        toegestane_soorten = regels.get('tekstsoorten', [])
        if toegestane_soorten and toegestane_soorten != ['alle']:
            if tekstsoort not in toegestane_soorten:
                self.warnings.append(
                    f"⚠️  Tekstsoort '{tekstsoort}' niet standaard voor G{groep}-{niveau}. "
                    f"Standaard: {', '.join(toegestane_soorten[:3])}..."
                )

        # 2. Ondersteuning niveau
        ondersteuning = item.get('ondersteuning')
        verwachte_ondersteuning = regels.get('ondersteuning')
        if verwachte_ondersteuning and ondersteuning:
            if ondersteuning != verwachte_ondersteuning:
                self.info.append(
                    f"ℹ️  Ondersteuning '{ondersteuning}' afwijkend van verwacht "
                    f"'{verwachte_ondersteuning}' voor G{groep}-{niveau}"
                )

        # 3. Tekst lengte (structuur_eisen)
        structuur_eisen = item.get('structuur_eisen', {})
        if structuur_eisen:
            lengte_min = structuur_eisen.get('lengte_min_woorden', 0)
            lengte_max = structuur_eisen.get('lengte_max_woorden', 999999)

            tekst_lengte_verwacht = regels.get('tekst_lengte')
            if tekst_lengte_verwacht:
                min_verwacht, max_verwacht = tekst_lengte_verwacht

                # Check if within reasonable range
                if lengte_min < min_verwacht * 0.7:  # Tolerantie 30%
                    self.warnings.append(
                        f"⚠️  Minimum lengte ({lengte_min}) is laag voor G{groep}-{niveau} "
                        f"(verwacht ~{min_verwacht})"
                    )
                if lengte_max > max_verwacht * 1.5:  # Tolerantie 50%
                    self.warnings.append(
                        f"⚠️  Maximum lengte ({lengte_max}) is hoog voor G{groep}-{niveau} "
                        f"(verwacht ~{max_verwacht})"
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


    def _check_tekstsoort(self, item: Dict[str, Any]):
        """Check text type appropriateness"""
        tekstsoort = item.get('tekstsoort', '')
        groep = item.get('groep')

        # 1. Tekstsoort vs groep
        if groep == 3:
            if tekstsoort not in ['losse_woorden', 'losse_zinnen', 'verhaal_eenvoudig']:
                self.errors.append(
                    f"❌ G3: Tekstsoort '{tekstsoort}' te complex. "
                    f"Gebruik: losse_woorden, losse_zinnen, of verhaal_eenvoudig"
                )

        if groep == 4:
            complexe_soorten = ['betoog', 'werkstuk', 'essay', 'column']
            if tekstsoort in complexe_soorten:
                self.warnings.append(
                    f"⚠️  G4: Tekstsoort '{tekstsoort}' is complex (meestal vanaf G5+)"
                )

        # 2. Tekstsoort kenmerken check
        if tekstsoort == 'betoog':
            # Should have argumenten in beoordelingscriteria
            criteria = item.get('beoordelingscriteria', {})
            inhoud = str(criteria.get('inhoud', '')).lower()
            if 'argument' not in inhoud and 'standpunt' not in inhoud:
                self.warnings.append(
                    "⚠️  Betoog: beoordelingscriteria-inhoud moet 'argumenten' vermelden"
                )

        elif tekstsoort in ['verslag', 'verslag_formeel']:
            criteria = item.get('beoordelingscriteria', {})
            inhoud = str(criteria.get('inhoud', '')).lower()
            if 'feitelijk' not in inhoud and 'objectief' not in inhoud:
                self.info.append(
                    "ℹ️  Verslag: vermeld 'feitelijk' of 'objectief' in beoordelingscriteria"
                )

        elif tekstsoort == 'instructie':
            criteria = item.get('beoordelingscriteria', {})
            structuur = str(criteria.get('structuur', '')).lower()
            if 'stappen' not in structuur and 'volgorde' not in structuur:
                self.warnings.append(
                    "⚠️  Instructie: beoordelingscriteria-structuur moet 'stappen' vermelden"
                )


    def _check_schrijfopdracht(self, item: Dict[str, Any]):
        """Check writing assignment quality"""
        opdracht = item.get('schrijfopdracht', '').strip()

        if not opdracht:
            self.errors.append("❌ Schrijfopdracht is leeg")
            return

        groep = item.get('groep')
        tekstsoort = item.get('tekstsoort', '')

        # 1. Lengte check
        if len(opdracht) < 20:
            self.warnings.append(
                f"⚠️  Schrijfopdracht is zeer kort ({len(opdracht)} karakters). "
                f"Zijn alle instructies duidelijk?"
            )

        # 2. Check of tekstsoort wordt genoemd
        if tekstsoort not in ['losse_woorden', 'losse_zinnen']:
            if tekstsoort.lower() not in opdracht.lower():
                self.info.append(
                    f"ℹ️  Tekstsoort '{tekstsoort}' wordt niet genoemd in opdracht "
                    f"(kan verwarrend zijn voor leerling)"
                )

        # 3. Check eisen in opdracht (G4+)
        if groep >= 4:
            eisen_woorden = ['minimaal', 'maximum', 'gebruik', 'schrijf', 'bevat']
            heeft_eisen = any(woord in opdracht.lower() for woord in eisen_woorden)
            if not heeft_eisen:
                self.warnings.append(
                    "⚠️  G4+: Schrijfopdracht zou duidelijke eisen moeten bevatten "
                    "(minimaal X woorden, gebruik Y, bevat Z)"
                )

        # 4. Check structuur vermelding (G4+)
        if groep >= 4 and tekstsoort not in ['losse_zinnen', 'losse_woorden']:
            structuur_woorden = ['begin', 'midden', 'eind', 'inleiding', 'kern', 'slot',
                                'alinea', 'structuur']
            heeft_structuur = any(woord in opdracht.lower() for woord in structuur_woorden)
            if not heeft_structuur:
                self.info.append(
                    "ℹ️  G4+: Overweeg structuur te vermelden in opdracht "
                    "(begin-midden-eind, inleiding-kern-slot)"
                )


    def _check_structuur_eisen(self, item: Dict[str, Any]):
        """Check structure requirements"""
        structuur_eisen = item.get('structuur_eisen', {})

        if not structuur_eisen:
            groep = item.get('groep')
            if groep >= 4:
                self.warnings.append(
                    "⚠️  Geen structuur_eisen aanwezig (aanbevolen voor G4+)"
                )
            return

        # 1. Lengte eisen
        lengte_min = structuur_eisen.get('lengte_min_woorden')
        lengte_max = structuur_eisen.get('lengte_max_woorden')

        if lengte_min is None and lengte_max is None:
            self.warnings.append(
                "⚠️  Structuur_eisen: geen lengte_min_woorden of lengte_max_woorden"
            )

        if lengte_min and lengte_max:
            if lengte_min > lengte_max:
                self.errors.append(
                    f"❌ Structuur_eisen: lengte_min ({lengte_min}) > lengte_max ({lengte_max})"
                )
            if lengte_max < lengte_min:
                self.errors.append(
                    f"❌ Structuur_eisen: lengte_max ({lengte_max}) < lengte_min ({lengte_min})"
                )

        # 2. Alinea's
        alineas = structuur_eisen.get('alineas')
        groep = item.get('groep')

        if isinstance(alineas, int):
            if groep == 3:
                if alineas > 1:
                    self.warnings.append(
                        f"⚠️  G3: {alineas} alinea's is te complex (G3 = geen alinea's)"
                    )
            elif groep == 4 and alineas > 3:
                self.info.append(
                    f"ℹ️  G4: {alineas} alinea's is veel (introductie alinea's in G4)"
                )

        # 3. Onderdelen
        onderdelen = structuur_eisen.get('onderdelen', [])
        if onderdelen:
            # Check valid structure
            geldige_structuren = [
                ['begin', 'midden', 'eind'],
                ['inleiding', 'kern', 'slot'],
                ['inleiding', 'kern', 'conclusie']
            ]

            if onderdelen not in geldige_structuren:
                # Check if it's a variation
                self.info.append(
                    f"ℹ️  Structuur onderdelen: {onderdelen} is niet-standaard"
                )


    def _check_beoordelingscriteria(self, item: Dict[str, Any]):
        """Check assessment criteria"""
        criteria = item.get('beoordelingscriteria', {})

        groep = item.get('groep')
        if groep >= 4 and not criteria:
            self.warnings.append(
                "⚠️  Geen beoordelingscriteria aanwezig (aanbevolen voor G4+)"
            )
            return

        if not criteria:
            return

        # Check all 4 dimensions
        dimensies = ['inhoud', 'structuur', 'taal', 'doelgroep_doel']

        for dimensie in dimensies:
            if dimensie not in criteria:
                if groep < 5 and dimensie == 'doelgroep_doel':
                    # Optional for G3-4
                    continue
                self.warnings.append(
                    f"⚠️  Beoordelingscriteria: '{dimensie}' ontbreekt"
                )
            elif not criteria.get(dimensie) or not str(criteria.get(dimensie)).strip():
                self.warnings.append(
                    f"⚠️  Beoordelingscriteria: '{dimensie}' is leeg"
                )

        # Check content quality
        for dimensie, tekst in criteria.items():
            if tekst and len(str(tekst).strip()) < 10:
                self.warnings.append(
                    f"⚠️  Beoordelingscriteria-{dimensie}: zeer kort ({len(str(tekst))} chars). "
                    f"Geef meer detail."
                )


    def _check_schrijfproces(self, item: Dict[str, Any]):
        """Check writing process steps"""
        proces_stappen = item.get('schrijfproces_stappen', [])

        groep = item.get('groep')
        if groep >= 4 and not proces_stappen:
            self.warnings.append(
                "⚠️  Geen schrijfproces_stappen aanwezig (aanbevolen voor G4+)"
            )
            return

        if not proces_stappen:
            return

        # Check standard steps
        standaard_stappen = ['plannen', 'schrijven', 'reviseren']
        for stap in standaard_stappen:
            if stap not in proces_stappen:
                self.info.append(
                    f"ℹ️  Schrijfproces: '{stap}' stap ontbreekt (standaard voor schrijfproces)"
                )

        # Check advanced steps for higher grades
        if groep >= 5:
            gevorderde_stappen = ['onderzoeken', 'herschrijven', 'oriënteren']
            heeft_gevorderd = any(stap in proces_stappen for stap in gevorderde_stappen)
            if not heeft_gevorderd:
                self.info.append(
                    f"ℹ️  G{groep}: Overweeg gevorderde stappen "
                    f"(onderzoeken, herschrijven, oriënteren)"
                )


    def _check_g3_specifiek(self, item: Dict[str, Any]):
        """Extra checks specific for Groep 3"""
        niveau = item.get('niveau')
        tekstsoort = item.get('tekstsoort', '')

        regels = self.NIVEAU_REGELS.get((3, niveau), {})

        # 1. Technisch schrijven dominant
        domein = item.get('schrijf_domein', '')
        verwacht_domein = regels.get('schrijf_domein')
        if verwacht_domein and domein != verwacht_domein:
            self.warnings.append(
                f"⚠️  G3-{niveau}: Schrijf_domein moet '{verwacht_domein}' zijn, "
                f"niet '{domein}'"
            )

        # 2. Klankzuiver spelling
        if 'spelling' in domein:
            spelling_focus = regels.get('spelling_focus')
            if 'klankzuiver' not in spelling_focus:
                self.errors.append(
                    f"❌ G3: Spelling moet klankzuiver zijn (GEEN regelgebonden!)"
                )

        # 3. Geen tekststructuur voor M3
        if niveau == 'M':
            structuur_eisen = item.get('structuur_eisen', {})
            onderdelen = structuur_eisen.get('onderdelen', [])
            if onderdelen:
                self.warnings.append(
                    "⚠️  G3-M: Geen tekststructuur vereist (alleen losse zinnen)"
                )

        # 4. Geleid schrijven
        ondersteuning = item.get('ondersteuning', '')
        if ondersteuning != 'geleid':
            self.warnings.append(
                f"⚠️  G3: Ondersteuning moet 'geleid' zijn, niet '{ondersteuning}'"
            )

        # 5. Korte zinnen
        opdracht = item.get('schrijfopdracht', '').lower()
        if 'zin' in opdracht:
            # Check if mentions short sentences
            if '3-5 woorden' not in opdracht and 'korte zin' not in opdracht:
                self.info.append(
                    "ℹ️  G3: Vermeld zinslengte (bijv. '3-5 woorden') in opdracht"
                )


    def _check_domein_specifiek(self, item: Dict[str, Any]):
        """Domain-specific checks"""
        domein = item.get('schrijf_domein', '')
        groep = item.get('groep')

        # 1. Technisch schrijven (G3 vooral)
        if 'technisch' in domein:
            if groep > 4:
                self.info.append(
                    f"ℹ️  G{groep}: Technisch schrijven is vooral focus in G3-4"
                )

            # Should mention lettervorming, tempo, etc.
            criteria = item.get('beoordelingscriteria', {})
            technisch = str(criteria.get('technisch', '')).lower()
            if criteria and not technisch:
                self.warnings.append(
                    "⚠️  Technisch domein: geen 'technisch' criterium in beoordelingscriteria"
                )

        # 2. Spelling domein
        if 'spelling' in domein and domein != 'spelling':
            # Spelling combined with other domain
            self.info.append(
                f"ℹ️  Spelling domein: check ook spelling-validator-v3.py voor spelling regels"
            )

        # 3. Stellen domein (G4+)
        if domein == 'stellen':
            if groep < 4:
                self.warnings.append(
                    f"⚠️  G{groep}: Stellen (compositie) is complex voor G3 "
                    f"(gebruik technisch+spelling)"
                )

            # Should have tekstsoort beyond simple
            tekstsoort = item.get('tekstsoort', '')
            if tekstsoort in ['losse_woorden', 'losse_zinnen']:
                self.warnings.append(
                    f"⚠️  Stellen domein met tekstsoort '{tekstsoort}' is te simpel. "
                    f"Gebruik verhaal, verslag, brief, etc."
                )


    def _check_doelgroep_doel(self, item: Dict[str, Any]):
        """Check target audience and purpose (G5+)"""
        doelgroep = item.get('doelgroep')
        schrijfdoel = item.get('schrijfdoel')

        # 1. Doelgroep aanwezig
        if not doelgroep:
            self.warnings.append(
                "⚠️  Geen doelgroep vermeld (aanbevolen voor G5+)"
            )

        # 2. Schrijfdoel aanwezig
        if not schrijfdoel:
            self.warnings.append(
                "⚠️  Geen schrijfdoel vermeld (aanbevolen voor G5+)"
            )
        elif schrijfdoel not in self.SCHRIJFDOELEN:
            self.info.append(
                f"ℹ️  Schrijfdoel '{schrijfdoel}' niet standaard. "
                f"Standaard: {', '.join(self.SCHRIJFDOELEN)}"
            )

        # 3. Cross-check tekstsoort en doel
        tekstsoort = item.get('tekstsoort', '')
        if tekstsoort and schrijfdoel:
            # Verhaal → vermaken
            if tekstsoort == 'verhaal' and schrijfdoel != 'vermaken':
                self.info.append(
                    f"ℹ️  Verhaal heeft meestal doel 'vermaken', niet '{schrijfdoel}'"
                )
            # Verslag → informeren/documenteren
            elif 'verslag' in tekstsoort and schrijfdoel not in ['informeren', 'documenteren']:
                self.info.append(
                    f"ℹ️  Verslag heeft meestal doel 'informeren'/'documenteren', niet '{schrijfdoel}'"
                )
            # Betoog → overtuigen
            elif 'betoog' in tekstsoort and schrijfdoel != 'overtuigen':
                self.info.append(
                    f"ℹ️  Betoog heeft meestal doel 'overtuigen', niet '{schrijfdoel}'"
                )
            # Instructie → instrueren
            elif tekstsoort == 'instructie' and schrijfdoel != 'instrueren':
                self.info.append(
                    f"ℹ️  Instructie heeft meestal doel 'instrueren', niet '{schrijfdoel}'"
                )


    def _check_metadata(self, item: Dict[str, Any]):
        """Check metadata completeness"""

        # 1. ID format
        item_id = item.get('id', '')
        expected_pattern = r'^SCH_G[3-8]_[ME]_\d{3}$'
        if not re.match(expected_pattern, item_id):
            self.warnings.append(
                f"⚠️  ID '{item_id}' volgt niet verwacht patroon: SCH_G[3-8]_[ME]_###"
            )

        # 2. Geschatte tijd
        tijd = item.get('geschatte_tijd_minuten')
        groep = item.get('groep')
        niveau = item.get('niveau')

        if tijd:
            regels = self.NIVEAU_REGELS.get((groep, niveau), {})
            tijd_range = regels.get('tijd_per_item')

            if tijd_range:
                min_tijd, max_tijd = tijd_range
                if not (min_tijd <= tijd <= max_tijd):
                    self.warnings.append(
                        f"⚠️  Geschatte tijd ({tijd} min) buiten verwacht "
                        f"({min_tijd}-{max_tijd} min) voor G{groep}-{niveau}"
                    )

        # 3. Voorbeeld antwoord (optioneel maar nuttig)
        if not item.get('voorbeeld_antwoord'):
            self.info.append(
                "ℹ️  Geen voorbeeld_antwoord aanwezig (optioneel maar nuttig voor docent)"
            )


    def _check_cross_validation(self, item: Dict[str, Any]):
        """Cross-validation checks"""

        # 1. Tekstsoort vs. beoordelingscriteria consistency
        tekstsoort = item.get('tekstsoort', '')
        criteria = item.get('beoordelingscriteria', {})

        if tekstsoort == 'betoog' and criteria:
            inhoud = str(criteria.get('inhoud', '')).lower()
            if 'argument' not in inhoud:
                self.warnings.append(
                    "⚠️  Betoog zonder 'argumenten' in beoordelingscriteria-inhoud"
                )

        # 2. Ondersteuning vs. groep
        ondersteuning = item.get('ondersteuning', '')
        groep = item.get('groep')

        if ondersteuning == 'vrij' and groep < 5:
            self.warnings.append(
                f"⚠️  G{groep}: 'Vrij' schrijven is complex (meestal vanaf G5)"
            )

        if ondersteuning == 'geleid' and groep > 5:
            self.info.append(
                f"ℹ️  G{groep}: 'Geleid' schrijven is veel ondersteuning (meestal G3-4)"
            )

        # 3. Lengte vs. tijd consistency
        structuur_eisen = item.get('structuur_eisen', {})
        tijd = item.get('geschatte_tijd_minuten')

        if structuur_eisen and tijd:
            lengte_min = structuur_eisen.get('lengte_min_woorden', 0)

            # Rough estimate: 5-10 woorden per minuut schrijven
            verwachte_min_tijd = lengte_min / 10  # optimistic
            verwachte_max_tijd = lengte_min / 3   # including planning/revision

            if tijd < verwachte_min_tijd:
                self.warnings.append(
                    f"⚠️  Tijd ({tijd} min) lijkt kort voor {lengte_min} woorden "
                    f"(verwacht {verwachte_min_tijd:.0f}-{verwachte_max_tijd:.0f} min)"
                )

        # 4. Schrijfproces vs. tijd
        proces = item.get('schrijfproces_stappen', [])
        if proces and tijd:
            if len(proces) > 3 and tijd < 30:
                self.warnings.append(
                    f"⚠️  Complex schrijfproces ({len(proces)} stappen) maar korte tijd ({tijd} min)"
                )


    def _calculate_score(self) -> float:
        """Calculate quality score"""
        error_penalty = len(self.errors) * 0.15
        warning_penalty = len(self.warnings) * 0.05

        score = max(0.0, 1.0 - error_penalty - warning_penalty)
        return round(score, 2)


def valideer_schrijven_items(filepath: str) -> None:
    """Validate writing assignment items from JSON file"""

    print("=" * 80)
    print("SCHRIJVEN VALIDATOR v3.0 - Enhanced Validation")
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

    validator = SchrijvenValidatorEnhanced()

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
        print("Usage: python schrijven-validator-v3.py <test-file.json>")
        print("\nExample:")
        print("  python schrijven-validator-v3.py test-schrijven-g3.json")
        sys.exit(1)

    valideer_schrijven_items(sys.argv[1])
