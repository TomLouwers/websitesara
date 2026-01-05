#!/usr/bin/env python3
"""
Comprehensive Exercise Validation System
=========================================

Validates exercises against quality standards for:
- Schema compliance (v2.0.0)
- Content quality (readability, spelling, grammar)
- Answer correctness
- Hint & feedback quality
- SLO alignment completeness

Usage:
    python scripts/comprehensive_validation.py --all
    python scripts/comprehensive_validation.py --category bl
    python scripts/comprehensive_validation.py --file data-v2/exercises/gb/gb_groep4_m4_core.json
    python scripts/comprehensive_validation.py --all --report validation-report.html
"""

import json
import os
import sys
import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

# Try to import optional dependencies
try:
    import textstat
    HAS_TEXTSTAT = True
except ImportError:
    HAS_TEXTSTAT = False
    print("⚠️  textstat not installed. Install with: pip install textstat")
    print("   Readability checks will be skipped.\n")


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "critical"  # Blocks publishing
    ERROR = "error"        # Should be fixed before publishing
    WARNING = "warning"    # Review recommended
    INFO = "info"          # Nice to have


@dataclass
class ValidationIssue:
    """Represents a validation issue"""
    severity: Severity
    category: str  # e.g., "schema", "readability", "answer", "hint"
    message: str
    location: str  # e.g., "item 5", "metadata"
    suggestion: str = ""

    def __str__(self):
        severity_emoji = {
            Severity.CRITICAL: "🔴",
            Severity.ERROR: "🟠",
            Severity.WARNING: "🟡",
            Severity.INFO: "🔵"
        }
        emoji = severity_emoji.get(self.severity, "")
        msg = f"{emoji} [{self.severity.value.upper()}] {self.category}: {self.message}"
        if self.location:
            msg += f" (at {self.location})"
        if self.suggestion:
            msg += f"\n   💡 Suggestion: {self.suggestion}"
        return msg


@dataclass
class ValidationResult:
    """Results of validating a single exercise file"""
    file_path: str
    exercise_id: str
    passed: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    quality_score: float = 0.0

    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.CRITICAL)

    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.ERROR)

    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)


class ExerciseValidator:
    """Validates exercise files against quality standards"""

    # Grade-level readability thresholds (Flesch Reading Ease for Dutch)
    READABILITY_THRESHOLDS = {
        3: 80,  # Very easy
        4: 75,  # Easy
        5: 70,  # Fairly easy
        6: 65,  # Standard
        7: 60,  # Fairly difficult
        8: 55,  # Difficult
    }

    def __init__(self, strict_mode: bool = False):
        """
        Args:
            strict_mode: If True, warnings become errors
        """
        self.strict_mode = strict_mode

    def validate_file(self, core_path: str, support_path: str = None) -> ValidationResult:
        """
        Validate an exercise file (core + optional support)

        Args:
            core_path: Path to core JSON file
            support_path: Optional path to support JSON file

        Returns:
            ValidationResult with all issues found
        """
        issues = []

        # Load core file
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
        except FileNotFoundError:
            return ValidationResult(
                file_path=core_path,
                exercise_id="unknown",
                passed=False,
                issues=[ValidationIssue(
                    Severity.CRITICAL,
                    "file",
                    f"File not found: {core_path}",
                    ""
                )]
            )
        except json.JSONDecodeError as e:
            return ValidationResult(
                file_path=core_path,
                exercise_id="unknown",
                passed=False,
                issues=[ValidationIssue(
                    Severity.CRITICAL,
                    "json",
                    f"Invalid JSON: {e}",
                    ""
                )]
            )

        # Load support file if specified
        support_data = None
        if support_path and os.path.exists(support_path):
            try:
                with open(support_path, 'r', encoding='utf-8') as f:
                    support_data = json.load(f)
            except json.JSONDecodeError as e:
                issues.append(ValidationIssue(
                    Severity.ERROR,
                    "json",
                    f"Invalid support JSON: {e}",
                    "support file"
                ))

        exercise_id = core_data.get('metadata', {}).get('id', 'unknown')

        # Run all validation checks
        issues.extend(self._validate_schema(core_data, "core"))
        if support_data:
            issues.extend(self._validate_schema(support_data, "support"))

        issues.extend(self._validate_metadata(core_data))
        issues.extend(self._validate_items(core_data, support_data))

        # Calculate quality score
        quality_score = self._calculate_quality_score(core_data, support_data, issues)

        # Determine if passed (no critical issues)
        passed = not any(i.severity == Severity.CRITICAL for i in issues)
        if self.strict_mode:
            passed = passed and not any(i.severity == Severity.ERROR for i in issues)

        return ValidationResult(
            file_path=core_path,
            exercise_id=exercise_id,
            passed=passed,
            issues=issues,
            quality_score=quality_score
        )

    def _validate_schema(self, data: Dict, file_type: str) -> List[ValidationIssue]:
        """Validate schema version and basic structure"""
        issues = []

        # Check schema version
        if 'schema_version' not in data:
            issues.append(ValidationIssue(
                Severity.CRITICAL,
                "schema",
                "Missing schema_version",
                file_type
            ))
        elif data['schema_version'] != "2.0.0":
            issues.append(ValidationIssue(
                Severity.WARNING,
                "schema",
                f"Schema version is {data['schema_version']}, expected 2.0.0",
                file_type
            ))

        # Check required top-level fields for core
        if file_type == "core":
            if 'metadata' not in data:
                issues.append(ValidationIssue(
                    Severity.CRITICAL,
                    "schema",
                    "Missing metadata object",
                    file_type
                ))

            # Check for items/exercises/problems array
            has_content = any(k in data for k in ['items', 'exercises', 'problems'])
            if not has_content:
                issues.append(ValidationIssue(
                    Severity.CRITICAL,
                    "schema",
                    "Missing items, exercises, or problems array",
                    file_type
                ))

        # Check required fields for support
        elif file_type == "support":
            if 'exercise_id' not in data:
                issues.append(ValidationIssue(
                    Severity.ERROR,
                    "schema",
                    "Missing exercise_id in support file",
                    file_type
                ))

        return issues

    def _validate_metadata(self, core_data: Dict) -> List[ValidationIssue]:
        """Validate metadata completeness and quality"""
        issues = []
        metadata = core_data.get('metadata', {})

        # Required metadata fields
        required_fields = ['id', 'type', 'category', 'language']
        for field in required_fields:
            if field not in metadata:
                issues.append(ValidationIssue(
                    Severity.ERROR,
                    "metadata",
                    f"Missing required field: {field}",
                    "metadata"
                ))

        # Check grade (either grade or grade_levels)
        if 'grade' not in metadata and 'grade_levels' not in metadata:
            issues.append(ValidationIssue(
                Severity.ERROR,
                "metadata",
                "Missing grade or grade_levels",
                "metadata"
            ))

        # Validate grade range
        grade = metadata.get('grade')
        if grade and (grade < 3 or grade > 8):
            issues.append(ValidationIssue(
                Severity.WARNING,
                "metadata",
                f"Grade {grade} outside normal range (3-8)",
                "metadata.grade"
            ))

        # Check SLO alignment (recommended)
        if 'slo_alignment' not in metadata:
            issues.append(ValidationIssue(
                Severity.WARNING,
                "metadata",
                "Missing SLO alignment - recommended for curriculum mapping",
                "metadata",
                "Add slo_alignment with kerndoelen, rekendomeinen, referentieniveau"
            ))
        else:
            slo = metadata['slo_alignment']
            # Check for basic SLO fields
            if 'referentieniveau' not in slo:
                issues.append(ValidationIssue(
                    Severity.INFO,
                    "metadata",
                    "Missing referentieniveau in SLO alignment",
                    "metadata.slo_alignment"
                ))

        return issues

    def _validate_items(self, core_data: Dict, support_data: Dict = None) -> List[ValidationIssue]:
        """Validate individual items/questions"""
        issues = []

        # Get items from various structures
        items = self._extract_items(core_data)
        support_items = self._extract_items(support_data) if support_data else {}

        if not items:
            issues.append(ValidationIssue(
                Severity.CRITICAL,
                "content",
                "No items found in exercise",
                "items"
            ))
            return issues

        grade = core_data.get('metadata', {}).get('grade', 5)
        category = core_data.get('metadata', {}).get('category', '')

        for idx, (item_id, item) in enumerate(items.items(), 1):
            item_location = f"item {idx} (id: {item_id})"

            # Validate item structure
            issues.extend(self._validate_item_structure(item, item_location))

            # Validate question text
            question_text = item.get('question', {}).get('text', '')
            if question_text:
                issues.extend(self._validate_text_quality(
                    question_text,
                    grade,
                    f"{item_location}.question"
                ))

            # Validate options for multiple choice
            if item.get('type') == 'multiple_choice' or not item.get('type'):
                issues.extend(self._validate_multiple_choice(item, item_location))

            # Validate answer
            issues.extend(self._validate_answer(item, item_location))

            # Validate support data if available
            support_item = support_items.get(item_id)
            if support_item:
                issues.extend(self._validate_support_item(support_item, item_location))
            else:
                issues.append(ValidationIssue(
                    Severity.INFO,
                    "support",
                    "No support data found for this item",
                    item_location,
                    "Add hints, feedback, and learning strategies"
                ))

        return issues

    def _validate_item_structure(self, item: Dict, location: str) -> List[ValidationIssue]:
        """Validate basic item structure"""
        issues = []

        if 'id' not in item and 'item_id' not in item:
            issues.append(ValidationIssue(
                Severity.ERROR,
                "schema",
                "Item missing id",
                location
            ))

        if 'question' not in item:
            issues.append(ValidationIssue(
                Severity.CRITICAL,
                "schema",
                "Item missing question",
                location
            ))
        elif not item['question'].get('text'):
            issues.append(ValidationIssue(
                Severity.CRITICAL,
                "content",
                "Question text is empty",
                location
            ))

        if 'answer' not in item:
            issues.append(ValidationIssue(
                Severity.CRITICAL,
                "schema",
                "Item missing answer",
                location
            ))

        return issues

    def _validate_multiple_choice(self, item: Dict, location: str) -> List[ValidationIssue]:
        """Validate multiple choice specific fields"""
        issues = []

        options = item.get('options', [])
        if not options:
            issues.append(ValidationIssue(
                Severity.CRITICAL,
                "content",
                "Multiple choice item has no options",
                location
            ))
            return issues

        if len(options) < 2:
            issues.append(ValidationIssue(
                Severity.CRITICAL,
                "content",
                "Multiple choice must have at least 2 options",
                location
            ))

        if len(options) > 6:
            issues.append(ValidationIssue(
                Severity.WARNING,
                "pedagogy",
                f"Too many options ({len(options)}). 4 is optimal for this age group.",
                location
            ))

        # Check that all options have text
        for opt_idx, option in enumerate(options):
            if not option.get('text'):
                issues.append(ValidationIssue(
                    Severity.ERROR,
                    "content",
                    f"Option {opt_idx} is missing text",
                    location
                ))

        # Check for duplicate options
        option_texts = []
        for opt in options:
            text = opt.get('text', '')
            # Handle cases where text might be a dict or other non-string type
            if isinstance(text, dict):
                text = str(text)  # Convert to string for comparison
            elif not isinstance(text, str):
                text = str(text) if text is not None else ''
            option_texts.append(text.strip().lower())

        if len(option_texts) != len(set(option_texts)):
            issues.append(ValidationIssue(
                Severity.ERROR,
                "content",
                "Duplicate answer options found",
                location
            ))

        return issues

    def _validate_answer(self, item: Dict, location: str) -> List[ValidationIssue]:
        """Validate answer correctness"""
        issues = []

        answer = item.get('answer', {})
        options = item.get('options', [])

        # For multiple choice, validate correct_index
        if options and 'correct_index' in answer:
            correct_idx = answer['correct_index']
            if not isinstance(correct_idx, int):
                issues.append(ValidationIssue(
                    Severity.CRITICAL,
                    "answer",
                    f"correct_index must be integer, got {type(correct_idx)}",
                    location
                ))
            elif correct_idx < 0 or correct_idx >= len(options):
                issues.append(ValidationIssue(
                    Severity.CRITICAL,
                    "answer",
                    f"correct_index {correct_idx} out of range (0-{len(options)-1})",
                    location
                ))

        return issues

    def _validate_text_quality(self, text: str, grade: int, location: str) -> List[ValidationIssue]:
        """Validate text readability and quality"""
        issues = []

        # Check text length
        if len(text.strip()) < 5:
            issues.append(ValidationIssue(
                Severity.WARNING,
                "content",
                "Text is very short (< 5 characters)",
                location
            ))

        # Check for placeholder text
        placeholders = ['TODO', 'XXX', 'FIXME', '[...]', '???']
        if any(p in text for p in placeholders):
            issues.append(ValidationIssue(
                Severity.ERROR,
                "content",
                "Text contains placeholder markers",
                location
            ))

        # Readability check (if textstat available)
        if HAS_TEXTSTAT and len(text.split()) >= 3:
            # Use Flesch Reading Ease (higher = easier)
            # Note: textstat has Dutch support with textstat.set_lang('nl')
            try:
                textstat.set_lang('nl')
                reading_ease = textstat.flesch_reading_ease(text)
                threshold = self.READABILITY_THRESHOLDS.get(grade, 60)

                if reading_ease < threshold - 15:  # More than 15 points below target
                    issues.append(ValidationIssue(
                        Severity.WARNING,
                        "readability",
                        f"Text may be too difficult for grade {grade} (score: {reading_ease:.1f}, target: >{threshold})",
                        location,
                        "Consider simplifying vocabulary or sentence structure"
                    ))
            except Exception as e:
                # Readability check failed, skip silently
                pass

        return issues

    def _validate_support_item(self, support_item: Dict, location: str) -> List[ValidationIssue]:
        """Validate support/feedback data quality"""
        issues = []

        # Check for hints
        hints = support_item.get('hints', [])
        if isinstance(support_item.get('hint'), str):
            hints = [support_item['hint']]  # Old format

        if not hints:
            issues.append(ValidationIssue(
                Severity.INFO,
                "hint",
                "No hints provided",
                location,
                "Add at least 1-2 progressive hints"
            ))
        elif len(hints) == 1:
            issues.append(ValidationIssue(
                Severity.INFO,
                "hint",
                "Only 1 hint provided. Consider adding 2-3 progressive hints",
                location
            ))
        elif len(hints) >= 3:
            # Good! Check hint quality
            for h_idx, hint in enumerate(hints[:3]):
                hint_text = hint.get('text', hint) if isinstance(hint, dict) else hint
                if len(hint_text.strip()) < 10:
                    issues.append(ValidationIssue(
                        Severity.WARNING,
                        "hint",
                        f"Hint {h_idx + 1} is very short",
                        f"{location}.hints[{h_idx}]"
                    ))

        # Check for feedback
        feedback = support_item.get('feedback', {})
        if not feedback:
            issues.append(ValidationIssue(
                Severity.WARNING,
                "feedback",
                "No feedback provided",
                location,
                "Add correct/incorrect feedback messages"
            ))
        else:
            # Check for per-option feedback
            if 'per_option' not in feedback:
                issues.append(ValidationIssue(
                    Severity.INFO,
                    "feedback",
                    "No per-option feedback. Consider adding specific feedback for each wrong answer",
                    location
                ))

        # Check for learning metadata
        learning = support_item.get('learning', {})
        if not learning:
            issues.append(ValidationIssue(
                Severity.INFO,
                "pedagogy",
                "No learning metadata (strategies, common errors)",
                location
            ))
        else:
            if 'reading_strategies' not in learning and 'math_strategies' not in learning:
                issues.append(ValidationIssue(
                    Severity.INFO,
                    "pedagogy",
                    "No learning strategies specified",
                    location
                ))

        return issues

    def _extract_items(self, data: Dict) -> Dict[Any, Dict]:
        """Extract items from various data structures, return dict keyed by item_id"""
        if not data:
            return {}

        items = {}

        # Simple structure: items[]
        if 'items' in data:
            for item in data['items']:
                item_id = item.get('id') or item.get('item_id')
                if item_id:
                    items[item_id] = item

        # BL structure: exercises[].items[]
        elif 'exercises' in data:
            for exercise in data['exercises']:
                for item in exercise.get('items', []):
                    item_id = item.get('id') or item.get('item_id')
                    if item_id:
                        items[item_id] = item

        # VS structure: problems[].items[]
        elif 'problems' in data:
            for problem in data['problems']:
                for item in problem.get('items', []):
                    item_id = item.get('id') or item.get('item_id')
                    if item_id:
                        items[item_id] = item

        return items

    def _calculate_quality_score(self, core_data: Dict, support_data: Dict,
                                 issues: List[ValidationIssue]) -> float:
        """
        Calculate quality score (0-100)

        Based on:
        - Absence of critical/error issues (40%)
        - Presence of quality features (60%)
          - Progressive hints (20%)
          - Per-option feedback (20%)
          - Learning strategies (10%)
          - SLO alignment (10%)
        """
        score = 100.0

        # Deduct for issues
        for issue in issues:
            if issue.severity == Severity.CRITICAL:
                score -= 20
            elif issue.severity == Severity.ERROR:
                score -= 10
            elif issue.severity == Severity.WARNING:
                score -= 2

        # Bonus for quality features
        items = self._extract_items(core_data)
        support_items = self._extract_items(support_data) if support_data else {}

        if items:
            total_items = len(items)
            items_with_hints = 0
            items_with_progressive_hints = 0
            items_with_per_option_feedback = 0
            items_with_strategies = 0

            for item_id, item in items.items():
                support_item = support_items.get(item_id, {})

                # Count hints
                hints = support_item.get('hints', [])
                if hints:
                    items_with_hints += 1
                if len(hints) >= 3:
                    items_with_progressive_hints += 1

                # Count per-option feedback
                if support_item.get('feedback', {}).get('per_option'):
                    items_with_per_option_feedback += 1

                # Count learning strategies
                learning = support_item.get('learning', {})
                if learning.get('reading_strategies') or learning.get('math_strategies'):
                    items_with_strategies += 1

            # Quality bonuses (percentage of items with feature × weight)
            score += (items_with_progressive_hints / total_items) * 20
            score += (items_with_per_option_feedback / total_items) * 20
            score += (items_with_strategies / total_items) * 10

        # SLO alignment bonus
        if core_data.get('metadata', {}).get('slo_alignment'):
            score += 10

        return max(0.0, min(100.0, score))


def validate_directory(directory: str, validator: ExerciseValidator) -> List[ValidationResult]:
    """Validate all exercises in a directory"""
    results = []
    directory_path = Path(directory)

    if not directory_path.exists():
        print(f"❌ Directory not found: {directory}")
        return results

    # Find all core files
    core_files = list(directory_path.glob("**/*_core.json"))

    print(f"Found {len(core_files)} exercise files in {directory}\n")

    for core_path in sorted(core_files):
        # Find corresponding support file
        support_path = core_path.parent / core_path.name.replace('_core.json', '_support.json')

        result = validator.validate_file(
            str(core_path),
            str(support_path) if support_path.exists() else None
        )
        results.append(result)

    return results


def print_summary(results: List[ValidationResult]):
    """Print validation summary"""
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed

    total_critical = sum(r.critical_count() for r in results)
    total_errors = sum(r.error_count() for r in results)
    total_warnings = sum(r.warning_count() for r in results)

    avg_quality = sum(r.quality_score for r in results) / total if total > 0 else 0

    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Total exercises:     {total}")
    print(f"Passed:              {passed} ✅")
    print(f"Failed:              {failed} ❌")
    print(f"\nIssue counts:")
    print(f"  Critical:          {total_critical} 🔴")
    print(f"  Errors:            {total_errors} 🟠")
    print(f"  Warnings:          {total_warnings} 🟡")
    print(f"\nAverage quality score: {avg_quality:.1f}%")
    print("=" * 80)


def generate_html_report(results: List[ValidationResult], output_path: str):
    """Generate HTML validation report"""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Exercise Validation Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
               padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px;
                    border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        .summary { background: #f8f9fa; padding: 20px; border-radius: 6px; margin: 20px 0; }
        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                       gap: 15px; margin-top: 15px; }
        .summary-card { background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #007bff; }
        .summary-card.passed { border-left-color: #28a745; }
        .summary-card.failed { border-left-color: #dc3545; }
        .summary-card h3 { margin: 0 0 10px 0; font-size: 14px; color: #666; }
        .summary-card .value { font-size: 28px; font-weight: bold; color: #333; }

        .exercise { border: 1px solid #dee2e6; border-radius: 6px; margin: 15px 0; overflow: hidden; }
        .exercise-header { background: #f8f9fa; padding: 15px; cursor: pointer; }
        .exercise-header:hover { background: #e9ecef; }
        .exercise-header.passed { border-left: 4px solid #28a745; }
        .exercise-header.failed { border-left: 4px solid #dc3545; }
        .exercise-id { font-weight: bold; font-size: 16px; }
        .quality-score { float: right; font-weight: bold; }
        .quality-high { color: #28a745; }
        .quality-medium { color: #ffc107; }
        .quality-low { color: #dc3545; }

        .exercise-body { padding: 15px; background: white; }
        .issue { padding: 10px; margin: 8px 0; border-radius: 4px; border-left: 4px solid; }
        .issue.critical { background: #f8d7da; border-left-color: #dc3545; }
        .issue.error { background: #fff3cd; border-left-color: #ffc107; }
        .issue.warning { background: #fff8e1; border-left-color: #ff9800; }
        .issue.info { background: #e7f3ff; border-left-color: #2196f3; }
        .issue-header { font-weight: bold; margin-bottom: 5px; }
        .issue-location { color: #666; font-size: 14px; }
        .issue-suggestion { margin-top: 8px; padding: 8px; background: rgba(255,255,255,0.5);
                          border-radius: 4px; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Exercise Validation Report</h1>
"""

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    total_critical = sum(r.critical_count() for r in results)
    total_errors = sum(r.error_count() for r in results)
    total_warnings = sum(r.warning_count() for r in results)
    avg_quality = sum(r.quality_score for r in results) / total if total > 0 else 0

    html += f"""
        <div class="summary">
            <h2>Summary</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <h3>Total Exercises</h3>
                    <div class="value">{total}</div>
                </div>
                <div class="summary-card passed">
                    <h3>Passed ✅</h3>
                    <div class="value">{passed}</div>
                </div>
                <div class="summary-card failed">
                    <h3>Failed ❌</h3>
                    <div class="value">{failed}</div>
                </div>
                <div class="summary-card">
                    <h3>Avg Quality</h3>
                    <div class="value">{avg_quality:.1f}%</div>
                </div>
                <div class="summary-card">
                    <h3>Critical 🔴</h3>
                    <div class="value">{total_critical}</div>
                </div>
                <div class="summary-card">
                    <h3>Errors 🟠</h3>
                    <div class="value">{total_errors}</div>
                </div>
                <div class="summary-card">
                    <h3>Warnings 🟡</h3>
                    <div class="value">{total_warnings}</div>
                </div>
            </div>
        </div>

        <h2>Exercise Details</h2>
"""

    # Individual exercises
    for result in sorted(results, key=lambda r: r.quality_score):
        status_class = "passed" if result.passed else "failed"
        quality_class = "quality-high" if result.quality_score >= 70 else "quality-medium" if result.quality_score >= 40 else "quality-low"

        html += f"""
        <div class="exercise">
            <div class="exercise-header {status_class}">
                <span class="exercise-id">{result.exercise_id}</span>
                <span class="quality-score {quality_class}">{result.quality_score:.1f}%</span>
                <div style="clear:both; font-size: 12px; color: #666; margin-top: 5px;">
                    {result.file_path}
                </div>
            </div>
"""

        if result.issues:
            html += '<div class="exercise-body">'
            for issue in result.issues:
                html += f"""
                <div class="issue {issue.severity.value}">
                    <div class="issue-header">{issue.category.upper()}: {issue.message}</div>
                    <div class="issue-location">Location: {issue.location}</div>
"""
                if issue.suggestion:
                    html += f'<div class="issue-suggestion">💡 {issue.suggestion}</div>'
                html += '</div>'
            html += '</div>'

        html += '</div>'

    html += """
    </div>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n📄 HTML report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Comprehensive exercise validation')
    parser.add_argument('--all', action='store_true', help='Validate all exercises in data-v2/exercises/')
    parser.add_argument('--category', help='Validate specific category (e.g., bl, gb, sp)')
    parser.add_argument('--file', help='Validate single file')
    parser.add_argument('--directory', help='Validate all files in directory')
    parser.add_argument('--report', help='Generate HTML report (specify output path)')
    parser.add_argument('--strict', action='store_true', help='Strict mode: warnings become errors')

    args = parser.parse_args()

    validator = ExerciseValidator(strict_mode=args.strict)
    results = []

    if args.file:
        # Validate single file
        support_path = args.file.replace('_core.json', '_support.json')
        result = validator.validate_file(args.file, support_path if os.path.exists(support_path) else None)
        results = [result]

        # Print issues
        if result.issues:
            print(f"\n{result.exercise_id} ({result.quality_score:.1f}% quality):")
            for issue in result.issues:
                print(f"  {issue}")
        else:
            print(f"\n✅ {result.exercise_id}: No issues found! Quality: {result.quality_score:.1f}%")

    elif args.category:
        # Validate category
        directory = f"data-v2/exercises/{args.category}"
        results = validate_directory(directory, validator)

    elif args.directory:
        # Validate directory
        results = validate_directory(args.directory, validator)

    elif args.all:
        # Validate all
        base_dir = Path("data-v2/exercises")
        if not base_dir.exists():
            print("❌ data-v2/exercises/ directory not found")
            return 1

        categories = [d for d in base_dir.iterdir() if d.is_dir()]
        for category_dir in sorted(categories):
            print(f"\n📁 Validating {category_dir.name}...")
            results.extend(validate_directory(str(category_dir), validator))

    else:
        parser.print_help()
        return 1

    # Print summary
    if results:
        print_summary(results)

        # Show failed exercises
        failed = [r for r in results if not r.passed]
        if failed:
            print(f"\n❌ Failed exercises ({len(failed)}):")
            for result in failed[:10]:  # Show first 10
                print(f"\n  {result.exercise_id} ({result.quality_score:.1f}%):")
                critical = [i for i in result.issues if i.severity == Severity.CRITICAL]
                for issue in critical[:3]:  # Show first 3 critical
                    print(f"    {issue}")
            if len(failed) > 10:
                print(f"\n  ... and {len(failed) - 10} more")

        # Generate HTML report if requested
        if args.report:
            generate_html_report(results, args.report)

        # Exit code
        return 0 if all(r.passed for r in results) else 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
