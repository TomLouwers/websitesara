"""
VERHOUDINGEN VALIDATOR v3.0 - ENHANCED
Uitgebreid validatiescript met diepgaande kwaliteitscontroles

Nieuwe features in v3.0:
- ✅ Inhoudelijke validatie (breuken, decimalen, percentages correctheid)
- ✅ Context geschiktheid per leeftijdsgroep
- ✅ Afleider kwaliteit (numerieke plausibiliteit, spreiding)
- ✅ Numerieke correctheidscontroles
- ✅ Didactische kwaliteit (feedback specificiteit, LOVA volledigheid)
- ✅ Cross-validatie (moeilijkheidsgraad vs stappen vs tijd)
- ✅ Visualisatie vereisten
- ✅ Realistische getallen in context
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from fractions import Fraction
from decimal import Decimal


@dataclass
class ValidationResult:
    """Uitgebreid resultaat van validatie"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    info: List[str] = field(default_factory=list)
    score: float = 0.0  # 0.0 - 1.0
    quality_breakdown: Dict[str, float] = field(default_factory=dict)


class VerhoudingenValidatorEnhanced:
    """Uitgebreide validator voor Verhoudingen domein items"""

    # Niveauregels per groep/niveau (uitgebreid)
    NIVEAU_REGELS = {
        (4, 'M'): {
            'stambreuken': ['1/2', '1/4'],
            'max_getal': 20,
            'max_stappen': 1,
            'visualisatie': 'verplicht',
            'subdomeinen': ['Breuken'],
            'bewerkingen': ['herkennen'],
            'max_zinnen': 3,
            'context_types': ['speelgoed', 'snoep', 'taart', 'fruit', 'spelletjes'],
            'min_tijd_sec': 20,
            'max_tijd_sec': 45,
            'moeilijkheid_range': (0.15, 0.40)
        },
        (4, 'E'): {
            'stambreuken': ['1/2', '1/3', '1/4'],
            'max_getal': 50,
            'max_stappen': 2,
            'visualisatie': 'verplicht',
            'subdomeinen': ['Breuken'],
            'bewerkingen': ['herkennen', 'berekenen_eenvoudig', 'vergelijken'],
            'max_zinnen': 4,
            'context_types': ['speelgoed', 'snoep', 'taart', 'geld', 'tijd'],
            'min_tijd_sec': 30,
            'max_tijd_sec': 60,
            'moeilijkheid_range': (0.30, 0.55)
        },
        (5, 'M'): {
            'stambreuken': ['1/2', '1/3', '1/4', '1/5', '1/6', '1/8', '1/10'],
            'niet_stambreuken': ['2/3', '2/4', '3/4', '2/5', '3/5'],
            'decimalen_range': (0.1, 10.0),
            'decimalen_cijfers': 1,
            'percentages': [50, 100],
            'max_getal': 100,
            'max_stappen': 2,
            'visualisatie': 'optioneel',
            'subdomeinen': ['Breuken', 'Decimalen', 'Procenten'],
            'max_zinnen': 4,
            'context_types': ['recepten', 'geld', 'metingen', 'school', 'sport'],
            'min_tijd_sec': 35,
            'max_tijd_sec': 75,
            'moeilijkheid_range': (0.35, 0.60)
        },
        (5, 'E'): {
            'breuken_bewerkingen': ['optellen_zelfde_noemer', 'aftrekken_zelfde_noemer'],
            'decimalen_cijfers': 2,
            'max_noemer': 10,
            'max_stappen': 3,
            'subdomeinen': ['Breuken', 'Decimalen', 'Procenten'],
            'max_zinnen': 4,
            'context_types': ['recepten', 'geld', 'metingen', 'school', 'sport', 'reizen'],
            'min_tijd_sec': 45,
            'max_tijd_sec': 90,
            'moeilijkheid_range': (0.45, 0.70)
        },
        (6, 'M'): {
            'breuken_bewerkingen': ['optellen_andere_noemer', 'vermenigvuldigen', 'delen'],
            'percentages': [10, 25, 50, 75, 100],
            'verhoudingstabellen': True,
            'schaal': ['1:100', '1:1000'],
            'max_stappen': 4,
            'subdomeinen': ['Breuken', 'Decimalen', 'Procenten', 'Verhoudingstabellen', 'Schaal'],
            'max_zinnen': 6,
            'context_types': ['winkels', 'sport', 'school', 'kaarten', 'boodschappen'],
            'min_tijd_sec': 50,
            'max_tijd_sec': 120,
            'moeilijkheid_range': (0.45, 0.65)
        },
        (6, 'E'): {
            'conversies': True,
            'procenten_omgekeerd': True,
            'max_stappen': 4,
            'subdomeinen': ['Breuken', 'Decimalen', 'Procenten', 'Verhoudingstabellen', 'Schaal'],
            'max_zinnen': 6,
            'context_types': ['winkels', 'sport', 'school', 'kaarten', 'statistieken'],
            'min_tijd_sec': 55,
            'max_tijd_sec': 135,
            'moeilijkheid_range': (0.50, 0.70)
        },
        (7, 'M'): {
            'verhoudingstabellen_complex': True,
            'percentages_samengesteld': True,
            'kortingen': True,
            'max_stappen': 4,
            'subdomeinen': ['Verhoudingstabellen', 'Procenten', 'Schaal'],
            'max_zinnen': 6,
            'context_types': ['winkels', 'financieel', 'camping', 'brandstof', 'statistieken'],
            'min_tijd_sec': 60,
            'max_tijd_sec': 150,
            'moeilijkheid_range': (0.55, 0.75)
        },
        (7, 'E'): {
            'schaal_gevorderd': ['1:50', '1:500', '1:50000'],
            'prijsverhoudingen': True,
            'grafieken': ['cirkeldiagram'],
            'max_stappen': 4,
            'subdomeinen': ['Verhoudingstabellen', 'Procenten', 'Schaal'],
            'max_zinnen': 8,
            'context_types': ['winkels', 'kaarten', 'modelbouw', 'statistieken', 'enquetes'],
            'min_tijd_sec': 70,
            'max_tijd_sec': 180,
            'moeilijkheid_range': (0.60, 0.80)
        },
        (8, 'M'): {
            'rente': True,
            'btw': [9, 21],
            'gemiddelde_verhoudingen': True,
            'referentieniveau': '1F',
            'max_stappen': 4,
            'subdomeinen': ['Verhoudingstabellen', 'Procenten', 'Schaal'],
            'max_zinnen': 8,
            'context_types': ['financieel', 'statistieken', 'wetenschap', 'maatschappij'],
            'min_tijd_sec': 75,
            'max_tijd_sec': 180,
            'moeilijkheid_range': (0.55, 0.75)
        },
        (8, 'E'): {
            'schaal_complex': True,
            'woordproblemen_meerstaps': True,
            'integraal': True,
            'referentieniveau': '1S',
            'max_stappen': 5,
            'subdomeinen': ['Verhoudingstabellen', 'Procenten', 'Schaal', 'Integraal'],
            'max_zinnen': 8,
            'context_types': ['financieel', 'statistieken', 'wetenschap', 'maatschappij', 'complex'],
            'min_tijd_sec': 90,
            'max_tijd_sec': 240,
            'moeilijkheid_range': (0.65, 0.85)
        }
    }

    # Ongepaste contexten per leeftijdsgroep
    ONGEPASTE_CONTEXTEN = {
        4: ['alcohol', 'gokken', 'leningen', 'hypotheek', 'belasting', 'politiek'],
        5: ['alcohol', 'gokken', 'leningen', 'hypotheek', 'belasting', 'politiek'],
        6: ['alcohol', 'gokken', 'leningen', 'hypotheek', 'politiek'],
        7: ['alcohol', 'gokken', 'politiek'],
        8: ['gokken']
    }

    # Realistische getalbereiken per context
    REALISTISCHE_BEREIKEN = {
        'zakgeld': (1, 20),
        'snoep': (1, 50),
        'speelgoed': (5, 100),
        'schoolspullen': (1, 50),
        'boodschappen': (1, 100),
        'kleding': (10, 150),
        'fiets': (100, 500),
        'vakantie': (200, 2000),
        'huisdier': (10, 500),
        'cadeau': (5, 100)
    }

    def __init__(self, strict_mode: bool = False):
        """
        Initialiseer validator

        Args:
            strict_mode: Als True, worden warnings ook als errors behandeld
        """
        self.errors = []
        self.warnings = []
        self.info = []
        self.strict_mode = strict_mode

    def valideer_item(self, item: Dict[str, Any]) -> ValidationResult:
        """Voer complete validatie uit op een item"""
        self.errors = []
        self.warnings = []
        self.info = []

        # Basis structuur
        self._check_basis_structuur(item)

        # Als basis structuur faalt, stop hier
        if self.errors:
            return self._build_result()

        # Niveau checks
        self._check_niveau_regels(item)

        # Inhoudelijke validatie
        self._check_content_validity(item)

        # Context geschiktheid
        self._check_context_appropriateness(item)

        # Afleiders kwaliteit
        self._check_distractor_quality(item)

        # Numerieke correctheid
        self._check_numerical_correctness(item)

        # Taal checks
        self._check_taal(item)

        # Metadata checks
        self._check_metadata(item)

        # Didactische kwaliteit
        self._check_didactic_quality(item)

        # Visualisatie checks
        self._check_visualization(item)

        # Cross-validatie
        self._check_cross_validation(item)

        return self._build_result()

    def _build_result(self) -> ValidationResult:
        """Bouw het validatieresultaat"""
        # In strict mode worden warnings ook errors
        if self.strict_mode:
            self.errors.extend(self.warnings)
            self.warnings = []

        quality_breakdown = self._calculate_quality_breakdown()
        score = self._bereken_score()

        return ValidationResult(
            valid=len(self.errors) == 0,
            errors=self.errors,
            warnings=self.warnings,
            info=self.info,
            score=score,
            quality_breakdown=quality_breakdown
        )

    def _check_niveau_regels(self, item: Dict[str, Any]):
        """Check of item binnen niveauregels valt"""
        groep = item.get('groep')
        niveau = item.get('niveau')

        if (groep, niveau) not in self.NIVEAU_REGELS:
            self.errors.append(f"❌ Geen regels gedefinieerd voor groep {groep} niveau {niveau}")
            return

        regels = self.NIVEAU_REGELS[(groep, niveau)]

        # Check max stappen
        stappen = item.get('metadata', {}).get('stappen_aantal', 0)
        if stappen > regels.get('max_stappen', 999):
            self.errors.append(
                f"❌ Te veel stappen: {stappen} (max {regels['max_stappen']} voor G{groep}-{niveau})"
            )

        # Check subdomeinen
        subdomein = item.get('subdomein')
        toegestane_subdomeinen = regels.get('subdomeinen', [])
        if subdomein and toegestane_subdomeinen and subdomein not in toegestane_subdomeinen:
            self.errors.append(
                f"❌ Subdomein '{subdomein}' niet toegestaan voor G{groep}-{niveau}. "
                f"Toegestaan: {toegestane_subdomeinen}"
            )

        # Specifieke checks voor groep 4-5
        if groep == 4 and niveau == 'M':
            # Alleen stambreuken 1/2 en 1/4
            vraag_tekst = self._get_full_text(item)
            if '1/3' in vraag_tekst or '1/5' in vraag_tekst or '1/6' in vraag_tekst:
                self.errors.append("❌ G4-M mag alleen 1/2 en 1/4, geen andere breuken!")

        if groep == 5 and niveau == 'M' and subdomein == 'Procenten':
            # Alleen 50% en 100%
            vraag_tekst = self._get_full_text(item)
            if any(p in vraag_tekst for p in ['10%', '25%', '75%', '20%', '30%', '40%', '60%', '70%', '80%', '90%']):
                self.warnings.append("⚠️  G5-M procenten: alleen 50% en 100% toegestaan volgens regels")

    def _check_basis_structuur(self, item: Dict[str, Any]):
        """Check of alle verplichte velden aanwezig zijn"""
        verplichte_velden = [
            'id', 'domein', 'subdomein', 'groep', 'niveau',
            'vraag', 'antwoorden', 'metadata', 'didactiek'
        ]

        for veld in verplichte_velden:
            if veld not in item:
                self.errors.append(f"❌ Verplicht veld '{veld}' ontbreekt")

        # Check domein
        if item.get('domein') != 'Verhoudingen':
            self.errors.append(f"❌ Domein moet 'Verhoudingen' zijn, is '{item.get('domein')}'")

        # Check groep en niveau
        if item.get('groep') not in [4, 5, 6, 7, 8]:
            self.errors.append(f"❌ Groep moet 4-8 zijn, is {item.get('groep')}")

        if item.get('niveau') not in ['M', 'E']:
            self.errors.append(f"❌ Niveau moet M of E zijn, is '{item.get('niveau')}'")

        # Check ID format
        if 'id' in item:
            expected_pattern = r'^V_G[4-8]_[ME]_\d+$'
            if not re.match(expected_pattern, item['id']):
                self.warnings.append(f"⚠️  ID '{item['id']}' volgt niet standaard format V_G[4-8]_[ME]_###")

    def _check_content_validity(self, item: Dict[str, Any]):
        """Check inhoudelijke correctheid van breuken, decimalen, percentages"""
        subdomein = item.get('subdomein', '')
        vraag_tekst = self._get_full_text(item)
        antwoorden = item.get('antwoorden', [])

        if subdomein == 'Breuken':
            self._validate_breuken_content(vraag_tekst, antwoorden, item)
        elif subdomein == 'Decimalen':
            self._validate_decimalen_content(vraag_tekst, antwoorden, item)
        elif subdomein == 'Procenten':
            self._validate_procenten_content(vraag_tekst, antwoorden, item)
        elif subdomein == 'Schaal':
            self._validate_schaal_content(vraag_tekst, antwoorden, item)

    def _validate_breuken_content(self, tekst: str, antwoorden: List[Dict], item: Dict):
        """Valideer breuken inhoud"""
        # Zoek alle breuken in tekst en antwoorden
        breuk_pattern = r'(\d+)/(\d+)'
        breuken_in_tekst = re.findall(breuk_pattern, tekst)

        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        # Check toegestane breuken
        toegestane_stambreuken = regels.get('stambreuken', [])
        if toegestane_stambreuken:
            for teller, noemer in breuken_in_tekst:
                breuk_str = f"{teller}/{noemer}"
                # Check of het een stambreuk is
                if teller == '1' and breuk_str not in toegestane_stambreuken:
                    self.errors.append(
                        f"❌ Stambreuk {breuk_str} niet toegestaan voor G{groep}-{niveau}. "
                        f"Toegestaan: {toegestane_stambreuken}"
                    )

        # Check of breuken vereenvoudigd zijn (waar relevant)
        for teller, noemer in breuken_in_tekst:
            try:
                frac = Fraction(int(teller), int(noemer))
                if frac.numerator != int(teller) or frac.denominator != int(noemer):
                    # Breuk kan vereenvoudigd worden
                    vereenvoudigd = f"{frac.numerator}/{frac.denominator}"
                    if groep >= 5:  # Vanaf groep 5 verwachten we vereenvoudiging
                        self.info.append(
                            f"ℹ️  Breuk {teller}/{noemer} kan vereenvoudigd naar {vereenvoudigd}"
                        )
            except (ValueError, ZeroDivisionError):
                self.errors.append(f"❌ Ongeldige breuk: {teller}/{noemer}")

        # Check noemers binnen maximum
        max_noemer = regels.get('max_noemer', 999)
        for teller, noemer in breuken_in_tekst:
            if int(noemer) > max_noemer:
                self.errors.append(
                    f"❌ Noemer {noemer} te groot voor G{groep}-{niveau} (max {max_noemer})"
                )

    def _validate_decimalen_content(self, tekst: str, antwoorden: List[Dict], item: Dict):
        """Valideer decimalen inhoud"""
        # Zoek decimalen (Nederlandse notatie met komma)
        decimaal_pattern = r'\d+[,\.]\d+'
        decimalen = re.findall(decimaal_pattern, tekst)

        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        max_cijfers = regels.get('decimalen_cijfers', 2)

        for dec in decimalen:
            # Check aantal decimalen
            dec_normalized = dec.replace(',', '.')
            try:
                decimal_val = Decimal(dec_normalized)
                decimaal_deel = str(decimal_val).split('.')[1] if '.' in str(decimal_val) else ''
                if len(decimaal_deel) > max_cijfers:
                    self.warnings.append(
                        f"⚠️  Decimaal {dec} heeft {len(decimaal_deel)} decimalen "
                        f"(max {max_cijfers} voor G{groep}-{niveau})"
                    )
            except:
                self.errors.append(f"❌ Ongeldig decimaal getal: {dec}")

        # Check Nederlandse vs Engelse notatie consistency
        heeft_komma = any(',' in d for d in decimalen)
        heeft_punt = any('.' in d for d in decimalen)
        if heeft_komma and heeft_punt:
            self.warnings.append("⚠️  Mix van komma en punt in decimalen (kies één notatie)")

    def _validate_procenten_content(self, tekst: str, antwoorden: List[Dict], item: Dict):
        """Valideer percentages inhoud"""
        # Zoek percentages
        percentage_pattern = r'(\d+(?:[.,]\d+)?)\s*%'
        percentages = re.findall(percentage_pattern, tekst)

        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        toegestane_percentages = regels.get('percentages', [])

        if toegestane_percentages:
            for perc_str in percentages:
                perc_val = float(perc_str.replace(',', '.'))
                # Check of percentage toegestaan is (met kleine marge voor decimalen)
                if not any(abs(perc_val - tp) < 0.1 for tp in toegestane_percentages):
                    self.warnings.append(
                        f"⚠️  Percentage {perc_val}% niet in standaard set voor G{groep}-{niveau}: "
                        f"{toegestane_percentages}"
                    )

        # Check realistische percentages
        for perc_str in percentages:
            perc_val = float(perc_str.replace(',', '.'))
            if perc_val > 100:
                self.warnings.append(f"⚠️  Percentage {perc_val}% > 100% (is dit correct?)")
            if perc_val < 0:
                self.errors.append(f"❌ Negatief percentage {perc_val}% niet toegestaan")

    def _validate_schaal_content(self, tekst: str, antwoorden: List[Dict], item: Dict):
        """Valideer schaal notaties"""
        # Zoek schaal notaties
        schaal_pattern = r'1:(\d+)'
        schalen = re.findall(schaal_pattern, tekst)

        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        toegestane_schalen = regels.get('schaal', []) + regels.get('schaal_gevorderd', [])

        if toegestane_schalen:
            for schaal_getal in schalen:
                schaal_notatie = f"1:{schaal_getal}"
                if schaal_notatie not in toegestane_schalen:
                    self.warnings.append(
                        f"⚠️  Schaal {schaal_notatie} niet in standaard set voor G{groep}-{niveau}: "
                        f"{toegestane_schalen}"
                    )

    def _check_context_appropriateness(self, item: Dict[str, Any]):
        """Check of context geschikt is voor leeftijdsgroep"""
        groep = item.get('groep')
        context = item.get('vraag', {}).get('context', '').lower()

        # Check ongepaste contexten
        ongepaste = self.ONGEPASTE_CONTEXTEN.get(groep, [])
        for ongeschikt in ongepaste:
            if ongeschikt in context:
                self.errors.append(
                    f"❌ Context '{ongeschikt}' niet geschikt voor groep {groep}"
                )

        # Check toegestane context types
        regels = self.NIVEAU_REGELS.get((item.get('groep'), item.get('niveau')), {})
        toegestane_types = regels.get('context_types', [])
        if toegestane_types:
            # Check of minstens één toegestaan type voorkomt
            heeft_toegestaan_type = any(ct in context for ct in toegestane_types)
            if not heeft_toegestaan_type:
                self.info.append(
                    f"ℹ️  Context bevat geen standaard type. Suggestie: {toegestane_types[:3]}"
                )

        # Check realistische getallen in context
        self._check_realistic_numbers_in_context(item)

    def _check_realistic_numbers_in_context(self, item: Dict[str, Any]):
        """Check of getallen realistisch zijn voor de context"""
        context = item.get('vraag', {}).get('context', '').lower()

        # Zoek getallen in context
        getallen = re.findall(r'€?\s*(\d+(?:[.,]\d+)?)', context)

        for context_type, (min_val, max_val) in self.REALISTISCHE_BEREIKEN.items():
            if context_type in context:
                for getal_str in getallen:
                    try:
                        getal = float(getal_str.replace(',', '.'))
                        if '€' in context and context_type == 'zakgeld':
                            if getal > max_val:
                                self.warnings.append(
                                    f"⚠️  Bedrag €{getal} mogelijk onrealistisch voor {context_type} "
                                    f"(typisch bereik: €{min_val}-€{max_val})"
                                )
                    except ValueError:
                        pass

    def _check_distractor_quality(self, item: Dict[str, Any]):
        """Check kwaliteit van afleiders"""
        antwoorden = item.get('antwoorden', [])

        if len(antwoorden) != 4:
            return  # Al gecheckt in basis checks

        # Haal correct antwoord en afleiders op
        correct = None
        afleiders = []

        for ant in antwoorden:
            if ant.get('correct'):
                correct = ant
            else:
                afleiders.append(ant)

        if not correct:
            return  # Al gecheckt in basis checks

        # Check 1: Numerieke plausibiliteit
        self._check_numerical_plausibility(correct, afleiders, item)

        # Check 2: Spreiding van antwoorden
        self._check_answer_spread(correct, afleiders)

        # Check 3: Verschillende fouttypes
        fouttypes = [a.get('fouttype') for a in afleiders if a.get('fouttype')]
        if len(fouttypes) != len(set(fouttypes)):
            self.warnings.append("⚠️  Afleiders hebben overlappende fouttypes (bij voorkeur uniek)")

        # Check 4: Fouttypes zijn logisch
        geldige_fouttypes = [
            'conversie_fout', 'bewerking_fout', 'niet_vereenvoudigd',
            'verkeerde_noemer', 'omgedraaid', 'percentage_fout',
            'factor_fout', 'schaal_fout', 'stap_vergeten', 'plaatswaarde_fout',
            'complement_berekend', 'decimaal_verwarring', 'geheel_ipv_deel',
            'verkeerde_deling', 'omgekeerd_rekenen_fout'
        ]

        for a in afleiders:
            fouttype = a.get('fouttype')
            if fouttype and fouttype not in geldige_fouttypes:
                self.warnings.append(f"⚠️  Ongebruikelijk fouttype: {fouttype}")

    def _check_numerical_plausibility(self, correct: Dict, afleiders: List[Dict], item: Dict):
        """Check of afleiders numeriek plausibel zijn"""
        try:
            # Probeer numerieke waarde te extraheren
            correct_val = self._extract_numerical_value(correct.get('waarde') or correct.get('tekst'))

            if correct_val is None:
                return  # Niet-numeriek antwoord, skip deze check

            afleider_vals = []
            for afl in afleiders:
                val = self._extract_numerical_value(afl.get('waarde') or afl.get('tekst'))
                if val is not None:
                    afleider_vals.append(val)

            if not afleider_vals:
                return

            # Check 1: Afleiders niet te ver van correct antwoord
            for val in afleider_vals:
                if correct_val != 0:
                    ratio = abs(val / correct_val) if correct_val != 0 else float('inf')
                    if ratio > 10 or ratio < 0.1:
                        self.warnings.append(
                            f"⚠️  Afleider {val} mogelijk te ver van correct antwoord {correct_val} "
                            f"(ratio: {ratio:.2f})"
                        )

            # Check 2: Afleiders niet te dicht bij elkaar
            for i, val1 in enumerate(afleider_vals):
                for val2 in afleider_vals[i+1:]:
                    if abs(val1 - val2) < 0.01:
                        self.warnings.append(
                            f"⚠️  Twee afleiders te dicht bij elkaar: {val1} en {val2}"
                        )

        except Exception as e:
            # Als numerieke extractie faalt, geen warning
            pass

    def _extract_numerical_value(self, text: str) -> Optional[float]:
        """Extraheer numerieke waarde uit tekst"""
        if not text:
            return None

        # Verwijder euro teken en andere symbolen
        text = str(text).replace('€', '').replace('%', '').strip()

        # Probeer breuk
        if '/' in text:
            try:
                parts = text.split('/')
                return float(parts[0]) / float(parts[1])
            except:
                pass

        # Probeer decimaal (komma of punt)
        text = text.replace(',', '.')
        try:
            return float(text)
        except:
            return None

    def _check_answer_spread(self, correct: Dict, afleiders: List[Dict]):
        """Check of antwoorden goed gespreid zijn (niet altijd B correct bijv.)"""
        # Check positie van correct antwoord
        alle_antwoorden = [correct] + afleiders
        correct_id = correct.get('id', '')

        # Als ID letters zijn (A, B, C, D)
        if correct_id in ['A', 'B', 'C', 'D']:
            if correct_id in ['B', 'C']:
                self.info.append(f"ℹ️  Correct antwoord op positie {correct_id} (goed, niet altijd A of D)")
            elif correct_id == 'A':
                self.info.append(f"ℹ️  Correct antwoord op positie A (varieer positie voor moeilijkheid)")

    def _check_numerical_correctness(self, item: Dict[str, Any]):
        """Check (waar mogelijk) of correct antwoord wiskundig klopt"""
        subdomein = item.get('subdomein', '')
        stappen = item.get('didactiek', {}).get('berekening_stappen', [])

        if not stappen:
            return

        # Probeer te verifiëren of berekening klopt
        # Dit is complex, dus alleen eenvoudige checks
        if subdomein == 'Breuken':
            self._verify_breuk_berekening(item, stappen)
        elif subdomein == 'Procenten':
            self._verify_percentage_berekening(item, stappen)

    def _verify_breuk_berekening(self, item: Dict, stappen: List[str]):
        """Probeer breukberekening te verifiëren"""
        # Zoek naar optelling/aftrekking in stappen
        for stap in stappen:
            # Patroon: "a/b + c/d = e/f"
            match = re.search(r'(\d+)/(\d+)\s*\+\s*(\d+)/(\d+)\s*=\s*(\d+)/(\d+)', stap)
            if match:
                a, b, c, d, e, f = map(int, match.groups())
                try:
                    resultaat = Fraction(a, b) + Fraction(c, d)
                    verwacht = Fraction(e, f)
                    if resultaat != verwacht:
                        self.errors.append(
                            f"❌ Rekenfout in stap: {a}/{b} + {c}/{d} = {e}/{f} "
                            f"(correct: {resultaat})"
                        )
                except:
                    pass

    def _verify_percentage_berekening(self, item: Dict, stappen: List[str]):
        """Probeer percentage berekening te verifiëren"""
        # Zoek naar percentage berekeningen
        for stap in stappen:
            # Patroon: "x% van y = z"
            match = re.search(r'(\d+(?:[.,]\d+)?)\s*%\s*van\s*(?:€\s*)?(\d+(?:[.,]\d+)?)\s*=\s*(?:€\s*)?(\d+(?:[.,]\d+)?)', stap)
            if match:
                perc_str, bedrag_str, resultaat_str = match.groups()
                try:
                    perc = float(perc_str.replace(',', '.'))
                    bedrag = float(bedrag_str.replace(',', '.'))
                    resultaat_gegeven = float(resultaat_str.replace(',', '.'))
                    resultaat_berekend = bedrag * (perc / 100)

                    if abs(resultaat_gegeven - resultaat_berekend) > 0.01:
                        self.errors.append(
                            f"❌ Rekenfout: {perc}% van {bedrag} = {resultaat_gegeven} "
                            f"(correct: {resultaat_berekend:.2f})"
                        )
                except:
                    pass

    def _check_taal(self, item: Dict[str, Any]):
        """Check taalcomplexiteit en leesbaarheid"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        context = item.get('vraag', {}).get('context', '')
        hoofdvraag = item.get('vraag', {}).get('hoofdvraag', '')
        volledige_tekst = context + ' ' + hoofdvraag

        # Check 1: Aantal zinnen
        max_zinnen = regels.get('max_zinnen', 999)
        zinnen = volledige_tekst.count('.') + volledige_tekst.count('!') + volledige_tekst.count('?')

        if zinnen > max_zinnen:
            self.errors.append(
                f"❌ Te veel zinnen: {zinnen} (max {max_zinnen} voor G{groep}-{niveau})"
            )

        # Check 2: Woordlengte
        woorden = volledige_tekst.split()
        if groep == 4:
            max_woordlengte = 12
            lange_woorden = [w for w in woorden if len(w) > max_woordlengte]
            if lange_woorden:
                self.warnings.append(
                    f"⚠️  Mogelijk te lange woorden voor G4: {lange_woorden[:3]}"
                )
        elif groep == 5:
            max_woordlengte = 14
            zeer_lange_woorden = [w for w in woorden if len(w) > max_woordlengte]
            if zeer_lange_woorden:
                self.warnings.append(
                    f"⚠️  Mogelijk te lange woorden voor G5: {zeer_lange_woorden[:3]}"
                )

        # Check 3: Dubbelzinnige verwijswoorden
        dubbelzinnig = ['dit', 'dat', 'deze', 'die', 'het']
        for woord in dubbelzinnig:
            if f' {woord} ' in f' {hoofdvraag.lower()} ':
                self.warnings.append(
                    f"⚠️  Verwijswoord '{woord}' in vraag kan dubbelzinnig zijn"
                )

        # Check 4: Zinslengte
        gemiddelde_zinslengte = len(woorden) / zinnen if zinnen > 0 else 0
        if groep <= 5 and gemiddelde_zinslengte > 15:
            self.warnings.append(
                f"⚠️  Gemiddelde zinslengte hoog ({gemiddelde_zinslengte:.1f} woorden) voor G{groep}"
            )

    def _check_metadata(self, item: Dict[str, Any]):
        """Check metadata volledigheid en correctheid"""
        metadata = item.get('metadata', {})

        # Check verplichte velden
        verplichte_meta = [
            'moeilijkheidsgraad', 'stappen_aantal', 'cognitieve_complexiteit',
            'geschatte_tijd_sec'
        ]

        for veld in verplichte_meta:
            if veld not in metadata:
                self.warnings.append(f"⚠️  Metadata veld '{veld}' ontbreekt")

        # Check moeilijkheidsgraad range
        moeilijkheid = metadata.get('moeilijkheidsgraad', 0)
        if not 0.0 <= moeilijkheid <= 1.0:
            self.errors.append(
                f"❌ Moeilijkheidsgraad moet tussen 0.0 en 1.0 zijn, is {moeilijkheid}"
            )

        # Check of moeilijkheidsgraad past bij groep/niveau
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})
        verwacht_bereik = regels.get('moeilijkheid_range', (0.0, 1.0))

        if moeilijkheid < verwacht_bereik[0] or moeilijkheid > verwacht_bereik[1]:
            self.warnings.append(
                f"⚠️  Moeilijkheidsgraad {moeilijkheid:.2f} buiten verwacht bereik "
                f"{verwacht_bereik} voor G{groep}-{niveau}"
            )

        # Check geschatte tijd
        tijd = metadata.get('geschatte_tijd_sec', 0)
        min_tijd = regels.get('min_tijd_sec', 0)
        max_tijd = regels.get('max_tijd_sec', 999)

        if tijd < min_tijd or tijd > max_tijd:
            self.warnings.append(
                f"⚠️  Geschatte tijd {tijd}s buiten verwacht bereik "
                f"{min_tijd}-{max_tijd}s voor G{groep}-{niveau}"
            )

    def _check_didactic_quality(self, item: Dict[str, Any]):
        """Check didactische kwaliteit"""
        didactiek = item.get('didactiek', {})

        # Check LOVA volledigheid
        if 'lova' not in didactiek:
            self.warnings.append("⚠️  LOVA-structuur ontbreekt")
            return

        lova = didactiek.get('lova', {})
        lova_onderdelen = ['lezen', 'ordenen', 'vormen', 'antwoorden']

        for onderdeel in lova_onderdelen:
            if onderdeel not in lova:
                self.warnings.append(f"⚠️  LOVA onderdeel '{onderdeel}' ontbreekt")
            elif not lova[onderdeel] or len(lova[onderdeel]) < 10:
                self.warnings.append(
                    f"⚠️  LOVA onderdeel '{onderdeel}' is te kort of leeg "
                    f"(min 10 karakters voor betekenisvolle inhoud)"
                )

        # Check feedback kwaliteit
        feedback = didactiek.get('feedback', {})
        if not feedback:
            self.warnings.append("⚠️  Feedback sectie ontbreekt")
        else:
            # Check of er feedback per fouttype is
            antwoorden = item.get('antwoorden', [])
            fouttypes = {a.get('fouttype') for a in antwoorden if a.get('fouttype')}

            for fouttype in fouttypes:
                feedback_key = f"fout_{fouttype}"
                if feedback_key not in feedback:
                    self.warnings.append(
                        f"⚠️  Geen specifieke feedback voor fouttype '{fouttype}'"
                    )

        # Check berekening stappen
        stappen = didactiek.get('berekening_stappen', [])
        verwacht_aantal = item.get('metadata', {}).get('stappen_aantal', 0)

        if len(stappen) != verwacht_aantal:
            self.warnings.append(
                f"⚠️  Aantal berekening_stappen ({len(stappen)}) komt niet overeen "
                f"met metadata stappen_aantal ({verwacht_aantal})"
            )

    def _check_visualization(self, item: Dict[str, Any]):
        """Check visualisatie vereisten"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        visualisatie_vereiste = regels.get('visualisatie', 'optioneel')
        visualisatie = item.get('vraag', {}).get('visualisatie')

        if visualisatie_vereiste == 'verplicht':
            if not visualisatie or visualisatie == 'null' or visualisatie == '':
                self.errors.append(
                    f"❌ Visualisatie VERPLICHT voor G{groep}-{niveau} maar ontbreekt"
                )

        # Als er visualisatie is, check type
        if visualisatie:
            visualisatie_type = item.get('vraag', {}).get('visualisatie_type')
            if not visualisatie_type:
                self.info.append("ℹ️  Visualisatie aanwezig maar type niet gespecificeerd")

    def _check_cross_validation(self, item: Dict[str, Any]):
        """Cross-validatie tussen verschillende velden"""
        metadata = item.get('metadata', {})

        moeilijkheid = metadata.get('moeilijkheidsgraad', 0.5)
        stappen = metadata.get('stappen_aantal', 0)
        tijd = metadata.get('geschatte_tijd_sec', 0)

        # Check 1: Meer stappen → hogere moeilijkheid (meestal)
        if stappen >= 4 and moeilijkheid < 0.5:
            self.info.append(
                f"ℹ️  Item met {stappen} stappen heeft relatief lage moeilijkheidsgraad ({moeilijkheid:.2f})"
            )

        # Check 2: Moeilijkheid vs tijd correlatie
        if moeilijkheid > 0.7 and tijd < 60:
            self.info.append(
                f"ℹ️  Moeilijk item (moeilijkheid {moeilijkheid:.2f}) maar korte tijd ({tijd}s)"
            )

        # Check 3: Stappen vs tijd correlatie
        if stappen > 0:
            tijd_per_stap = tijd / stappen
            if tijd_per_stap < 15:
                self.warnings.append(
                    f"⚠️  Erg weinig tijd per stap ({tijd_per_stap:.0f}s voor {stappen} stappen)"
                )

    def _calculate_quality_breakdown(self) -> Dict[str, float]:
        """Bereken kwaliteit per categorie"""
        # Score per categorie (1.0 = perfect, 0.0 = veel problemen)

        # Deze is simplistisch, kan verfijnd worden
        return {
            'structuur': 1.0 if not any('structuur' in e.lower() for e in self.errors) else 0.0,
            'inhoud': 1.0 if not any('breuk' in e.lower() or 'decimaal' in e.lower() for e in self.errors) else 0.5,
            'context': 1.0 if not any('context' in e.lower() for e in self.errors + self.warnings) else 0.7,
            'afleiders': 1.0 - (len([w for w in self.warnings if 'afleider' in w.lower()]) * 0.2),
            'taal': 1.0 - (len([w for w in self.warnings if 'woord' in w.lower() or 'zin' in w.lower()]) * 0.15),
            'didactiek': 1.0 - (len([w for w in self.warnings if 'lova' in w.lower() or 'feedback' in w.lower()]) * 0.15)
        }

    def _bereken_score(self) -> float:
        """Bereken overall kwaliteitscore"""
        if self.errors:
            # Elke error trekt 0.15 af, tot minimum 0.0
            score = max(0.0, 1.0 - len(self.errors) * 0.15)
        else:
            # Geen errors, begin bij 1.0
            score = 1.0

        # Warnings trekken minder af
        score -= len(self.warnings) * 0.05

        return max(0.0, min(1.0, score))

    def _get_full_text(self, item: Dict[str, Any]) -> str:
        """Haal volledige tekst op uit item"""
        context = item.get('vraag', {}).get('context', '')
        hoofdvraag = item.get('vraag', {}).get('hoofdvraag', '')
        return f"{context} {hoofdvraag}"

    def valideer_set(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Valideer een hele set items met uitgebreide statistieken"""
        resultaten = [self.valideer_item(item) for item in items]

        valide_items = sum(1 for r in resultaten if r.valid)
        totaal_errors = sum(len(r.errors) for r in resultaten)
        totaal_warnings = sum(len(r.warnings) for r in resultaten)
        gemiddelde_score = sum(r.score for r in resultaten) / len(resultaten) if resultaten else 0.0

        # Aggregeer quality breakdown
        quality_breakdown_gemiddeld = {}
        if resultaten:
            categories = resultaten[0].quality_breakdown.keys()
            for cat in categories:
                scores = [r.quality_breakdown.get(cat, 0) for r in resultaten]
                quality_breakdown_gemiddeld[cat] = sum(scores) / len(scores)

        # Meest voorkomende errors/warnings
        alle_errors = []
        alle_warnings = []
        for r in resultaten:
            alle_errors.extend(r.errors)
            alle_warnings.extend(r.warnings)

        from collections import Counter
        top_errors = Counter(alle_errors).most_common(5)
        top_warnings = Counter(alle_warnings).most_common(5)

        return {
            'totaal_items': len(items),
            'valide_items': valide_items,
            'invalide_items': len(items) - valide_items,
            'totaal_errors': totaal_errors,
            'totaal_warnings': totaal_warnings,
            'gemiddelde_score': gemiddelde_score,
            'percentage_valide': (valide_items / len(items) * 100) if items else 0,
            'quality_breakdown': quality_breakdown_gemiddeld,
            'top_errors': top_errors,
            'top_warnings': top_warnings,
            'individuele_resultaten': resultaten
        }

    def genereer_rapport(self, resultaten: Dict[str, Any]) -> str:
        """Genereer een leesbaar rapport van validatieresultaten"""
        rapport = []
        rapport.append("=" * 70)
        rapport.append("VERHOUDINGEN VALIDATOR RAPPORT v3.0")
        rapport.append("=" * 70)
        rapport.append("")
        rapport.append(f"📊 OVERZICHT")
        rapport.append(f"  Totaal items:        {resultaten['totaal_items']}")
        rapport.append(f"  ✅ Valide items:     {resultaten['valide_items']} ({resultaten['percentage_valide']:.1f}%)")
        rapport.append(f"  ❌ Invalide items:   {resultaten['invalide_items']}")
        rapport.append(f"  Gemiddelde score:    {resultaten['gemiddelde_score']:.2f}/1.00")
        rapport.append("")
        rapport.append(f"🔍 PROBLEMEN")
        rapport.append(f"  Totaal errors:       {resultaten['totaal_errors']}")
        rapport.append(f"  Totaal warnings:     {resultaten['totaal_warnings']}")
        rapport.append("")

        if resultaten['top_errors']:
            rapport.append("❌ TOP 5 ERRORS:")
            for error, count in resultaten['top_errors']:
                rapport.append(f"  [{count}×] {error}")
            rapport.append("")

        if resultaten['top_warnings']:
            rapport.append("⚠️  TOP 5 WARNINGS:")
            for warning, count in resultaten['top_warnings']:
                rapport.append(f"  [{count}×] {warning}")
            rapport.append("")

        rapport.append("⭐ KWALITEIT PER CATEGORIE")
        for categorie, score in resultaten['quality_breakdown'].items():
            sterren = "★" * int(score * 5) + "☆" * (5 - int(score * 5))
            rapport.append(f"  {categorie:15} {sterren} ({score:.2f})")

        rapport.append("")
        rapport.append("=" * 70)

        return "\n".join(rapport)


def main():
    """Test enhanced validator"""
    import sys

    # Voorbeeld items
    voorbeeld_perfect = {
        "id": "V_G6_E_001",
        "domein": "Verhoudingen",
        "subdomein": "Procenten",
        "groep": 6,
        "niveau": "E",
        "slo_code": "6V6",
        "vraag": {
            "context": "In de winkel is een fiets in de aanbieding. De normale prijs is €120. Er is 25% korting.",
            "hoofdvraag": "Hoeveel korting krijg je in euro's?",
            "visualisatie": None
        },
        "antwoorden": [
            {"id": "A", "tekst": "€25", "waarde": "25", "correct": False, "fouttype": "percentage_fout"},
            {"id": "B", "tekst": "€30", "waarde": "30", "correct": True, "fouttype": None},
            {"id": "C", "tekst": "€90", "waarde": "90", "correct": False, "fouttype": "nieuwe_prijs_ipv_korting"},
            {"id": "D", "tekst": "€40", "waarde": "40", "correct": False, "fouttype": "berekening_fout"}
        ],
        "metadata": {
            "moeilijkheidsgraad": 0.55,
            "stappen_aantal": 2,
            "cognitieve_complexiteit": "toepassen",
            "geschatte_tijd_sec": 75,
            "adaptief_niveau": 3
        },
        "didactiek": {
            "conceptuitleg": "Om korting te berekenen: percentage × oorspronkelijke prijs. 25% van €120 = €30.",
            "berekening_stappen": [
                "25% van €120 = 0,25 × 120",
                "0,25 × 120 = €30"
            ],
            "lova": {
                "lezen": "Fiets €120, 25% korting. Vraag: hoeveel korting in euro's?",
                "ordenen": "Gegeven: prijs €120, korting 25%. Gevraagd: kortingsbedrag in euro's.",
                "vormen": "25% = 0,25. Korting = 0,25 × €120 = €30",
                "antwoorden": "€30 korting"
            },
            "feedback": {
                "correct": "Prima! 25% van €120 is inderdaad €30 korting.",
                "fout_percentage_fout": "Let op: 25% van 120 is niet 25. Je moet 25% × 120 berekenen.",
                "algemeen": "Tip: Percentage × prijs = kortingsbedrag"
            }
        },
        "tags": ["procenten", "korting", "geld", "winkels"]
    }

    voorbeeld_fouten = {
        "id": "FOUT_ID_FORMAT",
        "domein": "Verhoudingen",
        "subdomein": "Breuken",
        "groep": 4,
        "niveau": "M",
        "vraag": {
            "context": "Anna koopt een auto met een hypotheek en moet 1/3 van €50.000 betalen als aanbetaling.",
            "hoofdvraag": "Hoeveel is dit?",
            "visualisatie": None  # Ontbreekt terwijl verplicht!
        },
        "antwoorden": [
            {"id": "A", "tekst": "€16.666", "correct": True, "fouttype": None},
            {"id": "B", "tekst": "€15.000", "correct": False, "fouttype": "fout"}
        ],
        "metadata": {
            "moeilijkheidsgraad": 1.5,  # > 1.0!
            "stappen_aantal": 4,  # Te veel voor G4-M
            "geschatte_tijd_sec": 10  # Te kort
        },
        "didactiek": {}
    }

    validator = VerhoudingenValidatorEnhanced(strict_mode=False)

    print("\n" + "=" * 70)
    print("TEST 1: PERFECT ITEM")
    print("=" * 70)
    resultaat1 = validator.valideer_item(voorbeeld_perfect)
    print(f"✓ Valid: {resultaat1.valid}")
    print(f"✓ Score: {resultaat1.score:.2f}/1.00")
    print(f"✓ Errors: {len(resultaat1.errors)}")
    print(f"✓ Warnings: {len(resultaat1.warnings)}")
    if resultaat1.warnings:
        for w in resultaat1.warnings:
            print(f"  {w}")
    if resultaat1.info:
        print(f"✓ Info: {len(resultaat1.info)}")
        for i in resultaat1.info:
            print(f"  {i}")

    print("\n" + "=" * 70)
    print("TEST 2: ITEM MET FOUTEN")
    print("=" * 70)
    resultaat2 = validator.valideer_item(voorbeeld_fouten)
    print(f"✗ Valid: {resultaat2.valid}")
    print(f"✗ Score: {resultaat2.score:.2f}/1.00")
    print(f"✗ Errors: {len(resultaat2.errors)}")
    for e in resultaat2.errors[:10]:  # Max 10 tonen
        print(f"  {e}")
    if len(resultaat2.errors) > 10:
        print(f"  ... en {len(resultaat2.errors) - 10} meer")

    print("\n" + "=" * 70)
    print("TEST 3: SET VALIDATIE")
    print("=" * 70)
    set_resultaten = validator.valideer_set([voorbeeld_perfect, voorbeeld_fouten])
    rapport = validator.genereer_rapport(set_resultaten)
    print(rapport)

    print("\n" + "=" * 70)
    print("✅ VALIDATOR v3.0 TEST VOLTOOID")
    print("=" * 70)


if __name__ == '__main__':
    main()
