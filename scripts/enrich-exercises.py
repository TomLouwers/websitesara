#!/usr/bin/env python3
"""
Exercise Enrichment Tool
========================

Enhances existing exercises by adding AI-generated pedagogical features:
- Progressive hints (3 levels)
- Per-option feedback
- Learning strategies (LOVA framework)
- Common errors documentation

This tool takes existing core exercises (questions + answers only) and generates
comprehensive support files to improve pedagogical quality from 30-40% to 70-85%.

Usage:
    # Enrich single exercise
    python3 scripts/enrich-exercises.py \\
        --file data-v2/exercises/gb/gb_groep3_e3_core.json

    # Enrich all exercises in category
    python3 scripts/enrich-exercises.py \\
        --category gb \\
        --validate

    # Enrich all exercises
    python3 scripts/enrich-exercises.py \\
        --all \\
        --validate

    # Dry-run to preview
    python3 scripts/enrich-exercises.py \\
        --category gb \\
        --dry-run
"""

import json
import os
import sys
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
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

# API models and costs
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
    "gpt-4o-mini": {
        "provider": "openai",
        "input_cost": 0.15,
        "output_cost": 0.60,
        "max_tokens": 16384
    }
}

DEFAULT_MODEL = "claude-3-haiku-20240307"  # Faster and cheaper for enrichment


@dataclass
class EnrichmentResult:
    """Result of enriching an exercise"""
    exercise_id: str
    success: bool
    support_path: Optional[str] = None
    validation_passed: bool = False
    quality_score_before: float = 0.0
    quality_score_after: float = 0.0
    tokens_used: Dict[str, int] = None
    cost_usd: float = 0.0
    error: Optional[str] = None


class ExerciseEnricher:
    """Enriches existing exercises with AI-generated pedagogical features"""

    def __init__(self, model: str = DEFAULT_MODEL, api_key: Optional[str] = None):
        """Initialize enricher with AI model"""
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

    def enrich_exercise(self, core_path: str, output_dir: str = "data-v2-draft/exercises") -> EnrichmentResult:
        """
        Enrich an exercise by generating support file

        Args:
            core_path: Path to existing core exercise file
            output_dir: Where to save enriched support file

        Returns:
            EnrichmentResult with paths and stats
        """
        core_path = Path(core_path)

        if not core_path.exists():
            return EnrichmentResult(
                exercise_id=core_path.stem,
                success=False,
                error=f"File not found: {core_path}"
            )

        # Load existing core file
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
        except Exception as e:
            return EnrichmentResult(
                exercise_id=core_path.stem,
                success=False,
                error=f"Failed to load JSON: {e}"
            )

        exercise_id = core_data.get('metadata', {}).get('id', core_path.stem)
        print(f"\n📝 Enriching: {exercise_id}")

        # Check if support file already exists
        existing_support = self._find_existing_support(core_path)
        if existing_support and existing_support.exists():
            print(f"   ⚠️  Support file already exists: {existing_support}")
            print(f"   Skipping (use --force to overwrite)")
            return EnrichmentResult(
                exercise_id=exercise_id,
                success=False,
                error="Support file already exists"
            )

        # Build prompt
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(core_data)

        # Call AI
        try:
            support_data, tokens = self._call_ai(system_prompt, user_prompt)
        except Exception as e:
            return EnrichmentResult(
                exercise_id=exercise_id,
                success=False,
                error=str(e)
            )

        # Calculate cost
        cost = self._calculate_cost(tokens)
        self.total_tokens["input"] += tokens["input"]
        self.total_tokens["output"] += tokens["output"]
        self.total_cost += cost

        print(f"   Tokens: {tokens['input']:,} in + {tokens['output']:,} out = ${cost:.4f}")

        # Determine output path
        category = core_data.get('metadata', {}).get('category', 'unknown')
        category_dir = Path(output_dir) / category
        category_dir.mkdir(parents=True, exist_ok=True)

        # Generate support filename
        support_filename = core_path.stem.replace('_core', '_support') + '.json'
        support_path = category_dir / support_filename

        # Write support file
        with open(support_path, 'w', encoding='utf-8') as f:
            json.dump(support_data, f, ensure_ascii=False, indent=2)

        print(f"   ✅ Saved support to {support_path}")

        return EnrichmentResult(
            exercise_id=exercise_id,
            success=True,
            support_path=str(support_path),
            tokens_used=tokens,
            cost_usd=cost
        )

    def _find_existing_support(self, core_path: Path) -> Optional[Path]:
        """Find existing support file for core exercise"""
        support_path = Path(str(core_path).replace('_core.json', '_support.json'))
        return support_path if support_path.exists() else None

    def _build_system_prompt(self) -> str:
        """Build system prompt for AI enrichment"""
        return """Je bent een expert onderwijsontwerper voor het Nederlandse basisonderwijs.

Je taak is om bestaande oefeningen te VERRIJKEN met pedagogische ondersteuning.
Je krijgt een oefening met vragen en antwoorden, en jouw taak is om toe te voegen:

1. **Progressieve hints** (3 niveaus per vraag):
   - Level 1: Algemene strategie hint (cost: 0 punten)
   - Level 2: Meer specifieke hint, focus op aanpak (cost: 1 punt)
   - Level 3: Bijna het antwoord, laatste stap (cost: 2 punten)

2. **Per-optie feedback**:
   - Correct feedback: Positieve bevestiging + uitleg waarom goed
   - Incorrect feedback: Voor elke foute optie, leg uit welke misconceptie dit is

3. **Learning strategies** (LOVA framework voor rekenen):
   - Reading strategy: Hoe lees je de vraag/probleem?
   - Math strategy: Welke rekenstrategie is handig?

4. **Common errors**:
   - Typische fouten die leerlingen maken bij dit type vraag
   - Uitleg waarom deze fout gemaakt wordt

**BELANGRIJKE RICHTLIJNEN:**
- Gebruik de context uit de originele vraag (groep, niveau, onderwerp)
- Hints moeten opbouwend zijn: van algemeen naar specifiek
- Feedback moet constructief en leerzaam zijn
- Gebruik Nederlandse didactische termen (splitsen, bruggetje, etc.)
- Voor wiskunde: gebruik KaTeX notatie ($...$) waar nodig
- Wees positief en motiverend in toon

**OUTPUT FORMAAT:**
Genereer ALLEEN het support JSON object (schema v2.0.0).
Geen tekst ervoor of erna, alleen valide JSON."""

    def _build_user_prompt(self, core_data: Dict) -> str:
        """Build user prompt from existing exercise"""
        metadata = core_data.get('metadata', {})
        items = core_data.get('items', [])

        # Extract key info
        exercise_id = metadata.get('id', 'unknown')
        grade = metadata.get('grade', 'onbekend')
        level = metadata.get('level', '')
        title = metadata.get('title', metadata.get('description', ''))
        category = metadata.get('category', '')

        # Format items for prompt
        items_text = ""
        for i, item in enumerate(items, 1):
            question = item.get('question', {}).get('text', '')
            options = item.get('options', [])
            answer = item.get('answer', {})
            correct_idx = answer.get('correct_index', 0)

            items_text += f"\n**Item {i}:**\n"
            items_text += f"Vraag: {question}\n"
            items_text += f"Opties:\n"
            for j, opt in enumerate(options):
                opt_text = opt.get('text', opt) if isinstance(opt, dict) else opt
                marker = " ✓ (CORRECT)" if j == correct_idx else ""
                items_text += f"  {chr(97+j)}) {opt_text}{marker}\n"

        return f"""Verrijk de volgende oefening met pedagogische ondersteuning.

**OEFENING CONTEXT:**
- ID: {exercise_id}
- Groep: {grade}
- Niveau: {level}
- Titel: {title}
- Categorie: {category}

**VRAGEN EN ANTWOORDEN:**
{items_text}

**GENEREER NU:**

Een support JSON object met deze structuur:

{{
  "schema_version": "2.0.0",
  "metadata": {{
    "id": "{exercise_id}",
    "exercise_id": "{exercise_id}",
    "category": "{category}",
    "grade": {grade}{f', "level": "{level}"' if level else ''}
  }},
  "support_items": [
    {{
      "item_id": 1,
      "hints": [
        {{ "level": 1, "text": "...", "cost_points": 0 }},
        {{ "level": 2, "text": "...", "cost_points": 1 }},
        {{ "level": 3, "text": "...", "cost_points": 2 }}
      ],
      "feedback": {{
        "correct": "...",
        "incorrect": [
          {{ "option_index": 0, "text": "..." }},
          ...
        ]
      }},
      "learning_strategies": {{
        "reading_strategy": {{ "name": "...", "description": "..." }},
        "math_strategy": {{ "name": "...", "description": "..." }}
      }},
      "common_errors": [
        {{ "error": "...", "explanation": "..." }}
      ]
    }}
  ]
}}

Genereer voor ALLE items in de oefening (items 1 t/m {len(items)}).

Begin nu met het JSON object:"""

    def _call_ai(self, system_prompt: str, user_prompt: str) -> Tuple[Dict, Dict]:
        """Call AI API and parse response"""
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
        support_data = self._parse_ai_response(content)

        return support_data, tokens

    def _parse_ai_response(self, content: str) -> Dict:
        """Parse AI response into support data"""
        # Clean up markdown code blocks if present
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```\s*$', '', content)
        content = content.strip()

        # Try to find JSON object
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_text = json_match.group(0)
        else:
            json_text = content

        try:
            support_data = json.loads(json_text)
            return support_data
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {e}\nContent: {content[:500]}")

    def _calculate_cost(self, tokens: Dict[str, int]) -> float:
        """Calculate cost in USD"""
        input_cost = (tokens["input"] / 1_000_000) * self.model_config["input_cost"]
        output_cost = (tokens["output"] / 1_000_000) * self.model_config["output_cost"]
        return input_cost + output_cost


def find_exercises_to_enrich(base_dir: str = "data-v2/exercises", category: Optional[str] = None) -> List[Path]:
    """
    Find all core exercises that don't have support files

    Args:
        base_dir: Base directory containing exercises
        category: Filter by category (e.g., 'gb', 'bl')

    Returns:
        List of paths to core files without support
    """
    base_path = Path(base_dir)
    core_files = []

    # Search pattern
    if category:
        pattern = f"{category}/*_core.json"
    else:
        pattern = "**/*_core.json"

    for core_file in base_path.glob(pattern):
        # Check if support file exists
        support_file = Path(str(core_file).replace('_core.json', '_support.json'))

        if not support_file.exists():
            core_files.append(core_file)

    return sorted(core_files)


def main():
    parser = argparse.ArgumentParser(
        description="Enrich existing exercises with AI-generated pedagogical features",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Input options
    parser.add_argument('--file', type=str, help='Enrich single exercise file')
    parser.add_argument('--category', type=str, help='Enrich all exercises in category (gb, bl, sp, etc.)')
    parser.add_argument('--all', action='store_true', help='Enrich all exercises')

    # Output options
    parser.add_argument('--output-dir', type=str, default='data-v2-draft/exercises',
                        help='Output directory for enriched support files (default: data-v2-draft/exercises)')

    # AI options
    parser.add_argument('--model', type=str, default=DEFAULT_MODEL,
                        choices=list(MODELS.keys()),
                        help=f'AI model to use (default: {DEFAULT_MODEL})')

    # Validation
    parser.add_argument('--validate', action='store_true',
                        help='Validate enriched exercises with comprehensive_validation.py')

    # Other options
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be enriched without actually doing it')
    parser.add_argument('--force', action='store_true',
                        help='Overwrite existing support files')
    parser.add_argument('--limit', type=int, help='Limit number of exercises to enrich')

    args = parser.parse_args()

    # Determine which files to enrich
    if args.file:
        files_to_enrich = [Path(args.file)]
    elif args.category:
        files_to_enrich = find_exercises_to_enrich(category=args.category)
    elif args.all:
        files_to_enrich = find_exercises_to_enrich()
    else:
        parser.error("Must specify --file, --category, or --all")

    if args.limit:
        files_to_enrich = files_to_enrich[:args.limit]

    print(f"\n{'='*80}")
    print("EXERCISE ENRICHMENT")
    print(f"{'='*80}\n")
    print(f"📁 Found {len(files_to_enrich)} exercises to enrich")

    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No files will be created\n")
        for f in files_to_enrich:
            print(f"   Would enrich: {f}")
        return

    if not files_to_enrich:
        print("\n✅ No exercises need enrichment (all have support files)")
        return

    # Initialize enricher
    try:
        enricher = ExerciseEnricher(model=args.model)
    except Exception as e:
        print(f"\n❌ Failed to initialize enricher: {e}")
        return 1

    # Enrich exercises
    results = []
    for i, core_file in enumerate(files_to_enrich, 1):
        print(f"\n[{i}/{len(files_to_enrich)}]", end=" ")
        result = enricher.enrich_exercise(core_file, args.output_dir)
        results.append(result)

        if not result.success and "already exists" not in result.error:
            print(f"   ❌ Error: {result.error}")

        time.sleep(0.5)  # Rate limiting

    # Summary
    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]

    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Enriched: {len(successful)} exercises ✅")
    if failed:
        print(f"Failed:   {len(failed)} exercises ❌")
    print(f"\nTotal tokens: {enricher.total_tokens['input']:,} in + {enricher.total_tokens['output']:,} out")
    print(f"Total cost:   ${enricher.total_cost:.2f}")
    print(f"{'='*80}\n")

    # Validation
    if args.validate and successful:
        print("🔍 Running validation...")
        # Import validation here to avoid circular dependency
        try:
            from comprehensive_validation import ExerciseValidator
            validator = ExerciseValidator()

            for result in successful:
                if result.support_path:
                    core_path = result.support_path.replace('_support.json', '_core.json')
                    validation_result = validator.validate_file(core_path, result.support_path)
                    print(f"   {result.exercise_id}: {validation_result.quality_score:.1f}% quality")
        except Exception as e:
            print(f"   ⚠️  Validation failed: {e}")

    return 0 if not failed else 1


if __name__ == '__main__':
    sys.exit(main())
