# 🧑‍🏫 TEACHING PLAN: Day 9 - Onchange & Wizards

**Status**: 🟡 In Progress
**Learner**: Phong
**Date**: 2026-01-25

---

## 0. PREPARATION CHECKLIST

- [ ] **Read Module Spec**: features align with Day 9 (Wizard, Onchange, read_group)
- [ ] **Read Daily Plan**: `day_09_onchange_wizard.md`
- [ ] **Read Actual Module**: confirmed current state (Day 8 completed)
- [ ] **Understand Goal**: Build "Batch Update" wizard + UI auto-fill features

---

## 1. SOURCE CODE READING (Just-in-Time)

### 1.1. `@api.onchange` Decorator
- [ ] **File**: `odoo/api.py`
- [ ] **Search**: `def onchange`
- [ ] **Focus**: Decorator logic, how it marks method for UI trigger.
- [ ] **Explain**: "UI-only trigger", not database-level constraint.

### 1.2. `TransientModel`
- [ ] **File**: `odoo/models.py`
- [ ] **Search**: `class TransientModel`
- [ ] **Focus**: Inheritance from BaseModel, simplified access rights, vacuum.
- [ ] **Explain**: "Temporary data", "Vacuum cron job".

### 1.3. Onchange Example
- [ ] **File**: `odoo/addons/base/models/res_partner.py`
- [ ] **Search**: `def onchange_state` (or similar simple onchange)
- [ ] **Focus**: How it updates fields in `self`.
- [ ] **Explain**: `self` is a virtual record here.

### 1.4. Wizard Example
- [ ] **File**: `odoo/addons/crm/wizard/crm_lead_lost.py` (or similar simple wizard)
- [ ] **Focus**: TransientModel definition, `action_lost_reason_apply` method.
- [ ] **Explain**: `target='new'`, `binding_model_id` (if present).

---

## 2. CONCEPTS TEACHING (100% Coverage)

### 🟢 Core Concepts
- [ ] **Concept 1: @api.onchange**
  - Trigger: UI interaction ONLY.
  - Virtual record: `self` is not in DB yet (for creates).
- [ ] **Concept 2: Onchange Warning & Domain**
  - Return `{'warning': ...}` or `{'domain': ...}`.
  - User can ignore warning (unlike Constraint).
- [ ] **Concept 3: TransientModel**
  - Temporary data, auto-vacuum.
  - Access rights: simpler (usually user sees own).
- [ ] **Concept 4: Wizard Action (target='new')**
  - Dialog/Popup mode.
- [ ] **Concept 5: Context & active_ids**
  - Passing data from source view to Wizard.
  - `active_ids`, `active_model`.
- [ ] **Concept 6: Binding Actions (binding_model_id)**
  - Adding to "Action" menu automatically.

### 🟡 Advanced Topics
- [ ] **Advanced 1: read_group vs Loop**
  - `read_group`: SQL GROUP BY (Fast).
  - Loop: Python iteration (Slow).

### ⚠️ Gotchas
- [ ] **Mistake 1**: Expecting Onchange to run on `create()` code.
- [ ] **Mistake 2**: Persistent Model -> O2M -> TransientModel (Forbidden).
- [ ] **Mistake 3**: Relying on Wizard data persistence.

---

## 3. EXERCISES (Hands-on)

### Ex 1: Basic Onchange - UX Improvement
- [ ] **Goal**: Auto-fill `assigned_user_id` from `project_id`.
- [ ] **Steps**: Add `@api.onchange('project_id')`.
- [ ] **Verify**: Select Project -> User changes.

### Ex 2: Onchange Warning
- [ ] **Goal**: Warn if Project has no Manager.
- [ ] **Steps**: Return `{'warning': ...}` in onchange.
- [ ] **Verify**: Select empty Project -> Popup warning.

### Ex 3: Financial Fields (read_group)
- [ ] **Goal**: `amount` (Task) & `total_revenue` (Project).
- [ ] **Steps**: Add fields. Implement `_compute_total_revenue` using `read_group`.
- [ ] **Verify**: Check computed value matches sum.

### Ex 4: Bulk Update Wizard (Model)
- [ ] **Goal**: `task.state.wizard` model.
- [ ] **Steps**: `new_state` field, `action_apply` using `active_ids`.
- [ ] **Verify**: Code compiles, model exists.

### Ex 5: Wizard View & Binding
- [ ] **Goal**: Form view + Action + Menu bind.
- [ ] **Steps**: XML view, Act Window with `binding_model_id`.
- [ ] **Verify**: Select tasks -> Action -> Batch Update.

---

## 4. QUESTIONS (Evaluation)

### Easy
- [ ] Q1: When does `@api.onchange` run?
- [ ] Q2: Difference between TransientModel and Model?
- [ ] Q3: Action attribute for Popup?

### Medium
- [ ] Q4: Usage of `active_ids`?
- [ ] Q5: Why `read_group` over loop?
- [ ] Q6: Code `read_group` syntax?

### Hard
- [ ] Q7: Scenario: Onchange + Warning + Logic design.
- [ ] Q8: Debug: Wizard data missing?
- [ ] Q9: Design: Server Action vs Wizard?

---

## 5. SESSION SUMMARY

**Score**: _/10
**Evaluation**:
<!-- To be filled after session -->

**Notes**:
<!-- Observations -->
