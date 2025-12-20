#!/usr/bin/env python3
"""
Fix decimal notation in Dutch text fields to use comma instead of period.

Rules:
1. Text fields (content, text, foutanalyse, berekening, uitleg, etc.) should use:
   - Comma for decimals: 1,5 (not 1.5)
   - Period for thousands: 1.200 (keep as is)
2. JSON number values keep period: "factor": 1.5
3. Money formatting: €240.0 → €240,00 or €240
"""

import json
import re
import sys


def fix_money_notation(text):
    """Fix money notation: €240.0 → €240,00 and €14.4 → €14,40"""
    # Pattern: €NUMBER.DECIMAL where DECIMAL is 1-2 digits
    def replace_money(match):
        amount = match.group(1)
        # Split on decimal point
        parts = amount.split('.')
        if len(parts) == 2:
            integer_part = parts[0]
            decimal_part = parts[1]
            # Pad decimal part to 2 digits
            decimal_part = decimal_part.ljust(2, '0')
            return f"€{integer_part},{decimal_part}"
        return match.group(0)

    # Match €NUMBER.NUMBER (not €1.200 which is thousands)
    # Only match if decimal part is 1-2 digits
    text = re.sub(r'€(\d+\.\d{1,2})(?!\d)', replace_money, text)
    return text


def fix_decimal_notation(text):
    """Fix decimal notation: 1.5 → 1,5 but keep 1.200 (thousands)"""
    # Match NUMBER.DECIMAL where DECIMAL is 1-2 digits (not thousands like 1.200)
    # Don't match if already in JSON value context or if it's thousands

    # Pattern: digit(s).digit(1-2) not followed by more digits
    def replace_decimal(match):
        full_match = match.group(0)
        number = match.group(1)
        decimal = match.group(2)

        # If decimal part has 3+ digits, it might be thousands notation (keep it)
        if len(decimal) >= 3:
            return full_match

        # Replace period with comma
        return f"{number},{decimal}"

    # Match numbers like 1.5, 12.75, 0.5 (but not 1.200, 84.000)
    text = re.sub(r'(\d+)\.(\d{1,2})(?!\d)', replace_decimal, text)
    return text


def fix_text_field(value):
    """Fix notation in a text field value"""
    if not isinstance(value, str):
        return value

    # First fix money notation
    value = fix_money_notation(value)
    # Then fix other decimals
    value = fix_decimal_notation(value)

    return value


def process_value(value, is_text_field=False):
    """Recursively process JSON values"""
    if isinstance(value, dict):
        return {k: process_value(v, k in [
            'text', 'foutanalyse', 'content', 'berekening',
            'uitleg', 'concept', 'hint', 'antwoord', 'logica_check',
            'hoofdvraag', 'resultaat'
        ]) for k, v in value.items()}
    elif isinstance(value, list):
        return [process_value(item, is_text_field) for item in value]
    elif is_text_field and isinstance(value, str):
        return fix_text_field(value)
    else:
        return value


def main():
    if len(sys.argv) != 3:
        print("Usage: python fix_decimal_notation.py input.json output.json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Read JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Process all values
    fixed_data = process_value(data)

    # Write back with same formatting
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=2)

    print(f"Fixed decimal notation in {input_file} → {output_file}")


if __name__ == '__main__':
    main()
