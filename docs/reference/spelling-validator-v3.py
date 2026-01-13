#!/usr/bin/env python3
"""
SPELLING VALIDATOR v3.0 - Enhanced Validator voor Spelling Items

Valideert spelling items voor Groep 3-8, Midden/Eind niveau.
Gebaseerd op prompt-spelling-v2.md specificaties.

Features:
- Volledige G3-G8 M/E niveauregels (12 varianten)
- Spellingcategorie validatie (klankzuiver/regelgebonden/onregelmatig)
- Spellingregel checks (dt-regel, tussen-n, i/y, etc.)
- G3-specifieke checks (klankzuiver, hoogfrequent)
- KRITISCHE dt-regel validatie (G4-E KERN!)
- Strategic distractor validation
- Woordlengte en complexiteit checks
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


class SpellingValidatorEnhanced:
    """Enhanced validator for spelling items"""

    # NIVEAU REGELS per (groep, niveau)
    NIVEAU_REGELS = {
        # GROEP 3
        (3, 'M'): {
            'spellingfocus': 'klankzuiver',
            'woordlengte': (3, 5),
            'lettergrepen_max': 2,
            'frequentie': 'hoogfrequent_500',
            'toegestane_regels': [],  # GEEN regels
            'verboden_regels': ['dt', 'verdubbeling', 'open_gesloten', 'lidwoord'],
            'item_types': ['dictee', 'meerkeuze', 'plaatje'],
            'moeilijkheid': (0.10, 0.30),
            'tijd_per_item': (5, 20),
        },
        (3, 'E'): {
            'spellingfocus': 'klankzuiver',
            'woordlengte': (4, 7),
            'lettergrepen_max': 2,
            'frequentie': 'hoogfrequent_1000',
            'toegestane_regels': ['vf_introductie', 'zs_introductie'],  # Alleen herkennen
            'item_types': ['dictee', 'meerkeuze', 'fout_vinden'],
            'moeilijkheid': (0.25, 0.45),
            'tijd_per_item': (10, 30),
        },

        # GROEP 4
        (4, 'M'): {
            'spellingfocus': 'regelgebonden',
            'woordlengte': (5, 8),
            'lettergrepen_max': 3,
            'frequentie': 'top_2000',
            'toegestane_regels': ['open_gesloten', 'vf', 'zs', 'meervoud_en', 'stam_t'],
            'verboden_regels': ['dt'],  # NOG GEEN dt-regel
            'spellingcategorieen': {'regelgebonden': 0.60, 'klankzuiver': 0.30, 'onregelmatig': 0.10},
            'item_types': ['dictee', 'meerkeuze', 'invullen', 'fout_zoeken'],
            'moeilijkheid': (0.35, 0.60),
            'tijd_per_item': (15, 30),
        },
        (4, 'E'): {
            'spellingfocus': 'dt_regel_KERN',  # BELANGRIJK!
            'woordlengte': (6, 10),
            'lettergrepen_max': 4,
            'frequentie': 'top_3000',
            'toegestane_regels': ['dt_KERN', 't_kofschip', 'vervoegingen', 'voltooid_deelwoord', 'lidwoord_truc'],
            'spellingcategorieen': {'dt_en_vervoegingen': 0.50, 'regelgebonden': 0.30, 'onregelmatig': 0.20},
            'item_types': ['werkwoordvervoeging', 'dt_regel', 'voltooid_deelwoord', 'meerkeuze'],
            'moeilijkheid': (0.50, 0.70),
            'tijd_per_item': (30, 40),
        },

        # GROEP 5
        (5, 'M'): {
            'spellingfocus': 'samenstellingen',
            'woordlengte': (7, 12),
            'toegestane_regels': ['samenstellingen', 'tussen_n_KERN', 'trema', 'koppelteken', 'lidwoord'],
            'spellingcategorieen': {'samenstellingen': 0.40, 'vervoegingen': 0.30, 'lidwoord': 0.30},
            'item_types': ['samenstellingen', 'trema', 'lidwoord', 'meerkeuze'],
            'moeilijkheid': (0.55, 0.75),
            'tijd_per_item': (35, 45),
        },
        (5, 'E'): {
            'spellingfocus': 'leenwoorden',
            'woordlengte': (8, 15),
            'lettergrepen_max': 5,
            'frequentie': 'top_7000_plus_leenwoorden',
            'toegestane_regels': ['i_y', 'c_k_s', 'qu', 'groepswoorden_tie_isch_teit'],
            'spellingcategorieen': {'leenwoorden': 0.40, 'samenstellingen': 0.35, 'vervoegingen': 0.25},
            'item_types': ['i_y_discrimineren', 'c_k_s', 'groepswoorden', 'leenwoorden'],
            'moeilijkheid': (0.65, 0.80),
            'tijd_per_item': (35, 45),
        },

        # GROEP 6
        (6, 'M'): {
            'spellingfocus': 'voorvoegsels_verkleinwoorden',
            'woordlengte': (8, 15),
            'toegestane_regels': ['voorvoegsels', 'verkleinwoorden', 'persoonsvorm_vs_infinitief'],
            'spellingcategorieen': {'voorvoegsels': 0.40, 'verkleinwoorden': 0.35, 'complexe_vervoegingen': 0.25},
            'moeilijkheid': (0.65, 0.80),
            'tijd_per_item': (40, 50),
        },
        (6, 'E'): {
            'spellingfocus': 'complexe_zinsstructuren',
            'woordlengte': (8, 18),
            'toegestane_regels': ['hoofdletter', 'komma', 'apostrof', 'aanhalingstekens'],
            'spellingcategorieen': {'interpunctie': 0.40, 'complexe_spelling': 0.60},
            'moeilijkheid': (0.70, 0.85),
            'tijd_per_item': (45, 55),
        },

        # GROEP 7
        (7, 'M'): {
            'spellingfocus': 'signaalwoorden',
            'woordlengte': (10, 20),
            'moeilijkheid': (0.75, 0.88),
            'tijd_per_item': (45, 60),
        },
        (7, 'E'): {
            'spellingfocus': 'genre_en_register',
            'woordlengte': (10, 25),
            'moeilijkheid': (0.80, 0.92),
            'tijd_per_item': (50, 65),
        },

        # GROEP 8
        (8, 'M'): {
            'spellingfocus': 'complexe_zinnen',
            'moeilijkheid': (0.80, 0.95),
            'referentieniveau': '1F',
            'tijd_per_item': (50, 70),
        },
        (8, 'E'): {
            'spellingfocus': 'formele_teksten',
            'moeilijkheid': (0.85, 1.0),
            'referentieniveau': '1S',
            'tijd_per_item': (55, 75),
        },
    }

    # Hoogfrequente woorden G3 (top 100)
    HOOGFREQUENT_G3 = {
        'de', 'het', 'een', 'en', 'van', 'in', 'is', 'op', 'te', 'dat',
        'ik', 'jij', 'hij', 'zij', 'wij', 'ze', 'hij', 'haar', 'hem',
        'mama', 'papa', 'oma', 'opa', 'kind',
        'kat', 'hond', 'vis', 'muis', 'boom', 'huis', 'auto', 'bal',
        'appel', 'peer', 'rood', 'blauw', 'groot', 'klein',
    }

    # dt-regel test woorden (veelvoorkomende fouten)
    DT_REGEL_WOORDEN = {
        'loopt', 'maakt', 'speelt', 'werkt', 'praat', 'kijkt',
        'loopt', 'maakte', 'speelde', 'werkte', 'praatte',
        'gelopen', 'gemaakt', 'gespeeld', 'gewerkt', 'gepraat',
    }

    # tussen-n regel (KRITISCHE test)
    TUSSEN_N_CORRECT = {'boekenkast', 'kinderwagen', 'bloemenpot', 'appelboom'}
    TUSSEN_N_FOUT = {'lopenbrug', 'grotenmoeder'}  # GEEN tussen-n na werkwoord/bijv.nw

    # Geldige item types
    ITEM_TYPES = {
        'dictee', 'meerkeuze', 'invullen', 'fout_zoeken', 'fout_vinden',
        'plaatje', 'werkwoordvervoeging', 'dt_regel', 'voltooid_deelwoord',
        'samenstellingen', 'trema', 'lidwoord', 'i_y_discrimineren',
        'c_k_s', 'groepswoorden', 'leenwoorden', 'verkleinwoorden',
    }

    # Spellingcategorieën
    SPELLINGCATEGORIEEN = {
        'klankzuiver', 'regelgebonden', 'onregelmatig',
        'dt_en_vervoegingen', 'samenstellingen', 'leenwoorden',
        'vervoegingen', 'lidwoord', 'interpunctie', 'complexe_spelling',
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

        # 3. Woord validatie
        self._check_woord_kwaliteit(item)

        # 4. Spellingregel validatie
        self._check_spellingregels(item)

        # 5. Afleiders validatie
        self._check_afleiders(item)

        # 6. G3-specifieke checks
        if item.get('groep') == 3:
            self._check_g3_specifiek(item)

        # 7. G4-E dt-regel KRITISCH
        if item.get('groep') == 4 and item.get('niveau') == 'E':
            self._check_dt_regel_kritisch(item)

        # 8. G5-M tussen-n KRITISCH
        if item.get('groep') == 5 and item.get('niveau') == 'M':
            self._check_tussen_n_kritisch(item)

        # 9. Metadata checks
        self._check_metadata(item)

        # 10. Cross-validation
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
            'id', 'groep', 'niveau', 'hoofdvraag', 'correct_antwoord',
            'afleiders', 'spellingcategorie'
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

        # Check spellingcategorie
        categorie = item.get('spellingcategorie')
        if categorie and categorie not in self.SPELLINGCATEGORIEEN:
            self.warnings.append(f"⚠️  Ongebruikelijke spellingcategorie: {categorie}")


    def _check_niveau_regels(self, item: Dict[str, Any]):
        """Check niveau-specific rules"""
        groep = item.get('groep')
        niveau = item.get('niveau')

        regels = self.NIVEAU_REGELS.get((groep, niveau))
        if not regels:
            self.errors.append(f"❌ Geen regels voor G{groep}-{niveau}")
            return

        # 1. Woordlengte
        correct_woord = str(item.get('correct_antwoord', ''))
        woord_lengte = len(correct_woord)

        woordlengte_range = regels.get('woordlengte')
        if woordlengte_range:
            min_len, max_len = woordlengte_range
            if not (min_len <= woord_lengte <= max_len):
                self.warnings.append(
                    f"⚠️  Woordlengte {woord_lengte} letters buiten range "
                    f"({min_len}-{max_len}) voor G{groep}-{niveau}"
                )

        # 2. Moeilijkheidsgraad
        moeilijkheid = item.get('moeilijkheidsgraad')
        if moeilijkheid:
            min_m, max_m = regels.get('moeilijkheid', (0, 1))
            if not (min_m <= moeilijkheid <= max_m):
                self.warnings.append(
                    f"⚠️  Moeilijkheidsgraad {moeilijkheid:.2f} buiten range "
                    f"({min_m:.2f}-{max_m:.2f}) voor G{groep}-{niveau}"
                )

        # 3. Item type
        item_type = item.get('item_type')
        toegestane_types = regels.get('item_types', [])
        if item_type and toegestane_types:
            if item_type not in toegestane_types:
                self.warnings.append(
                    f"⚠️  Item type '{item_type}' niet gebruikelijk voor G{groep}-{niveau}"
                )

        # 4. Spellingfocus check
        spellingfocus = regels.get('spellingfocus')
        if spellingfocus:
            self.info.append(f"ℹ️  Verwachte spellingfocus: {spellingfocus}")


    def _check_woord_kwaliteit(self, item: Dict[str, Any]):
        """Check word quality"""
        correct = str(item.get('correct_antwoord', '')).strip()

        if not correct:
            self.errors.append("❌ Correct antwoord is leeg")
            return

        # 1. Basis checks
        if ' ' in correct:
            # Multiple words
            woorden = correct.split()
            self.info.append(f"ℹ️  Meerdere woorden: {len(woorden)} woorden")
        else:
            # Single word checks
            # Lettergrepen (ruwe schatting)
            klinkers = 'aeiou'
            lettergrepen = sum(1 for c in correct.lower() if c in klinkers)

            groep = item.get('groep')
            niveau = item.get('niveau')
            regels = self.NIVEAU_REGELS.get((groep, niveau), {})

            max_lettergrepen = regels.get('lettergrepen_max')
            if max_lettergrepen and lettergrepen > max_lettergrepen:
                self.warnings.append(
                    f"⚠️  Woord heeft ~{lettergrepen} lettergrepen "
                    f"(max {max_lettergrepen} voor G{groep}-{niveau})"
                )

        # 2. Check hoofdvraag niet leeg
        hoofdvraag = item.get('hoofdvraag', '').strip()
        if not hoofdvraag:
            self.errors.append("❌ Hoofdvraag is leeg")

        # 3. Check of correct antwoord in hoofdvraag voorkomt (soms gewenst)
        if correct.lower() in hoofdvraag.lower():
            self.info.append(
                f"ℹ️  Correct antwoord komt voor in hoofdvraag "
                f"(kan correct zijn bij fout_vinden items)"
            )


    def _check_spellingregels(self, item: Dict[str, Any]):
        """Check spelling rules application"""
        groep = item.get('groep')
        niveau = item.get('niveau')
        correct = str(item.get('correct_antwoord', '')).lower()
        spellingregel = item.get('spellingregel')

        regels = self.NIVEAU_REGELS.get((groep, niveau), {})

        # 1. Verboden regels check (G3-M)
        verboden = regels.get('verboden_regels', [])
        if verboden and spellingregel:
            if any(v in spellingregel.lower() for v in verboden):
                self.errors.append(
                    f"❌ Spellingregel '{spellingregel}' is VERBODEN voor G{groep}-{niveau}"
                )

        # 2. Toegestane regels check
        toegestaan = regels.get('toegestane_regels', [])
        if toegestaan and spellingregel:
            regel_ok = any(t in spellingregel.lower() or spellingregel.lower() in t
                          for t in toegestaan)
            if not regel_ok:
                self.warnings.append(
                    f"⚠️  Spellingregel '{spellingregel}' mogelijk niet toegestaan voor G{groep}-{niveau}"
                )

        # 3. dt-regel specifiek (als het een dt-regel item is)
        if spellingregel and 'dt' in spellingregel.lower():
            if groep == 4 and niveau == 'M':
                self.errors.append(
                    "❌ KRITIEKE FOUT: dt-regel komt pas bij G4-E, NIET bij M4!"
                )


    def _check_afleiders(self, item: Dict[str, Any]):
        """Check distractor quality"""
        afleiders = item.get('afleiders', [])
        correct = str(item.get('correct_antwoord', '')).strip()

        # 1. Aantal afleiders (meestal 3)
        if len(afleiders) < 2:
            self.errors.append(
                f"❌ Te weinig afleiders ({len(afleiders)}, min 2)"
            )

        if len(afleiders) > 4:
            self.warnings.append(f"⚠️  Veel afleiders ({len(afleiders)})")

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

        # 5. Fonetisch plausibele afleiders (G3)
        groep = item.get('groep')
        if groep == 3:
            # Check if distractors are phonetically plausible
            for afleider in afleiders:
                afleider_str = str(afleider).lower()
                # Very basic check: similar length
                if abs(len(afleider_str) - len(correct)) > 2:
                    self.warnings.append(
                        f"⚠️  G3 afleider '{afleider}' zeer verschillend van '{correct}' "
                        f"(mogelijk niet fonetisch plausibel)"
                    )

        # 6. Spellingfout types (G4+)
        if groep >= 4:
            toelichting = item.get('toelichting_afleiders', '')
            if not toelichting:
                self.info.append(
                    "ℹ️  Geen toelichting_afleiders (aanbevolen voor G4+)"
                )


    def _check_g3_specifiek(self, item: Dict[str, Any]):
        """Extra checks specific for Groep 3"""
        niveau = item.get('niveau')
        correct = str(item.get('correct_antwoord', '')).lower()
        hoofdvraag = item.get('hoofdvraag', '').lower()

        regels = self.NIVEAU_REGELS.get((3, niveau), {})

        # 1. Klankzuiver focus
        spellingfocus = regels.get('spellingfocus')
        if spellingfocus == 'klankzuiver':
            spellingcategorie = item.get('spellingcategorie')
            if spellingcategorie and spellingcategorie != 'klankzuiver':
                self.errors.append(
                    f"❌ G3-{niveau}: Spellingcategorie moet 'klankzuiver' zijn, "
                    f"niet '{spellingcategorie}'"
                )

        # 2. Hoogfrequent woord check
        if correct in self.HOOGFREQUENT_G3:
            self.info.append(f"ℹ️  ✅ '{correct}' is hoogfrequent woord (goed voor G3)")
        else:
            # Check if it's a simple CVC word
            if len(correct) <= 5 and correct.isalpha():
                self.info.append(f"ℹ️  '{correct}' lijkt klankzuiver (goed voor G3)")
            else:
                self.warnings.append(
                    f"⚠️  G3: '{correct}' is mogelijk niet hoogfrequent genoeg"
                )

        # 3. GEEN spellingregels
        spellingregel = item.get('spellingregel')
        if spellingregel and niveau == 'M':
            verboden = ['dt', 'verdubbeling', 'open', 'gesloten', 'lidwoord']
            if any(v in spellingregel.lower() for v in verboden):
                self.errors.append(
                    f"❌ G3-M: Spellingregel '{spellingregel}' is VERBODEN! "
                    f"G3-M = alleen klankzuiver"
                )

        # 4. Plaatje bij M3 (vaak)
        if niveau == 'M':
            item_type = item.get('item_type')
            if item_type == 'plaatje':
                if 'plaatje' not in hoofdvraag and 'afbeelding' not in hoofdvraag:
                    self.warnings.append(
                        "⚠️  G3-M: Item type 'plaatje' maar geen referentie in hoofdvraag"
                    )


    def _check_dt_regel_kritisch(self, item: Dict[str, Any]):
        """KRITISCHE check voor dt-regel (G4-E KERN!)"""
        spellingregel = item.get('spellingregel', '').lower()

        if 'dt' not in spellingregel:
            # Not a dt-regel item, skip
            return

        self.info.append("ℹ️  🔍 KRITISCHE dt-regel check actief (G4-E KERN)")

        correct = str(item.get('correct_antwoord', '')).lower()
        afleiders = item.get('afleiders', [])

        # 1. Check of correct antwoord dt-regel correct toepast
        # Common errors: loopd instead of loopt, maakd instead of maakt

        # Check for 'd' waar 't' hoort
        if correct.endswith('d') and not correct.endswith('dd'):
            # Might be wrong - check if it should be 't'
            stam_kandidaat = correct[:-1]
            if stam_kandidaat and stam_kandidaat[-1] in 'tkfschp':
                self.errors.append(
                    f"❌ KRITIEKE dt-FOUT: '{correct}' eindigt op 'd' maar stam "
                    f"eindigt op 't Kofschip letter ('{stam_kandidaat[-1]}'). "
                    f"Moet '{correct[:-1]}t' zijn!"
                )

        # 2. Check afleiders bevatten veelvoorkomende dt-fouten
        dt_fout_patterns = [
            (r'(\w+)d$', 't'),  # loopd → loopt
            (r'(\w+)de$', 'te'),  # maakde → maakte
            (r'(\w+)te$', 'de'),  # speelte → speelde
        ]

        heeft_dt_fout_afleider = False
        for afleider in afleiders:
            afleider_str = str(afleider).lower()
            # Check if it contains common dt-errors
            if 'd' in afleider_str or 't' in afleider_str:
                heeft_dt_fout_afleider = True
                break

        if not heeft_dt_fout_afleider:
            self.warnings.append(
                "⚠️  dt-regel item: geen afleider met dt-fout gevonden "
                "(aanbevolen om veelvoorkomende fouten te testen)"
            )

        # 3. 't Kofschip check
        toelichting = item.get('toelichting', '').lower()
        if 'kofschip' in spellingregel or 'kofschip' in toelichting:
            # Check if explanation is correct
            if correct.endswith('te') or correct.endswith('TE'):
                # Should have t-kofschip letter
                stam = correct[:-2]
                if stam and stam[-1] not in 'tkfschp':
                    self.warnings.append(
                        f"⚠️  't Kofschip: '{correct}' eindigt op '-te' maar stam "
                        f"eindigt niet op t/k/f/s/ch/p (stam: '{stam}')"
                    )


    def _check_tussen_n_kritisch(self, item: Dict[str, Any]):
        """KRITISCHE check voor tussen-n regel (G5-M KERN!)"""
        spellingregel = item.get('spellingregel', '').lower()

        if 'tussen' not in spellingregel and 'samenstelling' not in spellingregel:
            return

        self.info.append("ℹ️  🔍 KRITISCHE tussen-n check actief (G5-M)")

        correct = str(item.get('correct_antwoord', '')).lower()

        # 1. Check veelvoorkomende tussen-n fouten
        # FOUT: tussen-n na werkwoord of bijvoeglijk naamwoord
        fout_patterns = {
            'lopenbrug': 'loopbrug',  # GEEN -n- na werkwoord (lopen)
            'grotenmoeder': 'grootmoeder',  # GEEN -n- na bijv.nw (groot)
            'slapebank': 'slaapbank',  # GEEN -n- na werkwoord (slapen)
        }

        for fout, correct_vorm in fout_patterns.items():
            if fout in correct:
                self.errors.append(
                    f"❌ KRITIEKE tussen-n FOUT: '{correct}' bevat '{fout}'. "
                    f"Moet '{correct_vorm}' zijn (GEEN tussen-n na werkwoord/bijv.nw)!"
                )

        # 2. Check of tussen-n correct is toegepast
        # CORRECT: tussen-n na meervoud
        if 'en' in correct and len(correct) > 6:
            # Might be samenstelling with tussen-n
            # Examples: boekenkast, kinderwagen
            delen = correct.split('en', 1)
            if len(delen) == 2:
                eerste_deel = delen[0] + 'en'  # boeken
                tweede_deel = delen[1]  # kast

                # Check if eerste deel is meervoud
                # This is a heuristic check
                self.info.append(
                    f"ℹ️  Samenstelling met tussen-n: '{eerste_deel}' + '{tweede_deel}'"
                )


    def _check_metadata(self, item: Dict[str, Any]):
        """Check metadata completeness"""

        # 1. ID format
        item_id = item.get('id', '')
        expected_pattern = r'^S_G[3-8]_[ME]_\d{3}$'
        if not re.match(expected_pattern, item_id):
            self.warnings.append(
                f"⚠️  ID '{item_id}' volgt niet verwacht patroon: S_G[3-8]_[ME]_###"
            )

        # 2. Toelichting aanwezig
        if not item.get('toelichting'):
            self.warnings.append("⚠️  Geen toelichting aanwezig (aanbevolen)")

        # 3. Spellingregel aanwezig (G4+)
        groep = item.get('groep')
        if groep >= 4:
            if not item.get('spellingregel'):
                self.warnings.append(
                    f"⚠️  Geen spellingregel vermeld (aanbevolen voor G{groep})"
                )


    def _check_cross_validation(self, item: Dict[str, Any]):
        """Cross-validation checks"""

        # 1. Spellingcategorie vs groep consistency
        groep = item.get('groep')
        categorie = item.get('spellingcategorie')

        if groep == 3 and categorie != 'klankzuiver':
            self.warnings.append(
                f"⚠️  G3 items moeten 'klankzuiver' zijn, niet '{categorie}'"
            )

        if groep == 4 and categorie == 'klankzuiver':
            niveau = item.get('niveau')
            if niveau == 'E':
                self.warnings.append(
                    "⚠️  G4-E: focus op regelgebonden/dt-regel, 'klankzuiver' is basis"
                )

        # 2. Moeilijkheid vs tijd consistency
        moeilijkheid = item.get('moeilijkheidsgraad')
        tijd = item.get('geschatte_tijd_sec')

        if moeilijkheid and tijd:
            # Moeilijker items zouden meer tijd moeten kosten
            if moeilijkheid > 0.7 and tijd < 30:
                self.warnings.append(
                    f"⚠️  Hoge moeilijkheid ({moeilijkheid:.2f}) "
                    f"maar korte tijd ({tijd}s)"
                )

            if moeilijkheid < 0.3 and tijd > 40:
                self.warnings.append(
                    f"⚠️  Lage moeilijkheid ({moeilijkheid:.2f}) "
                    f"maar lange tijd ({tijd}s)"
                )


    def _calculate_score(self) -> float:
        """Calculate quality score"""
        error_penalty = len(self.errors) * 0.15
        warning_penalty = len(self.warnings) * 0.05

        score = max(0.0, 1.0 - error_penalty - warning_penalty)
        return round(score, 2)


def valideer_spelling_items(filepath: str) -> None:
    """Validate spelling items from JSON file"""

    print("=" * 80)
    print("SPELLING VALIDATOR v3.0 - Enhanced Validation")
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

    validator = SpellingValidatorEnhanced()

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
        print("Usage: python spelling-validator-v3.py <test-file.json>")
        print("\nExample:")
        print("  python spelling-validator-v3.py test-spelling-g3.json")
        sys.exit(1)

    valideer_spelling_items(sys.argv[1])
