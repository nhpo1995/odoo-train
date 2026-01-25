# Procedure: Pre-Teaching Preparation

**Context**: You cannot teach what you haven't read.

## Step 1: Read the Lesson Plan
**Action**: Read `.agent/learning/daily_notes/day_XX_*.md`
-   Identify all 10-15 concepts.
-   Identify all 5+ exercises.
-   Identify specific source files referenced.

## Step 1.5: Knowledge Base Lookup (MANDATORY)
**Action**: Before reading source code, check if you have the theoretical knowledge.
1.  **Check References**: Look in `.agent/learning/references/` for relevant topic guides.
    -   *Found?* Read them to refresh memory.
    -   *Missing?* Proceed to Query.
2.  **Query Context7 (If Missing)**:
    -   Use `mcp_context7_query-docs` to get official documentation/best practices.
    -   *Example*: `query='odoo [topic] best practices'`
3.  **Save Reference**:
    -   Create a new file `.agent/learning/references/[topic_slug]_guide.md`.
    -   Save the Context7 insights there for future use.
    -   *Why?* To save context tokens for next time.

## Step 2: Read Source Code (MANDATORY)
**Action**: Call `view_file` on EVERY Odoo reference mentioned in the lesson plan.
-   *Why?* To explain line numbers accurately.
-   *Rule*: Do NOT skip this. You will be penalized if you hallucinate line numbers.

## Step 3: Check Actual State
**Action**: Read `.agent/learning/actual_module.md`
-   *Why?* To know if the student has previous day's code ready.

## Readiness Gate
Only proceed to greet the user ("Hi, let's start Day X") AFTER you have performed the above `view_file` calls.
