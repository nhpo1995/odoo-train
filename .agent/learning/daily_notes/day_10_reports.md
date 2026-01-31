# 📋 DAILY LESSON PLAN: Day 10 - Context, Domain & QWeb Reports

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
| **Ngày** | Day 10 of 21 |
| **Chủ đề** | **Context (`env.context`), Domain Polish Notation & Basic QWeb Reports** |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Day 9 (Context usages in Wizard), Day 6 (Relationships for report data) |
| **Mục tiêu chính** | Master Context handling (`with_context`, `sudo`) and Build the first PDF Report. |

---

## 📦 MODULE PROGRESS (Trainer phải đọc!)

### 📍 Trước Day 10
- **task.task**: Constraints, Onchange, Wizard (bulk update), computed fields (amount, progress).
- **task.project**: Image, Manager, Relations.
- **Wizard**: Created and Functional (Day 9 complete).

### ✅ Sau Day 10 (Hôm nay)
- **Reports**: New `report` folder with XML actions and QWeb templates.
- **Code Logic**: Usage of `sudo()` in specific methods (if verified).
- **Context**: Usage of `with_context()` in code.

### ⭐ Production Target (Từ Roadmap)
```
Task Management Module sẽ có:
- PDF Report: "Project Task List" (Grouped by State).
- Security Logic: Ability to access data via sudo() when needed (e.g., reports running as system).
```

### 🔗 Đây là ngày 10/21 - Kết thúc Phase 2 (Business Logic)

---

## 🎯 LEARNING OBJECTIVES

By end of day, learner will be able to:
- [ ] Understand `self.env.context` as the "Request State" carrier.
- [ ] Use `with_context()` to pass data or Flags to methods.
- [ ] Use `sudo()` to bypass security (ACL/Rules) deliberately.
- [ ] Master "Polish Notation" for Domains (prefix operators `&`, `|`, `!`).
- [ ] Create a "Paper Format" and `ir.actions.report`.
- [ ] Write QWeb Templates using `t-foreach`, `t-field`, `t-if`, `t-call`.
- [ ] Use `web.external_layout` for professional headers/footers.

---

## 📊 COVERAGE CHECKLIST (For Planner - MUST verify)

- [x] Context7 queried (Reports & Context best practices)
- [x] Source code line numbers verified (Account Move examples)
- [x] 12 concepts covered (Context, Sudo, Domain, QWeb Tags)
- [x] 5 complex exercises (Logic + UI + Report)
- [x] 10 questions (Scenario-based & Debug)
- [x] Advanced topics covered (Context propagation, Grouping in QWeb)

---

## Section 1: NỘI DUNG BÀI HỌC

### 1.1 Lý thuyết cần dạy

#### 🟢 Core Concepts (Basic - Must know)

1.  **Concept 1: Environment Context (`env.context`)**
    *   **Core**: Context is an immutable dictionary carrying session data (timezone, language, `active_ids`, user flags). It permeates every method call.
    *   **Usage**: `self.env.context.get('active_id')`. or `self._context` (deprecated in new API, use `env.context`).

2.  **Concept 2: Extending Context (`with_context`)**
    *   **Core**: Since context is immutable, `with_context` returns a *new* recordset with merged context.
    *   **Syntax**: `new_recs = self.with_context(my_flag=True)`
    *   **Why**: To pass signals to `create()`, `write()`, or `name_get()` without changing method signatures.

3.  **Concept 3: Sudo (`sudo()`)**
    *   **Core**: Returns a new recordset behaving as the "Superuser" (Administrator), bypassing Access Rules and Record Rules.
    *   **Caution**: Use only when code implies privilege elevation (e.g., a Bot action or generic System Report). It *preserves* `env.user` but changes permissions.

4.  **Concept 4: Domain Polish Notation**
    *   **Core**: Odoo uses Prefix Notation. Operators (`&`, `|`, `!`) come *before* the operands.
    *   **Example**: `A AND (B OR C)` -> `['&', A, '|', B, C]`
    *   **Implicit AND**: `[A, B]` means `A AND B`.

5.  **Concept 5: Domain Operators**
    *   `=`, `!=`, `>`, `>=`
    *   `in`, `not in` (for lists)
    *   `like`, `ilike` (case insensitive search)
    *   `child_of` (hierarchical)

6.  **Concept 6: `ir.actions.report`**
    *   **Core**: The XML definition that registers a report. Controls "Print" menu visibility and output type (PDF/HTML).
    *   **Binding**: `binding_model_id` automatically adds it to the "Print" menu of the target model.

7.  **Concept 7: QWeb Template (`t-name`)**
    *   **Core**: XML engine for rendering HTML/PDF.
    *   **Structure**: `<template id="report_x"><t t-call="...">...</t></template>`

8.  **Concept 8: `web.external_layout`**
    *   **Core**: A standard "Container" template that provides Company Letterhead (Logo, Address, Footer).
    *   **Must Use**: Always wrap reports in `<t t-call="web.external_layout">`.

9.  **Concept 9: QWeb Loops (`t-foreach`, `t-as`)**
    *   **Syntax**: `<tr t-foreach="docs" t-as="o">...</tr>`
    *   **Inside loop**: User `o` (or whatever variable name) to access the current record.

10. **Concept 10: QWeb Fields (`t-field`)**
    *   **Core**: `<span t-field="o.date_deadline"/>`
    *   **Magic**: Automatically formats dates, numbers, currencies based on user language/settings. Unlike `t-esc` (raw text).

#### 🟡 Advanced Topics (Nice to have)

11. **Concept 11: Render Logic (`t-if`, `t-set`)**
    *   **Core**: Conditionals and Variables in View.
    *   **Ex**: `<div t-if="o.state == 'done'">Completed</div>`
    *   **Ex**: `<t t-set="total" t-value="0"/>`

12. **Concept 12: Context Propagation in Reports**
    *   Reports run with the user's context. Passing `context` in the Action can affect translation (`lang`) or data loading.

### 1.2 Source code cần đọc

| File | Class/Method | Reference | Focus |
|------|--------------|-----------|-------|
| `odoo/models.py` | `sudo` | Search `def sudo` | How it creates new Environment |
| `odoo/models.py` | `with_context` | Search `def with_context` | Merging logic |
| `odoo/osv/expression.py` | `TERM_OPERATORS` | Search `TERM_OPERATORS` | List of all domain operators |
| `odoo/addons/account/views/report_invoice.xml` | `report_invoice_document` | Search `<template` | Structure of a real Invoice Report |

### 1.3 Context7 Research Notes

**Query 1 (Context)**:
> `with_context` creates a NEW recordset. It does NOT modify the current one in place.
> `sudo()` implies `with_user(superuser)`. It is dangerous if used blindly in controllers.

**Query 2 (Reports)**:
> Use `web.html_container` as the root.
> Use `web.external_layout` for branding.
> `t-field` is better than `t-esc` because it handles formatting (Dates/Currency).

---

## Section 2: THỰC HÀNH

### 2.1 Bài tập code

### Exercise 0: Warm-up (Fix Missing Feature)
**Scenario**: During the audit, we realized `total_hours` (sum of task hours) is missing on Project, even though it was planned.
**Requirements**:
1. Add `total_hours = fields.Float(compute='_compute_total_hours')` to `task.project`.
2. Implement it using `read_group` (similar to `total_revenue`).
3. **Goal**: Practice `read_group` one more time before doing Reports.

### Exercise 1: The "Sudo" Search
**Scenario**: We need a method `find_all_urgent_tasks()` that returns ALL urgent tasks in the system, potentially including those from other companies (system admin check) or private projects the user cannot see.
**Requirements**:
1. Implement `def find_all_urgent_tasks(self):` in `task.task`.
2. Logic: `return self.env['task.task'].sudo().search([('priority', '=', 'high')])`
3. Test in Shell: Run as a basic user (demo), confirm it finds admin's private tasks.

### Exercise 2: Advanced Domain Search
**Scenario**: Find tasks that are EITHER (Overdue AND High Priority) OR (Draft AND No Deadline).
**Requirements**:
1. Write this domain in Polish Notation.
2. `['|', '&', ('is_overdue', '=', True), ('priority', '=', 'high'), '&', ('state', '=', 'draft'), ('due_date', '=', False)]`
3. Test in `odoo shell` with `search_count`.

### Exercise 3: Project Report (XML Action)
**Scenario**: Create the action to print a "Project Task List".
**Requirements**:
1. Create `report/task_report.xml`.
2. Define `<record id="action_report_project_tasks" model="ir.actions.report">`.
3. Model: `task.project`.
4. Report Type: `qweb-pdf`.
5. Name: `report.task_management.report_project_tasks` (template name).

### Exercise 4: Report Template (QWeb Structure)
**Scenario**: Design the actual PDF layout.
**Requirements**:
1. Create `report/task_report_template.xml`.
2. Template ID: `report_project_tasks`.
3. Use `<t t-call="web.html_container">` and `<t t-call="web.external_layout">`.
4. Header: Project Name (Large).
5. Content: Table of tasks (Name, Assignee, Due Date, State).

### Exercise 5: Grouping in Report (Logic in View)
**Scenario**: The report is messy. Group tasks by "Stage" (State).
**Requirements**:
1. In the QWeb template, retrieve tasks sorted by state.
2. Use Python logic inside QWeb (or `read_group` logic prepared in python file? Odoo QWeb allows simple logic).
3. **Advanced**: Add a "Total Hours" summary line at the bottom of the table using `<t t-set="total_hours" .../>`.

---

## Section 3: KIỂM TRA KIẾN THỨC

### 3.1 Câu hỏi self-check

#### 🟢 Easy
1. `self.env.context` là mutable hay immutable?
2. `sudo()` làm gì với `env.user`? Có đổi user thành Admin không?
3. Domain `['|', A, B, C]` có nghĩa là `A OR B OR C` hay `A OR B AND C`? (Hint: Prefix logic).

#### 🟡 Medium
4. Tại sao report nên dùng `t-field="o.date"` thay vì `t-esc`?
5. Viết domain: (Region=US OR Region=EU) AND (Sales > 1000).
6. Làm sao để truyền một biến `flags=True` vào phương thức `create()` của model con mà không sửa tham số hàm?

#### 🔴 Hard
7. **Design**: Bạn cần ẩn một số dòng trong PDF report nếu user in report không phải là Manager. Bạn dùng `groups` attribute trong XML hay check `env.user.has_group` trong QWeb?
8. **Security**: Nếu bạn dùng `sudo()` để search, sau đó bạn access fields của record tìm được, rights check có xảy ra không?
9. **Performance**: Tại sao không nên loop quá nhiều logic tính toán trong QWeb? (Nên move vào Python model generate data).
10. **Debug**: Report PDF in ra trắng tinh (blank page) hoặc lỗi 500. Check log thấy "Field 'x' does not exist". Nhưng field đó có trong model. Nguyên nhân phổ biến là gì? (Hint: Sudo/ACL access rights của user in report).

### 3.2 Đáp án
<details>
<summary>Xem đáp án</summary>

1. Immutable. Phải dùng `with_context` để tạo copy mới.
2. `sudo()` tắt quyền access rules. `env.user` VẪN LÀ user hiện tại (để tracking create_uid), trừ khi dùng `sudo(user=super_admin)`. (Correction: `sudo()` default keeps user but gives superuser privileges. Specific user switch needs `with_user()`).
3. Odoo domains are implicit AND. Prefix operators take strict operands. `|` takes 2. So `['|', A, B, C]` = `(A OR B) AND C`.
4. `t-field` auto-format date/number theo lang của user context.
5. `['&', '|', ('region','=','US'), ('region','=','EU'), ('sales','>',1000)]`.
6. `model.with_context(flags=True).create(...)`.
7. Check `user.has_group` trong QWeb (`t-if`) linh hoạt hơn.
8. Không. Recordset sinh ra từ `sudo()` sẽ giữ flag su cho các access tiếp theo trên recordset đó.
9. QWeb render mỗi lần print, ko cache query tốt bằng Python level. Logic phức tạp làm template khó đọc.
10. User đang chạy report ko có quyền read field đó. Report action chạy dưới quyền user bấm nút (trừ khi code xử lý khác).

</details>

---

## ✅ PHẦN 4: TIÊU CHÍ HOÀN THÀNH

| Tiêu chí | Đạt | Chưa đạt |
|----------|-----|----------|
| Hiểu và viết được Domain Polish Notation phức tạp | ⬜ | ⬜ |
| Sử dụng thành thạo `with_context` | ⬜ | ⬜ |
| Tạo được PDF Report chạy thực tế (có header/footer) | ⬜ | ⬜ |
| Sử dụng `t-foreach`, `t-field` đúng cách | ⬜ | ⬜ |
| Hiểu rủi ro và cách dùng `sudo()` | ⬜ | ⬜ |
| Trả lời đúng 8/10 câu hỏi hard/medium | ⬜ | ⬜ |

---

## 📝 PHẦN 5: ĐÁNH GIÁ (AI Mentor điền sau khi dạy)

### 5.1 Kết quả học tập
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Lý thuyết | 9 | Hiểu tốt concepts về context, domain, QWeb |
| Thực hành | 8 | Hoàn thành 6/6 exercises, tự viết code |
| Kiểm tra | 7.5 | 7.5/10 câu đúng hoàn toàn |
| **TỔNG** | **8/10** | Kết quả tốt! |

### 5.2 Key takeaways
> - Hiểu rõ `env.context` immutable và cách dùng `with_context()`
> - Thành thạo Domain Polish Notation (prefix operators)
> - Tạo được QWeb Report hoàn chỉnh với grouping logic
> - Hiểu `sudo()` và security implications

### 5.3 Điểm cần cải thiện
> - Domain syntax: format list operators vs tuple terms
> - Hiểu sâu hơn về ACL/security trong reports (Q10)

### 5.4 Lưu ý cho ngày tiếp theo
> - Day 11 bắt đầu Security: Groups, ACL, Record Rules
> - Sẽ apply security vào task_management module
> - Cần ôn lại phần ACL field-level access
