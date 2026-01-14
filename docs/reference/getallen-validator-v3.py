"""
GETALLEN VALIDATOR v5.0 - IMPROVED PRODUCTION VERSION
Verbeterde validatie voor GETALLEN EN BEWERKINGEN domein (G3-G8)

Belangrijke wijzigingen t.o.v. v4:
- ✅ Breuken uitgesloten (aparte oefening)
- ✅ Tafelkennis G4-M uitgebreid (nu incl. 3 en 4)
- ✅ Visualisatie G3-E: sterk aanbevolen ipv verplicht
- ✅ Negatieve getallen vanaf G6-E (was G7)
- ✅ Semantische context-bewerking validatie
- ✅ Uitkomst binnen getallenruimte check
- ✅ Verbeterde afleider kwaliteitscontrole
- ✅ Talige complexiteit (bijzinnen G3)
- ✅ Distractorverdeling clustering check
- ✅ Hoofdrekenen "handig" met concrete voorbeelden
- ✅ Uitgebreide didactische kwaliteitscheck
- ✅ Betere regex voor bewerkingen (ook tekstueel)
- ✅ Legacy conversie met None voor onbekende waarden
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
import math


@dataclass
class ValidationResult:
    """Uitgebreid resultaat van validatie"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    info: List[str] = field(default_factory=list)
    score: float = 0.0  # 0.0 - 1.0
    quality_breakdown: Dict[str, float] = field(default_factory=dict)


class GetallenValidatorImproved:
    """
    Verbeterde validator voor GETALLEN EN BEWERKINGEN domein (G3-G8)
    
    Exclusies:
    - Breuken (aparte oefening)
    - Kommagetallen uitgebreid (alleen basis decimalen in hogere groepen)
    - Verhoudingen (aparte oefening)
    """

    # =====================================================================
    # NIVEAU REGELS PER GROEP/NIVEAU
    # =====================================================================
    NIVEAU_REGELS = {
        # GROEP 3 MIDDEN (M3)
        (3, 'M'): {
            'getallenruimte': (0, 20),
            'bewerkingen': ['optellen_tot_10', 'aftrekken_tot_10'],
            'verboden_bewerkingen': ['vermenigvuldigen', 'delen', 'tientalovergang'],
            'tafels': None,
            'strategieen': ['tellen', 'getalbeelden', 'splitsen_tot_10', 'vingers_gebruiken'],
            'hoofdrekenen': 'verplicht',
            'cijferend': 'verboden',
            'max_stappen': 1,
            'visualisatie': 'verplicht',
            'materialen': ['rekenrek', 'mab_blokjes', 'vingers', 'dobbelstenen', 'telraam'],
            'context_types': ['speelgoed', 'snoep', 'fruit', 'dieren', 'vingers', 'dobbelstenen'],
            'max_zinnen': 2,
            'max_woorden_per_zin': 8,
            'bijzinnen_toegestaan': False,  # NIEUW: Geen "die", "dat", "omdat" etc.
            'min_tijd_sec': 15,
            'max_tijd_sec': 40,
            'moeilijkheid_range': (0.10, 0.35),
            'afleider_types': ['plus_min_1', 'plus_min_2', 'omgekeerde_bewerking', 'tellfout'],
            'vraagwoorden': ['hoeveel', 'tel', 'bereken'],  # NIEUW: Toegestane vraagwoorden
        },
        
        # GROEP 3 EIND (E3)
        (3, 'E'): {
            'getallenruimte': (0, 50),
            'bewerkingen': [
                'optellen_tot_20_tientalovergang',
                'aftrekken_tot_20_tientalovergang',  # AANGEPAST: Expliciet tientalovergang
                'aftrekken_tot_20_terugrekenen',  # Invulopgaven: 14 - ? = 7
            ],
            'vermenigvuldig_intro': ['x2_verdubbelen', 'x5_groepjes', 'x10_groepjes'],
            'deel_intro': ['delen_door_2_halveren', 'delen_eerlijk_verdelen'],
            'tafels': None,  # Nog geen formele tafels
            'strategieen': [
                'bruggetje_van_10',
                'splitsen',
                'verdubbelen',
                'halveren',
                'tientalstructuur',
                'getallenlijnen',
            ],
            'hoofdrekenen': 'verplicht',
            'cijferend': 'verboden',
            'max_stappen': 2,
            'visualisatie': 'sterk_aanbevolen',  # AANGEPAST: Was 'verplicht'
            'materialen': ['rekenrek', 'mab_materiaal', 'honderdveld', 'getallenlijnen', 'speelgeld'],
            'context_types': ['geld_tot_10_euro', 'speelgoed', 'groepjes_kinderen', 'tijd_hele_halve_uren'],
            'max_zinnen': 3,
            'max_woorden_per_zin': 10,
            'bijzinnen_toegestaan': False,
            'min_tijd_sec': 20,
            'max_tijd_sec': 50,
            'moeilijkheid_range': (0.25, 0.50),
            'afleider_types': [
                'tiental_vergeten',
                'verkeerde_splitsing',
                'bewerking_omgedraaid',
                'eental_fout',
            ],
            'vraagwoorden': ['hoeveel', 'bereken', 'wat is', 'tel'],
        },
        
        # GROEP 4 MIDDEN (M4)
        (4, 'M'): {
            'getallenruimte': (0, 100),
            'bewerkingen': ['optellen_100', 'aftrekken_100', 'vermenigvuldigen', 'delen'],
            'tafels': ['1', '2', '3', '4', '5', '10'],  # AANGEPAST: 3 en 4 toegevoegd
            'tafels_verrijking': ['6', '7', '8', '9'],
            'tafel_tijd_sec': 5,  # Max 5 seconden per tafelsom G4-M
            'hoofdrekenen': 'verplicht',
            'cijferend': 'verboden',
            'max_stappen': 2,
            'visualisatie': 'aanbevolen',
            'strategieen': [
                'kolomsgewijs_optellen',
                'kolomsgewijs_aftrekken',
                'tafels_automatisch',
                'groepsgewijze_vermenigvuldiging',
            ],
            'context_types': ['geld_tot_20_euro', 'tijd_uren', 'lengtes_cm_m', 'gewichten_kg'],
            'max_zinnen': 3,
            'max_woorden_per_zin': 12,
            'bijzinnen_toegestaan': True,  # Vanaf G4 wel toegestaan
            'min_tijd_sec': 25,
            'max_tijd_sec': 60,
            'moeilijkheid_range': (0.30, 0.55),
            'afleider_types': [
                'tafel_verwisseling',
                'tiental_vergeten',
                'verkeerde_kolom',
                'bewerkingsverwarring',
            ],
        },
        
        # GROEP 4 EIND (E4)
        (4, 'E'): {
            'getallenruimte': (0, 1000),
            'bewerkingen': [
                'optellen_1000',
                'aftrekken_1000',
                'vermenigvuldigen',
                'staartdeling_eenvoudig',
            ],
            'tafels': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],  # Alle tafels
            'tafel_tijd_sec': 3,  # Max 3 seconden per tafelsom G4-E
            'hoofdrekenen': 'tot_100',
            'cijferend': 'vanaf_100',  # AANGEPAST: Was 'vanaf_1000'
            'max_stappen': 3,
            'visualisatie': 'optioneel',
            'strategieen': [
                'kolomsgewijs_met_lenen',
                'staartdeling',
                'tafels_automatisch',
                'schatten_afronden',
            ],
            'context_types': [
                'geld_tot_50_euro',
                'tijd_kwartieren',
                'meetkunde_omtrek',
                'weekplanning',
            ],
            'max_zinnen': 4,
            'max_woorden_per_zin': 14,
            'bijzinnen_toegestaan': True,
            'min_tijd_sec': 35,
            'max_tijd_sec': 75,
            'moeilijkheid_range': (0.40, 0.65),
        },
        
        # GROEP 5 MIDDEN (M5)
        (5, 'M'): {
            'getallenruimte': (0, 10000),
            'bewerkingen': [
                'optellen_10000',
                'aftrekken_10000',
                'vermenigvuldigen_meercijferig',
                'staartdeling',
            ],
            'tafels': 'automatisch',
            'handig_rekenen': [  # NIEUW: Expliciete lijst
                'vermenigvuldigen_met_10_100_1000',
                'delen_door_10_100',
                'vermenigvuldigen_met_25',  # 4×25=100
                'vermenigvuldigen_met_50',  # 2×50=100
                'verdubbelen_halveren_strategie',
            ],
            'hoofdrekenen': 'handig',
            'cijferend': 'kolomsgewijs',
            'max_stappen': 3,
            'context_types': [
                'grote_aantallen',
                'geld_tot_100_euro',
                'tijd_uren_minuten',
                'gewichten_g_kg',
                'afstanden_m_km',
            ],
            'max_zinnen': 4,
            'max_woorden_per_zin': 15,
            'bijzinnen_toegestaan': True,
            'min_tijd_sec': 40,
            'max_tijd_sec': 90,
            'moeilijkheid_range': (0.45, 0.70),
        },
        
        # GROEP 5 EIND (E5)
        (5, 'E'): {
            'getallenruimte': (0, 100000),
            'decimalen': {  # BEPERKT: Alleen basis
                'max_cijfers': 1,
                'bewerkingen': ['optellen', 'aftrekken'],
                'context': ['geld_centen', 'lengtes_dm'],
            },
            'bewerkingen': [
                'optellen_100000',
                'aftrekken_100000',
                'vermenigvuldigen_tiental',
                'staartdeling_2cijferig',
            ],
            'handig_rekenen': [
                'vermenigvuldigen_met_10_100_1000',
                'delen_door_10_100',
                'vermenigvuldigen_met_25_50',
                'verdubbelen_halveren',
            ],
            'max_stappen': 3,
            'context_types': [
                'grote_getallen',
                'afstanden_km',
                'inwoners',
                'decimalen_basis',
            ],
            'max_zinnen': 4,
            'max_woorden_per_zin': 16,
            'bijzinnen_toegestaan': True,
            'min_tijd_sec': 50,
            'max_tijd_sec': 100,
            'moeilijkheid_range': (0.50, 0.75),
        },
        
        # GROEP 6 MIDDEN (M6)
        (6, 'M'): {
            'getallenruimte': (0, 1000000),
            'decimalen': {
                'max_cijfers': 2,
                'bewerkingen': ['optellen', 'aftrekken', 'vermenigvuldigen'],
                'context': ['geld', 'lengtes', 'gewichten'],
            },
            'bewerkingen': [
                'alle_bewerkingen_binnen_miljoen',
                'decimalen_optellen_aftrekken',
                'decimalen_vermenigvuldigen',
            ],
            'handig_rekenen': [
                'procent_eenvoudig',  # 10%, 50%, 25%
                'vermenigvuldigen_decimalen',
            ],
            'max_stappen': 4,
            'context_types': ['miljoenen', 'decimalen', 'procenten_basis', 'verhoudingen_basis'],
            'max_zinnen': 5,
            'max_woorden_per_zin': 18,
            'bijzinnen_toegestaan': True,
            'min_tijd_sec': 60,
            'max_tijd_sec': 120,
            'moeilijkheid_range': (0.55, 0.80),
        },
        
        # GROEP 6 EIND (E6)
        (6, 'E'): {
            'getallenruimte': (0, 10000000),
            'decimalen': {
                'max_cijfers': 3,
                'bewerkingen': ['optellen', 'aftrekken', 'vermenigvuldigen', 'delen'],
                'context': ['geld', 'lengtes', 'gewichten', 'inhoud'],
            },
            'negatieve_getallen': 'introductie_context',  # NIEUW: Was G7
            'negatieve_context': ['temperatuur', 'schuld', 'onder_zeespiegel'],
            'bewerkingen': [
                'alle_bewerkingen_binnen_10_miljoen',
                'decimalen_alle_bewerkingen',
                'negatieve_getallen_optellen_aftrekken',
            ],
            'max_stappen': 4,
            'context_types': [
                'grote_getallen',
                'decimalen',
                'negatieve_context',
                'procenten',
            ],
            'max_zinnen': 5,
            'max_woorden_per_zin': 18,
            'bijzinnen_toegestaan': True,
            'min_tijd_sec': 70,
            'max_tijd_sec': 140,
            'moeilijkheid_range': (0.60, 0.85),
        },
        
        # GROEP 7 MIDDEN (M7)
        (7, 'M'): {
            'getallenruimte': (-1000000, 10000000),
            'decimalen': {
                'max_cijfers': 4,
                'alle_bewerkingen': True,
            },
            'negatieve_getallen': 'alle_bewerkingen',
            'machten': ['kwadraten', 'derdemachten'],
            'wortels': ['vierkantswortels_basis'],
            'bewerkingen': [
                'alle_bewerkingen',
                'negatieve_getallen_alle_bewerkingen',
                'machten_kwadraten',
            ],
            'max_stappen': 5,
            'context_types': [
                'negatieve_getallen',
                'decimalen_complex',
                'machten',
                'grote_berekeningen',
            ],
            'max_zinnen': 6,
            'max_woorden_per_zin': 20,
            'bijzinnen_toegestaan': True,
            'min_tijd_sec': 80,
            'max_tijd_sec': 160,
            'moeilijkheid_range': (0.65, 0.90),
        },
        
        # GROEP 7 EIND (E7)
        (7, 'E'): {
            'getallenruimte': 'onbeperkt',
            'wetenschappelijke_notatie': True,
            'wortels': ['vierkantswortels', 'derdemachtswortels'],
            'machten': 'alle',
            'bewerkingen': [
                'alle_bewerkingen',
                'wetenschappelijke_notatie',
                'complexe_berekeningen',
            ],
            'max_stappen': 5,
            'context_types': [
                'wetenschappelijk',
                'grote_kleine_getallen',
                'machten_wortels',
            ],
            'max_zinnen': 6,
            'max_woorden_per_zin': 22,
            'bijzinnen_toegestaan': True,
            'min_tijd_sec': 90,
            'max_tijd_sec': 180,
            'moeilijkheid_range': (0.70, 0.95),
        },
        
        # GROEP 8 MIDDEN (M8)
        (8, 'M'): {
            'getallenruimte': 'onbeperkt',
            'alle_bewerkingen': True,
            'referentieniveau': '1F',
            'bewerkingen': ['alle_bewerkingen', 'complexe_samengestelde_opgaven'],
            'max_stappen': 6,
            'context_types': ['alle', 'praktijkgericht', 'abstract'],
            'max_zinnen': 6,
            'max_woorden_per_zin': 22,
            'bijzinnen_toegestaan': True,
            'min_tijd_sec': 90,
            'max_tijd_sec': 180,
            'moeilijkheid_range': (0.70, 0.95),
        },
        
        # GROEP 8 EIND (E8)
        (8, 'E'): {
            'getallenruimte': 'onbeperkt',
            'alle_bewerkingen': True,
            'referentieniveau': '1S',
            'bewerkingen': ['alle_bewerkingen', 'havo_vwo_niveau'],
            'max_stappen': 6,
            'context_types': ['alle', 'wetenschappelijk', 'abstract'],
            'max_zinnen': 7,
            'max_woorden_per_zin': 25,
            'bijzinnen_toegestaan': True,
            'min_tijd_sec': 100,
            'max_tijd_sec': 200,
            'moeilijkheid_range': (0.75, 1.0),
        },
    }

    # =====================================================================
    # AFLEIDER TAXONOMIE (Cito-aligned)
    # =====================================================================
    AFLEIDER_CATEGORIEN = {
        'strategisch': [
            'plus_min_1',
            'plus_min_2',
            'tiental_vergeten',
            'verkeerde_splitsing',
            'bewerkingsverwarring',
            'tafel_verwisseling',
            'cijfer_omgedraaid',
        ],
        'empirisch': [
            'tellfout',
            'afrondfout',
            'verkeerde_kolom',
            'leesfout',
        ],
        'misconceptie': [
            'omgekeerde_bewerking',
            'bewerking_omgedraaid',
            'negatief_altijd_kleiner',  # -5 < -10 (fout!)
            'decimaal_vergroot',  # 3.4 > 3.12 (fout!)
            'vermenigvuldigen_vergroot_altijd',  # ×0.5 vergroot niet
        ],
    }

    # =====================================================================
    # CONTEXT-BEWERKING MAPPING (NIEUW)
    # =====================================================================
    CONTEXT_BEWERKING_MAP = {
        'optellen': [
            'bij elkaar',
            'erbij',
            'meer',
            'totaal',
            'samen',
            'in totaal',
            'krijgt erbij',
        ],
        'aftrekken': [
            'kwijt',
            'weggegeven',
            'minder',
            'over',
            'blijft over',
            'verliest',
            'geeft weg',
        ],
        'vermenigvuldigen': [
            'groepjes',
            'keer',
            'per stuk',
            'prijs per',
            'elk',
            'ieder',
            'verdubbelen',
        ],
        'delen': [
            'verdelen',
            'eerlijk verdelen',
            'groepen maken',
            'per persoon',
            'halveren',
        ],
    }

    # =====================================================================
    # STRATEGIE KEYWORDS (NIEUW)
    # =====================================================================
    STRATEGIE_KEYWORDS = [
        'bruggetje',
        'splitsen',
        'verdubbelen',
        'halveren',
        'tientalovergang',
        'kolomsgewijs',
        'staartdeling',
        'schatten',
        'afronden',
        'handig rekenen',
        'tafels',
        'groepjes',
        'getalbeeld',
        'getallenlijn',
        'rekenrek',
    ]

    # =====================================================================
    # MISCONCEPTIE KEYWORDS (NIEUW)
    # =====================================================================
    MISCONCEPTIE_KEYWORDS = [
        'misconceptie',
        'denkfout',
        'vergeet',
        'verwisselt',
        'verkeerde volgorde',
        'omgedraaid',
        'fout omdat',
    ]

    def __init__(self):
        """Initialiseer validator"""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def valideer_item(self, item: Dict[str, Any]) -> ValidationResult:
        """Valideer een enkel item volledig"""
        # Reset
        self.errors = []
        self.warnings = []
        self.info = []

        # Basis structuur
        self._check_required_fields(item)
        if self.errors:
            return self._build_result()

        # Groep/niveau validatie
        groep = item.get('groep')
        niveau = item.get('niveau', 'M')
        regels = self.NIVEAU_REGELS.get((groep, niveau))

        if not regels:
            self.errors.append(f"❌ Onbekende combinatie G{groep}-{niveau}")
            return self._build_result()

        # Voer alle checks uit
        self._check_getallenruimte(item, regels)
        self._check_bewerkingen(item, regels)
        self._check_tafels(item, regels)
        self._check_strategieen(item, regels)
        self._check_visualisatie(item, regels)
        self._check_context(item, regels)
        self._check_taal_complexiteit(item, regels)
        self._check_afleiders(item, regels)
        self._check_numerical_correctness(item)
        self._check_uitkomst_binnen_bereik(item, regels)  # NIEUW
        self._check_afleider_duplicaten(item)  # NIEUW
        self._check_afleider_clustering(item)  # NIEUW
        self._check_context_semantiek(item, regels)  # NIEUW
        self._check_moeilijkheid_tijd(item, regels)
        self._check_didactic_quality_enhanced(item, regels)  # VERBETERD
        self._check_cross_validation(item)

        return self._build_result()

    def _check_required_fields(self, item: Dict[str, Any]):
        """Controleer verplichte velden"""
        required = ['id', 'groep', 'hoofdvraag', 'correct_antwoord', 'afleiders', 'toelichting']
        for field in required:
            if field not in item or not item[field]:
                self.errors.append(f"❌ Verplicht veld '{field}' ontbreekt of is leeg")

        # Check ID format
        item_id = item.get('id', '')
        if not re.match(r'^G_G\d_[ME]_\d{3}$', item_id):
            self.warnings.append(
                f"⚠️  ID '{item_id}' volgt niet het verwachte patroon: G_G#_M/E_###"
            )

    def _check_getallenruimte(self, item: Dict[str, Any], regels: Dict[str, Any]):
        """Controleer getallenruimte per niveau"""
        hoofdvraag = item.get('hoofdvraag', '')
        getallenruimte = regels.get('getallenruimte')

        if getallenruimte == 'onbeperkt':
            return

        min_val, max_val = getallenruimte
        getallen = re.findall(r'\b\d+\b', hoofdvraag)

        for getal_str in getallen:
            getal = int(getal_str)
            if not (min_val <= getal <= max_val):
                self.errors.append(
                    f"❌ Getal {getal} valt buiten getallenruimte [{min_val}, {max_val}]"
                )

    def _check_bewerkingen(self, item: Dict[str, Any], regels: Dict[str, Any]):
        """Controleer bewerkingen in hoofdvraag"""
        hoofdvraag = item.get('hoofdvraag', '').lower()

        # Check verboden bewerkingen
        verboden = regels.get('verboden_bewerkingen', [])
        for bewerking in verboden:
            # AANGEPAST: Gebruik meer specifieke detectie voor bewerkingscontext
            if self._detect_bewerking_in_context(hoofdvraag, bewerking):
                self.errors.append(
                    f"❌ Verboden bewerking '{bewerking}' gedetecteerd in hoofdvraag"
                )

        # Check toegestane bewerkingen
        bewerkingen = regels.get('bewerkingen', [])
        if bewerkingen and not any(
            self._detect_bewerking_in_context(hoofdvraag, bew) for bew in bewerkingen
        ):
            self.info.append(
                f"ℹ️  Geen duidelijke bewerking uit lijst {bewerkingen} herkend"
            )

    def _detect_bewerking_in_context(self, tekst: str, bewerking: str) -> bool:
        """
        NIEUW: Detecteer of een bewerking daadwerkelijk in een rekenkundige context gebruikt wordt
        Voorkomt false positives zoals het woord "delen" in gewone zinnen
        """
        tekst_lower = tekst.lower()
        
        # Specifieke checks per bewerking
        if 'delen' in bewerking:
            # Check voor deelsymbolen of specifieke deelcontexten
            # AANGEPAST: alleen getal-dubbele punt-getal voor echte deelsom (niet "plaatje: 9")
            deelpatronen = [
                r'\d+\s*:\s*\d+',  # AANGEPAST: getal : getal (bijv. 12:4)
                r'\d+\s*÷\s*\d+',  # getal ÷ getal
                r'÷',  # deelsymbool op zichzelf
                r'gedeeld\s+door\s+\d',
                r'\d+\s+gedeeld\s+door',
                r'delen\s+door\s+\d',
                r'\d+\s+delen\s+door',
                r'verdeel\w*\s+\d+\s+door',
                r'\d+\s+verdeel',
            ]
            return any(re.search(patroon, tekst_lower) for patroon in deelpatronen)
        
        elif 'tientalovergang' in bewerking:
            # Check of er daadwerkelijk tientalovergang is (bijv. 7+5, 14-6)
            # Zoek naar optelling/aftrekking die over 10 gaat
            getallen = re.findall(r'\b(\d+)\s*([+\-])\s*(\d+)\b', tekst_lower)
            for num1_str, op, num2_str in getallen:
                num1, num2 = int(num1_str), int(num2_str)
                if op == '+':
                    # Tientalovergang bij optellen: eentallen > 10
                    if (num1 % 10) + (num2 % 10) >= 10 and num1 < 20 and num2 < 20:
                        return True
                elif op == '-':
                    # Tientalovergang bij aftrekken: gaan terug over 10
                    if num1 >= 10 and (num1 - num2) < 10:
                        return True
            return False
        
        else:
            # Gebruik standaard patronen voor andere bewerkingen
            patterns = self._get_bewerking_patterns(bewerking)
            return any(pattern in tekst_lower for pattern in patterns)

    def _get_bewerking_patterns(self, bewerking: str) -> List[str]:
        """
        VERBETERD: Geef tekstuele patronen voor een bewerking
        """
        patterns = {
            'optellen_tot_10': ['+', 'plus', 'erbij', 'bij elkaar', 'samen', 'totaal'],
            'aftrekken_tot_10': ['-', 'min', 'af', 'kwijt', 'over', 'minder'],
            'vermenigvuldigen': ['×', '*', 'x', 'keer', 'maal', 'groepjes van'],
            'delen': [':', '÷', 'gedeeld door', 'verdelen', 'per'],
            'tientalovergang': ['10', 'tien', 'tiental'],
        }
        return patterns.get(bewerking, [bewerking])

    def _check_tafels(self, item: Dict[str, Any], regels: Dict[str, Any]):
        """Controleer tafels per niveau"""
        hoofdvraag = item.get('hoofdvraag', '').lower()
        tafels_config = regels.get('tafels')

        if tafels_config is None:
            # Tafels niet toegestaan
            if any(sym in hoofdvraag for sym in ['×', '*', 'x', 'keer', 'maal']):
                # Check of het echt een tafel is
                numbers = re.findall(r'\b(\d+)\s*[×*x]\s*(\d+)\b', hoofdvraag)
                if numbers:
                    self.warnings.append(
                        "⚠️  Vermenigvuldiging gedetecteerd, maar tafels zijn nog niet ingevoerd op dit niveau"
                    )
        elif isinstance(tafels_config, list):
            # Specifieke tafels toegestaan
            numbers = re.findall(r'\b(\d+)\s*[×*x]\s*(\d+)\b', hoofdvraag)
            for num1, num2 in numbers:
                if num1 not in tafels_config and num2 not in tafels_config:
                    self.errors.append(
                        f"❌ Tafel van {num1}×{num2} niet toegestaan. Alleen tafels: {tafels_config}"
                    )

            # Check tafel snelheid
            tafel_tijd = regels.get('tafel_tijd_sec')
            if tafel_tijd and item.get('geschatte_tijd_sec'):
                if item['geschatte_tijd_sec'] < tafel_tijd:
                    self.warnings.append(
                        f"⚠️  Geschatte tijd {item['geschatte_tijd_sec']}s is korter dan "
                        f"minimale tafel-tijd {tafel_tijd}s"
                    )

    def _check_strategieen(self, item: Dict[str, Any], regels: Dict[str, Any]):
        """Controleer of juiste strategieën worden toegepast"""
        toelichting = item.get('toelichting', '').lower()
        strategieen = regels.get('strategieen', [])

        if not strategieen:
            return

        # Check of minstens één strategie wordt genoemd
        gevonden_strategieen = [
            strat
            for strat in strategieen
            if any(keyword in toelichting for keyword in strat.split('_'))
        ]

        if not gevonden_strategieen:
            self.warnings.append(
                f"⚠️  Geen van de aanbevolen strategieën {strategieen} genoemd in toelichting"
            )

    def _check_visualisatie(self, item: Dict[str, Any], regels: Dict[str, Any]):
        """Controleer visualisatie vereisten"""
        vis_requirement = regels.get('visualisatie')
        has_visual = item.get('has_visual', False)
        assets = item.get('assets', [])

        if vis_requirement == 'verplicht' and not has_visual and not assets:
            self.errors.append(
                "❌ Visualisatie is VERPLICHT voor dit niveau maar ontbreekt"
            )
        elif vis_requirement == 'sterk_aanbevolen' and not has_visual and not assets:
            self.warnings.append(
                "⚠️  Visualisatie is sterk aanbevolen voor dit niveau"
            )
        elif vis_requirement == 'aanbevolen' and not has_visual and not assets:
            self.info.append(
                "ℹ️  Overweeg een visualisatie toe te voegen (aanbevolen voor dit niveau)"
            )

    def _check_context(self, item: Dict[str, Any], regels: Dict[str, Any]):
        """Controleer context geschiktheid"""
        context = item.get('context', '').lower()
        context_tag = item.get('context_tag', '').lower()
        context_types = regels.get('context_types', [])

        if not context_types:
            return

        # Check of context past bij toegestane types
        match_found = any(
            ctx_type in context or ctx_type in context_tag
            for ctx_type in context_types
        )

        if not match_found:
            self.warnings.append(
                f"⚠️  Context '{context}' past mogelijk niet bij toegestane types: {context_types}"
            )

        # Speciale checks voor geld context
        if 'geld' in context or 'euro' in context:
            groep = item.get('groep', 0)
            hoofdvraag = item.get('hoofdvraag', '')
            bedragen = re.findall(r'€?\s*(\d+(?:[.,]\d{1,2})?)\s*(?:euro|cent)?', hoofdvraag)

            if groep == 3:
                for bedrag_str in bedragen:
                    bedrag = float(bedrag_str.replace(',', '.'))
                    if bedrag > 10:
                        self.warnings.append(
                            f"⚠️  Bedrag €{bedrag} te hoog voor G3 (max €10)"
                        )

    def _check_taal_complexiteit(self, item: Dict[str, Any], regels: Dict[str, Any]):
        """
        VERBETERD: Controleer talige complexiteit inclusief bijzinnen
        """
        hoofdvraag = item.get('hoofdvraag', '')

        # NIEUW: Filter visuele elementen (emoji blokken, symbolen) voordat zinnen tellen
        # Verwijder emoji blocks, box drawing characters, en andere visuele elementen
        hoofdvraag_clean = re.sub(r'[🟦🟧🟨🟩🟪🟫⬛⬜▪▫■□●○◆◇★☆♦♥♠♣]', '', hoofdvraag)
        hoofdvraag_clean = re.sub(r'[\u2500-\u257F]', '', hoofdvraag_clean)  # Box drawing
        hoofdvraag_clean = re.sub(r'\n+', ' ', hoofdvraag_clean)  # Newlines naar spaties
        hoofdvraag_clean = hoofdvraag_clean.strip()

        # Tel zinnen (nu zonder visuele elementen)
        zinnen = [z.strip() for z in re.split(r'[.!?]+', hoofdvraag_clean) if z.strip()]
        max_zinnen = regels.get('max_zinnen', 10)

        if len(zinnen) > max_zinnen:
            self.warnings.append(
                f"⚠️  Te veel zinnen: {len(zinnen)} (max {max_zinnen})"
            )

        # Tel woorden per zin
        max_woorden = regels.get('max_woorden_per_zin', 20)
        for idx, zin in enumerate(zinnen, 1):
            woorden = zin.split()
            if len(woorden) > max_woorden:
                self.warnings.append(
                    f"⚠️  Zin {idx} heeft {len(woorden)} woorden (max {max_woorden})"
                )

        # NIEUW: Check op bijzinnen voor G3
        bijzinnen_toegestaan = regels.get('bijzinnen_toegestaan', True)
        if not bijzinnen_toegestaan:
            bijzin_indicatoren = [
                'die',
                'dat',
                'omdat',
                'terwijl',
                'toen',
                'nadat',
                'voordat',
                'als',
                'wanneer',
            ]
            gevonden_bijzinnen = [
                indicator for indicator in bijzin_indicatoren if indicator in hoofdvraag.lower()
            ]
            if gevonden_bijzinnen:
                self.errors.append(
                    f"❌ Bijzinnen niet toegestaan voor dit niveau. Gevonden: {gevonden_bijzinnen}"
                )

        # NIEUW: Check vraagwoorden voor G3
        vraagwoorden = regels.get('vraagwoorden', [])
        if vraagwoorden:
            hoofdvraag_lower = hoofdvraag.lower()
            if not any(vw in hoofdvraag_lower for vw in vraagwoorden):
                self.warnings.append(
                    f"⚠️  Vraag gebruikt geen duidelijk vraagwoord uit: {vraagwoorden}"
                )

    def _check_afleiders(self, item: Dict[str, Any], regels: Dict[str, Any]):
        """Controleer afleiders kwaliteit"""
        afleiders = item.get('afleiders', [])
        correct = item.get('correct_antwoord', '')

        if not afleiders:
            self.errors.append("❌ Geen afleiders gedefinieerd")
            return

        if len(afleiders) < 3:
            self.warnings.append(
                f"⚠️  Slechts {len(afleiders)} afleiders (aanbevolen: 3-4)"
            )

        # Check afleider types
        afleider_types = regels.get('afleider_types', [])
        if afleider_types:
            self.info.append(
                f"ℹ️  Aanbevolen afleider types voor dit niveau: {afleider_types}"
            )

    def _check_numerical_correctness(self, item: Dict[str, Any]):
        """Controleer numerieke correctheid van berekeningen"""
        hoofdvraag = item.get('hoofdvraag', '')
        correct_antwoord = str(item.get('correct_antwoord', '')).strip()

        # Probeer simpele berekeningen te evalueren
        # Bijvoorbeeld: "12 + 5 = ?" → check of correct_antwoord = 17
        patterns = [
            (r'(\d+)\s*\+\s*(\d+)', lambda a, b: a + b, 'optellen'),
            (r'(\d+)\s*-\s*(\d+)', lambda a, b: a - b, 'aftrekken'),
            (r'(\d+)\s*[×*x]\s*(\d+)', lambda a, b: a * b, 'vermenigvuldigen'),
            (r'(\d+)\s*[:÷/]\s*(\d+)', lambda a, b: a / b if b != 0 else None, 'delen'),
        ]

        for pattern, calc, naam in patterns:
            matches = re.findall(pattern, hoofdvraag)
            if matches:
                for num1_str, num2_str in matches:
                    num1, num2 = int(num1_str), int(num2_str)
                    verwacht = calc(num1, num2)

                    if verwacht is not None:
                        # Check verschillende formats
                        try:
                            gegeven = float(correct_antwoord.replace(',', '.'))
                            if abs(gegeven - verwacht) > 0.01:
                                self.errors.append(
                                    f"❌ Berekening {num1} {naam} {num2} = {verwacht}, "
                                    f"maar correct_antwoord is {correct_antwoord}"
                                )
                        except ValueError:
                            self.warnings.append(
                                f"⚠️  Kan correct_antwoord '{correct_antwoord}' niet als getal interpreteren"
                            )

    def _check_uitkomst_binnen_bereik(self, item: Dict[str, Any], regels: Dict[str, Any]):
        """
        NIEUW: Controleer of uitkomst van berekening binnen getallenruimte blijft
        """
        getallenruimte = regels.get('getallenruimte')
        if getallenruimte == 'onbeperkt':
            return

        min_val, max_val = getallenruimte
        correct_antwoord = item.get('correct_antwoord', '')

        try:
            uitkomst = float(str(correct_antwoord).replace(',', '.'))
            if not (min_val <= uitkomst <= max_val):
                self.errors.append(
                    f"❌ Uitkomst {uitkomst} valt buiten getallenruimte [{min_val}, {max_val}]"
                )
        except (ValueError, TypeError):
            # Antwoord is geen getal (bijv. tekst), skip deze check
            pass

    def _check_afleider_duplicaten(self, item: Dict[str, Any]):
        """
        NIEUW: Controleer dat afleiders uniek zijn en niet gelijk aan correct antwoord
        """
        correct = str(item.get('correct_antwoord', '')).strip()
        afleiders = item.get('afleiders', [])

        # Check duplicaten in afleiders
        afleiders_str = [str(a).strip() for a in afleiders]
        if len(afleiders_str) != len(set(afleiders_str)):
            self.errors.append("❌ Er zijn dubbele afleiders")

        # Check of afleider gelijk is aan correct antwoord
        if correct in afleiders_str:
            self.errors.append(
                f"❌ Afleider '{correct}' is gelijk aan het correcte antwoord"
            )

    def _check_afleider_clustering(self, item: Dict[str, Any]):
        """
        NIEUW: Controleer of afleiders niet te dicht bij elkaar of bij correct antwoord liggen
        """
        try:
            correct = float(str(item.get('correct_antwoord', '')).replace(',', '.'))
            afleiders = [
                float(str(a).replace(',', '.'))
                for a in item.get('afleiders', [])
                if str(a).replace(',', '.').replace('-', '').replace('.', '').isdigit()
            ]

            if not afleiders:
                return  # Geen numerieke afleiders

            # Alle waarden (correct + afleiders)
            alle_waarden = sorted([correct] + afleiders)

            # Check op clustering (3+ waarden binnen range van 5)
            for i in range(len(alle_waarden) - 2):
                window = alle_waarden[i : i + 3]
                if max(window) - min(window) <= 5:
                    self.warnings.append(
                        f"⚠️  Afleiders clusteren: {window} liggen dicht bij elkaar (range ≤ 5)"
                    )
                    break

        except (ValueError, TypeError):
            # Niet-numerieke antwoorden, skip
            pass

    def _check_context_semantiek(self, item: Dict[str, Any], regels: Dict[str, Any]):
        """
        NIEUW: Controleer of context-verhaal past bij de bewerking
        """
        hoofdvraag = item.get('hoofdvraag', '').lower()

        # Detecteer bewerking
        bewerking_type = None
        if any(sym in hoofdvraag for sym in ['+', 'plus', 'erbij', 'bij elkaar']):
            bewerking_type = 'optellen'
        elif any(sym in hoofdvraag for sym in ['-', 'min', 'kwijt', 'minder']):
            bewerking_type = 'aftrekken'
        elif any(sym in hoofdvraag for sym in ['×', '*', 'keer', 'groepjes']):
            bewerking_type = 'vermenigvuldigen'
        elif any(sym in hoofdvraag for sym in [':', '÷', 'verdelen', 'delen']):
            bewerking_type = 'delen'

        if not bewerking_type:
            return

        # Check of context woorden passen bij bewerking
        context_woorden = self.CONTEXT_BEWERKING_MAP.get(bewerking_type, [])
        if context_woorden:
            match = any(woord in hoofdvraag for woord in context_woorden)
            if not match:
                self.warnings.append(
                    f"⚠️  Context-verhaal suggereert mogelijk niet de bewerking '{bewerking_type}'. "
                    f"Overweeg woorden als: {context_woorden}"
                )

    def _check_moeilijkheid_tijd(self, item: Dict[str, Any], regels: Dict[str, Any]):
        """Controleer moeilijkheid en tijd"""
        moeilijkheid = item.get('moeilijkheidsgraad')
        tijd = item.get('geschatte_tijd_sec')

        if moeilijkheid:
            moeilijkheid_range = regels.get('moeilijkheid_range')
            if moeilijkheid_range:
                min_m, max_m = moeilijkheid_range
                if not (min_m <= moeilijkheid <= max_m):
                    self.warnings.append(
                        f"⚠️  Moeilijkheid {moeilijkheid} buiten verwachte range [{min_m}, {max_m}]"
                    )

        if tijd:
            min_tijd = regels.get('min_tijd_sec', 0)
            max_tijd = regels.get('max_tijd_sec', 300)
            if not (min_tijd <= tijd <= max_tijd):
                self.warnings.append(
                    f"⚠️  Geschatte tijd {tijd}s buiten verwachte range [{min_tijd}, {max_tijd}]"
                )

    def _check_didactic_quality_enhanced(self, item: Dict[str, Any], regels: Dict[str, Any]):
        """
        VERBETERD: Uitgebreidere didactische kwaliteitscheck
        """
        toelichting = item.get('toelichting', '').lower()

        # NIEUW: Check of dit een auto-converted item is
        is_auto_converted = 'auto-convert' in toelichting or 'auto-conversie' in toelichting

        if is_auto_converted:
            self.errors.append(
                "❌ Item is auto-converted uit legacy formaat. "
                "Vul een volledige toelichting met strategie en misconceptie-uitleg."
            )
            return

        # Check minimale lengte
        if not toelichting or len(toelichting) < 30:
            self.warnings.append(
                "⚠️  Toelichting is erg kort (<30 karakters)"
            )
            return

        # NIEUW: Check op strategie-vermelding
        gevonden_strategieen = [
            kw for kw in self.STRATEGIE_KEYWORDS if kw in toelichting
        ]
        if not gevonden_strategieen:
            self.warnings.append(
                "⚠️  Geen duidelijke strategie genoemd in toelichting (bijv. splitsen, bruggetje)"
            )

        # NIEUW: Check op misconceptie-uitleg bij afleiders
        afleiders = item.get('afleiders', [])
        if afleiders:
            heeft_misconceptie_uitleg = any(
                kw in toelichting for kw in self.MISCONCEPTIE_KEYWORDS
            )
            if not heeft_misconceptie_uitleg:
                self.info.append(
                    "ℹ️  Overweeg in toelichting uit te leggen waarom afleiders fout zijn (misconcepties)"
                )

        # Check LOVA-elementen
        lova_keywords = ['lezen', 'ordenen', 'strategie', 'stappen', 'methode', 'aanpak']
        if not any(kw in toelichting for kw in lova_keywords):
            self.info.append(
                "ℹ️  Overweeg LOVA-elementen toe te voegen aan toelichting"
            )

    def _check_cross_validation(self, item: Dict[str, Any]):
        """Cross-validatie tussen moeilijkheid, stappen en tijd"""
        moeilijkheid = item.get('moeilijkheidsgraad')
        tijd = item.get('geschatte_tijd_sec')
        hoofdvraag = item.get('hoofdvraag', '')

        # Tel stappen (geschat op basis van bewerkingen)
        operations = len(re.findall(r'[+\-×*:÷]', hoofdvraag))

        # Consistency checks
        if moeilijkheid and tijd:
            if moeilijkheid > 0.7 and tijd < 30:
                self.warnings.append(
                    "⚠️  Inconsistentie: hoge moeilijkheid (>0.7) maar korte tijd (<30s)"
                )

            if moeilijkheid < 0.3 and tijd > 90:
                self.warnings.append(
                    "⚠️  Inconsistentie: lage moeilijkheid (<0.3) maar lange tijd (>90s)"
                )

        # Check stappen vs tijd
        if operations >= 3 and tijd and tijd < 40:
            self.warnings.append(
                f"⚠️  {operations} bewerkingen maar slechts {tijd}s tijd (mogelijk te weinig)"
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
            valid=valid, errors=self.errors, warnings=self.warnings, info=self.info, score=score
        )


def _convert_legacy_structure(data: Any) -> Optional[List[Dict[str, Any]]]:
    """
    AANGEPAST: Legacy conversie met verbeterde context extractie en visual detectie
    
    Ondersteun legacy MC-bestanden:
    - Top-level met schema_version/metadata/items
    - Items met question/options/answer.correct_index
    - Detecteer visuele elementen automatisch
    - Extract concrete context uit vraagtext
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

        # NIEUW: Detecteer visuele elementen in vraagtext
        question_text = q.get("text", "")
        has_visual = bool(re.search(r'[🟦🟧🟨🟩🟪🟫⬛⬜▪▫■□●○◆◇★☆♦♥♠♣]', question_text))
        has_visual = has_visual or bool(re.search(r'[\u2500-\u257F]', question_text))  # Box drawing
        has_visual = has_visual or 'plaatje' in question_text.lower() or 'afbeelding' in question_text.lower()
        
        # NIEUW: Extract concrete context uit vraagtext
        context_mapping = {
            'snoep': ['snoep', 'lolly', 'snoepje', 'drop', 'kauwgom'],
            'fruit': ['appel', 'peer', 'banaan', 'sinaasappel', 'kers', 'druif', 'fruit'],
            'speelgoed': ['auto', 'pop', 'blok', 'lego', 'knuffel', 'bal', 'knikker'],
            'dieren': ['hond', 'kat', 'vogel', 'vis', 'konijn', 'paard', 'kip', 'dier'],
            'vingers': ['vinger', 'hand'],
            'dobbelstenen': ['dobbelsteen', 'dobbel', 'steen'],
            'geld': ['euro', 'cent', 'geld', 'munten', 'briefje'],
            'tijd': ['uur', 'minuut', 'tijd', 'klok'],
            'groepjes': ['groep', 'kind', 'leerling', 'kinderen'],
        }
        
        detected_context = "algemeen"
        question_lower = question_text.lower()
        for context_key, keywords in context_mapping.items():
            if any(keyword in question_lower for keyword in keywords):
                detected_context = context_key
                break
        
        # Legacy theme als fallback
        theme = legacy.get("theme", "nvt")
        
        # AANGEPAST: Minimale toelichting, zodat gebruiker gedwongen wordt deze aan te vullen
        toelichting_basis = f"[AUTO-CONVERTED - VEREIST HANDMATIGE AANVULLING]\nOrigineel thema: {theme}."

        converted.append(
            {
                "id": new_id,
                "groep": groep,
                "niveau": niveau,
                "hoofdvraag": question_text,
                "correct_antwoord": correct_text,
                "afleiders": afleiders,
                "toelichting": toelichting_basis,  # Minimaal, dwingt handmatige check
                "context": theme,  # Originele theme behouden
                "has_visual": has_visual,  # AANGEPAST: Automatisch gedetecteerd
                "assets": [] if not has_visual else ["embedded_visual"],  # Placeholder
                "context_tag": detected_context,  # NIEUW: Gedetecteerde concrete context
                "moeilijkheidsgraad": None,  # Moet handmatig ingevuld
                "geschatte_tijd_sec": None,  # Moet handmatig ingevuld
            }
        )

    return converted


def valideer_bestand(filepath: str) -> List[ValidationResult]:
    """Valideer een JSON bestand met items"""
    validator = GetallenValidatorImproved()

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Ondersteun zowel lijst, enkel item, als legacy structuur
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
        print(f"\n{'=' * 70}")
        print(f"Valideer item {idx}/{len(items)}: {item.get('id', 'GEEN_ID')}")
        print(f"{'=' * 70}")

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
    print(f"\n{'=' * 70}")
    print("SAMENVATTING")
    print(f"{'=' * 70}")
    valid_count = sum(1 for r in resultaten if r.valid)
    print(f"✅ Valide items: {valid_count}/{len(resultaten)}")
    print(f"❌ Invalide items: {len(resultaten) - valid_count}/{len(resultaten)}")
    avg_score = sum(r.score for r in resultaten) / len(resultaten) if resultaten else 0
    print(f"📊 Gemiddelde score: {avg_score:.2f}")

    return resultaten


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Gebruik: python getallen-validator-v5-improved.py <json_bestand>")
        print("\nVoorbeeld JSON format:")
        print(
            json.dumps(
                {
                    "id": "G_G3_M_001",
                    "groep": 3,
                    "niveau": "M",
                    "hoofdvraag": "Lisa heeft 3 appels. Ze krijgt er 2 bij. Hoeveel appels heeft Lisa nu?",
                    "correct_antwoord": "5",
                    "afleiders": ["4", "6", "7"],
                    "toelichting": "Optellen tot 10 met splitsen strategie. 3 + 2 = 5. Gebruik vingers of blokjes om te tellen.",
                    "context": "fruit tellen",
                    "context_tag": "speelgoed",
                    "has_visual": True,
                    "assets": ["appels_plaatje.png"],
                    "moeilijkheidsgraad": 0.25,
                    "geschatte_tijd_sec": 25,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        sys.exit(1)

    valideer_bestand(sys.argv[1])
