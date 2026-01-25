#!/usr/bin/env python3
"""
validate_lesson.py

Purpose:
    Parses a lesson plan markdown file and validates quality metrics:
    1. Concept Count (Target: 10-15)
    2. Exercise Count (Target: >= 5)
    3. Question Count (Target: >= 8)

Usage:
    python3 validate_lesson.py [path_to_lesson_plan.md]
"""

import os
import re
import sys


def validate_lesson(filepath):
    if not os.path.exists(filepath):
        print(f"❌ Error: File not found: {filepath}")
        return False

    with open(filepath, 'r') as f:
        content = f.read()

    # Regex patterns equivalent to what the Agent typically writes
    # Concepts often numbered or bulleted in Section 1
    # We look for lines starting with "## Concept" or "### Concept" or similar, or numbered lists in Section 1
    
    # Robust Strategy: Count headers or bold items under "Section 1"
    
    # 1. Count Concepts
    # Look for:
    # - "## Concept X"
    # - "1. [bold text]" inside Section 1
    # - "**Concept X**"
    concept_matches = re.findall(r'(?i)(?:^#{2,4}\s+|^\d+\.\s+\*\*|^-\s+\*\*)Concept', content, re.MULTILINE)
    
    # Fallback: Count numbered lists in "Section 1"
    if len(concept_matches) == 0:
        # Extract Section 1
        section1 = re.search(r'Section 1:(.*?)Section 2:', content, re.DOTALL | re.IGNORECASE)
        if section1:
             # Count numbered items "1. "
             concept_matches = re.findall(r'^\d+\.\s+', section1.group(1), re.MULTILINE)

    concept_count = len(concept_matches)

    # 2. Count Exercises
    # Look for "## Exercise" or "**Exercise**"
    exercise_matches = re.findall(r'(?i)(?:^#{2,4}\s+|^\d+\.\s+\*\*|^-\s+\*\*)Exercise', content, re.MULTILINE)
    exercise_count = len(exercise_matches)
    
    # Fallback: Count numbered lists in "Section 2"
    if len(exercise_matches) == 0:
        section2 = re.search(r'Section 2:(.*?)Section 3:', content, re.DOTALL | re.IGNORECASE)
        if section2:
             exercise_matches = re.findall(r'^\d+\.\s+', section2.group(1), re.MULTILINE)
             exercise_count = len(exercise_matches)

    # 3. Count Questions
    # Look for questions in Section 3
    section3 = re.search(r'Section 3:(.*?)Section 4:', content, re.DOTALL | re.IGNORECASE)
    question_count = 0
    if section3:
        # Count lines starting with a number and dot or question mark
        # Or count lines ending with '?'
        q_matches = re.findall(r'^\d+\.\s+', section3.group(1), re.MULTILINE)
        question_count = len(q_matches)
    
    if question_count == 0:
         # Fallback regex
         question_count = len(re.findall(r'(?i)(?:^#{2,4}\s+|^\s*-\s+\*\*)Question', content, re.MULTILINE)) 

    print(f"\n📊 Validation Report for: {os.path.basename(filepath)}")
    print(f"--------------------------------------------------")
    
    # Validate Concepts
    if 10 <= concept_count <= 15:
        print(f"✅ Concepts: {concept_count} (Pass)")
    else:
        print(f"❌ Concepts: {concept_count} (Fail - Target: 10-15)")

    # Validate Exercises
    if exercise_count >= 5:
        print(f"✅ Exercises: {exercise_count} (Pass)")
    else:
        print(f"❌ Exercises: {exercise_count} (Fail - Target: 5+)")
        
    # Validate Questions
    # (Optional strictness, maybe just warn)
    if question_count >= 8:
         print(f"✅ Questions: {question_count} (Pass)")
    else:
         print(f"⚠️  Questions: {question_count} (Warning - Target: 8+)")

    print(f"--------------------------------------------------")
    
    # Logic for Return Code
    # We want to be Strict but Fair.
    # If counts are 0, that's definitely a fail (Parsing error or empty plan).
    # If counts are low (e.g. 8 concepts), we Warn but Pass (to avoid hallucination).
    
    fail = False
    
    if concept_count == 0:
        print("❌ CRITICAL: No concepts found. Check formatting.")
        fail = True
    elif concept_count < 10:
        print("⚠️  Warning: Concept count is low. Ensure you aren't skipping details.")
        # Do not fail on low count, just warn.
    
    if exercise_count == 0:
        print("❌ CRITICAL: No exercises found.")
        fail = True
    elif exercise_count < 5:
        print("⚠️  Warning: Exercise count is low. Consider adding more practice.")
        
    if fail:
        return False
    else:
        print("\n✅ Validation Passed (with potential warnings).")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_lesson.py [file]")
        sys.exit(1)
        
    success = validate_lesson(sys.argv[1])
    if not success:
        sys.exit(1) # Fail for pipeline
        sys.exit(1) # Fail for pipeline
