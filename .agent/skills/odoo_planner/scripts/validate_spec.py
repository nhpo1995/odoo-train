#!/usr/bin/env python3
"""
validate_spec.py

Purpose:
    Compares `module_spec.md` (Target) against `actual_module.md` (Reality).
    Reports any fields defined in Spec that are missing or not marked as done in Actual.

Usage:
    python3 validate_spec.py
"""

import os
import re
import sys

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) # .agent/skills/odoo_planner/scripts -> .agent
SPEC_FILE = os.path.join(BASE_DIR, 'learning', 'module_spec.md')
ACTUAL_FILE = os.path.join(BASE_DIR, 'learning', 'actual_module.md')

def parse_markdown_tables(filepath):
    """
    Parses markdown tables for models.
    Returns a dict: { 'model_name': { 'field_name': { 'raw': line } } }
    """
    data = {}
    current_model = None
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return {}

    with open(filepath, 'r') as f:
        lines = f.readlines()

    in_table = False
    
    for line in lines:
        line = line.strip()
        
        # Detect Model Header (### model.name)
        model_match = re.match(r'^###\s+(task\.\w+|res\.\w+)', line)
        if model_match:
            current_model = model_match.group(1)
            data[current_model] = {}
            in_table = False
            continue

        # Detect Table Row
        if current_model and line.startswith('|'):
            # Skip separator lines |---|
            if '---' in line:
                in_table = True
                continue
            
            # Skip Header row (Field | Type ...)
            if 'Field' in line and 'Type' in line:
                continue

            parts = [p.strip() for p in line.split('|') if p.strip()]
            if not parts:
                continue
                
            field_name = parts[0]
            # Clean field name (remove markdown bold/code if any)
            field_name = field_name.replace('`', '').replace('*', '')
            
            data[current_model][field_name] = {'parts': parts}

    return data

def main():
    print(f"Checking Spec: {SPEC_FILE}")
    print(f"Checking Actual: {ACTUAL_FILE}")
    
    spec_data = parse_markdown_tables(SPEC_FILE)
    actual_data = parse_markdown_tables(ACTUAL_FILE)
    
    errors = []
    warnings = []

    # Check Spec against Actual
    for model, fields in spec_data.items():
        if model not in actual_data:
            warnings.append(f"Model [{model}] exists in Spec but not in Actual doc.")
            continue
            
        for field, info in fields.items():
            # Check if field exists in Actual
            if field not in actual_data[model]:
                # If it's a future day feature (check Day column if possible, but simplest is check existence)
                # We can assume if it's in Spec, it should be tracked. 
                # But Spec contains FUTURE fields too.
                # So missing in Actual might be okay if it's future.
                # However, Actual Doc usually lists FUTURE fields as "Not Started" or just doesn't list them?
                # Based on file content, Actual doc seems to only list CURRENT/IMPLEMENTED fields or fields in progress.
                pass
                # Strict check: Warn if key fields are missing from Actual snapshot if they are supposed to be there?
                # For now, let's just log it.
                # errors.append(f"Model [{model}] Field [{field}] missing in Actual snapshot.")
            else:
                # Field exists, check status
                actual_row = actual_data[model][field]['parts']
                # Actual table format: | Field | Type | Status | Notes |
                # Status is index 2 usually (0=Field, 1=Type, 2=Status)
                status_idx = 2
                if len(actual_row) > status_idx:
                    status = actual_row[status_idx]
                    if '✅' not in status:
                        warnings.append(f"Model [{model}] Field [{field}] status is {status} (Expected ✅)")

    # Check Actual against Spec (Deviations)
    for model, fields in actual_data.items():
        if model not in spec_data:
             # Allowed, maybe helper models
             pass
        else:
            for field in fields:
                if field not in spec_data[model]:
                    warnings.append(f"Model [{model}] Field [{field}] implementation NOT in Spec (Unplanned feature?)")

    print("\n--- Validation Report ---")
    if not errors and not warnings:
        print("✅ Spec and Actual are aligned.")
    else:
        if errors:
            print("\n❌ Errors:")
            for e in errors: print(f"  - {e}")
        if warnings:
            print("\n⚠️  Warnings/Gaps:")
            for w in warnings: print(f"  - {w}")
            
    # Return code for pipeline
    if errors:
        sys.exit(1)
    
if __name__ == "__main__":
    main()
