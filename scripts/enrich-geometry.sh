#!/bin/bash
#
# Enrich all geometry (mk) exercises with hints and feedback
#

echo "🎯 Enriching Geometry Exercises"
echo "================================"
echo ""

CORE_FILES=$(ls data-v2/exercises/mk/*_core.json 2>/dev/null)
COUNT=$(echo "$CORE_FILES" | wc -l)

echo "Found $COUNT geometry exercise files"
echo ""

i=1
for file in $CORE_FILES; do
    echo "[$i/$COUNT] Processing: $(basename $file)"
    python3 scripts/enrich-exercises.py \
        --file "$file" \
        --force \
        --output-dir data-v2/exercises

    if [ $? -eq 0 ]; then
        echo "   ✅ Success"
    else
        echo "   ❌ Failed"
    fi

    echo ""
    ((i++))
done

echo "================================"
echo "✅ Geometry enrichment complete!"
