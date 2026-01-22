# 📋 DAY 3: create / write / unlink + Form View (task_management)

> **Ngày**: Day 3 of 21
> **Chủ đề**: CRUD Lifecycle + Form View Basics
> **Prerequisites**: Day 1-2 (Recordset, search/browse/filtered/mapped)
> **Module thực hành**: `task_management`

---

## 📦 MODULE PROGRESS (Trainer phải đọc!)

### 📍 Trước Day 3
- Module `task_management` **CHƯA TỒN TẠI**
- Day 1-2 dùng `library_mgmt` để học Recordset basics

### ✅ Sau Day 3 (Hôm nay)
- **Module `task_management` được tạo!**
- Model `task.task` với basic fields: name, description, state, priority
- Form view cơ bản với sheet/group/notebook
- Override create()/write() với logging

### ⭐ Production Target (Từ Roadmap)
```
Task Management Module hoàn chỉnh sẽ có:
- 3 Models: task.project, task.task, task.tag
- Views: Tree, Form, Kanban, Search
- Security: Manager vs Member
- Workflows, Computed fields, Reports
```

### 🔗 Đây là ngày 1/19 của việc build complete module

---

## 🎯 LEARNING OBJECTIVES

By end of day, learner will be able to:
- [ ] Giải thích lifecycle của record: create → write → unlink
- [ ] Override `create()` và `write()` đúng cách với `super()`
- [ ] Hiểu tại sao `@api.model_create_multi` decorator cần thiết
- [ ] Tạo Form view XML cơ bản với `<sheet>`, `<group>`, `<notebook>`
- [ ] Tạo được module `task_management` với model `task.task`

---

## 📊 COVERAGE CHECKLIST

- [x] Context7 queried (2 queries: CRUD best practices + Form view structure)
- [x] Source code line numbers verified
- [x] 12 concepts covered
- [x] 5 exercises (multi-step)
- [x] 8 questions (mixed difficulty)
- [x] Gotchas documented

---

## 📂 PHẦN 0: SOURCE CODE CẦN ĐỌC (TRAINER ĐỌC TRƯỚC!)

### 📖 Source Files

| # | File | Focus | Line Range | Mục đích user hiểu |
|---|------|-------|------------|-------------------|
| 1 | `odoo/models.py` | `def create` | L3798-3860 | Hiểu create() nhận vals_list, xử lý defaults, return records |
| 2 | `odoo/models.py` | `def write` | L3518-3600 | Hiểu write() update all records trong self, check access |
| 3 | `odoo/models.py` | `def unlink` | L3433-3516 | Hiểu unlink() xóa records, cascade effects, return True |

### 🎯 Focus Points cho từng Source:

**Source 1 - create() (L3798-3860):**
- **Focus**: Dòng 3798-3800: decorator `@api.model_create_multi` và signature
- **Focus**: Dòng 3843: `_add_missing_default_values(vals)` - Odoo tự fill defaults
- **Focus**: Dòng 3899: `_create(data_list)` - actual INSERT
- **Mục đích**: User hiểu create() nhận list (hoặc dict cho backward compat), fill defaults, return recordset mới

**Source 2 - write() (L3518-3600):**
- **Focus**: Dòng 3518: signature `def write(self, vals)` - nhận 1 dict
- **Focus**: Dòng 3590-3591: `if not self: return True` - empty recordset = no-op
- **Focus**: Dòng 3593-3595: check access rights/rules
- **Mục đích**: User hiểu write() update TẤT CẢ records trong self với CÙNG vals

**Source 3 - unlink() (L3433-3516):**
- **Focus**: Dòng 3437-3438: `if not self: return True`
- **Focus**: Dòng 3474: `DELETE FROM table WHERE id IN`
- **Focus**: Dòng 3504: `invalidate_cache()` - xóa cache sau delete
- **Mục đích**: User hiểu unlink() xóa vĩnh viễn, cascade effects, return True

---

## 📚 PHẦN 1: NỘI DUNG BÀI HỌC

### 1.1 Context7 Research Notes

**Query 1**: CRUD best practices
- `@api.model_create_multi` decorator cho create()
- Luôn gọi `super().create(vals_list)` khi override
- `@api.ondelete` recommended thay vì override unlink() trực tiếp

**Query 2**: Form view structure
- Root element: `<form>`
- Structure: `<sheet>` → `<group>` → `<field>`
- `<notebook>` cho tabs

---

### 1.2 Core Concepts (12 concepts)

#### 🟢 Concept 1: create() Method

**Core explanation:**
```python
# Signature (từ source L3800)
@api.model_create_multi
@api.returns('self', lambda value: value.id)
def create(self, vals_list):
    """
    Creates new records for the model.
    - vals_list: list of dicts HOẶC single dict (backward compat)
    - Returns: recordset của records mới tạo
    """
```

**Key points:**
- `create()` là **class method** (không có existing record)
- Nhận `vals_list` = list of dicts (Odoo 13+) hoặc single dict (backward compat)
- Tự động fill defaults (`_add_missing_default_values`)
- Return: recordset mới tạo

**So sánh SQLAlchemy:**
| SQLAlchemy | Odoo |
|------------|------|
| `session.add(obj)` | `Model.create(vals)` |
| `session.commit()` | Auto-commit (nếu không có try/except) |
| Object instance | Recordset |

**Khi nào dùng**: Tạo record mới từ code, import data, UI create

---

#### 🟢 Concept 2: write() Method

**Core explanation:**
```python
# Signature (từ source L3518)
def write(self, vals):
    """
    Updates ALL records in self with the SAME vals.
    - vals: single dict (không phải list!)
    - Returns: True
    """
```

**Key differences vs create:**
- `write()` là **instance method** (có self = existing records)
- Nhận **single dict**, không phải list
- Apply **CÙNG** vals cho TẤT CẢ records trong self
- Return: True (không phải recordset)

**Pattern quan trọng:**
```python
# Update nhiều records cùng 1 value
books = self.env['lib.book'].search([('state', '=', 'draft')])
books.write({'state': 'published'})  # Update TẤT CẢ
```

**So sánh SQLAlchemy:**
| SQLAlchemy | Odoo |
|------------|------|
| `query.update({...})` | `recordset.write({...})` |
| Per-record update | Batch update |

---

#### 🟢 Concept 3: unlink() Method

**Core explanation:**
```python
# Signature (từ source L3433)
def unlink(self):
    """
    Deletes ALL records in self.
    - No parameters (chỉ delete self)
    - Returns: True
    - CASCADE: Xóa related data (attachments, properties, etc.)
    """
```

**Key behaviors:**
- Xóa VĨNH VIỄN từ database
- Trigger cascade delete cho related records
- Invalidate cache sau delete
- Log deletion for auditing

**So sánh SQLAlchemy:**
| SQLAlchemy | Odoo |
|------------|------|
| `session.delete(obj)` | `recordset.unlink()` |
| Manual cascade config | Auto cascade |

---

#### 🟢 Concept 4: Override create() đúng cách

**Pattern chuẩn:**
```python
from odoo import api, models

class Task(models.Model):
    _name = 'task.task'
    
    @api.model_create_multi  # BẮT BUỘC cho Odoo 13+
    def create(self, vals_list):
        # TRƯỚC: Xử lý vals trước khi tạo
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = 'New Task'
        
        # GỌI SUPER - BẮT BUỘC!
        records = super().create(vals_list)
        
        # SAU: Xử lý sau khi tạo
        records._do_something_after_create()
        
        return records  # PHẢI return kết quả của super()
```

**Gotcha nếu không gọi super():**
- Record KHÔNG được tạo trong DB
- Defaults không được fill
- Constraints không được check
- Module sẽ BROKEN!

---

#### 🟢 Concept 5: Override write() đúng cách

**Pattern chuẩn:**
```python
def write(self, vals):
    # TRƯỚC: Xử lý trước update
    if 'state' in vals and vals['state'] == 'done':
        # Check điều kiện trước khi cho done
        for record in self:
            if not record.assigned_to:
                raise UserError("Cannot done without assignee!")
    
    # GỌI SUPER
    result = super().write(vals)
    
    # SAU: Xử lý sau update
    if 'state' in vals:
        self._notify_state_change()
    
    return result  # Return True
```

**Khác biệt với create():**
- Không cần `@api.model_create_multi`
- `self` đã là recordset (0..n records)
- Nên check `if 'field_name' in vals` trước khi xử lý

---

#### 🟢 Concept 6: @api.model_create_multi Decorator

**Tại sao cần:**
```python
# Odoo 12 và trước: create() nhận single dict
def create(self, vals):  # vals = {}

# Odoo 13+: create() nhận list of dicts
@api.model_create_multi
def create(self, vals_list):  # vals_list = [{}, {}, ...]
```

**Decorator này làm gì:**
- Convert single dict → list nếu caller pass dict
- Enable batch insert for performance
- Backward compatible

---

#### 🟢 Concept 7: Form View XML Structure

**Basic structure (từ Context7):**
```xml
<record id="view_task_form" model="ir.ui.view">
    <field name="name">task.task.form</field>
    <field name="model">task.task</field>
    <field name="arch" type="xml">
        <form string="Task">
            <sheet>
                <group>
                    <group>
                        <field name="name"/>
                        <field name="description"/>
                    </group>
                    <group>
                        <field name="state"/>
                        <field name="priority"/>
                    </group>
                </group>
                <notebook>
                    <page string="Details">
                        <field name="notes"/>
                    </page>
                </notebook>
            </sheet>
        </form>
    </field>
</record>
```

**Elements quan trọng:**
- `<form>`: Root element
- `<sheet>`: Content area (styling)
- `<group>`: Layout columns (2 groups = 2 columns)
- `<notebook>` + `<page>`: Tabs
- `<field>`: Data fields

---

#### 🟢 Concept 8: vals Dict Keys

**Khi create/write, vals chứa:**
```python
# Basic fields
vals = {
    'name': 'Task 1',           # Char
    'description': 'Desc',      # Text
    'priority': 'high',         # Selection
    'deadline': '2024-01-15',   # Date (STRING!)
}

# Many2one - chỉ ID
vals = {
    'project_id': 5,  # Integer ID, không phải recordset
}

# One2many/Many2many - commands
vals = {
    'tag_ids': [(6, 0, [1, 2, 3])],  # Replace với IDs
}
```

**Commands cho x2many (quan trọng!):**
- `(0, 0, {vals})` - Create new
- `(1, id, {vals})` - Update existing
- `(2, id, 0)` - Delete
- `(4, id, 0)` - Link existing
- `(6, 0, [ids])` - Replace all

---

#### 🟡 Advanced 1: Batch Create Performance

```python
# ❌ SLOW - N lần INSERT
for data in data_list:
    Model.create(data)

# ✅ FAST - 1 lần INSERT (batched)
Model.create(data_list)
```

**Tại sao batch nhanh hơn:**
- 1 transaction thay vì N
- Defaults computed once
- Constraints checked once

---

#### 🟡 Advanced 2: Context trong create/write

```python
# Pass context khi create
task = self.env['task.task'].with_context(
    default_project_id=5,
    tracking_disable=True  # No chatter messages
).create({'name': 'Task'})

# Context tự fill defaults
# default_<field_name> → auto set field value
```

---

#### ⚠️ Gotchas & Common Mistakes

**Gotcha 1: Quên gọi super()**
```python
# ❌ WRONG - Record không được tạo!
@api.model_create_multi
def create(self, vals_list):
    _logger.info("Creating...")
    # THIẾU super() → DB không có record!

# ✅ CORRECT
@api.model_create_multi
def create(self, vals_list):
    _logger.info("Creating...")
    return super().create(vals_list)
```

**Gotcha 2: Nhầm vals_list vs vals**
```python
# ❌ WRONG - TypeError
@api.model_create_multi
def create(self, vals):  # Nhầm tên parameter
    vals['state'] = 'draft'  # Error: list không có key!

# ✅ CORRECT
@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        vals['state'] = 'draft'
```

**Gotcha 3: Return sai type**
```python
# ❌ WRONG - UI broken
def write(self, vals):
    super().write(vals)
    return self  # SAI! write() phải return True

# ✅ CORRECT
def write(self, vals):
    return super().write(vals)  # Return True
```

---

## 📝 PHẦN 2: EXERCISES (5 exercises)

### Exercise 1: Setup task_management Module (30 mins)

**Yêu cầu:**
1. Tạo module structure:
```
custom_addons/task_management/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── task.py
├── views/
│   └── task_views.xml
└── security/
    └── ir.model.access.csv
```

2. Model `task.task` với fields:
   - `name` (Char, required)
   - `description` (Text)
   - `state` (Selection: draft/in_progress/done)
   - `priority` (Selection: low/medium/high)

3. Basic security để user có thể CRUD

**Success criteria:**
- [ ] Module install không lỗi
- [ ] `env['task.task'].search([])` chạy được trong shell

---

### Exercise 2: Override create() với logging (20 mins)

**Yêu cầu:**
```python
# Thêm vào task.py
import logging
_logger = logging.getLogger(__name__)

# Override create() để:
# 1. Log vals_list ra console
# 2. Set default state = 'draft' nếu chưa có
# 3. Log record ID sau khi tạo
```

**Test:**
```python
>>> task = env['task.task'].create({'name': 'Test'})
# Kiểm tra log output
>>> task.state  # Should be 'draft'
```

---

### Exercise 3: Override write() với validation (20 mins)

**Yêu cầu:**
```python
# Override write() để:
# 1. Nếu state chuyển sang 'done', check name không rỗng
# 2. Log mỗi khi state thay đổi
```

**Test:**
```python
>>> task = env['task.task'].create({'name': '', 'state': 'draft'})
>>> task.write({'state': 'done'})  # Should raise error!
```

---

### Exercise 4: Form View với notebook (30 mins)

**Yêu cầu:**
Tạo `views/task_views.xml` với:
1. Form view có:
   - Group 1: name, state
   - Group 2: priority, deadline (thêm field Date)
   - Notebook với 2 pages: "Description", "Notes"
2. Action window
3. Menu item

**Success criteria:**
- [ ] UI hiển thị form đẹp
- [ ] Tabs hoạt động

---

### Exercise 5: Test CRUD từ UI vs Shell (20 mins)

**Yêu cầu:**
1. Tạo task từ UI → observe vals trong log
2. Tạo task từ shell → so sánh vals
3. Update task từ UI → check log
4. Delete task → check cascade

**Questions to answer:**
- Vals từ UI có gì khác với shell?
- UI thêm fields nào tự động?

---

## ❓ PHẦN 3: KNOWLEDGE CHECK (8 questions)

### Easy (2 questions)

**Q1**: `create()` nhận parameter gì và return gì?
- A) Dict, True
- B) List of dicts, recordset
- C) Recordset, True
- D) Dict, recordset

<details>
<summary>Answer</summary>
**B) List of dicts (vals_list), recordset của records mới**
Note: Có thể nhận single dict cho backward compat, nhưng internally convert thành list.
</details>

**Q2**: `write({'state': 'done'})` apply cho bao nhiêu records?
- A) 1 record
- B) Record đầu tiên
- C) Tất cả records trong self
- D) Depends on filter

<details>
<summary>Answer</summary>
**C) Tất cả records trong self**
write() always update ALL records trong recordset với CÙNG vals.
</details>

### Medium (3 questions)

**Q3**: Điều gì xảy ra nếu override create() nhưng KHÔNG gọi super()?

<details>
<summary>Answer</summary>
- Record KHÔNG được tạo trong database
- Defaults không được fill
- Constraints không được check
- Method return None hoặc gì đó sai
- Module/feature sẽ broken completely
</details>

**Q4**: Tại sao cần `@api.model_create_multi` decorator?

<details>
<summary>Answer</summary>
- Backward compatibility: Convert single dict → list
- Enable batch INSERT cho performance
- Odoo 13+ expect vals_list, nhưng callers có thể pass single dict
- Decorator handle conversion tự động
</details>

**Q5**: Command `(6, 0, [1, 2, 3])` trong vals của x2many field làm gì?

<details>
<summary>Answer</summary>
Replace toàn bộ records hiện tại với records có IDs [1, 2, 3].
Tương đương: unlink all → link [1, 2, 3]
</details>

### Hard (3 questions)

**Q6**: Trong form view, tại sao cần `<sheet>` wrapper?

<details>
<summary>Answer</summary>
- `<sheet>` provides styling/layout container
- Cho phép buttons ở header (ngoài sheet)
- Responsive design
- Standard Odoo form styling
- Không bắt buộc nhưng highly recommended
</details>

**Q7**: Bạn có 1000 tasks cần update state. Code nào efficient hơn và tại sao?
```python
# Option A
for task in tasks:
    task.write({'state': 'done'})

# Option B
tasks.write({'state': 'done'})
```

<details>
<summary>Answer</summary>
**Option B** efficient hơn RẤT NHIỀU:
- Option A: 1000 SQL UPDATE queries
- Option B: 1 SQL UPDATE query với WHERE id IN (...)
- Performance difference: ~100x faster
</details>

**Q8**: Scenario: Override write() để log OLD value của state trước khi update. Code như thế nào?

<details>
<summary>Answer</summary>
```python
def write(self, vals):
    if 'state' in vals:
        for record in self:
            _logger.info(f"State change: {record.state} → {vals['state']}")
    return super().write(vals)
```
Key insight: Phải log TRƯỚC super() vì sau super() record.state đã là new value.
</details>

---

## ✅ PHẦN 4: REVIEW CRITERIA

| Tiêu chí | Self | AI |
|----------|------|-----|
| Giải thích được lifecycle: create → write → unlink | ⬜ | ⬜ |
| Override create() với super() đúng cách | ⬜ | ⬜ |
| Override write() với validation | ⬜ | ⬜ |
| Hiểu vals_list vs vals parameter | ⬜ | ⬜ |
| Tạo được Form view với sheet/group/notebook | ⬜ | ⬜ |
| Module task_management install và chạy được | ⬜ | ⬜ |

---

## 📝 PHẦN 5: ĐÁNH GIÁ (AI Mentor điền sau khi dạy)

### 5.1 Kết quả học tập
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Source code reading | 9 | Đọc và hiểu đúng create/write/unlink, phân biệt được vals_list vs vals, hiểu được flow |
| Lý thuyết | 8.5 | Hiểu CRUD lifecycle, decorators, XML structure. Hỏi deep questions về view_mode, attrs |
| Thực hành | 9.5 | Module structure hoàn chỉnh, override methods đúng pattern, validation logic chính xác, apply production attrs |
| Kiểm tra | 7.5 | 7/8 câu đúng/gần đúng. Câu 5 skip (x2many - chưa học), câu 8 thiếu log old value |
| **TỔNG** | **8.6/10** | **Xuất sắc!** |

### 5.2 Key takeaways

**Điểm mạnh:**
- Tư duy logic tốt: Tự phát hiện lỗi typo trong security file, nhận ra name required không cần validate
- Hỏi câu hỏi sâu: "Tại sao `@override` không dùng?", "view_mode hoạt động như thế nào?"
- Áp dụng production patterns: Sử dụng `attrs` để hide/show fields based on CREATE/UPDATE
- Self-learning: Test và confirm `attrs` hoạt động trên `<page>` (trainer đã nhầm)

**Kiến thức nắm vững:**
- `create()` nhận vals_list, return recordset
- `write()` apply cho TẤT CẢ records trong self
- Override pattern: log TRƯỚC super() để lấy old values
- Form view structure: `<form>` → `<sheet>` → `<group>` → `<notebook>`
- Action workflow: Menu → Action → View

### 5.3 Điểm cần cải thiện

1. **Source code comprehension**: Cần đọc kỹ hơn implementation details (ví dụ: dòng nào làm gì trong create/write)
2. **Edge cases**: Chưa tự động nghĩ đến edge cases khi validate (ví dụ: empty recordset)
3. **Performance thinking**: Hiểu vì sao batch nhanh hơn nhưng chưa thinking ngay từ đầu
4. **x2many commands**: Chưa học (sẽ học Day 6), cần note lại để ôn

### 5.4 Notes cho Day 4

**Chuẩn bị:**
- Module `task_management` đã có Form view hoàn chỉnh
- Cần thêm: Tree view (list), Search view (filters), Kanban view (cards)
- User đã hiểu `view_mode`, sẵn sàng học nhiều view types

**Focus points:**
- Tree view: Decorators, colors, buttons
- Search view: Filters, group by
- Kanban view: Card layout, drag & drop

**Tip**: User hỏi hay về "tại sao" → khuyến khích so sánh giữa các view types

---

## 🔗 CONTINUITY (Trainer phải đọc!)

### ⬅️ Ngày này builds on
- **Day 1**: Recordset concept - hiểu `self` là collection
- **Day 2**: search/browse/filtered/mapped - query và transform data

### ➡️ Ngày tiếp theo sẽ thêm (Day 4)
- **Tree view** để list tasks
- **Search view** với filters và group by
- **Kanban view** basics
- **Action + Menu** để truy cập module từ UI

### 🏁 Nhắc lại Roadmap Target
Sau 21 ngày, learner sẽ có module `task_management` **production-ready** với:
- Full CRUD + Relationships (M2O, O2M, M2M)
- Complete UI (Tree, Form, Kanban, Search)
- Security (ACL, Groups, Record Rules)
- Business Logic (Computed, Constraints, Workflows)
- Reports (QWeb PDF)

> ⚠️ **Trainer**: Day 3 là ngày **ĐẦU TIÊN** tạo module `task_management`. Từ ngày này trở đi, MỖI NGÀY sẽ thêm features vào module này cho đến khi hoàn chỉnh!
