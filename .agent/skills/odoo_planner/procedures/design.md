# Procedure: Design Phase

**Context**: Drafting the `day_XX_[topic].md` file.

## Quality Standards (NON-NEGOTIABLE)

1.  **100% Coverage**: The lesson must cover every sub-topic listed in the Roadmap.
2.  **No Toy Examples**:
    -   ❌ BAD: "Create a field `name`."
    -   ✅ GOOD: "Create a computed field `total_amount` that depends on `lines.subtotal`, handles currency, and recomputes on currency change."
3.  **Source-First**: Every concept explanation must reference a specific file and line number in `odoo/` source code that the student will read.

## Template Construction

Use the template at `.agent/learning/daily_template.md`.

### Section 1: Concepts (The "Why" & "How")
-   Define **10-15 concepts**.
-   Structure: Definition -> Source Code Ref -> Odoo vs Python/FastAPI comparison -> Gotchas.

### Section 2: Exercises (The "Do")
-   Define **5+ Exercises**.
-   **Must Include**:
    -   Scenario (Business Requirement)
    -   Technical Constraints (e.g., "Must use `api.depends`", "Must not use loop")
    -   **Validation Steps**: How does the student know it works? (e.g., "Check logs", "UI updates instantly")

### Section 3: Questions (The "Test")
-   Define **8-10 Questions**.
-   Focus on **Debugging** and **Architecture**, not just syntax memorization.

## Final Review & Validation (SCRIPT)

Before saving and finishing, you MUST run the validation script against your draft.
If you are drafting in memory/scratchpad, write it to a temp file first or the final path.

```bash
python3 .agent/skills/odoo_planner/scripts/validate_lesson.py .agent/learning/daily_notes/day_XX_[topic].md
```

-   **Pass**: Commit and Notify User.
-   **Fail**: Refine the content (Add more concepts/exercises) until it passes.

