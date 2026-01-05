# KaTeX Math Notation Guide

Professional math formatting for OefenPlatform exercises using KaTeX.

## What is KaTeX?

KaTeX is a fast, lightweight library for rendering mathematical notation. It makes math look professional and clear, especially important for:
- Fractions
- Exponents
- Mathematical symbols
- Equations

## How to Use

### Basic Syntax

Wrap LaTeX math in dollar signs:
- **Inline math:** `$...$` - Renders inline with text
- **Display math:** `$$...$$` - Renders centered on its own line

### Examples

#### Fractions

**Plain text (old):**
```
"3/4 + 1/2 = ?"
```

**KaTeX (new):**
```
"$\frac{3}{4} + \frac{1}{2}$ = ?"
```

**Renders as:** ¾ + ½ = ?

#### Multiplication & Division

**Plain text:**
```
"8 x 7 = ?"
"56 : 8 = ?"
```

**KaTeX:**
```
"$8 \times 7$ = ?"
"$56 \div 8$ = ?"
```

**Renders as:** 8 × 7 = ?, 56 ÷ 8 = ?

#### Exponents

**Plain text:**
```
"2^3 = ?"
"5^2 = ?"
```

**KaTeX:**
```
"$2^3$ = ?"
"$5^2$ = ?"
```

**Renders as:** 2³ = ?, 5² = ?

#### Square Roots

**Plain text:**
```
"Wortel van 16 = ?"
```

**KaTeX:**
```
"$\sqrt{16}$ = ?"
```

**Renders as:** √16 = ?

#### Percentages

**Plain text:**
```
"25% van 80 = ?"
```

**KaTeX:**
```
"$25\%$ van $80$ = ?"
```

**Renders as:** 25% van 80 = ?

#### Equations

**Plain text:**
```
"Los op: 2x + 5 = 13"
```

**KaTeX:**
```
"Los op: $2x + 5 = 13$"
```

**Renders as:** Los op: 2x + 5 = 13

## Common Symbols

| Symbol | LaTeX Code | Example |
|--------|------------|---------|
| × (multiply) | `\times` | `$5 \times 6$` |
| ÷ (divide) | `\div` | `$20 \div 4$` |
| ± (plus-minus) | `\pm` | `$\pm 3$` |
| ≤ (less equal) | `\leq` | `$x \leq 10$` |
| ≥ (greater equal) | `\geq` | `$x \geq 5$` |
| ≠ (not equal) | `\neq` | `$x \neq 0$` |
| √ (square root) | `\sqrt{}` | `$\sqrt{25}$` |
| ² (squared) | `^2` | `$x^2$` |
| ³ (cubed) | `^3` | `$x^3$` |
| ½ (fraction) | `\frac{1}{2}` | `$\frac{1}{2}$` |
| % (percent) | `\%` | `$50\%$` |
| ° (degree) | `^\circ` | `$90^\circ$` |
| π (pi) | `\pi` | `$\pi r^2$` |

## Exercise JSON Examples

### Multiple Choice with Math

```json
{
  "id": 1,
  "type": "multiple_choice",
  "theme": "breuken",
  "question": {
    "text": "Bereken: $\\frac{3}{4} + \\frac{1}{4}$"
  },
  "options": [
    {"text": "$\\frac{3}{8}$"},
    {"text": "$\\frac{4}{8}$"},
    {"text": "$\\frac{4}{4}$"},
    {"text": "$1$"}
  ],
  "answer": {
    "type": "single",
    "correct_index": 3
  }
}
```

**Note:** Use double backslashes `\\` in JSON strings!

### Hint with Math

```json
{
  "item_id": 1,
  "hints": [
    {
      "level": 1,
      "text": "Tel de tellers bij elkaar op: $3 + 1 = ?$",
      "cost_points": 0
    },
    {
      "level": 2,
      "text": "De noemers blijven hetzelfde: $\\frac{4}{4}$",
      "cost_points": 1
    },
    {
      "level": 3,
      "text": "$\\frac{4}{4} = 1$ (hele taart)",
      "cost_points": 2
    }
  ]
}
```

## Best Practices

### 1. Keep It Simple

Don't overuse math notation. Use it only where it adds clarity:

**Good:**
```
"Bereken: $8 + 7$"
```

**Overkill:**
```
"Bereken: $8$ $+$ $7$"
```

### 2. Use Spaces

Add spaces around operators in LaTeX for readability:

**Good:**
```
"$5 \times 6 = 30$"
```

**Hard to read:**
```
"$5\times6=30$"
```

### 3. Escape Backslashes in JSON

Always use double backslashes in JSON:

**Correct:**
```json
{"text": "$\\frac{1}{2}$"}
```

**Wrong:**
```json
{"text": "$\frac{1}{2}$"}  ← Will not work!
```

### 4. Test in Browser

After creating exercises, always test in the actual quiz to verify rendering.

## Advanced Features

### Aligned Equations

```
$$
\begin{align}
2x + 5 &= 13 \\
2x &= 8 \\
x &= 4
\end{align}
$$
```

### Matrices (for advanced math)

```
$\begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}$
```

### Geometry

```
"De oppervlakte van een cirkel: $A = \pi r^2$"
"De omtrek van een rechthoek: $O = 2l + 2b$"
```

## Troubleshooting

### Math Not Rendering

**Problem:** Text shows as `$\frac{1}{2}$` instead of rendering

**Solutions:**
1. Check double backslashes in JSON: `\\frac` not `\frac`
2. Verify KaTeX is loaded (check browser console)
3. Make sure dollar signs are present
4. Check LaTeX syntax (KaTeX is strict!)

### Invalid LaTeX

**Problem:** KaTeX error in console

**Solutions:**
1. Verify LaTeX syntax at https://katex.org/
2. Common errors:
   - Missing braces: `\frac12` → `\frac{1}{2}`
   - Unescaped percent: `25%` → `25\%`
   - Wrong command: `\multiplication` → `\times`

### Text Looks Weird

**Problem:** Math renders but looks odd

**Solutions:**
1. Use inline `$...$` not display `$$...$$` in questions
2. Add spaces around operators
3. Don't mix plain text and LaTeX: `3/4` vs `$\frac{3}{4}$` (pick one style)

## Migration from Plain Text

To convert existing exercises, use the conversion script:

```bash
python3 scripts/convert-math-notation.py \
  --file data-v2/exercises/gb/gb_groep4_m4_core.json \
  --output data-v2/exercises/gb/gb_groep4_m4_core_katex.json
```

The script will:
- Convert `3/4` → `$\frac{3}{4}$`
- Convert `x` → `$\times$`
- Convert `^2` → `$^2$`
- Preserve non-math text

## Further Reading

- **KaTeX Documentation:** https://katex.org/docs/supported.html
- **LaTeX Math Symbols:** https://katex.org/docs/support_table.html
- **LaTeX Tutorial:** https://www.overleaf.com/learn/latex/Mathematical_expressions

---

**Quick Reference Card**

| What | LaTeX | Example |
|------|-------|---------|
| Fraction | `\frac{a}{b}` | `$\frac{3}{4}$` |
| Multiply | `\times` | `$5 \times 6$` |
| Divide | `\div` | `$20 \div 4$` |
| Squared | `^2` | `$x^2$` |
| Root | `\sqrt{x}` | `$\sqrt{16}$` |
| Percent | `\%` | `$25\%$` |

**Remember:** Use `\\` in JSON, `\` everywhere else!
