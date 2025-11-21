import 'package:flutter/material.dart';
import '../../models/verhoudingstabel_model.dart';
import 'animated_arrow.dart';

/// Widget voor recepten opschalen met een factor
/// Toont simpele × factor animatie
class ScaleFactorWidget extends StatefulWidget {
  final ScaleFactorData data;

  const ScaleFactorWidget({
    Key? key,
    required this.data,
  }) : super(key: key);

  @override
  State<ScaleFactorWidget> createState() => _ScaleFactorWidgetState();
}

class _ScaleFactorWidgetState extends State<ScaleFactorWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  bool _showResult = false;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    );

    _scaleAnimation = Tween<double>(begin: 1.0, end: widget.data.factor).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOutCubic),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _startAnimation() {
    setState(() {
      _showResult = false;
    });
    _controller.forward().then((_) {
      setState(() {
        _showResult = true;
      });
    });
  }

  void _reset() {
    _controller.reset();
    setState(() {
      _showResult = false;
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
          children: [
            _buildTitle(),
            const SizedBox(height: 32),
            _buildScaleVisualization(),
            const SizedBox(height: 32),
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
          colors: [Colors.orange.shade300, Colors.pink.shade300],
        ),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.restaurant, color: Colors.white, size: 28),
          const SizedBox(width: 12),
          Text(
            'Recept Opschalen ×${widget.data.factor}',
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

  Widget _buildScaleVisualization() {
    // Vind personen en bloem kolommen
    final originalPersonen = widget.data.kolommen
        .firstWhere((k) => k.label == 'origineel' && k.eenheid == 'personen');
    final newPersonen = widget.data.kolommen
        .firstWhere((k) => k.label == 'nieuw' && k.eenheid == 'personen');
    final originalBloem = widget.data.kolommen
        .firstWhere((k) => k.label.contains('origineel') && k.eenheid == 'gram');
    final newBloem = widget.data.kolommen
        .firstWhere((k) => k.label.contains('nieuw') && k.eenheid == 'gram');

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.orange.shade50,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.orange.shade200, width: 2),
      ),
      child: Column(
        children: [
          // Personen rij
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _buildPersonenBox(originalPersonen.waarde.toInt(), false),
              const SizedBox(width: 40),
              AnimatedArrow(
                operatie: '×${widget.data.factor}',
                color: Colors.orange,
              ),
              const SizedBox(width: 40),
              _buildPersonenBox(newPersonen.waarde.toInt(), true),
            ],
          ),
          const SizedBox(height: 32),

          // Bloem rij met animatie
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _buildBloemBox(originalBloem.waarde, false),
              const SizedBox(width: 40),
              AnimatedArrow(
                operatie: '×${widget.data.factor}',
                color: Colors.brown,
              ),
              const SizedBox(width: 40),
              _buildBloemBox(newBloem.waarde, true),
            ],
          ),

          if (_showResult) ...[
            const SizedBox(height: 24),
            _buildResultBanner(),
          ],
        ],
      ),
    );
  }

  Widget _buildPersonenBox(int aantal, bool isNew) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isNew ? Colors.orange.shade100 : Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: Colors.orange.shade400,
          width: isNew ? 3 : 2,
        ),
      ),
      child: Column(
        children: [
          Row(
            mainAxisSize: MainAxisSize.min,
            children: List.generate(
              aantal > 4 ? 4 : aantal,
              (index) => Padding(
                padding: const EdgeInsets.symmetric(horizontal: 4),
                child: Icon(
                  Icons.person,
                  size: 32,
                  color: Colors.orange.shade700,
                ),
              ),
            ),
          ),
          if (aantal > 4)
            Text(
              '+${aantal - 4} meer',
              style: TextStyle(
                fontSize: 12,
                color: Colors.orange.shade700,
              ),
            ),
          const SizedBox(height: 8),
          Text(
            '$aantal personen',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.orange.shade900,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBloemBox(num gram, bool isNew) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        final displayValue = !isNew || !_controller.isAnimating
            ? gram
            : (widget.data.kolommen[2].waarde +
                (gram - widget.data.kolommen[2].waarde) *
                    _scaleAnimation.value);

        return TweenAnimationBuilder<double>(
          duration: const Duration(milliseconds: 300),
          tween: Tween(begin: 1.0, end: isNew && _showResult ? 1.1 : 1.0),
          builder: (context, scale, child) {
            return Transform.scale(
              scale: scale,
              child: Container(
                width: 140,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: isNew && _showResult
                      ? Colors.green.shade100
                      : Colors.white,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(
                    color: isNew && _showResult
                        ? Colors.green.shade400
                        : Colors.brown.shade400,
                    width: isNew && _showResult ? 3 : 2,
                  ),
                  boxShadow: isNew && _showResult
                      ? [
                          BoxShadow(
                            color: Colors.green.withOpacity(0.3),
                            blurRadius: 12,
                            spreadRadius: 3,
                          )
                        ]
                      : [],
                ),
                child: Column(
                  children: [
                    Icon(
                      Icons.grain,
                      size: 40,
                      color: Colors.brown.shade700,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      '${displayValue.toStringAsFixed(0)} gram',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: isNew && _showResult
                            ? Colors.green.shade700
                            : Colors.brown.shade900,
                      ),
                    ),
                    Text(
                      'bloem',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey.shade600,
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        );
      },
    );
  }

  Widget _buildResultBanner() {
    return TweenAnimationBuilder<double>(
      duration: const Duration(milliseconds: 500),
      tween: Tween(begin: 0.0, end: 1.0),
      builder: (context, value, child) {
        return Opacity(
          opacity: value,
          child: Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.green.shade100,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.green.shade400, width: 2),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.check_circle, color: Colors.green.shade700, size: 32),
                const SizedBox(width: 12),
                Text(
                  'Perfect! Alle ingrediënten zijn opgeschaald!',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.green.shade900,
                  ),
                ),
              ],
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
        if (_controller.isCompleted)
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
        if (_controller.isCompleted) const SizedBox(width: 16),
        if (!_controller.isAnimating)
          ElevatedButton.icon(
            onPressed: _startAnimation,
            icon: const Icon(Icons.play_arrow),
            label: Text(_controller.isCompleted ? 'Nog een keer' : 'Start Animatie'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.orange.shade400,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            ),
          ),
      ],
    );
  }
}
