# 📋 DAY 8 - Teaching Plan: Constraints & Data Integrity

> **Generated**: 2026-01-22 | **Status**: 🟡 In Progress

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
- [ ] Explain decorator purpose (L103-133)
- [ ] Show warning about dotted fields
- [ ] Explain trigger mechanics (create/write)
- [ ] User confirms understanding

### File 2: `odoo/models.py` - _sql_constraints
- [ ] Show attribute definition (L343-344)
- [ ] Explain tuple format: (name, sql_def, message)
- [ ] User confirms understanding

### File 3: `odoo/models.py` - _add_sql_constraints
- [ ] Show method logic (L2652-2677)
- [ ] Explain how constraints applied to DB
- [ ] User confirms understanding

### File 4: `odoo/exceptions.py` - ValidationError
- [ ] Show exception class (L114-120)
- [ ] Compare with UserError
- [ ] User confirms understanding

### File 5: `res_users.py` - @api.constrains examples
- [ ] Show _check_company (L462-465)
- [ ] Show _check_action_id (L467-471)
- [ ] User confirms understanding

### File 6: `ir_actions.py` - unlink pattern
- [ ] Show unlink override (L59-67)
- [ ] Explain deletion protection
- [ ] User confirms understanding

### File 7: `ir_actions_views.xml` - statusbar widget
- [ ] Show widget usage (L428)
- [ ] Explain statusbar_visible attribute
- [ ] User confirms understanding

---

## ✅ Concepts Checklist (12 total)

- [ ] 1. Data Integrity Layers (SQL vs Python)
- [ ] 2. _sql_constraints Structure & Naming
- [ ] 3. SQL Unique Composite (name + project)
- [ ] 4. SQL CHECK Constraints for Ranges
- [ ] 5. @api.constrains Trigger Mechanics
- [ ] 6. ValidationError vs UserError vs IntegrityError
- [ ] 7. Float Precision Gotcha
- [ ] 8. Date/Datetime Validation
- [ ] 9. Constraint Performance on Recordsets
- [ ] 10. Delete Protection (unlink override)
- [ ] 11. Statusbar Widget for State
- [ ] 12. Testing & Upgrade Constraints

---

## ✅ Exercises Checklist (6 total)

- [ ] Exercise 1: SQL Constraint - Unique Task Name per Project
  - Add _sql_constraints with unique(name, project_id)
  - Test: Create duplicate → error

- [ ] Exercise 2: SQL CHECK - Non-negative Hours
  - Add CHECK constraint for hours_estimated >= 0
  - Test: Enter negative → error

- [ ] Exercise 3: Python Constraint - Due Date & Float Safety
  - @api.constrains with float_compare
  - Test: Past due_date → error

- [ ] Exercise 4: Protect Data - Prevent Deleting "Done" Tasks
  - Override unlink() with state check
  - Test: Delete done task → UserError

- [ ] Exercise 5: Statusbar UI for Task State
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
| Source Code Reading | ⏳ | 0/7 |
| Concepts | ⏳ | 0/12 |
| Exercises | ⏳ | 0/6 |
| Questions | ⏳ | 0/9 |

---

## 📝 Evaluation (Trainer fills after session)

| Block | Score (/10) | Notes |
|-------|-------------|-------|
| Source code reading | _ | |
| Theory | _ | |
| Practice | _ | |
| Questions | _ | |
| **TOTAL** | **_/10** | |

### Key Takeaways
> _

### Areas to Improve
> _

### Notes for Day 9
> _

---

## 📝 Session Notes

_(Trainer fills during session)_
