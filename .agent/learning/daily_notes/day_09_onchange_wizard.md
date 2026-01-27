# 📋 DAILY LESSON PLAN: Day 9 - Onchange & Wizards

> **Hướng dẫn cho AI Training Planner:**
> 1. Đọc `odoo_roadmap.md` để hiểu overview của ngày cần plan
> 2. **MANDATORY**: Query Context7 ≥2 lần để lấy best practices
> 3. Copy template này thành file mới: `day_XX_[topic].md`
> 4. Điền chi tiết vào các phần `<!-- PLANNER: ... -->`
> 5. AI Mentor sẽ dùng file này để dạy và fill phần Đánh giá

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 9 of 21 |
| **Chủ đề** | **Interactive UI (@api.onchange) & Wizards (TransientModel)** |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Day 6 (Relationships), Day 7 (Computed), Day 8 (Constraints) |
| **Mục tiêu chính** | Create dynamic UI interactions and build the first Wizard for batch processing. |

---

## 📦 MODULE PROGRESS (Trainer phải đọc!)

### 📍 Trước Day 9
- **task.task**: Constraints (hours >= 0), Statusbar, Unlink protection.
- **task.project**: Basic fields, relations.
- **Views**: Tree, Form (with notebook), Kanban.

### ✅ Sau Day 9 (Hôm nay)
- **task.task**: Auto-fill assigned user based on project.
- **task.project**: Total revenue computation (read_group).
- **task.state.wizard**: New TransientModel for bulk updating task states.
- **Actions**: Wizard appearing in "Action" menu (binding_model_id).

### ⭐ Production Target (Từ Roadmap)
```
Task Management Module sẽ có:
- Wizard "Batch Update" xử lý nhiều records cùng lúc.
- UI thông minh: Chọn Project -> Tự điền Manager vào Assignee.
- Performance: Sử dụng read_group thay vì loop để tính tổng.
```

### 🔗 Đây là ngày 9/21 của việc build complete module

---

## 🎯 LEARNING OBJECTIVES

By end of day, learner will be able to:
- [ ] Implement `@api.onchange` to update UI fields dynamically.
- [ ] Understand key differences between `onchange` and `computed` fields.
- [ ] Create a `TransientModel` and understand its lifecycle (vacuum).
- [ ] Create a Wizard with `target='new'` (dialog mode).
- [ ] Use `binding_model_id` to add actions to the "Action" menu.
- [ ] Handle `active_ids` from `self.env.context` to process selected records.
- [ ] (Advanced) Use `read_group` for high-performance aggregation.

---

## 📊 COVERAGE CHECKLIST (For Planner - MUST verify)

- [x] Context7 queried (min 2 queries documented in 1.4)
- [x] Source code line numbers verified
- [x] 10 concepts covered (Onchange, TransientModel, Wizard Action, Context, etc.)
- [x] 5 complex exercises (Onchange, Warnings, Wizard Model, Wizard View, Action)
- [x] 9 questions (mixed Easy/Medium/Hard)
- [x] Advanced topics section filled (read_group)
- [x] Gotchas/Common mistakes documented (Onchange in imports, active_ids)
- [x] Performance considerations included (TransientModel vacuum, read_group)

---

## Section 1: NỘI DUNG BÀI HỌC

### 1.1 Lý thuyết cần dạy

#### 🟢 Core Concepts (Basic - Must know)

1. **Concept 1: @api.onchange**
   - **Core explanation**: Decorator triggers ONLY when user changes a field in the Form View. It does NOT trigger on `create` or `write` from code (unless explicitly called). Used for UI assistance (auto-fill, dynamic domains).
   - **Syntax/Usage**:
     ```python
     @api.onchange('project_id')
     def _onchange_project_id(self):
         if self.project_id:
             self.assigned_user_id = self.project_id.manager_id
     ```
   - **When to use**: Auto-filling default values based on other fields, or strictly UI-side logic.
   - **Comparison**: `Computed` fields are for data logic (always consistent). `Onchange` is for UI convenience (user can change it later).

2. **Concept 2: Onchange Warning & Domain**
   - **Core explanation**: Onchange can return a dictionary to show a popup warning or set a dynamic domain for another field temporarily.
   - **Syntax**:
     ```python
     return {
         'warning': {'title': "Warning", 'message': "..."}
         # OR 'domain': {'other_field': [('id', 'in', [...])]}
     }
     ```

3. **Concept 3: TransientModel**
   - **Core explanation**: A model based on `models.TransientModel` (not `Model`). Data is temporary and periodically cleaned up by Odoo (system vacuum). No access rules needed (user sees own records).
   - **When to use**: Wizards, Dialogs, Report configuration popups.
   - **Gotcha**: Do not relate TransientModel to persistent Model via Many2one from Model side (M2O on Transient pointing to Model is OK).

4. **Concept 4: Wizard Action (target='new')**
   - **Core explanation**: An `ir.actions.act_window` with `target="new"` opens the view in a modal dialog (popup) instead of the main screen.
   - **Usage**:
     ```xml
     <field name="target">new</field>
     <field name="view_mode">form</field>
     ```

5. **Concept 5: Context & active_ids**
   - **Core explanation**: When an action is triggered from a list view selection, Odoo passes the selected record IDs in `self.env.context['active_ids']`.
   - **When to use**: In Wizard's `default_get` or action methods to know which records to process.

6. **Concept 6: Binding Actions (binding_model_id)**
   - **Core explanation**: To make an Action appear in the "Action" gear menu (formerly "Print/Action" sidebar), use `binding_model_id`.
   - **Syntax**:
     ```xml
     <field name="binding_model_id" ref="model_task_task"/>
     ```

#### 🟡 Advanced Topics (Nice to have)

7. **Concept 7: Advanced read_group vs Loop**
   - **Deep dive**: Aggregating data (Sum, Count, Avg) over many records. Looping `for rec in self` triggers N queries or loads all data to memory (slow). `read_group` runs 1 SQL `GROUP BY` query.
   - **Example**:
     ```python
     # BAD
     total = sum(task.amount for task in self.task_ids)
     
     # GOOD (1 SQL query)
     data = self.env['task.task'].read_group(
         [('project_id', 'in', self.ids)], 
         ['amount:sum', 'project_id'], 
         ['project_id']
     )
     ```
   - **Performance**: O(1) database query vs O(N) Python loop. Crucial for reporting.

#### ⚠️ Gotchas & Common Mistakes (Critical)

8. **Concept 8: Relying on Onchange for Data Integrity**
   - ❌ Wrong: Using onchange to validate data or set critical values.
   - Why: If you import data via CSV or create via code `env['model'].create({...})`, **onchange does NOT run**. Use Constraints or Computed fields for integrity.

9. **Concept 9: TransientModel Relations**
   - ❌ Wrong: `task.task` has `One2many` to `task.wizard`.
   - Why: Persistent models cannot point to Transient models (DB constraint issues when transient data is deleted). Transient can point to Persistent (Many2one).

10. **Concept 10: Wizard Record Persistence**
   - ❌ Wrong: Expecting wizard data to stay forever.
   - Why: Odoo vacuum cron job deletes them automatically (usually every 24h or based on config).

### 1.2 Source code cần đọc

| File | Class/Method | Reference | Focus |
|------|--------------|-----------|-------|
| `odoo/api.py` | `onchange` | Search `def onchange` | Decorator logic (UI only) |
| `odoo/models.py` | `TransientModel` | Search `class TransientModel` | Differences from Model (access rights, vacuum) |
| `odoo/addons/base/models/res_partner.py` | `onchange_state` | Search `onchange` | Example of address onchange |
| `odoo/addons/crm/wizard/crm_lead_lost.py` | `CrmLeadLost` | Entire file | Example of simple Wizard structure |

### 1.3 Kiến thức liên quan

| Odoo Concept | Tương đương Python/Framework | Khác biệt quan trọng |
|--------------|------------------------------|---------------------|
| `@api.onchange` | React `useEffect` / frontend event | Chạy Python code nhưng trigger bởi Frontend event |
| `TransientModel` | Redis/Temp store | Vẫn lưu trong PostgreSQL nhưng tự xóa |
| `active_ids` | `request.state` / Payload | Context dictionary truyền ngầm data |

### 1.4 Context7 Research Notes

**Query 1**: `Odoo onchange vs computed fields differences best practices`
```
Key insights:
- "Never ever use an onchange to add business logic... only triggered in form view."
- Computed fields are safer because they run on create/write ensuring consistency.
- Onchange is strictly for "UI Assistance" (filling defaults).
- Warning: Onchange can return {'warning': ...} which computed fields cannot.
```

**Query 2**: `Odoo wizard tutorial TransientModel active_ids binding_model_id`
```
Key insights:
- TransientModel: Super-class for temporary records, simplified access rights (user sees own).
- action_create_order example uses TransientModel.
- Helper methods: `transient_vacuum()` cleans up old records.
- Action target="new" for dialogs.
```

---

## Section 2: THỰC HÀNH

### 2.1 Bài tập code

### Exercise 1: Basic Onchange - UX Improvement

**Scenario**: When a user selects a Project for a Task, the "Assigned To" field should automatically default to that Project's Manager to save time.

**Requirements**:
1. Add `onchange` handler for `project_id` in `task.task`.
2. Logic: If `project_id` and `project_id.manager_id` exists, set `assigned_user_id` to manager.
3. Test in UI: Change Project -> Witness User change.

**Expected Input**: Select Project A (Manager: Alice).
**Expected Output**: `assigned_user_id` becomes Alice.

---

### Exercise 2: Onchange Warning - Data Validation UI

**Scenario**: Warn the user if they select a Project that has no Manager assigned (potential process issue).

**Requirements**:
1. Extend the onchange from Ex 1.
2. If `project_id` exists but `manager_id` is empty:
   - Return a `warning` dictionary with title "Warning" and message "This project has no manager assigned!".
3. Note: This does not block saving, just warns.

**Expected Output**: A popup dialog appears in UI when selecting such a project.

---

### Exercise 3: Financial Fields (Preparation for Read Group)

**Scenario**: We need to track the financial value of tasks.

**Requirements**:
1. Add `amount = fields.Float("Revenue", digits=(16, 2))` to `task.task`.
2. Add `total_revenue = fields.Float("Total Revenue", compute="_compute_total_revenue")` to `task.project`.
3. In `_compute_total_revenue`, use **read_group** to sum the amount.
   - Hint: `self.env['task.task'].read_group([('project_id', 'in', self.ids)], ['amount', 'project_id'], ['project_id'])`
   - Iterate the result dictionary to set values.

**Warning**: Do NOT use `for project in self: project.total_revenue = sum(...)` (Looping is forbidden here).

---

### Exercise 4: The Bulk Update Wizard (Model)

**Scenario**: Managers need to move 50 tasks to "Done" at once. Doing it one by one is painful.

**Requirements**:
1. Create new file `models/wizard.py` and `views/wizard_views.xml`.
2. Model `task.state.wizard` (TransientModel).
3. Field `new_state` (Selection - same as task state) - Required.
4. Method `action_apply`:
   - Get `active_ids` from context.
   - `browse` tasks.
   - `write` new state.

---

### Exercise 5: Wizard View & Binding Action

**Requirements**:
1. Create a Form View for the wizard (simple group with `new_state`).
2. Add "Apply" and "Cancel" buttons (`special="cancel"`).
3. Create `ir.actions.act_window` for the wizard:
   - `target="new"`.
   - `binding_model_id` ref to `model_task_task`.
4. Update `__manifest__.py` to include new files (don't forget access rights!).
5. Create `security/ir.model.access.csv` entry for the wizard model.

**Expected Result**:
- Go to Task List View.
- Select 3 Tasks.
- Click "Action" (gear icon) -> "Batch Update State".
- Select "Done" -> Click Apply.
- All 3 tasks become Done.

---

### 2.2 Shell commands

```python
# Purpose: Check TransientModel vacuum (Admin only)
self.env['task.state.wizard'].transient_vacuum()

# Purpose: Test read_group syntax (Key skill!)
self.env['task.task'].read_group([], ['amount:sum'], ['project_id'])
# Output: [{'project_id': (1, 'Proj A'), 'amount': 500.0, 'project_id_count': 5}, ...]
```

### 2.3 Debug tasks

- [ ] **Debug 1: Wizard Access Error**
  - Scenario: User clicks Action but gets "Access Error".
  - Cause: Forgot `ir.model.access.csv` for the new Wizard model.
  - Fix: Add entry (Task Manager -> Perm Create/Write/Read/Unlink).

- [ ] **Debug 2: Onchange not running**
  - Scenario: Create task via `odoo shell` or `create()` method, but `assigned_user_id` is empty (not auto-filled).
  - Cause: Onchange only runs in UI.
  - Discussion: Is this a feature or a bug? (Feature).

### 2.4 Real-World Scenarios

**Scenario A: Clean Up Old Data**
- **Task description**: Use a wizard to find and archive tasks older than 1 year.
- **Concepts used**: Wizard, Search Domain, Write.
- **Difficulty**: Intermediate.

---

## Section 3: KIỂM TRA KIẾN THỨC

### 3.1 Câu hỏi self-check

#### 🟢 Easy (Recall)
1. `@api.onchange` chạy khi nào? Có chạy khi `create()` bằng code không?
2. `TransientModel` khác `Model` thường ở điểm chính nào?
3. Để Wizard mở dạng Popup, cần dùng attribute gì trong Action?

#### 🟡 Medium (Apply)
4. Context `active_ids` chứa giá trị gì khi mở Wizard từ List View?
5. Tại sao **không nên** dùng vòng lặp `for` để tính tổng (sum) 10,000 tasks trong Project?
6. Viết code `read_group` để đếm số lượng task theo từng `priority`.

#### 🔴 Hard (Analyze)
7. **Scenario**: Bạn muốn User chọn Project, hệ thống tự điền Manager VÀ show warning nếu Manager đó đang nghỉ phép (check field `is_absent` bên res.users). Design logic dùng Onchange.
8. **Debug**: Wizard chạy OK, nhưng sau 1 ngày vào tìm lại data trong table wizard thì mất hết. Tại sao? Khách hàng muốn lưu lịch sử thao tác wizard thì làm thế nào?
9. **Design**: So sánh 2 cách Bulk Update: Server Action vs Wizard. Khi nào dùng cái nào?

### 3.2 Đáp án

<details>
<summary>Xem đáp án</summary>

#### Easy Answers:
1. Chỉ chạy khi user tương tác trên Form View. Không chạy khi create/write code (trừ khi gọi `_onchange_...` thủ công).
2. Data tạm thời (auto-deleted), access rights đơn giản hơn.
3. `target="new"`.

#### Medium Answers:
4. List các IDs của records đang được select.
5. Vòng lặp `for` load từng record (hoặc all data) vào RAM và xử lý Python → Chậm (O(N)). `read_group` dùng SQL aggregation → Nhanh (O(1)).
6. `self.env['task.task'].read_group([], ['priority'], ['priority'])`.

#### Hard Answers:
7. Tạo `@api.onchange('project_id')`. Check `project.manager_id`. Nếu `is_absent`: return `{'warning': ...}`. Vẫn gán `assigned_user_id` nhưng cảnh báo.
8. TransientModel tự xóa (vacuum). Muốn lưu lịch sử: Phải tạo 1 Model thường (e.g., `task.history`) và copy data từ Wizard sang đó lúc `apply`.
9. Server Action: Nhanh, logic đơn giản (Python code/Update record). Wizard: Cần input từ user (chọn option, nhập lý do) trước khi execute.

</details>

---

## ✅ PHẦN 4: TIÊU CHÍ HOÀN THÀNH

| Tiêu chí | Đạt | Chưa đạt |
|----------|-----|----------|
| Hiểu rõ sự khác biệt Onchange vs Compute | ⬜ | ⬜ |
| Tạo được Onchange auto-fill và warning | ⬜ | ⬜ |
| Tạo được Wizard Model & Action binding | ⬜ | ⬜ |
| Sử dụng được context `active_ids` | ⬜ | ⬜ |
| Hiểu khái niệm `read_group` (optimization) | ⬜ | ⬜ |
| Trả lời đúng ≥7/9 câu hỏi | ⬜ | ⬜ |

---

## 📝 PHẦN 5: ĐÁNH GIÁ (AI Mentor điền sau khi dạy)

### 5.1 Kết quả học tập
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Lý thuyết | 10 | Hiểu rõ cơ chế Onchange/Transient |
| Thực hành | 10 | Code chạy chuẩn, UI tốt |
| Kiểm tra | 10 | Nắm chắc performance read_group |
| **TỔNG** | **10/10** | **Xuất sắc** |

### 5.2 Key takeaways
> Hoàn thành xuất sắc Wizard và Onchange. Đã hiểu rõ khi nào dùng TransientModel vs Model thường. Performance tư duy tốt (read_group).

### 5.3 Điểm cần cải thiện
> Không có. Tiếp tục phát huy.

### 5.4 Lưu ý cho ngày tiếp theo
> Day 10 sẽ nặng về QWeb Reports. Chuẩn bị tinh thần debug XML.

---

## 🔗 CONTINUITY (Trainer phải đọc!)

### ⬅️ Ngày này builds on
- Day 6 (Relationships): Dùng `project_id` cho Onchange; `active_ids` cho Wizard.
- Day 7 (Computed): So sánh logic với Onchange.
- Day 8 (Constraints): Wizard cũng phải tuân thủ constraints của model chính.

### ➡️ Ngày tiếp theo sẽ thêm
- Day 10 (Reports & QWeb): Dùng context sâu hơn, tạo PDF Report.
- Day 11 (Security): Phân quyền ai được chạy Wizard.

### 🏁 Nhắc lại Roadmap Target
Sau 21 ngày, user sẽ có module `task_management` hoàn chỉnh. Hôm nay thêm khả năng xử lý hàng loạt (Bulk Actions) - một tính năng Enterprise-grade quan trọng.
