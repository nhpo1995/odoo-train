# 🎓 MID-TERM REVIEW: ODOO BASICS (Day 1 - Day 8)

> **Learner**: Phong
> **Goal**: Evaluate understanding of Odoo ORM, Views, and Business Logic basics.
> **Format**: Real-time Q&A + Coding Exercises.
> **Pass Criteria**: >80% accuracy.

---

## 🟢 PART 1: ORM FOUNDATION (Day 1-2)

### Q1: Recordset Nature
**Question**: `self` trong Odoo model method là gì? Tại sao khi viết `self.name` có thể gây lỗi `Expected singleton`?
**Answer Key**:
- `self` là một Recordset (collection of records), có thể chứa 0, 1 hoặc nhiều records.
- `self.name` chỉ hoạt động nếu `len(self) == 1`.
- Nếu `len(self) > 1` (batch processing) hoặc `len(self) == 0`, truy cập field trực tiếp sẽ gây lỗi.
- Phải loop: `for rec in self: print(rec.name)`

### Q2: Search vs Browse vs Filtered
**Question**: Phân biệt 3 method sau:
1. `self.env['model'].search([...])`
2. `self.env['model'].browse([ids])`
3. `records.filtered(lambda r: ...)`
**Answer Key**:
- `search`: Query DB trả về recordset theo domain.
- `browse`: Tạo recordset từ list IDs (không query DB ngay, lazy loading).
- `filtered`: Filter trên memory từ recordset đã có (Python side).

### Q3: Mapped & Performance
**Question**: Viết code lấy list tên của tất cả tasks trong project hiện tại. Cách nào tối ưu hơn giữa Loop và Mapped?
**Answer Key**:
- `names = self.project_id.task_ids.mapped('name')`
- Tối ưu hơn Loop vì `mapped` dùng C-implementation và batch prefetching hiệu quả hơn python loop thuần cho việc lấy field simple.

---

## 🟢 PART 2: VIEWS & ACTIONS (Day 3-5)

### Q4: View Architecture
**Question**: Cấu trúc phân cấp của một Form View chuẩn là gì? (Gợi ý: bắt đầu từ tag `<form>`)
**Answer Key**:
`<form>` -> `<header>` (statusbar/buttons) -> `<sheet>` (data) -> `<group>`/`<notebook>`

### Q5: Action & Menu
**Question**: Để một Menu Item hiển thị được view, nó cần liên kết với object nào? Object đó liên kết với View như thế nào?
**Answer Key**:
- Menu Item liên kết với `ir.actions.act_window` (Action).
- Action định nghĩa `res_model` và `view_mode`. Odoo tự tìm View có model tương ứng hoặc dùng `view_id`/`view_ids` để chỉ định cụ thể.

---

## 🟢 PART 3: RELATIONSHIPS (Day 6)

### Q6: M2O vs O2M vs M2M
**Question**:
- `Many2one`: Lưu gì trong DB?
- `One2many`: Lưu gì trong DB?
- `Many2many`: Lưu gì trong DB?
**Answer Key**:
- M2O: Lưu Foreign Key (Integer ID) trong bảng của model hiện tại.
- O2M: Không lưu gì trong bảng hiện tại (Virtual field). Nó trỏ ngược lại field M2O bên kia.
- M2M: Tạo một bảng trung gian (Relational Table) lưu cặp IDs (column1, column2).

### Q7: Relational Field Attribute
**Question**: Field `One2many` bắt buộc phải có param nào liên quan đến model đích?
**Answer Key**:
`inverse_name`: Tên field Many2one ở model đích trỏ ngược lại model này.

---

## 🟢 PART 4: COMPUTED FIELDS & CONSTRAINTS (Day 7-8)

### Q8: Compute Store vs Non-Store
**Question**: Sự khác biệt cốt lõi giữa `store=True` và `store=False` (default) là gì về mặt lưu trữ và khả năng search?
**Answer Key**:
- `store=True`: Tính toán xong lưu kết quả vào DB. Search được trực tiếp bằng SQL. Recalculate khi dependencies thay đổi.
- `store=False`: Tính toán on-the-fly (runtime) mỗi khi access. Không lưu DB. Không search được bằng SQL (trừ khi define `search=` method).

### Q9: Depends Logic
**Question**: Tại sao `@api.depends('project_id.manager_id')` lại tốn resource hơn `@api.depends('state')`?
**Answer Key**:
Vì nó truy cập xuyên model (Cross-model dependency). Khi Manager thay đổi, Odoo phải tìm ngược lại tất cả Tasks thuộc Project của Manager đó để tính lại. Chain càng dài, cost càng cao.

### Q10: Python vs SQL Constraints
**Question**: Bạn cần đảm bảo `code` của Task là duy nhất. Bạn chọn loại constraint nào? Tại sao?
**Answer Key**:
- Chọn **SQL Constraint** (`UNIQUE(code)`).
- Vì Python constraint (`@api.constrains`) không đảm bảo atomic transaction (bị race condition) khi nhiều user tạo cùng lúc. SQL constraint chặn ngay tại DB level tuyệt đối an toàn.

---

## 🔴 PART 5: CODING CHALLENGE (Live)

### Ex 1: The "Lazy" Query
**Req**: Viết method `action_clean_drafts(self)`:
- Tìm tất cả tasks `state='draft'` và `create_date` cũ hơn 7 ngày.
- Xóa chúng.
- Return action reload view.

### Ex 2: The "Smart" Compute
**Req**: Thêm field `urgency_level` (Selection: normal, high, critical).
- Compute logic:
    - Nếu `due_date` < now -> 'critical'
    - Nếu `priority` == 'high' -> 'high'
    - Else -> 'normal'
- Yêu cầu: `store=True`.

---

## 📝 GRADING LOG
| Q | Topic | Score | Notes |
|---|-------|-------|-------|
| 1 | Recordset | 9/10 | Concept solid. Correctly identified `self` as Recordset and singleton risk. Missed explicit code fix (loop). |
| 2 | ORM Methods | 10/10 | Excellent breakdown: Search (DB query), Browse (Lazy/IDs), Filtered (In-memory). |
| 3 | Performance | 8/10 | Logic correct (avoid loop N+1), but syntax overly complex. Should use `self.task_ids.mapped('name')` directly instead of re-searching. |
| 4 | Views | 10/10 | Correct form view structure identified: form > header > sheet > notebook/group. |
| 5 | Actions | 10/10 | Correct linkage (Menu->Action) and priority mechanism (view_mode order). |
| 6 | Relations DB| 4/10 | Confused Python-level objects (recordsets) with DB implementation. Failed to identify that O2M is virtual (no DB column) and M2M uses a separate table. |
| 7 | O2M Params | 10/10 | Correct. Identified `inverse_name` as the critical link back to M2O field. |
| 8 | Compute | 10/10 | Correct. Clear distinction on Storage (DB vs Runtime) and Searchability (SQL vs search method). Added good point about Constraint trigger. |
| 9 | Depends | 10/10 | Correct. Explained the complexity of traversing relationships (multiple queries/joins) vs local updates. Identified performance impact accurately. |
| 10| Constraints | 10/10 | Correct choice (SQL) and explanation (Race Condition/Concurrency). Understood that runtime checks are insufficient for uniqueness. |
| C1| Coding 1 | 8/10 | Initial: N+1 issue. Final: Perfect batch logic + UX notification. |
| C2| Coding 2 | 10/10 | Initial: Typo in depends. Final: Correct logic. |
| **TOTAL** | | **109/120 (90%)** | **PASSED (Excellent)** |

---

## 🏆 FINAL VERDICT

> **Strengths**: 
> - Logic Code & UX tư duy rất tốt (Code Challenge 1 sau khi fix).
> - Hiểu sâu về Performance (Active vs Batch processing).
> - Nắm chắc kiến thức View/Action/Constraint.

> **Weaknesses (Cần ôn lại)**:
> - **Database Schema**: Vẫn còn lơ mơ về cách lưu trữ M2O/O2M/M2M trong DB (Q6). Cần phân biệt rõ Python Object vs SQL Table.
> - **Syntax precision**: Đôi khi còn ẩu (depend on self, map on dotted field).

> **Recommendation**: Đủ điều kiện qua môn! Sẵn sàng cho Day 9 (Wizards).
