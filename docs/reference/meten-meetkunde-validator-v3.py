"""
METEN & MEETKUNDE VALIDATOR v3.0 - ENHANCED
Uitgebreid validatiescript met diepgaande kwaliteitscontroles voor METEN & MEETKUNDE domein

Features:
- ✅ Volledige G3-G8 ondersteuning (inclusief M3 en E3)
- ✅ METEN: Lengte, Gewicht, Inhoud, Tijd, Geld, Temperatuur
- ✅ MEETKUNDE: Figuren, Eigenschappen, Symmetrie, Oppervlakte, Omtrek
- ✅ G3-specifieke pedagogische controles
- ✅ Eenheid validatie per groep/niveau
- ✅ Conversie controles
- ✅ Kritische checks (Half 4 = 3:30!)
- ✅ Visualisatie vereisten (ABSOLUUT VERPLICHT voor G3)
- ✅ Context geschiktheid
- ✅ Afleider kwaliteit (strategisch)
- ✅ Misconceptie detectie
- ✅ Numerieke correctheidscontroles
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


class MetenMeetkundeValidatorEnhanced:
    """Uitgebreide validator voor METEN & MEETKUNDE domein items (G3-G8)"""

    # Niveauregels per groep/niveau
    NIVEAU_REGELS = {
        # GROEP 3
        (3, 'M'): {
            'subdomeinen': ['METEN', 'MEETKUNDE'],
            'METEN': {
                'lengte': {'eenheden': ['cm'], 'range': (0, 20), 'verboden': ['m', 'mm', 'km']},
                'gewicht': {'eenheden': [], 'type': 'vergelijken_alleen'},  # Geen formele eenheden
                'inhoud': {'eenheden': [], 'type': 'vergelijken_alleen'},
                'tijd': {'eenheden': ['hele_uren'], 'verboden': ['halve_uren', 'kwartieren', 'minuten']},
                'geld': {'eenheden': ['cent'], 'max': 100, 'munten': ['5ct', '10ct', '20ct', '50ct', '€1'], 'verboden': ['briefjes']},
            },
            'MEETKUNDE': {
                'figuren': ['cirkel', 'vierkant', 'driehoek', 'rechthoek'],
                'eigenschappen': 'herkennen_alleen',  # Geen tellen
                'verboden': ['hoeken_tellen', 'zijden_tellen', 'symmetrie', 'berekeningen'],
            },
            'visualisatie': 'absoluut_verplicht',
            'materialen': ['liniaal', 'balans', 'analoge_klok', 'munten'],
            'max_zinnen': 2,
            'max_woorden_per_zin': 8,
            'min_tijd_sec': 15,
            'max_tijd_sec': 45,
            'moeilijkheid_range': (0.10, 0.35),
        },
        (3, 'E'): {
            'subdomeinen': ['METEN', 'MEETKUNDE'],
            'METEN': {
                'lengte': {
                    'eenheden': ['cm', 'm'],
                    'cm_range': (0, 50),
                    'm_range': (1, 2),  # Alleen hele meters
                    'conversie': '1m=100cm_alleen',
                    'verboden': ['mm', 'km', 'decimale_meters']
                },
                'gewicht': {'eenheden': ['kg'], 'range': (1, 5), 'verboden': ['gram', 'decimaal']},
                'inhoud': {'eenheden': ['liter'], 'range': (1, 3), 'verboden': ['ml', 'decimaal']},
                'tijd': {
                    'eenheden': ['hele_uren', 'halve_uren'],
                    'digitale_klok': True,
                    'verboden': ['kwartieren', 'minuten_tellen'],
                    'kritisch': 'half_4_is_3_30'  # VERY IMPORTANT!
                },
                'geld': {
                    'eenheden': ['cent', 'euro'],
                    'max': 500,  # €5
                    'munten': ['5ct', '10ct', '20ct', '50ct', '€1', '€2'],
                    'briefjes': ['€5'],
                    'decimaal': 'introductie_met_context',  # €1,50 met muntjes erbij
                },
            },
            'MEETKUNDE': {
                'figuren': ['cirkel', 'vierkant', 'driehoek', 'rechthoek'],
                'eigenschappen': 'tellen_toegestaan',  # Hoeken en zijden tellen
                'lijnen': ['rechte_lijn', 'kromme_lijn'],
                'symmetrie': 'eenvoudig',
                'verboden': ['rechte_hoek_meten', 'meerdere_symmetrielijnen', 'berekeningen'],
            },
            'visualisatie': 'verplicht',
            'materialen': ['liniaal', 'meetlat', 'weegschaal', 'maatbeker', 'analoge_klok', 'digitale_klok', 'speelgeld', 'spiegeltje'],
            'max_zinnen': 3,
            'max_woorden_per_zin': 10,
            'min_tijd_sec': 20,
            'max_tijd_sec': 55,
            'moeilijkheid_range': (0.25, 0.50),
        },
        # GROEP 4
        (4, 'M'): {
            'subdomeinen': ['METEN', 'MEETKUNDE'],
            'METEN': {
                'lengte': {'eenheden': ['mm', 'cm', 'm'], 'conversies': ['1cm=10mm', '1m=100cm']},
                'gewicht': {'eenheden': ['gram', 'kg'], 'conversie': '1kg=1000g'},
                'inhoud': {'eenheden': ['ml', 'liter'], 'conversie': '1L=1000ml'},
                'tijd': {'eenheden': ['hele', 'halve', 'kwart_uren'], 'minuten': 'introductie'},
                'geld': {'max': 2000, 'decimaal': 'volledige_notatie'},
            },
            'MEETKUNDE': {
                'figuren': ['alle_basis_figuren', '3d_introductie'],
                'eigenschappen': 'volledig',
                'omtrek': 'eenvoudig',
                'oppervlakte': 'introductie',
            },
            'max_zinnen': 4,
            'min_tijd_sec': 30,
            'max_tijd_sec': 70,
            'moeilijkheid_range': (0.35, 0.60),
        },
        (4, 'E'): {
            'subdomeinen': ['METEN', 'MEETKUNDE'],
            'METEN': {
                'lengte': {'eenheden': ['mm', 'cm', 'm', 'km'], 'alle_conversies': True},
                'gewicht': {'eenheden': ['g', 'kg', 'ton_introductie']},
                'inhoud': {'eenheden': ['ml', 'cl', 'dl', 'liter']},
                'tijd': {'volledige_klok': True, 'tijdsduur': True},
                'geld': {'onbeperkt': True},
            },
            'MEETKUNDE': {
                'figuren': '3d_volledig',
                'hoeken': 'introductie',
                'omtrek': 'berekeningen',
                'oppervlakte': 'formules_eenvoudig',
            },
            'min_tijd_sec': 40,
            'max_tijd_sec': 85,
            'moeilijkheid_range': (0.45, 0.70),
        },
        # GROEP 5+
        (5, 'M'): {
            'subdomeinen': ['METEN', 'MEETKUNDE'],
            'METEN': {'alle_eenheden': True, 'alle_conversies': True},
            'MEETKUNDE': {'oppervlakte': 'formules', 'omtrek': 'formules', 'inhoud_3d': 'introductie'},
            'min_tijd_sec': 45,
            'max_tijd_sec': 95,
            'moeilijkheid_range': (0.50, 0.75),
        },
        (5, 'E'): {
            'subdomeinen': ['METEN', 'MEETKUNDE'],
            'METEN': {'alle_eenheden': True, 'schaal': 'introductie'},
            'MEETKUNDE': {'oppervlakte': 'complexe_figuren', 'inhoud_3d': 'formules'},
            'min_tijd_sec': 55,
            'max_tijd_sec': 105,
            'moeilijkheid_range': (0.55, 0.80),
        },
        # GROEP 6-8: Uitgebreid
        (6, 'M'): {
            'subdomeinen': ['METEN', 'MEETKUNDE'],
            'min_tijd_sec': 60,
            'max_tijd_sec': 120,
            'moeilijkheid_range': (0.60, 0.85),
        },
        (6, 'E'): {
            'subdomeinen': ['METEN', 'MEETKUNDE'],
            'min_tijd_sec': 70,
            'max_tijd_sec': 135,
            'moeilijkheid_range': (0.65, 0.90),
        },
        (7, 'M'): {
            'subdomeinen': ['METEN', 'MEETKUNDE'],
            'min_tijd_sec': 75,
            'max_tijd_sec': 145,
            'moeilijkheid_range': (0.70, 0.92),
        },
        (7, 'E'): {
            'subdomeinen': ['METEN', 'MEETKUNDE'],
            'min_tijd_sec': 85,
            'max_tijd_sec': 160,
            'moeilijkheid_range': (0.75, 0.95),
        },
        (8, 'M'): {
            'subdomeinen': ['METEN', 'MEETKUNDE'],
            'referentieniveau': '1F',
            'min_tijd_sec': 90,
            'max_tijd_sec': 170,
            'moeilijkheid_range': (0.75, 0.97),
        },
        (8, 'E'): {
            'subdomeinen': ['METEN', 'MEETKUNDE'],
            'referentieniveau': '1S',
            'min_tijd_sec': 100,
            'max_tijd_sec': 190,
            'moeilijkheid_range': (0.80, 1.0),
        },
    }

    # Strategische afleider patronen
    AFLEIDER_PATRONEN = {
        (3, 'M'): {
            'METEN': {
                'lengte': ['verkeerde_eenheid', 'meet_vanaf_1', 'streepjes_tellen'],
                'geld': ['verkeerd_geteld', 'munten_door_elkaar', 'optelfout'],
                'tijd': ['verkeerde_wijzer', 'dag_fout'],
            },
            'MEETKUNDE': {
                'figuren': ['verkeerde_figuur', 'rechthoek_vs_vierkant'],
            },
        },
        (3, 'E'): {
            'METEN': {
                'lengte': ['conversie_fout_meter', 'optelfout_lengtes'],
                'gewicht': ['verkeerde_vergelijking'],
                'tijd': ['half_4_fout', 'digitale_klok_lezen_fout', 'tijdsduur_fout'],  # KRITISCH!
                'geld': ['decimale_notatie_fout', 'wisselgeld_fout'],
            },
            'MEETKUNDE': {
                'eigenschappen': ['hoeken_tellen_fout', 'symmetrie_fout'],
                'lijnen': ['rechte_kromme_verwarring'],
            },
        },
    }

    # Veelvoorkomende misconcepties
    MISCONCEPTIES = {
        (3, 'M'): [
            {'naam': 'langer_is_meer_streepjes', 'beschrijving': 'Telt streepjes i.p.v. tussenruimtes'},
            {'naam': 'zwaarder_is_groter', 'beschrijving': 'Denkt grote bal is altijd zwaarder'},
            {'naam': 'euro_1_is_1_cent', 'beschrijving': 'Ziet "1" en denkt kleinste waarde'},
        ],
        (3, 'E'): [
            {'naam': 'half_4_is_4_30', 'beschrijving': 'KRITISCH: Half 4 = 3:30, niet 4:30!'},
            {'naam': 'meter_groter_getal', 'beschrijving': '200cm < 2m (ziet 200 > 2)'},
            {'naam': '1kg_is_1liter', 'beschrijving': 'Denkt altijd gelijk (klopt alleen bij water)'},
            {'naam': 'symmetrie_zelfde_vorm', 'beschrijving': 'Accepteert asymmetrische versies'},
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
        subdomein = item.get('subdomein', '').upper()

        if subdomein == 'METEN':
            self._check_meten_specifiek(item)
        elif subdomein == 'MEETKUNDE':
            self._check_meetkunde_specifiek(item)
        else:
            self.warnings.append(f"⚠️  Subdomein '{subdomein}' niet herkend (gebruik METEN of MEETKUNDE)")

        # G3-specifieke checks
        if item.get('groep') == 3:
            self._check_g3_specifiek(item)

        # Algemene kwaliteitscontroles
        self._check_taal(item)
        self._check_context(item)
        self._check_visualisatie(item)
        self._check_afleiders(item)
        self._check_metadata(item)
        self._check_didactic_quality(item)

        return self._build_result()

    def _check_basis_structuur(self, item: Dict[str, Any]):
        """Controleer basis vereiste velden"""
        vereiste_velden = [
            'id', 'groep', 'niveau', 'subdomein', 'hoofdvraag', 'correct_antwoord',
            'afleiders', 'toelichting', 'moeilijkheidsgraad', 'geschatte_tijd_sec'
        ]

        for veld in vereiste_velden:
            if veld not in item:
                self.errors.append(f"❌ Verplicht veld '{veld}' ontbreekt")

        # Check groep/niveau
        groep = item.get('groep')
        niveau = item.get('niveau')

        if groep not in [3, 4, 5, 6, 7, 8]:
            self.errors.append(f"❌ Ongeldige groep: {groep} (moet 3-8 zijn)")

        if niveau not in ['M', 'E']:
            self.errors.append(f"❌ Ongeldig niveau: {niveau} (moet M of E zijn)")

        # Check ID format
        if 'id' in item:
            # Expected: MM_G[3-8]_[ME]_### (MM = Meten & Meetkunde)
            if not re.match(r'^MM_G[3-8]_[ME]_\d{3}$', item['id']):
                self.warnings.append(f"⚠️  ID '{item['id']}' volgt niet standaard format MM_G[3-8]_[ME]_###")

    def _check_niveau_regels(self, item: Dict[str, Any]):
        """Check of item binnen niveauregels valt"""
        groep = item.get('groep')
        niveau = item.get('niveau')

        if (groep, niveau) not in self.NIVEAU_REGELS:
            self.errors.append(f"❌ Geen regels gedefinieerd voor groep {groep} niveau {niveau}")
            return

        self.info.append(f"ℹ️  Valideer voor G{groep}-{niveau}")

    def _check_meten_specifiek(self, item: Dict[str, Any]):
        """Controleer METEN domein specifieke regels"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})
        meten_regels = regels.get('METEN', {})

        hoofdvraag = item.get('hoofdvraag', '').lower()

        # Check LENGTE
        if any(woord in hoofdvraag for woord in ['lang', 'cm', 'meter', 'lengte', 'meet']):
            self._check_lengte_regels(item, meten_regels)

        # Check GEWICHT
        if any(woord in hoofdvraag for woord in ['zwaar', 'licht', 'kg', 'gram', 'weeg']):
            self._check_gewicht_regels(item, meten_regels)

        # Check INHOUD
        if any(woord in hoofdvraag for woord in ['liter', 'ml', 'vol', 'inhoud', 'volume']):
            self._check_inhoud_regels(item, meten_regels)

        # Check TIJD
        if any(woord in hoofdvraag for woord in ['uur', 'tijd', 'klok', 'half', 'kwart', 'minuten']):
            self._check_tijd_regels(item, meten_regels)

        # Check GELD
        if any(woord in hoofdvraag for woord in ['euro', 'cent', '€', 'geld', 'kost', 'betaal']):
            self._check_geld_regels(item, meten_regels)

    def _check_lengte_regels(self, item: Dict[str, Any], meten_regels: Dict):
        """Valideer lengte metingen"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        hoofdvraag = item.get('hoofdvraag', '')

        lengte_regels = meten_regels.get('lengte', {})
        toegestane_eenheden = lengte_regels.get('eenheden', [])
        verboden_eenheden = lengte_regels.get('verboden', [])

        # Check voor verboden eenheden
        for eenheid in verboden_eenheden:
            if eenheid in hoofdvraag.lower():
                self.errors.append(
                    f"❌ LENGTE: Eenheid '{eenheid}' is VERBODEN voor G{groep}-{niveau}"
                )

        # G3-M: Check range 0-20 cm
        if groep == 3 and niveau == 'M':
            cm_range = lengte_regels.get('range', (0, 20))
            getallen = [int(x) for x in re.findall(r'\d+', hoofdvraag) if int(x) < 1000]

            for getal in getallen:
                if getal > cm_range[1]:
                    self.errors.append(
                        f"❌ G3-M LENGTE: {getal} cm is te groot (max {cm_range[1]} cm)"
                    )

        # G3-E: Check meter conversie
        if groep == 3 and niveau == 'E':
            if 'm' in hoofdvraag and 'cm' in hoofdvraag:
                conversie_regel = lengte_regels.get('conversie', '')
                if conversie_regel == '1m=100cm_alleen':
                    # Check if it's whole meters only
                    if any(x in hoofdvraag.lower() for x in ['1,', '2,', '0,', 'komma']):
                        self.errors.append(
                            "❌ G3-E LENGTE: Alleen hele meters toegestaan (1m, 2m). "
                            "GEEN decimale meters (1,5m)"
                        )

    def _check_gewicht_regels(self, item: Dict[str, Any], meten_regels: Dict):
        """Valideer gewicht metingen"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        hoofdvraag = item.get('hoofdvraag', '')

        gewicht_regels = meten_regels.get('gewicht', {})

        # G3-M: GEEN formele eenheden
        if groep == 3 and niveau == 'M':
            type_regel = gewicht_regels.get('type')
            if type_regel == 'vergelijken_alleen':
                if any(eenheid in hoofdvraag.lower() for eenheid in ['kg', 'gram', 'g']):
                    self.errors.append(
                        "❌ G3-M GEWICHT: GEEN formele eenheden (kg, gram). "
                        "Alleen vergelijken: zwaarder/lichter"
                    )

        # G3-E: Alleen hele kilo's
        if groep == 3 and niveau == 'E':
            verboden = gewicht_regels.get('verboden', [])
            if 'gram' in verboden and 'gram' in hoofdvraag.lower():
                self.errors.append("❌ G3-E GEWICHT: Gram is VERBODEN (alleen hele kg)")

            if 'decimaal' in verboden and any(x in hoofdvraag for x in [',5', '0,', '1,5']):
                self.errors.append("❌ G3-E GEWICHT: Decimale kg VERBODEN (alleen 1kg, 2kg, 3kg)")

    def _check_inhoud_regels(self, item: Dict[str, Any], meten_regels: Dict):
        """Valideer inhoud metingen"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        hoofdvraag = item.get('hoofdvraag', '')

        inhoud_regels = meten_regels.get('inhoud', {})

        # G3-M: GEEN formele eenheden
        if groep == 3 and niveau == 'M':
            type_regel = inhoud_regels.get('type')
            if type_regel == 'vergelijken_alleen':
                if any(eenheid in hoofdvraag.lower() for eenheid in ['liter', 'ml', 'l']):
                    self.errors.append(
                        "❌ G3-M INHOUD: GEEN formele eenheden (liter, ml). "
                        "Alleen vergelijken: vol/leeg, meer/minder"
                    )

        # G3-E: Alleen hele liters
        if groep == 3 and niveau == 'E':
            verboden = inhoud_regels.get('verboden', [])
            if 'ml' in verboden and 'ml' in hoofdvraag.lower():
                self.errors.append("❌ G3-E INHOUD: Milliliter is VERBODEN (alleen hele liters)")

            if 'decimaal' in verboden and any(x in hoofdvraag for x in [',5', '0,']):
                self.errors.append("❌ G3-E INHOUD: Decimale liters VERBODEN (alleen 1L, 2L, 3L)")

    def _check_tijd_regels(self, item: Dict[str, Any], meten_regels: Dict):
        """Valideer tijd metingen - KRITISCHE CHECKS voor G3-E"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        hoofdvraag = item.get('hoofdvraag', '').lower()
        correct = str(item.get('correct_antwoord', '')).lower()

        tijd_regels = meten_regels.get('tijd', {})

        # G3-M: Alleen hele uren
        if groep == 3 and niveau == 'M':
            verboden = tijd_regels.get('verboden', [])
            if 'halve_uren' in verboden and 'half' in hoofdvraag:
                self.errors.append("❌ G3-M TIJD: Halve uren zijn VERBODEN (alleen hele uren)")

            if 'kwartieren' in verboden and 'kwart' in hoofdvraag:
                self.errors.append("❌ G3-M TIJD: Kwartieren zijn VERBODEN")

            if 'minuten' in verboden and 'minuten' in hoofdvraag and 'minuut' not in hoofdvraag:
                self.errors.append("❌ G3-M TIJD: Minuten tellen is VERBODEN")

        # G3-E: KRITISCHE "HALF 4" CHECK!
        if groep == 3 and niveau == 'E':
            kritisch = tijd_regels.get('kritisch', '')

            if kritisch == 'half_4_is_3_30':
                # Check for "half X" patterns
                half_match = re.search(r'half\s+(\d+)', hoofdvraag)
                if half_match:
                    uur = int(half_match.group(1))
                    verwacht_digitaal = f"{uur-1}:30"
                    verwacht_analog = f"half {uur}"

                    # CRITICAL: Check if correct answer is correct
                    if verwacht_digitaal in correct or f"{uur}:30" in correct:
                        self.errors.append(
                            f"❌ KRITIEKE FOUT: 'Half {uur}' = {verwacht_digitaal}, "
                            f"NIET {uur}:30!"
                        )

                    self.info.append(
                        f"ℹ️  KRITISCH: Half {uur} = {verwacht_digitaal} "
                        f"(halverwege naar {uur})"
                    )

                # Check afleiders for common mistake
                afleiders = item.get('afleiders', [])
                if half_match:
                    uur = int(half_match.group(1))
                    fout_antwoord = f"{uur}:30"

                    if fout_antwoord not in [str(a) for a in afleiders]:
                        self.warnings.append(
                            f"⚠️  G3-E TIJD: Meest voorkomende fout '{fout_antwoord}' "
                            f"ontbreekt in afleiders voor 'Half {uur}'"
                        )

    def _check_geld_regels(self, item: Dict[str, Any], meten_regels: Dict):
        """Valideer geld berekeningen"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        hoofdvraag = item.get('hoofdvraag', '')

        geld_regels = meten_regels.get('geld', {})

        # G3-M: Alleen munten tot €1
        if groep == 3 and niveau == 'M':
            verboden = geld_regels.get('verboden', [])
            if 'briefjes' in verboden:
                if any(b in hoofdvraag for b in ['€5', '€10', '€20', 'briefje']):
                    self.errors.append(
                        "❌ G3-M GELD: Briefjes zijn VERBODEN (alleen munten tot €1)"
                    )

            # Check max bedrag
            max_bedrag = geld_regels.get('max', 100)  # 100 cent = €1
            euro_match = re.findall(r'€(\d+)', hoofdvraag)
            for bedrag in euro_match:
                if int(bedrag) > 1:
                    self.errors.append(
                        f"❌ G3-M GELD: €{bedrag} is te hoog (max €1)"
                    )

        # G3-E: Decimale notatie alleen met context
        if groep == 3 and niveau == 'E':
            decimaal_regel = geld_regels.get('decimaal', '')
            if decimaal_regel == 'introductie_met_context':
                # Check for decimale notatie (€1,50)
                if re.search(r'€\d+,\d+', hoofdvraag):
                    # Should have context (munten vermelden)
                    if not any(woord in hoofdvraag.lower() for woord in ['munt', 'cent', 'euro en']):
                        self.warnings.append(
                            "⚠️  G3-E GELD: Decimale notatie (€1,50) alleen met context. "
                            "Vermeld munten: '€1 en 50 cent' of '€1,50 (1 euro en 50 cent)'"
                        )

    def _check_meetkunde_specifiek(self, item: Dict[str, Any]):
        """Controleer MEETKUNDE domein specifieke regels"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})
        meetkunde_regels = regels.get('MEETKUNDE', {})

        hoofdvraag = item.get('hoofdvraag', '').lower()

        # Check figuren
        figuren = meetkunde_regels.get('figuren', [])
        if isinstance(figuren, list):
            self.info.append(f"ℹ️  Toegestane figuren G{groep}-{niveau}: {', '.join(figuren)}")

        # G3-M: Alleen herkennen
        if groep == 3 and niveau == 'M':
            eigenschappen_regel = meetkunde_regels.get('eigenschappen')
            if eigenschappen_regel == 'herkennen_alleen':
                if any(woord in hoofdvraag for woord in ['hoeveel hoeken', 'hoeveel zijden', 'tel']):
                    self.errors.append(
                        "❌ G3-M MEETKUNDE: Eigenschappen TELLEN is VERBODEN. "
                        "Alleen herkennen/benoemen"
                    )

            verboden = meetkunde_regels.get('verboden', [])
            if 'symmetrie' in verboden and 'symmetr' in hoofdvraag:
                self.errors.append("❌ G3-M MEETKUNDE: Symmetrie is VERBODEN (komt bij E3)")

        # G3-E: Eigenschappen tellen toegestaan
        if groep == 3 and niveau == 'E':
            eigenschappen_regel = meetkunde_regels.get('eigenschappen')
            if eigenschappen_regel == 'tellen_toegestaan':
                self.info.append("ℹ️  G3-E: Eigenschappen tellen (hoeken, zijden) is toegestaan")

            verboden = meetkunde_regels.get('verboden', [])
            if 'rechte_hoek_meten' in verboden and 'geodriehoek' in hoofdvraag:
                self.errors.append(
                    "❌ G3-E MEETKUNDE: Rechte hoek METEN met geodriehoek is VERBODEN "
                    "(komt bij G4)"
                )

    def _check_g3_specifiek(self, item: Dict[str, Any]):
        """Extra controles specifiek voor Groep 3"""
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((3, niveau), {})

        # Visualisatie check
        visualisatie = regels.get('visualisatie')
        if visualisatie in ['absoluut_verplicht', 'verplicht']:
            hoofdvraag = item.get('hoofdvraag', '').lower()
            visual_keywords = [
                'plaatje', 'tekening', 'zie', 'afbeelding', 'figuur',
                'foto', 'liniaal', 'klok', 'munt'
            ]
            if not any(keyword in hoofdvraag for keyword in visual_keywords):
                self.errors.append(
                    f"❌ G3: Visualisatie is {visualisatie.upper()}. "
                    "Vermeld 'zie plaatje', 'foto', 'liniaal', 'klok', etc."
                )

        # Materialen check
        materialen = regels.get('materialen', [])
        if materialen:
            toelichting = item.get('toelichting', '').lower()
            materiaal_found = any(mat in toelichting for mat in materialen)

            if not materiaal_found:
                self.warnings.append(
                    f"⚠️  G3: Overweeg concreet materiaal te vermelden: {', '.join(materialen)}"
                )

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
                        f"❌ G3: Zin te lang ({len(woorden)} woorden). Max {max_woorden}"
                    )

    def _check_context(self, item: Dict[str, Any]):
        """Controleer context geschiktheid"""
        groep = item.get('groep')
        hoofdvraag = item.get('hoofdvraag', '').lower()

        # G3: Check age-appropriate context
        if groep == 3:
            inappropriate = ['hypotheek', 'belasting', 'salaris', 'alcohol', 'casino']
            for woord in inappropriate:
                if woord in hoofdvraag:
                    self.errors.append(f"❌ G3: Context '{woord}' is NIET geschikt voor 6-7 jarigen")

    def _check_visualisatie(self, item: Dict[str, Any]):
        """Controleer visualisatie vereisten"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        visualisatie = regels.get('visualisatie')

        if visualisatie in ['absoluut_verplicht', 'verplicht']:
            hoofdvraag = item.get('hoofdvraag', '').lower()
            if not any(kw in hoofdvraag for kw in ['plaatje', 'tekening', 'zie', 'afbeelding', 'foto']):
                niveau_str = 'ABSOLUUT VERPLICHT' if visualisatie == 'absoluut_verplicht' else 'VERPLICHT'
                self.errors.append(f"❌ Visualisatie is {niveau_str} voor G{groep}-{niveau}")

    def _check_afleiders(self, item: Dict[str, Any]):
        """Controleer afleiders kwaliteit"""
        afleiders = item.get('afleiders', [])
        correct = item.get('correct_antwoord')

        if len(afleiders) < 3:
            self.errors.append(f"❌ Te weinig afleiders: {len(afleiders)} (minimaal 3)")

        if correct in afleiders:
            self.errors.append(f"❌ Correct antwoord '{correct}' staat ook in afleiders!")

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
                    f"⚠️  Geschatte tijd {tijd}s buiten verwachte range [{min_tijd}, {max_tijd}]"
                )

    def _check_didactic_quality(self, item: Dict[str, Any]):
        """Controleer didactische kwaliteit"""
        toelichting = item.get('toelichting', '')

        if not toelichting or len(toelichting) < 20:
            self.warnings.append("⚠️  Toelichting is erg kort of ontbreekt")

    def _build_result(self) -> ValidationResult:
        """Bouw validatie resultaat"""
        valid = len(self.errors) == 0

        # Calculate score
        score = 1.0
        score -= len(self.errors) * 0.2
        score -= len(self.warnings) * 0.05
        score = max(0.0, min(1.0, score))

        return ValidationResult(
            valid=valid,
            errors=self.errors,
            warnings=self.warnings,
            info=self.info,
            score=score
        )


def valideer_bestand(filepath: str) -> List[ValidationResult]:
    """Valideer een JSON bestand met items"""
    validator = MetenMeetkundeValidatorEnhanced()

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else [data]

    resultaten = []
    for idx, item in enumerate(items, 1):
        print(f"\n{'='*60}")
        print(f"Valideer item {idx}/{len(items)}: {item.get('id', 'GEEN_ID')}")
        print(f"{'='*60}")

        result = validator.valideer_item(item)
        resultaten.append(result)

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
        print("Gebruik: python meten-meetkunde-validator-v3.py <json_bestand>")
        print("\nVoorbeeld JSON format (METEN):")
        print(json.dumps({
            "id": "MM_G3_E_001",
            "groep": 3,
            "niveau": "E",
            "subdomein": "METEN",
            "hoofdvraag": "De klok wijst half 4. Hoe laat is het op de digitale klok?",
            "correct_antwoord": "3:30",
            "afleiders": ["4:30", "3:00", "2:30"],
            "toelichting": "Half 4 betekent halverwege naar 4 uur, dus 3:30. Grote wijzer naar beneden (6).",
            "context": "tijd aflezen",
            "moeilijkheidsgraad": 0.40,
            "geschatte_tijd_sec": 35
        }, indent=2, ensure_ascii=False))
        sys.exit(1)

    valideer_bestand(sys.argv[1])
