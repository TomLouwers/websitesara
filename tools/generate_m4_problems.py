import json

# Problem templates for each topic
problems_data = [
    # Aftrekken (3 more - IDs 21-23)
    {"id": 21, "title": "Speelgoed opruimen", "theme": "aftrekken", "operation": "45 - 18", "answer": 27, "context": "Er liggen 45 speelgoedblokken op de grond. Kim ruimt er 18 op.", "question": "Hoeveel blokken liggen er nog op de grond?", "unit": "blokken"},
    {"id": 22, "title": "Vogels op het dak", "theme": "aftrekken", "operation": "52 - 27", "answer": 25, "context": "Er zitten 52 vogels op het dak. Dan vliegen er 27 weg.", "question": "Hoeveel vogels blijven er over?", "unit": "vogels"},
    {"id": 23, "title": "Pagina's lezen", "theme": "aftrekken", "operation": "80 - 43", "answer": 37, "context": "Een boek heeft 80 pagina's. Sofie heeft al 43 pagina's gelezen.", "question": "Hoeveel pagina's moet Sofie nog lezen?", "unit": "pagina's"},

    # Optellen (2 more - IDs 24-25)
    {"id": 24, "title": "Kralen rijgen", "theme": "optellen", "operation": "23 + 19", "answer": 42, "context": "Maya heeft 23 rode kralen en 19 blauwe kralen.", "question": "Hoeveel kralen heeft Maya in totaal?", "unit": "kralen"},
    {"id": 25, "title": "Punten scoren", "theme": "optellen", "operation": "38 + 27", "answer": 65, "context": "Bij een spelletje scoort team A 38 punten en team B 27 punten.", "question": "Hoeveel punten hebben beide teams samen?", "unit": "punten"},

    # Vermenigvuldigen (2 more - IDs 26-27)
    {"id": 26, "title": "Eieren in dozen", "theme": "vermenigvuldigen", "operation": "6 × 7", "answer": 42, "context": "In een doos zitten 6 eieren. De boer heeft 7 dozen.", "question": "Hoeveel eieren heeft de boer in totaal?", "unit": "eieren"},
    {"id": 27, "title": "Wielen van fietsen", "theme": "vermenigvuldigen", "operation": "8 × 2", "answer": 16, "context": "Er staan 8 fietsen in de schuur. Elke fiets heeft 2 wielen.", "question": "Hoeveel wielen zijn er in totaal?", "unit": "wielen"},

    # Geld (2 more - IDs 28-29)
    {"id": 28, "title": "Spaarpot", "theme": "geld", "operation": "10 × 0.50", "answer": 5, "context": "Liam heeft 10 munten van 50 cent in zijn spaarpot.", "question": "Hoeveel euro heeft Liam gespaard?", "unit": "euro"},
    {"id": 29, "title": "Speelgoed kopen", "theme": "geld", "operation": "10 - 6", "answer": 4, "context": "Een speelgoedauto kost €6. Isa geeft een briefje van €10.", "question": "Hoeveel wisselgeld krijgt Isa terug?", "unit": "euro"},

    # Verhoudingen (4 more - IDs 30-33)
    {"id": 30, "title": "Appels delen", "theme": "verhoudingen", "operation": "12 ÷ 2", "answer": 6, "context": "Er liggen 12 appels op tafel. De helft is groen.", "question": "Hoeveel groene appels zijn er?", "unit": "appels"},
    {"id": 31, "title": "Pizza snijden", "theme": "verhoudingen", "operation": "8 ÷ 4", "answer": 2, "context": "Een pizza is in 8 stukken gesneden. Een kwart van de pizza is met kaas.", "question": "Hoeveel stukken zijn met kaas?", "unit": "stukken"},
    {"id": 32, "title": "Kleurpotloden", "theme": "verhoudingen", "operation": "20 ÷ 2", "answer": 10, "context": "In een doos zitten 20 kleurpotloden. De helft is rood.", "question": "Hoeveel rode kleurpotloden zitten er in de doos?", "unit": "kleurpotloden"},
    {"id": 33, "title": "Snoepjes verdelen", "theme": "verhoudingen", "operation": "24 ÷ 3", "answer": 8, "context": "Oma heeft 24 snoepjes. Een derde is voor de kinderen.", "question": "Hoeveel snoepjes krijgen de kinderen?", "unit": "snoepjes"},

    # Tijd (4 more - IDs 34-37)
    {"id": 34, "title": "Huiswerk maken", "theme": "tijd", "operation": "45 min", "answer": "drie kwartier", "context": "Jamal begint om 14:00 uur met zijn huiswerk. Hij is klaar om 14:45 uur.", "question": "Hoelang heeft Jamal aan zijn huiswerk gewerkt?", "unit": "tijd"},
    {"id": 35, "title": "Naar school fietsen", "theme": "tijd", "operation": "15 min", "answer": "kwartier", "context": "Lisa fietst elke dag 15 minuten naar school.", "question": "Hoeveel is dat in kwartier?", "unit": "tijd"},
    {"id": 36, "title": "Film kijken", "theme": "tijd", "operation": "120 min", "answer": 2, "context": "Een film duurt 120 minuten.", "question": "Hoeveel uur duurt de film?", "unit": "uur"},
    {"id": 37, "title": "Zwemles", "theme": "tijd", "operation": "30 min × 2", "answer": "1 uur", "context": "De zwemles duurt 30 minuten. Er zijn 2 lessen achter elkaar.", "question": "Hoelang duren beide lessen samen?", "unit": "tijd"},

    # Lengte (4 more - IDs 38-41)
    {"id": 38, "title": "Touw meten", "theme": "lengte", "operation": "150 cm", "answer": "1,5 meter", "context": "Een touw is 150 centimeter lang.", "question": "Hoeveel meter is dat?", "unit": "meter"},
    {"id": 39, "title": "Springen", "theme": "lengte", "operation": "80 + 95", "answer": 175, "context": "Tim springt 80 cm ver. Eva springt 95 cm ver.", "question": "Hoeveel centimeter springen ze samen?", "unit": "centimeter"},
    {"id": 40, "title": "Potlood en pen", "theme": "lengte", "operation": "14 - 9", "answer": 5, "context": "Een potlood is 14 cm lang. Een pen is 9 cm lang.", "question": "Hoeveel centimeter langer is het potlood?", "unit": "centimeter"},
    {"id": 41, "title": "Boom en struik", "theme": "lengte", "operation": "3 meter", "answer": 300, "context": "Een boom is 3 meter hoog.", "question": "Hoeveel centimeter is dat?", "unit": "centimeter"},

    # Gewicht (4 more - IDs 42-45)
    {"id": 42, "title": "Rugzak wegen", "theme": "gewicht", "operation": "3500 gram", "answer": "3,5 kg", "context": "Een rugzak weegt 3500 gram.", "question": "Hoeveel kilogram is dat?", "unit": "kilogram"},
    {"id": 43, "title": "Fruit wegen", "theme": "gewicht", "operation": "300 + 450", "answer": 750, "context": "Een appel weegt 300 gram. Een banaan weegt 450 gram.", "question": "Hoeveel gram wegen ze samen?", "unit": "gram"},
    {"id": 44, "title": "Zware tas", "theme": "gewicht", "operation": "5 kg", "answer": 5000, "context": "Mama's boodschappentas weegt 5 kilogram.", "question": "Hoeveel gram is dat?", "unit": "gram"},
    {"id": 45, "title": "Afvallen", "theme": "gewicht", "operation": "4000 - 500", "answer": 3500, "context": "Een pakket weegt 4000 gram. Na het uitpakken weegt de inhoud 500 gram minder.", "question": "Hoeveel gram weegt de inhoud?", "unit": "gram"},

    # Inhoud (4 more - IDs 46-49)
    {"id": 46, "title": "Regenton", "theme": "inhoud", "operation": "50 liter", "answer": 50000, "context": "In een regenton zit 50 liter water.", "question": "Hoeveel milliliter is dat?", "unit": "milliliter"},
    {"id": 47, "title": "Emmer vullen", "theme": "inhoud", "operation": "8 liter", "answer": 8000, "context": "Een emmer bevat 8 liter water.", "question": "Hoeveel milliliter is dat?", "unit": "milliliter"},
    {"id": 48, "title": "Sap drinken", "theme": "inhoud", "operation": "1500 ml", "answer": "1,5 liter", "context": "In een pak zit 1500 milliliter sap.", "question": "Hoeveel liter is dat?", "unit": "liter"},
    {"id": 49, "title": "Aquarium", "theme": "inhoud", "operation": "3000 ÷ 500", "answer": 6, "context": "Een aquarium bevat 3000 milliliter water. Een beker kan 500 milliliter bevatten.", "question": "Hoeveel bekers water zitten er in het aquarium?", "unit": "bekers"},

    # Meetkunde (4 more - IDs 50-53)
    {"id": 50, "title": "Driehoek tekenen", "theme": "meetkunde", "operation": "5 + 5 + 5", "answer": 15, "context": "Noah tekent een gelijkzijdige driehoek. Elke zijde is 5 cm lang.", "question": "Hoeveel centimeter is de omtrek?", "unit": "centimeter"},
    {"id": 51, "title": "Rechthoek", "theme": "meetkunde", "operation": "6 + 4 + 6 + 4", "answer": 20, "context": "Een rechthoek is 6 cm lang en 4 cm breed.", "question": "Hoeveel centimeter is de omtrek?", "unit": "centimeter"},
    {"id": 52, "title": "Hek rond tuin", "theme": "meetkunde", "operation": "8 + 8 + 8 + 8", "answer": 32, "context": "Een vierkante tuin heeft zijden van 8 meter.", "question": "Hoelang moet het hek zijn om helemaal rond de tuin te gaan?", "unit": "meter"},
    {"id": 53, "title": "Raam meten", "theme": "meetkunde", "operation": "3 × 4", "answer": 12, "context": "Een vierkant raam heeft zijden van 3 meter.", "question": "Hoeveel meter is de omtrek van het raam?", "unit": "meter"}
]

print("Generated", len(problems_data), "problems")
print("IDs:", [p["id"] for p in problems_data])
