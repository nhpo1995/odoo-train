# 📋 DAY 8 - Constraints & Data Integrity

> **Generated**: 2026-01-22 | **Workflow**: Planner v2 (with Module Spec reference)

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 8 of 21 |
| **Chủ đề** | Constraints - Validation (@api.constrains, _sql_constraints) & Protection (@api.ondelete) |
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
- Data Protection: Prevent deleting 'done' tasks (@api.ondelete)
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
- [ ] Sử dụng `@api.ondelete` để bảo vệ data quan trọng khỏi bị xóa nhầm
- [ ] Hiểu `at_uninstall=False` trong ondelete
- [ ] Debug lỗi `IntegrityError` (từ SQL) vs `ValidationError` (từ Python)

---

## 📚 PHẦN 1: NỘI DUNG BÀI HỌC (5 Concepts)

### 1.1 Source Code Files cần đọc

| File | Focus Area | Line Range | Purpose |
|------|------------|------------|---------|
| `odoo/api.py` | `def constrains()` | L330-350 | Decorator `constrains` |
| `odoo/api.py` | `def ondelete()` | L358-380 | Decorator `ondelete` |
| `odoo/models.py` | `_sql_constraints` | Search in file | Attribute `_sql_constraints` format |
| `odoo/exceptions.py` | `ValidationError` | Class def | Exception dùng cho validate |

---

### 1.2 Concepts chi tiết

#### 🟢 Concept 1: Constraints Overview - Python vs SQL

**Core explanation:**
Constraints là quy tắc để đảm bảo data luôn đúng (Data Integrity). Odoo có 2 tầng validate:

| Feature | SQL Constraints (`_sql_constraints`) | Python Constraints (`@api.constrains`) |
|---------|--------------------------------------|----------------------------------------|
| **Level** | Database (PostgreSQL) | Server Application (Python) |
| **Performance** | ⚡ Rất nhanh (Native DB) | 🐢 Chậm hơn (Code logic) |
| **Logic** | Đơn giản (Unique, Check range) | Phức tạp (Cross-record, Helper methods) |
| **Trigger** | Khi commit transaction | Khi field change (create/write) |
| **Error Msg** | Ít thân thiện (IntegrityError) | Tùy chỉnh (`ValidationError`) |
| **Use Case** | Unique inputs, Simple checks | Business logic phức tạp, Date comparison |

**Rule of Thumb:**
> Luôn ưu tiên **SQL Constraints** nếu có thể (vì performance và atomic integrity). Chỉ dùng Python Constraints khi logic quá phức tạp cho SQL.

---

#### 🟢 Concept 2: SQL Constraints (`_sql_constraints`)

**Syntax:**
```python
class Task(models.Model):
    _name = 'task.task'
    
    _sql_constraints = [
        # (name, sql_def, message)
        ('name_project_unique', 'unique(name, project_id)', 'Task title must be unique in Project!'),
        ('hours_estimated_positive', 'CHECK(hours_estimated >= 0)', 'Estimated hours must be positive!'),
    ]
```

**Key points:**
1. Defined as list of tuples `(constraint_name, sql_definition, error_message)`
2. `constraint_name` phải là duy nhất trong model (thường là `model_field_unique`)
3. `sql_definition`: Standard SQL syntax (`UNIQUE`, `CHECK`, `EXCLUDE`)
4. **Trigger:** Constraints được tạo trong DB khi upgrade module.
5. **Gotcha:** Nếu DB đang có data vi phạm (vd: đã có duplicate names), upgrade sẽ **FAIL**! Phải clean data trước.

---

#### 🟢 Concept 3: Python Constraints (`@api.constrains`)

**Syntax:**
```python
from odoo.exceptions import ValidationError

@api.constrains('due_date')
def _check_due_date(self):
    for record in self:
        if record.due_date and record.due_date < fields.Datetime.now():
            raise ValidationError("Due date cannot be in the past!")
```

**Key points:**
1. Decorator `@api.constrains('field1', 'field2')` defines triggers.
2. Method VALIDATE từng record (`for record in self`).
3. Raise `ValidationError` nếu vi phạm.
4. **Warning:** Không dùng cho unique check (race condition). Unique phải dùng SQL Constraint.

**Comparison w/ Computed Fields:**
- Computed: *Tính toán giá trị* (Set value)
- Constraints: *Kiểm tra giá trị* (Raise Error)

---

#### 🟢 Concept 4: ValidationError Exception

**Core explanation:**
`ValidationError` là exception chuyên dụng cho user input validation. Khi raise, Odoo sẽ hiển thị popup đỏ cảnh báo user và rollback transaction.

**Best Practice:**
- Message nên rõ ràng: "Sai cái gì" + "Tại sao sai" + "Nên nhập thế nào".
- Ví dụ: "Giờ ước tính (5h) không thể nhỏ hơn Giờ đã làm (8h). Vui lòng điều chỉnh lại."

---

#### 🟢 Concept 5: Data Protection (`@api.ondelete`)

**Core explanation:**
`@api.ondelete` là "last line of defense" trước khi record bị xóa vĩnh viễn khỏi DB. Dùng để ngăn chặn xóa dữ liệu quan trọng (vd: Đã chốt sổ, Đã hoàn thành).

**Syntax:**
```python
from odoo.exceptions import UserError

@api.ondelete(at_uninstall=False)
def _unlink_except_done(self):
    if any(record.state == 'done' for record in self):
        raise UserError("You cannot delete a 'Done' task!")
```

**Parameters:**
- `at_uninstall=False`: (Crucial) Constraint không chạy khi uninstall module.
  - Tại sao? Khi uninstall, Odoo xóa TOÀN BỘ table. Nếu check này chạy, uninstall sẽ fail → User không thể gỡ module.
  - Luôn set `False` trừ trường hợp cực kỳ đặc biệt.

---

## 📝 PHẦN 2: BÀI TẬP THỰC HÀNH (4 Exercises)

### Exercise 1: SQL Constraint - Unique Task Name
**Requirement:** Trong MỘT project, không được phép có 2 task trùng tên.
1. Thêm `_sql_constraints` vào `task.task`.
2. Logic: `unique(name, project_id)`.
3. Message: "Task title must be unique within the same Project!"
4. **Test:**
   - Tạo task "A" ở Project 1.
   - Tạo task "A" ở Project 2 → OK.
   - Tạo task "A" ở Project 1 → Lỗi popup.

**Tip:** Restart server & Upgrade module (`-u task_management`) để logic SQL được apply vào Postgres.

---

### Exercise 2: Python Constraint - Positive Hours
**Requirement:** `hours_estimated` phải lớn hơn hoặc bằng 0. (Thực ra có thể dùng SQL CHECK constraint, nhưng dùng Python để tập).
1. Thêm method `_check_hours` với `@api.constrains('hours_estimated')`.
2. Raise `ValidationError` nếu `hours_estimated < 0`.
3. **Complex check:** Thêm logic: `hours_spent` không được lớn hơn `hours_estimated`? (Optional logic: Nếu ước tính 5h mà làm 6h thì sao? Thường là cho phép, nên chỉ cảnh báo hoặc không check. Hãy implement logic: **Nếu task đã Done, thì hours_spent phải > 0**).

Let's stick to strict requirement:
- `hours_estimated >= 0`
- `hours_spent >= 0` (Dùng 1 method check cả 2 fields)

---

### Exercise 3: Advanced Python Validation - Due Date
**Requirement:** `due_date` phải lớn hơn ngày tạo `create_date` (nếu có).
1. `@api.constrains('due_date')`
2. So sánh `due_date` với `create_date` (hoặc `fields.Datetime.now()` nếu new record).
3. **Problem:** `create_date` có thể chưa có khi check (lúc Create).
   - Solution: Compare với `fields.Datetime.now()`.
   - Logic: Due Date > Now.

---

### Exercise 4: Protect Data - Prevent Deleting "Done" Tasks
**Requirement:** Không cho phép xóa Task đã ở trạng thái 'done'.
1. Dùng `@api.ondelete(at_uninstall=False)`.
2. Check `self.state`.
3. Raise `UserError` (not ValidationError) vì đây là hành động User (Action), không phải Data Validation. (Thực ra ValidationError cũng ok, nhưng UserError hợp ngữ cảnh hơn cho actions).

**Critical UX Checklist:**
- [ ] Delete "Done" task → Show Popup Warning.
- [ ] Delete "Draft" task → OK.
- [ ] Uninstall module logic: verify `at_uninstall=False` (Mental check).

---

## ❓ PHẦN 3: CÂU HỎI KIỂM TRA (deep understanding)

### Basic
1. SQL Constraints khác gì Python Constraints về thời điểm trigger?
2. Tại sao `_sql_constraints` lại có performance tốt hơn?
3. Khi nào dùng `UserError` vs `ValidationError`?

### Advanced
4. **Scenario:** Bạn khai báo SQL constraint `unique(name)`. Nhưng trong DB đã có 2 record trùng tên từ trước. Khi upgrade module điều gì xảy ra? Cách xử lý?
5. **Race Condition:** Tại sao không nên dùng Python `@api.constrains` để check tính duy nhất (uniqueness)? (Gợi ý: 2 users save cùng lúc).
6. **Uninstall Safety:** Tại sao `@api.ondelete` cần `at_uninstall=False`? Nếu set `True` thì rủi ro là gì?
7. **Constraint vs Computed:** Nếu bạn đổi value của computed field (store=True) trong DB, constraint có chạy lại không?

---
