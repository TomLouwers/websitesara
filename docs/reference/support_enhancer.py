#!/usr/bin/env python3
"""
SUPPORT FILE ENHANCER v2.0 - Teacher Edition
Genereert kindvriendelijke uitleg voor support files - zoals een echte juf/meester!

Usage:
    python support_enhancer.py <directory>
    python support_enhancer.py .  # Huidige directory
    python support_enhancer.py /path/to/exercises/
"""

import json
import re
import os
import sys
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import random


class KindvriendelijkeUitlegGenerator:
    """Genereert uitleg zoals een echte juf/meester - warm, begrijpelijk en bemoedigend"""

    # Strategie templates per groep - in natuurlijke kindertaal!
    STRATEGIE_TEMPLATES = {
        # GROEP 3
        (3, 'M'): {
            'optellen': [
                "Je moet {num1} en {num2} bij elkaar optellen. Dat kun je doen door te tellen! Begin bij {num1}, en tel dan {num2} verder: {num1}... en dan tel je {num2} erbij. Zo kom je uit op {answer}!",
                "Oké, we gaan tellen! Je hebt {num1}, en daar komt nog {num2} bij. Je kunt je vingers gebruiken om te helpen. Tel maar mee: {num1}... en dan nog {num2} verder tellen... en je komt uit op {answer}!",
                "We doen {num1} plus {num2}. Je kunt ook blokjes pakken om het te zien: pak {num1} blokjes, en leg er nog {num2} bij. Tel ze allemaal en je hebt {answer} blokjes!",
            ],
            'aftrekken': [
                "Je begint met {num1}. Nu moet je er {num2} afhalen. Stel je voor dat je {num1} snoepjes hebt, en je geeft er {num2} weg. Hoeveel houd je dan over? Precies, {answer}!",
                "Dit is aftrekken! Start bij {num1} en tel {num2} terug. Zo: {num1}... nu tel je {num2} terug... en dan houd je {answer} over.",
                "Je hebt {num1} dingetjes, en je moet er {num2} weghalen. Het is net alsof je {num1} appels hebt en er {num2} opeet. Dan blijven er {answer} appels over!",
            ],
        },
        (3, 'E'): {
            'optellen_bruggetje': [
                "Dit is een mooie truc! We gaan via het getal 10. Kijk: je hebt {num1}, en je wilt er {num2} bij doen. Eerst maken we 10: {num1} plus {split1} is 10. En dan doen we de rest erbij: 10 plus {split2} is {answer}. Slim hè?",
                "We gebruiken een bruggetje! Van {num1} naar 10 is {split1}. Dus we doen eerst {num1} plus {split1}, dat is 10. Nu hebben we nog {split2} over om erbij te doen: 10 plus {split2} geeft {answer}!",
                "Let op deze slimme manier! Eerst stappen we naar 10: {num1} plus {split1} maakt 10. Dan pakken we de rest van de {num2}, dat is nog {split2}. Dus 10 plus {split2} is {answer}. Goed zo!",
            ],
            'optellen_splitsen': [
                "We gaan de {num2} in stukjes knippen! Eerst doen we {num1} plus {split1}, dat is {round10}. En dan doen we er nog {split2} bij. {round10} plus {split2} is {answer}!",
                "Kijk, we maken de {num2} in twee stukjes: {split1} en {split2}. Eerst rekenen we {num1} plus {split1}, dat wordt {round10}. Nu doen we er {split2} bij: {round10} plus {split2} is {answer}!",
            ],
            'aftrekken_bruggetje': [
                "We trekken af via het getal 10 - dat maakt het makkelijker! Eerst gaan we van {num1} naar 10, dat is min {split1}. Dan trekken we nog {split2} af: 10 min {split2} is {answer}.",
                "Dit aftrekken doen we in stapjes via 10. Van {num1} naar 10 is {split1} eraf. Nu moeten we nog {split2} afhalen: 10 min {split2} geeft {answer}!",
            ],
        },
        # GROEP 4
        (4, 'M'): {
            'optellen': [
                "Bij optellen beginnen we altijd rechts! Eerst tel je de eentallen bij elkaar op, dan de tientallen. Reken maar mee: de eentallen van {num1} en {num2} optellen, en de tientallen erbij. Zo kom je op {answer}!",
                "We tellen {num1} en {num2} bij elkaar op. Begin rechts bij de eentallen, tel die op. Dan de tientallen. Let op of je van de eentallen een tientje overhoudt! Het antwoord is {answer}.",
                "Oké, {num1} plus {num2}. Zet ze mooi onder elkaar, eentallen onder eentallen. Tel eerst rechts de eentallen op, dan links de tientallen. Je krijgt {answer}!",
            ],
            'aftrekken': [
                "Bij aftrekken werk je ook van rechts naar links. Trek eerst de eentallen af, dan de tientallen. Let goed op: als het niet kan, moet je een tientje lenen! Het antwoord is {answer}.",
                "{num1} min {num2}. Zet ze onder elkaar. Begin rechts: kun je de eentallen aftrekken? En dan de tientallen. Soms moet je lenen, let daar op! Je komt uit op {answer}.",
                "We gaan aftrekken! {num1} min {num2}. Werk van rechts naar links: eerst eentallen, dan tientallen. Als de onderkant groter is, moet je lenen bij de buren! Het wordt {answer}.",
            ],
            'vermenigvuldigen': [
                "Dit is de tafel van {num2}! Je moet {num1} keer de {num2} doen. Dat is {num1} × {num2} = {answer}. Ken je je tafels al goed? Dan weet je dit uit je hoofd!",
                "Kijk, we vermenigvuldigen! {num1} × {num2} betekent: {num1} keer de {num2}. Je kunt het ook zien als {num1} groepjes van {num2}. Dat wordt {answer}!",
                "We doen de tafel! {num1} × {num2} is {answer}. Tip: als je de tafels kent, gaat dit super snel. Anders kun je het ook optellen: {num2} + {num2} + {num2}... {num1} keer!",
            ],
            'delen': [
                "Nu gaan we delen! {num1} gedeeld door {num2}. Dat betekent: hoeveel keer past {num2} in {num1}? Tel maar: 1 keer {num2}, 2 keer {num2}... Het past {answer} keer!",
                "Delen is het omgekeerde van vermenigvuldigen. {num1} : {num2} = {answer}. Je kunt het checken met de tafel van {num2}: {answer} × {num2} = {num1}. Klopt!",
                "{num1} verdelen in groepjes van {num2}. Hoeveel groepjes kun je maken? Precies, {answer} groepjes! Je kunt ook denken: {answer} keer {num2} is {num1}.",
            ],
        },
        (4, 'E'): {
            'optellen': [
                "Bij grotere getallen werk je kolomsgewijs. Zet {num1} en {num2} netjes onder elkaar. Tel op van rechts naar links: eerst eentallen, dan tientallen, dan honderdtallen. Onthoud goed wat je moet doorgeven! Het antwoord is {answer}.",
                "Optellen tot 1000: {num1} + {num2}. Werk systematisch van rechts naar links. Als de eentallen samen meer dan 10 zijn, geef je 1 door naar de tientallen. Zo kom je op {answer}!",
            ],
            'aftrekken': [
                "Aftrekken met grotere getallen: {num1} − {num2} = {answer}. Zet ze onder elkaar en werk van rechts naar links. Als je moet lenen, haal je 1 van de positie links en maak je er 10 bij de huidige positie.",
                "Trek kolomsgewijs af: {num1} min {num2}. Let goed op bij het lenen! Als je 5 − 8 moet doen, leen je 1 van de tientallen. Dan wordt het 15 − 8. Het antwoord is {answer}.",
            ],
            'vermenigvuldigen': [
                "Vermenigvuldigen: {num1} × {num2} = {answer}. Als je de tafels goed kent, kun je dit snel uitrekenen. Anders kun je het doen met kolomsgewijs vermenigvuldigen.",
            ],
            'delen': [
                "Delen: {num1} : {num2} = {answer}. Denk aan de tafels: hoeveel keer {num2} heb je nodig voor {num1}? Controleer je antwoord door te vermenigvuldigen: {answer} × {num2} = {num1}.",
            ],
        },
        # GROEP 5
        (5, 'M'): {
            'optellen': [
                "We tellen {num1} en {num2} bij elkaar op. Zet de getallen mooi onder elkaar: eentallen onder eentallen, tientallen onder tientallen, honderdtallen onder honderdtallen. Tel ze op van rechts naar links. Vergeet niet om te onthouden! Het antwoord is {answer}.",
                "Optellen met grote getallen! Begin altijd rechts. Tel de eentallen, vergeet niet wat je onthoudt. Dan de tientallen, dan de honderdtallen. Zo kom je netjes op {answer}!",
            ],
            'aftrekken': [
                "We trekken {num2} af van {num1}. Zet ze onder elkaar, en werk van rechts naar links. Als je een cijfer niet kunt aftrekken, moet je lenen bij je linkerbuur! Het antwoord is {answer}.",
                "Aftrekken met grotere getallen: {num1} − {num2}. Begin rechts bij de eentallen. Kun je aftrekken? Zo niet, leen dan een tientje. Dan de tientallen, dan de honderdtallen. Je krijgt {answer}!",
            ],
            'vermenigvuldigen': [
                "Vermenigvuldigen: {num1} × {num2} = {answer}. Dit is de tafel van {num2}! Als je deze tafel goed kent, weet je het antwoord meteen. Anders kun je het in stapjes uitrekenen.",
                "{num1} keer {num2} is {answer}. Gebruik de tafel van {num2} die je uit je hoofd kent, of reken het uit met kolomsgewijs vermenigvuldigen.",
            ],
            'staartdeling': [
                "We gaan staartdelen! {num1} : {num2} = {answer}. Hoeveel keer past {num2} in {num1}? Dat is {answer} keer. Je kunt het controleren: {answer} × {num2} = {num1}!",
                "Staartdeling: {num1} gedeeld door {num2}. Denk aan de tafel van {num2}. Hoeveel keer {num2} heb je nodig om {num1} te maken? {answer} keer!",
            ],
        },
        (5, 'E'): {
            'optellen': [
                "Bij zeer grote getallen werk je kolomsgewijs. Zet {num1} en {num2} netjes onder elkaar met alle cijfers op de juiste plaats. Begin rechts en werk naar links. Het antwoord is {answer}.",
                "Optellen tot 100.000: zet de getallen onder elkaar en let goed op de plaatswaarde. Eentallen, tientallen, honderdtallen, duizendtallen, tienduizendtallen - allemaal netjes onder elkaar. Reken van rechts naar links: {num1} + {num2} = {answer}.",
            ],
            'aftrekken': [
                "Aftrekken met grote getallen: {num1} − {num2} = {answer}. Zet ze kolomsgewijs onder elkaar. Werk systematisch van rechts naar links en leen waar nodig.",
                "Trek af: {num1} min {num2}. Let goed op de plaatswaarde van elk cijfer. Begin rechts en werk naar links, leen bij je linkerbuur als het nodig is. Het antwoord is {answer}.",
            ],
            'vermenigvuldigen': [
                "Vermenigvuldigen: {num1} × {num2} = {answer}. Gebruik kolomsgewijs vermenigvuldigen of splits het getal in handige delen.",
            ],
            'delen': [
                "Delen: {num1} : {num2} = {answer}. Gebruik staartdeling: hoeveel keer past {num2} in elk deel van {num1}?",
            ],
        },
        # GROEP 6
        (6, 'M'): {
            'optellen': [
                "Rekenen met getallen in de miljoenen: {num1} + {num2} = {answer}. Zet de getallen kolomsgewijs onder elkaar, let goed op de plaatswaarde. Werk systematisch van rechts naar links.",
                "Optellen: {num1} + {num2}. Controleer eerst hoeveel cijfers elk getal heeft. Zet ze netjes onder elkaar en tel op. Vergeet niet om door te geven naar de volgende kolom! Het antwoord is {answer}.",
            ],
            'aftrekken': [
                "Aftrekken: {num1} − {num2} = {answer}. Zet de getallen onder elkaar, let op de plaatswaarde van miljoenen, honderdduizenden, tienduizenden, etc. Trek af van rechts naar links.",
                "Bij grote getallen is het extra belangrijk om netjes te werken. Zet {num1} en {num2} onder elkaar, en trek kolomsgewijs af. Leen indien nodig. Het antwoord is {answer}.",
            ],
            'vermenigvuldigen': [
                "Vermenigvuldigen: {num1} × {num2} = {answer}. Bij grote getallen kun je vaak handig werken met ronde getallen of het getal splitsen.",
            ],
            'delen': [
                "Delen: {num1} : {num2} = {answer}. Gebruik staartdeling en werk systematisch. Schat eerst ongeveer wat het antwoord zou kunnen zijn.",
            ],
        },
        (6, 'E'): {
            'optellen': [
                "Optellen tot 2 miljoen: {num1} + {num2} = {answer}. Werk kolomsgewijs, let op alle plaatswaarden. Een goede tip: schat eerst het antwoord globaal, dan kun je checken of je uitkomst logisch is.",
            ],
            'aftrekken': [
                "Aftrekken: {num1} − {num2} = {answer}. Bij hele grote getallen is het verstandig om eerst te schatten. Werk dan kolomsgewijs, let goed op bij het lenen.",
            ],
            'vermenigvuldigen': [
                "Vermenigvuldigen: {num1} × {num2} = {answer}. Gebruik een slimme strategie: verdeel het probleem in kleinere stukken of werk met afronding.",
            ],
            'delen': [
                "Delen: {num1} : {num2} = {answer}. Schat eerst globaal, gebruik dan staartdeling. Controleer je antwoord door te vermenigvuldigen.",
            ],
        },
        # GROEP 7
        (7, 'M'): {
            'optellen': [
                "Rekenen met grote getallen (tot 5 miljoen): {num1} + {num2} = {answer}. Let goed op bij negatieve getallen! Een negatief getal optellen is hetzelfde als aftrekken.",
                "Optellen: {num1} + {num2} = {answer}. Bij hele grote getallen is schatten eerst een goede strategie. Werk daarna kolomsgewijs uit en controleer of je schatting klopt.",
            ],
            'aftrekken': [
                "Aftrekken: {num1} − {num2} = {answer}. Let op: als je een negatief getal aftrekt, tel je eigenlijk op! Bijvoorbeeld: 5 − (−3) = 5 + 3 = 8.",
                "Bij aftrekken met negatieve getallen: twee negatieve tekens naast elkaar worden een plus! {num1} − {num2} = {answer}.",
            ],
            'vermenigvuldigen': [
                "Vermenigvuldigen: {num1} × {num2} = {answer}. Let op de tekens: negatief × positief = negatief, negatief × negatief = positief.",
            ],
            'delen': [
                "Delen: {num1} : {num2} = {answer}. Bij negatieve getallen: let op het teken van je antwoord. Negatief gedeeld door positief geeft negatief.",
            ],
        },
        (7, 'E'): {
            'optellen': [
                "Rekenen tot 5 miljoen: {num1} + {num2} = {answer}. Werk systematisch, let goed op de tekens bij negatieve getallen.",
            ],
            'aftrekken': [
                "Aftrekken: {num1} − {num2} = {answer}. Bij negatieve getallen: min en min wordt plus! Werk de bewerking stap voor stap uit.",
            ],
            'vermenigvuldigen': [
                "Vermenigvuldigen: {num1} × {num2} = {answer}. Onthoud de tekenregels: + × + = +, − × − = +, + × − = −.",
            ],
            'delen': [
                "Delen: {num1} : {num2} = {answer}. Pas de tekenregels toe: twee gelijke tekens geeft +, twee verschillende tekens geeft −.",
            ],
        },
        # GROEP 8
        (8, 'M'): {
            'optellen': [
                "Rekenen met zeer grote getallen (tot 18 miljoen): {num1} + {num2} = {answer}. Schat eerst globaal, werk dan precies uit. Let goed op de tekens!",
            ],
            'aftrekken': [
                "Aftrekken: {num1} − {num2} = {answer}. Bij deze grote getallen is het belangrijk om netjes te werken. Schat eerst, reken dan precies uit.",
            ],
            'vermenigvuldigen': [
                "Vermenigvuldigen: {num1} × {num2} = {answer}. Werk systematisch en let op de tekenregels bij negatieve getallen.",
            ],
            'delen': [
                "Delen: {num1} : {num2} = {answer}. Gebruik efficiënte strategieën en controleer je antwoord door te vermenigvuldigen.",
            ],
        },
        (8, 'E'): {
            'optellen': [
                "Optellen tot 18 miljoen: {num1} + {num2} = {answer}. Bij deze getallen is een goede strategie essentieel. Schat globaal, werk netjes uit, controleer je antwoord.",
            ],
            'aftrekken': [
                "Aftrekken: {num1} − {num2} = {answer}. Werk systematisch, let op negatieve getallen en controleer of je antwoord logisch is.",
            ],
            'vermenigvuldigen': [
                "Vermenigvuldigen: {num1} × {num2} = {answer}. Gebruik slimme rekenstrategieën en let goed op de tekens.",
            ],
            'delen': [
                "Delen: {num1} : {num2} = {answer}. Gebruik staartdeling of splits het probleem in kleinere stappen. Controleer je antwoord!",
            ],
        },
    }

    def __init__(self, groep: int, niveau: str):
        self.groep = groep
        self.niveau = niveau
        self.templates = self.STRATEGIE_TEMPLATES.get((groep, niveau), {})

    def analyseer_vraag(self, vraag_text: str) -> Optional[Dict[str, Any]]:
        """Analyseer de vraag en detecteer bewerking + getallen"""

        # Filter visuele elementen (emoji blokken)
        vraag_clean = re.sub(r'[🟦🟧🟨🟩🟪🟫⬛⬜▪▫■□●○◆◇★☆♦♥♠♣]', '', vraag_text)
        vraag_clean = re.sub(r'[\u2500-\u257F]', '', vraag_clean)  # Box drawing
        vraag_clean = re.sub(r'\n+', ' ', vraag_clean)  # Newlines naar spaties
        vraag_clean = vraag_clean.strip()

        # Detecteer tekstuele optelling patronen
        # "9 snoepjes, 4 erbij" of "8 appels, 5 erbij"
        text_patterns_plus = [
            r'(\d+)[^,\d]*,?\s*(\d+)\s*(?:erbij|er\s*bij)',
            r'(\d+)[^,\d]*\s+(?:krijgt?|kreeg)\s+(?:er\s*)?(\d+)\s+(?:bij|erbij)',
            r'(\d+)[^,\d]*\s+en\s+(?:nog\s*)?(\d+)',
        ]

        for pattern in text_patterns_plus:
            match = re.search(pattern, vraag_clean.lower())
            if match:
                num1, num2 = int(match.group(1)), int(match.group(2))
                return {
                    'bewerking': 'optellen',
                    'num1': num1,
                    'num2': num2,
                    'teken': '+',
                    'answer': num1 + num2,
                }

        # Detecteer expliciete optelling met + (inclusief negatieve getallen voor groep 7-8)
        match = re.search(r'(-?\d+)\s*\+\s*(-?\d+)', vraag_clean)
        if match:
            num1, num2 = int(match.group(1)), int(match.group(2))
            return {
                'bewerking': 'optellen',
                'num1': num1,
                'num2': num2,
                'teken': '+',
                'answer': num1 + num2,
            }

        # Detecteer tekstuele aftrekking patronen
        # "12 appels, 4 kwijt" of "10 snoepjes, 3 weggegeven"
        text_patterns_minus = [
            r'(\d+)[^,\d]*,?\s*(\d+)\s*(?:kwijt|weg|weggegeven|afgegeven|verloren)',
            r'(\d+)[^,\d]*\s+(?:geeft?|gaf)\s+(\d+)\s+(?:weg|af)',
            r'(\d+)[^,\d]*\s+(?:verliest?|verloor)\s+(\d+)',
        ]

        for pattern in text_patterns_minus:
            match = re.search(pattern, vraag_clean.lower())
            if match:
                num1, num2 = int(match.group(1)), int(match.group(2))
                return {
                    'bewerking': 'aftrekken',
                    'num1': num1,
                    'num2': num2,
                    'teken': '-',
                    'answer': num1 - num2,
                }

        # Detecteer expliciete aftrekking met - (inclusief negatieve getallen)
        match = re.search(r'(-?\d+)\s*-\s*(-?\d+)', vraag_clean)
        if match:
            num1, num2 = int(match.group(1)), int(match.group(2))
            return {
                'bewerking': 'aftrekken',
                'num1': num1,
                'num2': num2,
                'teken': '-',
                'answer': num1 - num2,
            }

        # Detecteer vermenigvuldiging (inclusief negatieve getallen)
        match = re.search(r'(-?\d+)\s*[×*x]\s*(-?\d+)', vraag_clean)
        if match:
            num1, num2 = int(match.group(1)), int(match.group(2))
            return {
                'bewerking': 'vermenigvuldigen',
                'num1': num1,
                'num2': num2,
                'teken': '×',
                'answer': num1 * num2,
            }

        # Detecteer deling (inclusief negatieve getallen)
        match = re.search(r'(-?\d+)\s*[:÷]\s*(-?\d+)', vraag_clean)
        if match:
            num1, num2 = int(match.group(1)), int(match.group(2))
            if num2 != 0:
                return {
                    'bewerking': 'delen',
                    'num1': num1,
                    'num2': num2,
                    'teken': ':',
                    'answer': num1 // num2,
                }

        return None

    def bepaal_strategie(self, analyse: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Bepaal de beste strategie voor deze som"""
        bewerking = analyse['bewerking']
        num1 = analyse['num1']
        num2 = analyse['num2']
        answer = analyse['answer']

        # GROEP 3-E: Bruggetje vs Splitsen
        if self.groep == 3 and self.niveau == 'E':
            if bewerking == 'optellen':
                # Check of bruggetje van 10 logisch is
                eental1 = num1 % 10
                eental2 = num2 % 10

                if eental1 + eental2 >= 10 and num1 < 20:
                    # Bruggetje van 10
                    split1 = 10 - num1  # Hoeveel naar 10
                    split2 = num2 - split1  # Rest
                    return 'optellen_bruggetje', {
                        'split1': split1,
                        'split2': split2,
                    }
                elif num1 < 10 and num2 >= 5:
                    # Splitsen via 10
                    split1 = 10 - num1
                    split2 = num2 - split1
                    return 'optellen_splitsen', {
                        'split1': split1,
                        'split2': split2,
                        'round10': 10,
                    }

        # Default: gewoon de bewerking
        return bewerking, {}

    def genereer_uitleg(self, analyse: Dict[str, Any]) -> str:
        """Genereer strategie-uitleg in kindvriendelijke taal"""
        strategie_type, extra_params = self.bepaal_strategie(analyse)

        # Zoek template
        templates = self.templates.get(strategie_type, [])
        if not templates:
            # Fallback naar generieke bewerking
            templates = self.templates.get(analyse['bewerking'], [])

        if not templates:
            # Ultieme fallback - maar ook kindvriendelijk!
            num1 = analyse['num1']
            num2 = analyse['num2']
            answer = analyse['answer']
            teken = analyse['teken']
            return f"We rekenen {num1} {teken} {num2} uit. Het antwoord is {answer}!"

        # Selecteer random template voor variatie!
        template = random.choice(templates)
        params = {**analyse, **extra_params}

        try:
            return template.format(**params)
        except KeyError as e:
            # Fallback als parameters missen
            return f"We rekenen {analyse['num1']} {analyse['teken']} {analyse['num2']} uit. Het antwoord is {analyse['answer']}!"

    def leg_fout_antwoord_uit(self, analyse: Dict[str, Any], fout_antwoord: str) -> str:
        """
        Leg uit waarom een fout antwoord verleidelijk is, maar niet klopt.
        Gebruik natuurlijke kindertaal - geen technische termen!
        """
        try:
            fout_num = int(fout_antwoord)
        except ValueError:
            return f"Het antwoord {fout_antwoord} klopt niet helemaal."

        correct = analyse['answer']
        num1 = analyse['num1']
        num2 = analyse['num2']
        bewerking = analyse['bewerking']
        teken = analyse['teken']

        # Verschil tussen fout en goed
        verschil = abs(fout_num - correct)

        # TELFOUTEN (off-by-one, off-by-two)
        if verschil <= 2:
            if fout_num > correct:
                return f"Let op! Je hebt {fout_num} gerekend, maar dat is net iets te veel. Het goede antwoord is {correct}. Misschien ben je een keer te ver geteld?"
            else:
                return f"Bijna goed! Je hebt {fout_num}, maar het moet {correct} zijn. Je bent een stapje te weinig verder gegaan."

        # TIENTAL VERGETEN (alleen bij optellen in groep 3)
        if bewerking == 'optellen' and self.groep == 3:
            if num1 < 20 and num2 < 10:
                # Check of ze alleen de eentallen hebben opgeteld
                if fout_num == (num1 % 10) + num2:
                    return f"Ah, ik snap wat er gebeurt! Je hebt {num1 % 10} + {num2} = {fout_num} gedaan. Maar {num1} is niet {num1 % 10}, het is {num1}! Er zit ook nog een tientje in. Als je het goed doet, wordt het {correct}."

        # SOM OMGEDRAAID
        if bewerking == 'aftrekken' and fout_num == num2 - num1:
            return f"Oeps! Je hebt de som omgedraaid. Je hebt {num2} - {num1} = {fout_num} gedaan, maar het moet {num1} - {num2} = {correct} zijn. Let goed op welk getal vooraan staat!"

        # VERKEERDE TAFEL
        if bewerking == 'vermenigvuldigen':
            # Zoek welke tafel dit zou kunnen zijn
            for i in range(2, 11):
                if num1 * i == fout_num:
                    return f"Je hebt de tafel van {i} gebruikt en uitkomt op {fout_num}. Maar we moeten de tafel van {num2} gebruiken! {num1} × {num2} = {correct}."
                if num2 * i == fout_num:
                    return f"Je hebt de tafel van {i} gebruikt en uitkomt op {fout_num}. Maar we moeten de tafel van {num1} gebruiken! {num1} × {num2} = {correct}."

        # VERKEERDE BEWERKING GEBRUIKT
        # Check of ze plus hebben gedaan in plaats van min
        if bewerking == 'aftrekken' and fout_num == num1 + num2:
            return f"Let op het minteken! Je hebt opgeteld ({num1} + {num2} = {fout_num}), maar het is een min-som. {num1} - {num2} = {correct}."

        # Check of ze min hebben gedaan in plaats van plus
        if bewerking == 'optellen' and fout_num == abs(num1 - num2):
            return f"Kijk goed naar het teken! Je hebt afgetrokken, maar het is een plus-som. {num1} + {num2} = {correct}."

        # REKENFOUTEN BIJ LENEN (groep 4 en hoger)
        if self.groep >= 4 and bewerking == 'aftrekken':
            # Mogelijk vergeten te lenen
            if fout_num < correct and fout_num > 0:
                return f"Hmm, {fout_num} is niet helemaal goed. Het lijkt erop dat je misschien vergeten bent te lenen bij het aftrekken. Check je som nog eens goed! Het goede antwoord is {correct}."

        # NEGATIEVE GETALLEN (groep 7-8)
        if self.groep >= 7:
            # Fout met tekens bij negatieve getallen
            # Bijvoorbeeld: -5 + 3 = 8 (had -2 moeten zijn)
            if (num1 < 0 or num2 < 0) and fout_num == abs(num1) + abs(num2):
                return f"Let op de mintekens! Als een getal negatief is, moet je daar rekening mee houden. Het goede antwoord is {correct}, niet {fout_num}."

            # Fout bij dubbel minteken: -5 - (-3) moet -2 zijn, niet -8
            if bewerking == 'aftrekken' and num2 < 0 and fout_num == num1 - abs(num2):
                return f"Vergeet niet: min en min wordt plus! Je hebt {num1} − ({num2}), dus twee mintekens naast elkaar. Dat wordt: {num1} + {abs(num2)} = {correct}."

            # Teken vergeten bij vermenigvuldigen/delen
            if bewerking == 'vermenigvuldigen' and fout_num == abs(correct):
                return f"Je hebt de berekening goed gedaan, maar het teken vergeten! Negatief × positief = negatief (of andersom). Het antwoord is {correct}, niet {fout_num}."

        # ALGEMENE REKENFOUTEN
        if verschil <= 10:
            return f"Je antwoord {fout_num} is bijna goed, maar niet helemaal. Reken de som nog een keer rustig na: {num1} {teken} {num2} = {correct}."

        # GROTE AFWIJKING - maar wel bemoedigend!
        if verschil < 100:
            return f"Het antwoord {fout_num} klopt niet. Kijk nog eens goed naar de som en reken het stap voor stap uit. Het goede antwoord is {correct}."
        else:
            return f"Het antwoord {fout_num} is helaas niet juist. Het goede antwoord is {correct}. Reken de som nog eens rustig na!"

    def bouw_volledige_uitleg(self, analyse: Dict[str, Any], foute_antwoorden: List[str]) -> str:
        """
        Bouw een complete uitleg zoals een juf/meester zou doen.
        Warm, bemoedigend en helder!
        """
        correct = analyse['answer']

        # 1. Start met het goede antwoord (positief!)
        uitleg_delen = [f"Het goede antwoord is {correct}!"]

        # 2. Leg de strategie uit
        strategie_uitleg = self.genereer_uitleg(analyse)
        uitleg_delen.append(strategie_uitleg)

        # 3. Als er foute antwoorden zijn, leg die uit (max 2 voor leesbaarheid)
        if foute_antwoorden:
            # Sorteer foute antwoorden op "hoe dicht bij het goede antwoord"
            # Want die zijn het belangrijkst om uit te leggen
            try:
                foute_sorted = sorted(
                    foute_antwoorden[:3],  # Max 3
                    key=lambda x: abs(int(x) - correct) if x.isdigit() else 999
                )
            except:
                foute_sorted = foute_antwoorden[:2]

            # Voeg uitleg toe voor de meest relevante foute antwoorden
            for i, fout in enumerate(foute_sorted[:2]):  # Max 2 foute antwoorden uitleggen
                uitleg_fout = self.leg_fout_antwoord_uit(analyse, fout)

                # Voeg een natuurlijke overgang toe
                if i == 0:
                    uitleg_delen.append(uitleg_fout)
                else:
                    uitleg_delen.append(uitleg_fout)

        # 4. Sluit af met bemoediging
        afsluiters = [
            "Goed gedaan!",
            "Snap je het?",
            "Nu snap je het vast!",
            "Probeer het zelf ook eens!",
        ]

        # Alleen afsluiter toevoegen als de uitleg niet te lang is
        if sum(len(deel) for deel in uitleg_delen) < 300:
            uitleg_delen.append(random.choice(afsluiters))

        # Voeg samen met natuurlijke overgangen
        return " ".join(uitleg_delen)


class SupportFileEnhancer:
    """Verbetert support files met kindvriendelijke uitleg"""

    def __init__(self, directory: str, backup: bool = True):
        self.directory = Path(directory)
        self.backup = backup
        self.stats = {
            'processed': 0,
            'enhanced': 0,
            'skipped': 0,
            'errors': 0,
        }

    def vind_file_paren(self) -> List[Tuple[Path, Path]]:
        """Vind alle *_core.json + *_support.json paren"""
        paren = []

        for core_file in self.directory.glob('*_core.json'):
            support_file = core_file.parent / core_file.name.replace('_core.json', '_support.json')
            if support_file.exists():
                paren.append((core_file, support_file))

        return paren

    def maak_backup(self, filepath: Path):
        """Maak backup van bestand"""
        if not self.backup:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = filepath.parent / f"{filepath.stem}_backup_{timestamp}{filepath.suffix}"
        shutil.copy2(filepath, backup_file)
        print(f"  💾 Backup: {backup_file.name}")

    def enhance_support_file(self, core_file: Path, support_file: Path):
        """Verbeter één support file met kindvriendelijke uitleg"""
        print(f"\n{'='*70}")
        print(f"📝 Bewerk: {support_file.name}")
        print(f"{'='*70}")

        # Laad files
        try:
            with open(core_file, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            with open(support_file, 'r', encoding='utf-8') as f:
                support_data = json.load(f)
        except Exception as e:
            print(f"❌ Fout bij laden: {e}")
            self.stats['errors'] += 1
            return

        # Extract metadata
        meta = core_data.get('metadata', {})
        groep = meta.get('grade', 3)
        niveau = meta.get('level', 'M')
        if isinstance(niveau, str):
            niveau = niveau[0].upper()

        print(f"📊 Groep {groep}-{niveau}")

        # Maak backup
        self.maak_backup(support_file)

        # Initialiseer de kindvriendelijke uitleg generator
        generator = KindvriendelijkeUitlegGenerator(groep, niveau)

        # Verwerk items
        core_items = core_data.get('items', [])
        support_items = support_data.get('items', [])

        # Maak dictionary van support items
        support_dict = {item.get('item_id'): item for item in support_items}

        enhanced_count = 0

        for core_item in core_items:
            item_id = core_item.get('id')
            question_text = core_item.get('question', {}).get('text', '')

            # DEBUG: Print vraag
            vraag_preview = question_text[:60].replace('\n', ' ') + ('...' if len(question_text) > 60 else '')
            print(f"\n  📝 Item {item_id}: {vraag_preview}")

            # Vind correct antwoord en foute antwoorden
            options = core_item.get('options', [])
            answer_data = core_item.get('answer', {})
            correct_idx = answer_data.get('correct_index', 0)

            correct_answer = ""
            foute_antwoorden = []
            if options:
                for idx, opt in enumerate(options):
                    text = opt.get('text') if isinstance(opt, dict) else str(opt)
                    if idx == correct_idx:
                        correct_answer = str(text)
                    else:
                        foute_antwoorden.append(str(text))

            # Analyseer vraag
            analyse = generator.analyseer_vraag(question_text)

            # DEBUG: Laat zien wat gedetecteerd is
            if analyse:
                print(f"     → Gedetecteerd: {analyse['num1']} {analyse['teken']} {analyse['num2']} = {analyse['answer']}")
            else:
                print(f"     → Geen bewerking gedetecteerd")

            # Als we de vraag niet kunnen analyseren, maak dan een basis-uitleg
            if not analyse:
                support_item = support_dict.get(item_id)
                if support_item:
                    oude_explanation = support_item.get('feedback', {}).get('explanation', '')

                    # Alleen verbeteren als er nog geen goede uitleg is
                    if len(oude_explanation) < 50:
                        nieuwe_explanation = (
                            f"Het goede antwoord is {correct_answer}. "
                            f"Kijk goed naar de vraag en denk rustig na over welk antwoord het beste past!"
                        )

                        if 'feedback' not in support_item:
                            support_item['feedback'] = {}
                        support_item['feedback']['explanation'] = nieuwe_explanation
                        print(f"  ⚡ Item {item_id}: Basis uitleg toegevoegd")
                        enhanced_count += 1
                    else:
                        print(f"  ⏭️  Item {item_id}: Al goede uitleg aanwezig")
                        self.stats['skipped'] += 1
                else:
                    print(f"  ⚠️  Item {item_id}: Niet gevonden in support file")
                    self.stats['skipped'] += 1
                continue

            # Bouw de volledige kindvriendelijke uitleg!
            nieuwe_explanation = generator.bouw_volledige_uitleg(analyse, foute_antwoorden)

            # Update support item
            support_item = support_dict.get(item_id)
            if support_item:
                oude_explanation = support_item.get('feedback', {}).get('explanation', '')

                # Check of er al goede kindvriendelijke content is
                # We kijken of de uitleg al lang genoeg is EN natuurlijk klinkt
                if len(oude_explanation) > 100 and any(
                    woord in oude_explanation.lower()
                    for woord in ['kijk', 'let op', 'snap je', 'goed zo', 'probeer', 'kun je', 'bijna']
                ):
                    print(f"  ✅ Item {item_id}: Al kindvriendelijke uitleg aanwezig")
                    self.stats['skipped'] += 1
                    continue

                # Update met nieuwe kindvriendelijke uitleg!
                if 'feedback' not in support_item:
                    support_item['feedback'] = {}
                support_item['feedback']['explanation'] = nieuwe_explanation

                print(f"  ✨ Item {item_id}: Kindvriendelijke uitleg toegevoegd!")
                print(f"     {nieuwe_explanation[:100]}...")
                enhanced_count += 1
            else:
                print(f"  ⚠️  Item {item_id}: Niet gevonden in support file")
                self.stats['skipped'] += 1

        # Schrijf terug
        if enhanced_count > 0:
            try:
                with open(support_file, 'w', encoding='utf-8') as f:
                    json.dump(support_data, f, indent=2, ensure_ascii=False)
                print(f"\n✅ Support file bijgewerkt: {enhanced_count} items verrijkt met kindvriendelijke uitleg!")
                self.stats['enhanced'] += enhanced_count
            except Exception as e:
                print(f"❌ Fout bij schrijven: {e}")
                self.stats['errors'] += 1
        else:
            print(f"\nℹ️  Geen items enhanced (al compleet of niet analyseerbaar)")

        self.stats['processed'] += 1

    def run(self):
        """Verwerk alle bestanden"""
        print("\n" + "="*70)
        print("🚀 SUPPORT FILE ENHANCER v2.0 - Teacher Edition!")
        print("   Met kindvriendelijke uitleg, zoals een echte juf/meester!")
        print("="*70)
        print(f"📁 Directory: {self.directory}")
        print(f"💾 Backup: {'Ja' if self.backup else 'Nee'}")

        # Vind paren
        paren = self.vind_file_paren()
        print(f"\n📊 Gevonden: {len(paren)} core/support paren")

        if not paren:
            print("\n⚠️  Geen *_core.json + *_support.json paren gevonden!")
            return

        # Bevestiging
        response = input("\n🤔 Doorgaan met enhancen? (y/n): ")
        if response.lower() not in ['y', 'yes', 'ja', 'j']:
            print("❌ Geannuleerd")
            return

        # Verwerk elk paar
        for core_file, support_file in paren:
            self.enhance_support_file(core_file, support_file)

        # Stats
        print("\n" + "="*70)
        print("📊 SAMENVATTING")
        print("="*70)
        print(f"✅ Verwerkt: {self.stats['processed']} files")
        print(f"✨ Enhanced: {self.stats['enhanced']} items")
        print(f"⏭️  Geskipt: {self.stats['skipped']} items")
        print(f"❌ Errors: {self.stats['errors']}")
        print("\n🎉 Klaar! De uitleg is nu veel kindvriendelijker!")


def main():
    if len(sys.argv) < 2:
        print("Usage: python support_enhancer.py <directory>")
        print("\nVoorbeeld:")
        print("  python support_enhancer.py .")
        print("  python support_enhancer.py /pad/naar/oefeningen/")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"❌ Directory niet gevonden: {directory}")
        sys.exit(1)

    enhancer = SupportFileEnhancer(directory, backup=True)
    enhancer.run()


if __name__ == "__main__":
    main()
