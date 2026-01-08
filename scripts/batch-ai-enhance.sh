#!/bin/bash

#
# Batch AI Enhancement Script
#
# Processes all template files systematically by grade level
#
# Usage:
#   ./scripts/batch-ai-enhance.sh [--auto-approve] [--grade=4|5|6|7|8]
#

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
AUTO_APPROVE=""
GRADE=""

# Parse arguments
for arg in "$@"; do
  case $arg in
    --auto-approve)
      AUTO_APPROVE="--auto-approve"
      echo -e "${YELLOW}⚠️  Auto-approve mode enabled${NC}"
      ;;
    --grade=*)
      GRADE="${arg#*=}"
      ;;
    --help|-h)
      cat << EOF
Batch AI Enhancement Script

Processes all template files systematically by grade level.

Usage:
  ./scripts/batch-ai-enhance.sh [options]

Options:
  --auto-approve          Skip review, auto-approve all (fast but no quality check)
  --grade=N              Process only specific grade (4, 5, 6, 7, or 8)
  --help, -h             Show this help message

Examples:
  # Process all grades with review
  ./scripts/batch-ai-enhance.sh

  # Process all grades, auto-approve
  ./scripts/batch-ai-enhance.sh --auto-approve

  # Process only Groep 4
  ./scripts/batch-ai-enhance.sh --grade=4

  # Process only Groep 8, auto-approve
  ./scripts/batch-ai-enhance.sh --grade=8 --auto-approve

Environment:
  Requires ANTHROPIC_API_KEY or OPENAI_API_KEY to be set.

EOF
      exit 0
      ;;
  esac
done

# Check API key
if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
  echo -e "${RED}Error: No API key found${NC}"
  echo "Please set ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable"
  echo ""
  echo "Example:"
  echo "  export ANTHROPIC_API_KEY=\"sk-ant-your-key-here\""
  exit 1
fi

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Batch AI Enhancement - All Grades   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Function to process a file
process_file() {
  local file=$1
  local grade=$2
  local desc=$3

  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${GREEN}Processing: ${desc}${NC}"
  echo -e "${BLUE}File: ${file}${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""

  if [ ! -f "$file" ]; then
    echo -e "${RED}✗ File not found: ${file}${NC}"
    echo ""
    return 1
  fi

  node scripts/ai-enhancer.js "$file" $AUTO_APPROVE

  local exit_code=$?
  echo ""

  if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}✓ Successfully processed: ${desc}${NC}"
  else
    echo -e "${RED}✗ Failed to process: ${desc}${NC}"
  fi

  echo ""
  return $exit_code
}

# Track statistics
TOTAL_FILES=0
SUCCESS_FILES=0
FAILED_FILES=0

# Process Groep 4
if [ -z "$GRADE" ] || [ "$GRADE" = "4" ]; then
  echo -e "${BLUE}════════════════════════════════════════${NC}"
  echo -e "${BLUE}   GROEP 4 (Foundation) - 413 questions${NC}"
  echo -e "${BLUE}════════════════════════════════════════${NC}"
  echo ""

  ((TOTAL_FILES++))
  if process_file "data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json" "4" "Groep 4 - Reading (153 Q)"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi

  ((TOTAL_FILES++))
  if process_file "data/exercises/gb/gb_groep4_m4_TEMPLATE.json" "4" "Groep 4 - Math (260 Q)"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi
fi

# Process Groep 5
if [ -z "$GRADE" ] || [ "$GRADE" = "5" ]; then
  echo -e "${BLUE}════════════════════════════════════════${NC}"
  echo -e "${BLUE}   GROEP 5 (Development) - 393 questions${NC}"
  echo -e "${BLUE}════════════════════════════════════════${NC}"
  echo ""

  ((TOTAL_FILES++))
  if process_file "data/exercises/bl/bl_groep5_e5_1_TEMPLATE.json" "5" "Groep 5 - Reading Set 1 (153 Q)"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi

  ((TOTAL_FILES++))
  if process_file "data/exercises/bl/bl_groep5_m5_1_TEMPLATE.json" "5" "Groep 5 - Reading Set 2 (153 Q)"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi

  ((TOTAL_FILES++))
  if process_file "data/exercises/gb/gb_groep5_m5_TEMPLATE.json" "5" "Groep 5 - Math (240 Q)"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi
fi

# Process Groep 6
if [ -z "$GRADE" ] || [ "$GRADE" = "6" ]; then
  echo -e "${BLUE}════════════════════════════════════════${NC}"
  echo -e "${BLUE}   GROEP 6 (Intermediate) - 386 questions${NC}"
  echo -e "${BLUE}════════════════════════════════════════${NC}"
  echo ""

  ((TOTAL_FILES++))
  if process_file "data/exercises/bl/bl_groep6_e6_1_TEMPLATE.json" "6" "Groep 6 - Reading Set 1 (153 Q)"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi

  ((TOTAL_FILES++))
  if process_file "data/exercises/bl/bl_groep6_m6_1_TEMPLATE.json" "6" "Groep 6 - Reading Set 2 (153 Q)"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi

  ((TOTAL_FILES++))
  if process_file "data/exercises/gb/gb_groep6_m6_TEMPLATE.json" "6" "Groep 6 - Math (80 Q)"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi
fi

# Process Groep 7
if [ -z "$GRADE" ] || [ "$GRADE" = "7" ]; then
  echo -e "${BLUE}════════════════════════════════════════${NC}"
  echo -e "${BLUE}   GROEP 7 (Advanced) - 386 questions${NC}"
  echo -e "${BLUE}════════════════════════════════════════${NC}"
  echo ""

  ((TOTAL_FILES++))
  if process_file "data/exercises/bl/bl_groep7_e7_1_TEMPLATE.json" "7" "Groep 7 - Reading Set 1 (153 Q)"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi

  ((TOTAL_FILES++))
  if process_file "data/exercises/bl/bl_groep7_m7_1_TEMPLATE.json" "7" "Groep 7 - Reading Set 2 (153 Q)"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi

  ((TOTAL_FILES++))
  if process_file "data/exercises/gb/gb_groep7_m7_TEMPLATE.json" "7" "Groep 7 - Math (80 Q)"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi
fi

# Process Groep 8
if [ -z "$GRADE" ] || [ "$GRADE" = "8" ]; then
  echo -e "${BLUE}════════════════════════════════════════${NC}"
  echo -e "${BLUE}   GROEP 8 (Mastery) - 509 questions${NC}"
  echo -e "${BLUE}════════════════════════════════════════${NC}"
  echo ""

  ((TOTAL_FILES++))
  if process_file "data/exercises/bl/bl_groep8_e8_1_TEMPLATE.json" "8" "Groep 8 - Reading Set 1 (153 Q)"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi

  ((TOTAL_FILES++))
  if process_file "data/exercises/bl/bl_groep8_m8_1_TEMPLATE.json" "8" "Groep 8 - Reading Set 2 (153 Q)"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi

  ((TOTAL_FILES++))
  if process_file "data/exercises/gb/gb_groep8_e8_TEMPLATE.json" "8" "Groep 8 - Math (203 Q) ⭐ LARGEST"; then
    ((SUCCESS_FILES++))
  else
    ((FAILED_FILES++))
  fi
fi

# Summary
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         BATCH PROCESSING COMPLETE      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Total files processed:  ${TOTAL_FILES}${NC}"
echo -e "${GREEN}Successfully enhanced:  ${SUCCESS_FILES}${NC}"
echo -e "${RED}Failed:                 ${FAILED_FILES}${NC}"
echo ""

if [ $SUCCESS_FILES -eq $TOTAL_FILES ]; then
  echo -e "${GREEN}✨ All files processed successfully!${NC}"
  echo ""
  echo -e "${YELLOW}Next steps:${NC}"
  echo "  1. Run validator: node scripts/schema-validator-v2.js"
  echo "  2. Test enhanced files in browser"
  echo "  3. Review quality and refine as needed"
  echo "  4. Replace templates with AI_ENHANCED versions"
  echo "  5. Commit and celebrate! 🎉"
else
  echo -e "${YELLOW}⚠️  Some files failed to process. Review errors above.${NC}"
fi

echo ""
