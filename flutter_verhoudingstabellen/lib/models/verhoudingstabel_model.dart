/// Data models voor verhoudingstabellen
/// Gebaseerd op de JSON structuur in verhaaltjessommen - Template.json

class VerhoudingstabelData {
  final String type;
  final dynamic data;

  VerhoudingstabelData({
    required this.type,
    required this.data,
  });

  factory VerhoudingstabelData.fromJson(Map<String, dynamic> json) {
    final type = json['type'] as String;

    switch (type) {
      case 'verhouding':
        return VerhoudingstabelData(
          type: type,
          data: VerhoudingData.fromJson(json),
        );
      case 'schaalfactor':
        return VerhoudingstabelData(
          type: type,
          data: ScaleFactorData.fromJson(json),
        );
      case 'schaal':
        return VerhoudingstabelData(
          type: type,
          data: ScaleMapData.fromJson(json),
        );
      case 'percentage_verdeling':
        return VerhoudingstabelData(
          type: type,
          data: PercentageDistributionData.fromJson(json),
        );
      default:
        throw Exception('Unknown verhoudingstabel type: $type');
    }
  }
}

/// Model voor verhoudingen (bv. melk:bloem 3:2)
class VerhoudingData {
  final String ratio;
  final List<String> labels;
  final List<VerhoudingKolom> kolommen;
  final List<Operatie> operaties;

  VerhoudingData({
    required this.ratio,
    required this.labels,
    required this.kolommen,
    required this.operaties,
  });

  factory VerhoudingData.fromJson(Map<String, dynamic> json) {
    return VerhoudingData(
      ratio: json['ratio'] as String,
      labels: List<String>.from(json['labels'] ?? []),
      kolommen: (json['kolommen'] as List)
          .map((k) => VerhoudingKolom.fromJson(k))
          .toList(),
      operaties: (json['operaties'] as List)
          .map((o) => Operatie.fromJson(o))
          .toList(),
    );
  }
}

class VerhoudingKolom {
  final num waarde;
  final String eenheid;
  final String label;
  final String rij;
  final String? berekening;

  VerhoudingKolom({
    required this.waarde,
    required this.eenheid,
    required this.label,
    required this.rij,
    this.berekening,
  });

  factory VerhoudingKolom.fromJson(Map<String, dynamic> json) {
    return VerhoudingKolom(
      waarde: json['waarde'] as num,
      eenheid: json['eenheid'] as String,
      label: json['label'] as String,
      rij: json['rij'] as String,
      berekening: json['berekening'] as String?,
    );
  }
}

class Operatie {
  final int van;
  final int naar;
  final String operatie;
  final String uitleg;

  Operatie({
    required this.van,
    required this.naar,
    required this.operatie,
    required this.uitleg,
  });

  factory Operatie.fromJson(Map<String, dynamic> json) {
    return Operatie(
      van: json['van'] as int,
      naar: json['naar'] as int,
      operatie: json['operatie'] as String,
      uitleg: json['uitleg'] as String,
    );
  }
}

/// Model voor schaalfactor (recepten opschalen)
class ScaleFactorData {
  final double factor;
  final List<ScaleKolom> kolommen;
  final List<SimpleOperatie> operaties;

  ScaleFactorData({
    required this.factor,
    required this.kolommen,
    required this.operaties,
  });

  factory ScaleFactorData.fromJson(Map<String, dynamic> json) {
    return ScaleFactorData(
      factor: (json['factor'] as num).toDouble(),
      kolommen: (json['kolommen'] as List)
          .map((k) => ScaleKolom.fromJson(k))
          .toList(),
      operaties: (json['operaties'] as List)
          .map((o) => SimpleOperatie.fromJson(o))
          .toList(),
    );
  }
}

class ScaleKolom {
  final num waarde;
  final String eenheid;
  final String label;
  final String? berekening;

  ScaleKolom({
    required this.waarde,
    required this.eenheid,
    required this.label,
    this.berekening,
  });

  factory ScaleKolom.fromJson(Map<String, dynamic> json) {
    return ScaleKolom(
      waarde: json['waarde'] as num,
      eenheid: json['eenheid'] as String,
      label: json['label'] as String,
      berekening: json['berekening'] as String?,
    );
  }
}

class SimpleOperatie {
  final int van;
  final int naar;
  final String operatie;
  final String uitleg;

  SimpleOperatie({
    required this.van,
    required this.naar,
    required this.operatie,
    required this.uitleg,
  });

  factory SimpleOperatie.fromJson(Map<String, dynamic> json) {
    return SimpleOperatie(
      van: json['van'] as int,
      naar: json['naar'] as int,
      operatie: json['operatie'] as String,
      uitleg: json['uitleg'] as String,
    );
  }
}

/// Model voor schaal (plattegrond/kaart)
class ScaleMapData {
  final String schaal;
  final List<ScaleKolom> kolommen;
  final List<SimpleOperatie> operaties;

  ScaleMapData({
    required this.schaal,
    required this.kolommen,
    required this.operaties,
  });

  factory ScaleMapData.fromJson(Map<String, dynamic> json) {
    return ScaleMapData(
      schaal: json['schaal'] as String,
      kolommen: (json['kolommen'] as List)
          .map((k) => ScaleKolom.fromJson(k))
          .toList(),
      operaties: (json['operaties'] as List)
          .map((o) => SimpleOperatie.fromJson(o))
          .toList(),
    );
  }
}

/// Model voor percentage verdeling
class PercentageDistributionData {
  final num totaal;
  final String eenheid;
  final List<Categorie> categorieën;

  PercentageDistributionData({
    required this.totaal,
    required this.eenheid,
    required this.categorieën,
  });

  factory PercentageDistributionData.fromJson(Map<String, dynamic> json) {
    return PercentageDistributionData(
      totaal: json['totaal'] as num,
      eenheid: json['eenheid'] as String,
      categorieën: (json['categorieën'] as List)
          .map((c) => Categorie.fromJson(c))
          .toList(),
    );
  }
}

class Categorie {
  final String label;
  final num percentage;
  final num aantal;
  final String berekening;

  Categorie({
    required this.label,
    required this.percentage,
    required this.aantal,
    required this.berekening,
  });

  factory Categorie.fromJson(Map<String, dynamic> json) {
    return Categorie(
      label: json['label'] as String,
      percentage: json['percentage'] as num,
      aantal: json['aantal'] as num,
      berekening: json['berekening'] as String,
    );
  }
}
