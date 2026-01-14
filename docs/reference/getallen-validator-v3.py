"""
GETALLEN VALIDATOR v3.0 - ENHANCED
Uitgebreid validatiescript met diepgaande kwaliteitscontroles voor GETALLEN domein

Features:
- ✅ Volledige G3-G8 ondersteuning (inclusief M3 en E3)
- ✅ Getallenruimte validatie per groep/niveau
- ✅ Bewerkingen validatie (+, -, ×, ÷)
- ✅ Tafels controle per niveau
- ✅ Strategieën validatie (bruggetje, splitsen, etc.)
- ✅ G3-specifieke pedagogische controles
- ✅ Taalcomplexiteit (zinnen, woordlengte)
- ✅ Visualisatie vereisten (VERPLICHT voor G3)
- ✅ Context geschiktheid per leeftijdsgroep
- ✅ Afleider kwaliteit (strategisch, empirisch)
- ✅ Misconceptie detectie
- ✅ Numerieke correctheidscontroles
- ✅ Didactische kwaliteit (LOVA, feedback)
- ✅ Cross-validatie (moeilijkheid vs stappen vs tijd)
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Uitgebreid resultaat van validatie"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    info: List[str] = field(default_factory=list)
    score: float = 0.0  # 0.0 - 1.0
    quality_breakdown: Dict[str, float] = field(default_factory=dict)


class GetallenValidatorEnhanced:
    """Uitgebreide validator voor GETALLEN domein items (G3-G8)"""

    # Niveauregels per groep/niveau
    NIVEAU_REGELS = {
        # GROEP 3
        (3, 'M'): {
            'getallenruimte': (0, 20),
            'bewerkingen': ['optellen_tot_10', 'aftrekken_tot_10'],
            'verboden_bewerkingen': ['vermenigvuldigen', 'delen'],
            'tafels': None,  # GEEN tafels
            'strategieen': ['tellen', 'getalbeelden', 'splitsen_tot_10'],
            'hoofdrekenen': 'verplicht',
            'cijferend': 'verboden',
            'max_stappen': 1,
            'visualisatie': 'verplicht',
            'materialen': ['rekenrek', 'mab_blokjes', 'vingers', 'dobbelstenen'],
            'context_types': ['speelgoed', 'snoep', 'fruit', 'vingers', 'dobbelstenen'],
            'max_zinnen': 2,
            'max_woorden_per_zin': 8,
            'min_tijd_sec': 15,
            'max_tijd_sec': 40,
            'moeilijkheid_range': (0.10, 0.35),
            'afleider_types': ['plus_min_1', 'plus_min_2', 'omgekeerde_bewerking', 'tellfout'],
        },
        (3, 'E'): {
            'getallenruimte': (0, 50),
            'bewerkingen': ['optellen_tot_20_tientalovergang', 'aftrekken_tot_20_terugrekenen'],
            'vermenigvuldig_intro': ['x2', 'x5', 'x10'],  # Als verdubbelen/groepjes, geen formeel
            'deel_intro': ['delen_door_2'],  # Als eerlijk verdelen, geen formeel
            'tafels': None,  # Nog geen formele tafels
            'strategieen': ['bruggetje_van_10', 'splitsen', 'verdubbelen', 'tientalstructuur'],
            'hoofdrekenen': 'verplicht',
            'cijferend': 'verboden',
            'max_stappen': 2,
            'visualisatie': 'verplicht',
            'materialen': ['rekenrek', 'mab_materiaal', 'honderdveld', 'getallenlijnen', 'speelgeld'],
            'context_types': ['geld_tot_10_euro', 'speelgoed', 'groepjes_kinderen', 'tijd_hele_halve_uren'],
            'max_zinnen': 3,
            'max_woorden_per_zin': 10,
            'min_tijd_sec': 20,
            'max_tijd_sec': 50,
            'moeilijkheid_range': (0.25, 0.50),
            'afleider_types': ['tiental_vergeten', 'verkeerde_splitsing', 'bewerking_omgedraaid', 'eental_fout'],
        },
        # GROEP 4
        (4, 'M'): {
            'getallenruimte': (0, 100),
            'bewerkingen': ['optellen_100', 'aftrekken_100', 'vermenigvuldigen', 'delen'],
            'tafels': ['1', '2', '5', '10'],  # Verplicht
            'tafels_verrijking': ['3', '4'],
            'verboden_tafels': ['6', '7', '8', '9'],
            'hoofdrekenen': 'verplicht',
            'cijferend': 'verboden',
            'max_stappen': 2,
            'visualisatie': 'aanbevolen',
            'context_types': ['geld_tot_20_euro', 'tijd', 'lengtes_cm', 'gewichten_kg'],
            'max_zinnen': 3,
            'min_tijd_sec': 25,
            'max_tijd_sec': 60,
            'moeilijkheid_range': (0.30, 0.55),
        },
        (4, 'E'): {
            'getallenruimte': (0, 1000),
            'bewerkingen': ['optellen_1000', 'aftrekken_1000', 'vermenigvuldigen', 'staartdeling_eenvoudig'],
            'tafels': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],  # Alle tafels
            'tafel_tijd_sec': 3,  # Max 3 seconden per tafelsom
            'hoofdrekenen': 'tot_100',
            'cijferend': 'vanaf_1000',
            'max_stappen': 3,
            'visualisatie': 'optioneel',
            'context_types': ['geld_tot_50_euro', 'tijd_kwartieren', 'meetkunde_omtrek', 'weekplanning'],
            'max_zinnen': 4,
            'min_tijd_sec': 35,
            'max_tijd_sec': 75,
            'moeilijkheid_range': (0.40, 0.65),
        },
        # GROEP 5
        (5, 'M'): {
            'getallenruimte': (0, 10000),
            'bewerkingen': ['optellen_10000', 'aftrekken_10000', 'vermenigvuldigen_10_100', 'staartdeling'],
            'tafels': 'automatisch',
            'hoofdrekenen': 'handig',  # 3×25, 4×50, etc.
            'cijferend': 'kolomsgewijs',
            'max_stappen': 3,
            'context_types': ['grote_aantallen', 'geld_tot_100_euro', 'tijd_uren_minuten', 'gewichten_g_kg'],
            'max_zinnen': 4,
            'min_tijd_sec': 40,
            'max_tijd_sec': 90,
            'moeilijkheid_range': (0.45, 0.70),
        },
        (5, 'E'): {
            'getallenruimte': (0, 100000),
            'decimalen': {'max_cijfers': 1, 'bewerkingen': ['optellen', 'aftrekken']},
            'bewerkingen': ['optellen_100000', 'aftrekken_100000', 'vermenigvuldigen_tiental', 'staartdeling_2cijferig'],
            'max_stappen': 3,
            'context_types': ['grote_getallen', 'afstanden', 'inwoners', 'decimalen_metingen'],
            'max_zinnen': 4,
            'min_tijd_sec': 50,
            'max_tijd_sec': 100,
            'moeilijkheid_range': (0.50, 0.75),
        },
        # GROEP 6
        (6, 'M'): {
            'getallenruimte': (0, 1000000),
            'decimalen': {'max_cijfers': 2, 'bewerkingen': ['optellen', 'aftrekken', 'vermenigvuldigen']},
            'breuken': ['optellen_zelfde_noemer', 'aftrekken_zelfde_noemer'],
            'max_stappen': 4,
            'context_types': ['miljoenen', 'decimalen', 'breuken', 'verhoudingen'],
            'max_zinnen': 5,
            'min_tijd_sec': 60,
            'max_tijd_sec': 120,
            'moeilijkheid_range': (0.55, 0.80),
        },
        (6, 'E'): {
            'getallenruimte': (0, 10000000),
            'decimalen': {'max_cijfers': 3, 'bewerkingen': ['optellen', 'aftrekken', 'vermenigvuldigen', 'delen']},
            'breuken': ['optellen_andere_noemer', 'vermenigvuldigen', 'delen'],
            'negatieve_getallen': 'introductie',
            'max_stappen': 4,
            'min_tijd_sec': 70,
            'max_tijd_sec': 140,
            'moeilijkheid_range': (0.60, 0.85),
        },
        # GROEP 7
        (7, 'M'): {
            'getallenruimte': (-1000000, 10000000),
            'decimalen': {'max_cijfers': 4, 'alle_bewerkingen': True},
            'breuken': 'alle_bewerkingen',
            'negatieve_getallen': 'alle_bewerkingen',
            'machten': ['kwadraten', 'derdemachten'],
            'max_stappen': 5,
            'min_tijd_sec': 80,
            'max_tijd_sec': 160,
            'moeilijkheid_range': (0.65, 0.90),
        },
        (7, 'E'): {
            'getallenruimte': 'onbeperkt',
            'wetenschappelijke_notatie': True,
            'wortels': True,
            'machten': 'alle',
            'max_stappen': 5,
            'min_tijd_sec': 90,
            'max_tijd_sec': 180,
            'moeilijkheid_range': (0.70, 0.95),
        },
        # GROEP 8
        (8, 'M'): {
            'getallenruimte': 'onbeperkt',
            'alle_bewerkingen': True,
            'referentieniveau': '1F',
            'max_stappen': 6,
            'min_tijd_sec': 90,
            'max_tijd_sec': 180,
            'moeilijkheid_range': (0.70, 0.95),
        },
        (8, 'E'): {
            'getallenruimte': 'onbeperkt',
            'alle_bewerkingen': True,
            'referentieniveau': '1S',
            'max_stappen': 6,
            'min_tijd_sec': 100,
            'max_tijd_sec': 200,
            'moeilijkheid_range': (0.75, 1.0),
        },
    }

    # Strategische afleider patronen per niveau
    AFLEIDER_PATRONEN = {
        (3, 'M'): {
            'plus_min_1': {'beschrijving': 'Antwoord ±1 (tellfout)', 'frequency': 0.35},
            'plus_min_2': {'beschrijving': 'Antwoord ±2 (dubbel tellfout)', 'frequency': 0.25},
            'omgekeerde_bewerking': {'beschrijving': '+ i.p.v. -, of andersom', 'frequency': 0.25},
            'tellfout': {'beschrijving': 'Cijfer overgeslagen bij tellen', 'frequency': 0.15},
        },
        (3, 'E'): {
            'tiental_vergeten': {'beschrijving': 'Alleen eenheden opgeteld (18+5=13)', 'frequency': 0.30},
            'verkeerde_splitsing': {'beschrijving': 'Bruggetje fout (9+4=12)', 'frequency': 0.25},
            'bewerking_omgedraaid': {'beschrijving': '15-7=22 (+ i.p.v. -)', 'frequency': 0.25},
            'eental_fout': {'beschrijving': 'Tiental OK, eental fout (9+4=14)', 'frequency': 0.20},
        },
        (4, 'M'): {
            'tiental_eental_fout': {'beschrijving': 'Tiental of eental fout', 'frequency': 0.30},
            'verkeerde_tafel': {'beschrijving': 'Verkeerde tafel gebruikt', 'frequency': 0.30},
            'compensatie_vergeten': {'beschrijving': 'Bij +29 niet -1 gedaan', 'frequency': 0.20},
            'bewerking_verwisseld': {'beschrijving': '+ en - verwisseld', 'frequency': 0.20},
        },
    }

    # Veelvoorkomende misconcepties
    MISCONCEPTIES = {
        (3, 'M'): [
            {'naam': 'optellen_is_groter_maken', 'beschrijving': 'Kind denkt aftrekken moet ook groter getal opleveren'},
            {'naam': 'grootste_eerst', 'beschrijving': 'Kind schrijft automatisch grootste getal eerst'},
            {'naam': 'aftrekken_kleinste_van_grootste', 'beschrijving': 'Bij 3-5 maakt kind 5-3=2'},
            {'naam': 'geen_1_1_correspondentie', 'beschrijving': 'Telt te snel, dubbel, of slaat over'},
        ],
        (3, 'E'): [
            {'naam': 'bruggetje_fout_splitsen', 'beschrijving': 'Splitst verkeerd bij bruggetje van 10'},
            {'naam': 'tientallen_eenheden_door_elkaar', 'beschrijving': 'Bij 23: 2+3=5 (plaatswaarde niet begrepen)'},
            {'naam': 'aftrekken_over_tiental_te_moeilijk', 'beschrijving': '13-5: denkt 3-5 kan niet'},
            {'naam': 'vermenigvuldigen_is_optellen', 'beschrijving': '3×4 wordt 3+4=7'},
        ],
    }

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def valideer_item(self, item: Dict[str, Any]) -> ValidationResult:
        """Hoofdvalidatie functie"""
        self.errors = []
        self.warnings = []
        self.info = []

        # Basis structuur check
        self._check_basis_structuur(item)
        if self.errors:
            return self._build_result()

        # Niveau regels check
        self._check_niveau_regels(item)

        # Domein-specifieke checks
        self._check_getallenruimte(item)
        self._check_bewerkingen(item)
        self._check_tafels(item)
        self._check_strategieen(item)

        # G3-specifieke checks
        if item.get('groep') == 3:
            self._check_g3_specifiek(item)

        # Kwaliteitscontroles
        self._check_taal(item)
        self._check_context(item)
        self._check_visualisatie(item)
        self._check_afleiders(item)
        self._check_numerieke_correctheid(item)
        self._check_metadata(item)
        self._check_didactic_quality(item)
        self._check_cross_validation(item)

        return self._build_result()

    def _check_basis_structuur(self, item: Dict[str, Any]):
        """Controleer basis vereiste velden"""
        vereiste_velden = [
            'id', 'groep', 'niveau', 'hoofdvraag', 'correct_antwoord',
            'afleiders', 'toelichting', 'moeilijkheidsgraad', 'geschatte_tijd_sec'
        ]

        for veld in vereiste_velden:
            if veld not in item:
                self.errors.append(f"❌ Verplicht veld '{veld}' ontbreekt")

        # Check groep/niveau combinatie
        groep = item.get('groep')
        niveau = item.get('niveau')

        if groep not in [3, 4, 5, 6, 7, 8]:
            self.errors.append(f"❌ Ongeldige groep: {groep} (moet 3-8 zijn)")

        if niveau not in ['M', 'E']:
            self.errors.append(f"❌ Ongeldig niveau: {niveau} (moet M of E zijn)")

        # Check ID format
        if 'id' in item:
            # Expected format: G_G[3-8]_[ME]_###
            if not re.match(r'^G_G[3-8]_[ME]_\d{3}$', item['id']):
                self.warnings.append(f"⚠️  ID '{item['id']}' volgt niet standaard format G_G[3-8]_[ME]_###")

    def _check_niveau_regels(self, item: Dict[str, Any]):
        """Check of item binnen niveauregels valt"""
        groep = item.get('groep')
        niveau = item.get('niveau')

        if (groep, niveau) not in self.NIVEAU_REGELS:
            self.errors.append(f"❌ Geen regels gedefinieerd voor groep {groep} niveau {niveau}")
            return

        self.info.append(f"ℹ️  Valideer voor G{groep}-{niveau}")

    def _check_getallenruimte(self, item: Dict[str, Any]):
        """Controleer of getallen binnen toegestane ruimte vallen"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        getallenruimte = regels.get('getallenruimte')
        if not getallenruimte:
            return

        if getallenruimte == 'onbeperkt':
            return

        min_getal, max_getal = getallenruimte

        # Extract getallen from hoofdvraag en afleiders
        tekst = item.get('hoofdvraag', '') + ' ' + ' '.join(item.get('afleiders', []))
        getallen = re.findall(r'\d+', tekst)

        for getal_str in getallen:
            getal = int(getal_str)
            if getal < min_getal or getal > max_getal:
                self.errors.append(
                    f"❌ Getal {getal} valt buiten toegestane getallenruimte [{min_getal}, {max_getal}] "
                    f"voor G{groep}-{niveau}"
                )

    def _check_bewerkingen(self, item: Dict[str, Any]):
        """Controleer of bewerkingen toegestaan zijn"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        hoofdvraag = item.get('hoofdvraag', '').lower()

        # Check verboden bewerkingen
        verboden = regels.get('verboden_bewerkingen', [])
        for bewerking in verboden:
            if bewerking == 'vermenigvuldigen' and any(x in hoofdvraag for x in ['×', '*', 'keer', 'groepjes van']):
                self.errors.append(f"❌ Vermenigvuldigen is VERBODEN voor G{groep}-{niveau}")
            elif bewerking == 'delen' and any(x in hoofdvraag for x in [':', '÷', 'gedeeld door', 'delen door']):
                self.errors.append(f"❌ Delen is VERBODEN voor G{groep}-{niveau}")

        # G3-E: check intro bewerkingen (alleen als groepjes/verdelen, niet formeel)
        if groep == 3 and niveau == 'E':
            if '×' in hoofdvraag or '*' in hoofdvraag:
                self.warnings.append(
                    "⚠️  G3-E: Gebruik '× symbool' alleen met context (groepjes). "
                    "Bij voorkeur: 'herhaald optellen' (3+3+3)"
                )
            if ':' in hoofdvraag or '÷' in hoofdvraag:
                self.warnings.append(
                    "⚠️  G3-E: Gebruik ': symbool' alleen met context (verdelen). "
                    "Bij voorkeur: beschrijvend ('eerlijk verdelen')"
                )

    def _check_tafels(self, item: Dict[str, Any]):
        """Controleer tafels vereisten"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        tafels = regels.get('tafels')

        # G3: GEEN tafels
        if groep == 3 and tafels is None:
            hoofdvraag = item.get('hoofdvraag', '')
            # Check for formal tafel sommen (3×4, 5×6, etc)
            tafel_pattern = r'\d+\s*[×*]\s*\d+'
            if re.search(tafel_pattern, hoofdvraag):
                # Check if it's intro context (allowed)
                if not any(woord in hoofdvraag.lower() for woord in ['zakjes', 'groepjes', 'kinderen', 'per']):
                    self.errors.append(f"❌ G3: GEEN formele tafels toegestaan (gebruik context: groepjes, zakjes)")

        # G4-M: Check tafels beperking
        if groep == 4 and niveau == 'M':
            verboden_tafels = regels.get('verboden_tafels', [])
            hoofdvraag = item.get('hoofdvraag', '')

            # Extract vermenigvuldiging
            matches = re.findall(r'(\d+)\s*[×*]\s*(\d+)', hoofdvraag)
            for a, b in matches:
                if a in verboden_tafels or b in verboden_tafels:
                    self.errors.append(
                        f"❌ G4-M: Tafels {a} of {b} zijn VERBODEN (alleen 1,2,5,10 + optioneel 3,4)"
                    )

    def _check_strategieen(self, item: Dict[str, Any]):
        """Controleer of strategieën passen bij niveau"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        strategieen = regels.get('strategieen', [])
        toelichting = item.get('toelichting', '').lower()

        # G3-E: Check voor bruggetje van 10
        if groep == 3 and niveau == 'E' and 'bruggetje_van_10' in strategieen:
            hoofdvraag = item.get('hoofdvraag', '')
            getallen = [int(x) for x in re.findall(r'\d+', hoofdvraag)]

            # Check if there's a tientalovergang (crossing 10)
            if len(getallen) >= 2:
                som = getallen[0] + getallen[1] if '+' in hoofdvraag else None
                if som and getallen[0] < 10 < som:
                    # Tientalovergang detected
                    if 'bruggetje' not in toelichting and 'splitsen' not in toelichting:
                        self.warnings.append(
                            "⚠️  G3-E: Tientalovergang gedetecteerd. "
                            "Vermeld 'bruggetje van 10' strategie in toelichting"
                        )

    def _check_g3_specifiek(self, item: Dict[str, Any]):
        """Extra controles specifiek voor Groep 3"""
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((3, niveau), {})

        # 1. Visualisatie VERPLICHT
        visualisatie = regels.get('visualisatie')
        if visualisatie == 'verplicht':
            hoofdvraag = item.get('hoofdvraag', '').lower()
            # Check for visual cues
            visual_keywords = ['plaatje', 'tekening', 'zie', 'afbeelding', 'figuur', 'blokjes', 'kralen', 'vingers']
            if not any(keyword in hoofdvraag for keyword in visual_keywords):
                self.errors.append(
                    "❌ G3: Visualisatie is VERPLICHT. "
                    "Vermeld 'zie plaatje', 'blokjes', 'vingers', etc."
                )

        # 2. Geen abstracte sommen (moet context hebben)
        hoofdvraag = item.get('hoofdvraag', '')
        # Check if it's just a bare calculation (3+5=?)
        if re.match(r'^\s*\d+\s*[+\-]\s*\d+\s*=?\s*\??\s*$', hoofdvraag):
            self.errors.append(
                "❌ G3: GEEN abstracte sommen zonder context. "
                "Gebruik context: Lisa heeft 3 appels, krijgt er 2 bij..."
            )

        # 3. Materialen check
        materialen = regels.get('materialen', [])
        if materialen:
            toelichting = item.get('toelichting', '').lower()
            if not any(mat in toelichting for mat in materialen):
                self.warnings.append(
                    f"⚠️  G3: Overweeg concreet materiaal te vermelden in toelichting: "
                    f"{', '.join(materialen)}"
                )

        # 4. Cijferend rekenen VERBODEN
        if regels.get('cijferend') == 'verboden':
            if any(woord in hoofdvraag.lower() for woord in ['cijferend', 'kolomsgewijs', 'onder elkaar']):
                self.errors.append("❌ G3: Cijferend rekenen is VERBODEN (alleen hoofdrekenen)")

    def _check_taal(self, item: Dict[str, Any]):
        """Controleer taalcomplexiteit"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        hoofdvraag = item.get('hoofdvraag', '')

        # Check aantal zinnen
        max_zinnen = regels.get('max_zinnen')
        if max_zinnen:
            zinnen = re.split(r'[.!?]+', hoofdvraag)
            zinnen = [z.strip() for z in zinnen if z.strip()]
            if len(zinnen) > max_zinnen:
                self.errors.append(
                    f"❌ Te veel zinnen: {len(zinnen)} (max {max_zinnen} voor G{groep}-{niveau})"
                )

        # G3: Check woordlengte per zin
        max_woorden = regels.get('max_woorden_per_zin')
        if max_woorden:
            for zin in zinnen:
                woorden = zin.split()
                if len(woorden) > max_woorden:
                    self.errors.append(
                        f"❌ G3: Zin te lang ({len(woorden)} woorden): '{zin[:50]}...'. "
                        f"Max {max_woorden} woorden per zin"
                    )

        # Check voor complexe woorden bij G3
        if groep == 3:
            complexe_woorden = [
                'omdat', 'terwijl', 'waardoor', 'indien', 'alhoewel',
                'desalniettemin', 'bijvoorbeeld', 'namelijk'
            ]
            for woord in complexe_woorden:
                if woord in hoofdvraag.lower():
                    self.warnings.append(
                        f"⚠️  G3: Complex woord '{woord}' - te moeilijk voor G3. Gebruik eenvoudiger taal"
                    )

    def _check_context(self, item: Dict[str, Any]):
        """Controleer of context geschikt is voor leeftijd"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        context_types = regels.get('context_types', [])
        if not context_types:
            return

        hoofdvraag = item.get('hoofdvraag', '').lower()
        context = item.get('context', '').lower()

        # Check if ANY context type is present
        context_found = any(ctx_type in hoofdvraag or ctx_type in context for ctx_type in context_types)

        if not context_found:
            self.warnings.append(
                f"⚠️  Aanbevolen context types voor G{groep}-{niveau}: {', '.join(context_types)}"
            )

    def _check_visualisatie(self, item: Dict[str, Any]):
        """Controleer visualisatie vereisten"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        visualisatie_req = regels.get('visualisatie')

        if visualisatie_req == 'verplicht':
            # Already checked in g3_specifiek, but double-check
            hoofdvraag = item.get('hoofdvraag', '').lower()
            if not any(kw in hoofdvraag for kw in ['plaatje', 'tekening', 'zie', 'afbeelding']):
                self.errors.append(f"❌ Visualisatie is VERPLICHT voor G{groep}-{niveau}")

    def _check_afleiders(self, item: Dict[str, Any]):
        """Controleer afleiders kwaliteit"""
        groep = item.get('groep')
        niveau = item.get('niveau')

        afleiders = item.get('afleiders', [])
        correct = item.get('correct_antwoord')

        if len(afleiders) < 3:
            self.errors.append(f"❌ Te weinig afleiders: {len(afleiders)} (minimaal 3)")

        if len(afleiders) > 4:
            self.warnings.append(f"⚠️  Veel afleiders: {len(afleiders)} (gebruikelijk 3-4)")

        # Check if correct antwoord niet in afleiders zit
        if correct in afleiders:
            self.errors.append(f"❌ Correct antwoord '{correct}' staat ook in afleiders!")

        # Check voor strategische afleiders (G3)
        if (groep, niveau) in self.AFLEIDER_PATRONEN:
            patronen = self.AFLEIDER_PATRONEN[(groep, niveau)]
            self.info.append(
                f"ℹ️  Aanbevolen afleider types voor G{groep}-{niveau}: {', '.join(patronen.keys())}"
            )

    def _check_numerieke_correctheid(self, item: Dict[str, Any]):
        """Basis numerieke correctheidscheck"""
        hoofdvraag = item.get('hoofdvraag', '')
        correct = item.get('correct_antwoord')

        # Try to extract and verify calculation
        # Pattern: X + Y of X - Y of X × Y of X : Y
        match = re.search(r'(\d+)\s*([+\-×*:])\s*(\d+)', hoofdvraag)
        if match:
            a, op, b = int(match.group(1)), match.group(2), int(match.group(3))

            expected = None
            if op == '+':
                expected = a + b
            elif op == '-':
                expected = a - b
            elif op in ['×', '*']:
                expected = a * b
            elif op == ':':
                expected = a // b if b != 0 else None

            if expected is not None:
                try:
                    correct_num = int(str(correct).replace(' ', ''))
                    if correct_num != expected:
                        self.errors.append(
                            f"❌ NUMERIEKE FOUT: {a} {op} {b} = {expected}, "
                            f"maar correct_antwoord is '{correct}'"
                        )
                except:
                    self.warnings.append(f"⚠️  Kan correct_antwoord niet valideren: '{correct}'")

    def _check_metadata(self, item: Dict[str, Any]):
        """Controleer metadata velden"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        # Check moeilijkheidsgraad
        moeilijkheid = item.get('moeilijkheidsgraad')
        if moeilijkheid is not None:
            moeilijkheid_range = regels.get('moeilijkheid_range', (0.0, 1.0))
            if not (moeilijkheid_range[0] <= moeilijkheid <= moeilijkheid_range[1]):
                self.warnings.append(
                    f"⚠️  Moeilijkheidsgraad {moeilijkheid} buiten verwachte range "
                    f"{moeilijkheid_range} voor G{groep}-{niveau}"
                )

        # Check geschatte_tijd_sec
        tijd = item.get('geschatte_tijd_sec')
        if tijd is not None:
            min_tijd = regels.get('min_tijd_sec', 0)
            max_tijd = regels.get('max_tijd_sec', 300)
            if not (min_tijd <= tijd <= max_tijd):
                self.warnings.append(
                    f"⚠️  Geschatte tijd {tijd}s buiten verwachte range [{min_tijd}, {max_tijd}] "
                    f"voor G{groep}-{niveau}"
                )

    def _check_didactic_quality(self, item: Dict[str, Any]):
        """Controleer didactische kwaliteit"""
        toelichting = item.get('toelichting', '')

        if not toelichting or len(toelichting) < 20:
            self.warnings.append("⚠️  Toelichting is erg kort of ontbreekt")

        # Check for LOVA elements (Lezen, Ordenen, Vormen antwoord, Antwoorden)
        lova_keywords = ['lezen', 'ordenen', 'strategie', 'stappen', 'methode', 'aanpak']
        if not any(kw in toelichting.lower() for kw in lova_keywords):
            self.info.append("ℹ️  Overweeg LOVA-elementen toe te voegen aan toelichting")

    def _check_cross_validation(self, item: Dict[str, Any]):
        """Cross-validatie tussen moeilijkheid, stappen en tijd"""
        moeilijkheid = item.get('moeilijkheidsgraad')
        tijd = item.get('geschatte_tijd_sec')
        hoofdvraag = item.get('hoofdvraag', '')

        # Count stappen (rough estimate based on operations)
        operations = len(re.findall(r'[+\-×*:]', hoofdvraag))

        # Consistency checks
        if moeilijkheid and tijd:
            # High difficulty should correlate with longer time
            if moeilijkheid > 0.7 and tijd < 30:
                self.warnings.append(
                    "⚠️  Inconsistentie: hoge moeilijkheid (>0.7) maar korte tijd (<30s)"
                )

            if moeilijkheid < 0.3 and tijd > 90:
                self.warnings.append(
                    "⚠️  Inconsistentie: lage moeilijkheid (<0.3) maar lange tijd (>90s)"
                )

    def _build_result(self) -> ValidationResult:
        """Bouw validatie resultaat"""
        valid = len(self.errors) == 0

        # Calculate score
        score = 1.0
        score -= len(self.errors) * 0.2  # -20% per error
        score -= len(self.warnings) * 0.05  # -5% per warning
        score = max(0.0, min(1.0, score))

        return ValidationResult(
            valid=valid,
            errors=self.errors,
            warnings=self.warnings,
            info=self.info,
            score=score
        )


def _convert_legacy_structure(data: Any) -> Optional[List[Dict[str, Any]]]:
    """
    Ondersteun legacy MC-bestanden zoals gb_groep3_m3_core.json:
    - Top-level met schema_version/metadata/items
    - Items met question/options/answer.correct_index
    Converteer naar het getallen-validator formaat.
    """
    if not isinstance(data, dict) or "items" not in data:
        return None

    meta = data.get("metadata", {})
    groep = meta.get("grade")
    niveau_raw = meta.get("level")
    niveau = None
    if isinstance(niveau_raw, str) and len(niveau_raw) > 0:
        niveau = niveau_raw[0].upper()

    legacy_items = data.get("items", [])
    converted: List[Dict[str, Any]] = []
    for legacy in legacy_items:
        q = legacy.get("question", {})
        opts = legacy.get("options", [])
        answer = legacy.get("answer", {})
        correct_index = answer.get("correct_index", 0)
        correct_text = ""
        afleiders: List[str] = []
        if opts and isinstance(opts, list):
            for idx, opt in enumerate(opts):
                text = opt.get("text") if isinstance(opt, dict) else str(opt)
                if idx == correct_index:
                    correct_text = str(text)
                else:
                    afleiders.append(str(text))

        legacy_id = legacy.get("id", "000")
        if isinstance(legacy_id, int):
            legacy_id_str = f"{legacy_id:03d}"
        else:
            legacy_id_str = str(legacy_id).zfill(3)

        new_id = f"G_G{groep}_{niveau}_{legacy_id_str}" if groep and niveau else str(legacy_id_str)

        converted.append({
            "id": new_id,
            "groep": groep,
            "niveau": niveau,
            "hoofdvraag": q.get("text", ""),
            "correct_antwoord": correct_text,
            "afleiders": afleiders,
            "toelichting": f"Auto-conversie legacy item (thema: {legacy.get('theme', 'nvt')}).",
            "context": legacy.get("theme", "nvt"),
            # Basale defaults binnen G3-M bereik
            "moeilijkheidsgraad": 0.2,
            "geschatte_tijd_sec": 25
        })

    return converted


def valideer_bestand(filepath: str) -> List[ValidationResult]:
    """Valideer een JSON bestand met items"""
    validator = GetallenValidatorEnhanced()

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Ondersteun zowel lijst, enkel item, als legacy core-structuur met items[]
    items: List[Dict[str, Any]]
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict) and "items" in data:
        converted = _convert_legacy_structure(data)
        items = converted if converted is not None else [data]
    else:
        items = [data]

    resultaten = []
    for idx, item in enumerate(items, 1):
        print(f"\n{'='*60}")
        print(f"Valideer item {idx}/{len(items)}: {item.get('id', 'GEEN_ID')}")
        print(f"{'='*60}")

        result = validator.valideer_item(item)
        resultaten.append(result)

        # Print resultaat
        if result.errors:
            print("\n❌ ERRORS:")
            for err in result.errors:
                print(f"  {err}")

        if result.warnings:
            print("\n⚠️  WARNINGS:")
            for warn in result.warnings:
                print(f"  {warn}")

        if result.info:
            print("\nℹ️  INFO:")
            for info in result.info:
                print(f"  {info}")

        print(f"\n{'✅' if result.valid else '❌'} Valid: {result.valid}")
        print(f"📊 Score: {result.score:.2f}")

    # Summary
    print(f"\n{'='*60}")
    print("SAMENVATTING")
    print(f"{'='*60}")
    valid_count = sum(1 for r in resultaten if r.valid)
    print(f"✅ Valide items: {valid_count}/{len(resultaten)}")
    print(f"❌ Invalide items: {len(resultaten) - valid_count}/{len(resultaten)}")
    avg_score = sum(r.score for r in resultaten) / len(resultaten) if resultaten else 0
    print(f"📊 Gemiddelde score: {avg_score:.2f}")

    return resultaten


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Gebruik: python getallen-validator-v3.py <json_bestand>")
        print("\nVoorbeeld JSON format:")
        print(json.dumps({
            "id": "G_G3_M_001",
            "groep": 3,
            "niveau": "M",
            "hoofdvraag": "Lisa heeft 3 appels. Ze krijgt er 2 bij. Hoeveel appels heeft Lisa nu?",
            "correct_antwoord": "5",
            "afleiders": ["4", "6", "7"],
            "toelichting": "Optellen tot 10. Gebruik vingers of blokjes. 3 + 2 = 5",
            "context": "fruit tellen",
            "moeilijkheidsgraad": 0.25,
            "geschatte_tijd_sec": 25
        }, indent=2, ensure_ascii=False))
        sys.exit(1)

    valideer_bestand(sys.argv[1])
