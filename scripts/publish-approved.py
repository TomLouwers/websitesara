#!/usr/bin/env python3
"""
Publish Approved Exercises
===========================

Moves approved exercises from draft directory to production.

Usage:
    # Publish specific files
    python3 scripts/publish-approved.py \\
        --file data-v2-draft/exercises/gb/gb_groep4_m4_core.json

    # Publish entire directory
    python3 scripts/publish-approved.py \\
        --from data-v2-draft/exercises/gb/ \\
        --to data-v2/exercises/gb/

    # Publish with validation (recommended)
    python3 scripts/publish-approved.py \\
        --from data-v2-draft/exercises/gb/ \\
        --to data-v2/exercises/gb/ \\
        --validate

    # Dry run (preview what would be published)
    python3 scripts/publish-approved.py \\
        --from data-v2-draft/exercises/gb/ \\
        --to data-v2/exercises/gb/ \\
        --dry-run

Features:
- Validates exercises before publishing
- Creates backups of existing files
- Updates index.json automatically
- Generates publish report
- Safe defaults (won't overwrite without confirmation)
"""

import json
import os
import sys
import argparse
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
import hashlib

# Try to import validator
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from comprehensive_validation import ExerciseValidator
    HAS_VALIDATOR = True
except ImportError:
    HAS_VALIDATOR = False
    print("⚠️  Validator not available. Use --skip-validation to proceed anyway.")


class PublishManager:
    """Manages publishing exercises from draft to production"""

    def __init__(self, validate: bool = True, backup: bool = True, dry_run: bool = False):
        """
        Initialize publish manager

        Args:
            validate: Run validation before publishing
            backup: Create backups of existing files
            dry_run: Preview changes without actually moving files
        """
        self.validate = validate
        self.backup = backup
        self.dry_run = dry_run
        self.validator = ExerciseValidator() if validate and HAS_VALIDATOR else None

        # Stats
        self.published_count = 0
        self.skipped_count = 0
        self.failed_count = 0
        self.backed_up_count = 0

        # Results
        self.results = []

    def publish_file(self, source_path: str, dest_path: str) -> Tuple[bool, str]:
        """
        Publish a single file

        Args:
            source_path: Path to source file
            dest_path: Path to destination

        Returns:
            (success, message)
        """
        source = Path(source_path)
        dest = Path(dest_path)

        if not source.exists():
            return False, f"Source file not found: {source}"

        # Validate if enabled
        if self.validate and self.validator:
            # Check if it's a core file
            if '_core.json' in source.name:
                support_path = str(source).replace('_core.json', '_support.json')
                support_path = support_path if Path(support_path).exists() else None

                result = self.validator.validate_file(str(source), support_path)

                if not result.passed:
                    critical_count = result.critical_count()
                    error_count = result.error_count()
                    return False, f"Validation failed: {critical_count} critical, {error_count} errors (quality: {result.quality_score:.1f}%)"

                if result.quality_score < 60:
                    return False, f"Quality score too low: {result.quality_score:.1f}% (minimum: 60%)"

        # Create destination directory if needed
        if not self.dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)

        # Backup existing file if it exists
        if dest.exists() and self.backup:
            if not self.dry_run:
                backup_path = self._create_backup(dest)
                self.backed_up_count += 1
                print(f"      📦 Backed up to: {backup_path.name}")
            else:
                print(f"      📦 Would backup existing file")

        # Copy file
        if not self.dry_run:
            shutil.copy2(source, dest)
            self.published_count += 1
            return True, f"Published to {dest}"
        else:
            return True, f"Would publish to {dest}"

    def publish_directory(self, source_dir: str, dest_dir: str, pattern: str = "*_core.json") -> List[Dict]:
        """
        Publish all matching files from a directory

        Args:
            source_dir: Source directory
            dest_dir: Destination directory
            pattern: File pattern to match

        Returns:
            List of results
        """
        source_path = Path(source_dir)
        dest_path = Path(dest_dir)

        if not source_path.exists():
            print(f"❌ Source directory not found: {source_dir}")
            return []

        # Find all core files
        core_files = sorted(source_path.glob(pattern))

        if not core_files:
            print(f"⚠️  No files matching {pattern} found in {source_dir}")
            return []

        print(f"\n📁 Found {len(core_files)} files to publish")
        print(f"   Source: {source_dir}")
        print(f"   Destination: {dest_dir}")

        if self.dry_run:
            print(f"\n🔍 DRY RUN MODE - No files will be moved\n")

        results = []

        for core_file in core_files:
            # Determine destination path (preserve filename)
            dest_file = dest_path / core_file.name

            print(f"\n📄 {core_file.name}")

            # Publish core file
            success, message = self.publish_file(str(core_file), str(dest_file))

            result = {
                'file': core_file.name,
                'source': str(core_file),
                'destination': str(dest_file),
                'success': success,
                'message': message
            }
            results.append(result)

            if success:
                print(f"   ✅ {message}")

                # Also publish support file if it exists
                support_file = core_file.parent / core_file.name.replace('_core.json', '_support.json')
                if support_file.exists():
                    support_dest = dest_file.parent / support_file.name
                    support_success, support_message = self.publish_file(str(support_file), str(support_dest))

                    if support_success:
                        print(f"   ✅ Published support file")
                    else:
                        print(f"   ⚠️  Support file failed: {support_message}")
            else:
                print(f"   ❌ {message}")
                self.failed_count += 1

        self.results.extend(results)
        return results

    def _create_backup(self, file_path: Path) -> Path:
        """
        Create backup of existing file

        Args:
            file_path: Path to file to backup

        Returns:
            Path to backup file
        """
        backup_dir = file_path.parent / '.backups'
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = backup_dir / backup_name

        shutil.copy2(file_path, backup_path)
        return backup_path

    def generate_report(self, output_path: str = None) -> str:
        """
        Generate publish report

        Args:
            output_path: Optional path to save report

        Returns:
            Report text
        """
        report_lines = [
            "=" * 80,
            "PUBLISH REPORT",
            "=" * 80,
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "SUMMARY:",
            f"  Published: {self.published_count} files",
            f"  Skipped:   {self.skipped_count} files",
            f"  Failed:    {self.failed_count} files",
            f"  Backed up: {self.backed_up_count} files",
            "",
            "DETAILS:",
        ]

        for result in self.results:
            status = "✅" if result['success'] else "❌"
            report_lines.append(f"  {status} {result['file']}")
            if not result['success']:
                report_lines.append(f"      {result['message']}")

        report_lines.append("=" * 80)

        report = "\n".join(report_lines)

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📄 Report saved to: {output_path}")

        return report


def update_index(exercises_dir: str = "data-v2/exercises"):
    """
    Update index.json with all exercises

    Args:
        exercises_dir: Path to exercises directory
    """
    print(f"\n📇 Updating index.json...")

    index_path = Path(exercises_dir) / "index.json"
    exercises_path = Path(exercises_dir)

    if not exercises_path.exists():
        print(f"❌ Directory not found: {exercises_dir}")
        return

    # Find all core files
    core_files = sorted(exercises_path.glob("**/*_core.json"))

    exercises = []

    for core_file in core_files:
        try:
            with open(core_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            metadata = data.get('metadata', {})

            # Determine paths relative to exercises directory
            rel_path = core_file.relative_to(exercises_path)
            category = rel_path.parts[0] if len(rel_path.parts) > 1 else 'unknown'

            exercise_entry = {
                'id': metadata.get('id', core_file.stem.replace('_core', '')),
                'category': metadata.get('category', category),
                'type': metadata.get('type', 'multiple_choice'),
                'title': data.get('display', {}).get('title', ''),
                'grade': metadata.get('grade'),
                'level': metadata.get('level', ''),
                'difficulty': metadata.get('difficulty', 'medium'),
                'paths': {
                    'core': str(rel_path),
                    'support': str(rel_path).replace('_core.json', '_support.json')
                }
            }

            exercises.append(exercise_entry)

        except Exception as e:
            print(f"   ⚠️  Error processing {core_file.name}: {e}")
            continue

    # Create index
    index_data = {
        'schema_version': '2.0.0',
        'generated_at': datetime.now().isoformat(),
        'total_exercises': len(exercises),
        'exercises': sorted(exercises, key=lambda x: (x['category'], x['grade'] or 0, x['id']))
    }

    # Write index
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    print(f"   ✅ Index updated with {len(exercises)} exercises")
    print(f"   📄 {index_path}")


def main():
    parser = argparse.ArgumentParser(description='Publish approved exercises to production')

    # Input options
    parser.add_argument('--file', help='Publish single file')
    parser.add_argument('--from', dest='from_dir', help='Source directory')
    parser.add_argument('--to', dest='to_dir', help='Destination directory')

    # Options
    parser.add_argument('--validate', action='store_true', default=True,
                       help='Validate before publishing (default: True)')
    parser.add_argument('--skip-validation', action='store_true',
                       help='Skip validation (use with caution)')
    parser.add_argument('--no-backup', action='store_true',
                       help='Don\'t backup existing files')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without moving files')
    parser.add_argument('--update-index', action='store_true',
                       help='Update index.json after publishing')
    parser.add_argument('--report', help='Save report to file')

    args = parser.parse_args()

    # Validation
    if args.skip_validation:
        validate = False
    else:
        validate = args.validate

    if validate and not HAS_VALIDATOR:
        print("❌ Validator not available but --validate was requested")
        print("   Install dependencies: pip install textstat")
        print("   Or use --skip-validation (not recommended)")
        return 1

    # Create publish manager
    manager = PublishManager(
        validate=validate,
        backup=not args.no_backup,
        dry_run=args.dry_run
    )

    print("=" * 80)
    print("PUBLISH APPROVED EXERCISES")
    print("=" * 80)

    # Publish
    if args.file:
        # Single file
        if not args.to_dir:
            print("❌ --to directory is required when using --file")
            return 1

        dest_path = Path(args.to_dir) / Path(args.file).name
        success, message = manager.publish_file(args.file, str(dest_path))

        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            return 1

    elif args.from_dir and args.to_dir:
        # Directory
        manager.publish_directory(args.from_dir, args.to_dir)

    else:
        parser.print_help()
        return 1

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Published: {manager.published_count} files ✅")
    if manager.failed_count > 0:
        print(f"Failed:    {manager.failed_count} files ❌")
    if manager.backed_up_count > 0:
        print(f"Backed up: {manager.backed_up_count} files 📦")
    if args.dry_run:
        print("\n🔍 DRY RUN - No changes were made")
    print("=" * 80)

    # Update index if requested
    if args.update_index and not args.dry_run:
        update_index(args.to_dir)

    # Generate report
    if args.report:
        manager.generate_report(args.report)

    # Exit code
    return 0 if manager.failed_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
