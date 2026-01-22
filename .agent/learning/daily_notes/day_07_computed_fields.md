# 📋 DAY 7 - Computed Fields + @api.depends

> **Generated**: 2026-01-20 | **Workflow**: Planner v2 (with Module Spec reference)

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 7 of 21 |
| **Chủ đề** | Computed Fields - @api.depends, store, inverse, search |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Day 5 (Fields System), Day 6 (Relational Fields) |
| **Module Spec Reference** | `.agent/learning/module_spec.md` |

---

## 📦 MODULE STATE (From Module Spec & Current Code)

### 🎯 Day 7 Targets (From Module Spec)
```
| Day | Feature Added | Model(s) Affected |
| 7   | Computed fields | task.task, task.project |

Cụ thể cần thêm:
- task.project: task_count (computed Integer)
- task.task: hours_remaining (computed Float) 
- task.task: progress (computed Float)
- task.task: is_overdue (computed Boolean) ← ⚠️ ĐÃ CÓ (ahead of schedule)
```

### 📍 ACTUAL Current State (Before Day 7)

**File: `models/task.py` (~131 lines)**
```python
# ĐÃ CÓ COMPUTED FIELDS (ahead of schedule):
is_overdue = fields.Boolean(compute="_compute_is_overdue")  # ✅ Day 5
has_urgent_tags = fields.Boolean(compute="_compute_has_urgent_tag")  # ✅ Day 6

# @api.depends đã dùng:
@api.depends("due_date", "state")  # ✅
@api.depends("tag_ids", "tag_ids.name")  # ✅ Cross-model dependency

# ❌ CHƯA CÓ (Day 7 targets):
hours_remaining = fields.Float(compute="_compute_hours")
progress = fields.Float(compute="_compute_progress")
```

**File: `models/project.py` (~21 lines)**
```python
# ĐÃ CÓ:
task_ids = fields.One2many('task.task', 'project_id')  # O2M from Day 6

# ❌ CHƯA CÓ (Day 7 targets):
task_count = fields.Integer(compute="_compute_task_count")
```

---

### ✅ Sau Day 7 (Expected Output)

**task.py sẽ có thêm:**
```python
hours_remaining = fields.Float(
    string='Hours Remaining',
    compute='_compute_hours',
    store=True,  # Searchable & Sortable
)

progress = fields.Float(
    string='Progress (%)',
    compute='_compute_progress',
    inverse='_inverse_progress',  # Editable!
)

@api.depends('hours_estimated', 'hours_spent')
def _compute_hours(self):
    for record in self:
        record.hours_remaining = record.hours_estimated - record.hours_spent

@api.depends('hours_estimated', 'hours_spent')
def _compute_progress(self):
    for record in self:
        if record.hours_estimated:
            record.progress = (record.hours_spent / record.hours_estimated) * 100
        else:
            record.progress = 0.0

def _inverse_progress(self):
    for record in self:
        if record.hours_estimated:
            record.hours_spent = (record.progress / 100) * record.hours_estimated
```

**project.py sẽ có thêm:**
```python
task_count = fields.Integer(
    string='Task Count',
    compute='_compute_task_count',
    store=True,
)

@api.depends('task_ids')
def _compute_task_count(self):
    for project in self:
        project.task_count = len(project.task_ids)
```

---

## 🎯 LEARNING OBJECTIVES

By end of day, learner will be able to:
- [ ] Hiểu bản chất computed fields: tự động tính toán khi dependencies thay đổi
- [ ] Sử dụng `@api.depends` decorator với single và multiple dependencies
- [ ] Phân biệt `store=True` vs `store=False` và impact lên search/sort
- [ ] Implement `inverse` method để make computed field editable
- [ ] Implement `search` method để enable domain filter trên non-stored computed
- [ ] Hiểu cross-model dependencies: `@api.depends('project_id.manager_id')`
- [ ] Debug computed field issues: không recompute, circular dependencies
- [ ] Performance considerations: cascade recompute costs

---

## 📚 PHẦN 1: NỘI DUNG BÀI HỌC (12 Concepts)

### 1.1 Source Code Files cần đọc

| File | Focus Area | Line Range | Purpose |
|------|------------|------------|---------|
| `odoo/api.py` | `def depends()` | L185-207 | Hiểu decorator implementation |
| `odoo/api.py` | `def depends_context()` | L210-233 | Context dependencies |
| `odoo/fields.py` | `class Field` | L116-280 | Field attributes: compute, inverse, search, store |
| `odoo/fields.py` | `_setup_regular_full()` | L432-463 | How depends are resolved |
| `odoo/fields.py` | `resolve_depends()` | L639-674 | Dependency resolution logic |

---

### 1.2 Concepts chi tiết

#### 🟢 Concept 1: Computed Field Basics

**Core explanation:**
Computed field là field có giá trị được TÍNH TOÁN từ các fields khác, không lưu trực tiếp từ user input. Khi dependency fields thay đổi, Odoo tự động gọi lại compute method.

**Syntax:**
```python
from odoo import models, fields, api

class Task(models.Model):
    _name = 'task.task'
    
    hours_estimated = fields.Float()
    hours_spent = fields.Float()
    
    # Computed field - TỰ ĐỘNG tính toán
    hours_remaining = fields.Float(compute='_compute_hours')
    
    def _compute_hours(self):
        for record in self:
            record.hours_remaining = record.hours_estimated - record.hours_spent
```

**Key points:**
1. `compute='_compute_hours'` - chỉ định method name (string)
2. `_compute_hours(self)` - method PHẢI iterate qua `self` (recordset)
3. Mỗi record PHẢI được assign giá trị (không thể skip)

**Comparison vs SQLAlchemy:**
```python
# SQLAlchemy: @hybrid_property + expression
class Task(Base):
    @hybrid_property
    def hours_remaining(self):
        return self.hours_estimated - self.hours_spent
    
    @hours_remaining.expression
    def hours_remaining(cls):
        return cls.hours_estimated - cls.hours_spent

# Odoo: fields.Float(compute=...) + store=True
hours_remaining = fields.Float(compute='_compute_hours', store=True)
```

---

#### 🟢 Concept 2: @api.depends Decorator

**Core explanation (From Odoo Source):**
`@api.depends` specifies which fields trigger recomputation. Khi BẤT KỲ field nào trong depends thay đổi, compute method sẽ được gọi lại.

**Source code (odoo/api.py L185-207):**
```python
def depends(*args):
    """ Return a decorator that specifies the field dependencies of a "compute"
        method (for new-style function fields). Each argument must be a string
        that consists in a dot-separated sequence of field names::

            pname = fields.Char(compute='_compute_pname')

            @api.depends('partner_id.name', 'partner_id.is_company')
            def _compute_pname(self):
                for record in self:
                    if record.partner_id.is_company:
                        record.pname = (record.partner_id.name or "").upper()
                    else:
                        record.pname = record.partner_id.name

        One may also pass a single function as argument. In that case, the
        dependencies are given by calling the function with the field's model.
    """
    if args and callable(args[0]):
        args = args[0]
    elif any('id' in arg.split('.') for arg in args):
        raise NotImplementedError("Compute method cannot depend on field 'id'.")
    return attrsetter('_depends', args)
```

**Patterns:**
```python
# Single dependency
@api.depends('hours_spent')
def _compute_something(self):
    ...

# Multiple dependencies (OR logic - khi BẤT KỲ field nào thay đổi)
@api.depends('hours_estimated', 'hours_spent')
def _compute_hours(self):
    ...

# Cross-model dependency (dot notation)
@api.depends('project_id.manager_id')
def _compute_manager_name(self):
    for task in self:
        task.manager_name = task.project_id.manager_id.name

# Deep traversal
@api.depends('project_id.task_ids.state')
def _compute_project_done_count(self):
    ...
```

**⚠️ Critical Rules:**
1. CANNOT depend on `id` field - raise NotImplementedError
2. Dependencies MUST be field names, không phải expressions
3. Dot notation cho cross-model: `'relational_field.target_field'`

---

#### 🟢 Concept 3: store=True vs store=False

**Core explanation:**
`store` parameter quyết định computed field có được lưu vào DB column không.

| Attribute | `store=True` | `store=False` (default) |
|-----------|--------------|-------------------------|
| DB Column | ✅ Yes | ❌ No (virtual) |
| Searchable | ✅ Yes | ❌ Only with `search` method |
| Sortable | ✅ Yes | ❌ No |
| Recompute | On dependency change | Every read |
| Performance | Better for reads | Better for storage |

**Source code (odoo/fields.py L336-344):**
```python
if attrs.get('compute'):
    # by default, computed fields are not stored, computed in superuser
    # mode if stored, not copied (unless stored and explicitly not
    # readonly), and readonly (unless inversible)
    attrs['store'] = store = attrs.get('store', False)  # ← DEFAULT = False
    attrs['compute_sudo'] = attrs.get('compute_sudo', store)
    if not (attrs['store'] and not attrs.get('readonly', True)):
        attrs['copy'] = attrs.get('copy', False)
    attrs['readonly'] = attrs.get('readonly', not attrs.get('inverse'))
```

**When to use which:**
```python
# store=True: Thường search/sort, ít thay đổi
task_count = fields.Integer(compute='_compute_count', store=True)

# store=False: Real-time, không cần search
is_late = fields.Boolean(compute='_compute_is_late')  # Check now()
```

**Gotcha:**
- `store=True` + `@api.depends('o2m_field')` có thể gây cascade recompute đắt đỏ
- Sau khi change store=False → store=True, cần `-u module` để tạo column

---

#### 🟢 Concept 4: compute_sudo Parameter

**Core explanation:**
`compute_sudo` controls whether compute method runs as superuser (bypass access rights).

```python
# Default behavior (Source: odoo/fields.py L341):
attrs['compute_sudo'] = attrs.get('compute_sudo', store)
# → store=True: compute_sudo=True (default)
# → store=False: compute_sudo=False (default)
```

**When to use:**
```python
# Compute cần access records user không có quyền
total_company_revenue = fields.Float(
    compute='_compute_revenue',
    compute_sudo=True,  # Access all invoices regardless of user ACL
)

# KHÔNG nên dùng nếu có thể leak sensitive data
user_sensitive_data = fields.Char(
    compute='_compute_data',
    compute_sudo=False,  # Respect ACL
)
```

---

#### 🟢 Concept 5: inverse Method - Editable Computed Fields

**Core explanation:**
`inverse` method cho phép user EDIT computed field thông qua UI. Khi user thay đổi computed field, inverse method được gọi để update source fields.

**Pattern:**
```python
progress = fields.Float(
    string='Progress (%)',
    compute='_compute_progress',
    inverse='_inverse_progress',  # ← Makes it editable!
    store=True,
)

@api.depends('hours_estimated', 'hours_spent')
def _compute_progress(self):
    for record in self:
        if record.hours_estimated:
            record.progress = (record.hours_spent / record.hours_estimated) * 100
        else:
            record.progress = 0.0

def _inverse_progress(self):
    """When user edits progress, calculate hours_spent"""
    for record in self:
        if record.hours_estimated:
            # Reverse calculation: hours_spent = progress% * estimated
            record.hours_spent = (record.progress / 100) * record.hours_estimated
```

**Source code implication (odoo/fields.py L344):**
```python
attrs['readonly'] = attrs.get('readonly', not attrs.get('inverse'))
# → If inverse is defined, readonly=False by default
```

**Use cases:**
- Progress bar editable
- Currency conversion (edit either side)
- Unit conversion (meters ↔ feet)

---

#### 🟢 Concept 6: search Method - Enable Filtering

**Core explanation:**
`search` method enables domain filtering on NON-STORED computed fields. Khi user filter, method trả về domain để convert sang searchable fields.

**Pattern:**
```python
is_overdue = fields.Boolean(
    compute='_compute_is_overdue',
    search='_search_is_overdue',  # ← Enable filtering!
)

@api.depends('due_date', 'state')
def _compute_is_overdue(self):
    now = fields.Datetime.now()
    for record in self:
        record.is_overdue = bool(
            record.due_date and 
            record.due_date < now and 
            record.state != 'done'
        )

def _search_is_overdue(self, operator, value):
    """Convert domain to searchable fields"""
    # Handle: [('is_overdue', '=', True)]
    if operator == '=' and value is True:
        return [
            ('due_date', '<', fields.Datetime.now()),
            ('state', '!=', 'done'),
        ]
    elif operator == '=' and value is False:
        return ['|',
            ('due_date', '>=', fields.Datetime.now()),
            ('state', '=', 'done'),
        ]
    else:
        raise UserError(f"Unsupported search operator: {operator}")
```

**Return value:**
- Must return a DOMAIN list
- Domain searches on STORED fields only
- Complex logic may require OR operators

---

#### 🟢 Concept 7: @api.depends_context

**Core explanation:**
`@api.depends_context` specifies CONTEXT keys that affect computation. Used for non-stored computed fields that depend on runtime context.

**Source code (odoo/api.py L210-233):**
```python
def depends_context(*args):
    """ Return a decorator that specifies the context dependencies of a
    non-stored "compute" method. Each argument is a key in the context's
    dictionary::

        price = fields.Float(compute='_compute_product_price')

        @api.depends_context('pricelist')
        def _compute_product_price(self):
            for product in self:
                if product.env.context.get('pricelist'):
                    pricelist = self.env['product.pricelist'].browse(...)
                else:
                    ...

    All dependencies must be hashable. The following keys have special support:
    * `company` (value in context or current company id),
    * `uid` (current user id and superuser flag),
    * `active_test` (value in env.context or value in field.context).
    """
```

**Example:**
```python
@api.depends_context('company')
def _compute_company_specific_value(self):
    for record in self:
        company = self.env.company
        record.value = company.some_setting * record.amount
```

---

#### 🟢 Concept 8: Cross-Model Dependencies

**Core explanation:**
Computed fields có thể depend on fields từ related models thông qua dot notation.

**Pattern:**
```python
# Depend on M2O target field
@api.depends('project_id.manager_id.name')
def _compute_manager_name(self):
    for task in self:
        task.manager_name = task.project_id.manager_id.name or 'N/A'

# Depend on O2M records (careful: performance!)
@api.depends('task_ids')  # Triggers when tasks added/removed
def _compute_task_count(self):
    for project in self:
        project.task_count = len(project.task_ids)

# Depend on O2M field values
@api.depends('task_ids.state')  # Triggers when any task state changes
def _compute_done_count(self):
    for project in self:
        project.done_count = len(project.task_ids.filtered(
            lambda t: t.state == 'done'
        ))
```

**⚠️ Performance Warning:**
- `@api.depends('o2m_field.some_field')` triggers recompute for EVERY change to ANY child record
- 100 tasks change → parent recomputes 100 times
- Consider `store=True` carefully for O2M dependencies

---

#### 🟢 Concept 9: Recursive Dependencies

**Core explanation:**
A computed field can depend on itself (indirectly) - Odoo detects and handles this.

**Source code (odoo/fields.py L659-660):**
```python
if field is self and index:
    self.recursive = True
```

**Example:**
```python
# Self-referential (parent-child relationship)
parent_id = fields.Many2one('task.task')
child_ids = fields.One2many('task.task', 'parent_id')

total_hours = fields.Float(compute='_compute_total_hours', store=True)

@api.depends('hours_estimated', 'child_ids.total_hours')
def _compute_total_hours(self):
    for task in self:
        # Sum self + all children (recursive)
        task.total_hours = task.hours_estimated + sum(task.child_ids.mapped('total_hours'))
```

**Gotcha:**
- Can cause infinite loops if not careful
- Odoo has safeguards but deep recursion still expensive

---

#### 🟢 Concept 10: Related Fields (Shortcut)

**Core explanation:**
`related` parameter is shorthand for simple computed fields that just return a related value.

```python
# Verbose way
manager_name = fields.Char(compute='_compute_manager_name')

@api.depends('project_id.manager_id.name')
def _compute_manager_name(self):
    for task in self:
        task.manager_name = task.project_id.manager_id.name

# Shorthand with related
manager_name = fields.Char(related='project_id.manager_id.name')
```

**Related field attributes:**
- `related_sudo=True` (default) - compute as superuser
- `readonly=True` (default) - unless explicitly False
- Automatically inherits type from target field

---

#### 🟢 Concept 11: Field Recomputation Triggers

**Core explanation:**
Odoo maintains a dependency graph to know WHEN to recompute fields.

**How it works (odoo/fields.py L639-674):**
```python
def resolve_depends(self, registry):
    """ Return the dependencies of `self` as a collection of field tuples. """
    for dotnames in self.depends:
        for fname in dotnames.split('.'):
            field = Model._fields[fname]
            yield tuple(field_seq)  # Trigger tuple
```

**Debug recomputation:**
```python
# In shell
task = env['task.task'].browse(1)
task.hours_spent = 5  # This should trigger recompute

# Check if recompute happened
print(task.hours_remaining)  # Should reflect new value

# Force recompute (if needed)
task._compute_hours()
```

---

#### 🟢 Concept 12: Common Pitfalls & Debugging

**Pitfall 1: Missing @api.depends**
```python
# BAD - No decorator = never recomputes!
def _compute_hours(self):
    for record in self:
        record.hours_remaining = record.hours_estimated - record.hours_spent

# GOOD
@api.depends('hours_estimated', 'hours_spent')
def _compute_hours(self):
    ...
```

**Pitfall 2: Not assigning all records**
```python
# BAD - Some records not assigned
@api.depends('amount')
def _compute_tax(self):
    for record in self:
        if record.amount > 0:
            record.tax = record.amount * 0.1
        # MISSING: else case leaves record.tax unassigned!

# GOOD
@api.depends('amount')
def _compute_tax(self):
    for record in self:
        if record.amount > 0:
            record.tax = record.amount * 0.1
        else:
            record.tax = 0.0
```

**Pitfall 3: Division by zero**
```python
# BAD
@api.depends('estimated', 'spent')
def _compute_progress(self):
    for r in self:
        r.progress = r.spent / r.estimated  # ZeroDivisionError!

# GOOD
@api.depends('estimated', 'spent')
def _compute_progress(self):
    for r in self:
        r.progress = (r.spent / r.estimated * 100) if r.estimated else 0.0
```

**Pitfall 4: Expensive O2M dependencies**
```python
# DANGEROUS - Recomputes on EVERY task state change
@api.depends('task_ids.state')
def _compute_all_done(self):
    ...

# BETTER - Use scheduled action or button to refresh periodically
all_done = fields.Boolean(compute='_compute_all_done', store=True)
# Only recompute when explicitly needed
```

---

## 📝 PHẦN 2: BÀI TẬP THỰC HÀNH (5+ Exercises)

### Exercise 1: Add task_count to task.project

**Requirements:**
1. Thêm computed field `task_count` vào `models/project.py`:
   - Type: `Integer`
   - Compute: count of `task_ids`
   - Store: `True` (để có thể sort trong list)
2. Add `@api.depends('task_ids')` decorator
3. Update Project Kanban view: hiển thị badge với task count

**Expected Result:**
- Project list sortable by task count
- Kanban shows "X tasks" badge
- Count auto-updates khi add/remove tasks

**Critical UX Checklist:**
- [ ] Badge displays correctly in Kanban
- [ ] Sort by task_count works in tree view
- [ ] Count updates when task added to project

**Shell test:**
```python
project = env['task.project'].browse(1)
print(f"Task count: {project.task_count}")
# Create new task
env['task.task'].create({'name': 'Test', 'description': 'x', 'project_id': project.id})
project.invalidate_cache()  # Clear cache to force recompute
print(f"New task count: {project.task_count}")  # Should be +1
```

---

### Exercise 2: Add hours_remaining to task.task

**Requirements:**
1. Add field `hours_remaining` trong `models/task.py`:
   - Type: `Float`
   - Compute: `hours_estimated - hours_spent`
   - Store: `True`
2. Add `@api.depends('hours_estimated', 'hours_spent')`
3. Update Task Form view: hiển thị hours_remaining (readonly)
4. Update Task Tree view: add column với decoration khi negative

**Expected Result:**
- hours_remaining auto-calculates
- Tree shows red decoration when hours_remaining < 0
- Form shows computed value

**Tree view decoration:**
```xml
<field name="hours_remaining" decoration-danger="hours_remaining &lt; 0"/>
```

---

### Exercise 3: Add editable progress field with inverse

**Requirements:**
1. Add field `progress` trong `models/task.py`:
   - Type: `Float`
   - Compute: `(hours_spent / hours_estimated) * 100`
   - Inverse: `_inverse_progress` - when edited, update `hours_spent`
   - Store: `True`
2. Handle edge case: `hours_estimated = 0` → progress = 0
3. Update Form view: display with widget="progressbar"

**Expected Result:**
- Progress auto-calculates from hours
- User can EDIT progress bar directly
- Editing progress updates hours_spent

**Inverse method logic:**
```python
def _inverse_progress(self):
    for record in self:
        if record.hours_estimated:
            record.hours_spent = (record.progress / 100) * record.hours_estimated
```

**Testing:**
```python
task = env['task.task'].browse(1)
task.hours_estimated = 10
task.hours_spent = 5
print(task.progress)  # Should be 50.0

task.progress = 80  # Edit via inverse
print(task.hours_spent)  # Should be 8.0
```

---

### Exercise 4: Add search method for is_overdue

**Requirements:**
1. Add `search='_search_is_overdue'` to existing `is_overdue` field
2. Implement search method that converts to domain on stored fields
3. Test: Filter tasks by "Overdue = Yes" in search view

**Search method:**
```python
def _search_is_overdue(self, operator, value):
    if operator == '=' and value is True:
        return [
            ('due_date', '<', fields.Datetime.now()),
            ('state', '!=', 'done'),
        ]
    elif operator == '=' and value is False:
        return ['|',
            ('due_date', '=', False),
            '|',
            ('due_date', '>=', fields.Datetime.now()),
            ('state', '=', 'done'),
        ]
    return []
```

**Update search view:**
```xml
<filter name="overdue" string="Overdue" domain="[('is_overdue', '=', True)]"/>
```

---

### Exercise 5: Cross-model computed field

**Requirements:**
1. Add `project_manager_name` to `task.task`:
   - Type: `Char`
   - Related: `project_id.manager_id.name`
2. OR implement with `@api.depends('project_id.manager_id.name')`
3. Display in Task form header

**Two approaches:**
```python
# Approach A: related (simple)
project_manager_name = fields.Char(related='project_id.manager_id.name', store=False)

# Approach B: computed (more control)
project_manager_name = fields.Char(compute='_compute_manager_name')

@api.depends('project_id.manager_id.name')
def _compute_manager_name(self):
    for task in self:
        task.project_manager_name = task.project_id.manager_id.name or 'No Manager'
```

---

## ❓ PHẦN 3: CÂU HỎI KIỂM TRA (10 Questions)

### Level: Easy (3)
1. Computed field mặc định có được lưu vào DB không? (`store=True` hay `store=False` default?)
2. `@api.depends` decorator dùng để làm gì? Viết ví dụ depends 2 fields.
3. Khi nào dùng `inverse` method? Cho 1 use case thực tế.

### Level: Medium (4)
4. **Debug**: Computed field `total` không update khi `amount` thay đổi. Liệt kê 3 nguyên nhân và cách fix.
5. **Performance**: Tại sao `@api.depends('task_ids.state')` có thể gây performance issues? Đề xuất giải pháp.
6. **Search**: Viết `_search_is_high_priority` method cho field non-stored `is_high_priority = priority == 'high'`.
7. **Gotcha**: Điều gì xảy ra nếu computed method không assign value cho một số records?

### Level: Hard (3)
8. **Design**: So sánh `related='field.name'` vs `compute='_compute_x'`. Khi nào dùng cái nào?
9. **Production**: Thiết kế computed field `total_revenue` cho `project` = sum of all `task.amount`. Xem xét:
   - store vs non-store
   - Performance khi 1000+ tasks
   - Searchability requirements
10. **Integration**: Viết complete solution cho: Task progress tính từ completed subtasks. Subtask là self-reference (parent_id). Total progress = (done_subtasks / total_subtasks) * 100.

---

## 🎓 PHẦN 4: ADVANCED TOPICS

### 4.1 compute_sudo và Security
```python
# Compute với data user không có access
total_all_orders = fields.Float(
    compute='_compute_total',
    compute_sudo=True,  # Bypass ACL
)

@api.depends('company_id')
def _compute_total(self):
    # Runs as superuser, can access all orders
    Order = self.env['sale.order'].sudo()
    for record in self:
        orders = Order.search([('company_id', '=', record.company_id.id)])
        record.total_all_orders = sum(orders.mapped('amount_total'))
```

### 4.2 Dynamic Dependencies
```python
@api.depends(lambda self: [f'field_{i}' for i in range(10)])
def _compute_dynamic(self):
    ...
```

### 4.3 Optimizing O2M Computed Fields
```python
# SLOW: Calls len() N times in a loop
@api.depends('order_ids')
def _compute_order_count(self):
    for partner in self:
        partner.order_count = len(partner.order_ids)

# FAST: Single SQL query with read_group
@api.depends('order_ids')
def _compute_order_count(self):
    data = self.env['sale.order'].read_group(
        domain=[('partner_id', 'in', self.ids)],
        fields=['partner_id'],
        groupby=['partner_id'],
    )
    counts = {item['partner_id'][0]: item['partner_id_count'] for item in data}
    for partner in self:
        partner.order_count = counts.get(partner.id, 0)
```

---

## ⚠️ PHẦN 5: GOTCHAS & COMMON MISTAKES

1. **Missing @api.depends**: Computed field never recomputes
2. **Missing assignment**: Some records have no value → CacheMiss error
3. **Division by zero**: Always check denominator
4. **Expensive O2M depends**: `@api.depends('o2m.field')` triggers on EVERY child change
5. **store=True after install**: Need `-u module` to create DB column
6. **Circular dependency**: Field A depends on B, B depends on A → RecursionError
7. **search method wrong return**: Must return domain list, not bool

---

## 📊 PHẦN 6: Evaluation (To be filled by Trainer)

| Tiêu chí | Weight | Điểm (/10) | Ghi chú |
|----------|--------|------------|---------|
| Hiểu computed vs regular fields | 15% | 9/10 | Hiểu rõ store, compute, decorator |
| @api.depends usage correct | 20% | 9/10 | Đúng dependencies, hiểu dot-notation |
| store=True/False decision | 15% | 8/10 | Hiểu khi nào store, performance impact |
| inverse method implementation | 15% | 9/10 | Implement progress inverse đúng |
| search method implementation | 10% | 7/10 | Hiểu logic nhưng nhầm value type |
| Debug computed issues | 15% | 8/10 | Liệt kê 2/3 nguyên nhân |
| Trả lời câu hỏi (8+ correct) | 10% | 8/10 | Easy 3/3, Medium 2.5/4, Hard 3/3 |
| **TỔNG** | **100%** | **8.4** | |

---

## 📌 KẾT QUẢ VÀ GHI CHÚ AI

### Kết quả ngày
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Đọc source (2h) | 9 | Hiểu depends, resolve_depends, Field class |
| Viết code (2h) | 9 | task_count, hours_remaining, progress all correct |
| Shell/Debug (2h) | 8 | Test tốt, debug cache issue, kanban image |
| Tổng kết (1h) | 8 | Questions 8.5/10 |
| **TỔNG NGÀY 7** | **8.5/10** | Strong performance |

### 📌 Ghi chú AI
> - Learner đã nắm vững computed fields, @api.depends, inverse, search
> - Hiểu read_group optimization dù chưa cần dùng thực tế
> - Tự debug được cache issues và kanban image display
> - Cần review: search method (nhầm Boolean value vs string)
> - Bonus: Học thêm kanban_image(), t-att-src QWeb directives

### ⚠️ Lưu ý cho Day 8
> Day 8 sẽ học Constraints:
> - @api.constrains decorator
> - _sql_constraints
> - @api.ondelete
> - ValidationError vs UserError
> - Note: Computed fields từ Day 7 có thể được validate bằng constraints Day 8
> 
> **TODO**: Review roadmap và module_spec để đảm bảo đủ complexity (thêm amount, total_revenue, subtasks)
