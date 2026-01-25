# Procedure: Research Phase

**Context**: Before creating any lesson plan, you must gather facts to ensure the lesson is grounded in reality, not hallucination.

## Step 1: Strict Context Loading (MANDATORY)

You must read these files in order. Do not proceed until you have read them.

1.  **Target**: Read `.agent/learning/module_spec.md`
    -   *Goal*: What features *should* exist by this day?
2.  **Reality**: Read `.agent/learning/actual_module.md`
    -   *Goal*: What features *actually* exist?
    -   *Gap*: Note any missing features from previous days.
3.  **Schedule**: Read `.agent/learning/odoo_roadmap.md`
    -   *Goal*: What is the specific topic for today?
4.  **History**: Read `.agent/learning/daily_notes/day_XX_*.md` (Previous Day)
    -   *Goal*: Check "Evaluation" & "Issues for Next Day".

## Step 2: Automated Reality Check (SCRIPT)

Run the validation script to see if the spec matches the code.

```bash
python3 .agent/skills/odoo_planner/scripts/validate_spec.py
```

-   If the script reports errors (mismatch): **Stop.** You must update `module_spec.md` or note these gaps to be fixed in the new lesson plan.
-   If the script passes: Proceed.

## Step 3: Knowledge Acquisition (Context7)

**Rule**: You generally do NOT know enough about Odoo internals just from training data. You MUST query Context7.

**Action**:
1.  Check if a reference guide exists in `.agent/learning/references/`.
2.  If NOT, perform **at least 2 queries** to Context7:
    -   Query 1: Overview & Best Practices (`libraryId='/websites/odoo'`)
    -   Query 2: Advanced patterns & specific gotchas.
3.  **Synthesize**: If you queried Context7, CREATE a new reference file at `.agent/learning/references/[topic].md` so you don't have to query again next time.

## Checkpoint
-   [ ] Know the Target (Spec)
-   [ ] Know the Reality (Actual Code)
-   [ ] Know the Knowledge (Context7/Docs)

-> Proceed to **Design Phase**.
