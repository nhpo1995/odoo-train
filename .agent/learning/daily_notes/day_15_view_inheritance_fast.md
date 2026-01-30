# 📋 Day 15 - View Inheritance XPath (FAST-TRACK)

> **Mode**: ⚡ ACCELERATED - Focus on job-critical skills
> **Duration**: 4 giờ (chiều Ngày 1)
> **Goal**: Master xpath để sửa views có sẵn

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 15 of 21 (Fast-track) |
| **Chủ đề** | **View Inheritance với XPath** |
| **Thời lượng** | 4 tiếng |
| **Prerequisites** | Day 4 (Views basics) |
| **Mục tiêu chính** | Sửa được views có sẵn bằng xpath |

---

## 🎯 LEARNING OBJECTIVES

By end of session:
- [ ] Hiểu inherit_id trong view
- [ ] Viết được xpath expression đúng
- [ ] Dùng được 5 positions: inside, before, after, replace, attributes
- [ ] Sửa được nhiều loại views (form, tree, kanban)

---

## Section 1: CONCEPTS (30 phút)

### 1.1 View Inheritance Basics

```xml
<record id="view_task_form_inherit" model="ir.ui.view">
    <field name="name">task.task.form.inherit</field>
    <field name="model">task.task</field>
    <field name="inherit_id" ref="task_management.view_task_form"/>
    <field name="arch" type="xml">
        <!-- xpath changes here -->
    </field>
</record>
```

**Key**: `inherit_id` = ID của view CHA cần sửa

### 1.2 XPath Syntax

| Pattern | Meaning |
|---------|---------|
| `//field[@name='name']` | Field có name='name' |
| `//notebook` | Element notebook |
| `//page[@name='details']` | Page có name='details' |
| `//button[@name='action_done']` | Button với method |
| `//group[1]` | Group đầu tiên |
| `//div[hasclass('oe_button_box')]` | Div có class |

### 1.3 Five Positions

| Position | Usage | Example |
|----------|-------|---------|
| `after` | Thêm SAU | `<field name="new"/>` sau field cũ |
| `before` | Thêm TRƯỚC | `<field name="new"/>` trước field cũ |
| `inside` | Thêm VÀO CUỐI | Thêm field vào group |
| `replace` | THAY THẾ | Đổi widget hoặc xóa |
| `attributes` | SỬA attribute | invisible, readonly, required |

### 1.4 Advanced Dynamic Attributes (New)

**1. Context-based Visibility**:
```xml
<attribute name="invisible">context.get('hide_notes')</attribute>
```

**2. Parent Field (in Subviews)**:
```xml
<!-- Trong One2many subview -->
<field name="qty" invisible="parent.state == 'done'"/>
```

**3. Add/Remove Classes**:
```xml
<attribute name="class" add="text-danger" remove="text-muted" separator=" "/>
```

---

## Section 2: EXERCISES (3.5 giờ)

### 🟢 Exercise 1: Add Field After (10 phút)

**Task**: Thêm field `priority` SAU field `name` trong task form

**Expected**:
```xml
<xpath expr="//field[@name='name']" position="after">
    <field name="priority" widget="priority"/>
</xpath>
```

---

### 🟢 Exercise 2: Add Field Before (10 phút)

**Task**: Thêm field `code` TRƯỚC field `name`

**Expected**:
```xml
<xpath expr="//field[@name='name']" position="before">
    <field name="code" readonly="1"/>
</xpath>
```

---

### 🟢 Exercise 3: Add Field Inside Group (15 phút)

**Task**: Thêm field `create_date` vào cuối group chính

**Expected**:
```xml
<xpath expr="//group[@name='main']" position="inside">
    <field name="create_date" readonly="1"/>
</xpath>
```

---

### 🟡 Exercise 4: Replace Widget (15 phút)

**Task**: Đổi `tag_ids` từ default sang `many2many_tags` với colors

**Expected**:
```xml
<xpath expr="//field[@name='tag_ids']" position="replace">
    <field name="tag_ids" widget="many2many_tags" 
           options="{'color_field': 'color'}"/>
</xpath>
```

---

### 🟡 Exercise 5: Hide Field Conditionally (20 phút)

**Task**: Ẩn `hours_spent` khi state = 'draft'

**Expected**:
```xml
<xpath expr="//field[@name='hours_spent']" position="attributes">
    <attribute name="invisible">state == 'draft'</attribute>
</xpath>
```

---

### 🟡 Exercise 6: Add Notebook Page (20 phút)

**Task**: Thêm tab "Advanced" với create_date và write_date

**Expected**:
```xml
<xpath expr="//notebook" position="inside">
    <page string="Advanced" name="advanced">
        <group>
            <field name="create_date" readonly="1"/>
            <field name="write_date" readonly="1"/>
        </group>
    </page>
</xpath>
```

---

### 🔴 Exercise 7: Modify Tree View Decoration (25 phút)

**Task**: Trong tree view, highlight tasks quá hạn (due_date < today) bằng màu đỏ

**Step 1**: Tìm tree view inherit
**Step 2**: Thêm decoration

**Expected**:
```xml
<record id="view_task_tree_inherit" model="ir.ui.view">
    <field name="name">task.task.tree.inherit</field>
    <field name="model">task.task</field>
    <field name="inherit_id" ref="task_management.view_task_tree"/>
    <field name="arch" type="xml">
        <xpath expr="//tree" position="attributes">
            <attribute name="decoration-danger">due_date &lt; current_date</attribute>
        </xpath>
    </field>
</record>
```

---

### 🔴 Exercise 8: Complex - Multiple Changes (30 phút)

**Task**: Trong một view inheritance file, thực hiện:
1. Thêm field `estimated_hours` sau `name`
2. Ẩn button delete cho state='done'
3. Thêm class CSS cho oe_title

**Expected**:
```xml
<record id="view_task_form_custom" model="ir.ui.view">
    <field name="name">task.task.form.custom</field>
    <field name="model">task.task</field>
    <field name="inherit_id" ref="task_management.view_task_form"/>
    <field name="arch" type="xml">
        <!-- 1. Add field -->
        <xpath expr="//field[@name='name']" position="after">
            <field name="estimated_hours"/>
        </xpath>
        
        <!-- 2. Hide delete button -->
        <xpath expr="//button[@name='unlink']" position="attributes">
            <attribute name="invisible">state == 'done'</attribute>
        </xpath>
        
        <!-- 3. Add CSS class -->
        <xpath expr="//div[hasclass('oe_title')]" position="attributes">
            <attribute name="class" add="o_task_title" separator=" "/>
        </xpath>
    </field>
</record>
```

### 🔴 Exercise 9: Dynamic Context (New - 15 phút)

**Task**: Ẩn field `description` nếu trong context có key `hide_desc`.

**Expected**:
```xml
<xpath expr="//field[@name='description']" position="attributes">
    <attribute name="invisible">context.get('hide_desc')</attribute>
</xpath>
```

### 🔴 Exercise 10: Parent Field in Subview (New - 20 phút)

**Task**: Trong View subtask (One2many), ẩn field `deadline` nếu Parent Task đã done.

**Expected**:
```xml
<field name="child_ids">
    <tree editable="bottom">
        <field name="name"/>
        <!-- parent refers to the Main Task -->
        <field name="date_deadline" invisible="parent.state == 'done'"/>
    </tree>
</field>
```

---

## Section 3: QUICK CHECK (10 phút)

1. `inherit_id` reference đến gì?
2. Để thêm field VÀO CUỐI group, dùng position gì?
3. `position="replace"` với nội dung trống làm gì?
4. XPath match 2 elements sẽ gây lỗi gì?
5. Làm sao thêm class mà không xóa class cũ?

<details>
<summary>Đáp án</summary>

1. View ID của view cha
2. `position="inside"`
3. Xóa element đó
4. Error - xpath match multiple
5. `<attribute name="class" add="new_class" separator=" "/>`
6. `context.get('key')` check gì? (Check keys trong context dictionary)
7. `parent.field` dùng ở đâu? (Dùng trong subviews O2M/M2M)

</details>

---

## ✅ TIÊU CHÍ HOÀN THÀNH

| Tiêu chí | Đạt |
|----------|-----|
| Exercise 1-3 (basic) | ✅ |
| Exercise 4-6 (intermediate) | ✅ |
| Exercise 7-8 (advanced) | ✅ |
| Exercise 9-10 (new advanced) | ✅ |
| Quick check 5/5 | ✅ |

---

## 📝 ĐÁNH GIÁ (Mentor điền)

| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Concepts | 10/10 | Excellent understanding of XPath & Advanced attributes |
| Exercises | 9.5/10 | 10/10 completed. Minor XML syntax errors. |
| **TỔNG** | **9.5/10** | **Outstanding! Ready for Model Inheritance.** |
