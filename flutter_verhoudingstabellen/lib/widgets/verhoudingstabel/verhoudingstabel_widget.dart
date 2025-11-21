import 'package:flutter/material.dart';
import '../../models/verhoudingstabel_model.dart';
import 'ratio_table_widget.dart';
import 'scale_factor_widget.dart';
import 'percentage_distribution_widget.dart';

/// Main widget die automatisch het juiste type verhoudingstabel kiest
class VerhoudingstabelWidget extends StatelessWidget {
  final Map<String, dynamic> verhoudingstabelJson;

  const VerhoudingstabelWidget({
    Key? key,
    required this.verhoudingstabelJson,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    try {
      final data = VerhoudingstabelData.fromJson(verhoudingstabelJson);

      switch (data.type) {
        case 'verhouding':
          return RatioTableWidget(data: data.data as VerhoudingData);

        case 'schaalfactor':
          return ScaleFactorWidget(data: data.data as ScaleFactorData);

        case 'schaal':
          // Voor nu gebruiken we dezelfde widget als schaalfactor
          // In de toekomst kunnen we een specifieke ScaleMapWidget maken
          return ScaleFactorWidget(
            data: ScaleFactorData(
              factor: _extractScaleFactor(data.data as ScaleMapData),
              kolommen: (data.data as ScaleMapData).kolommen,
              operaties: (data.data as ScaleMapData).operaties,
            ),
          );

        case 'percentage_verdeling':
          return PercentageDistributionWidget(
            data: data.data as PercentageDistributionData,
          );

        default:
          return _buildErrorWidget('Unknown type: ${data.type}');
      }
    } catch (e) {
      return _buildErrorWidget('Error loading verhoudingstabel: $e');
    }
  }

  double _extractScaleFactor(ScaleMapData data) {
    // Extract factor from schaal like "1:300" -> 300
    final parts = data.schaal.split(':');
    if (parts.length == 2) {
      return double.tryParse(parts[1]) ?? 1.0;
    }
    return 1.0;
  }

  Widget _buildErrorWidget(String message) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.red.shade50,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.red.shade300, width: 2),
      ),
      child: Row(
        children: [
          Icon(Icons.error_outline, color: Colors.red.shade700, size: 32),
          const SizedBox(width: 16),
          Expanded(
            child: Text(
              message,
              style: TextStyle(
                fontSize: 16,
                color: Colors.red.shade900,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
