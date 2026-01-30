# 📋 Day 16 - Model Inheritance + Override (FAST-TRACK)

> **Mode**: ⚡ ACCELERATED - Focus on job-critical skills
> **Duration**: 7 giờ (Ngày 2 full)
> **Goal**: Extend models và override methods đúng cách

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 16 of 21 (Fast-track) |
| **Chủ đề** | **Model Inheritance + Method Override** |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Day 15 (View Inheritance), Day 3 (CRUD) |
| **Mục tiêu chính** | Extend models và override methods đúng cách |

---

## 🎯 LEARNING OBJECTIVES

By end of session:
- [ ] Extend model có sẵn thêm fields
- [ ] Override CRUD methods (create/write/unlink)
- [ ] Hiểu super() positioning (trước/sau)
- [ ] Fix được common bugs khi override

---

## Section 1: CONCEPTS (1 giờ)

### 1.1 Model Inheritance với _inherit

```python
class ResPartner(models.Model):
    _inherit = 'res.partner'  # Extend existing
    
    task_count = fields.Integer(compute='_compute_task_count')
```

### 1.2 Override Pattern

```python
@api.model_create_multi
def create(self, vals_list):
    # BEFORE: Pre-process
    for vals in vals_list:
        vals['code'] = self._generate_code()
    
    # SUPER: Create records
    records = super().create(vals_list)
    
    # AFTER: Post-process
    for record in records:
        record._send_notification()
    
    return records  # MUST return!
```

### 1.3 super() Positioning

| Scenario | Call super() | Why |
|----------|--------------|-----|
| Validate data | BEFORE | Stop early if invalid |
| Modify vals | BEFORE | Vals used by parent |
| Process created record | AFTER | Record exists |
| Send notification | AFTER | Ensure success |

### 1.4 Common Bugs

1. **Forgot return**: `return super().write(vals)`
2. **Modify vals AFTER super**: Too late!
3. **Infinite loop**: `self.field = val` trong write() gọi write() lại
4. **Wrong self**: Trong create(), self là empty

### 1.5 Prototype Inheritance (`_inherit` + `_name`)

Copy toàn bộ features của model cũ sang model MỚI (tách biệt hoàn toàn).

```python
class TaskArchive(models.Model):
    _name = 'task.archive'      # New table
    _inherit = 'task.task'      # Copy columns from task.task
```

### 1.6 Delegation Inheritance (`_inherits`)

Nhúng model khác vào model này (transparent).

```python
class TaskUser(models.Model):
    _name = 'task.user'
    _inherits = {'res.users': 'user_id'}
    
    user_id = fields.Many2one('res.users', required=True, ondelete='cascade')
```
Field của `res.users` (name, login) có thể truy cập trực tiếp từ `task.user`.

---

## Section 2: EXERCISES (6 giờ)

### 🟢 Exercise 1: Extend res.partner (15 phút)

**Task**: Thêm `task_ids` và `task_count` vào res.partner

**Expected**:
```python
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    task_ids = fields.One2many('task.task', 'assigned_to')
    task_count = fields.Integer(compute='_compute_task_count')
    
    def _compute_task_count(self):
        for partner in self:
            partner.task_count = len(partner.task_ids)
```

---

### 🟢 Exercise 2: Override create() - Auto Sequence (20 phút)

**Task**: Tự động tạo code "TASK-001" khi create

**Expected**:
```python
@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('task.task')
    return super().create(vals_list)
```

---

### 🟢 Exercise 3: Override write() - Track State (20 phút)

**Task**: Khi state đổi sang 'done', set completion_date

**Expected**:
```python
def write(self, vals):
    if vals.get('state') == 'done':
        vals['completion_date'] = fields.Date.today()
    return super().write(vals)
```

---

### 🟢 Exercise 4: Override unlink() - Prevent Delete (20 phút)

**Task**: Không cho xóa task đã done

**Expected**:
```python
def unlink(self):
    for task in self:
        if task.state == 'done':
            raise UserError(_("Cannot delete completed tasks!"))
    return super().unlink()
```

---

### 🟡 Exercise 5: Fix Bug - Missing Return (15 phút)

**Buggy code**:
```python
def write(self, vals):
    if vals.get('state'):
        self._log_state_change(vals['state'])
    super().write(vals)
```

**Fix**: Thêm `return`

---

### 🟡 Exercise 6: Fix Bug - Wrong self in create (20 phút)

**Buggy code**:
```python
def create(self, vals_list):
    super().create(vals_list)
    for record in self:  # BUG: self is empty!
        record.message_post(body="Created!")
```

**Fix**: Use return value của super()

---

### 🟡 Exercise 7: Fix Bug - Infinite Loop (25 phút)

**Buggy code**:
```python
def write(self, vals):
    result = super().write(vals)
    if vals.get('state') == 'done':
        self.completion_date = fields.Date.today()  # BUG: triggers write!
    return result
```

**Fix**: Set value in vals BEFORE super()

---

### 🔴 Exercise 8: Override copy() (30 phút)

**Task**: Khi duplicate task, thêm "(Copy)" vào name và reset state

**Expected**:
```python
def copy(self, default=None):
    default = dict(default or {})
    default.update({
        'name': f"{self.name} (Copy)",
        'state': 'draft',
        'completion_date': False,
    })
    return super().copy(default)
```

---

### 🔴 Exercise 9: Override name_get() (25 phút)

**Task**: Hiển thị task với format "[CODE] Name (State)"

**Expected**:
```python
def name_get(self):
    result = []
    for record in self:
        name = f"[{record.code}] {record.name} ({record.state})"
        result.append((record.id, name))
    return result
```

---

### 🔴 Exercise 10: Combined - Full Lifecycle (40 phút)

**Task**: Implement đầy đủ lifecycle cho task.task:

1. **create()**: Auto-generate code, send notification
2. **write()**: Track state changes, log old vs new
3. **unlink()**: Prevent delete if has children
4. **copy()**: Reset state, clear dates

**Template**:
```python
class TaskTask(models.Model):
    _inherit = 'task.task'
    
    @api.model_create_multi
    def create(self, vals_list):
        # TODO: Implement
        pass
    
    def write(self, vals):
        # TODO: Track old state
        pass
    
    def unlink(self):
        # TODO: Check children
        pass
    
    def copy(self, default=None):
    def copy(self, default=None):
        # TODO: Reset fields
        pass
```

### 🔴 Exercise 11: Prototype Inheritance (New - 20 phút)

**Task**: Tạo model `task.template` copy cấu trúc của `task.task` nhưng tách biệt dữ liệu.

**Expected**:
```python
class TaskTemplate(models.Model):
    _name = 'task.template'
    _inherit = 'task.task'
    _description = "Task Template"
    
    # Override fields nếu cần (VD: bỏ required)
    project_id = fields.Many2one('task.project', required=False)
```

---

## Section 3: COMBINED PRACTICE (Cuối ngày)

### Real Scenario: Customize Sale Order

**Task**: Extend `sale.order` với:
1. Field `custom_notes` (Text)
2. Field `approval_required` (Boolean)
3. Override `action_confirm()` để check approval

Đây là preview cho mock task Ngày 4.

---

## Section 4: QUICK CHECK

1. `_inherit` vs `_inherits` khác nhau thế nào?
2. Khi nào call super() TRƯỚC logic?
3. Tại sao phải return từ write()?
4. Trong create(), self là gì?
5. Làm sao tránh infinite loop trong write()?

---

## ✅ TIÊU CHÍ HOÀN THÀNH

| Tiêu chí | Đạt |
|----------|-----|
| Exercise 1-4 (basic) | ⬜ |
| Exercise 5-7 (bug fixes) | ⬜ |
| Exercise 8-10 (advanced) | ⬜ |
| Combined practice | ⬜ |

---

## 📝 ĐÁNH GIÁ (Mentor điền)

| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Concepts | _ | |
| Exercises | _ | |
| Bug fixes | _ | |
| **TỔNG** | **_/10** | |
