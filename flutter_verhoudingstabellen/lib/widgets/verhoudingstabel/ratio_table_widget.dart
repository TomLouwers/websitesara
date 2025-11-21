import 'package:flutter/material.dart';
import '../../models/verhoudingstabel_model.dart';
import 'animated_arrow.dart';

/// Widget voor verhoudingen (bv. melk:bloem 3:2)
/// Toont visueel hoe je van gegeven waarde naar antwoord komt via "1 deel"
class RatioTableWidget extends StatefulWidget {
  final VerhoudingData data;

  const RatioTableWidget({
    Key? key,
    required this.data,
  }) : super(key: key);

  @override
  State<RatioTableWidget> createState() => _RatioTableWidgetState();
}

class _RatioTableWidgetState extends State<RatioTableWidget> {
  int _currentStep = 0;
  final int _totalSteps = 3; // Gegeven → 1 deel → Antwoord

  void _nextStep() {
    if (_currentStep < _totalSteps - 1) {
      setState(() {
        _currentStep++;
      });
    }
  }

  void _reset() {
    setState(() {
      _currentStep = 0;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Titel met ratio
            _buildTitle(),
            const SizedBox(height: 24),

            // De tabel met animaties
            _buildRatioTable(),
            const SizedBox(height: 24),

            // Uitleg van huidige stap
            _buildStepExplanation(),
            const SizedBox(height: 16),

            // Controle knoppen
            _buildControls(),
          ],
        ),
      ),
    );
  }

  Widget _buildTitle() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.purple.shade300, Colors.blue.shade300],
        ),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.calculate, color: Colors.white, size: 28),
          const SizedBox(width: 12),
          Text(
            'Verhouding ${widget.data.ratio}',
            style: const TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRatioTable() {
    // Groepeer kolommen per rij
    final melkKolommen = widget.data.kolommen
        .where((k) => k.rij == 'melk')
        .toList();
    final delenKolommen = widget.data.kolommen
        .where((k) => k.rij == 'delen')
        .toList();
    final bloemKolommen = widget.data.kolommen
        .where((k) => k.rij == 'bloem')
        .toList();

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.blue.shade50,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.blue.shade200, width: 2),
      ),
      child: Column(
        children: [
          // Melk rij
          _buildRow(
            label: 'Melk',
            icon: Icons.local_drink,
            color: Colors.lightBlue,
            kolommen: melkKolommen,
          ),
          const SizedBox(height: 16),

          // Delen rij
          _buildRow(
            label: 'Delen',
            icon: Icons.pie_chart,
            color: Colors.orange,
            kolommen: delenKolommen,
          ),
          const SizedBox(height: 16),

          // Bloem rij
          _buildRow(
            label: 'Bloem',
            icon: Icons.grain,
            color: Colors.brown,
            kolommen: bloemKolommen,
          ),
        ],
      ),
    );
  }

  Widget _buildRow({
    required String label,
    required IconData icon,
    required Color color,
    required List<VerhoudingKolom> kolommen,
  }) {
    return Row(
      children: [
        // Label met icoon
        SizedBox(
          width: 100,
          child: Row(
            children: [
              Icon(icon, color: color, size: 24),
              const SizedBox(width: 8),
              Text(
                label,
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: color,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(width: 20),

        // Kolommen met pijlen
        Expanded(
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              // Kolom 1: Gegeven waarde
              if (kolommen.isNotEmpty)
                _buildValueBox(
                  kolommen[0],
                  0,
                  color,
                  isHighlighted: _currentStep >= 0,
                ),

              // Pijl 1: Delen operatie
              if (_currentStep >= 1 && widget.data.operaties.isNotEmpty)
                AnimatedArrow(
                  operatie: widget.data.operaties[0].operatie,
                  color: color,
                  animationDelay: const Duration(milliseconds: 300),
                ),

              // Kolom 2: 1 deel
              if (kolommen.length > 1 && _currentStep >= 1)
                _buildValueBox(
                  kolommen[1],
                  1,
                  color,
                  isHighlighted: _currentStep >= 1,
                ),

              // Pijl 2: Vermenigvuldig operatie
              if (_currentStep >= 2 &&
                  widget.data.operaties.length > 1 &&
                  kolommen.length > 2)
                AnimatedArrow(
                  operatie: widget.data.operaties[1].operatie,
                  color: color,
                  animationDelay: const Duration(milliseconds: 600),
                ),

              // Kolom 3: Antwoord
              if (kolommen.length > 2 && _currentStep >= 2)
                _buildValueBox(
                  kolommen[2],
                  2,
                  color,
                  isHighlighted: _currentStep >= 2,
                  isAnswer: true,
                ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildValueBox(
    VerhoudingKolom kolom,
    int stepIndex,
    Color color, {
    bool isHighlighted = false,
    bool isAnswer = false,
  }) {
    return TweenAnimationBuilder<double>(
      duration: const Duration(milliseconds: 500),
      tween: Tween(begin: 0.0, end: isHighlighted ? 1.0 : 0.3),
      builder: (context, value, child) {
        return Transform.scale(
          scale: 0.9 + (value * 0.1),
          child: Container(
            width: 100,
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 16),
            decoration: BoxDecoration(
              color: isAnswer
                  ? Colors.green.shade100
                  : Colors.white.withOpacity(value),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: isAnswer
                    ? Colors.green.shade400
                    : color.withOpacity(value),
                width: isAnswer ? 3 : 2,
              ),
              boxShadow: isHighlighted
                  ? [
                      BoxShadow(
                        color: color.withOpacity(0.3),
                        blurRadius: 8,
                        spreadRadius: 2,
                      )
                    ]
                  : [],
            ),
            child: Column(
              children: [
                Text(
                  '${kolom.waarde}',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: isAnswer ? Colors.green.shade700 : color,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  kolom.eenheid,
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey.shade700,
                  ),
                ),
                if (kolom.berekening != null) ...[
                  const SizedBox(height: 8),
                  Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: Colors.blue.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      kolom.berekening!,
                      style: TextStyle(
                        fontSize: 11,
                        color: Colors.blue.shade900,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildStepExplanation() {
    String explanation;
    IconData icon;
    Color color;

    switch (_currentStep) {
      case 0:
        explanation =
            '👀 Stap 1: Hier beginnen we! We hebben ${widget.data.kolommen[0].waarde} ${widget.data.kolommen[0].eenheid} ${widget.data.kolommen[0].rij}.';
        icon = Icons.start;
        color = Colors.blue;
        break;
      case 1:
        explanation = widget.data.operaties.isNotEmpty
            ? '🧮 Stap 2: ${widget.data.operaties[0].uitleg}. Nu weten we wat 1 deel is!'
            : 'Berekenen...';
        icon = Icons.calculate;
        color = Colors.orange;
        break;
      case 2:
        explanation = widget.data.operaties.length > 1
            ? '🎯 Stap 3: ${widget.data.operaties[1].uitleg}. Klaar!'
            : 'Antwoord gevonden!';
        icon = Icons.celebration;
        color = Colors.green;
        break;
      default:
        explanation = '';
        icon = Icons.info;
        color = Colors.grey;
    }

    return TweenAnimationBuilder<double>(
      key: ValueKey(_currentStep),
      duration: const Duration(milliseconds: 400),
      tween: Tween(begin: 0.0, end: 1.0),
      builder: (context, value, child) {
        return Opacity(
          opacity: value,
          child: Transform.translate(
            offset: Offset(0, 20 * (1 - value)),
            child: Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: color, width: 2),
              ),
              child: Row(
                children: [
                  Icon(icon, color: color, size: 32),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      explanation,
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w500,
                        color: color.shade900,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildControls() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        if (_currentStep > 0)
          ElevatedButton.icon(
            onPressed: _reset,
            icon: const Icon(Icons.replay),
            label: const Text('Opnieuw'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.grey.shade300,
              foregroundColor: Colors.black87,
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            ),
          ),
        if (_currentStep > 0) const SizedBox(width: 16),
        if (_currentStep < _totalSteps - 1)
          ElevatedButton.icon(
            onPressed: _nextStep,
            icon: const Icon(Icons.arrow_forward),
            label: const Text('Volgende Stap'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.blue.shade400,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            ),
          ),
        if (_currentStep == _totalSteps - 1)
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            decoration: BoxDecoration(
              color: Colors.green.shade100,
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: Colors.green.shade400, width: 2),
            ),
            child: Row(
              children: [
                Icon(Icons.check_circle, color: Colors.green.shade700),
                const SizedBox(width: 8),
                Text(
                  'Klaar!',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.green.shade700,
                  ),
                ),
              ],
            ),
          ),
      ],
    );
  }
}
