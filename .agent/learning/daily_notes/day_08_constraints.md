# 📋 DAY 8 - Constraints & Data Integrity

> **Generated**: 2026-01-22 | **Workflow**: Planner v2 (with Module Spec reference)

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 8 of 21 |
| **Chủ đề** | Constraints - Validation (@api.constrains, _sql_constraints) & Protection (unlink/@api.ondelete) |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Day 7 (Computed fields), Day 3 (CRUD) |
| **Module Spec Reference** | `.agent/learning/module_spec.md` |

---

## 📦 MODULE STATE (From Module Spec & Current Code)

### 🎯 Day 8 Targets (From Module Spec)
```
| Day | Feature Added | Model(s) Affected |
| 8   | Constraints, Statusbar | task.task |

Cụ thể cần thêm:
- SQL Constraints: Unique Name per Project
- Python Constraints: Validate numeric data (hours_estimated >= 0)
- Data Protection: Prevent deleting 'done' tasks (override `unlink`, or `@api.ondelete` if available)
- Logical Validation: Due Date must be in future (when set)
```

### 📍 ACTUAL Current State (Before Day 8)

**File: `models/task.py` (~178 lines)**
- ✅ `hours_estimated`, `hours_spent` (Float) exist
- ✅ `project_id` (Many2one) exists
- ✅ `state` (Selection) exists
- ❌ **Chưa có constraints nào** (Data có thể nhập âm, trùng tên, etc.)

---

## 🎯 LEARNING OBJECTIVES

By end of day, learner will be able to:
- [ ] Phân biệt rõ Python Constraints (`@api.constrains`) vs SQL Constraints (`_sql_constraints`)
- [ ] Implement SQL Constraints để đảm bảo Data Integrity level database (Performance tốt nhất)
- [ ] Implement Python Constraints với logic phức tạp và `ValidationError` custom message
- [ ] Bảo vệ data khi delete (override `unlink` hoặc `@api.ondelete` nếu có)
- [ ] Hiểu `at_uninstall=False` (nếu dùng `@api.ondelete`)
- [ ] Debug lỗi `IntegrityError` (từ SQL) vs `ValidationError` (từ Python)

---

## 📚 PHẦN 1: NỘI DUNG BÀI HỌC (12 Concepts)

### 1.1 Source Code Files cần đọc

| File | Focus Area | Line Range | Purpose |
|------|------------|------------|---------|
| `odoo/api.py` | `def constrains()` | L103-133 | Decorator `constrains` + warning trigger |
| `odoo/models.py` | `_sql_constraints` | L343-344 | Attribute format |
| `odoo/models.py` | `_add_sql_constraints()` | L2652-2674 | SQL constraints applied to DB |
| `odoo/exceptions.py` | `ValidationError` | L114-120 | Exception cho Python constraints |
| `odoo/addons/base/models/res_users.py` | `@api.constrains` example | L462-472 | Real-world constraint |
| `odoo/addons/test_inherit/models.py` | `_sql_constraints` example | L126-133 | Unique SQL constraint |
| `odoo/addons/base/views/ir_actions_views.xml` | Statusbar widget | L421-429 | `widget="statusbar"` |
| `odoo/addons/base/models/ir_actions.py` | `unlink()` pattern | L59-67 | Unlink logic before delete |

---

### 1.2 Concepts chi tiết

#### 🟢 Concept 1: Data Integrity Layers (SQL vs Python)

**Explanation:**
Odoo có 2 tầng validate: DB-level (SQL) và application-level (Python). SQL constraints đảm bảo tính atomic và nhanh, Python constraints linh hoạt cho logic phức tạp.

**Code example (source):**
`odoo/models.py` L343-344 (`_sql_constraints`) + `odoo/api.py` L103-133 (`@api.constrains`).

**Compare (SQLAlchemy/FastAPI):**
- SQLAlchemy: `UniqueConstraint`, `CheckConstraint`.
- FastAPI: Pydantic validation chỉ ở layer request, không đảm bảo DB-level integrity.

**Gotcha:**
Python constraints không thể thay thế SQL uniqueness khi có concurrency (race condition).

---

#### 🟢 Concept 2: `_sql_constraints` Structure & Naming

**Explanation:**
`_sql_constraints` là list tuples: `(name, sql_def, message)`. Tên phải unique per model, thường đặt theo `model_field_unique`.

**Code example (source):**
`odoo/addons/test_inherit/models.py` L126-133.

**Compare:**
SQLAlchemy khai báo constraint ở model/table level; Odoo lưu trong `_sql_constraints`.

**Gotcha:**
Nếu DB đã có data vi phạm, upgrade module sẽ fail.

---

#### 🟢 Concept 3: SQL Unique Composite (name + project)

**Explanation:**
Unique theo 1 field thường không đủ; cần composite unique để tránh trùng tên trong cùng project.

**Code example (custom):**
```python
_sql_constraints = [
    ('name_project_unique', 'unique(name, project_id)', 'Task title must be unique in Project!'),
]
```

**Compare:**
SQLAlchemy: `UniqueConstraint('name', 'project_id')`.

**Gotcha:**
Khi đổi project của task, uniqueness cũng bị re-check; cần test update.

---

#### 🟢 Concept 4: SQL CHECK Constraints for Ranges

**Explanation:**
Check constraints phù hợp cho numeric ranges (>= 0, <= 100).

**Code example (custom):**
```python
('hours_estimated_nonneg', 'CHECK(hours_estimated >= 0)', 'Estimated hours must be positive!')
```

**Compare:**
SQLAlchemy `CheckConstraint("hours_estimated >= 0")`.

**Gotcha:**
SQL errors thường trả message khó đọc nếu message không rõ.

---

#### 🟢 Concept 5: `@api.constrains` Trigger Mechanics

**Explanation:**
`@api.constrains` chỉ chạy khi field được khai báo xuất hiện trong `create`/`write`. Dotted fields bị ignore.

**Code example (source):**
`odoo/api.py` L121-129 (warning) + `odoo/addons/base/models/res_users.py` L462-472.

**Compare:**
SQLAlchemy validators chạy khi object set attribute; Odoo chạy theo batch recordset.

**Gotcha:**
Fields không nằm trong view có thể không trigger; cần override `create` nếu cần bắt buộc check.

---

#### 🟢 Concept 6: ValidationError vs UserError vs IntegrityError

**Explanation:**
- `ValidationError`: Python constraints thất bại, message thân thiện.
- `UserError`: ngăn action (UI button, delete).
- `IntegrityError`: DB constraint fail (SQL).

**Code example (source):**
`odoo/exceptions.py` L114-120 (`ValidationError`).

**Compare:**
FastAPI trả HTTP 422 cho validation; Odoo hiển thị popup.

**Gotcha:**
SQL error không tự map sang field; cần message rõ trong `_sql_constraints`.

---

#### 🟢 Concept 7: Float Precision Gotcha

**Explanation:**
So sánh float trực tiếp dễ sai do precision. Dùng `float_compare()`/`float_is_zero()`.

**Code example (Context7):**
```python
from odoo.tools.float_utils import float_compare
if float_compare(hours_spent, hours_estimated, precision_digits=2) > 0:
    raise ValidationError("Spent hours exceed estimate.")
```

**Compare:**
SQLAlchemy thường rely on DB numeric precision; Odoo cần utils để tránh lỗi UI.

**Gotcha:**
`0.1 + 0.2 != 0.3` -> constraint sai nếu so sánh trực tiếp.

---

#### 🟢 Concept 8: Date/Datetime Validation

**Explanation:**
`create_date` có thể chưa có khi record mới tạo; dùng `fields.Datetime.now()` để so sánh.

**Code example (Context7):**
```python
@api.constrains('due_date')
def _check_due_date(self):
    for rec in self:
        if rec.due_date and rec.due_date < fields.Datetime.now():
            raise ValidationError("Due date cannot be in the past")
```

**Compare:**
SQLAlchemy có server_default; Odoo cần check ở Python layer.

**Gotcha:**
Timezone: dùng `fields.Datetime` thay vì `datetime.now()` thuần.

---

#### 🟢 Concept 9: Constraint Performance on Recordsets

**Explanation:**
Constraints chạy trên recordset; tránh query trong loop. Nếu cần lookup, batch và dùng `mapped`.

**Code example (pattern):**
```python
projects = self.mapped('project_id')
# avoid per-record search in loop
```

**Compare:**
SQLAlchemy event listeners dễ gây N+1 nếu không batch.

**Gotcha:**
Heavy constraints làm chậm create/write batch.

---

#### 🟢 Concept 10: Delete Protection (unlink override)

**Explanation:**
Trong repo này không có `@api.ondelete`; dùng `unlink()` override để chặn delete.

**Code example (source):**
`odoo/addons/base/models/ir_actions.py` L59-67 (unlink flow).

**Compare:**
FastAPI thường chặn delete ở endpoint; Odoo chặn ở model layer.

**Gotcha:**
Đừng quên gọi `super().unlink()` khi pass validation.

---

#### 🟢 Concept 11: Statusbar Widget cho State

**Explanation:**
`widget="statusbar"` giúp user thấy tiến trình state và kiểm soát transitions.

**Code example (source):**
`odoo/addons/base/views/ir_actions_views.xml` L421-429.

**Compare:**
UI pattern tương tự progress/status component trong frontend apps.

**Gotcha:**
`statusbar_visible` chỉ hiển thị các state được list; state ngoài list sẽ ẩn.

---

#### 🟢 Concept 12: Testing & Upgrade Constraints

**Explanation:**
SQL constraints chỉ được apply khi upgrade module; test via UI + shell và verify error messages.

**Code example (process):**
`-u task_management` sau khi thay `_sql_constraints`.

**Compare:**
DB migrations trong SQLAlchemy (Alembic) tương tự module upgrade.

**Gotcha:**
Duplicate data trước upgrade sẽ gây crash; cần cleanup trước.

---

## 📝 PHẦN 2: BÀI TẬP THỰC HÀNH (6 Exercises)

### Exercise 1: SQL Constraint - Unique Task Name per Project
**Requirement:** Trong MỘT project, không được phép có 2 task trùng tên.
1. Thêm `_sql_constraints` vào `task.task`.
2. Logic: `unique(name, project_id)`.
3. Message: "Task title must be unique within the same Project!"
4. **Test:**
   - Tạo task "A" ở Project 1.
   - Tạo task "A" ở Project 2 → OK.
   - Tạo task "A" ở Project 1 → Lỗi popup.

**Shell/Upgrade:**
- `./odoo-bin -u task_management -d <db>`

---

### Exercise 2: SQL CHECK - Non-negative Hours
**Requirement:** `hours_estimated` và `hours_spent` phải >= 0 (DB-level).
1. Thêm CHECK constraint.
2. Test nhập giá trị âm -> IntegrityError.
3. **Debug task:** Clean existing negative data trước khi upgrade.

**Expected Result:**
- Popup lỗi rõ ràng khi nhập âm.
- Upgrade không fail vì dữ liệu đã sạch.

---

### Exercise 3: Python Constraint - Due Date & Float Safety
**Requirement:** `due_date` > `now` và `hours_spent` không vượt `hours_estimated` khi state = done.
1. `@api.constrains('due_date', 'hours_spent', 'hours_estimated', 'state')`
2. Dùng `float_compare` với precision 2.
3. Raise `ValidationError` với message rõ.

**Hints:**
- `from odoo.tools.float_utils import float_compare`
- `fields.Datetime.now()`

---

### Exercise 4: Protect Data - Prevent Deleting "Done" Tasks
**Requirement:** Không cho phép xóa task đã `state='done'`.
1. Override `unlink()` trong `task.task`.
2. Nếu `any(rec.state == 'done')` → raise `UserError`.
3. Gọi `super().unlink()` khi pass check.

**Critical UX Checklist:**
- [ ] Delete "Done" task → Popup warning.
- [ ] Delete "Draft" task → OK.

---

### Exercise 5: Statusbar UI for Task State
**Requirement:** Hiển thị statusbar cho `state` trong form view.
1. Thêm `widget="statusbar"` vào field `state`.
2. Set `statusbar_visible="draft,in_progress,done"`.
3. Ensure statusbar hiển thị đúng thứ tự.

**Critical UX Checklist:**
- [ ] Statusbar hiển thị 3 bước rõ ràng.
- [ ] Chuyển state từ header button vẫn update.

---

### Exercise 6: Constraint Failure Drill (Upgrade)
**Scenario:** Có 2 tasks trùng tên trong cùng project trước khi add unique constraint.
1. Tạo duplicate data.
2. Upgrade module → observe failure.
3. Fix data bằng shell → upgrade lại thành công.

**Expected Result:**
- Hiểu flow: data cleanup → upgrade → constraint applied.

---

## ❓ PHẦN 3: CÂU HỎI KIỂM TRA (deep understanding)

### Basic
1. SQL Constraints khác gì Python Constraints về thời điểm trigger?
2. `_sql_constraints` có format tuple gồm những phần nào?
3. Khi nào dùng `UserError` vs `ValidationError`?
4. Vì sao `@api.constrains` không nên dùng để check uniqueness?

### Advanced
5. **Scenario:** Bạn khai báo SQL constraint `unique(name)` nhưng DB đã có duplicate. Upgrade sẽ xảy ra gì? Cách xử lý?
6. **Trigger**: Vì sao `@api.constrains` có thể không chạy nếu field không nằm trong view?
7. **Float**: Tại sao nên dùng `float_compare()` khi check hours?
8. **Delete**: So sánh `unlink()` override vs `@api.ondelete` (nếu có). Khi nào dùng mỗi cách?
9. **Computed vs Constraint**: Nếu computed field store=True thay đổi trong DB, constraint có chạy lại không? Vì sao?

---

## ✅ PHẦN 4: TIÊU CHÍ HOÀN THÀNH (STRICT)

- [ ] Có đủ **2 SQL constraints** (unique + check) và message rõ ràng
- [ ] Có **Python constraint** với `ValidationError` và dùng `float_compare`
- [ ] Có **unlink protection** cho task `state='done'`
- [ ] Statusbar hiển thị đúng 3 trạng thái trong form view
- [ ] Đã test upgrade constraint và xử lý duplicate data
- [ ] Trả lời đúng ≥7/9 câu hỏi kiểm tra

---

## 📌 PHẦN 5: KẾT QUẢ VÀ GHI CHÚ AI (Mentor fill)

### 5.1 Kết quả học tập
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Source code reading | _ | |
| Lý thuyết | _ | |
| Thực hành | _ | |
| Kiểm tra | _ | |
| **TỔNG** | **_/10** | |

### 5.2 Key takeaways
> _

### 5.3 Điểm cần cải thiện
> _

### 5.4 Lưu ý cho Day 9
> _
