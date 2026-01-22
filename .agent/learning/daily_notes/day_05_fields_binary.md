# 📋 DAY 5 - Fields System + Binary Images

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 5 of 21 |
| **Chủ đề** | Fields System - Descriptors, Basic Types, Binary/Image Fields |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Day 4 (Views: Tree, Search, Kanban), Day 3 (CRUD, Form view) |
| **Mục tiêu chính** | Hiểu Field là Python descriptors, master các loại field cơ bản (Char, Integer, Float, Boolean, Date, Datetime, Text, Selection), và implement Binary/Image fields cho upload ảnh bìa project |

---

## 📦 MODULE PROGRESS (Trainer phải đọc!)

### 📍 Trước Day 5
Module `task_management` đã có:
- Model `task.task` với basic fields: name, description, state (Selection), priority
- Complete views: Form (với attrs), Tree (với decorations), Kanban (QWeb cards), Search (filters + group by)
- Action + Menu hoàn chỉnh

### ✅ Sau Day 5 (Hôm nay)
Module sẽ có thêm:
- **Model mới**: `task.project` với Binary image field (project cover image)
- **Enhanced `task.task`** với production-critical fields:
  - `due_date` (Datetime) - Deadline tracking
  - `hours_estimated` (Float) - Effort planning
  - `hours_spent` (Float) - Actual effort
- **Image widget** trong form views - upload và display images
- **Deep understanding** of Field descriptors (Python pattern)

### ⭐ Production Target (Từ Roadmap)
```
Task Management Module (Day 5 - Fields foundation):
- task.project model → Container cho tasks với cover image
- task.task enhanced → Deadline + effort tracking fields
- Binary/Image handling → File uploads ready
- Field system mastery → Nền tảng cho Day 6 (Relationships)
```

### 🔗 Đây là ngày 5/19 của việc build complete module

**Day 5 significance**: Fields là TRÁI TIM của Odoo models. Hiểu field descriptors = hiểu cách Odoo định nghĩa data schema declaratively. Day này builds foundation cho ALL future features (computed fields, relational fields, constraints).

---

## 🎯 LEARNING OBJECTIVES

By end of day, learner will be able to:
- [ ] Giải thích Field là Python descriptor và cách chúng hoạt động (class-level vs instance-level)
- [ ] Sử dụng thành thạo 8 basic field types với đúng use cases
- [ ] Phân biệt Binary vs Image field và khi nào dùng
- [ ] Implement image upload với widget="image" trong form view
- [ ] Master field attributes: required, readonly, default, string, help, store
- [ ] Tạo được task.project model với image field
- [ ] Enhance task.task với deadline + effort tracking fields
- [ ] Debug field-related errors (validation, descriptor assignment, etc.)

---

## 📊 COVERAGE CHECKLIST (For Planner - MUST verify)

- [x] Context7 queried (2 queries: field types/attributes, Binary/Image fields)
- [x] Source code line numbers verified (fields.py: Field L116-1212, Image L2163-2226, Selection L2228-2435, Char L1604-1659)
- [x] 14 concepts covered (descriptors, 8 basic types, Binary, Image, Selection, attributes, widgets)
- [x] 5 complex exercises (create task.project, image upload, enhance task.task, debug scenarios)
- [x] 10 questions (Easy: 3, Medium: 4, Hard: 3 - scenario/debug/design)
- [x] Advanced topics section filled (Image resizing, translate, company_dependent)
- [x] Gotchas/Common mistakes documented (6 gotchas)
- [x] Performance considerations included (store=False, binary size)

---

## 📚 PHẦN 1: NỘI DUNG BÀI HỌC

### 1.1 Lý thuyết cần dạy

#### 🟢 Core Concepts: Field Descriptors

- [ ] **Concept 1: Field là Python Descriptor**
  - **Core explanation**: Field trong Odoo KHÔNG phải là giá trị data, mà là **descriptor object** (Python pattern). Khi define `name = fields.Char()`, bạn tạo descriptor ở class level. Descriptor control access (`__get__`, `__set__`) khi truy cập `record.name`. Giá trị thực tế stored trong cache/database, KHÔNG trong field object.
  - **Syntax**:
    ```python
    class Task(models.Model):
        _name = 'task.task'
        name = fields.Char('Task Name')  # Descriptor object (class-level)
    
    # Usage:
    task = env['task.task'].browse(1)
    print(task.name)  # Descriptor's __get__ trigged → fetch từ cache/DB
    task.name = 'New'  # Descriptor's __set__ triggered → write to cache/DB
    ```
  - **When to use**: LUÔN LUÔN - đây là cách duy nhất để define fields trong Odoo
  - **Comparison vs SQLAlchemy**: Tương tự `Column(String())` trong SQLAlchemy - cả 2 đều dùng descriptor pattern
  - **Gotcha**: KHÔNG BAO GIỜ assign descriptor: `task.name = fields.Char()` là SAI (override descriptor)

---

#### 🟢 Core Concepts: Basic Field Types

- [ ] **Concept 2: Char Field - Single-line Text**
  - **Core explanation**: `fields.Char()` cho short text (≤256 chars mặc định). Stored as `VARCHAR` trong PostgreSQL. Parameter `size` limit length (Odoo 14+ không bắt buộc size). Hiển thị dạng single-line input trong form view.
  - **Syntax**:
    ```python
    name = fields.Char(string='Task Name', required=True, size=100)
    reference = fields.Char('Reference Code', size=20, help='e.g. TASK-001')
    ```
  - **When to use**: Names, codes, short descriptions, URLs, email (without validation)
  - **Performance**: Index với `index=True` cho fields search thường xuyên

- [ ] **Concept 3: Text Field - Multi-line Text**
  - **Core explanation**: `fields.Text()` cho long text (no size limit). Stored as `TEXT` trong PostgreSQL. Hiển thị dạng textarea trong form view. Support translation với `translate=True`.
  - **Syntax**:
    ```python
    description = fields.Text('Description')
    notes = fields.Text('Internal Notes', translate=True)  # Multi-language
    ```
  - **When to use**: Descriptions, notes, comments, rich content
  - **Gotcha**: Text fields KHÔNG nên search với `ilike` trên large datasets (chậm)

- [ ] **Concept 4: Integer Field - Whole Numbers**
  - **Core explanation**: `fields.Integer()` cho số nguyên. Stored as `INT4` (32-bit) trong PostgreSQL. Range: -2,147,483,648 đến 2,147,483,647. Hiển thị dạng number input trong form view.
  - **Syntax**:
    ```python
    sequence = fields.Integer('Sequence', default=10)
    count = fields.Integer('Task Count', readonly=True)
    ```
  - **When to use**: Counters, sequences, quantities (nguyên), priority levels
  - **Advanced**: Dùng `group_operator='sum'` cho aggregation trong read_group()

- [ ] **Concept 5: Float Field - Decimal Numbers**
  - **Core explanation**: `fields.Float()` cho số thập phân. Parameter `digits=(precision, scale)` control độ chính xác. Stored as `NUMERIC` trong PostgreSQL. Default precision based on field type.
  - **Syntax**:
    ```python
    hours_estimated = fields.Float('Estimated Hours', digits=(6, 2))  # 9999.99
    price = fields.Float('Price', digits=(10, 4))  # For currency-like precision
    progress = fields.Float('Progress %', digits=(5, 2))  # 100.00%
    ```
  - **When to use**: Prices (before Monetary), hours, percentages, measurements
  - **Gotcha**: Float comparison issues - dùng rounding hoặc Monetary cho currency

- [ ] **Concept 6: Boolean Field - True/False**
  - **Core explanation**: `fields.Boolean()` cho true/false values. Stored as `BOOL` trong PostgreSQL. Default value `False` nếu không set. Hiển thị dạng checkbox trong form view.
  - **Syntax**:
    ```python
    is_active = fields.Boolean('Active', default=True)
    is_urgent = fields.Boolean('Urgent Task')
    ```
  - **When to use**: Flags, toggles, yes/no questions
  - **Advanced**: Dùng trong decorations: `decoration-danger="is_urgent"`

- [ ] **Concept 7: Date và Datetime Fields - Temporal Data**
  - **Core explanation**: 
    - `fields.Date()` - Date only (YYYY-MM-DD), stored as `DATE` trong PostgreSQL
    - `fields.Datetime()` - Date + Time (UTC), stored as `TIMESTAMP` trong PostgreSQL
    - Odoo LUÔN lưu Datetime as UTC, convert sang user timezone khi hiển thị
  - **Syntax**:
    ```python
    from odoo import fields
    
    start_date = fields.Date('Start Date', default=fields.Date.today)
    due_date = fields.Datetime('Due Date', default=fields.Datetime.now)
    ```
  - **When to use**:
    - Date: Birthdays, deadlines (no time), reporting by day
    - Datetime: Timestamps, appointments, audit logs
  - **Gotcha**: `fields.Datetime.now()` (CALL function) vs `fields.Datetime.now` (function reference for default)
  - **Advanced**: Compare datetime: `record.due_date < fields.Datetime.now()` for overdue check

---

#### 🟢 Core Concepts: Binary & Image Fields

- [ ] **Concept 8: Binary Field - File Storage**
  - **Core explanation**: `fields.Binary()` stores file data as base64-encoded bytes. Used for ANY file type (PDF, images, CSV, etc.). Data stored directly IN database (hoặc filestore nếu config). Return type: bytes hoặc base64 string.
  - **Syntax**:
    ```python
    attachment = fields.Binary('File Attachment')
    pdf_report = fields.Binary('PDF Report', attachment=True)
    ```
  - **When to use**: Generic file uploads, non-image files, attachments
  - **Parameter `attachment=True`**: Store in filestore (external), not in DB column → better performance
  - **Gotcha**: Binary data VERY large → avoid load trong list views (performance killer)

- [ ] **Concept 9: Image Field - Special Binary with Auto-resize**
  - **Core explanation**: `fields.Image()` extends Binary specifically for images. Auto-resize images to `max_width`/`max_height` maintaining aspect ratio. Parameter `verify_resolution=True` (default) ensures max resolution limit (50MB pixels). If no limits → just use Binary.
  - **Syntax**:
    ```python
    # Source: odoo/fields.py L2163-2226
    class TaskProject(models.Model):
        _name = 'task.project'
        
        image = fields.Image('Cover Image', max_width=1920, max_height=1080)
        image_small = fields.Image('Thumbnail', max_width=128, max_height=128)
    ```
  - **When to use**: User avatars, product images, cover photos, thumbnails
  - **Advanced**: Tạo multiple image fields với different sizes (lazy loading pattern)
  - **Performance**: Odoo auto-resize on write() → save bandwidth + storage

- [ ] **Concept 10: Image Widget trong XML Views**
  - **Core explanation**: Widget `widget="image"` trong form view hiển thị image preview + upload button. Options: `preview_image` (field name for preview), `accepted_file_extensions` (filter file types). Kanban widget với `aside` tag cho side image layout.
  - **Syntax (Form View)**:
    ```xml
    <field name="image" widget="image" class="oe_avatar"/>
    <field name="image_small" widget="image" options="{'preview_image': 'image'}"/>
    ```
  - **Syntax (Kanban View)**:
    ```xml
    <kanban>
        <field name="image"/>
        <templates>
            <t t-name="card" class="flex-row">
                <aside>
                    <field name="image" widget="image" alt="Cover"/>
                </aside>
                <main>
                    <field name="name"/>
                </main>
            </t>
        </templates>
    </kanban>
    ```
  - **When to use**: ANY Binary/Image field trong UI
  - **Gotcha**: Image field MUST be declared before `<templates>` trong kanban

---

#### 🟢 Core Concepts: Selection Field & Attributes

- [ ] **Concept 11: Selection Field - Dropdown với Fixed Choices**
  - **Core explanation**: `fields.Selection()` cho exclusive choice from list. Parameter `selection` = list of tuples `(value, label)`. Value stored in DB, label hiển thị cho user. Validation auto - reject values not in list.
  - **Syntax**:
    ```python
    # Source: odoo/fields.py L2228-2435
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True)
    
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Priority', default='medium')
    ```
  - **Advanced - Dynamic selection**: Use method name or callable
    ```python
    def _get_states(self):
        return [('draft', 'Draft'), ('done', 'Done')]
    
    state = fields.Selection(selection='_get_states', string='State')
    ```
  - **When to use**: State machines, priorities, categories, enums
  - **Gotcha**: Changing selection values DANGEROUS - need migration + `ondelete` policy

- [ ] **Concept 12: Field Attributes - required, readonly, default**
  - **Core explanation**: 
    - `required=True`: Field MUST have value (database NOT NULL + UI validation)
    - `readonly=True`: UI cannot modify, but code CAN (security: không enforce ở ORM)
    - `default=<value>`: Default value for NEW records (static value hoặc lambda)
    - `string='Label'`: User-facing label (default = capitalized field name)
    - `help='tooltip'`: Tooltip text trong UI
  - **Syntax**:
    ```python
    name = fields.Char('Task Name', required=True, help='Enter a descriptive name')
    reference = fields.Char('Code', readonly=True, default='/')  # Auto-gen code
    priority = fields.Selection(..., default='medium')
    create_uid = fields.Many2one('res.users', default=lambda self: self.env.user)
    ```
  - **Default callable**: `default=lambda self: self.env.user.id` → dynamic default
  - **Gotcha**: `readonly` trong field definition ≠ `readonly` trong view XML (view override field)

- [ ] **Concept 13: store, copy, index Attributes**
  - **Core explanation**:
    - `store=True` (default): Store in database column
    - `store=False`: Computed fields without DB storage (pure compute)
    - `copy=True` (default): Copy value khi duplicate record
    - `copy=False`: Don't copy (for One2many, computed fields)
    - `index=True`: Create database index → faster search
  - **Syntax**:
    ```python
    name = fields.Char('Name', index=True)  # Indexed for fast search
    total = fields.Float(compute='_compute_total', store=True)  # Computed + stored
    child_ids = fields.One2many(..., copy=False)  # Don't duplicate children
    ```
  - **When to use index**: Fields in search domains, domain filters, group by
  - **Performance**: Index = faster read, slower write → trade-off

- [ ] **Concept 14: Widget Types cho Different Fields**
  - **Core explanation**: Widget attribute control field rendering trong UI. Different widgets for different field types.
  - **Common widgets**:
    - Binary/Image: `widget="image"`, `widget="pdf_viewer"`
    - Selection: `widget="radio"`, `widget="badge"`, `widget="priority"`
    - Many2many: `widget="many2many_tags"`
    - Char: `widget="email"`, `widget="phone"`, `widget="url"`
    - Float: `widget="percentage"`, `widget="monetary"`
  - **Syntax**:
    ```xml
    <field name="image" widget="image" class="oe_avatar"/>
    <field name="priority" widget="priority"/>
    <field name="tag_ids" widget="many2many_tags" options="{'color_field': 'color'}"/>
    ```
  - **When to use**: Enhance UX - better visual representation
  - **Advanced**: Custom widgets có thể define trong JavaScript

---

### 1.2 Source code cần đọc

| File | Class/Method | Line range | Focus |
|------|--------------|------------|-------|
| `odoo/fields.py` | `Field` | L116 - L1212 | Descriptor pattern, field initialization, base class |
| `odoo/fields.py` | `Char` | L1604 - L1659 | Basic string field implementation |
| `odoo/fields.py` | `Text` | L1662 - L1680 | Text field vs Char differences |
| `odoo/fields.py` | `Image` | L2163 - L2226 | Image field với auto-resize logic (`_image_process`) |
| `odoo/fields.py` | `Selection` | L2228 - L2435 | Selection validation, selection_add mechanism |

### 1.3 Kiến thức liên quan

| Odoo Concept | Tương đương Python/Framework | Khác biệt quan trọng |
|--------------|------------------------------|---------------------|
| Field descriptor | SQLAlchemy `Column`, Django Field | Odoo có cache layer phức tạp hơn |
| Char(size=100) | `VARCHAR(100)` trong SQL | Odoo 14+ không require size |
| Binary field base64 | Python `base64` module | Odoo auto-encode/decode |
| Image auto-resize | PIL/Pillow image resize | Odoo integrated, không cần manual code |
| Selection validation | Enum validation | Odoo raise ValidationError auto |

### 1.4 Advanced Topics

- **Image field multi-size pattern**: Define `image` (original), `image_medium` (512x512), `image_small` (128x128) for different contexts (form, kanban, list)
- **Field translation**: `translate=True` cho Char/Text fields → multi-language support
- **Company-dependent fields**: `company_dependent=True` → different values per company (stored as ir.property)
- **Field method-based defaults**: Use `@api.model` decorated method for complex default logic
- **Binary filestore**: `attachment=True` stores Binary/Image outside DB (in `filestore/` directory) → better performance
- **Selection `ondelete` policy**: When removing selection options, define `ondelete={'old_value': 'set null'}` to handle existing records

### 1.5 Common Gotchas & Mistakes

1. **Descriptor assignment gotcha**:
   - ❌ Wrong: `task.name = fields.Char()` (override descriptor!)
   - ✅ Correct: `task.name = 'New Name'` (assign value through descriptor)
   - Why: Field object là descriptor ở class level, không override ở instance level

2. **Image vs Binary confusion**:
   - ❌ Wrong: Use `fields.Binary()` cho images without validation
   - ✅ Correct: Use `fields.Image()` cho images → auto-resize + validation
   - Why: Image field có built-in protection và optimization

3. **Float default gotcha**:
   - ❌ Wrong: `hours = fields.Float(default=lambda self: self.compute_hours())`
   - ✅ Correct: Define default method properly hoặc use static value
   - Why: Default CANNOT call instance methods (no record yet)

4. **Selection validation**:
   - ❌ Wrong: Write value not in selection list → ValidationError
   - ✅ Correct: Always validate input against `field.get_values(env)`
   - Why: Selection auto-validates, but manual check needed for API inputs

5. **Binary data in list views**:
   - ❌ Wrong: Show Binary field trong tree view
   - ✅ Correct: Use `column_invisible="1"` or don't include
   - Why: Binary data large → slow list view performance

6. **Datetime timezone confusion**:
   - ❌ Wrong: Compare `record.due_date` với local datetime
   - ✅ Correct: Always compare với UTC datetime: `fields.Datetime.now()`
   - Why: Odoo stores ALL datetime as UTC

### 1.6 Context7 Research Summary

**Query 1**: `Odoo 14 comprehensive guide fields descriptors Binary field Image widget`
- Source: https://www.odoo.com/documentation/master/developer/reference/backend/orm
- Key insights:
  - Field types: Char (CharField), Integer, Float, Boolean, Date, Datetime, Text, Binary, Selection
  - Attributes: string, help, readonly, required, index, default, groups, company_dependent, copy, store
  - Image field with `max_width`/`max_height` auto-resize maintaining aspect ratio
  - `verify_resolution=True` ensures max resolution (50MB pixels)
- Best practice: Use Image instead of Binary for images → automatic validation and optimization

**Query 2**: `Odoo 14 Binary field image upload advanced patterns gotchas`
- Source: https://www.odoo.com/documentation/master/developer/reference/frontend/javascript_reference
- Key insights:
  - Image widget options: `preview_image`, `accepted_file_extensions`
  - Kanban side image layout: `<aside>` + `<main>` with `class="flex-row"` on card
  - Widget displays bin_size string ("6.5kb") and constructs image source URL
  - Binary fields support `attachment=True` for filestore storage (not DB)
- Gotcha: Fields used in QWeb templates MUST be declared before `<templates>`

---

## 💻 PHẦN 2: THỰC HÀNH

### 2.1 Bài tập code

**Exercise 1: Create task.project Model with Image** - [Basic warmup]

**Scenario**: Project là container cho tasks. Mỗi project cần cover image để visual identification.

**Requirements** (Chi tiết từng bước):

1. **Create file** `models/project.py`:
   - Path: `custom_addons/task_management/models/project.py`
   - Import: `from odoo import fields, models`

2. **Define model** `task.project` với EXACT fields:
   ```python
   class Project(models.Model):
       _name = "task.project"
       _description = "Project"
       
       name = fields.Char(string="Project Name", required=True, index=True)
       description = fields.Text(string="Description")
       image = fields.Image(string="Cover", max_width=1920, max_height=1080)
   ```

3. **Update** `models/__init__.py`:
   - Thêm dòng: `from . import project`

4. **Update** `security/ir.model.access.csv`:
   - Thêm dòng: `access_task_project_user,task.project access,model_task_project,base.group_user,1,1,1,1`

5. **KHÔNG update manifest** cho views - Exercise 2 sẽ làm!

**Testing Commands**:
```python
# Restart Odoo với: odoo-bin -u task_management
# Trong shell:
env['task.project']  # Expected: task.project()
env['task.project'].create({'name': 'Web Project'})  # Expected: task.project(1,)
```

**Expected Output**: 
- Model loads: `env['task.project']` returns `task.project()`
- Create works: `task.project(1,)` với ID

---

**Exercise 2: Create Views for task.project with Image Upload** - [Intermediate]

**Scenario**: Users cần upload cover image và manage projects từ UI.

**Requirements** (Chi tiết từng bước):

> [!IMPORTANT]
> Reference file `task_views.xml` để xem cấu trúc mẫu. Menu parent ID là `menu_task_root` (KHÔNG PHẢI menu_task_management).

**Step 1: Create file** `views/project_views.xml`
- Path: `custom_addons/task_management/views/project_views.xml`
- Root tag: `<odoo>...</odoo>`

**Step 2: Create Form View** (record model="ir.ui.view"):
- Record ID: `view_task_project_form`
- Field `name`: `task.project.form`
- Field `model`: `task.project`
- Structure bên trong `<form>` → `<sheet>` theo THỨ TỰ:

  a. **Image field** (top-right):
     ```xml
     <field name="image" widget="image" class="oe_avatar"/>
     ```
  
  b. **Title section**: 
     ```xml
     <div class="oe_title">
         <h1><field name="name" placeholder="Project Name..."/></h1>
     </div>
     ```
  
  c. **Description group**:
     ```xml
     <group>
         <field name="description" placeholder="Project description..."/>
     </group>
     ```

**Step 3: Create Tree View** (record model="ir.ui.view"):
- Record ID: `view_task_project_tree`
- Structure: `<tree>` với `<field name="name"/>`

**Step 4: Create Action** (record model="ir.actions.act_window"):
- Record ID: `action_task_project`
- Field `name`: `Projects`
- Field `res_model`: `task.project`
- Field `view_mode`: `tree,form`

**Step 5: Create Menu Item** (menuitem tag, KHÔNG PHẢI record):
```xml
<menuitem id="menu_task_project" 
          name="Projects"
          parent="menu_task_root"
          action="action_task_project"
          sequence="5"/>
```

**Step 6: Update Manifest**:
- Thêm `"views/project_views.xml"` vào `data` list trong `__manifest__.py`

**Testing**:
1. Restart Odoo: `odoo-bin -u task_management`
2. Navigate: Task Management → Projects
3. Click Create → Form view với image upload
4. Upload image → Displays as circular avatar (top-right)
5. Save → Project shows in tree view

**Expected Visual Result**:
- Form view có image circular (top-right)
- Name field lớn với placeholder
- Description field trong group

**Common Gotchas**:
- ❌ Menu parent `menu_task_management` → KHÔNG TỒN TẠI
- ✅ Menu parent `menu_task_root` → ĐÚNG
- ❌ Quên thêm vào manifest → Views không load
- ❌ Thiếu security access → AccessError

---

**Exercise 3: Enhance task.task with Deadline & Effort Fields** - [Production-level]

**Scenario**: Task management cần deadline tracking và effort estimation/tracking.

**Requirements**:
1. Add fields to `task.task` model (`models/task.py`):
   ```python
   due_date = fields.Datetime('Due Date', help='Task deadline')
   hours_estimated = fields.Float('Estimated Hours', digits=(6, 2))
   hours_spent = fields.Float('Hours Spent', digits=(6, 2))
   ```
2. Update `task_views.xml` form view:
   - Add `due_date` trong header (before state field)
   - Add group "Effort Tracking" với `hours_estimated` và `hours_spent`
3. Update tree view:
   - Add `due_date` column (with date widget)
   - Add decoration: `decoration-danger="due_date and due_date < context_today()"`
4. Restart Odoo + upgrade module

**Expected results**:
- Form view shows due_date field với datetime picker
- Tree view shows overdue tasks in RED color
- Hours fields accept decimal input (e.g., 2.5 hours)

**Constraints**:
- Hours fields should NOT accept negative values (hint for Day 8 - Constraints)
- Due date should be in future (validation logic later)

**Hints**:
- Context_today: Built-in context variable for today's date
- Datetime widget auto in form view for Datetime fields
- Decoration expressions have access to field values

---

**Exercise 4: Create Kanban View for Projects with Side Image** - [Advanced]

**Scenario**: Project kanban view với image ở side (modern layout pattern).

**Requirements**:
1. Create kanban view record trong `project_views.xml`
2. Declare fields: name, description, image
3. Card layout (QWeb template):
   - Root `<t t-name="card" class="flex-row">`
   - `<aside>`: Image field (widget="image", alt="Cover")
   - `<main class="ms-2">`: Name (bold, large) + Description (muted)
4. Group by default: không có (simple kanban list)
5. Update action view_mode: `"tree,kanban,form"`

**Expected behavior**:
- Projects hiển thị dạng cards với image bên trái
- Image missing → placeholder image
- Click card → open form view

**Challenges**:
- Ensure image field declared before `<templates>`
- Use correct Bootstrap classes: `flex-row`, `ms-2`, `fw-bold`, `text-muted`

**Self-assessment**:
- Does image display correctly?
- Is layout responsive wenn no image?
- Card clickable to open form?

---

**Exercise 5: Debug Field Definition Errors** - [Expert debugging]

**Scenario**: Common field definition bugs cần debug.

**Buggy Code 1** - Descriptor assignment:
```python
class Task(models.Model):
    _name = 'task.task'
    
    def reset_name(self):
        self.name = fields.Char('Reset')  # BUG!
```
- **Expected**: Method should reset name về empty string
- **Actual**: Overwrites field descriptor
- **Goal**: Identify bug, explain why wrong, fix it

**Buggy Code 2** - Image without max size:
```python
class Project(models.Model):
    _name = 'task.project'
    image = fields.Binary('Cover')  # ISSUE!
```
- **Problem**: Using Binary instead of Image for photos
- **Issue**: No auto-resize → huge files in DB
- **Goal**: Change to Image field với appropriate max_width/max_height

**Buggy Code 3** - Float comparison:
```python
if record.hours_spent == 2.5:  # GOTCHA!
    print("Exactly 2.5 hours")
```
- **Issue**: Float precision comparison
- **Expected**: May not match due to float precision
- **Goal**: Use rounding or threshold comparison

**Debugging approach**:
1. Read error messages carefully
2. Check field definition syntax against docs
3. Test in shell: `env['model'].fields_get(['field_name'])`

---

## ❓ PHẦN 3: KIỂM TRA KIẾN THỨC

### 3.1 Câu hỏi self-check

#### 🟢 Easy (Recall - Q1-3)

**Q1**: Field trong Odoo là gì? Descriptor hay value? Giá trị thực tế được stored ở đâu?

**Q2**: Liệt kê 5 basic field types và use case điển hình của mỗi type.

**Q3**: Syntax để tạo Image field với max size 800x600 là gì?

---

#### 🟡 Medium (Apply - Q4-7)

**Q4**: So sánh `fields.Char(size=100)` vs `fields.Text()`. Khi nào dùng Char, khi nào dùng Text?

**Q5**: Field attribute `readonly=True` khác gì với `attrs="{'readonly': [('state', '=', 'done')]}"` trong view XML?

**Q6**: Tại sao Image field có parameter `max_width`/`max_height`? Điều gì xảy ra khi user upload ảnh lớn hơn limit?

**Q7**: Code sau có bug gì? Làm sao fix?
```python
class Task(models.Model):
    _name = 'task.task'
    due_date = fields.Datetime('Deadline', default=fields.Datetime.now())  # BUG?
```

---

#### 🔴 Hard (Analyze - Q8-10)

**Q8**: **Scenario**: Bạn có field `image = fields.Binary('Photo')` trong model. User upload ảnh 5MB. Performance issue gì xảy ra trong list view? Làm sao optimize?

**Approach**:
- Identify: Binary data loaded TOÀN BỘ trong tree view
- Impact: Slow query + large memory
- Solution 1: Use `column_invisible="1"` hoặc remove from tree
- Solution 2: Change to `fields.Image()` + create thumbnail field
- Solution 3: `attachment=True` for filestore storage

**Q9**: **Debug**: User report error "Wrong value for task.task.priority: 'urgent'". Field definition:
```python
priority = fields.Selection([('low', 'Low'), ('high', 'High')], default='low')
```
Code trying to write:
```python
task.write({'priority': 'urgent'})
```
Explain error và fix approach.

**Q10**: **Design**: Requirements - Task cần track "Complexity" với 3 levels: Simple, Medium, Complex. Complexity affect estimated hours (Simple=2h, Medium=5h, Complex=10h). Design field structure và explain choice.

**Options**:
- Option A: `complexity = fields.Selection(...) + hours_estimated = fields.Float(readonly=True, compute=...)`
- Option B: `complexity = fields.Selection(...) + hours_estimated = fields.Float()` with onchange
- Trade-offs: Computed (auto) vs Manual (flexible)

---

### 3.2 Đáp án

<details>
<summary>Xem đáp án</summary>

#### Easy Answers:

**Q1**: 
- Answer: Field là **Python descriptor object**, KHÔNG phải value
- Giá trị thực tế stored trong **Odoo cache** (memory) và **database** (persistent)
- Why: Descriptor pattern cho phép control field access/assignment ở class level
- Related concept: Concept 1 - Field Descriptor

**Q2**:
1. `fields.Char()` - Short text (names, codes, emails)
2. `fields.Text()` - Long text (descriptions, notes)
3. `fields.Integer()` - Whole numbers (counts, sequences)
4. `fields.Float()` - Decimals (prices, hours, percentages)
5. `fields.Boolean()` - True/False flags (is_active, is_urgent)

**Q3**:
```python
image = fields.Image('Cover Photo', max_width=800, max_height=600)
```

---

#### Medium Answers:

**Q4**:
- **Char**:
  - Characteristics: Single-line, stored as VARCHAR, default limit ~256 chars
  - When to use: Names, codes, short text, display in lists
- **Text**:
  - Characteristics: Multi-line, stored as TEXT, no limit
  - When to use: Descriptions, long notes, không cần search thường xuyên
- Rule of thumb: Char cho display fields, Text cho content fields

**Q5**:
- **Field-level `readonly=True`**:
  - Affects: UI only (form view input disabled)
  - Does NOT prevent: Code-level writes `record.write({'field': value})`
- **View XML `attrs`**:
  - Affects: UI only, CONDITIONAL readonly
  - Dynamic: Based on other field values trong record
- Comparison: attrs flexible hơn (conditional), field readonly static

**Q6**:
- Purpose: Auto-resize images để save storage + bandwidth
- Process: Khi write, Odoo resize ảnh maintaining aspect ratio
- If uploaded 2000x1500 với max_width=800, max_height=600:
  - Result: Resize to 800x600 (aspect ratio maintained → might be 800x600 hoặc less)
- Performance: Smaller images = faster load trong UI

**Q7**:
- Bug: `default=fields.Datetime.now()` - CALL function MỘT LẦN khi define field
- Issue: Default value fix tại thời điểm module load, không dynamic cho mỗi record
- Fix: `default=fields.Datetime.now` (function reference, NO parentheses)
- Why: Odoo call function reference mỗi lần tạo record mới

---

#### Hard Answers:

**Q8**:
- **Problem**: Binary field trong tree view load TOÀN BỘ 5MB cho MỖI record hiển thị (80 records default = 400MB!)
- **Performance impact**:
  - Slow PostgreSQL query (select binary data)
  - Large memory usage trong Python
  - Slow rendering trong browser
- **Solutions**:
  1. **Remove from tree**: `column_invisible="1"` hoặc không include
  2. **Use Image + thumbnail**: Define `image_small = fields.Image(max_width=128)`, show trong tree instead
  3. **Filestore**: `attachment=True` → store outside DB (but still load issue)
  4. **Best practice**: NEVER show binary trong list views
- **Concepts used**: Binary field, Image field, Performance optimization

**Q9**:
- **Error explanation**:
  - Selection field validates: accepted values = ['low', 'high']
  - Code tries to write 'urgent' → NOT in selection list
  - Odoo raises `ValueError: Wrong value for task.task.priority: 'urgent'`
- **Root cause**: Missing 'urgent' option trong selection list
- **Fix approach**:
  1. Add 'urgent' to selection:
     ```python
     priority = fields.Selection([
         ('low', 'Low'), 
         ('high', 'High'),
         ('urgent', 'Urgent')  # Add this
     ], default='low')
     ```
  2. OR change write code to use valid value: `{'priority': 'high'}`
- **Prevention**: Always validate input against field definition trước khi write

**Q10**:
- **Option A - Computed hours** (RECOMMENDED for strict workflow):
  ```python
  complexity = fields.Selection([
      ('simple', 'Simple'),
      ('medium', 'Medium'),
      ('complex', 'Complex')
  ], required=True)
  
  hours_estimated = fields.Float(compute='_compute_hours', store=True, readonly=True)
  
  @api.depends('complexity')
  def _compute_hours(self):
      mapping = {'simple': 2, 'medium': 5, 'complex': 10}
      for task in self:
          task.hours_estimated = mapping.get(task.complexity, 0)
  ```
  - Pros: Auto-update, consistent, cannot manual override
  - Cons: Inflexible - không customize hours per task
  
- **Option B - Onchange** (RECOMMENDED for flexible workflow):
  ```python
  complexity = fields.Selection(...)
  hours_estimated = fields.Float('Estimated Hours')
  
  @api.onchange('complexity')
  def _onchange_complexity(self):
      mapping = {'simple': 2, 'medium': 5, 'complex': 10}
      if self.complexity:
          self.hours_estimated = mapping[self.complexity]
  ```
  - Pros: Auto-fill nhưng user can override
  - Cons: Only works in UI, not via code
  
- **Recommendation**: Option B for flexibility - users có thể adjust estimate based on specific task

</details>

---

## ✅ PHẦN 4: TIÊU CHÍ HOÀN THÀNH

| Tiêu chí | Đạt | Chưa đạt |
|----------|-----|----------|
| Giải thích được Field là descriptor với ví dụ | ✅ | ⬜ |
| Sử dụng được 8 basic field types đúng context | ✅ | ⬜ |
| Phân biệt được Binary vs Image và khi nào dùng | ✅ | ⬜ |
| Tạo thành công task.project với Image field | ✅ | ⬜ |
| Form view upload image hoạt động | ✅ | ⬜ |
| Enhance task.task với due_date + hours fields | ✅ | ⬜ |
| Hiểu field attributes: required, readonly, default | ✅ | ⬜ |
| Kanban với side image layout hoạt động | ✅ | ⬜ |
| Debug được 3 buggy field definitions | ✅ | ⬜ |
| Trả lời đúng ≥8/10 câu hỏi | ⬜ | 📝 (skipped for time) |

---

## 📝 PHẦN 5: ĐÁNH GIÁ (AI Mentor điền sau khi dạy)

### 5.1 Kết quả học tập
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Source code reading | 7 | Đọc fields.py (Field, Image, Selection) với hướng dẫn |
| Lý thuyết | 8 | Hiểu descriptor pattern, field types, Image vs Binary |
| Thực hành | 9 | Hoàn thành 5/5 exercises, Trello-style kanban với placeholder |
| Kiểm tra | 7 | Exercise 5: 2/3 bugs đúng, skip Questions section |
| **TỔNG** | **8/10** | **Tốt - Sẵn sàng Day 6** |

### 5.2 Key takeaways
> - Field là Python descriptor, KHÔNG BAO GIỜ gán `self.name = fields.Char()` trong method
> - Image field với max_width/max_height tự động resize, tránh bloat DB
> - Float comparison cần dùng `float_compare()` hoặc round
> - Kanban view cần declare fields trước `<templates>`
> - `t-if/t-else` pattern cho conditional rendering trong QWeb

### 5.3 Điểm cần cải thiện
> - Cần ôn lại Float precision gotcha (không biết ở Exercise 5)
> - Chưa làm Questions section (PHẦN 3) - nên tự ôn bài
> - Kanban image gặp nhiều lỗi do thiếu research - cần đọc source code nhiều hơn

### 5.4 Lưu ý cho Day 6
> - Day 6 sẽ EXTEND task.project và task.task (không tạo mới)
> - Cần thêm: `project_id = fields.Many2one('task.project')` vào task.task
> - Cần thêm: `task_ids = fields.One2many('task.task', 'project_id')` vào task.project
> - Module state đã sẵn sàng cho relational fields

---

## 🔗 CONTINUITY (Trainer phải đọc!)

### ⬅️ Ngày này builds on
- **Day 4**: Views (form, tree, kanban) - giờ add image widget vào views
- **Day 3**: Form view structure - enhance với image uploads
- **Day 2**: Recordset methods - field values accessed via descriptors
- **Day 1**: Model basics - fields define model schema

### ➡️ Ngày tiếp theo sẽ thêm (Day 6)
- **Relationships**: Many2one (task → project), One2many (project → tasks), Many2many (task ↔ tags)
- **Use today's fields**: project_id field linking task.task to task.project
- **Build on Image**: Display project cover trong task kanban cards
- **Relational widgets**: many2many_tags cho tag_ids field

### 🏁 Nhắc lại Roadmap Target

Sau 21 ngày, learner sẽ có module `task_management` **production-ready** với:
- **Full Models** (Day 5 completes basic field types!)
  - task.project → Container với image ✅
  - task.task → Enhanced với deadline tracking ✅
- Complete UI (Tree, Form, Kanban, Search)
- Security (ACL, Groups, Record Rules)
- Business Logic (Computed, Constraints, Workflows)
- Reports (QWeb PDF)

> ⚠️ **Trainer**: Day 5 là FOUNDATION day! Field system = core của Odoo models. User PHẢI hiểu descriptor pattern - ảnh hưởng đến ALL future concepts (computed fields, relational fields, etc.). Emphasize hands-on với image upload - practical skill cực quan trọng cho custom frontend work. Day 6 sẽ build relationships TRÊN fields đã define hôm nay!

---

## 📦 MODULE STATE TRACKER (After Day 5 Completion)

### Files Structure
```
custom_addons/task_management/
├── __init__.py
├── __manifest__.py (updated: +views/project_views.xml)
├── models/
│   ├── __init__.py (updated: +project import)
│   ├── task.py (updated: +due_date, +hours_estimated, +hours_spent)
│   └── project.py (NEW)
├── views/
│   ├── task_views.xml (updated: +hours fields, +due_date decoration)
│   └── project_views.xml (NEW)
└── security/
    └── ir.model.access.csv (updated: +task.project access)
```

### Models State

**task.task:**
- name (Char, required)
- description (Text, required)
- state (Selection: draft/in_progress/done)
- priority (Selection: low/medium/high)
- due_date (Datetime) ← NEW Day 5
- hours_estimated (Float, digits=(6,2)) ← NEW Day 5
- hours_spent (Float, digits=(6,2)) ← NEW Day 5

**task.project:** ← NEW MODEL Day 5
- name (Char, required, index)
- description (Text)
- image (Image, max 1920x1080)

### Views State

**task_views.xml:**
- Tree view: name, state, priority, due_date with overdue decoration
- Form view: +Effort Tracking group with hours fields
- Kanban view: basic card layout
- Search view: filters by state/priority

**project_views.xml:** ← NEW Day 5
- Form view: image avatar, title, description
- Tree view: name column
- Action: action_task_project
- Menu: Task Management → Projects

### Security State
- task.task: full access for base.group_user
- task.project: full access for base.group_user

---

### ➡️ Day 6 INPUT (What Day 6 will BUILD ON)

Day 6 will **EXTEND** (not recreate) these models:

**EXTEND task.project:**
- Add: `task_ids = fields.One2many('task.task', 'project_id')`
- Add: `task_count = fields.Integer(compute='_compute_task_count')`

**EXTEND task.task:**
- Add: `project_id = fields.Many2one('task.project', 'Project')`
- Add: `tag_ids = fields.Many2many('task.tag')`
- Add: `assigned_user_id = fields.Many2one('res.users')`

**CREATE task.tag:** (New model)
- name (Char)
- color (Integer)

