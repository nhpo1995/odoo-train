# 🧑‍🏫 Teaching Log [Day 10]: Context, Domain & Reports

> **Status**: 🟡 In Progress
> **Date**: 2026-01-27
> **Score**: _/10

---

## 1. 📂 Source Code Reading (Sequential)

### 1.1. `odoo/models.py` (Environment Context & Sudo)
- [x] **View File**: `odoo/models.py`
- [x] **Search**: `def sudo`
- [x] **Explain**: `sudo()` creates new env with superuser privileges (bypassing ACL/Rules).
- [x] **Search**: `def with_context`
- [x] **Explain**: Immutability of context -> returns new recordset.
- [x] **Verify Question**: "Tại sao phải dùng `with_context` để sửa context thay vì sửa trực tiếp `self.env.context`?"
- [x] **Confirm Understanding** (Y/N)

### 1.2. `odoo/osv/expression.py` (Domain Operators)
- [x] **View File**: `odoo/osv/expression.py`
- [x] **Search**: `TERM_OPERATORS`
- [x] **Explain**: Polish Notation structure (`&`, `|`, `!`) and available operators.
- [x] **Verify Question**: "Domain Odoo dùng prefix hay infix notation? `['|', A, B]` nghĩa là gì?"
- [x] **Confirm Understanding** (Y/N)

### 1.3. `odoo/addons/account/views/report_invoice.xml` (Real Report Template)
- [x] **View File**: `odoo/addons/account/views/report_invoice.xml`
- [x] **Search**: `<template id="report_invoice_document">`
- [x] **Explain**: `t-call="web.external_layout"`, `t-set="o"`, `t-field`.
- [x] **Verify Question**: "Tag nào dùng để render field có format (ngày tháng, tiền tệ)?"
- [x] **Confirm Understanding** (Y/N)

---

## 2. 🧠 Concepts (100% Coverage)

- [x] **1. Environment Context (`env.context`)** - Immutable dict, request state.
- [x] **2. Extending Context (`with_context`)** - Merging context, passing flags.
- [x] **3. Sudo (`sudo()`)** - Superuser privileges, `env.user` preservation.
- [x] **4. Domain Polish Notation** - Prefix operators (`&`, `|`, `!`).
- [x] **5. Domain Operators** - `=`, `!=`, `in`, `like`, `child_of`.
- [x] **6. `ir.actions.report`** - Report registration, binding model.
- [x] **7. QWeb Template (`t-name`)** - Structure, `t-call`.
- [x] **8. `web.external_layout`** - Standard header/footer.
- [x] **9. QWeb Loops (`t-foreach`)** - Iterating docs.
- [x] **10. QWeb Fields (`t-field`)** - Smart formatting vs `t-esc`.
- [x] **11. Render Logic (`t-if`, `t-set`)** (Advanced) - Conditionals/Vars in view.
- [x] **12. Context Propagation** (Advanced) - Passing context to reports.

---

## 3. 🛠️ Exercises (Hands-on)

### Exercise 0: Warm-up (Fix Missing Feature)
- [x] **Present**: Add `total_hours` to `task.project` using `read_group`.
- [x] **Learner coding...** (AI Implemented per request)
- [x] **Check Result**: Correct `read_group` syntax?
- [x] **Verify**: Field appears? Calculation correct?

### Exercise 1: The "Sudo" Search
- [x] Present: `find_all_urgent_tasks` using `sudo()`.
- [x] Learner coding...
- [x] Check Result: Returns private/admin tasks?
- [x] Explain risks.

### Exercise 2: Advanced Domain Search
- [ ] Present: Logic `(Overdue & High) | (Draft & No Deadline)`.
- [ ] Learner coding (Polish Notation)...
- [ ] Check Result: `['|', '&', ..., '&', ...]`
- [ ] Verify shell execution.

### Exercise 3: Project Report (XML Action)
- [ ] Present: Create `ir.actions.report` for `task.project`.
- [ ] Learner coding (`task_report.xml`)...
- [ ] Check Result: Action created? Appears in Print menu?

### Exercise 4: Report Template (QWeb Structure)
- [ ] Present: Create `task_report_template.xml` with `external_layout`.
- [ ] Learner coding...
- [ ] Check Result: PDF prints with Header/Footer? Data correct?

### Exercise 5: Grouping in Report (Logic)
- [ ] Present: Group tasks by State in PDF.
- [ ] Learner coding (Python or QWeb logic)...
- [ ] Check Result: Tasks grouped? Totals correct?
- [ ] Verify: Use `t-set` for totals.

---

## 4. ❓ Questions (Understanding Check)

- [ ] Q1: `self.env.context` mutable/immutable?
- [ ] Q2: `sudo()` modifies `env.user`?
- [ ] Q3: Logic of `['|', A, B, C]`?
- [ ] Q4: Why `t-field` over `t-esc`?
- [ ] Q5: Domain `(US or EU) AND Sales > 1000`.
- [ ] Q6: Pass flag to `create()`?
- [ ] Q7: Hide lines in report (Design)?
- [ ] Q8: `sudo()` and field access rights?
- [ ] Q9: Performance of QWeb loops vs Python?
- [ ] Q10: Debug "Field does not exist" in report?

---

## 5. 📝 Evaluation

| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Lý thuyết | _ | |
| Thực hành | _ | |
| Kiểm tra | _ | |
| **TỔNG** | **_/10** | |

### Notes
> ...
