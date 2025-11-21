import 'dart:math' as math;
import 'package:flutter/material.dart';
import '../../models/verhoudingstabel_model.dart';

/// Widget voor percentage verdeling (bv. bibliotheek boeken)
/// Toont visueel hoe 100% verdeeld is over categorieën
class PercentageDistributionWidget extends StatefulWidget {
  final PercentageDistributionData data;

  const PercentageDistributionWidget({
    Key? key,
    required this.data,
  }) : super(key: key);

  @override
  State<PercentageDistributionWidget> createState() =>
      _PercentageDistributionWidgetState();
}

class _PercentageDistributionWidgetState
    extends State<PercentageDistributionWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  int? _selectedIndex;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    )..forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
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
            const SizedBox(height: 24),
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Pie chart
                Expanded(
                  flex: 2,
                  child: _buildPieChart(),
                ),
                const SizedBox(width: 32),
                // Legenda
                Expanded(
                  flex: 3,
                  child: _buildLegend(),
                ),
              ],
            ),
            const SizedBox(height: 24),
            _buildTotalBar(),
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
          colors: [Colors.teal.shade300, Colors.green.shade300],
        ),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.pie_chart, color: Colors.white, size: 28),
          const SizedBox(width: 12),
          Text(
            '${widget.data.totaal} ${widget.data.eenheid} Verdelen',
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

  Widget _buildPieChart() {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return AspectRatio(
          aspectRatio: 1,
          child: CustomPaint(
            painter: PieChartPainter(
              categorieën: widget.data.categorieën,
              animationValue: _controller.value,
              selectedIndex: _selectedIndex,
            ),
          ),
        );
      },
    );
  }

  Widget _buildLegend() {
    final colors = _getCategoryColors();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Verdeling:',
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: Colors.grey.shade800,
          ),
        ),
        const SizedBox(height: 16),
        ...List.generate(
          widget.data.categorieën.length,
          (index) {
            final cat = widget.data.categorieën[index];
            final isSelected = _selectedIndex == index;

            return Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: InkWell(
                onTap: () {
                  setState(() {
                    _selectedIndex = isSelected ? null : index;
                  });
                },
                borderRadius: BorderRadius.circular(12),
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 200),
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: isSelected
                        ? colors[index].withOpacity(0.2)
                        : Colors.grey.shade50,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: isSelected ? colors[index] : Colors.grey.shade300,
                      width: isSelected ? 3 : 1,
                    ),
                  ),
                  child: Row(
                    children: [
                      // Kleur indicator
                      Container(
                        width: 24,
                        height: 24,
                        decoration: BoxDecoration(
                          color: colors[index],
                          shape: BoxShape.circle,
                        ),
                      ),
                      const SizedBox(width: 12),
                      // Label en cijfers
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              cat.label.toUpperCase(),
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: colors[index],
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              '${cat.percentage}% = ${cat.aantal} ${widget.data.eenheid}',
                              style: TextStyle(
                                fontSize: 14,
                                color: Colors.grey.shade700,
                              ),
                            ),
                            if (isSelected) ...[
                              const SizedBox(height: 8),
                              Container(
                                padding: const EdgeInsets.all(8),
                                decoration: BoxDecoration(
                                  color: colors[index].withOpacity(0.1),
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Text(
                                  '📝 ${cat.berekening}',
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: colors[index].shade900,
                                    fontStyle: FontStyle.italic,
                                  ),
                                ),
                              ),
                            ],
                          ],
                        ),
                      ),
                      // Percentage badge
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 6,
                        ),
                        decoration: BoxDecoration(
                          color: colors[index],
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text(
                          '${cat.percentage}%',
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            );
          },
        ),
      ],
    );
  }

  Widget _buildTotalBar() {
    final colors = _getCategoryColors();

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.grey.shade100,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade300, width: 2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Totaal = 100%',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Colors.grey.shade800,
            ),
          ),
          const SizedBox(height: 12),
          // Gestapelde balk
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: SizedBox(
              height: 40,
              child: AnimatedBuilder(
                animation: _controller,
                builder: (context, child) {
                  return Row(
                    children: List.generate(
                      widget.data.categorieën.length,
                      (index) {
                        final cat = widget.data.categorieën[index];
                        return Expanded(
                          flex: (cat.percentage * _controller.value).toInt(),
                          child: Container(
                            color: colors[index],
                            child: Center(
                              child: Text(
                                _controller.value > 0.8
                                    ? '${cat.percentage}%'
                                    : '',
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                  );
                },
              ),
            ),
          ),
          const SizedBox(height: 12),
          // Som onder de balk
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ...List.generate(
                widget.data.categorieën.length * 2 - 1,
                (i) {
                  if (i.isEven) {
                    final cat = widget.data.categorieën[i ~/ 2];
                    return Text(
                      '${cat.aantal}',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: colors[i ~/ 2],
                      ),
                    );
                  } else {
                    return Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 8),
                      child: Text(
                        '+',
                        style: TextStyle(
                          fontSize: 16,
                          color: Colors.grey.shade600,
                        ),
                      ),
                    );
                  }
                },
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 8),
                child: Text(
                  '=',
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.grey.shade600,
                  ),
                ),
              ),
              Text(
                '${widget.data.totaal} ${widget.data.eenheid}',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.green.shade700,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  List<Color> _getCategoryColors() {
    return [
      Colors.blue.shade400,
      Colors.purple.shade400,
      Colors.orange.shade400,
      Colors.green.shade400,
      Colors.red.shade400,
    ];
  }
}

/// Custom painter voor de pie chart
class PieChartPainter extends CustomPainter {
  final List<Categorie> categorieën;
  final double animationValue;
  final int? selectedIndex;

  PieChartPainter({
    required this.categorieën,
    required this.animationValue,
    this.selectedIndex,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = math.min(size.width, size.height) / 2 * 0.8;

    final colors = [
      Colors.blue.shade400,
      Colors.purple.shade400,
      Colors.orange.shade400,
      Colors.green.shade400,
      Colors.red.shade400,
    ];

    double startAngle = -math.pi / 2; // Start bovenaan

    for (int i = 0; i < categorieën.length; i++) {
      final cat = categorieën[i];
      final sweepAngle =
          (cat.percentage / 100) * 2 * math.pi * animationValue;
      final isSelected = selectedIndex == i;

      final paint = Paint()
        ..color = colors[i]
        ..style = PaintingStyle.fill;

      // Teken segment
      final segmentCenter = Offset(
        center.dx + (isSelected ? 10 : 0) * math.cos(startAngle + sweepAngle / 2),
        center.dy + (isSelected ? 10 : 0) * math.sin(startAngle + sweepAngle / 2),
      );

      canvas.drawArc(
        Rect.fromCircle(
          center: segmentCenter,
          radius: isSelected ? radius * 1.1 : radius,
        ),
        startAngle,
        sweepAngle,
        true,
        paint,
      );

      // Teken witte lijn tussen segmenten
      if (animationValue > 0.5) {
        final linePaint = Paint()
          ..color = Colors.white
          ..strokeWidth = 3
          ..style = PaintingStyle.stroke;

        canvas.drawLine(
          center,
          Offset(
            center.dx + radius * math.cos(startAngle),
            center.dy + radius * math.sin(startAngle),
          ),
          linePaint,
        );
      }

      startAngle += sweepAngle;
    }

    // Wit centrum cirkel
    canvas.drawCircle(
      center,
      radius * 0.4,
      Paint()..color = Colors.white,
    );

    // Totaal in centrum
    if (animationValue > 0.8) {
      final textPainter = TextPainter(
        text: TextSpan(
          text: '100%',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.grey.shade800,
          ),
        ),
        textDirection: TextDirection.ltr,
      );
      textPainter.layout();
      textPainter.paint(
        canvas,
        Offset(
          center.dx - textPainter.width / 2,
          center.dy - textPainter.height / 2,
        ),
      );
    }
  }

  @override
  bool shouldRepaint(PieChartPainter oldDelegate) {
    return oldDelegate.animationValue != animationValue ||
        oldDelegate.selectedIndex != selectedIndex;
  }
}
