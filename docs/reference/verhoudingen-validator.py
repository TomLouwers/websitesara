"""
VERHOUDINGEN VALIDATOR v2.0
Validatiescript voor gegenereerde verhoudingen items
"""

import json
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Resultaat van validatie"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    score: float  # 0.0 - 1.0


class VerhoudingenValidator:
    """Validator voor Verhoudingen domein items"""

    # Niveauregels per groep/niveau
    NIVEAU_REGELS = {
        (4, 'M'): {
            'stambreuken': ['1/2', '1/4'],
            'max_getal': 20,
            'max_stappen': 1,
            'visualisatie': 'verplicht',
            'subdomeinen': ['Breuken'],
            'bewerkingen': ['herkennen'],
            'max_zinnen': 3
        },
        (4, 'E'): {
            'stambreuken': ['1/2', '1/3', '1/4'],
            'max_getal': 50,
            'max_stappen': 2,
            'visualisatie': 'verplicht',
            'subdomeinen': ['Breuken'],
            'bewerkingen': ['herkennen', 'berekenen_eenvoudig', 'vergelijken'],
            'max_zinnen': 4
        },
        (5, 'M'): {
            'stambreuken': ['1/2', '1/3', '1/4', '1/5', '1/6', '1/8', '1/10'],
            'niet_stambreuken': ['2/3', '2/4', '3/4', '2/5', '3/5'],
            'decimalen': [0.1, 0.9, 1.0, 10.0],
            'percentages': [50, 100],
            'max_getal': 100,
            'max_stappen': 2,
            'visualisatie': 'optioneel',
            'subdomeinen': ['Breuken', 'Decimalen', 'Procenten'],
            'max_zinnen': 4
        },
        (5, 'E'): {
            'breuken_bewerkingen': ['optellen_zelfde_noemer', 'aftrekken_zelfde_noemer'],
            'decimalen_cijfers': 2,
            'max_noemer': 10,
            'max_stappen': 3,
            'subdomeinen': ['Breuken', 'Decimalen', 'Procenten'],
            'max_zinnen': 4
        },
        (6, 'M'): {
            'breuken_bewerkingen': ['optellen_andere_noemer', 'vermenigvuldigen', 'delen'],
            'percentages': [10, 25, 50, 75, 100],
            'verhoudingstabellen': True,
            'schaal': ['1:100', '1:1000'],
            'max_stappen': 4,
            'subdomeinen': ['Breuken', 'Decimalen', 'Procenten', 'Verhoudingstabellen', 'Schaal'],
            'max_zinnen': 6
        },
        (6, 'E'): {
            'conversies': True,
            'procenten_omgekeerd': True,
            'max_stappen': 4,
            'subdomeinen': ['Breuken', 'Decimalen', 'Procenten', 'Verhoudingstabellen', 'Schaal'],
            'max_zinnen': 6
        },
        (7, 'M'): {
            'verhoudingstabellen_complex': True,
            'percentages_samengesteld': True,
            'kortingen': True,
            'max_stappen': 4,
            'subdomeinen': ['Verhoudingstabellen', 'Procenten', 'Schaal'],
            'max_zinnen': 6
        },
        (7, 'E'): {
            'schaal_gevorderd': ['1:50', '1:500', '1:50000'],
            'prijsverhoudingen': True,
            'grafieken': ['cirkeldiagram'],
            'max_stappen': 4,
            'subdomeinen': ['Verhoudingstabellen', 'Procenten', 'Schaal'],
            'max_zinnen': 8
        },
        (8, 'M'): {
            'rente': True,
            'btw': [9, 21],
            'gemiddelde_verhoudingen': True,
            'referentieniveau': '1F',
            'max_stappen': 4,
            'subdomeinen': ['Verhoudingstabellen', 'Procenten', 'Schaal'],
            'max_zinnen': 8
        },
        (8, 'E'): {
            'schaal_complex': True,
            'woordproblemen_meerstaps': True,
            'integraal': True,
            'referentieniveau': '1S',
            'max_stappen': 5,
            'subdomeinen': ['Verhoudingstabellen', 'Procenten', 'Schaal', 'Integraal'],
            'max_zinnen': 8
        }
    }

    def __init__(self):
        self.errors = []
        self.warnings = []

    def valideer_item(self, item: Dict[str, Any]) -> ValidationResult:
        """Valideer een enkel item"""
        self.errors = []
        self.warnings = []

        # Basis structuur checks
        self._check_basis_structuur(item)

        # Niveau checks
        self._check_niveau_regels(item)

        # Afleider checks
        self._check_afleiders(item)

        # Taal checks
        self._check_taal(item)

        # Metadata checks
        self._check_metadata(item)

        # Bereken score
        score = self._bereken_score()

        return ValidationResult(
            valid=len(self.errors) == 0,
            errors=self.errors,
            warnings=self.warnings,
            score=score
        )

    def _check_basis_structuur(self, item: Dict[str, Any]):
        """Check of alle verplichte velden aanwezig zijn"""
        verplichte_velden = [
            'id', 'domein', 'subdomein', 'groep', 'niveau',
            'vraag', 'antwoorden', 'metadata', 'didactiek'
        ]

        for veld in verplichte_velden:
            if veld not in item:
                self.errors.append(f"Verplicht veld '{veld}' ontbreekt")

        # Check domein
        if item.get('domein') != 'Verhoudingen':
            self.errors.append(f"Domein moet 'Verhoudingen' zijn, is '{item.get('domein')}'")

        # Check groep en niveau
        if item.get('groep') not in [4, 5, 6, 7, 8]:
            self.errors.append(f"Groep moet 4-8 zijn, is {item.get('groep')}")

        if item.get('niveau') not in ['M', 'E']:
            self.errors.append(f"Niveau moet M of E zijn, is '{item.get('niveau')}'")

    def _check_niveau_regels(self, item: Dict[str, Any]):
        """Check of item binnen niveauregels valt"""
        groep = item.get('groep')
        niveau = item.get('niveau')

        if (groep, niveau) not in self.NIVEAU_REGELS:
            self.errors.append(f"Geen regels gedefinieerd voor groep {groep} niveau {niveau}")
            return

        regels = self.NIVEAU_REGELS[(groep, niveau)]

        # Check max stappen
        stappen = item.get('metadata', {}).get('stappen_aantal', 0)
        if stappen > regels.get('max_stappen', 999):
            self.errors.append(
                f"Te veel stappen: {stappen} (max {regels['max_stappen']} voor G{groep}-{niveau})"
            )

        # Check subdomeinen
        subdomein = item.get('subdomein')
        toegestane_subdomeinen = regels.get('subdomeinen', [])
        if subdomein and toegestane_subdomeinen and subdomein not in toegestane_subdomeinen:
            self.errors.append(
                f"Subdomein '{subdomein}' niet toegestaan voor G{groep}-{niveau}. "
                f"Toegestaan: {toegestane_subdomeinen}"
            )

        # Specifieke checks voor groep 4-5
        if groep == 4 and niveau == 'M':
            # Alleen stambreuken 1/2 en 1/4
            vraag_tekst = item.get('vraag', {}).get('context', '') + item.get('vraag', {}).get('hoofdvraag', '')
            if '1/3' in vraag_tekst or '1/5' in vraag_tekst:
                self.errors.append("G4-M mag alleen 1/2 en 1/4, geen andere breuken!")

        if groep == 5 and niveau == 'M' and subdomein == 'Procenten':
            # Alleen 50% en 100%
            vraag_tekst = item.get('vraag', {}).get('context', '') + item.get('vraag', {}).get('hoofdvraag', '')
            if any(p in vraag_tekst for p in ['10%', '25%', '75%', '20%']):
                self.warnings.append("G5-M procenten: alleen 50% en 100% toegestaan volgens regels")

    def _check_afleiders(self, item: Dict[str, Any]):
        """Check afleiders en fouttypes"""
        antwoorden = item.get('antwoorden', [])

        # Check aantal
        if len(antwoorden) != 4:
            self.errors.append(f"Moet exact 4 antwoorden hebben, heeft {len(antwoorden)}")

        # Check exact 1 correct
        correct_count = sum(1 for a in antwoorden if a.get('correct', False))
        if correct_count != 1:
            self.errors.append(f"Moet exact 1 correct antwoord hebben, heeft {correct_count}")

        # Check verschillende fouttypes
        fouttypes = [a.get('fouttype') for a in antwoorden if a.get('fouttype')]
        if len(fouttypes) != len(set(fouttypes)):
            self.warnings.append("Afleiders hebben overlappende fouttypes (bij voorkeur uniek)")

        # Check of fouttypes logisch zijn voor domein
        geldige_fouttypes = [
            'conversie_fout', 'bewerking_fout', 'niet_vereenvoudigd',
            'verkeerde_noemer', 'omgedraaid', 'percentage_fout',
            'factor_fout', 'schaal_fout', 'stap_vergeten', 'plaatswaarde_fout'
        ]

        for a in antwoorden:
            if a.get('fouttype') and a['fouttype'] not in geldige_fouttypes:
                self.warnings.append(f"Ongebruikelijk fouttype: {a['fouttype']}")

    def _check_taal(self, item: Dict[str, Any]):
        """Check taalcomplexiteit"""
        groep = item.get('groep')
        niveau = item.get('niveau')

        regels = self.NIVEAU_REGELS.get((groep, niveau), {})
        max_zinnen = regels.get('max_zinnen', 999)

        context = item.get('vraag', {}).get('context', '')
        hoofdvraag = item.get('vraag', {}).get('hoofdvraag', '')
        volledige_tekst = context + ' ' + hoofdvraag

        # Tel zinnen (simpele benadering)
        zinnen = volledige_tekst.count('.') + volledige_tekst.count('!') + volledige_tekst.count('?')

        if zinnen > max_zinnen:
            self.errors.append(
                f"Te veel zinnen: {zinnen} (max {max_zinnen} voor G{groep}-{niveau})"
            )

        # Check woord lengte voor jonge groepen
        if groep == 4:
            woorden = volledige_tekst.split()
            lange_woorden = [w for w in woorden if len(w) > 12]
            if lange_woorden:
                self.warnings.append(
                    f"Mogelijk te lange woorden voor G4: {lange_woorden[:3]}"
                )

    def _check_metadata(self, item: Dict[str, Any]):
        """Check metadata velden"""
        metadata = item.get('metadata', {})

        # Check verplichte metadata velden
        verplichte_meta = [
            'moeilijkheidsgraad', 'stappen_aantal', 'cognitieve_complexiteit'
        ]

        for veld in verplichte_meta:
            if veld not in metadata:
                self.warnings.append(f"Metadata veld '{veld}' ontbreekt")

        # Check moeilijkheidsgraad range
        moeilijkheid = metadata.get('moeilijkheidsgraad', 0)
        if not 0.0 <= moeilijkheid <= 1.0:
            self.errors.append(
                f"Moeilijkheidsgraad moet tussen 0.0 en 1.0 zijn, is {moeilijkheid}"
            )

        # Check didactiek
        didactiek = item.get('didactiek', {})
        if 'lova' not in didactiek:
            self.warnings.append("LOVA-structuur ontbreekt in didactiek")

        lova = didactiek.get('lova', {})
        lova_onderdelen = ['lezen', 'ordenen', 'vormen', 'antwoorden']
        for onderdeel in lova_onderdelen:
            if onderdeel not in lova:
                self.warnings.append(f"LOVA onderdeel '{onderdeel}' ontbreekt")

    def _bereken_score(self) -> float:
        """Bereken kwaliteitscore 0.0 - 1.0"""
        if self.errors:
            return 0.0

        # Start met perfecte score
        score = 1.0

        # Trek af voor warnings
        score -= len(self.warnings) * 0.05

        return max(0.0, score)

    def valideer_set(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Valideer een hele set items"""
        resultaten = [self.valideer_item(item) for item in items]

        valide_items = sum(1 for r in resultaten if r.valid)
        totaal_errors = sum(len(r.errors) for r in resultaten)
        totaal_warnings = sum(len(r.warnings) for r in resultaten)
        gemiddelde_score = sum(r.score for r in resultaten) / len(resultaten) if resultaten else 0.0

        return {
            'totaal_items': len(items),
            'valide_items': valide_items,
            'invalide_items': len(items) - valide_items,
            'totaal_errors': totaal_errors,
            'totaal_warnings': totaal_warnings,
            'gemiddelde_score': gemiddelde_score,
            'percentage_valide': (valide_items / len(items) * 100) if items else 0,
            'individuele_resultaten': resultaten
        }


def main():
    """Test validator met voorbeeld"""

    # Voorbeeld item (correct)
    voorbeeld_correct = {
        "id": "V_G5_E_001",
        "domein": "Verhoudingen",
        "subdomein": "Breuken",
        "groep": 5,
        "niveau": "E",
        "vraag": {
            "context": "Anna heeft een taart in 4 gelijke stukken gesneden. Ze eet 2 stukken op.",
            "hoofdvraag": "Welk deel van de taart heeft Anna opgegeten?"
        },
        "antwoorden": [
            {"id": "A", "tekst": "2/4", "correct": False, "fouttype": "niet_vereenvoudigd"},
            {"id": "B", "tekst": "1/2", "correct": True, "fouttype": None},
            {"id": "C", "tekst": "2/8", "correct": False, "fouttype": "verkeerde_noemer"},
            {"id": "D", "tekst": "4/2", "correct": False, "fouttype": "omgedraaid"}
        ],
        "metadata": {
            "moeilijkheidsgraad": 0.45,
            "stappen_aantal": 2,
            "cognitieve_complexiteit": "begrijpen"
        },
        "didactiek": {
            "lova": {
                "lezen": "Context lezen",
                "ordenen": "Gegevens ordenen",
                "vormen": "Breuk vormen",
                "antwoorden": "1/2"
            }
        }
    }

    # Voorbeeld item (fout: te veel stappen)
    voorbeeld_fout = {
        "id": "V_G4_M_001",
        "domein": "Verhoudingen",
        "subdomein": "Breuken",
        "groep": 4,
        "niveau": "M",
        "vraag": {
            "context": "Een pizza wordt in 8 stukken gesneden. Jan eet 3 stukken en Piet eet 2 stukken.",
            "hoofdvraag": "Hoeveel stukken blijven er over als je ze bij elkaar optelt en dan halveert?"
        },
        "antwoorden": [
            {"id": "A", "tekst": "1.5", "correct": True, "fouttype": None},
            {"id": "B", "tekst": "2", "correct": False, "fouttype": "berekening_fout"}
        ],
        "metadata": {
            "moeilijkheidsgraad": 0.75,
            "stappen_aantal": 4  # TE VEEL voor G4-M!
        },
        "didactiek": {}
    }

    validator = VerhoudingenValidator()

    print("=" * 60)
    print("VERHOUDINGEN VALIDATOR TEST")
    print("=" * 60)

    # Test correct item
    print("\n1. Validatie CORRECT item:")
    print("-" * 60)
    resultaat = validator.valideer_item(voorbeeld_correct)
    print(f"Valid: {resultaat.valid}")
    print(f"Score: {resultaat.score:.2f}")
    print(f"Errors: {len(resultaat.errors)}")
    print(f"Warnings: {len(resultaat.warnings)}")
    if resultaat.warnings:
        for w in resultaat.warnings:
            print(f"  - {w}")

    # Test fout item
    print("\n2. Validatie FOUT item:")
    print("-" * 60)
    resultaat = validator.valideer_item(voorbeeld_fout)
    print(f"Valid: {resultaat.valid}")
    print(f"Score: {resultaat.score:.2f}")
    print(f"Errors: {len(resultaat.errors)}")
    for e in resultaat.errors:
        print(f"  - ERROR: {e}")
    if resultaat.warnings:
        for w in resultaat.warnings:
            print(f"  - WARNING: {w}")

    print("\n" + "=" * 60)
    print("VALIDATIE VOLTOOID")
    print("=" * 60)


if __name__ == '__main__':
    main()
