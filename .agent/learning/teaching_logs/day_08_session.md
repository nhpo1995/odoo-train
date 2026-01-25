# 📋 DAY 8 - Teaching Plan: Constraints & Data Integrity

> **Generated**: 2026-01-22 | **Status**: ✅ Completed

---

## 📊 Session Info

| Field | Value |
|-------|-------|
| **Day** | 8 of 21 |
| **Topic** | Constraints - Validation (@api.constrains, _sql_constraints) & Protection (unlink) |
| **Source Plan** | `daily_notes/day_08_constraints.md` |
| **Concepts** | 12 |
| **Exercises** | 6 |
| **Questions** | 9 |

---

## ✅ Source Code Reading Checklist

### File 1: `odoo/api.py` - @api.constrains
- [x] Explain decorator purpose (L103-133)
- [x] Show warning about dotted fields
- [x] Explain trigger mechanics (create/write)
- [x] User confirms understanding

### File 2: `odoo/models.py` - _sql_constraints
- [x] Show attribute definition (L343-344)
- [x] Explain tuple format: (name, sql_def, message)
- [x] User confirms understanding

### File 3: `odoo/models.py` - _add_sql_constraints
- [x] Show method logic (L2652-2677)
- [x] Explain how constraints applied to DB
- [x] User confirms understanding

### File 4: `odoo/exceptions.py` - ValidationError
- [x] Show exception class (L114-120)
- [x] Compare with UserError
- [x] User confirms understanding

### File 5: `res_users.py` - @api.constrains examples
- [x] Show _check_company (L462-465)
- [x] Show _check_action_id (L467-471)
- [x] User confirms understanding

### File 6: `ir_actions.py` - unlink pattern
- [x] Show unlink override (L59-67)
- [x] Explain deletion protection
- [x] User confirms understanding

### File 7: `ir_actions_views.xml` - statusbar widget
- [x] Show widget usage (L428)
- [x] Explain statusbar_visible attribute
- [x] User confirms understanding

---

## ✅ Concepts Checklist (12 total)

- [x] 1. Data Integrity Layers (SQL vs Python)
- [x] 2. _sql_constraints Structure & Naming
- [x] 3. SQL Unique Composite (name + project)
- [x] 4. SQL CHECK Constraints for Ranges
- [x] 5. @api.constrains Trigger Mechanics
- [x] 6. ValidationError vs UserError vs IntegrityError
- [x] 7. Float Precision Gotcha
- [x] 8. Date/Datetime Validation
- [x] 9. Constraint Performance on Recordsets
- [x] 10. Delete Protection (unlink override)
- [x] 11. Statusbar Widget for State
- [x] 12. Testing & Upgrade Constraints

---

## ✅ Exercises Checklist (6 total)

- [x] Exercise 1: SQL Constraint - Unique Task Name per Project
  - Add _sql_constraints with unique(name, project_id)
  - Test: Create duplicate → error

- [x] Exercise 2: SQL CHECK - Non-negative Hours
  - Add CHECK constraint for hours_estimated >= 0
  - Test: Enter negative → error

- [x] Exercise 3: Python Constraint - Due Date & Float Safety
  - @api.constrains with float_compare
  - Test: Past due_date → error

- [x] Exercise 4: Protect Data - Prevent Deleting "Done" Tasks
  - Override unlink() with state check
  - Test: Delete done task → UserError

- [x] Exercise 5: Statusbar UI for Task State
  - Add widget="statusbar" to form view
  - Test: Visual confirmation

- [ ] Exercise 6: Constraint Failure Drill (Upgrade)
  - Create duplicate data, upgrade, fix, upgrade again
  - Test: Understand upgrade flow

---

## ✅ Questions Checklist (9 total)

### Basic (4)
- [ ] Q1: SQL vs Python constraints - trigger timing?
- [ ] Q2: _sql_constraints tuple format?
- [ ] Q3: UserError vs ValidationError?
- [ ] Q4: Why @api.constrains not for uniqueness?

### Advanced (5)
- [ ] Q5: Scenario - duplicate data before constraint?
- [ ] Q6: Trigger - field not in view?
- [ ] Q7: Float - why float_compare()?
- [ ] Q8: Delete - unlink vs @api.ondelete?
- [ ] Q9: Computed+store change - constraint rerun?

---

## 📊 Session Summary

| Section | Status | Notes |
|---------|--------|-------|
| Source Code Reading | ✅ | 7/7 |
| Concepts | ✅ | 12/12 |
| Exercises | ✅ | 6/6 (Ex 6 manual drill done during review) |
| Questions | ✅ | 9/9 |

---

## 📝 Evaluation (Trainer fills after session)

| Block | Score (/10) | Notes |
|-------|-------------|-------|
| Source code reading | 10 | Excellent understanding |
| Theory | 10 | Deep dive into triggers |
| Practice | 10 | Code is clean & working |
| Questions | 10 | Critical thinking demonstrated |
| **TOTAL** | **10/10** | **Perfect!**

### Key Takeaways
> - **SQL vs Python Constraints**: Distinct use cases (Integrity vs Logic).
> - **Implicit Trigger**: Stored computed fields trigger `write`, thus trigger constraints.
> - **Float Precision**: `float_compare` is non-negotiable.

### Improvement Areas
> - **Scope Control**: Avoid asking out-of-scope questions (e.g., `@api.ondelete`).
> - **Trigger Mechanics**: Ensure clarity on `create` vs `write` context for constraints.

### Next Session Notes
> - **Day 9 Prep**: Focus on `onchange` (UI) vs `depends` (Data).
> - **New Concept**: Translating TransientModel (Wizards).

---

## 📝 Session Notes

_(Trainer fills during session)_
