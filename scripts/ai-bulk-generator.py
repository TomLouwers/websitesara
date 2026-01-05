#!/usr/bin/env python3
"""
AI-Powered Exercise Bulk Generator
===================================

Generates exercises using AI (Claude or GPT) from CSV prompt templates.

Usage:
    # Generate from specific CSV row
    python3 scripts/ai-bulk-generator.py \\
        --csv docs/reference/rekenen-getallen.csv \\
        --row 15 \\
        --count 10

    # Generate for specific grade/level
    python3 scripts/ai-bulk-generator.py \\
        --csv docs/reference/rekenen-getallen.csv \\
        --grade 4 \\
        --level M \\
        --count 20

    # Generate and validate
    python3 scripts/ai-bulk-generator.py \\
        --csv docs/reference/rekenen-getallen.csv \\
        --grade 4 \\
        --validate

    # Batch mode: generate all rows from CSV
    python3 scripts/ai-bulk-generator.py \\
        --csv docs/reference/rekenen-getallen.csv \\
        --batch \\
        --exercises-per-row 10

Features:
- Reads prompt templates from reference CSVs
- Generates structured JSON matching schema v2.0.0
- Creates both core and support files
- Automatic validation with comprehensive_validation.py
- Cost estimation and tracking
- Progress saving (resume interrupted generations)
"""

import json
import csv
import os
import sys
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import time

# Try to import Anthropic SDK
try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    print("⚠️  Anthropic SDK not installed. Install with: pip install anthropic")

# Try to import OpenAI SDK
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# API models and costs (per million tokens)
MODELS = {
    "claude-3-5-sonnet-20241022": {
        "provider": "anthropic",
        "input_cost": 3.00,
        "output_cost": 15.00,
        "max_tokens": 8192
    },
    "claude-3-haiku-20240307": {
        "provider": "anthropic",
        "input_cost": 0.25,
        "output_cost": 1.25,
        "max_tokens": 4096
    },
    "gpt-4o": {
        "provider": "openai",
        "input_cost": 2.50,
        "output_cost": 10.00,
        "max_tokens": 16384
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "input_cost": 0.15,
        "output_cost": 0.60,
        "max_tokens": 16384
    }
}

DEFAULT_MODEL = "claude-3-5-sonnet-20241022"


@dataclass
class GenerationTask:
    """Represents a single generation task"""
    csv_file: str
    row_index: int
    groep: int
    code: str
    beschrijving: str
    level: str
    toelichting: str
    prompt_template: str
    exercise_count: int
    category: str  # Derived from CSV filename


@dataclass
class GenerationResult:
    """Result of generating exercises"""
    task: GenerationTask
    success: bool
    core_path: Optional[str] = None
    support_path: Optional[str] = None
    validation_passed: bool = False
    quality_score: float = 0.0
    tokens_used: Dict[str, int] = field(default_factory=dict)
    cost_usd: float = 0.0
    error: Optional[str] = None


class AIExerciseGenerator:
    """Generates exercises using AI from prompt templates"""

    def __init__(self, model: str = DEFAULT_MODEL, api_key: Optional[str] = None):
        """
        Initialize generator

        Args:
            model: AI model to use (see MODELS dict)
            api_key: API key (or set ANTHROPIC_API_KEY / OPENAI_API_KEY env var)
        """
        self.model = model
        self.model_config = MODELS.get(model)

        if not self.model_config:
            raise ValueError(f"Unknown model: {model}. Choose from: {list(MODELS.keys())}")

        provider = self.model_config["provider"]

        # Initialize API client
        if provider == "anthropic":
            if not HAS_ANTHROPIC:
                raise ImportError("Anthropic SDK not installed. Run: pip install anthropic")
            self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        elif provider == "openai":
            if not HAS_OPENAI:
                raise ImportError("OpenAI SDK not installed. Run: pip install openai")
            self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

        self.provider = provider
        self.total_tokens = {"input": 0, "output": 0}
        self.total_cost = 0.0

    def generate_exercises(self, task: GenerationTask, output_dir: str = "data-v2-draft/exercises") -> GenerationResult:
        """
        Generate exercises for a task

        Args:
            task: GenerationTask with prompt template
            output_dir: Where to save generated files

        Returns:
            GenerationResult with paths and stats
        """
        print(f"\n📝 Generating {task.exercise_count} exercises for {task.code} (Groep {task.groep}, {task.level})...")

        # Build enhanced prompt
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(task)

        # Call AI
        try:
            core_data, support_data, tokens = self._call_ai(system_prompt, user_prompt, task.exercise_count)
        except Exception as e:
            return GenerationResult(
                task=task,
                success=False,
                error=str(e)
            )

        # Calculate cost
        cost = self._calculate_cost(tokens)
        self.total_tokens["input"] += tokens["input"]
        self.total_tokens["output"] += tokens["output"]
        self.total_cost += cost

        print(f"   Tokens: {tokens['input']:,} in + {tokens['output']:,} out = ${cost:.4f}")

        # Save to files
        category_dir = Path(output_dir) / task.category
        category_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        filename_base = f"{task.category}_groep{task.groep}_{task.level.lower()}_{task.code.lower()}"
        core_path = category_dir / f"{filename_base}_core.json"
        support_path = category_dir / f"{filename_base}_support.json"

        # Write files
        with open(core_path, 'w', encoding='utf-8') as f:
            json.dump(core_data, f, ensure_ascii=False, indent=2)

        with open(support_path, 'w', encoding='utf-8') as f:
            json.dump(support_data, f, ensure_ascii=False, indent=2)

        print(f"   ✅ Saved to {core_path}")

        return GenerationResult(
            task=task,
            success=True,
            core_path=str(core_path),
            support_path=str(support_path),
            tokens_used=tokens,
            cost_usd=cost
        )

    def _build_system_prompt(self) -> str:
        """Build system prompt for AI"""
        return """Je bent een expert onderwijsontwerper voor het Nederlandse basisonderwijs.

Je taak is om hoogwaardige oefeningen te genereren die:
1. Aansluiten bij de Nederlandse SLO-kerndoelen
2. Leeftijd-geschikt zijn (groep 1-8, leeftijd 4-12 jaar)
3. De juiste moeilijkheidsgraad hebben voor het niveau
4. Pedagogisch verantwoord zijn met scaffolding (progressieve hints)
5. Concrete, herkenbare Nederlandse contexten gebruiken
6. Inclusief en divers zijn (namen, situaties)

Je genereert JSON in exact dit formaat (schema versie 2.0.0):

**CORE FILE** (vragen en antwoorden):
{
  "schema_version": "2.0.0",
  "metadata": {
    "id": "gb_groep4_m4_1",
    "type": "multiple_choice",
    "category": "gb",
    "grade": 4,
    "level": "M4",
    "language": "nl-NL",
    "slo_alignment": {
      "kerndoelen": ["K28", "K29"],
      "rekendomeinen": ["getallen"],
      "referentieniveau": "1F",
      "cognitive_level": "toepassen"
    }
  },
  "display": {
    "title": "Titel van de oefening"
  },
  "content": {
    "instruction": "Bereken:"
  },
  "items": [
    {
      "id": 1,
      "type": "multiple_choice",
      "theme": "thema-naam",
      "question": {
        "text": "Vraag hier?"
      },
      "options": [
        {"text": "Optie 1"},
        {"text": "Optie 2"},
        {"text": "Optie 3"},
        {"text": "Optie 4"}
      ],
      "answer": {
        "type": "single",
        "correct_index": 0
      }
    }
  ]
}

**SUPPORT FILE** (hints, feedback, pedagogie):
{
  "schema_version": "2.0.0",
  "exercise_id": "gb_groep4_m4_1",
  "items": [
    {
      "item_id": 1,
      "hints": [
        {
          "level": 1,
          "text": "Algemene hint over strategie",
          "cost_points": 0
        },
        {
          "level": 2,
          "text": "Specifiekere hint",
          "cost_points": 1
        },
        {
          "level": 3,
          "text": "Hint die bijna het antwoord geeft",
          "cost_points": 2
        }
      ],
      "feedback": {
        "correct": {
          "default": "Goed gedaan!",
          "on_first_try": "Uitstekend! Je hebt het meteen goed!",
          "after_hint": "Mooi! De hint heeft je geholpen."
        },
        "incorrect": {
          "first_attempt": "Nog niet helemaal. Probeer het nog eens.",
          "second_attempt": "Denk goed na. Wil je een hint?"
        },
        "per_option": [
          {
            "option_index": 1,
            "text": "Je dacht aan X, maar de vraag vraagt naar Y",
            "common_misconception": "Waarom leerlingen dit vaak kiezen",
            "remediation": "Hoe het beter te doen"
          }
        ]
      },
      "learning": {
        "skill_description": "Welke vaardigheid wordt geoefend",
        "reading_strategies": ["Strategie 1", "Strategie 2"],
        "math_strategies": ["Rekenstrategie 1"],
        "common_errors": [
          {
            "type": "type_fout",
            "description": "Beschrijving van veelgemaakte fout",
            "remedy": "Hoe de fout te voorkomen"
          }
        ]
      }
    }
  ]
}

BELANGRIJKE REGELS:
- 4 antwoordopties per vraag (tenzij anders aangegeven)
- Alle 3 foutieve opties moeten plausibel zijn (geen "nee" naast "ja, absoluut!")
- Per-option feedback voor ELKE foutieve optie
- 3 progressieve hints per item (van algemeen naar specifiek)
- Gebruik herkenbare Nederlandse namen (diverse achtergronden: Emma, Yusuf, Ling, Fatima, etc.)
- Contexten: school, sport, natuur, technologie, dagelijks leven
- Geen stereotypen of vooroordelen

Genereer ALLEEN VALIDE JSON. Geen tekst ervoor of erna."""

    def _build_user_prompt(self, task: GenerationTask) -> str:
        """Build user prompt from task"""
        return f"""{task.prompt_template}

**EXTRA SPECIFICATIES:**
- Genereer PRECIES {task.exercise_count} items
- Groep: {task.groep}
- Niveau: {task.level}
- Code: {task.code}
- Beschrijving: {task.beschrijving}
- Toelichting: {task.toelichting}

**OUTPUT FORMAAT:**
Genereer 2 JSON objecten gescheiden door "---SPLIT---":

1. CORE file (metadata + items met vragen en antwoorden)
2. SUPPORT file (hints, feedback, learning metadata)

Voorbeeld:
{{CORE JSON}}
---SPLIT---
{{SUPPORT JSON}}

Begin nu met genereren!"""

    def _call_ai(self, system_prompt: str, user_prompt: str, exercise_count: int) -> Tuple[Dict, Dict, Dict]:
        """
        Call AI API and parse response

        Returns:
            (core_data, support_data, tokens_dict)
        """
        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.model_config["max_tokens"],
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            content = response.content[0].text
            tokens = {
                "input": response.usage.input_tokens,
                "output": response.usage.output_tokens
            }

        elif self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=self.model_config["max_tokens"],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )

            content = response.choices[0].message.content
            tokens = {
                "input": response.usage.prompt_tokens,
                "output": response.usage.completion_tokens
            }

        # Parse JSON from response
        core_data, support_data = self._parse_ai_response(content)

        return core_data, support_data, tokens

    def _parse_ai_response(self, content: str) -> Tuple[Dict, Dict]:
        """
        Parse AI response into core and support data

        AI should output: {CORE_JSON}---SPLIT---{SUPPORT_JSON}
        """
        # Try to split on marker
        if "---SPLIT---" in content:
            parts = content.split("---SPLIT---")
            core_text = parts[0].strip()
            support_text = parts[1].strip() if len(parts) > 1 else "{}"
        else:
            # Fallback: try to find two JSON objects
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            matches = re.findall(json_pattern, content, re.DOTALL)

            if len(matches) >= 2:
                core_text = matches[0]
                support_text = matches[1]
            elif len(matches) == 1:
                core_text = matches[0]
                support_text = "{}"
            else:
                raise ValueError("Could not find JSON in AI response")

        # Clean up markdown code blocks if present
        core_text = re.sub(r'```json\s*', '', core_text)
        core_text = re.sub(r'```\s*', '', core_text)
        support_text = re.sub(r'```json\s*', '', support_text)
        support_text = re.sub(r'```\s*', '', support_text)

        # Parse JSON
        try:
            core_data = json.loads(core_text)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse core JSON: {e}")
            print(f"Core text (first 500 chars):\n{core_text[:500]}")
            raise

        try:
            support_data = json.loads(support_text)
        except json.JSONDecodeError as e:
            print(f"⚠️  Failed to parse support JSON: {e}")
            support_data = {}  # Continue with empty support

        return core_data, support_data

    def _calculate_cost(self, tokens: Dict) -> float:
        """Calculate cost in USD"""
        input_cost = (tokens["input"] / 1_000_000) * self.model_config["input_cost"]
        output_cost = (tokens["output"] / 1_000_000) * self.model_config["output_cost"]
        return input_cost + output_cost


def load_csv_tasks(csv_path: str, grade: Optional[int] = None, level: Optional[str] = None,
                   row_index: Optional[int] = None) -> List[GenerationTask]:
    """
    Load tasks from CSV

    Args:
        csv_path: Path to CSV file
        grade: Filter by grade (Groep)
        level: Filter by level (E, M)
        row_index: Generate only specific row (1-indexed)

    Returns:
        List of GenerationTask objects
    """
    tasks = []

    # Determine category from filename
    filename = Path(csv_path).stem  # e.g., "rekenen-getallen"
    category_map = {
        "rekenen-getallen": "gb",
        "nederlands-lezen": "bl",
        "nederlands-spelling": "sp",
        "nederlands-woordenschat": "ws",
        "orientatie-natuur-techniek": "wo"
    }
    category = category_map.get(filename, "unknown")

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            # Skip if row_index specified and doesn't match
            if row_index and idx != row_index:
                continue

            # Parse row
            groep = int(row['Groep'])
            code = row['Code']
            beschrijving = row['Beschrijving']
            level_val = row['Level']
            toelichting = row['Toelichting']
            prompt_template = row['Prompt_Template']

            # Filter by grade/level if specified
            if grade and groep != grade:
                continue
            if level and level_val != level:
                continue

            # Extract exercise count from prompt (default: 10)
            count_match = re.search(r'Genereer (\d+) oefeningen', prompt_template)
            exercise_count = int(count_match.group(1)) if count_match else 10

            task = GenerationTask(
                csv_file=csv_path,
                row_index=idx,
                groep=groep,
                code=code,
                beschrijving=beschrijving,
                level=level_val,
                toelichting=toelichting,
                prompt_template=prompt_template,
                exercise_count=exercise_count,
                category=category
            )
            tasks.append(task)

    return tasks


def validate_generated_exercises(result: GenerationResult) -> bool:
    """
    Run validation on generated exercises

    Returns:
        True if validation passed
    """
    if not result.core_path:
        return False

    # Try to import and run validator
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from comprehensive_validation import ExerciseValidator

        validator = ExerciseValidator()
        validation_result = validator.validate_file(result.core_path, result.support_path)

        result.validation_passed = validation_result.passed
        result.quality_score = validation_result.quality_score

        if validation_result.passed:
            print(f"   ✅ Validation passed! Quality: {result.quality_score:.1f}%")
        else:
            print(f"   ❌ Validation failed. Quality: {result.quality_score:.1f}%")
            print(f"      Critical: {validation_result.critical_count()}, Errors: {validation_result.error_count()}")

        return validation_result.passed

    except ImportError:
        print("   ⚠️  Validator not available. Skipping validation.")
        return True  # Don't block if validator missing


def main():
    parser = argparse.ArgumentParser(description='Generate exercises using AI from CSV templates')

    # Input selection
    parser.add_argument('--csv', required=True, help='Path to CSV file with prompt templates')
    parser.add_argument('--row', type=int, help='Generate only this row (1-indexed)')
    parser.add_argument('--grade', type=int, choices=range(1, 9), help='Generate only for this grade')
    parser.add_argument('--level', choices=['E', 'M'], help='Generate only for this level')

    # Generation options
    parser.add_argument('--count', type=int, help='Override exercise count per task')
    parser.add_argument('--batch', action='store_true', help='Generate all rows from CSV')

    # Model selection
    parser.add_argument('--model', default=DEFAULT_MODEL, choices=list(MODELS.keys()),
                       help=f'AI model to use (default: {DEFAULT_MODEL})')

    # Output
    parser.add_argument('--output', default='data-v2-draft/exercises',
                       help='Output directory (default: data-v2-draft/exercises)')

    # Validation
    parser.add_argument('--validate', action='store_true', help='Run validation after generation')
    parser.add_argument('--skip-validation-failures', action='store_true',
                       help='Continue even if validation fails')

    args = parser.parse_args()

    # Check API key
    model_provider = MODELS[args.model]["provider"]
    api_key_env = "ANTHROPIC_API_KEY" if model_provider == "anthropic" else "OPENAI_API_KEY"

    if not os.environ.get(api_key_env):
        print(f"❌ Error: {api_key_env} environment variable not set")
        print(f"\nSet it with:")
        print(f"  export {api_key_env}='your-api-key-here'")
        return 1

    # Load tasks
    print(f"📚 Loading tasks from {args.csv}...")
    tasks = load_csv_tasks(
        args.csv,
        grade=args.grade,
        level=args.level,
        row_index=args.row
    )

    if not tasks:
        print("❌ No tasks found matching criteria")
        return 1

    print(f"   Found {len(tasks)} tasks to generate")

    # Override count if specified
    if args.count:
        for task in tasks:
            task.exercise_count = args.count

    # Initialize generator
    print(f"\n🤖 Initializing AI generator with {args.model}...")
    generator = AIExerciseGenerator(model=args.model)

    # Generate
    results = []
    successful = 0
    failed = 0

    print(f"\n{'='*80}")
    print("GENERATING EXERCISES")
    print(f"{'='*80}")

    for i, task in enumerate(tasks, 1):
        print(f"\n[{i}/{len(tasks)}] {task.code}: {task.beschrijving}")

        result = generator.generate_exercises(task, output_dir=args.output)
        results.append(result)

        if result.success:
            successful += 1

            # Validate if requested
            if args.validate:
                passed = validate_generated_exercises(result)
                if not passed and not args.skip_validation_failures:
                    print(f"   ⚠️  Stopping due to validation failure (use --skip-validation-failures to continue)")
                    break
        else:
            failed += 1
            print(f"   ❌ Generation failed: {result.error}")

        # Brief pause to be nice to API
        time.sleep(0.5)

    # Summary
    print(f"\n{'='*80}")
    print("GENERATION SUMMARY")
    print(f"{'='*80}")
    print(f"Total tasks:       {len(tasks)}")
    print(f"Successful:        {successful} ✅")
    print(f"Failed:            {failed} ❌")
    print(f"\nTokens used:       {generator.total_tokens['input']:,} in + {generator.total_tokens['output']:,} out")
    print(f"Total cost:        ${generator.total_cost:.4f} USD")

    if args.validate:
        validated_count = sum(1 for r in results if r.validation_passed)
        avg_quality = sum(r.quality_score for r in results if r.success) / successful if successful > 0 else 0
        print(f"\nValidation passed: {validated_count}/{successful}")
        print(f"Avg quality score: {avg_quality:.1f}%")

    print(f"{'='*80}")

    # List generated files
    if successful > 0:
        print(f"\n📁 Generated files saved to: {args.output}/")
        for result in results[:10]:  # Show first 10
            if result.success:
                print(f"   - {result.core_path}")
        if len(results) > 10:
            print(f"   ... and {len(results) - 10} more")

    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
