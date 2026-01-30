# 📋 Teaching Plan: Day 16 - Model Inheritance

> **Status**: 🟡 In Progress
> **Date**: 2026-01-30
> **Trainer**: AI Odoo Mentor

---

## 0. Introduction
- [x] Introduction & Context
- [x] Show Overview
- [x] Confirm Readiness

## 1. 📂 Source Code Reading

| File | Focus | Line Range | Done |
|------|-------|------------|------|
| `odoo/models.py` | `def create` | Search `def create` | [x] |
| `odoo/models.py` | `def write` | Search `def write` | [x] |
| `odoo/models.py` | `def unlink` | Search `def unlink` | [x] |
| `odoo/models.py` | `def copy` | Search `def copy` | [x] |
| `odoo/models.py` | `@model_create_multi` | Search `def model_create_multi` | [x] |

---

## 2. 🧠 Concepts (100% Coverage)

### 2.1 Model Inheritance
- [x] **1.1 Model Inheritance (`_inherit`)**
  - Context: Extending existing models (e.g., res.partner) to add new business logic.
  - Explain: `_inherit` works like a patch.
  - Verify: "What happens to the existing data when you add a field via inheritance?"

### 2.2 Override Patterns
- [x] **1.2 Override Pattern**
  - Context: Modifying standard behavior (create/write/unlink).
  - Key: `super().method()`.
  - Verify: "Why do we need to call super()?"

- [x] **1.3 super() Positioning**
  - Context: Deciding when to execute custom logic (Validation vs Post-processing).
  - Verify: "When should you put code BEFORE super()?"

- [x] **1.4 Common Bugs**
  - Context: Avoiding pitfalls.
  - List: Missing return, modifying vals too late, infinite loops, wrong self.
  - Verify: "What causes a RecursionError in `write()`?"

### 2.3 Other Inheritance Types
- [x] **1.5 Prototype Inheritance (`_name` + `_inherit`)**
  - Context: Copying features to a NEW model.
  - Verify: "Does this affect the original model?"

- [x] **1.6 Delegation Inheritance (`_inherits`)**
  - Context: Embedding another model (Transparent inheritance).
  - Verify: "How is this different from regular Many2one?"

---

## 3. 💻 Exercises (Hands-on)

> **Requirement**: Learner TỰ VIẾT code. No copy-paste.

### 🟢 Basic
- [x] **Exercise 1: Extend res.partner**
  - Task: Add `task_ids` (O2M) and `task_count` (Compute) to `res.partner`.
  - Goal: Practice basic extension.

- [x] **Exercise 2: Override create() - Auto Sequence**
  - Task: Generate code 'TASK-001' on create if not provided.
  - Goal: Pre-process vals.

- [x] **Exercise 3: Override write() - Track State**
  - Task: Set `completion_date` when state becomes 'done'.
  - Goal: Inspect vals in write.

- [x] **Exercise 4: Override unlink() - Prevent Delete**
  - Task: Raise error if deleting 'done' tasks.
  - Goal: Validation before super.

### 🟡 Debugging (Fix Bugs)
- [ ] **Exercise 5: Fix Bug - Missing Return**
  - Task: Fix code that forgets `return super()`.
  
- [ ] **Exercise 6: Fix Bug - Wrong self in create**
  - Task: Fix code trying to use `self` inside `create`.

- [ ] **Exercise 7: Fix Bug - Infinite Loop**
  - Task: Fix `write` triggering `write`.

### 🔴 Advanced
- [x] **Exercise 8: Override copy()**
  - Task: Add "(Copy)" suffix and reset state/dates.

- [x] **Exercise 9: Override name_get()**
  - Task: Format: "[CODE] Name (State)".

- [x] **Exercise 10: Combined - Full Lifecycle**
  - Task: Implement full lifecycle (create/write/unlink/copy) for `task.task`.

- [x] **Exercise 11: Prototype Inheritance**
  - Task: Create `task.template` model copying `task.task` structure.

- [x] **Exercise 12: Mail Thread Integration (Chatter)**
  - Task: Add `mail` dependency, inherit `mail.thread`, add chatter to view.

---

## 4. ❓ Questions (Check Understanding)

- [x] Q1: `_inherit` vs `_inherits` vs Prototype (`_name` + `_inherit`)?
- [x] Q2: When to call `super()` BEFORE logic vs AFTER logic?
- [x] Q3: Why MUST we return the result of `super()` in `write` and `create`?
- [x] Q4: Why is `self` empty in `create()` method? How to access created records?
- [x] Q5: How to prevent Infinite Recursion when modifying fields inside `write()`?

---

## 5. 📝 Evaluation & Notes

### Session Notes
- [ ] ...

### Evaluation Table
| Block | Score (/10) | Notes |
|-------|-------------|-------|
| Concepts | | |
| Exercises | | |
| Debugging | | |
| **Total** | **/10** | |
