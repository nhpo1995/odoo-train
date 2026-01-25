# 🎯 ODOO 14 LEARNING ROADMAP (21 Days)

> **Mục tiêu**: Trở thành Odoo Junior Developer có thể nhận task công ty
> **Thời gian**: 21 ngày liên tục × 7 tiếng/ngày
> **Module thực hành**:
> - Day 1-2: `library_mgmt` (Recordset basics) ✅ DONE
> - Day 3-21: `task_management` (Complete app: relationships, workflows, UI, Security)

---

## 🎯 SẢN PHẨM CUỐI CÙNG: Task Management Module

**Sau 21 ngày, bạn sẽ có một module PRODUCTION-READY với:**

### 📦 Models hoàn chỉnh:
- `task.project` - Quản lý projects với cover image
- `task.task` - Tasks với states, priorities, deadlines, subtasks
- `task.tag` - Color-coded tags

### 🖥️ Views đầy đủ:
- Tree view - List tasks với filters
- Form view - Edit với notebook, statusbar
- Kanban view - Drag & drop theo state
- Search view - Filter & group by
- **Calendar view** - Task deadlines by date

### 🔐 Security 2-tier:
- **Manager**: Full CRUD, manage projects
- **Member**: Create tasks, edit own, no delete

### ⚙️ Business Logic:
- Computed fields (hours_remaining, progress, task_count, **total_revenue**)
- Constraints (date validation, hours >= 0)
- Onchange (auto-assign user từ project)
- Workflows (Draft → In Progress → Done)
- Wizards (Bulk state change)
- **Subtasks** (parent_id self-reference)
- **Financial** (amount field, total_revenue read_group)

### 📄 Reports:
- PDF Task List với QWeb
- Project Summary report

### ⏰ Automation:
- Scheduled Actions (Auto-mark overdue)

---

## 📊 PROGRESS TRACKER

| Phase | Ngày | Trạng thái | Điểm TB |
|-------|------|------------|---------|
| 1. ORM Foundation | Day 1-5 | ✅ DONE | 8.8/10 |
| 2. Business Logic | Day 6-10 | ⏳ (3/5) | 8.75/10 |
| 3. Security | Day 11-13 | ⬜ | _/10 |
| 3b. Subtasks | Day 14 | ⬜ | _/10 |
| 4. Module Reading | Day 15-17 | ⬜ | _/10 |
| 5. Controller | Day 18-19 | ⬜ | _/10 |
| 6. Consolidation | Day 20-21 | ⬜ | _/10 |

**Tổng tiến độ**: 8/21 ngày học

**Chi tiết Phase 1:**
- Day 1: 9.5/10 ✅
- Day 2: 9.5/10 ✅
- Day 3: 8.6/10 ✅
- Day 4: 8.5/10 ✅ _(estimated retrospectively)_
- Day 5: 8.0/10 ✅

**Chi tiết Phase 2:**
- Day 6: 9.0/10 ✅ (+ Bonus: Deadlock, Recursion)
- Day 7: 8.5/10 ✅ (Computed fields, inverse, search, read_group)
- [x] Day 8: 10/10 ✅ (Constraints, Protection, Statusbar)
- Day 9: _/10 ⏳ (Onchange, Wizards)

---

# 📅 PHASE 1: ORM FOUNDATION (Day 1-5)

### 🛠️ Debug checklist (Phase 1)
- [ ] Reproduce in `odoo shell` with the same user/context
- [ ] Log `self.ids`, `self._context`, `self.env.user` in ORM methods
- [ ] Compare `search()` vs `filtered()` outputs and query counts

---

## Day 1: Recordset - Lý do bạn "mù" khi đọc module

### 🎯 Mục đích chủ đạo
Hiểu Recordset là gì, tại sao `self` trong Odoo luôn là collection, không phải single object.

### 📚 Đề mục cần học
- [ ] Recordset concept
- [ ] `BaseModel.__iter__`, `__len__`, `__bool__`
- [ ] Tại sao `for record in self` hoạt động
- [ ] Empty recordset vs None

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/models.py` | Class `BaseModel` | Tìm `__iter__`, `__len__` |
| `odoo/models.py` | Class `Model` | Inheritance từ BaseModel |

### ✅ Tiêu chí đạt
- [ ] Giải thích được tại sao `self` không bao giờ đảm bảo là 1 record
- [ ] Viết được model `lib.book` load không lỗi
- [ ] Chạy được `env['lib.book'].search([])` trong shell

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | 10 | Hiểu rõ BaseModel, env, recordset |
| Viết code (2h) | 9 | Tạo model thành công |
| Shell/Debug (2h) | 9 | Debug name_get, len(self) |
| Tổng kết (1h) | 10 | Trả lời đủ câu hỏi |
| **TỔNG NGÀY 1** | **9.5/10** | ✅ Xuất sắc! |

### 📌 Ghi chú AI
> **Key takeaways Day 1:**
> - `self` luôn là recordset (0..n), không giả định singleton
> - `env` = context + registry + security
> - UI tự gọi `name_get()` ngầm
> - Domain: prefix notation, `|` chỉ ăn 2 điều kiện
> - `_rec_name` quyết định display name

### ⚠️ Lưu ý cho Day 2
> Sẵn sàng học `mapped()`, `filtered()` - vectorized methods trên recordset

---

## Day 2: search / browse / filtered / mapped

### 🎯 Mục đích chủ đạo
Master 4 methods quan trọng nhất để query và transform recordsets.

### 📚 Đề mục cần học
- [ ] `search()` - tìm records theo domain
- [ ] `browse()` - lấy record theo IDs
- [ ] `filtered()` - lọc recordset theo lambda
- [ ] `mapped()` - transform recordset
- [ ] **Record Cache** - First access = DB read, subsequent = cache hit
- [ ] **Prefetch optimization** - Batch loading pattern trong loops
- [ ] **Performance gotcha** - Tránh N+1 queries với mapped()

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/models.py` | Method `search` | Tìm `def search` |
| `odoo/models.py` | Method `browse` | Tìm `def browse` |
| `odoo/models.py` | Method `filtered` | Tìm `def filtered` |
| `odoo/models.py` | Method `mapped` | Tìm `def mapped` |
| `odoo/models.py` | Prefetch mechanism | Tìm `prefetch` |

### ✅ Tiêu chí đạt
- [ ] Phân biệt được khi nào dùng search vs browse
- [ ] Viết được `books.mapped('name')` và hiểu kết quả
- [ ] Viết được `books.filtered(lambda b: b.name)` và hiểu kết quả
- [ ] In được `self` trong method và biết số records
- [ ] **Hiểu cache mechanism**: Tại sao access lần 2 nhanh hơn?
- [ ] **Tránh N+1**: Khi nào `mapped('field')` tốt hơn loop?

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Lý thuyết | 10 | Hiểu rõ 6 concepts + advanced |
| Thực hành | 9 | 4/4 exercises, nhầm search/filtered ban đầu |
| Kiểm tra | 10 | Trả lời đúng câu hỏi tổng hợp |
| **TỔNG NGÀY 2** | **9.5/10** | ✅ Xuất sắc |

### 📌 Ghi chú AI
> ✅ **Hoàn thành**: search/browse/filtered/mapped/sorted/chaining
> ✅ **Strengths**: Hiểu lazy loading, return types, performance
> ⚠️ **Improvement**: Ban đầu nhầm search() vs filtered(), đã sửa
> 💡 **Insight**: Cần exercises phức tạp hơn Day 3+

### ⚠️ Lưu ý cho Day 3
> 🚀 Day 3: CRUD (create/write/unlink) + Form View
> 📝 Exercises cần multi-step, real-world scenarios
> 💪 Learner ready với foundation vững

---

## Day 3: create / write / unlink + Form View (task_management)

### 🎯 Mục đích chủ đạo
Hiểu lifecycle của record (tạo, sửa, xóa) và tạo task_management module với model `task.task`.

### 📦 Module Setup
```
custom_addons/task_management/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── task.py
└── views/
    └── task_views.xml
```

### 📚 Đề mục cần học
- [ ] `create()` - tạo record mới
- [ ] `write()` - cập nhật record
- [ ] `unlink()` - xóa record
- [ ] Override `create`/`write` đúng cách với `super()`
- [ ] Form view XML cơ bản

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/models.py` | Method `create` | Tìm `def create` |
| `odoo/models.py` | Method `write` | Tìm `def write` |
| `odoo/models.py` | Method `unlink` | Tìm `def unlink` |

### ✅ Tiêu chí đạt
- [ ] Tạo module `task_management` với model `task.task`
- [ ] Model có: name, description, state (Selection)
- [ ] Override `create` với `_logger.info(vals)`
- [ ] Tạo record từ UI và shell, so sánh `vals`
- [ ] Viết được form view cho `task.task`

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | 9 | Đọc create/write/unlink, phân biệt vals_list vs vals |
| Viết code (2h) | 9.5 | Module structure hoàn chỉnh, override methods đúng pattern |
| Shell/Debug (2h) | 8.5 | Hiểu CRUD lifecycle, form view structure |
| Tổng kết (1h) | 7.5 | 7/8 câu đúng, thiếu x2many commands |
| **TỔNG NGÀY 3** | **8.6/10** | ✅ Xuất sắc! |

### 📌 Ghi chú AI
> **Key takeaways Day 3:**
> - `create()` nhận vals_list, return recordset
> - `write()` apply cho TẤT CẢ records trong self
> - Override pattern: log TRƯỚC super() để lấy old values
> - Form view structure: `<form>` → `<sheet>` → `<group>` → `<notebook>`
> - Tư duy logic tốt: Tự phát hiện lỗi, áp dụng production attrs

### ⚠️ Lưu ý cho Day 4
> 🚀 Day 4: Tree, Search, Kanban views
> 📝 User đã hiểu `view_mode`, sẵn sàng học nhiều view types
> 💪 Module `task_management` có Form view hoàn chỉnh

---

## Day 4: Views - Tree, Search, Action, Menu, Kanban (task_management)

### 🎯 Mục đích chủ đạo
Tạo đầy đủ UI cho task_management: list view, search filters, menu, + Kanban basics.

### 📚 Đề mục cần học
- [ ] Tree view (list view)
- [ ] Search view + filters + group by
- [ ] Action (ir.actions.act_window)
- [ ] Menu items (ir.ui.menu)
- [ ] Kanban view basics (từ Context7: t-name="kanban-card")
- [ ] **group_expand** - Hiển thị tất cả Kanban columns kể cả khi trống
- [ ] **_expand_states pattern** - Method trả về list states cho Kanban

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/addons/base/views/res_partner_views.xml` | Tree view | `<tree>` tag |
| `odoo/addons/base/views/res_partner_views.xml` | Search view | `<search>` tag |
| `odoo/addons/project/views/project_views.xml` | Kanban reference | `<kanban>` tag |
| `odoo/fields.py` | group_expand | Tìm `group_expand` |

### ✅ Tiêu chí đạt
- [ ] Tạo được tree view cho `task.task`
- [ ] Tạo được search view với filter theo state
- [ ] Tạo được action và menu để truy cập module
- [ ] Module xuất hiện trong menu Odoo
- [ ] Tạo được Kanban view cơ bản
- [ ] **Implement group_expand cho Kanban:**
  - [ ] Tạo method `_expand_states(self, states, domain, order)`
  - [ ] Thêm `group_expand="_expand_states"` vào Selection field
  - [ ] Test: Tất cả columns hiện thị kể cả khi không có task

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | 8 | Read res_partner, project views |
| Lý thuyết (2h) | 9 | 12 concepts covered |
| Thực hành (2h) | 8 | 5 exercises completed |
| Kiểm tra (1h) | 9 | 8 questions |
| **TỔNG NGÀY 4** | **8.5/10** | _(Estimated retrospectively)_ |

### 📌 Ghi chú AI
> - Tree decorations với conditions
> - Search filters + group by
> - Kanban QWeb basic cards
> - Complete UI workflow

### ⚠️ Lưu ý cho Day 5
> - Binary fields, image upload
> - StatusBar widget

---

## Day 5: Fields System + Binary Image (task_management)

### 🎯 Mục đích chủ đạo
Hiểu Odoo Field là descriptors, các loại field phổ biến, + **Binary image field** cho ảnh bìa.

### 📚 Đề mục cần học
- [ ] Field descriptors (Char, Integer, Float, Boolean, Date, Datetime, Text)
- [ ] Selection field (đã dùng cho state)
- [ ] **Binary field** - cho image/file
- [ ] Field attributes: required, readonly, default, string
- [ ] Image widget trong XML (từ Context7)

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/fields.py` | Class `Field` | Base class |
| `odoo/fields.py` | Class `Binary` | Binary/Image field |
| `odoo/fields.py` | Class `Selection` | Selection field |

### ✅ Tiêu chí đạt
- [x] Thêm field `image = fields.Image('Cover')` vào `task.project` với max_width/max_height
- [x] Hiển thị image trong form view với widget="image"
- [x] **Thêm fields quan trọng vào `task.task`:**
  - [x] `due_date = fields.Datetime('Due Date')` - **DEADLINE tracking**
  - [x] `hours_estimated = fields.Float('Estimated Hours')` - Effort planning
  - [x] `hours_spent = fields.Float('Hours Spent')` - Actual effort
- [x] Giải thích được Field là descriptor, không phải value

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | 7 | fields.py - Field, Image, Selection classes |
| Viết code (2h) | 9 | 5/5 exercises, Trello-style kanban |
| Shell/Debug (2h) | 8 | Kanban image cần nhiều debug |
| Tổng kết (1h) | 8 | Exercise 5 debug quiz 2/3 |
| **TỔNG NGÀY 5** | **8/10** | ✅ Tốt - Sẵn sàng Day 6 |

### 📌 Ghi chú AI
> - Field là Python descriptor, không gán `self.field = fields.X()` trong method
> - Image field tự động resize, Binary không có
> - Kanban view cần declare fields trước `<templates>`
> - t-if/t-else cho conditional rendering trong QWeb
> - Float comparison dùng `float_compare()` hoặc round

### ⚠️ Lưu ý cho Day 6
> - Day 6 sẽ EXTEND task.project và task.task (dùng `_inherit`)
> - Thêm `project_id = fields.Many2one('task.project')` vào task.task
> - Thêm `task_ids = fields.One2many('task.task', 'project_id')` vào task.project
> - Tạo task.tag model mới với Many2many relationship

---

# 📅 PHASE 2: BUSINESS LOGIC (Day 6-10)

### 🛠️ Debug checklist (Phase 2)
- [ ] Log `vals` before/after `create()`/`write()` and compare with UI inputs
- [ ] Use `--log-level=debug_sql` for slow domains and N+1 detection
- [ ] Validate x2many commands with `mapped()` and `exists()`

---

## Day 6: Relationships - task.project, task.tag (M2O, O2M, M2M)

### 🎯 Mục đích chủ đạo
Master quan hệ giữa các model: **Project ↔ Task ↔ Tags** (pattern từ Context7).

### 📦 Thêm Models
```python
# EXTEND task.project (created in Day 5) - Add relationships
class Project(models.Model):
    _inherit = 'task.project'  # EXTEND, không tạo mới!
    task_ids = fields.One2many('task.task', 'project_id')  # O2M

# CREATE task.tag - Labels cho tasks (NEW model)
class TaskTag(models.Model):
    _name = 'task.tag'
    name = fields.Char()
    color = fields.Integer()

# EXTEND task.task - Add relationships
class Task(models.Model):
    _inherit = 'task.task'  # EXTEND existing model
    project_id = fields.Many2one('task.project')  # M2O to project
    tag_ids = fields.Many2many('task.tag')  # M2M to tags
```

### 📚 Đề mục cần học
- [ ] Many2one (M2O): task.task → task.project
- [ ] One2many (O2M): project.task_ids (inverse của M2O)
- [ ] Many2many (M2M): task.task ↔ task.tag
- [ ] Comodel_name, inverse_name, relation
- [ ] **ondelete** - cascade, set null, restrict (Data integrity)
- [ ] **check_company** - Multi-company support
- [ ] **Command patterns** - Command.create, link, set, clear, unlink
- [ ] **delegate** - Field delegation pattern

### 📂 Source code cần đọc (+ Context7 patterns)
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/fields.py` | Class `Many2one` | Tìm `class Many2one` |
| `odoo/fields.py` | Class `One2many` | Tìm `class One2many` |
| `odoo/fields.py` | Class `Many2many` | Tìm `class Many2many` |
| `odoo/fields.py` | Command class | Tìm `class Command` |

### ✅ Tiêu chí đạt
- [ ] Tạo model `task.project` và `task.tag`
- [ ] Thêm `project_id = fields.Many2one('task.project', ondelete='cascade')` - **Với ondelete!**
- [ ] **Thêm `assigned_user_id = fields.Many2one('res.users', 'Assigned To')`** - Track assignee
- [ ] Thêm `tag_ids = fields.Many2many('task.tag')` vào task.task
- [ ] Truy cập được `task.project_id.name` (M2O) và `project.task_ids` (O2M)
- [ ] **CRUD Commands pattern:**
  - [ ] `Command.create({'name': 'New'})` - Tạo mới inline
  - [ ] `Command.link(id)` - Liên kết existing record
  - [ ] `Command.set([ids])` - Replace tất cả
  - [ ] `Command.clear()` - Xóa tất cả links
- [ ] **Test ondelete**: Delete project → Tasks auto-deleted
- [ ] **Enhance Kanban view với QWeb loops:**
  - [ ] Học `t-foreach` để loop qua `tag_ids`
  - [ ] Hiển thị tags trong Kanban card với colors

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | 10 | M2O, O2M, M2M class - hiểu sâu |
| Viết code (2h) | 9 | Exercises hoàn thành, 1 lỗi syntax nhỏ |
| Shell/Debug (2h) | 9 | Fix circular M2M relation_table issue |
| Tổng kết (1h) | 9 | 10/10 câu hỏi + Bonus Deadlock/Recursion |
| **TỔNG NGÀY 6** | **9.0/10** | ✅ Xuất sắc! |

### ❓ Câu hỏi kiểm tra
1. **Concept**: Khi nào dùng `ondelete='cascade'` vs `ondelete='restrict'`? ✅ Trả lời đúng
2. **Debug**: Task có `project_id` nhưng `task.project_id.name` trả về `False`. ✅
3. **Command**: Viết code để thêm 2 tags mới và xóa 1 tag cũ trong một lần write. ✅
4. **Performance**: Tại sao `task.project_id.name` nhanh hơn? ✅
5. **Design**: Khi nào nên dùng Many2many vs tạo model trung gian? ✅
6. **Gotcha**: Xảy ra gì khi `inverse_name` sai trong One2many? ✅

### 🔗 Liên kết kiến thức
- **Prerequisites**: Day 3 (CRUD), Day 5 (Fields)
- **Builds on**: Viết fields, hiểu model structure
- **Prepares for**: Day 7 (Computed sử dụng relational fields)
- **Module state sau Day 6**: task.task có project_id, tag_ids, assigned_user_id

### 📌 Ghi chú AI
> **Key takeaways Day 6:**
> - M2O tạo FK column, O2M là virtual (không column)
> - M2M cần explicit `relation`, `column1`, `column2` khi khai báo 2 phía
> - Command patterns: `(0,0,{})` create, `(4,id,0)` link, `(5,0,0)` clear, `(6,0,[ids])` set
> - Transaction lifecycle: 1 Request = 1 Transaction (lock giữ đến return)
> - **Bonus**: Deadlock = vòng tròn khóa lẫn nhau, Odoo auto-retry 5 lần

### ⚠️ Lưu ý cho Day 7
> Day 7 sẽ tạo computed fields dựa trên relational fields đã học:
> - `task_count` = len(project.task_ids) 
> - `is_overdue` dựa vào state và due_date
> - Cần hiểu rõ M2O/O2M trước khi học @api.depends

---

## Day 7: Computed Fields + @api.depends (task_management)

### 🎯 Mục đích chủ đạo
Tạo computed fields cho `task.task` và `task.project` - tự động tính toán.

### 📚 Đề mục cần học
- [ ] Computed field (compute parameter)
- [ ] @api.depends decorator
- [ ] Store=True vs Store=False
- [ ] Compute method pattern
- [ ] **inverse** - Make computed field editable
- [ ] **search** - Enable search on computed fields
- [ ] **Performance** - Cascade recompute costs

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/api.py` | `depends` decorator | Tìm `def depends` |
| `odoo/fields.py` | Computed field logic | Tìm `compute` |
| `odoo/fields.py` | inverse, search | Tìm `inverse`, `search` |

### ✅ Tiêu chí đạt
- [ ] Tạo `task_count = fields.Integer(compute='_compute_task_count')` trên `task.project`
- [ ] Tạo `hours_remaining = fields.Float(compute='_compute_hours')` trên `task.task`
- [ ] **Tạo `is_overdue = fields.Boolean(compute='_compute_is_overdue')`** - **Overdue detection**
  - [ ] `@api.depends('state', 'due_date')` - Multiple dependencies
  - [ ] Logic: `state != 'done' and due_date < now()` - Datetime comparison
  - [ ] Use in tree decoration: `decoration-danger="is_overdue"` - Production UX
- [ ] Hiểu khi nào cần `store=True`
- [ ] Hiểu `@api.depends` trigger recompute khi nào
- [ ] **Editable computed với inverse:**
  - [ ] Tạo computed `progress = hours_spent / hours_estimated * 100`
  - [ ] Thêm `inverse='_inverse_progress'` để edit được
- [ ] **Searchable computed:**
  - [ ] Thêm `search='_search_is_overdue'`
  - [ ] Test: Filter tasks overdue trong search view

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | 9 | Hiểu depends, resolve_depends, Field class |
| Viết code (2h) | 9 | task_count, hours_remaining, progress all correct |
| Shell/Debug (2h) | 8 | Test tốt, debug cache issue, kanban image |
| Tổng kết (1h) | 8 | Questions 8.5/10 |
| **TỔNG NGÀY 7** | **8.5/10** | Strong performance |

### ❓ Câu hỏi kiểm tra
1. **Concept**: `store=True` thay đổi gì về cách computed field hoạt động?
2. **Debug**: Computed field không recompute khi thay đổi related field. Tại sao?
3. **Performance**: Tại sao `@api.depends('task_ids.state')` có thể chậm?
4. **Inverse**: Viết inverse method cho `progress = hours_spent / hours_estimated * 100`.
5. **Search**: Viết search method để filter `is_overdue = True`.
6. **Design**: Khi nào dùng computed vs regular field?

### 🔗 Liên kết kiến thức
- **Prerequisites**: Day 6 (Relational fields cho @api.depends)
- **Builds on**: M2O, O2M để tạo dependencies
- **Prepares for**: Day 8 (Constraints cũng validate computed values)
- **Module state sau Day 7**: task.task có is_overdue, hours_remaining; project có task_count

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 8
> Day 8 thêm constraints để validate data từ computed fields:
> - hours_estimated >= 0 (Python constraint)
> - is_overdue kết hợp với constraint logic
> - @api.ondelete để validate trước khi xóa

---

## Day 8: Constraints - @api.constrains + SQL (task_management)

### 🎯 Mục đích chủ đạo
Đảm bảo data integrity cho `task.task` bằng Python và SQL constraints.

### 📚 Đề mục cần học
- [ ] @api.constrains decorator
- [ ] ValidationError exception
- [ ] _sql_constraints
- [ ] Khi nào dùng Python vs SQL constraint
- [ ] **@api.ondelete** - Validate before delete
- [ ] **at_uninstall parameter** - Skip check when uninstall module

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/api.py` | `constrains` decorator | Tìm `def constrains` |
| `odoo/models.py` | `_sql_constraints` | Tìm `_sql_constraints` |
| `odoo/exceptions.py` | `ValidationError` | Exception class |
| `odoo/api.py` | `ondelete` decorator | Tìm `def ondelete` |

### ✅ Tiêu chí đạt
- [ ] Tạo Python constraint: `hours_estimated >= 0` trên `task.task`
- [ ] Tạo SQL constraint: `date_end >= date_start`
- [ ] Hiểu lỗi ValidationError xuất hiện ở đâu trong UI
- [ ] **@api.ondelete pattern:**
  - [ ] Không cho xóa task đã `state='done'`
  - [ ] Raise UserError với message rõ ràng
  - [ ] Test: Cố xóa done task → Error message

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | 10 | Đọc constraint/protection methods kỹ lưỡng |
| Viết code (2h) | 10 | 5/5 exercises (SQL + Python constraints, Unlink) |
| Shell/Debug (2h) | 10 | Fix float comparison debug issues |
| Tổng kết (1h) | 10 | 9/9 questions correct (1 correction for Mentor) |
| **TỔNG NGÀY 8** | **10/10** | ✅ Excellent! |

### 📌 Ghi chú AI
> **Key takeaways Day 8:**
> - SQL Constraints (`_sql_constraints`) = DB integrity (Unique, Check)
> - Python Constraints (`@api.constrains`) = Application logic (Cross-field)
> - `float_compare` > `==` for floats
> - Implicit write by Stored Computed fields triggers constraints
> - Protection: `unlink()` override > `@api.ondelete` (complex cases)

### ❓ Câu hỏi kiểm tra
1. **Concept**: Khi nào dùng Python constraint vs SQL constraint? Cho 2 ví dụ.
2. **Debug**: ValidationError xuất hiện nhưng không rõ field nào lỗi. Làm sao fix?
3. **SQL**: Viết `_sql_constraints` cho: `name` phải unique trong mỗi project.
4. **@api.ondelete**: Tại sao cần `at_uninstall=False`?
5. **Error handling**: ValidationError vs UserError - khi nào dùng cái nào?
6. **Gotcha**: Constraint không chạy khi import data qua CSV. Tại sao?

### 🔗 Liên kết kiến thức
- **Prerequisites**: Day 7 (Computed fields để hiểu validation logic)
- **Builds on**: is_overdue để thêm constraint
- **Prepares for**: Day 9 (Onchange cũng validate UI-side)
- **Module state sau Day 8**: task.task có constraints cho hours, dates; @api.ondelete

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 9
> Day 9 kết hợp computed + onchange + wizard:
> - Onchange auto-fill user từ project (UI-side)
> - Wizard dùng context active_ids từ Day 6 relationships
> - Integration test tất cả features Phase 2

---

## Day 9: @api.onchange + Wizards (task_management)

### 🎯 Mục đích chủ đạo
Phân biệt onchange (UI-only) vs computed (data-driven) + **Tạo Wizard đầu tiên**.

### 🧭 Scope split
- **Core (must)**: @api.onchange + Wizard bulk update + context active_ids
- **Advanced (required)**: Smoke test nhanh; full integration test chuyển về Day 20
- **Rule**: Nếu thiếu thời gian, kéo dài ngày; không bỏ phần Advanced.

### 📚 Đề mục cần học
- [ ] @api.onchange decorator
- [ ] Onchange chỉ chạy khi UI thay đổi
- [ ] Computed chạy khi data thay đổi
- [ ] Khi nào dùng cái nào
- [ ] **TransientModel** - Model tạm thời cho Wizard
- [ ] **Wizard action** - target='new' và context passing
- [ ] **active_ids, active_model** - context đặc biệt

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/api.py` | `onchange` decorator | Tìm `def onchange` |
| `odoo/addons/base/wizard/` | Wizard examples | Toàn bộ folder |

### ✅ Tiêu chí đạt
- [ ] Tạo onchange: chọn `project_id` → auto-fill `user_id` từ project manager
- [ ] Phân biệt được khi nào dùng onchange vs computed
- [ ] **Tạo Wizard "Bulk State Change":**
  - [ ] Model `task.state.wizard` (TransientModel)
  - [ ] Field `new_state` (Selection) - chọn state mới
  - [ ] Method `action_apply()` - update tất cả selected tasks
  - [ ] Action với `target='new'` và `binding_model_id`
- [ ] **Test Wizard:** Select nhiều tasks → Action → Wizard → Apply

### 📦 Output artifacts
- Wizard model + view + action (binding)
- Onchange logic trong task/task.project
- Ghi chú test: UI-only behavior vs stored data
### 🧪 Smoke test (15-20 phút)
- [ ] Create Project → Create Tasks → Assign tags
- [ ] Test onchange trên UI
- [ ] Test Wizard bulk action

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | _ | |
| Viết code (2h) | _ | |
| Shell/Debug (2h) | _ | |
| Tổng kết (1h) | _ | |
| **TỔNG NGÀY 9** | **_/10** | |

### ❓ Câu hỏi kiểm tra
1. **Concept**: Onchange chạy khi nào? Computed chạy khi nào? So sánh.
2. **Debug**: Onchange không chạy khi update qua shell. Tại sao?
3. **Wizard**: Tại sao wizard dùng TransientModel thay vì Model?
4. **Context**: Lấy danh sách selected IDs từ context như thế nào?
5. **Action**: Viết action với `binding_model_id` để wizard xuất hiện trong Actions menu.
6. **Integration**: Nếu wizard update state, computed field nào sẽ recompute?

### 🔗 Liên kết kiến thức
- **Prerequisites**: Day 6 (Relationships cho context), Day 7 (Computed)
- **Builds on**: Tất cả features Phase 2
- **Prepares for**: Day 10 (Context sâu hơn + Report)
- **Module state sau Day 9**: Wizard bulk change, onchange auto-fill, Phase 2 complete

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 10
> Day 10 kết thúc Phase 2:
> - Context + Domain sâu hơn
> - QWeb Report PDF đầu tiên (hiển thị tasks by project)
> - sudo(), with_context() cho backend operations

---

## Day 10: Context, Domain + QWeb Reports

### 🎯 Mục đích chủ đạo
Hiểu context truyền thông tin, domain filter records + **Tạo PDF Report đầu tiên**.

### 📚 Đề mục cần học
- [ ] `self.env.context` - dictionary truyền suốt request
- [ ] `with_context()` - thay đổi context
- [ ] Domain syntax: `[('field', 'operator', 'value')]`
- [ ] Domain operators: =, !=, in, not in, like, ilike, >, <
- [ ] **QWeb Template Engine** - t-foreach, t-field, t-if
- [ ] **ir.actions.report** - PDF report action
- [ ] **web.external_layout** - Header/Footer template
- [ ] **sudo()** - Bypass security cho backend operations
- [ ] **with_user()** - Execute as different user

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/api.py` | Environment class | Tìm `class Environment` |
| `odoo/osv/expression.py` | Domain parsing | Tìm `TERM_OPERATORS` |
| `odoo/addons/base/reports/` | Report examples | Toàn bộ folder |
| `odoo/models.py` | sudo, with_context | Tìm `def sudo`, `def with_context` |

### ✅ Tiêu chí đạt
- [ ] Debug được `self.env.context` trong method
- [ ] Hiểu vì sao search với context khác cho kết quả khác
- [ ] Viết được domain phức tạp (AND, OR)
- [ ] **Tạo "Task List Report" PDF:**
  - [ ] QWeb template với `t-foreach` loop tasks
  - [ ] Hiển thị: name, state, priority, due_date
  - [ ] Group tasks by state
  - [ ] Sử dụng `web.external_layout` cho header/footer
- [ ] **Report Action:** Nút "Print" trong Project form
- [ ] **Test Report:** Generate PDF từ UI
- [ ] **Environment methods:**
  - [ ] Dùng `sudo()` để bypass security trong backend logic
  - [ ] Dùng `with_context()` để pass custom values

### 📦 Output artifacts
- Report XML + QWeb template
- report/ folder structure

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | _ | |
| Viết code (2h) | _ | |
| Shell/Debug (2h) | _ | |
| Tổng kết (1h) | _ | |
| **TỔNG NGÀY 10** | **_/10** | |

### ❓ Câu hỏi kiểm tra
1. **Concept**: `env.context.get('key')` vs `env.context['key']` - khác nhau gì?
2. **Domain**: Viết domain: tasks overdue HOẶC priority='high' trong project X.
3. **QWeb**: `t-field` vs `t-esc` khi nào dùng cái nào?
4. **sudo()**: Tại sao report cần `sudo()` để lấy đủ data?
5. **Report**: Làm sao group tasks by state trong QWeb template?
6. **Gotcha**: Report PDF trống - debug như thế nào?

### 🔗 Liên kết kiến thức
- **Prerequisites**: Day 9 (Wizard dùng context), Day 6 (Relationships cho report data)
- **Builds on**: Context từ wizard, domain từ search views
- **Prepares for**: Phase 3 Security (sudo() quan trọng cho bypass)
- **Module state sau Day 10**: PDF report hoàn chỉnh, Phase 2 COMPLETE

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 11
> Phase 3 SECURITY bắt đầu:
> - ACL restricts MODEL-level access
> - Sử dụng sudo() từ Day 10 để bypass trong backend
> - ACL sẽ ảnh hưởng report nếu user không có quyền

---

# 📅 PHASE 3: SECURITY (Day 11-13) + SUBTASKS (Day 14)

### 🛠️ Debug checklist (Phase 3)
- [ ] Test with different users/groups; compare `sudo()` vs normal
- [ ] Confirm ACL + record rules with dev mode access checks
- [ ] Verify access errors in UI and server logs

---

## Day 11: ACL - Access Control List (task_management)

### 🎯 Mục đích chủ đạo
Hiểu cách Odoo kiểm soát ai được CRUD model nào cho `task_management`.

### 📚 Đề mục cần học
- [ ] File `ir.model.access.csv` structure
- [ ] Columns: id, name, model_id:id, group_id:id, perm_read/write/create/unlink
- [ ] Base user vs Admin
- [ ] AccessError khi không có quyền

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/addons/base/security/ir.model.access.csv` | ACL format | Toàn bộ file |
| `odoo/addons/base/models/ir_model.py` | IrModelAccess class | Tìm `class IrModelAccess` |

### ✅ Tiêu chí đạt
- [ ] Tạo được `security/ir.model.access.csv` cho `task_management` (task.task, task.project, task.tag)
- [ ] Test user không quyền → xem AccessError
- [ ] Hiểu ACL chỉ check ở model level, không check record

### 📦 Output artifacts
- `security/ir.model.access.csv` entries đầy đủ cho 3 models
- Checklist test user quyền/không quyền

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | _ | |
| Viết code (2h) | _ | |
| Shell/Debug (2h) | _ | |
| Tổng kết (1h) | _ | |
| **TỔNG NGÀY 11** | **_/10** | |

### ❓ Câu hỏi kiểm tra
1. **Concept**: ACL check ở level nào? Model hay Record?
2. **CSV syntax**: `model_id:id` có format gì? Cho ví dụ cho `task.task`.
3. **Debug**: User thấy AccessError nhưng admin thì không. Làm sao debug?
4. **group_id**: Nếu `group_id/id` trống, ai có quyền?
5. **Wizard ACL**: Wizard model cũng cần ACL không? Tại sao?
6. **Manifest**: ACL file phải khai báo ở đâu trong `__manifest__.py`?

### 🔗 Liên kết kiến thức
- **Prerequisites**: Day 10 (sudo() để bypass ACL)
- **Builds on**: Module từ Phase 2 cần ACL để hoạt động
- **Prepares for**: Day 12 (Groups để tổ chức ACL)
- **Module state sau Day 11**: ACL cho task.task, task.project, task.tag

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 12
> Day 12 tạo Groups để tổ chức ACL:
> - group_manager vs group_member
> - ACL từ Day 11 sẽ reference groups từ Day 12
> - Implied groups cho kế thừa quyền

---

## Day 12: Groups (task_management)

### 🎯 Mục đích chủ đạo
Tổ chức quyền cho `task_management` thành groups: Manager vs Member.

### 📚 Đề mục cần học
- [ ] res.groups model
- [ ] Implied groups (inheritance)
- [ ] Category groups
- [ ] groups="" attribute trong XML

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/addons/base/security/base_groups.xml` | Group definitions | Toàn bộ file |
| `odoo/addons/base/models/res_users.py` | Groups relation | Tìm `groups_id` |

### ✅ Tiêu chí đạt
- [ ] Tạo được groups: `task_management.group_manager`, `task_management.group_member`
- [ ] Manager: full CRUD trên tất cả models
- [ ] Member: chỉ đọc và tạo tasks, không xóa
- [ ] Hide delete button dựa trên groups

### 📦 Output artifacts
- `security.xml` groups + category
- View attrs/groups cho nút delete

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | _ | |
| Viết code (2h) | _ | |
| Shell/Debug (2h) | _ | |
| Tổng kết (1h) | _ | |
| **TỔNG NGÀY 12** | **_/10** | |

### ❓ Câu hỏi kiểm tra
1. **Concept**: Implied groups hoạt động thế nào? Cho ví dụ.
2. **XML**: Viết XML tạo group `group_manager` kế thừa từ `group_member`.
3. **View**: Làm sao hide nút Delete chỉ cho Member, không cho Manager?
4. **Category**: Tại sao cần category cho groups?
5. **Debug**: User trong group nhưng vẫn không có quyền. Làm sao trace?
6. **ACL update**: Sau khi tạo groups, ACL cần update gì?

### 🔗 Liên kết kiến thức
- **Prerequisites**: Day 11 (ACL để gán vào groups)
- **Builds on**: ACL rows sờ dụng group_id từ Day 12
- **Prepares for**: Day 13 (Record Rules filter records theo groups)
- **Module state sau Day 12**: 2 groups (manager/member), ACL updated với groups

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 13
> Day 13 thêm Record Rules (row-level):
> - ACL = model-level, Record Rules = row-level
> - Rule sử dụng groups từ Day 12
> - domain_force dùng syntax từ Day 10

---

## Day 13: Record Rules + Security Debug (ir.rule)

### 🎯 Mục đích chủ đạo
Kiểm soát user chỉ thấy/sửa records cụ thể (row-level security) + **Debug security issues**.

### 📚 Đề mục cần học
- [ ] ir.rule model
- [ ] domain_force field
- [ ] Global rules vs Group rules
- [ ] perm_read/write/create/unlink trên rule
- [ ] **Multi-company rules** - company_ids pattern
- [ ] **Company-aware domains** - ('company_id', 'in', company_ids)
- [ ] **Security Debug:** Đọc AccessError, sudo() bypass, log rule evaluation
- [ ] **Security flow**: request → ACL → Record Rule → Data
- [ ] **Debug tools**: `_check_access()`, `check_field_access_rights()`

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/addons/base/models/ir_rule.py` | IrRule class, `_compute_domain` | Tìm `class IrRule` |
| `odoo/addons/base/security/base_security.xml` | Rule examples | Tìm `ir.rule` |
| `odoo/addons/sale/security/` | Multi-company examples | Toàn bộ folder |
| `odoo/models.py` | `check_access_rights`, `_check_access` | Kiểm tra ACL |

### ✅ Tiêu chí đạt
- [ ] Tạo được rule: member chỉ thấy tasks mình được assign
- [ ] Test rule sai → debug tại sao không thấy records
- [ ] Hiểu ACL vs Record Rule khác nhau
- [ ] **Multi-company rule pattern:**
  - [ ] Thêm `company_id` field vào task.task và task.project
  - [ ] Tạo rule: `['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]`
  - [ ] Test: User company A không thấy tasks company B
- [ ] **Debug 3 security bugs:**
  - [ ] Bug 1: Missing ACL cho wizard model
  - [ ] Bug 2: Record rule sai domain
  - [ ] Bug 3: Group membership không đúng
- [ ] **Integration Test Security:**
  - [ ] Test Phase 3 với 2 users (manager/member)
  - [ ] Verify: member không thấy tasks của member khác
  - [ ] Verify: manager thấy hết

### 📦 Output artifacts
- Record rules trong `security.xml`
- `company_id` field + test notes multi-company
- 3 bug scenarios + root-cause notes
- Checklist test security (manager vs member)

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | _ | |
| Viết code (2h) | _ | |
| Shell/Debug (2h) | _ | |
| Tổng kết (1h) | _ | |
| **TỔNG NGÀY 13** | **_/10** | |

### ❓ Câu hỏi kiểm tra
1. **Concept**: ACL vs Record Rule - khi nào dùng cái nào?
2. **domain_force**: Viết rule: Member chỉ thấy tasks assigned cho mình hoặc unassigned.
3. **Global rule**: Tại sao global rule không có group? Ảnh hưởng gì?
4. **Multi-company**: `company_ids` lấy từ đâu trong domain_force?
5. **Debug**: User không thấy records dù ACL = full access. Làm sao debug?
6. **sudo()**: sudo() bypass cả ACL và Record Rule?
7. **Debug flow**: Security check thực hiện theo thứ tự nào? ACL hay Rule trước?
8. **AccessError**: Làm sao phân biệt lỗi do ACL vs Record Rule?
9. **Common bug**: Tại sao wizard hay bị AccessError?
10. **Production**: Khi nào nên dùng sudo() trong production code?

### 🔗 Liên kết kiến thức
- **Prerequisites**: Day 10 (Domain), Day 12 (Groups)
- **Builds on**: Domain syntax, group references
- **Prepares for**: Day 14 (Subtasks - self-referential relationships)
- **Module state sau Day 13**: Security hoàn chỉnh (ACL + Groups + Rules + Debug skills), Phase 3 COMPLETE

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 14
> Day 14 chuyển sang Phase 3b - Subtasks:
> - Self-referential Many2one (parent_id)
> - One2many inverse (child_ids)
> - Recursive computed fields (subtask_count)

---

## Day 14: Subtasks - Self-Referential Relationships (Phase 3b)

### 🎯 Mục đích chủ đạo
Implement subtasks với self-referential Many2one và computed subtask_count.

### 📚 Đề mục cần học
- [ ] **Self-referential Many2one** - task.task → task.task (parent_id)
- [ ] **Inverse One2many** - child_ids từ parent_id
- [ ] **Recursive computed fields** - subtask_count counting children
- [ ] **Domain với parent** - Chỉ hiển thị parent tasks trong dropdown
- [ ] **View hierarchy** - Hiển thị subtasks trong form view
- [ ] **Gotchas**: Circular reference prevention, recursion depth

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/addons/project/models/project.py` | parent_id pattern | Tìm `parent_id` |
| `odoo/fields.py` | Self-referential check | Tìm `comodel_name` |
| `odoo/addons/hr/models/hr_employee.py` | Manager hierarchy | Tìm `parent_id` |

### ✅ Tiêu chí đạt
- [ ] **Add parent_id field:**
  - [ ] `parent_id = fields.Many2one('task.task', string='Parent Task', index=True)`
  - [ ] Domain: `[('id', '!=', id), ('parent_id', '=', False)]` - Chỉ show top-level tasks
  - [ ] ondelete='cascade' - Xóa parent → xóa subtasks
- [ ] **Add child_ids field:**
  - [ ] `child_ids = fields.One2many('task.task', 'parent_id', string='Subtasks')`
- [ ] **Add subtask_count computed:**
  - [ ] `subtask_count = fields.Integer(compute='_compute_subtask_count')`
  - [ ] @api.depends('child_ids')
- [ ] **Update Views:**
  - [ ] Form: Tab "Subtasks" với O2M widget
  - [ ] Tree: Column subtask_count với badge
  - [ ] Kanban: Show subtask indicator
- [ ] **Test scenarios:**
  - [ ] Create task → Add subtask → Verify count
  - [ ] Delete parent → Verify subtasks deleted
  - [ ] Prevent circular reference (parent = child)

### 📦 Output artifacts
- Updated task.py với parent_id, child_ids, subtask_count
- Updated task_views.xml với Subtasks tab
- Test notes: hierarchy và deletion cascade

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | _ | |
| Viết code (2h) | _ | |
| Shell/Debug (2h) | _ | |
| Tổng kết (1h) | _ | |
| **TỔNG NGÀY 14** | **_/10** | |

### ❓ Câu hỏi kiểm tra
1. **Self-ref**: Tại sao cần domain `('id', '!=', id)` cho parent_id?
2. **Circular**: Làm sao prevent circular reference (A → B → A)?
3. **Cascade**: ondelete='cascade' vs 'set null' cho subtasks - chọn cái nào?
4. **Computed**: `subtask_count` cần store=True không? Tại sao?
5. **View**: Hiển thị subtasks trong Kanban như thế nào?
6. **Performance**: Với nhiều levels (sub-sub-tasks), performance concern gì?

### 🔗 Liên kết kiến thức
- **Prerequisites**: Day 6 (Relationships M2O/O2M), Day 7 (Computed fields)
- **Builds on**: Relationships + computed logic
- **Prepares for**: Day 15 (Module Reading - thấy hierarchy patterns)
- **Module state sau Day 14**: Subtasks hoàn chỉnh (parent_id, child_ids, subtask_count)

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 15
> Phase 4 MODULE READING bắt đầu:
> - Đọc module Odoo có sẵn (res.partner)
> - Thấy security patterns trong production module
> - mail.thread integration basics

---

# 📅 PHASE 4: MODULE READING (Day 15-17)

### 🛠️ Debug checklist (Phase 4)
- [ ] Trace overrides with `_logger` and check `super()` order
- [ ] Inspect view inheritance results in developer mode
- [ ] Compare context propagation across inherited methods

---

## Day 15: Read Existing Module + mail.thread Integration

### 🎯 Mục đích chủ đạo
Đọc và hiểu module có sẵn của Odoo (res_partner) + **Integrate mail.thread cho chatter**.

### 📚 Đề mục cần học
- [ ] File structure của module chuẩn
- [ ] __manifest__.py
- [ ] models/, views/, security/
- [ ] Trace flow từ menu → action → view → model
- [ ] **mail.thread mixin** - Chatter integration
- [ ] **mail.activity.mixin** - Activity scheduling
- [ ] **Tracking fields** - track_visibility parameter

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/addons/base/models/res_partner.py` | Partner model | Toàn bộ file |
| `odoo/addons/base/__manifest__.py` | Manifest | Toàn bộ file |
| `odoo/addons/base/views/res_partner_views.xml` | Views | Toàn bộ file |
| `odoo/addons/mail/models/mail_thread.py` | mail.thread | Tìm `class MailThread` |

### ✅ Tiêu chí đạt
- [ ] Vẽ được diagram: file nào liên quan đến res.partner
- [ ] Hiểu flow data từ UI → model
- [ ] Tìm được method nào được override
- [ ] **mail.thread integration cho task.task:**
  - [ ] Add `_inherit = ['mail.thread', 'mail.activity.mixin']`
  - [ ] Add `'mail'` to depends trong __manifest__.py
  - [ ] Add chatter widget trong form view: `<div class="oe_chatter">...</div>`
  - [ ] Add tracking to important fields: `tracking=True`
- [ ] **Test chatter:** Post message, log changes, schedule activity

### 📦 Output artifacts
- Sơ đồ module (flow + file map)
- Notes các method override quan trọng
- Updated task.task với mail.thread

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | _ | |
| Viết code (2h) | _ | |
| Shell/Debug (2h) | _ | |
| Tổng kết (1h) | _ | |
| **TỔNG NGÀY 15** | **_/10** | |

### ❓ Câu hỏi kiểm tra
1. **Structure**: Module Odoo chuẩn có những folder nào?
2. **Manifest**: `depends` và `data` trong manifest khác nhau thế nào?
3. **Flow**: Trace flow khi user click menu đến xem record.
4. **Patterns**: res.partner dùng computed fields nào? Tại sao?
5. **mail.thread**: message_post() làm gì? Khi nào được gọi tự động?
6. **Tracking**: tracking=True hoạt động thế nào? Store ở đâu?
7. **Activity**: mail.activity.mixin cho phép làm gì trong UI?

### 🔗 Liên kết kiến thức
- **Prerequisites**: Phase 1-3 (Hiểu models, views, security)
- **Builds on**: Kiến thức tổng hợp để đọc source
- **Prepares for**: Day 16 (Inheritance patterns)
- **Module state sau Day 15**: Hiểu cấu trúc module Odoo, task.task có chatter

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 16
> Day 16 học 3 loại Inheritance:
> - `_inherit` để extend res.partner
> - View inheritance với xpath từ Day 4
> - Advanced xpath patterns

---

## Day 16: Inheritance (Model + View)

### 🎯 Mục đích chủ đạo
Master 3 loại inheritance trong Odoo + **Advanced Xpath patterns**.

### 🧭 Scope split
- **Core (must)**: _inherit (extend), view inheritance basic xpath
- **Advanced (required)**: _inherits + advanced xpath patterns
- **Rule**: Nếu thiếu thời gian, kéo dài ngày; không bỏ phần Advanced.

### 📚 Đề mục cần học
- [ ] `_inherit` (extend existing model, same _name)
- [ ] `_inherit` + `_name` (prototype inheritance, new model)
- [ ] `_inherits` (delegation inheritance)
- [ ] View inheritance với xpath
- [ ] **Xpath position="attributes"** - Modify existing attributes
- [ ] **add/remove pattern** - Class manipulation
- [ ] **Dynamic expressions** - context.get(), parent.field trong views

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/models.py` | `_inherit` logic | Tìm `_inherit` |
| `odoo/models.py` | `_inherits` logic | Tìm `_inherits` |
| Module bất kỳ extend res.partner | View inheritance | `<xpath>` |
| Odoo docs | Xpath attributes | position="attributes" |

### ✅ Tiêu chí đạt
- [ ] Extend res.partner thêm field mới
- [ ] Extend view thêm field vào form
- [ ] Giải thích được 3 loại inheritance
- [ ] **Advanced Xpath:**
  - [ ] Dùng `position="attributes"` để set invisible/readonly
  - [ ] Dùng `<attribute name="class" add="mt-1" remove="mt-2"/>`
  - [ ] Dùng `invisible="context.get('key') and field == value"`
  - [ ] Dùng `invisible="parent.field_name"` trong subviews

### 📦 Output artifacts
- Model extension + view inheritance XML
- Ghi chú xpath patterns đã dùng

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | _ | |
| Viết code (2h) | _ | |
| Shell/Debug (2h) | _ | |
| Tổng kết (1h) | _ | |
| **TỔNG NGÀY 16** | **_/10** | |

### ❓ Câu hỏi kiểm tra
1. **Concept**: `_inherit` vs `_inherits` khác nhau thế nào? Cho ví dụ.
2. **Prototype**: `_inherit + _name` tạo ra gì? Khi nào dùng?
3. **Xpath**: Viết xpath để thêm field sau `phone` trong partner form.
4. **Attributes**: Viết xpath set `invisible="True"` cho field `website`.
5. **Dynamic**: `context.get('key')` trong invisible hoạt động thế nào?
6. **Gotcha**: Xpath không match - debug như thế nào?

### 🔗 Liên kết kiến thức
- **Prerequisites**: Day 15 (Hiểu module structure), Day 4 (Views basics)
- **Builds on**: View concepts, model relationships
- **Prepares for**: Day 17 (Override methods)
- **Module state sau Day 16**: Extended res.partner, view inheritance thành thạo

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 17
> Day 17 thực hành override + debug:
> - Dùng _inherit từ Day 16 để override methods
> - super() pattern cần nắm chắc
> - Common bugs và cách fix

---

## Day 17: Override Methods + Fix Bugs + Calendar/Assets

### 🎯 Mục đích chủ đạo
Override method đúng cách, fix bugs phổ biến + **Calendar view và frontend customization**.

### 📚 Đề mục cần học
- [ ] Override method pattern (super())
- [ ] **super() positioning** - Gọi trước hay sau logic?
- [ ] Đọc traceback và phân tích
- [ ] Debug step-by-step với logging
- [ ] **Common ORM bugs:**
  - [ ] `browse([])` trả về empty recordset
  - [ ] `mapped()` trên empty recordset
  - [ ] Missing `ensure_one()`
  - [ ] `vals` vs `vals_list` confusion
  - [ ] Recursive call không có `sudo()`
- [ ] **Debug tools**: `_logger.debug()`, `pdb`, traceback
- [ ] **Calendar view** - date_start, date_stop, color
- [ ] **Web assets bundles** - `web.assets_backend`, debug=assets
- [ ] **CSS/JS basics** - Static files, manifest registration

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/addons/sale/models/sale_order.py` | Override create/write | Tìm `def create` |
| `odoo/models.py` | super() pattern | Tìm `super()` |
| `odoo/models.py` | ensure_one | Tìm `def ensure_one` |
| `odoo/addons/web/__manifest__.py` | Assets bundles | `web.assets_backend` |
| `odoo/addons/calendar/views/` | Calendar view examples | Toàn bộ folder |

### ✅ Tiêu chí đạt
- [ ] Override method đúng cách với super()
- [ ] **Fix 5 pre-made bugs:**
  - [ ] Bug 1: `browse(id)` thay vì `browse([id])`
  - [ ] Bug 2: Missing `return super().create(vals)`
  - [ ] Bug 3: Modify `vals` sau khi super()
  - [ ] Bug 4: `ensure_one()` missing trên expected single record
  - [ ] Bug 5: Infinite loop do thiếu `sudo()` trong override
- [ ] Đọc được traceback và tìm root cause
- [ ] **Calendar view cho task.task:**
  - [ ] Tạo `<calendar>` view với `date_start="due_date"`
  - [ ] Add color field mapping
  - [ ] Add quick create
- [ ] **Frontend customization:**
  - [ ] Thêm `static/src/css/task_kanban.css`
  - [ ] Thêm `static/src/js/task_debug.js`
  - [ ] Register assets trong `__manifest__.py` → `web.assets_backend`
  - [ ] Add class `o_task_overdue` trong Kanban template
  - [ ] Verify bằng `?debug=assets` + console log từ JS

### 📦 Output artifacts
- Patch notes cho từng bug fix
- Calendar view XML
- Assets files + manifest block
- Checklist debug steps (traceback → root cause → fix)

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | _ | |
| Viết code (2h) | _ | |
| Shell/Debug (2h) | _ | |
| Tổng kết (1h) | _ | |
| **TỔNG NGÀY 17** | **_/10** | |

### ❓ Câu hỏi kiểm tra
1. **super()**: Khi nào gọi super() trước vs sau logic riêng?
2. **Traceback**: Dòng nào trong traceback cho biết root cause?
3. **browse()**: `browse(5)` vs `browse([5])` khác nhau thế nào?
4. **ensure_one()**: Khi nào cần, khi nào không?
5. **vals**: Tại sao modify vals SAU super() có thể gây bug?
6. **Calendar**: date_start vs date_stop trong calendar view?
7. **Assets**: Làm sao debug CSS/JS với `?debug=assets`?

### 🔗 Liên kết kiến thức
- **Prerequisites**: Day 3 (CRUD), Day 16 (Inheritance)
- **Builds on**: _inherit để override, super() pattern
- **Prepares for**: Day 18 (Controllers cũng cần error handling)
- **Module state sau Day 17**: Debug skills hoàn chỉnh, Calendar view, frontend assets, Phase 4 COMPLETE

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 18
> Phase 5 CONTROLLER bắt đầu:
> - HTTP Controllers tạo API
> - Error handling tương tự Day 17
> - auth patterns để kết nối với security từ Phase 3

---

# 📅 PHASE 5: CONTROLLER (Day 18-19)

### 🛠️ Debug checklist (Phase 5)
- [ ] Log request params + headers; validate auth context
- [ ] Test endpoints with curl/Postman for 200/403/404 paths
- [ ] Inspect response payloads and error stacks

---

## Day 18: HTTP Controllers

### 🎯 Mục đích chủ đạo
Tạo API endpoints trong Odoo.

### 📚 Đề mục cần học
- [ ] Controller class + @http.route decorator
- [ ] **type='jsonrpc'** vs **type='http'** - Response formats
- [ ] **auth options**: user, public, none, bearer
- [ ] Request/Response handling
- [ ] **CORS** - Access-Control-Allow-Origin
- [ ] **Error handling** - try/except trong controllers
- [ ] **csrf** - Khi nào cần csrf='False'

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/http.py` | Controller class | Tìm `class Controller` |
| `odoo/http.py` | route decorator | Tìm `def route` |
| `odoo/http.py` | Response class | Tìm `class Response` |

### ✅ Tiêu chí đạt
- [ ] Tạo được JSON controller trả về danh sách tasks
- [ ] **REST-like API:**
  - [ ] GET `/api/tasks` - List all tasks
  - [ ] GET `/api/tasks/<int:id>` - Get single task
  - [ ] Trả về JSON response
- [ ] Test với auth='user' và auth='public'
- [ ] **Error handling:**
  - [ ] 404: Task not found
  - [ ] 403: Access denied
  - [ ] 500: Internal error
- [ ] Xử lý được request parameters

### 📦 Output artifacts
- `controllers/main.py` với routes + error handling
- Sample curl/Postman requests + expected responses

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | _ | |
| Viết code (2h) | _ | |
| Shell/Debug (2h) | _ | |
| Tổng kết (1h) | _ | |
| **TỔNG NGÀY 18** | **_/10** | |

### ❓ Câu hỏi kiểm tra
1. **Route**: `type='jsonrpc'` vs `type='http'` khác nhau thế nào?
2. **Auth**: auth='none' dùng khi nào? Có rủi ro gì?
3. **bearer**: auth='bearer' hoạt động như thế nào với API key?
4. **CORS**: Làm sao enable CORS cho external app?
5. **Error**: Trả về 404 error trong JSON controller?
6. **Security**: Controller có chịu ACL và Record Rules không?

### 🔗 Liên kết kiến thức
- **Prerequisites**: Day 17 (Error handling), Phase 3 (Security)
- **Builds on**: auth patterns kết nối với groups từ Day 12
- **Prepares for**: Day 19 (Scheduled actions và external API)
- **Module state sau Day 18**: REST-like API cho task_management

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 19
> Day 19 Scheduled Actions + External API:
> - ir.cron cho background jobs
> - Gọi external API từ Odoo
> - Kết hợp với controller từ Day 18

---

## Day 19: Scheduled Actions + External API

### 🎯 Mục đích chủ đạo
Tạo background jobs tự động + Kết nối Odoo với service bên ngoài.

### 📚 Đề mục cần học
- [ ] **ir.cron model** - Scheduled actions
- [ ] **Cron method pattern** - @api.model method
- [ ] **Interval types** - minutes, hours, days, weeks, months
- [ ] requests library trong Odoo
- [ ] Xử lý exception khi gọi external API
- [ ] Timeout handling

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `odoo/addons/base/models/ir_cron.py` | Cron model | Toàn bộ file |
| `odoo/addons/iap/models/iap.py` | External API example | Toàn bộ file |

### ✅ Tiêu chí đạt
- [ ] **Tạo Scheduled Action "Auto-mark Overdue":**
  - [ ] Cron job chạy mỗi ngày lúc 00:00
  - [ ] Tìm tasks: `due_date < now AND state != 'done'`
  - [ ] Update field `is_overdue = True`
  - [ ] Log số lượng tasks updated
- [ ] Tạo được method gọi mock API (weather/notification)
- [ ] Xử lý được timeout/error
- [ ] Hiểu khi nào nên gọi sync vs async

### 📦 Output artifacts
- Cron method + cron record (data)
- External API call helper + error handling notes

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | _ | |
| Viết code (2h) | _ | |
| Shell/Debug (2h) | _ | |
| Tổng kết (1h) | _ | |
| **TỔNG NGÀY 19** | **_/10** | |

### ❓ Câu hỏi kiểm tra
1. **ir.cron**: Cron method cần decorator gì? Tại sao @api.model?
2. **Interval**: Cài đặt cron chạy mỗi 30 phút như thế nào?
3. **Exception**: Nếu cron job fail, Odoo xử lý thế nào?
4. **External API**: requests.get() block thread. Có vấn đề không?
5. **Timeout**: Làm sao set timeout cho external API call?
6. **Security**: Cron job chạy với user nào? Có bypass security không?

### 🔗 Liên kết kiến thức
- **Prerequisites**: Day 18 (Controllers, error handling)
- **Builds on**: HTTP concepts, background processing
- **Prepares for**: Day 20 (Integration of all features)
- **Module state sau Day 19**: Auto-mark overdue cron job, external API pattern

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 20
> Day 20-21 là Consolidation:
> - Review toàn bộ task_management module
> - Integration testing
> - Production checklist

---

# 📅 PHASE 6: CONSOLIDATION (Day 20-21)

### 🛠️ Debug checklist (Phase 6)
- [ ] Run end-to-end scenarios and capture regressions
- [ ] Verify performance with `--log-level=debug_sql`
- [ ] Use `?debug=assets` to trace frontend assets if UI issues appear

---

## Day 20: Integration Testing + Production Checklist

### 🎯 Mục đích chủ đạo
Test toàn bộ task_management module end-to-end, chuẩn bị production-ready checklist.

### 📚 Đề mục cần học
- [ ] **Integration Testing** - End-to-end workflow tests
- [ ] **Data integrity validation** - Check constraints work together
- [ ] **Performance baseline** - Measure query counts
- [ ] **Production checklist:**
  - [ ] ir.model.access.csv complete
  - [ ] Security groups defined
  - [ ] Record rules tested
  - [ ] Demo data working
- [ ] **Code review patterns** - Self-review checklist

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| `custom_addons/task_management/` | Toàn bộ module | Review |
| `odoo/tests/common.py` | Test patterns | TransactionCase |

### ✅ Tiêu chí đạt
- [ ] **Full Integration Test:**
  - [ ] Create project → Add tasks → Assign tags
  - [ ] Test wizard bulk update
  - [ ] Test onchange auto-fill
  - [ ] Verify computed fields update
  - [ ] Test security (manager vs member)
  - [ ] Generate PDF report
  - [ ] Trigger cron job manually
  - [ ] Include smoke/integration checks từ Day 9
- [ ] **Production Checklist:** All items checked
- [ ] **Self-assessment:** Đủ để nhận task công ty?

### 📦 Output artifacts
- Integration checklist + defect log
- Production checklist snapshot

### ❓ Câu hỏi kiểm tra
1. **Integration**: Làm sao test end-to-end mà không bỏ sót feature?
2. **Checklist**: Item nào trong production checklist quan trọng nhất?
3. **Performance**: Làm sao đo số queries trong một operation?
4. **Demo data**: Tại sao demo data quan trọng?
5. **Version**: __manifest__.py version format chuẩn?
6. **Self-review**: Code review pattern quan trọng nhất là gì?

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Integration Test | _ | |
| Production Checklist | _ | |
| Self-Assessment | _ | |
| **TỔNG NGÀY 20** | **_/10** | |

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

### ⚠️ Lưu ý cho Day 21
> Day 21 compares Odoo versions và final assessment

---

## Day 21: Version Differences + Final Assessment

### 🎯 Mục đích chủ đạo
Hiểu điểm khác biệt Odoo 14 vs 17/19 + **Final assessment** để xác định job readiness.

### 📚 Đề mục cần học
- [ ] **API changes 14 → 17 → 19:**
  - [ ] `api.multi` removed (17+)
  - [ ] QWeb changes in newer versions
  - [ ] assets bundle changes (17+)
- [ ] **New features 17/19:**
  - [ ] Spreadsheet integration
  - [ ] New ORM features
- [ ] **Migration patterns** - What transfers directly
- [ ] **Job readiness self-assessment**

### 📂 Source code cần đọc
| File | Focus | Dòng gợi ý |
|------|-------|------------|
| Odoo release notes | 14 → 17 → 19 changes | Online |
| Context7 | Version-specific patterns | Query |

### ✅ Tiêu chí đạt
- [ ] List được 5+ API differences 14 vs 17/19
- [ ] **Final Practical Test:**
  - [ ] Viết 1 model mới từ scratch
  - [ ] Thêm computed field với inverse
  - [ ] Thêm security group + record rule
  - [ ] Create view với xpath inheritance
  - [ ] Debug 1 pre-made bug
- [ ] **Self-Assessment:** Rate ORM, Security, Debug (1-10)

### 📦 Output artifacts
- Summary differences 14 vs 17/19
- Final practical test notes + scoring

### ❓ Câu hỏi kiểm tra
1. **Version**: `@api.multi` bị loại bỏ từ version nào?
2. **Migration**: Code Odoo 14 chạy không thay đổi trên 17?
3. **QWeb**: QWeb templates thay đổi gì giữa versions?
4. **Assets**: assets bundle quản lý khác nhau thế nào?
5. **Job**: Task nào dễ nhất để bắt đầu công việc thực tế?
6. **Growth**: Bước tiếp theo từ Junior → Mid-level?

### 📝 Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Version Research | _ | |
| Final Practical Test | _ | |
| Self-Assessment | _ | |
| **TỔNG NGÀY 21** | **_/10** | |

### 📌 Ghi chú AI
> _(AI sẽ điền sau khi hoàn thành)_

---

# 🎓 KẾT THÚC KHÓA HỌC

## Tổng kết điểm
| Phase | Điểm |
|-------|------|
| Phase 1: ORM Foundation | _/50 |
| Phase 2: Business Logic | _/50 |
| Phase 3: Security | _/40 |
| Phase 4: Module Reading | _/30 |
| Phase 5: Controller | _/20 |
| Phase 6: Consolidation | _/20 |
| **TỔNG** | **_/210** |

## Đánh giá cuối khóa
> _(AI điền sau Day 21)_

## Task công ty có thể nhận
- [ ] Tạo module mới
- [ ] Sửa bug ORM
- [ ] Sửa bug security
- [ ] Chỉnh sửa views
- [ ] Thêm field mới
- [ ] Override method

## Task cần thêm thời gian
> _(AI điền)_
