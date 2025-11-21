import 'package:flutter/material.dart';
import 'widgets/verhoudingstabel/verhoudingstabel_widget.dart';

void main() {
  runApp(const VerhoudingstabellenDemoApp());
}

class VerhoudingstabellenDemoApp extends StatelessWidget {
  const VerhoudingstabellenDemoApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Verhoudingstabellen Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const DemoPage(),
    );
  }
}

class DemoPage extends StatefulWidget {
  const DemoPage({Key? key}) : super(key: key);

  @override
  State<DemoPage> createState() => _DemoPageState();
}

class _DemoPageState extends State<DemoPage> {
  int _selectedIndex = 0;

  final List<Map<String, dynamic>> _examples = [
    {
      'title': '🥛 Verhouding: Melk & Bloem (3:2)',
      'subtitle': 'Pannenkoeken maken met verhoudingen',
      'data': {
        "type": "verhouding",
        "ratio": "3:2",
        "labels": ["melk", "delen", "bloem"],
        "kolommen": [
          {
            "waarde": 300,
            "eenheid": "ml",
            "label": "gegeven",
            "rij": "melk"
          },
          {
            "waarde": 3,
            "eenheid": "delen",
            "label": "verhouding",
            "rij": "delen"
          },
          {
            "waarde": 100,
            "eenheid": "ml",
            "label": "1 deel",
            "rij": "melk",
            "berekening": "300 ÷ 3"
          },
          {
            "waarde": 1,
            "eenheid": "deel",
            "label": "1 deel",
            "rij": "delen"
          },
          {
            "waarde": 200,
            "eenheid": "gram",
            "label": "antwoord",
            "rij": "bloem",
            "berekening": "2 × 100"
          },
          {
            "waarde": 2,
            "eenheid": "delen",
            "label": "verhouding",
            "rij": "delen"
          }
        ],
        "operaties": [
          {
            "van": 0,
            "naar": 2,
            "operatie": "÷3",
            "uitleg": "Bereken 1 deel"
          },
          {
            "van": 2,
            "naar": 4,
            "operatie": "×2",
            "uitleg": "Bloem is 2 delen"
          }
        ]
      }
    },
    {
      'title': '🎂 Recept Opschalen (×1,5)',
      'subtitle': 'Taart voor meer personen bakken',
      'data': {
        "type": "schaalfactor",
        "factor": 1.5,
        "kolommen": [
          {
            "waarde": 8,
            "eenheid": "personen",
            "label": "origineel"
          },
          {
            "waarde": 12,
            "eenheid": "personen",
            "label": "nieuw"
          },
          {
            "waarde": 200,
            "eenheid": "gram",
            "label": "bloem origineel"
          },
          {
            "waarde": 300,
            "eenheid": "gram",
            "label": "bloem nieuw",
            "berekening": "200 × 1,5"
          }
        ],
        "operaties": [
          {
            "van": 0,
            "naar": 1,
            "operatie": "×1,5",
            "uitleg": "12 personen is 1,5× zoveel als 8"
          }
        ]
      }
    },
    {
      'title': '📚 Percentage Verdeling',
      'subtitle': '800 boeken in de bibliotheek',
      'data': {
        "type": "percentage_verdeling",
        "totaal": 800,
        "eenheid": "boeken",
        "categorieën": [
          {
            "label": "kinderboek",
            "percentage": 35,
            "aantal": 280,
            "berekening": "35% van 800"
          },
          {
            "label": "roman",
            "percentage": 45,
            "aantal": 360,
            "berekening": "45% van 800"
          },
          {
            "label": "stripboek",
            "percentage": 20,
            "aantal": 160,
            "berekening": "20% van 800"
          }
        ]
      }
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Verhoudingstabellen voor Sara 🎨'),
        backgroundColor: Colors.blue.shade400,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: Row(
        children: [
          // Sidebar met voorbeelden
          Container(
            width: 300,
            color: Colors.grey.shade100,
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _examples.length,
              itemBuilder: (context, index) {
                final example = _examples[index];
                final isSelected = _selectedIndex == index;

                return Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: Material(
                    color: Colors.transparent,
                    child: InkWell(
                      onTap: () {
                        setState(() {
                          _selectedIndex = index;
                        });
                      },
                      borderRadius: BorderRadius.circular(12),
                      child: Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: isSelected
                              ? Colors.blue.shade100
                              : Colors.white,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(
                            color: isSelected
                                ? Colors.blue.shade400
                                : Colors.grey.shade300,
                            width: isSelected ? 3 : 1,
                          ),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              example['title'],
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: isSelected
                                    ? Colors.blue.shade900
                                    : Colors.grey.shade800,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              example['subtitle'],
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.grey.shade600,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
          ),

          // Main content
          Expanded(
            child: Container(
              color: Colors.white,
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(32),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Titel van huidige voorbeeld
                    Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [
                            Colors.purple.shade100,
                            Colors.blue.shade100,
                          ],
                        ),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            _examples[_selectedIndex]['title'],
                            style: const TextStyle(
                              fontSize: 28,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            _examples[_selectedIndex]['subtitle'],
                            style: TextStyle(
                              fontSize: 16,
                              color: Colors.grey.shade700,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 32),

                    // De verhoudingstabel widget
                    VerhoudingstabelWidget(
                      verhoudingstabelJson: _examples[_selectedIndex]['data'],
                    ),

                    const SizedBox(height: 32),

                    // Info box
                    Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: Colors.amber.shade50,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(
                          color: Colors.amber.shade300,
                          width: 2,
                        ),
                      ),
                      child: Row(
                        children: [
                          Icon(
                            Icons.lightbulb,
                            color: Colors.amber.shade700,
                            size: 32,
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Text(
                              'Tip: Klik op de knoppen om stap voor stap de berekening te zien!',
                              style: TextStyle(
                                fontSize: 14,
                                color: Colors.amber.shade900,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
