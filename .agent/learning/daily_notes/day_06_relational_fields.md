# 📋 DAY 6 - Relational Fields (M2O, O2M, M2M)

> **Generated**: 2026-01-19 | **Workflow**: Planner v2 (with Module Spec reference)

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 6 of 21 |
| **Chủ đề** | Relational Fields - Many2one, One2many, Many2many + Command Patterns |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Day 3 (CRUD), Day 5 (Fields System, Binary) |
| **Module Spec Reference** | `.agent/learning/module_spec.md` |

---

## 📦 MODULE STATE (From Module Spec & Current Code)

### 🎯 Day 6 Targets (From Module Spec)
```
| Day | Feature Added | Model(s) Affected |
| 6   | Relationships | task.task, task.project, task.tag |

Cụ thể cần thêm:
- task.task: project_id (M2O), assigned_user_id (M2O), tag_ids (M2M)
- task.project: task_ids (O2M), manager_id (M2O)
- NEW: task.tag model (name, color)
```

### 📍 ACTUAL Current State (Before Day 6)

**File: `models/task.py` (93 lines)**
```python
# ĐÃ CÓ:
name = fields.Char(required=True)
description = fields.Text(required=True)
state = fields.Selection([draft/in_progress/done], required=True, group_expand="_expand_states")
priority = fields.Selection([low/medium/high])
due_date = fields.Datetime()
hours_estimated = fields.Float(digits=(6,2))
hours_spent = fields.Float(digits=(6,2))
is_overdue = fields.Boolean(compute="_compute_is_overdue")  # ⚠️ Day 7 content done early
color = fields.Integer()

# Methods đã có:
_expand_states(), _compute_is_overdue(), create(), write()
action_mark_done(), action_delete(), action_admin_only()

# ❌ CHƯA CÓ (Day 6 targets):
project_id = fields.Many2one(...)
assigned_user_id = fields.Many2one(...)
tag_ids = fields.Many2many(...)
```

**File: `models/project.py` (11 lines)**
```python
# ĐÃ CÓ:
name = fields.Char(required=True, index=True)
description = fields.Text()
image = fields.Image(max_width=1920, max_height=1080)

# ❌ CHƯA CÓ (Day 6 targets):
task_ids = fields.One2many(...)
manager_id = fields.Many2one(...)
```

**File: `models/tag.py` - CHƯA TỒN TẠI**
```python
# ❌ CẦN TẠO MỚI
```

**Views đã có:**
- Tree: Advanced với decorations, is_overdue highlighting
- Form: 2 columns, notebook, float_time widgets
- Kanban: Color picker, dropdown menu, priority/state widgets
- Search: Filters, group by

---

### ✅ Sau Day 6 (Expected Output)

**task.py sẽ có thêm:**
```python
project_id = fields.Many2one('task.project', ondelete='cascade', index=True)
assigned_user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
tag_ids = fields.Many2many('task.tag')
```

**project.py sẽ có thêm:**
```python
task_ids = fields.One2many('task.task', 'project_id')
manager_id = fields.Many2one('res.users', string='Manager')
```

**NEW: models/tag.py:**
```python
class TaskTag(models.Model):
    _name = 'task.tag'
    name = fields.Char(required=True)
    color = fields.Integer()
```

**Views updates:**
- Task Form: thêm project_id, assigned_user_id, tag_ids
- Task Tree: thêm project_id column
- Project Form: thêm tab "Tasks" với O2M inline
- Task Kanban: hiển thị tags với t-foreach

---

## 🎯 LEARNING OBJECTIVES

By end of day, learner will be able to:
- [ ] Phân biệt được 3 loại relational fields (M2O, O2M, M2M) và khi nào dùng
- [ ] Giải thích các parameters quan trọng: comodel_name, inverse_name, ondelete, domain, check_company
- [ ] Implement production-ready relational fields theo Module Spec
- [ ] Sử dụng Command patterns (create, link, set, clear, unlink) để write relational fields
- [ ] Truy cập related data qua dot notation và hiểu lazy loading
- [ ] Update views để hiển thị relational fields correctly
- [ ] Debug relational field errors (wrong inverse_name, orphan records, ACL missing)

---

## 📚 PHẦN 1: NỘI DUNG BÀI HỌC (10-12 Concepts)

### 1.1 Source Code Files cần đọc

| File | Focus Area | Line Range | Purpose |
|------|------------|------------|---------|
| `odoo/fields.py` | `class Many2one` | ~L2020-2160 | Hiểu M2O implementation, parameters |
| `odoo/fields.py` | `class One2many` | ~L2483-2580 | Hiểu O2M virtual field |
| `odoo/fields.py` | `class Many2many` | ~L2580-2750 | Hiểu M2M intermediate table |
| `odoo/fields.py` | `class Command` | ~L20-120 | Command patterns |
| `odoo/addons/sale/models/sale_order.py` | Real M2O/O2M usage | Toàn bộ | Production patterns |

---

### 1.2 Concepts chi tiết

#### 🟢 Concept 1: Many2one Field (M2O) - FK Relationship

**Core explanation (Context7):**
Many2one tạo FK relationship từ current model đến target model. Giá trị là recordset size 0 (empty) hoặc 1 (single record). Trong DB, Odoo tạo INTEGER column chứa ID của record target.

**Syntax:**
```python
# Basic
project_id = fields.Many2one('task.project', string='Project')

# Production pattern (theo Module Spec)
project_id = fields.Many2one(
    'task.project',
    string='Project',
    ondelete='cascade',  # Delete task khi project bị xóa
    index=True,          # Performance: tạo DB index
)

# Link đến built-in model với default
assigned_user_id = fields.Many2one(
    'res.users',
    string='Assigned To',
    default=lambda self: self.env.user,  # Auto-assign current user
)
```

**Parameters quan trọng (Context7):**
| Parameter | Description | Values/Example |
|-----------|-------------|----------------|
| `comodel_name` | Target model (REQUIRED) | `'task.project'` |
| `ondelete` | Action khi target deleted | `'cascade'`, `'set null'`, `'restrict'` |
| `index` | Create DB index | `True` (recommended cho FK) |
| `domain` | Filter available options | `[('active', '=', True)]` |
| `delegate` | Access target fields directly | `True` (_inherits pattern) |
| `check_company` | Multi-company validation | `True` |

**ondelete options chi tiết:**
- `'cascade'` (DEFAULT): Task xóa khi Project xóa → Strong dependency (e.g., Order Lines)
- `'set null'`: Task.project_id = NULL → Optional relationship (e.g., Assigned User)
- `'restrict'`: Không cho xóa Project nếu có Tasks → Data protection (e.g., Account với Transactions)

**Comparison vs SQLAlchemy:**
```python
# SQLAlchemy
project_id = Column(Integer, ForeignKey('project.id', ondelete='CASCADE'))

# Odoo
project_id = fields.Many2one('task.project', ondelete='cascade')
```

**Gotcha:**
- Quên `ondelete='cascade'` → orphan records khi delete parent
- Quên `index=True` → slow queries khi JOIN

---

#### 🟢 Concept 2: One2many Field (O2M) - Virtual Reverse Relationship

**Core explanation (Context7):**
One2many là "reverse" của Many2one. KHÔNG tạo column trong DB (virtual field). Giá trị là recordset của TẤT CẢ records từ comodel có inverse_name = current record.

**Syntax:**
```python
# On task.project model (theo Module Spec)
task_ids = fields.One2many(
    'task.task',         # comodel_name (REQUIRED)
    'project_id',        # inverse_name (REQUIRED) - M2O field name trên task.task
    string='Tasks',
)
```

**Parameters (Context7):**
| Parameter | Description |
|-----------|-------------|
| `comodel_name` | Model chứa M2O field (REQUIRED) |
| `inverse_name` | Tên M2O field trên comodel (REQUIRED) |
| `domain` | Filter records (optional) |
| `context` | Context dict cho client-side (set defaults) |
| `bypass_search_access` | Bypass ACL (default: False) |

**Relationship Pattern:**
```
task.project               task.task
┌──────────────┐          ┌──────────────────┐
│ id           │◄─────────│ project_id (M2O) │  ← Real column in DB
│ name         │          │ name             │
│ task_ids     │─────────▶│                  │  ← Virtual, computes from M2O
└──────────────┘          └──────────────────┘
```

**Production pattern với context:**
```python
task_ids = fields.One2many(
    'task.task',
    'project_id',
    context={'default_priority': 'high'},  # Auto-set priority khi create từ O2M
)
```

**Gotcha:**
- `inverse_name` PHẢI chính xác = tên M2O field trên comodel
- Sai inverse_name = O2M luôn trả về EMPTY recordset, không báo lỗi!

---

#### 🟢 Concept 3: Many2many Field (M2M) - N:N Relationship

**Core explanation (Context7):**
Many2many tạo N:N relationship qua intermediate table (auto-generated). Giá trị là recordset không giới hạn size.

**Syntax:**
```python
# Basic - Odoo auto-creates relation table
tag_ids = fields.Many2many('task.tag', string='Tags')

# Explicit relation table (khi cần control hoặc 2 M2M giữa same models)
tag_ids = fields.Many2many(
    'task.tag',
    'task_task_tag_rel',    # relation - table name
    'task_id',               # column1 - FK to current model
    'tag_id',                # column2 - FK to comodel
    string='Tags',
)
```

**Auto-generated table:**
```sql
-- Odoo tạo table với naming convention: {model1}_{model2}_rel
CREATE TABLE task_task_task_tag_rel (
    task_task_id INTEGER REFERENCES task_task(id),
    task_tag_id INTEGER REFERENCES task_tag(id)
);
```

**Khi nào dùng M2M vs model trung gian?**
| Use Case | Choice | Example |
|----------|--------|---------|
| Simple N:N, no extra data | M2M | Task ↔ Tags |
| Need extra attributes | Model trung gian | Order ↔ Product + qty, price |
| Need ordering/sequence | Model trung gian | Playlist ↔ Songs + position |

**Gotcha:**
- 2 M2M fields giữa same 2 models PHẢI có explicit `relation` name khác nhau
- Không có `ondelete` cho M2M (xóa record = tự động xóa rows trong relation table)

---

#### 🟢 Concept 4: Command Patterns (QUAN TRỌNG!)

**Core explanation (Context7):**
Command class provides static methods để manipulate O2M và M2M fields khi write. RPC dùng tuples, Python nên dùng Command methods.

**All Commands:**
```python
from odoo.fields import Command

# CREATE (0): Tạo related record mới inline
task.write({'tag_ids': [Command.create({'name': 'Urgent', 'color': 1})]})

# UPDATE (1): Update existing related record
task.write({'tag_ids': [Command.update(tag_id, {'color': 2})]})

# DELETE (2): Delete related record từ DB (chỉ O2M)
project.write({'task_ids': [Command.delete(task_id)]})

# UNLINK (3): Remove relation, không xóa record
task.write({'tag_ids': [Command.unlink(tag_id)]})

# LINK (4): Link existing record
task.write({'tag_ids': [Command.link(existing_tag_id)]})

# CLEAR (5): Xóa tất cả relations
task.write({'tag_ids': [Command.clear()]})

# SET (6): Replace tất cả bằng list IDs
task.write({'tag_ids': [Command.set([1, 2, 3])]})
```

**Tuple format (RPC/XML):**
| Command | Tuple | Python |
|---------|-------|--------|
| CREATE | `(0, 0, {values})` | `Command.create(values)` |
| UPDATE | `(1, id, {values})` | `Command.update(id, values)` |
| DELETE | `(2, id, 0)` | `Command.delete(id)` |
| UNLINK | `(3, id, 0)` | `Command.unlink(id)` |
| LINK | `(4, id, 0)` | `Command.link(id)` |
| CLEAR | `(5, 0, 0)` | `Command.clear()` |
| SET | `(6, 0, [ids])` | `Command.set(ids)` |

**Gotcha O2M delete vs unlink:**
- `Command.delete()` = XÓA record khỏi DB
- `Command.unlink()` = Set inverse field = False (record vẫn tồn tại)

---

#### 🟢 Concept 5: Dot Notation Access & Lazy Loading

**Core explanation:**
Truy cập related data qua dot notation. Odoo auto-load related records (lazy loading = query khi cần).

```python
task = env['task.task'].browse(1)

# Dot notation - trigger lazy load
print(task.project_id.name)       # 1 query for project
print(task.project_id.task_ids)   # 1 query for all project's tasks

# Chained access
print(task.assigned_user_id.partner_id.email)  # Multiple queries
```

**Performance problem - N+1 queries:**
```python
# BAD - N+1 queries (1 for tasks + N for projects)
tasks = env['task.task'].search([])
for task in tasks:
    print(task.project_id.name)  # Query mỗi iteration!

# GOOD - 2 queries max (prefetch)
tasks = env['task.task'].search([])
projects = tasks.mapped('project_id')  # 1 query for all unique projects
for task in tasks:
    print(task.project_id.name)  # Already in cache
```

---

#### 🟢 Concept 6: View Integration - Display Relational Fields

**Form view - M2O dropdown:**
```xml
<field name="project_id"/>
<field name="assigned_user_id"/>
<field name="tag_ids" widget="many2many_tags"/>  <!-- Tags widget -->
```

**Form view - O2M inline list (trong Project form):**
```xml
<notebook>
    <page string="Tasks" name="tasks">
        <field name="task_ids">
            <tree editable="bottom">  <!-- Inline edit -->
                <field name="name"/>
                <field name="state"/>
                <field name="priority"/>
            </tree>
        </field>
    </page>
</notebook>
```

**Kanban - Display tags với t-foreach:**
```xml
<field name="tag_ids"/>  <!-- Declare field -->

<div class="o_kanban_tags">
    <t t-foreach="record.tag_ids.raw_value" t-as="tag">
        <span t-attf-class="badge badge-pill" t-att-style="'background-color: #...'">
            <!-- Need to lookup tag name separately or use widget -->
        </span>
    </t>
</div>

<!-- Better: Use widget -->
<field name="tag_ids" widget="many2many_tags"/>
```

---

#### 🟢 Concept 7: ACL cho Model mới (task.tag)

**QUAN TRỌNG:** Model mới PHẢI có ACL, không thì users không thể access!

**File: security/ir.model.access.csv**
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_task_tag_user,task.tag.user,model_task_tag,base.group_user,1,1,1,1
```

**Gotcha:**
- Quên ACL = User thấy "Access Denied" khi load form với M2O/M2M đến model đó
- Debug: Check log cho "AccessError"

---

## 📝 PHẦN 2: BÀI TẬP THỰC HÀNH (5+ Exercises)

### Exercise 1: Tạo model task.tag

**Requirements:**
1. Tạo file `models/tag.py`
2. Define model `task.tag` với:
   - `name` (Char, required)
   - `color` (Integer, default=0)
3. Update `models/__init__.py`
4. Tạo `security/ir.model.access.csv` với ACL cho task.tag
5. Update `__manifest__.py` với security file
6. Tạo basic views (tree, form) trong `views/tag_views.xml`
7. Thêm menu item

**Expected Result:**
- Có thể CRUD tags từ menu
- Mỗi tag có color index

**Critical UX Checklist:**
- [ ] Menu "Tags" xuất hiện
- [ ] Form create/edit works
- [ ] Tree list displays correctly

**Gotcha cần chú ý:**
- Quên `from . import tag` trong `__init__.py` → Model không load
- Quên ACL → Access Denied

---

### Exercise 2: Thêm Many2one fields vào task.task

**Requirements:**
1. Thêm vào `task.py`:
   ```python
   project_id = fields.Many2one('task.project', string='Project', ondelete='cascade', index=True)
   assigned_user_id = fields.Many2one('res.users', string='Assigned To', default=lambda self: self.env.user)
   ```
2. Update Task Form view: hiển thị 2 fields mới (in header group)
3. Update Task Tree view: thêm `project_id` column
4. Update Search view: thêm group by `project_id`

**Expected Result:**
- Task có dropdown chọn Project
- Task auto-assign cho current user
- Tree shows project column
- Can group tasks by project

**Shell test ondelete:**
```python
# Test: Delete project → Tasks auto-deleted
project = env['task.project'].create({'name': 'Test Project'})
task = env['task.task'].create({'name': 'Test Task', 'project_id': project.id, 'description': 'Test'})
print(f"Task ID: {task.id}")
project.unlink()  # Delete project
result = env['task.task'].search([('id', '=', task.id)])
print(f"Task after delete: {result}")  # Should be empty []
```

---

### Exercise 3: Thêm One2many vào task.project

**Requirements:**
1. Thêm vào `project.py`:
   ```python
   task_ids = fields.One2many('task.task', 'project_id', string='Tasks')
   manager_id = fields.Many2one('res.users', string='Project Manager')
   ```
2. Update Project Form view: thêm tab "Tasks" với inline editable tree
3. Thêm manager field trong header

**Expected Result:**
- Trong Project form, thấy tab "Tasks" với danh sách tasks
- Có thể tạo/edit task trực tiếp từ Project form
- Tasks tự động có project_id set

**Critical UX Checklist:**
- [ ] Tab "Tasks" visible
- [ ] Click "Add a line" creates new inline row
- [ ] Save creates task with correct project_id

---

### Exercise 4: Thêm Many2many và update Kanban

**Requirements:**
1. Thêm vào `task.py`:
   ```python
   tag_ids = fields.Many2many('task.tag', string='Tags')
   ```
2. Update Task Form view: tags với widget="many2many_tags"
3. Update Task Kanban view: 
   - Declare `<field name="tag_ids"/>`
   - Hiển thị tags (có thể dùng widget hoặc t-foreach)

**Expected Result:**
- Có thể assign multiple tags cho task
- Tags hiển thị trong Kanban cards

---

### Exercise 5: Master Command Patterns (Shell Practice)

**Requirements:** Thực hành TẤT CẢ Commands trong shell:

```python
from odoo.fields import Command

# Setup
task = env['task.task'].browse(1)  # hoặc search 1 task
tag1 = env['task.tag'].create({'name': 'Bug', 'color': 1})
tag2 = env['task.tag'].create({'name': 'Feature', 'color': 2})

# Exercise A: Link tag1 vào task
# YOUR CODE HERE

# Exercise B: Create new tag inline và link
# YOUR CODE HERE

# Exercise C: Set tags = [tag1, tag2] (replace all)
# YOUR CODE HERE

# Exercise D: Unlink tag1 (remove relation only)
# YOUR CODE HERE

# Exercise E: Clear all tags
# YOUR CODE HERE

# Exercise F: Create multiple với mix commands
# YOUR CODE HERE
```

---

## ❓ PHẦN 3: CÂU HỎI KIỂM TRA (10 Questions)

### Level: Easy (3)
1. Many2one tạo column trong DB không? One2many thì sao? Tại sao?
2. Viết field M2O link task.task đến res.users với default là current user.
3. `ondelete='cascade'` nghĩa là gì? Cho 2 real-world examples.

### Level: Medium (4)
4. **Debug**: O2M `task_ids` luôn trả về empty recordset dù có tasks trong DB. Liệt kê 3 nguyên nhân có thể và cách debug.
5. **Command**: Viết code thêm 2 tags mới, link 1 tag có sẵn, xóa 1 tag cũ trong MỘT lần write.
6. Khi nào nên dùng M2M vs tạo model trung gian? Cho example cho mỗi case.
7. Tại sao model mới (task.tag) cần ACL? Điều gì xảy ra nếu quên?

### Level: Hard (3)
8. **Performance**: Giải thích N+1 query problem với relational fields. Viết code BAD và GOOD.
9. **Design**: Thiết kế relationships cho: 
   - Employee works in Department
   - Department has Manager (Employee) 
   - Employee has Skills (N:N với extra "level" attribute)
10. **Production**: `check_company=True` làm gì? Khi nào cần? Điều gì xảy ra nếu user truy cập record từ company khác?

---

## 🎓 PHẦN 4: ADVANCED TOPICS

### 4.1 delegate Parameter (_inherits pattern)
```python
class Task(models.Model):
    partner_id = fields.Many2one('res.partner', delegate=True, required=True)
    # Giờ có thể access task.name, task.email... trực tiếp từ partner
```

### 4.2 domain và context trên relational fields
```python
# Filter available options (only active projects)
project_id = fields.Many2one(
    'task.project',
    domain=[('active', '=', True)],
)

# Filter cho specific user (dynamic)
project_id = fields.Many2one(
    'task.project',
    domain="[('manager_id', '=', uid)]",  # String = evaluated at runtime
)

# Pass context cho defaults
task_ids = fields.One2many(
    'task.task',
    'project_id',
    context={'default_priority': 'high', 'default_state': 'draft'},
)
```

### 4.3 bypass_search_access
```python
# Cho phép O2M load records mà user không có read access
task_ids = fields.One2many(
    'task.task',
    'project_id',
    bypass_search_access=True,  # Cẩn thận với security!
)
```

---

## ⚠️ PHẦN 5: GOTCHAS & COMMON MISTAKES

1. **Orphan records**: Quên `ondelete='cascade'` → tasks không bị xóa khi delete project
2. **Wrong inverse_name**: O2M luôn empty vì inverse_name không match M2O field name
3. **M2M table conflict**: 2 M2M fields giữa same models PHẢI có explicit `relation` name
4. **Command confusion**: `delete()` xóa record từ DB, `unlink()` chỉ remove relation
5. **N+1 queries**: Dot notation trong loops = slow, dùng `mapped()` hoặc prefetch
6. **ACL missing**: Model mới cần ACL trong ir.model.access.csv, không thì Access Denied
7. **String domain**: Khi dùng string domain `"[(...)]"`, variables như `uid` được evaluate runtime

---

## 📊 PHẦN 5: Evaluation
| Tiêu chí | Weight | Điểm (/10) | Ghi chú |
|----------|--------|------------|---------|
| Hiểu M2O/O2M/M2M differences | 20% | 10/10 | Nắm chắc bản chất DB & Virtual fields |
| Implement relational fields | 20% | 9/10 | Code tốt, trừ 1 điểm syntax error (typo) |
| Command patterns thành thạo | 15% | 8/10 | Hiểu concept, cần practice thêm real-world |
| Update views correctly | 15% | 9/10 | Logic đúng, trừ điểm lỗi cú pháp attrs |
| Debug relational issues | 15% | 9/10 | Tự fix được circular dependency issue |
| Trả lời câu hỏi (8+ correct) | 15% | 9/10 | Trả lời xuất sắc câu Hard level |
| **TỔNG** | **100%** | **9.0** | **XUẤT SẮC** 🌟 |

---

## 📌 KẾT QUẢ VÀ GHI CHÚ AI

### Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | 10 | M2O, O2M, M2M class - hiểu sâu tất cả attributes |
| Viết code (2h) | 9 | Exercises hoàn thành, 1 lỗi syntax nhỏ (comodel_name) |
| Shell/Debug (2h) | 9 | Fix circular M2M relation_table issue, Command patterns |
| Tổng kết (1h) | 9 | 10/10 câu hỏi + Bonus Deadlock/Recursion simulation |
| **TỔNG NGÀY 6** | **9.0/10** | **XUẤT SẮC** 🌟 |

### 📌 Ghi chú AI
> **Key takeaways Day 6:**
> - M2O tạo FK column (int4), O2M là virtual (không column), M2M tạo relation table
> - M2M cần explicit `relation`, `column1`, `column2` khi khai báo 2 phía để tránh circular reference
> - Command patterns: `(0,0,{})` create, `(4,id,0)` link, `(5,0,0)` clear, `(6,0,[ids])` set
> - Transaction lifecycle: 1 Request = 1 Transaction (lock giữ đến khi return)
> - **Bonus**: Deadlock = vòng tròn khóa lẫn nhau, Odoo auto-retry 5 lần
> - **Bonus**: RecursionError = computed field depends trên chính nó

### ⚠️ Lưu ý cho Day 7
> Day 7 sẽ tạo computed fields dựa trên relational fields đã học:
> - `task_count = len(project.task_ids)` ← dùng O2M từ Day 6
> - `hours_remaining = hours_estimated - hours_spent` ← đã có fields
> - Note: `is_overdue` đã implement, Day 7 sẽ review
> - `@api.depends('project_id.xxx')` ← dùng M2O từ Day 6 cho cross-model dependencies
