# 📋 Day 17 - CSS + Calendar + Debug (FAST-TRACK)

> **Mode**: ⚡ ACCELERATED - Focus on job-critical skills
> **Duration**: 7 giờ (Ngày 3 full)
> **Goal**: Frontend styling + Debug skills

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 17 of 21 (Fast-track) |
| **Chủ đề** | **CSS + Calendar + Debug** |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Day 15-16 (Inheritance) |
| **Mục tiêu chính** | Custom styling + debug từ traceback |

---

## 🎯 LEARNING OBJECTIVES

By end of session:
- [ ] Thêm được CSS file custom
- [ ] Tạo được Calendar view
- [ ] Đọc được traceback và tìm root cause
- [ ] Fix được common Odoo errors

---

## Section 1: CSS CUSTOMIZATION (1.5 giờ)

### 1.1 File Structure

```
task_management/
├── static/
│   └── src/
│       └── css/
│           └── task_style.css
```

### 1.2 Register in Manifest

```python
'assets': {
    'web.assets_backend': [
        'task_management/static/src/css/task_style.css',
    ],
},
```

**Tip**: Dùng URL param `?debug=assets` để debug CSS/JS gốc (không bị minified).

### 🟢 Exercise CSS-1: Basic Styling (15 phút)

**Task**: Tạo CSS file với styling cho task cards

**Expected**:
```css
/* static/src/css/task_style.css */
.o_task_urgent {
    border-left: 4px solid #dc3545;
    background-color: #fff5f5;
}

.o_task_done {
    opacity: 0.6;
}
```

---

### 🟢 Exercise CSS-2: Apply Class in Kanban (20 phút)

**Task**: Apply CSS class dựa trên priority

**Expected** (trong kanban template):
```xml
<div t-attf-class="oe_kanban_global_click #{record.priority.raw_value == '2' ? 'o_task_urgent' : ''}">
```

---

## Section 2: CALENDAR VIEW (1.5 giờ)

### 2.1 Calendar Basics

```xml
<calendar string="Tasks" date_start="due_date" color="project_id">
    <field name="name"/>
    <field name="assigned_to"/>
</calendar>
```

### 🟢 Exercise Calendar-1: Create Calendar View (20 phút)

**Task**: Tạo calendar view cho task.task

**Expected**:
```xml
<record id="view_task_calendar" model="ir.ui.view">
    <field name="name">task.task.calendar</field>
    <field name="model">task.task</field>
    <field name="arch" type="xml">
        <calendar string="Task Calendar" 
                  date_start="due_date" 
                  color="project_id"
                  quick_create="0">
            <field name="name"/>
            <field name="assigned_to"/>
            <field name="state"/>
        </calendar>
    </field>
</record>
```

---

## Section 3: DEBUG SKILLS (4 giờ) ⭐ CRITICAL

### 3.1 Đọc Traceback

**Cách đọc** (từ DƯỚI lên):
1. Dòng cuối = Error type + message
2. Dòng trên = File + line gây lỗi
3. Trace ngược = Call stack

### Debug Scenario 1: AttributeError (20 phút)

**Traceback**:
```
File "/odoo/custom_addons/task_management/models/task.py", line 45
    record.nonexistent_field
AttributeError: 'task.task' object has no attribute 'nonexistent_field'
```

**Questions**:
1. Lỗi gì?
2. File nào?
3. Dòng nào?
4. Root cause?

**Answer**: Field không tồn tại, check spelling hoặc chưa upgrade module

---

### Debug Scenario 2: ValidationError (25 phút)

**Traceback**:
```
odoo.exceptions.ValidationError: 
Due date must be in the future!
```

**Task**: Tìm constraint gây lỗi và fix

**Hint**: Check `@api.constrains` trong model

---

### Debug Scenario 3: AccessError (25 phút)

**Traceback**:
```
odoo.exceptions.AccessError:
You are not allowed to modify 'task.task' (task.task) records.
Allowed groups: Task Manager
```

**Task**: 
1. User thuộc group nào?
2. ACL cho phép gì?
3. Làm sao fix?

---

### Debug Scenario 4: RecursionError (30 phút)

**Traceback**:
```
RecursionError: maximum recursion depth exceeded
```

**Buggy code** (tìm lỗi):
```python
def write(self, vals):
    result = super().write(vals)
    if vals.get('state') == 'done':
        self.completion_date = fields.Date.today()
    return result
```

**Task**: Tại sao bị infinite loop? Fix như thế nào?

---

### Debug Scenario 5: KeyError in vals (30 phút)

**Traceback**:
```
KeyError: 'partner_id'
```

**Buggy code**:
```python
def create(self, vals_list):
    for vals in vals_list:
        partner = self.env['res.partner'].browse(vals['partner_id'])
    return super().create(vals_list)
```

**Task**: Tại sao error? (Hint: partner_id có thể không có trong vals)

---

### Debug Scenario 6: Empty Recordset patterns (New - 20 phút)

**Bug 1**: `browse([])` returns Empty, not False (như mong đợi).
**Bug 2**: `mapped()` trên Empty recordset returns `[]` (List), không phải Recordset.

**Check**:
```python
tasks = self.env['task.task'].browse([])
if tasks: 
    print("Zero tasks but evaluates to True??") # NO, Recordset([]) is Falsy
    
val = tasks.mapped('name') # Returns []
```

### Debug Scenario 7: ensure_one() (New - 15 phút)

**Error**: `Expected singleton: task.task(1, 2)`

**Cause**: Gọi field/method trên recordset có nhiều hơn 1 record.
**Fix**: `self.ensure_one()` hoặc loop.

### Debug Scenario 8: val vs vals_list (New - 15 phút)

**Confusion**:
- `create(vals_list)`: list of dicts (Odoo 12+)
- `write(vals)`: single dict

**Bug**: `create` cố truy cập `vals_list['name']` → Error (phải loop).

---

### 🔴 Debug Challenge: Real Error Log (45 phút)

**Task**: Analyze log file và tìm tất cả errors

```log
2024-01-29 09:00:01,234 ERROR db odoo.sql_db: bad query: SELECT ...
2024-01-29 09:00:02,345 WARNING db odoo.models: Access Denied by ACLs for operation read on model task.task
2024-01-29 09:00:03,456 ERROR db odoo.addons.task_management.models.task: TypeError: unsupported operand type(s)
```

**Questions**:
1. Có bao nhiêu errors?
2. Error nghiêm trọng nhất?
3. Cách fix từng error?

---

## Section 4: INTEGRATION PRACTICE (cuối ngày)

### Mini Project: Custom Task Card

**Task**: Kết hợp tất cả skills:
1. CSS: Style urgent tasks
2. XPath: Add priority badge trong kanban
3. Override: Log khi task done

---

## ✅ TIÊU CHÍ HOÀN THÀNH

| Tiêu chí | Đạt |
|----------|-----|
| CSS exercises | ⬜ |
| Calendar view working | ⬜ |
| Debug scenarios 1-5 | ⬜ |
| Debug challenge | ⬜ |
| Mini project | ⬜ |

---

## 📝 ĐÁNH GIÁ (Mentor điền)

| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| CSS/Calendar | _ | |
| Debug skills | _ | |
| Integration | _ | |
| **TỔNG** | **_/10** | |
