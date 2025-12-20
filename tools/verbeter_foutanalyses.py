#!/usr/bin/env python3
"""
Script om foutanalyses te verbeteren in verhaaltjessommen - Template.json
Voegt diagnostische uitleg en reflectievragen toe waar deze ontbreken.
"""

import json

def verbeter_foutanalyses():
    # Laad de template
    with open('verhaaltjessommen - Template.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Verbeteringen per ID
    verbeteringen = {
        6: {  # Zwembad vullen - Optellen debiet
            0: {  # Vraag 1
                0: "Je hebt waarschijnlijk 240 - 180 = 60 berekend (aftrekken in plaats van optellen). Als beide kranen TEGELIJK open staan, moet je de hoeveelheden OPTELLEN: 240 + 180 = ?\n\n🤔 **Reflectievraag:** Als er 240 liter uit kraan A komt en 180 liter uit kraan B, hoeveel liter komt er dan in totaal in het zwembad?",
                # Optie 1 is correct
                2: "Je hebt alleen kraan A genomen (240 L/min) en kraan B vergeten! De vraag zegt 'beide kranen tegelijk'. Je moet beide debietsnelheden optellen: 240 + 180 = ?\n\n🤔 **Reflectievraag:** Hoeveel kranen staan er open volgens de vraag?",
                3: "Je hebt waarschijnlijk 240 × 2 = 480 berekend (verdubbeld), maar kraan B stroomt NIET even snel als kraan A! Kraan B = 180 L/min. Je moet OPTELLEN, niet verdubbelen: 240 + 180 = ?\n\n🤔 **Reflectievraag:** Zijn beide kranen even snel, of hebben ze verschillende snelheden?"
            },
            1: {  # Vraag 2
                0: "Je hebt een rekenfout gemaakt. Controleer je deling: 84.000 ÷ 420 = ? (niet 420). Let op dat je de juiste deler gebruikt (het antwoord uit vraag 1).\n\n🤔 **Reflectievraag:** Hoeveel liter per minuut stroomt er in het zwembad volgens vraag 1?",
                1: "Je hebt waarschijnlijk 84.000 ÷ 240 = 350 gerekend (alleen kraan A). Maar beide kranen staan open! Gebruik het juiste debiet uit vraag 1: 84.000 ÷ 420 = ?\n\n🤔 **Reflectievraag:** Heb je het antwoord uit vraag 1 (420 L/min) gebruikt voor deze berekening?",
                # Optie 2 is correct
                3: "Controleer je berekening. Je moet de totale inhoud (84.000 L) delen door het debiet per minuut uit vraag 1 (420 L/min). Bereken: 84.000 ÷ 420 = ?\n\n🤔 **Reflectievraag:** Welke rekenregel gebruik je om tijd te berekenen: delen of vermenigvuldigen?"
            }
        },
        9: {  # Groentekwekerij - Breuk van totaal
            0: {  # Vraag 1
                1: "Dit is de opbrengst van VORIG jaar! Je hebt je laten afleiden door ruis in de tekst. De vraag gaat over DIT seizoen. Je moet berekenen: als 45 kg = ⅓, dan is het totaal = 45 × 3.\n\n🤔 **Reflectievraag:** Gaat de vraag over vorig jaar of dit seizoen?",
                2: "Je hebt 45 × 2 = 90 berekend, maar 45 kg is ⅓ van het totaal, niet de helft! Om het totaal te vinden: 45 × 3 = ?\n\n🤔 **Reflectievraag:** Als 45 kg = ⅓ is, met hoeveel moet je dan vermenigvuldigen voor het hele totaal?",
                3: "Controleer je berekening. Als 45 kg = ⅓ van het totaal is, dan bereken je het totaal zo: 45 × 3 = ?\n\n🤔 **Reflectievraag:** Hoeveel keer past ⅓ in een heel (1)?"
            }
        },
        19: {  # Fruit verkopen - Verhoudingen
            0: {  # Vraag 1
                0: "Je hebt het aantal PEREN berekend in plaats van appels! De verhouding is 5:3 (appels:peren). Je berekende (3/8) × 64 = 24 peren. Voor appels moet je (5/8) × 64 berekenen.\n\n🤔 **Reflectievraag:** Staat het getal 5 voor appels of voor peren in de verhouding 5:3?",
                1: "Je hebt 64 ÷ 2 = 32 berekend (gehalveerd), maar vergeten dat de verhouding 5:3 is (NIET 1:1)! Je moet eerst de verhouding optellen: 5 + 3 = 8 delen. Appels = (5/8) × 64 = ?\n\n🤔 **Reflectievraag:** Zijn er evenveel appels als peren, of is de verhouding anders?",
                # Optie 2 is correct
                3: "Controleer je berekening met verhoudingen. Eerst bereken je het totaal aantal delen: 5 + 3 = 8. Dan bereken je appels: (5/8) × 64 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen zijn er in totaal bij de verhouding 5:3?"
            },
            1: {  # Vraag 2 - Aftreksom
                0: "Je hebt 40 - 20 = 20 berekend, maar er worden maar 15 appels verkocht (niet 20)! Controleer de opgave: hoeveel appels worden er verkocht? Bereken: 40 - 15 = ?\n\n🤔 **Reflectievraag:** Hoeveel appels worden er volgens de vraag verkocht?",
                1: "Je hebt vergeten te aftrekken! Je gaf 35 als antwoord, maar dat zou betekenen dat er maar 5 appels verkocht zijn (40 - 5 = 35). De vraag zegt dat er 15 appels verkocht worden. Bereken: 40 - 15 = ?\n\n🤔 **Reflectievraag:** Wat is de rekenoperatie bij 'hoeveel blijven er over'? Optellen of aftrekken?",
                2: "Je hebt 40 - 10 = 30 berekend, maar er worden 15 appels verkocht (niet 10)! Controleer de getallen in de vraag goed. Bereken: 40 - 15 = ?\n\n🤔 **Reflectievraag:** Hoeveel appels worden er verkocht volgens de vraag: 10 of 15?"
                # Optie 3 is correct (25)
            },
            2: {  # Vraag 3 - Verhoudingen peren
                0: "Je hebt waarschijnlijk een verkeerde berekening gemaakt met de verhouding. Als appels:peren = 5:3 en er zijn 40 appels, dan bereken je: (3/5) × 40 = ?\n\n🤔 **Reflectievraag:** Als 5 delen = 40 appels, hoeveel appels zijn dan 1 deel?",
                1: "Je hebt misschien de verhouding verkeerd toegepast. Bij verhouding 5:3 (appels:peren) en 40 appels, bereken je peren zo: (3/5) × 40 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen peren horen bij 5 delen appels in de verhouding 5:3?",
                # Optie 2 is correct (24)
                3: "Controleer je berekening. De verhouding appels:peren = 5:3. Als er 40 appels zijn (5 delen), dan bereken je peren (3 delen): (3/5) × 40 = ?\n\n🤔 **Reflectievraag:** Heb je vermenigvuldigd met 3/5 of met een ander getal?"
            }
        },
        62: {  # Verf mengen - Verhoudingen
            0: {  # Vraag 1
                0: "Je hebt waarschijnlijk 15 - 9 = 6 berekend (aftrekken), maar bij verhoudingen moet je VERMENIGVULDIGEN! De verhouding is rood:geel = 5:3. Als je 15 L rood hebt, bereken je geel: (3/5) × 15 = ?\n\n🤔 **Reflectievraag:** Bij verhoudingen, tel je af of vermenigvuldig je met een breuk?",
                1: "Controleer je berekening met verhoudingen. De verhouding rood:geel = 5:3 betekent: voor elke 5 delen rood heb je 3 delen geel nodig. Bereken: (3/5) × 15 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen geel horen bij 5 delen rood in de verhouding 5:3?",
                # Optie 2 is correct
                3: "Dit is de hoeveelheid ROOD verf! De vraag vraagt naar GEEL. Je moet de verhouding gebruiken: rood:geel = 5:3. Als rood = 15 L, dan geel = (3/5) × 15 = ?\n\n🤔 **Reflectievraag:** Vraagt de vraag naar rode of gele verf?"
            }
        },
        63: {  # Limonade maken - Verhoudingen
            0: {  # Vraag 1
                0: "Je hebt de helft berekend (2 ÷ 4 = 0,5, en dan 0,5 ÷ 2 = 0,25... of 2 ÷ 10 = 0,2). Maar de verhouding siroop:water = 1:4 betekent 1+4=5 delen totaal. Siroop = (1/5) × 2 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen zijn er in totaal bij de verhouding 1:4?",
                1: "Dit is de hoeveelheid WATER (4/5 × 2 = 1,6... of andere berekening)! De vraag vraagt naar SIROOP. Bij verhouding 1:4 (siroop:water), siroop = (1/5) × 2 = ?\n\n🤔 **Reflectievraag:** Staat het getal 1 voor siroop of voor water in de verhouding 1:4?",
                2: "Je hebt afgerond naar 0,5 L, maar dat is niet de juiste berekening. Bij verhouding siroop:water = 1:4 (totaal 5 delen), bereken je: siroop = (1/5) × 2 = ?\n\n🤔 **Reflectievraag:** Waarom zou je afronden als de vraag om een exact bedrag vraagt?",
                # Optie 3 is correct
            }
        },
        64: {  # Schoolklas - Verhoudingen
            0: {  # Vraag 1
                0: "Controleer je berekening. Bij verhouding jongens:meisjes = 4:5 (totaal 9 delen) bereken je: jongens = (4/9) × 27 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen zijn er in totaal bij de verhouding 4:5?",
                # Optie 1 is correct
                2: "Je hebt waarschijnlijk (5/9) × 27 = 15 berekend, en daar iets van afgetrokken. Maar controleer: de verhouding is jongens:meisjes = 4:5. Jongens = (4/9) × 27 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen jongens zijn er bij de verhouding 4:5?",
                3: "Dit zou het aantal MEISJES kunnen zijn (5/9) × 27 = 15! De vraag vraagt naar JONGENS. Bij verhouding 4:5, jongens = (4/9) × 27 = ?\n\n🤔 **Reflectievraag:** Vraagt de vraag naar jongens of meisjes?"
            }
        },
        65: {  # Betonmengsel - 3-delige verhouding
            0: {  # Vraag 1
                0: "Controleer je berekening. De verhouding cement:zand:grind = 1:2:3 heeft 1+2+3=6 delen totaal. Cement = (1/6) × 60 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen zijn er in totaal bij de verhouding 1:2:3?",
                # Optie 1 is correct
                2: "Je hebt waarschijnlijk (2/6) × 60 = 20 berekend en daar nog iets mee gedaan. Maar cement is het EERSTE getal in 1:2:3. Cement = (1/6) × 60 = ?\n\n🤔 **Reflectievraag:** Welk getal staat voor cement in de verhouding cement:zand:grind = 1:2:3?",
                3: "Dit zou GRIND kunnen zijn (3/6) × 60 = 30... maar dan gehalveerd? Cement is het eerste deel: (1/6) × 60 = ?\n\n🤔 **Reflectievraag:** Vraagt de vraag naar cement, zand of grind?"
            }
        },
        66: {  # Schapenboerderij - Omgekeerde verhouding
            0: {  # Vraag 1
                # Optie 0 is correct
                1: "Controleer je berekening. Je weet dat wit = 63 schapen en de verhouding zwart:wit = 2:9. Dus als 9 delen = 63, dan is 1 deel = 7. Zwart = 2 × 7 = ?\n\n🤔 **Reflectievraag:** Hoeveel schapen horen bij 1 deel als 9 delen = 63 schapen?",
                2: "Controleer je berekening met de verhouding. Zwart:wit = 2:9, wit = 63. Als 9 delen = 63, dan 1 deel = 7, dus zwart = 2 × 7 = ?\n\n🤔 **Reflectievraag:** Heb je eerst berekend hoeveel schapen er bij 1 deel horen?",
                3: "Je hebt waarschijnlijk (2/9) × 81 = 18 berekend, maar er zijn NIET 81 witte schapen! Er zijn 63 witte schapen. Als 9 delen = 63, dan zwart (2 delen) = ?\n\n🤔 **Reflectievraag:** Hoeveel witte schapen zijn er volgens de opgave?"
            }
        },
        73: {  # Aquarium vissen - Omgekeerde verhouding
            0: {  # Vraag 1 - Guppy's
                0: "Je hebt waarschijnlijk een rekenfout gemaakt. Als 3 delen = 24 goudvissen, dan is 1 deel = 8. Guppy's (8 delen) = 8 × 8 = ?\n\n🤔 **Reflectievraag:** Als 3 delen = 24 goudvissen, hoeveel is dan 1 deel?",
                1: "Je hebt het aantal GOUDVISSEN gegeven! De vraag vraagt naar GUPPY'S. Als 1 deel = 8, dan guppy's (8 delen) = 8 × 8 = ?\n\n🤔 **Reflectievraag:** Vraagt de vraag naar goudvissen of naar guppy's?",
                2: "Controleer je berekening. Als 1 deel = 8, dan guppy's (8 delen) = 8 × 8 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen heeft guppy's in de verhouding goudvissen:guppy's = 3:8?"
                # Optie 3 is correct (64)
            },
            1: {  # Vraag 2 - Totaal
                0: "Je hebt niet alle vissen geteld. Tel op: 24 goudvissen + 64 guppy's = ?\n\n🤔 **Reflectievraag:** Heb je beide soorten vissen bij elkaar opgeteld?",
                1: "Controleer je optelling. Totaal = 24 + 64 = ?\n\n🤔 **Reflectievraag:** Welke twee getallen moet je bij elkaar optellen?",
                2: "Je hebt te veel of te weinig geteld. Het totaal is: 24 goudvissen + 64 guppy's = ?\n\n🤔 **Reflectievraag:** Heb je het juiste aantal guppy's gebruikt (64)?"
                # Optie 3 is correct (88)
            }
        },
        74: {  # Speeltuin toestellen - Omgekeerde verhouding
            0: {  # Vraag 1 - Schommels
                0: "Je hebt waarschijnlijk een rekenfout gemaakt. Als 2 delen = 6 wippen, dan is 1 deel = 3. Schommels (4 delen) = 4 × 3 = ?\n\n🤔 **Reflectievraag:** Als 2 delen = 6 wippen, hoeveel is dan 1 deel?",
                1: "Je hebt waarschijnlijk glijbanen en schommels verwisseld. Schommels heeft 4 delen (niet 3). Als 1 deel = 3, dan schommels = 4 × 3 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen heeft schommels in de verhouding 4:3:2?",
                2: "Controleer je berekening. Als 1 deel = 3, dan schommels (4 delen) = 4 × 3 = ?\n\n🤔 **Reflectievraag:** Als 1 deel = 3, wat is dan 4 × 3?"
                # Optie 3 is correct (12)
            },
            1: {  # Vraag 2 - Glijbanen
                0: "Je hebt het aantal WIPPEN gegeven! De vraag vraagt naar GLIJBANEN. Als 1 deel = 3, dan glijbanen (3 delen) = 3 × 3 = ?\n\n🤔 **Reflectievraag:** Vraagt de vraag naar wippen of naar glijbanen?",
                1: "Controleer je berekening. Als 1 deel = 3, dan glijbanen (3 delen) = 3 × 3 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen heeft glijbanen in de verhouding schommels:glijbanen:wippen = 4:3:2?",
                2: "Je hebt waarschijnlijk een rekenfout gemaakt. Glijbanen heeft 3 delen: 3 × 3 = ?\n\n🤔 **Reflectievraag:** Als 1 deel = 3, wat is dan 3 × 3?"
                # Optie 3 is correct (9)
            }
        },
        75: {  # Theemelange samenstellen - Omgekeerde verhouding
            0: {  # Vraag 1 - Kruidenthee
                0: "Je hebt waarschijnlijk de verhouding verkeerd toegepast. Als 5 delen = 40 gram groene thee, dan is 1 deel = 8. Kruidenthee (3 delen) = 3 × 8 = ?\n\n🤔 **Reflectievraag:** Als 5 delen = 40 gram, hoeveel is dan 1 deel?",
                1: "Je hebt waarschijnlijk 40 ÷ 2 = 20 berekend, maar de verhouding is 5:3 (NIET 1:1)! Als 1 deel = 8, dan kruidenthee (3 delen) = 3 × 8 = ?\n\n🤔 **Reflectievraag:** Is de verhouding groene:kruiden gelijk aan 1:1, of is het 5:3?",
                2: "Controleer je berekening. Als 1 deel = 8, dan kruidenthee (3 delen) = 3 × 8 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen heeft kruidenthee in de verhouding 5:3?"
                # Optie 3 is correct (24)
            },
            1: {  # Vraag 2 - Totaal
                0: "Je hebt alleen de groene thee geteld! Tel ook de kruidenthee mee: 40 + 24 = ?\n\n🤔 **Reflectievraag:** Heb je beide soorten thee bij elkaar opgeteld?",
                1: "Controleer je optelling. Totaal = 40 gram groene thee + 24 gram kruidenthee = ?\n\n🤔 **Reflectievraag:** Welke twee getallen moet je optellen voor het totaal?",
                2: "Je hebt te veel of te weinig geteld. Het totaal is: 40 + 24 = ?\n\n🤔 **Reflectievraag:** Heb je het juiste aantal gram kruidenthee gebruikt (24)?"
                # Optie 3 is correct (64)
            }
        },
        72: {  # Trailmix maken - Verhouding met totaal gegeven
            0: {  # Vraag 1 - Noten
                # Optie 0 is correct (200)
                1: "Je hebt waarschijnlijk een rekenfout gemaakt. De verhouding noten:rozijnen:chocolade = 4:2:1 heeft 4+2+1=7 delen. Noten = (4/7) × 350 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen zijn er in totaal bij de verhouding 4:2:1?",
                2: "Je hebt waarschijnlijk (3/7) × 350 = 150 berekend. Maar noten heeft 4 delen (niet 3)! Bereken: (4/7) × 350 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen heeft noten in de verhouding 4:2:1?",
                3: "Controleer je berekening. Bij verhouding 4:2:1 (totaal 7 delen), noten = (4/7) × 350 = ?\n\n🤔 **Reflectievraag:** Welke breuk gebruik je voor noten: 4/7 of een andere breuk?"
            },
            1: {  # Vraag 2 - Chocolade
                0: "Je hebt waarschijnlijk een rekenfout gemaakt. Chocolade heeft 1 deel uit 7 totaal: (1/7) × 350 = ?\n\n🤔 **Reflectievraag:** Als 1 deel = 50, wat is dan het antwoord voor chocolade (1 deel)?",
                1: "Controleer je berekening. Chocolade is het kleinste deel (1 uit 7): (1/7) × 350 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen heeft chocolade in de verhouding noten:rozijnen:chocolade = 4:2:1?",
                # Optie 2 is correct (50)
                3: "Je hebt waarschijnlijk een verkeerde breuk gebruikt. Chocolade heeft 1 deel (niet 2): (1/7) × 350 = ?\n\n🤔 **Reflectievraag:** Welk getal staat voor chocolade in de verhouding 4:2:1?"
            }
        },
        80: {  # Bibliotheek boeken - Omgekeerde verhouding
            0: {  # Vraag 1 - Fictie
                # Optie 0 is correct (200)
                1: "Je hebt waarschijnlijk een rekenfout gemaakt. Als 6 delen = 240 kinderboeken, dan is 1 deel = 40. Fictie (5 delen) = 5 × 40 = ?\n\n🤔 **Reflectievraag:** Als 6 delen = 240, hoeveel is dan 1 deel?",
                2: "Controleer je berekening. Als 1 deel = 40, dan fictie (5 delen) = 5 × 40 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen heeft fictie in de verhouding 5:4:6?",
                3: "Je hebt het aantal KINDERBOEKEN gegeven! De vraag vraagt naar FICTIE. Als 1 deel = 40, dan fictie (5 delen) = 5 × 40 = ?\n\n🤔 **Reflectievraag:** Vraagt de vraag naar kinderboeken of naar fictieboeken?"
            },
            1: {  # Vraag 2 - Non-fictie
                0: "Je hebt waarschijnlijk een rekenfout gemaakt. Als 6 delen = 240, dan is 1 deel = 40. Non-fictie (4 delen) = 4 × 40 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen heeft non-fictie in de verhouding fictie:non-fictie:kinderboeken = 5:4:6?",
                1: "Controleer je berekening. Als 1 deel = 40, dan non-fictie (4 delen) = 4 × 40 = ?\n\n🤔 **Reflectievraag:** Als 1 deel = 40, wat is dan 4 × 40?",
                2: "Je hebt waarschijnlijk fictie en non-fictie verwisseld. Non-fictie heeft 4 delen (niet 5). Als 1 deel = 40, dan non-fictie = 4 × 40 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen heeft non-fictie: 4 of 5?"
                # Optie 3 is correct (160)
            },
            2: {  # Vraag 3 - Totaal
                0: "Je hebt niet alle boeken meegeteld. Tel op: 200 fictie + 160 non-fictie + 240 kinderboeken = ?\n\n🤔 **Reflectievraag:** Heb je alle drie de soorten boeken bij elkaar opgeteld?",
                1: "Controleer je optelling. Het totaal is: 200 + 160 + 240 = ?\n\n🤔 **Reflectievraag:** Welke drie getallen moet je bij elkaar optellen?",
                2: "Je hebt te veel geteld of een rekenfout gemaakt. Tel: 200 fictie + 160 non-fictie + 240 kinderboeken = ?\n\n🤔 **Reflectievraag:** Heb je per ongeluk een getal dubbel geteld of verkeerd opgeteld?"
                # Optie 3 is correct (600)
            }
        },
        77: {  # Fruitschaal vullen - Omgekeerde verhouding
            0: {  # Vraag 1 - Peren
                0: "Je hebt waarschijnlijk de verhouding gehalveerd: 24 ÷ 2 = 12. Maar de verhouding is 6:4:5 (NIET 2:1)! Als 6 delen = 24 appels, dan is 1 deel = 4. Peren (4 delen) = 4 × 4 = ?\n\n🤔 **Reflectievraag:** Als 6 delen = 24 appels, hoeveel is dan 1 deel?",
                1: "Controleer je berekening. Als 6 delen = 24 appels, dan is 1 deel = 4. Peren heeft 4 delen, dus peren = 4 × 4 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen horen bij peren in de verhouding 6:4:5?",
                # Optie 2 is correct (16)
                3: "Je hebt waarschijnlijk (4/6) × 24 = 16 berekend en daar nog iets bijgeteld, of een andere fout gemaakt. Controleer: als 1 deel = 4, dan peren (4 delen) = ?\n\n🤔 **Reflectievraag:** Heb je vermenigvuldigd met het juiste aantal delen (4)?"
            },
            1: {  # Vraag 2 - Sinaasappels
                0: "Je hebt waarschijnlijk een rekenfout gemaakt. Als 6 delen = 24 appels, dan is 1 deel = 4. Sinaasappels (5 delen) = 5 × 4 = ?\n\n🤔 **Reflectievraag:** Als 1 deel = 4, en sinaasappels heeft 5 delen, wat is dan 5 × 4?",
                1: "Je hebt waarschijnlijk peren en sinaasappels verwisseld, of een andere fout gemaakt. Sinaasappels heeft 5 delen (niet 4). Als 1 deel = 4, dan sinaasappels = 5 × 4 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen heeft sinaasappels in de verhouding appels:peren:sinaasappels = 6:4:5?",
                2: "Je hebt het aantal APPELS gegeven! De vraag vraagt naar SINAASAPPELS. Als 1 deel = 4, dan sinaasappels (5 delen) = 5 × 4 = ?\n\n🤔 **Reflectievraag:** Vraagt de vraag naar appels of naar sinaasappels?",
                # Optie 3 is correct (20)
            },
            2: {  # Vraag 3 - Totaal
                0: "Je hebt niet alle fruit meegeteld. Tel op: 24 appels + 16 peren + 20 sinaasappels = ?\n\n🤔 **Reflectievraag:** Heb je alle drie de soorten fruit bij elkaar opgeteld?",
                1: "Controleer je optelling. Tel alle fruit: 24 + 16 + 20 = ?\n\n🤔 **Reflectievraag:** Welke drie getallen moet je bij elkaar optellen voor het totaal?",
                # Optie 2 is correct (60)
                3: "Je hebt te veel geteld of een rekenfout gemaakt. Het totaal is: 24 appels + 16 peren + 20 sinaasappels = ?\n\n🤔 **Reflectievraag:** Heb je per ongeluk een getal dubbel geteld?"
            }
        },
        71: {  # Bloementuin aanleggen - 3-delige verhouding
            0: {  # Vraag 1 - Tulpen
                0: "Je hebt waarschijnlijk (5/12) × 120 = 50 berekend. Maar de verhouding tulpen:rozen:narcissen = 5:3:2 heeft 5+3+2=10 delen (niet 12)! Tulpen = (5/10) × 120 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen zijn er in totaal bij de verhouding 5:3:2?",
                1: "Je hebt waarschijnlijk een rekenfout gemaakt of de verkeerde breuk gebruikt. Bij verhouding 5:3:2 (totaal 10 delen), tulpen = (5/10) × 120 = ?\n\n🤔 **Reflectievraag:** Welke breuk gebruik je voor tulpen: 5/10 of een andere breuk?",
                2: "Je hebt waarschijnlijk rozen en tulpen verwisseld. Controleer: tulpen is het EERSTE getal in de verhouding 5:3:2. Tulpen = (5/10) × 120 = ?\n\n🤔 **Reflectievraag:** Welk getal in de verhouding 5:3:2 staat voor tulpen?"
                # Optie 3 is correct (60)
            },
            1: {  # Vraag 2 - Narcissen
                # Optie 0 is correct (24)
                1: "Je hebt waarschijnlijk een verkeerde breuk gebruikt. Narcissen is het DERDE getal in 5:3:2 (tulpen:rozen:narcissen), dus narcissen = (2/10) × 120 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen horen bij narcissen in de verhouding 5:3:2?",
                2: "Je hebt waarschijnlijk (3/10) × 120 = 30 berekend - dat zijn de ROZEN! Narcissen is het laatste getal (2 delen): (2/10) × 120 = ?\n\n🤔 **Reflectievraag:** Staat het getal 2 voor narcissen of voor rozen in de verhouding tulpen:rozen:narcissen = 5:3:2?",
                3: "Je hebt waarschijnlijk (3/10) × 120 = 36 berekend - dat zijn de ROZEN! Narcissen heeft 2 delen (niet 3): (2/10) × 120 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen heeft narcissen: 2 of 3?"
            },
            2: {  # Vraag 3 - Rozen
                0: "Je hebt waarschijnlijk (3/12) × 120 = 30 berekend. Maar het totaal aantal delen is 5+3+2=10 (niet 12)! Rozen = (3/10) × 120 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen zijn er totaal bij de verhouding 5:3:2?",
                1: "Controleer je berekening. Bij verhouding tulpen:rozen:narcissen = 5:3:2 (totaal 10 delen), rozen = (3/10) × 120 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen heeft rozen in de verhouding 5:3:2?",
                # Optie 2 is correct (36)
                3: "Je hebt waarschijnlijk een verkeerde breuk gebruikt of een rekenfout gemaakt. Rozen heeft 3 delen uit 10 totaal: (3/10) × 120 = ?\n\n🤔 **Reflectievraag:** Welke breuk gebruik je voor rozen: 3/10 of een andere?"
            }
        },
        2: {  # Voetbaltoernooi - Combinatoriek
            0: {  # Vraag 1
                0: "Je hebt waarschijnlijk 6 + 6 gerekend of een andere verkeerde berekening gemaakt. Bij 'elk team speelt tegen elk ander team' moet je bedenken: elk team speelt tegen 5 andere teams (niet tegen zichzelf). Dat is 6 × 5 = 30, maar dan tel je elke wedstrijd dubbel!\n\n🤔 **Reflectievraag:** Als team A tegen team B speelt, is dat dan 1 wedstrijd of 2 wedstrijden?",
                # Optie 1 is correct
                2: "Je bent dichtbij! Je hebt waarschijnlijk een rekenfout gemaakt. De formule is: (aantal teams × tegenstanders per team) ÷ 2. Controleer: (6 × 5) ÷ 2 = ?\n\n🤔 **Reflectievraag:** Hoeveel tegenstanders heeft elk team? (Hint: het totaal minus 1)",
                3: "Je hebt 6 × 5 = 30 berekend, maar vergeten te delen door 2! Als team A tegen team B speelt, tel je die wedstrijd twee keer: één keer bij A en één keer bij B. Je moet dus delen door 2 om dubbeltellingen te voorkomen.\n\n🤔 **Reflectievraag:** Als team A tegen team B speelt, is dat dan 1 wedstrijd of 2 verschillende wedstrijden?"
            },
            1: {  # Vraag 2
                0: "Je hebt waarschijnlijk alleen 12 toeschouwers genomen en vergeten te vermenigvuldigen. Je moet berekenen: aantal toeschouwers × aantal wedstrijden. Gebruik je antwoord uit vraag 1!\n\n🤔 **Reflectievraag:** Als er 12 toeschouwers bij elke wedstrijd zijn, hoeveel mensen zijn er dan in totaal bij 2 wedstrijden?",
                # Optie 1 is correct
                2: "Controleer je berekening. Heb je het juiste aantal wedstrijden gebruikt uit vraag 1? Het moet zijn: 12 toeschouwers × 15 wedstrijden = ?\n\n🤔 **Reflectievraag:** Hoeveel wedstrijden waren er volgens vraag 1?",
                3: "Je hebt waarschijnlijk het verkeerde aantal wedstrijden gebruikt (30 in plaats van 15). Controleer eerst je antwoord bij vraag 1. Het juiste aantal wedstrijden is 15, dus: 12 × 15 = ?\n\n🤔 **Reflectievraag:** Heb je de dubbeltelling bij vraag 1 correct verwerkt? Het antwoord moet 15 wedstrijden zijn, niet 30."
            }
        }
    }

    # Pas verbeteringen toe
    aanpassingen_gemaakt = 0
    for item in data:
        item_id = item.get('id')
        if item_id in verbeteringen and 'questions' in item:
            for q_idx, question in enumerate(item['questions']):
                if q_idx in verbeteringen[item_id] and 'options' in question:
                    for opt_idx, option in enumerate(question['options']):
                        if opt_idx in verbeteringen[item_id][q_idx]:
                            nieuwe_analyse = verbeteringen[item_id][q_idx][opt_idx]
                            oude_analyse = option.get('foutanalyse', '')

                            # Alleen updaten als de oude analyse zwak is (kort of leeg)
                            if len(oude_analyse) < 50 or '🤔' not in oude_analyse:
                                option['foutanalyse'] = nieuwe_analyse
                                aanpassingen_gemaakt += 1
                                print(f"✅ Verbeterd: ID {item_id}, Vraag {q_idx + 1}, Optie {opt_idx + 1}")
                                print(f"   OUD: {oude_analyse[:60]}...")
                                print(f"   NIEUW: {nieuwe_analyse[:60]}...")
                                print()

    # Schrijf terug
    with open('verhaaltjessommen - Template.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Klaar! {aanpassingen_gemaakt} foutanalyses verbeterd.")
    return aanpassingen_gemaakt

if __name__ == '__main__':
    verbeter_foutanalyses()
