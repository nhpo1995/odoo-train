# 🧑‍🏫 TEACHING PLAN: Day 9 - Onchange & Wizards
Status: ✅ Completed

## 1. PRE-SESSION CHECKLIST
- [ ] Read `odoo/api.py` (onchange decorator mechanism)
- [ ] Read `odoo/models.py` (TransientModel class definition)
- [ ] Read `odoo/addons/base/models/res_partner.py` (onchange_state example)
- [ ] Read `odoo/addons/crm/wizard/crm_lead_lost.py` (Wizard structure example)

## 2. SOURCE CODE READING (Sequential)

### 2.1 File: `odoo/api.py`
- [x] **Introduction**: "Decorator `@api.onchange` xử lý UI updates."
- [x] **Focus**: `def onchange`
- [x] **Explain**: Triggered by JS, runs Python, returns value/domain/warning.
- [x] **Verify**: "Tại sao onchange không chạy khi gọi `create()` từ code?"

### 2.2 File: `odoo/models.py`
- [x] **Introduction**: "`TransientModel` - Class cha cho Wizards."
- [x] **Focus**: `class TransientModel`
- [x] **Explain**: Differences from `Model` (vacuum, access rights).
- [x] **Verify**: "Dữ liệu trong TransientModel tồn tại bao lâu?"

### 2.3 File: `odoo/addons/base/models/res_partner.py`
- [x] **Introduction**: "Ví dụ thực tế của Onchange."
- [x] **Focus**: `onchange_state` (or similar address onchange)
- [x] **Explain**: How changing state updates country or vice versa.
- [x] **Verify**: "Nếu user đổi Country, field nào sẽ bị clear giá trị?"

### 2.4 File: `odoo/addons/base/wizard/base_module_upgrade.py`
- [x] **Introduction**: "Cấu trúc chuẩn của một Wizard."
- [x] **Focus**: Class definition, fields, action method.
- [x] **Explain**: `TransientModel`, method `update_module`.
- [x] **Verify**: "Class này kế thừa từ đâu? Khác gì Model thường?"

### 2.5 File: `odoo/addons/base/wizard/base_module_upgrade_views.xml` (UI Context)
- [x] **Introduction**: "Giao diện và Action của Wizard."
- [x] **Focus**: `target="new"`, Button calling method.
- [x] **Explain**: MVC connection (View -> Method), Transient fields in UI.
- [x] **Verify**: "Thuộc tính nào giúp mở Wizard dạng Popup?"

### 2.6 File: `odoo/addons/base/views/res_partner_views.xml` (UI Context for Onchange)
- [x] **Introduction**: "Onchange trigger từ UI."
- [x] **Focus**: Field declaration (No explicit onchange needed usually).
- [x] **Explain**: Odoo automatically binds `@api.onchange` to fields.
- [x] **Verify**: "Field nào trigger onchange?"

## 3. CONCEPTS (100% Coverage)

### 🟢 Core Concepts
- [x] **1. @api.onchange**: UI trigger, not DB constraint.
- [x] **2. Onchange Return**: `{'warning': ...}` or `{'domain': ...}`.
- [x] **3. TransientModel**: Temporary data, vacuum strategy.
- [x] **4. Wizard Action**: `target="new"` for modal dialogs.
- [x] **5. Context active_ids**: Passing selection from List View.
- [x] **6. Binding Actions**: `binding_model_id` to show in "Action" menu.

### 🟡 Advanced Topics
- [x] **7. read_group vs Loop**: Performance optimization for aggregation.
- [x] **8. Onchange Limitations**: No running on imports/code.
- [x] **9. Relations Restriction**: Persistent -> Transient (Forbidden).
- [x] **10. Wizard Persistence**: Don't rely on ID stability.

## 4. EXERCISES

- [x] **Ex 1: Basic Onchange - UX Improvement**
    - [x] Create `@api.onchange('project_id')`.
    - [x] Logic: Auto-fill `assigned_user_id` from Project Manager.
    - [x] **Check**: Change Project -> User updates?

- [x] **Ex 2: Onchange Warning - Data Validation UI**
    - [x] Extend Ex 1: Warn if Project has no manager.
    - [x] Return `{'warning': ...}`.
    - [x] **Check**: Select empty-manager project -> Popup?

- [x] **Ex 3: Financial Fields (read_group)**
    - [x] Add `amount` (task) & `total_revenue` (project).
    - [x] Implement `read_group` in compute method (No Loop!).
    - [x] **Check**: Correct sum?

- [x] **Ex 4: The Bulk Update Wizard (Model)**
    - [x] Create `task.state.wizard` (TransientModel).
    - [x] Field `new_state` (Selection).
    - [x] Method `action_apply` using `active_ids`.
    - [x] **Check**: Code structure correct?

- [x] **Ex 5: Wizard View & Binding Action**
    - [x] Create Form View (`new_state`, buttons).
    - [x] Create Action (`target="new"`, `binding_model_id`).
    - [x] **Check**: Action menu appears? Batch update works?

## 5. QUESTIONS

- [x] **Q1**: Onchange run when? (Recall)
- [x] **Q2**: TransientModel difference? (Recall)
- [x] **Q3**: Wizard popup attribute? (Recall)
- [x] **Q4**: active_ids content? (Apply)
- [x] **Q5**: Why no loop for sum? (Apply)
- [x] **Q6**: Write read_group code? (Apply)
- [x] **Q7**: Scenario check manager absent? (Analyze)
- [x] **Q8**: Wizard data lost? (Analyze)
- [x] **Q9**: Server Action vs Wizard? (Analyze)

## 6. EVALUATION

### 6.1 Scores
| Block | Score | Notes |
|-------|-------|-------|
| Reading | 10/10 | Excellent preparation |
| Theory | 10/10 | Understood TransientModel core |
| Practice| 10/10 | Completed offline perfectly |
| Quest | 10/10 | Verified logic |
| **Final** | **10/10** | **Outstanding** |

### 6.2 Session Notes
- Learner completed all exercises offline.
- Code verified: Wizard, Onchange, read_group all correct.
- Ready for Day 10.
