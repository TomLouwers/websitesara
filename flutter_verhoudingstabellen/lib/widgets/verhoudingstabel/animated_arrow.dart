import 'package:flutter/material.dart';

/// Geanimeerde pijl om bewerkingen te tonen
class AnimatedArrow extends StatefulWidget {
  final String operatie;
  final bool isVertical;
  final Color color;
  final Duration animationDelay;

  const AnimatedArrow({
    Key? key,
    required this.operatie,
    this.isVertical = false,
    this.color = Colors.blue,
    this.animationDelay = Duration.zero,
  }) : super(key: key);

  @override
  State<AnimatedArrow> createState() => _AnimatedArrowState();
}

class _AnimatedArrowState extends State<AnimatedArrow>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  late Animation<double> _opacityAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    );

    _scaleAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeOutBack),
    );

    _opacityAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeIn),
    );

    // Start animatie met delay
    Future.delayed(widget.animationDelay, () {
      if (mounted) {
        _controller.forward();
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Opacity(
          opacity: _opacityAnimation.value,
          child: Transform.scale(
            scale: _scaleAnimation.value,
            child: widget.isVertical
                ? _buildVerticalArrow()
                : _buildHorizontalArrow(),
          ),
        );
      },
    );
  }

  Widget _buildHorizontalArrow() {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(
          widget.operatie,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: widget.color,
          ),
        ),
        const SizedBox(height: 4),
        Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 40,
              height: 3,
              color: widget.color,
            ),
            CustomPaint(
              size: const Size(12, 12),
              painter: ArrowHeadPainter(color: widget.color),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildVerticalArrow() {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(
          widget.operatie,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: widget.color,
          ),
        ),
        const SizedBox(width: 8),
        Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 3,
              height: 30,
              color: widget.color,
            ),
            CustomPaint(
              size: const Size(12, 12),
              painter: ArrowHeadPainter(
                color: widget.color,
                isVertical: true,
              ),
            ),
          ],
        ),
      ],
    );
  }
}

/// Custom painter voor pijlpunt
class ArrowHeadPainter extends CustomPainter {
  final Color color;
  final bool isVertical;

  ArrowHeadPainter({
    required this.color,
    this.isVertical = false,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;

    final path = Path();

    if (isVertical) {
      // Pijl naar beneden
      path.moveTo(size.width / 2, size.height);
      path.lineTo(0, 0);
      path.lineTo(size.width, 0);
    } else {
      // Pijl naar rechts
      path.moveTo(size.width, size.height / 2);
      path.lineTo(0, 0);
      path.lineTo(0, size.height);
    }

    path.close();
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}
