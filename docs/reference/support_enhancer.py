#!/usr/bin/env python3
"""
SUPPORT FILE ENHANCER v1.0
Automatisch strategie-uitleg genereren voor support files

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


class StrategieGenerator:
    """Genereert pedagogisch verantwoorde strategie-uitleg per groep/niveau"""
    
    # Strategie templates per groep
    STRATEGIE_TEMPLATES = {
        # GROEP 3
        (3, 'M'): {
            'optellen': [
                "Tel de getallen bij elkaar op: {num1} en {num2}. Je kunt je vingers of blokjes gebruiken om te tellen.",
                "Begin bij {num1}, tel dan nog {num2} erbij. Zo kom je op {answer}.",
            ],
            'aftrekken': [
                "Begin bij {num1} en tel {num2} terug. Dan houd je {answer} over.",
                "Je hebt {num1}, nu haal je er {num2} af. Dat is {answer}.",
            ],
        },
        (3, 'E'): {
            'optellen_bruggetje': [
                "Gebruik het bruggetje van 10: eerst {num1} + {split1} = 10, dan nog {split2} erbij. Zo kom je op {answer}.",
                "Maak eerst 10: {num1} + {split1} = 10. Dan tel je nog {split2} erbij. Dat wordt {answer}.",
            ],
            'optellen_splitsen': [
                "Splits de {num2} in {split1} en {split2}. Eerst reken je {num1} + {split1} = {round10}, dan nog + {split2} = {answer}.",
            ],
            'aftrekken_bruggetje': [
                "Trek af via 10: {num1} - {split1} = 10, dan nog - {split2} = {answer}.",
            ],
        },
        # GROEP 4
        (4, 'M'): {
            'optellen': [
                "Tel de getallen op, eerst de eentallen dan de tientallen.",
            ],
            'aftrekken': [
                "Trek af, eerst de eentallen dan de tientallen. Let op of je moet lenen!",
            ],
            'vermenigvuldigen': [
                "Dit is de tafel van {num2}: {num1} × {num2} = {answer}. Dat is {num1} keer de {num2}.",
                "Je moet de tafel van {num1} gebruiken: {num1} × {num2} = {answer}.",
            ],
            'delen': [
                "Hoeveel keer past {num2} in {num1}? Dat is {answer} keer. Je kunt de tafel van {num2} gebruiken om dit te controleren.",
            ],
        },
        # GROEP 5
        (5, 'M'): {
            'optellen': [
                "Tel de getallen bij elkaar op. Werk van rechts naar links: eerst eentallen, dan tientallen, dan honderdtallen.",
            ],
            'aftrekken': [
                "Trek af van rechts naar links. Onthoud: als het niet kan, moet je eerst lenen!",
            ],
            'vermenigvuldigen': [
                "Dit is de tafel van {num2}: {num1} × {num2} = {answer}.",
            ],
            'staartdeling': [
                "{num1} delen door {num2} geeft {answer}. Je kunt de tafel van {num2} gebruiken om te helpen.",
            ],
        },
    }
    
    # Misconceptie patronen
    MISCONCEPTIES = {
        'tiental_vergeten': "Je vergeet dat {num1} eerst naar 10 gaat",
        'verkeerde_splitsing': "Je splitst de {num2} verkeerd ({wrong} i.p.v. {correct})",
        'plus_min_1': "Je rekent {num1} {op} {wrong} in plaats van {num2}",
        'bewerking_omgedraaid': "Je draait de bewerking om ({wrong} i.p.v. {correct})",
        'tafel_fout': "Dit is niet de tafel van {num}, maar {answer}",
        'leesfout': "Je leest waarschijnlijk {wrong} in plaats van {num}",
    }
    
    def __init__(self, groep: int, niveau: str):
        self.groep = groep
        self.niveau = niveau
        self.templates = self.STRATEGIE_TEMPLATES.get((groep, niveau), {})
    
    def analyseer_vraag(self, vraag_text: str) -> Optional[Dict[str, Any]]:
        """Analyseer de vraag en detecteer bewerking + getallen"""
        
        # NIEUW: Filter visuele elementen (emoji blokken) voordat analyseren
        vraag_clean = re.sub(r'[🟦🟧🟨🟩🟪🟫⬛⬜▪▫■□●○◆◇★☆♦♥♠♣]', '', vraag_text)
        vraag_clean = re.sub(r'[\u2500-\u257F]', '', vraag_clean)  # Box drawing
        vraag_clean = re.sub(r'\n+', ' ', vraag_clean)  # Newlines naar spaties
        vraag_clean = vraag_clean.strip()
        
        # NIEUW: Detecteer tekstuele optelling patronen
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
        
        # Detecteer expliciete optelling met +
        match = re.search(r'(\d+)\s*\+\s*(\d+)', vraag_clean)
        if match:
            num1, num2 = int(match.group(1)), int(match.group(2))
            return {
                'bewerking': 'optellen',
                'num1': num1,
                'num2': num2,
                'teken': '+',
                'answer': num1 + num2,
            }
        
        # NIEUW: Detecteer tekstuele aftrekking patronen
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
        
        # Detecteer expliciete aftrekking met -
        match = re.search(r'(\d+)\s*-\s*(\d+)', vraag_clean)
        if match:
            num1, num2 = int(match.group(1)), int(match.group(2))
            return {
                'bewerking': 'aftrekken',
                'num1': num1,
                'num2': num2,
                'teken': '-',
                'answer': num1 - num2,
            }
        
        # Detecteer vermenigvuldiging
        match = re.search(r'(\d+)\s*[×*x]\s*(\d+)', vraag_clean)
        if match:
            num1, num2 = int(match.group(1)), int(match.group(2))
            return {
                'bewerking': 'vermenigvuldigen',
                'num1': num1,
                'num2': num2,
                'teken': '×',
                'answer': num1 * num2,
            }
        
        # Detecteer deling
        match = re.search(r'(\d+)\s*[:÷]\s*(\d+)', vraag_clean)
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
        """Genereer strategie-uitleg"""
        strategie_type, extra_params = self.bepaal_strategie(analyse)
        
        # Zoek template
        templates = self.templates.get(strategie_type, [])
        if not templates:
            # Fallback naar generieke bewerking
            templates = self.templates.get(analyse['bewerking'], [])
        
        if not templates:
            # Ultieme fallback
            return f"Bereken {analyse['num1']} {analyse['teken']} {analyse['num2']} = {analyse['answer']}."
        
        # Selecteer eerste template en vul in
        template = templates[0]
        params = {**analyse, **extra_params}
        
        try:
            return template.format(**params)
        except KeyError as e:
            # Fallback als parameters missen
            return f"Bereken {analyse['num1']} {analyse['teken']} {analyse['num2']} = {analyse['answer']}."
    
    def analyseer_afleiders(self, analyse: Dict[str, Any], afleiders: List[str]) -> Dict[str, str]:
        """Genereer misconceptie-uitleg voor afleiders"""
        misconcepties = {}
        correct = analyse['answer']
        num1 = analyse['num1']
        num2 = analyse['num2']
        bewerking = analyse['bewerking']
        
        for afleider in afleiders:
            try:
                afl_num = int(afleider)
            except ValueError:
                continue
            
            # Plus/min 1 of 2
            if abs(afl_num - correct) <= 2:
                diff = afl_num - correct
                if diff > 0:
                    misconcepties[afleider] = f"Je rekent {num1} {analyse['teken']} {num2 + diff} in plaats van {num2} (tellfout)."
                else:
                    misconcepties[afleider] = f"Je rekent {num1} {analyse['teken']} {num2 + diff} in plaats van {num2} (tellfout)."
            
            # Tiental vergeten (voor optellen met tientalovergang)
            elif bewerking == 'optellen' and num1 < 20 and num2 < 10:
                if afl_num == (num1 % 10) + num2:
                    misconcepties[afleider] = f"Je vergeet dat {num1} eerst naar 10 gaat (misconceptie: tiental vergeten)."
            
            # Bewerking omgedraaid
            elif bewerking == 'aftrekken' and afl_num == num2 - num1:
                misconcepties[afleider] = f"Je draait de som om: {num2} - {num1} in plaats van {num1} - {num2}."
            
            # Tafel fout
            elif bewerking == 'vermenigvuldigen':
                # Check of het een andere tafel is
                for i in range(1, 11):
                    if num1 * i == afl_num or num2 * i == afl_num:
                        misconcepties[afleider] = f"Dit is de tafel van {i}, niet de gevraagde som."
                        break
            
            # Generic fallback
            if afleider not in misconcepties:
                misconcepties[afleider] = f"Check je berekening, het antwoord is {correct}."
        
        return misconcepties


class SupportFileEnhancer:
    """Verbetert support files met strategie-uitleg"""
    
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
        """Verbeter één support file"""
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
        
        # Initialiseer strategie generator
        generator = StrategieGenerator(groep, niveau)
        
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
            
            # Vind correct antwoord
            options = core_item.get('options', [])
            answer_data = core_item.get('answer', {})
            correct_idx = answer_data.get('correct_index', 0)
            
            correct_answer = ""
            afleiders = []
            if options:
                for idx, opt in enumerate(options):
                    text = opt.get('text') if isinstance(opt, dict) else str(opt)
                    if idx == correct_idx:
                        correct_answer = str(text)
                    else:
                        afleiders.append(str(text))
            
            # Analyseer vraag
            analyse = generator.analyseer_vraag(question_text)
            
            # DEBUG: Laat zien wat gedetecteerd is
            if analyse:
                print(f"     → Gedetecteerd: {analyse['num1']} {analyse['teken']} {analyse['num2']} = {analyse['answer']}")
            else:
                print(f"     → Geen bewerking gedetecteerd")
            
            if not analyse:
                # NIEUW: Fallback voor niet-analyseerbare vragen
                # Maak een minimale verbetering van de explanation
                oude_explanation = ""
                support_item = support_dict.get(item_id)
                if support_item:
                    oude_explanation = support_item.get('feedback', {}).get('explanation', '')
                
                # Als de oude explanation erg kort is, voeg minimale verbetering toe
                if len(oude_explanation) < 50:
                    nieuwe_explanation = (
                        f"Het juiste antwoord is: {correct_answer}. "
                        f"Lees de vraag zorgvuldig en kies het goede antwoord."
                    )
                    
                    if support_item:
                        if 'feedback' not in support_item:
                            support_item['feedback'] = {}
                        support_item['feedback']['explanation'] = nieuwe_explanation
                        print(f"  ⚡ Item {item_id}: Basis-enhancement (vraag niet analyseerbaar)")
                        enhanced_count += 1
                    else:
                        print(f"  ⚠️  Item {item_id}: Niet gevonden in support file")
                        self.stats['skipped'] += 1
                else:
                    print(f"  ⏭️  Item {item_id}: Kan vraag niet analyseren (al content aanwezig)")
                    self.stats['skipped'] += 1
                continue
            
            # Genereer strategie-uitleg
            strategie_uitleg = generator.genereer_uitleg(analyse)
            
            # Analyseer afleiders
            misconcepties = generator.analyseer_afleiders(analyse, afleiders)
            
            # Bouw volledige explanation
            misconceptie_tekst = " ".join([
                f"Afleider {afl} is fout omdat {uitleg}"
                for afl, uitleg in list(misconcepties.items())[:3]  # Max 3 afleiders
            ])
            
            nieuwe_explanation = (
                f"Het juiste antwoord is: {correct_answer}. "
                f"{strategie_uitleg} "
                f"{misconceptie_tekst}"
            ).strip()
            
            # Update support item
            support_item = support_dict.get(item_id)
            if support_item:
                oude_explanation = support_item.get('feedback', {}).get('explanation', '')
                
                # Check of er al goede content is
                if len(oude_explanation) > 50 and any(kw in oude_explanation.lower() for kw in ['bruggetje', 'splitsen', 'strategie', 'misconceptie']):
                    print(f"  ✅ Item {item_id}: Al goede uitleg aanwezig, skip")
                    self.stats['skipped'] += 1
                    continue
                
                # Update
                if 'feedback' not in support_item:
                    support_item['feedback'] = {}
                support_item['feedback']['explanation'] = nieuwe_explanation
                
                print(f"  ✨ Item {item_id}: Enhanced!")
                print(f"     {nieuwe_explanation[:80]}...")
                enhanced_count += 1
            else:
                print(f"  ⚠️  Item {item_id}: Niet gevonden in support file")
                self.stats['skipped'] += 1
        
        # Schrijf terug
        if enhanced_count > 0:
            try:
                with open(support_file, 'w', encoding='utf-8') as f:
                    json.dump(support_data, f, indent=2, ensure_ascii=False)
                print(f"\n✅ Support file bijgewerkt: {enhanced_count} items enhanced")
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
        print("🚀 SUPPORT FILE ENHANCER v1.0")
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
        print("\n🎉 Klaar!")


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
