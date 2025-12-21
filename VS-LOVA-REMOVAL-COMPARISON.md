# VS Support File - Before & After LOVA Removal

## File Size Comparison

| Version | Before (with LOVA) | After (standardized) | Reduction |
|---------|-------------------|---------------------|-----------|
| **Original Support** | 2.12 MB | 1.8 MB | -15% (320 KB) |
| **Enhanced Support** | 3.6 MB | 3.3 MB | -8% (300 KB) |

## Structure Comparison

### ❌ BEFORE (with LOVA - teacher pedagogy)
```json
{
  "item_id": "1_a",
  "hint": "💡 Let op: Je moet TWEE stappen doen...",
  "feedback": { "per_option": [...] },
  "explanation": { "concept": "...", "steps": [...] },
  "lova": {                                    // ❌ Teacher-facing
    "step1_reading": {
      "noise_information": [...],
      "main_question": "...",
      "sub_steps": [...]
    },
    "step2_organizing": {
      "relevant_numbers": {...},
      "tool": "...",
      "conversions": []
    },
    "step3_forming": {
      "operations": [...]                      // ❌ Duplicates explanation.steps
    },
    "step4_answering": {
      "expected_unit": "...",
      "logic_check": "...",
      "answer": "..."
    }
  },
  "learning": {
    "skill": "word_problems",
    "theme": "geld",
    "error_types": [...],
    "requires_multi_step": true
  }
}
```

### ✅ AFTER (standardized - student-facing)
```json
{
  "item_id": "1_a",
  "hint": "💡 Let op: Je moet TWEE stappen doen...",         // ✅ Student hint
  "feedback": {
    "per_option": [                                          // ✅ Specific error feedback
      {
        "option_index": 0,
        "text": "Dit is het startbudget...",
        "error_type": "leesfout_ruis",
        "remedial_basis_id": null
      }
    ]
  },
  "explanation": {                                           // ✅ Step-by-step solution
    "concept": "Dit is een aftreksom...",
    "steps": [
      "Bereken eerst de totale kosten...",
      "Trek dit bedrag af..."
    ],
    "calculation_table": [...]
  },
  "learning": {                                              // ✅ Metadata for analytics
    "skill": "word_problems",
    "theme": "geld",
    "error_types": ["leesfout_ruis", "rekenfout_basis"],
    "requires_multi_step": true
  }
}
```

## What We Kept (Student-Facing)

✅ **hint** - Clear guidance for students
✅ **feedback.per_option** - Specific error explanations with reflective questions
✅ **explanation.concept** - What type of problem this is
✅ **explanation.steps** - Step-by-step solution
✅ **explanation.calculation_table** - Visual table of calculations
✅ **learning.error_types** - For analytics and remediation
✅ **learning.theme** - Mathematical theme (geld, breuken, etc.)
✅ **learning.requires_multi_step** - Complexity indicator

## What We Removed (Teacher Pedagogy)

❌ **lova.step1_reading** - Teacher's reading analysis
❌ **lova.step2_organizing** - Teacher's number extraction guide
❌ **lova.step3_forming** - Duplicate of explanation.steps
❌ **lova.step4_answering** - Teacher's answer verification

## Benefits

1. **Consistent with all other categories** - Same template structure
2. **Student-focused** - Only content students actually see
3. **Smaller file sizes** - 15% reduction
4. **Easier to maintain** - Less duplication
5. **Cleaner schema** - Simpler validation

## Unique VS Features Still Preserved

✅ **Per-option error analysis** - Every wrong answer has specific feedback
✅ **Error type classification** - leesfout_ruis, rekenfout_basis, conceptfout
✅ **Reflective questions** - 🤔 prompts for metacognition
✅ **Calculation tables** - Markdown tables for visual clarity
✅ **Multi-step detection** - Flag for complex problems
✅ **Remedial links** - remedial_basis_id for practice exercises
