# Procedure: Pre-Teaching Preparation

**Context**: You cannot teach what you haven't read.

## Step 1: Read the Lesson Plan
**Action**: Read `.agent/learning/daily_notes/day_XX_*.md`
-   Identify all 10-15 concepts.
-   Identify all 5+ exercises.
-   Identify specific source files referenced.

## Step 2: Read Source Code (MANDATORY)
**Action**: Call `view_file` on EVERY Odoo reference mentioned in the lesson plan.
-   *Why?* To explain line numbers accurately.
-   *Rule*: Do NOT skip this. You will be penalized if you hallucinate line numbers.

## Step 3: Check Actual State
**Action**: Read `.agent/learning/actual_module.md`
-   *Why?* To know if the student has previous day's code ready.

## Readiness Gate
Only proceed to greet the user ("Hi, let's start Day X") AFTER you have performed the above `view_file` calls.
