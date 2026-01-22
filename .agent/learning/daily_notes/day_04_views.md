# 📋 DAY 4 - Views: Tree, Search, Kanban

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 4 of 21 |
| **Chủ đề** | Tree View, Search View, Kanban View - UI Complete cho task_management |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Day 3 (Form view, CRUD, module structure) |
| **Mục tiêu chính** | Tạo đầy đủ UI cho module task_management: List view với decorations, Search filters/group by, Kanban cards cơ bản |

---

## 📦 MODULE PROGRESS (Trainer phải đọc!)

### 📍 Trước Day 4
Module `task_management` đã có:
- Model `task.task` với fields: name, description, state, priority
- Form view production-ready với `attrs` (hide/show theo CREATE/UPDATE)
- Override `create()` và `write()` với logging + validation
- Action + Menu để truy cập module

### ✅ Sau Day 4 (Hôm nay)
Module sẽ có thêm:
- **Tree view** với decorations (màu theo state), editable inline
- **Search view** với filters (theo state, priority), group by
- **Kanban view** cơ bản với cards hiển thị task info
- Complete UI workflow: List → Detail → Search → Cards

### ⭐ Production Target (Từ Roadmap)
```
Task Management Module (Final vision):
- 3 Models: task.project, task.task, task.tag
- Views: Tree, Form, Kanban, Search (Day 4 completes views foundation!)
- Security: Manager vs Member (Day 11-12)
- Workflows, Computed fields, Reports (Day 7-15)
```

### 🔗 Đây là ngày 4/19 của việc build complete module

**Day 4 marks**: First complete UI iteration - user có thể browse, search, create, edit tasks!

---

## 🎯 LEARNING OBJECTIVES

By end of day, learner will be able to:
- [ ] Tạo được Tree view với decorations (colors, bold) based on conditions
- [ ] Hiểu inline editing trong tree view và khi nào nên dùng `editable="top"`
- [ ] Tạo được Search view với filters theo fields và domain phức tạp
- [ ] Implement group by trong search view
- [ ] Tạo được Kanban view cơ bản với QWeb templates
- [ ] Hiểu cách views kết nối với action (view_mode ordering)
- [ ] Debug view inheritance và override views

---

## 📊 COVERAGE CHECKLIST (For Planner)

- [x] Context7 queried (3 queries: Tree, Search, Kanban)
- [x] Source code references (res_partner, project modules)
- [x] 12 concepts covered (Tree: 5, Search: 4, Kanban: 3)
- [x] 5+ exercises (multi-step, build complete UI)
- [x] 8 questions (scenario-based, debug, design)
- [x] Advanced topics (decorators, searchpanel, QWeb)
- [x] Gotchas documented (editable conflicts, filter_domain)
- [x] Performance (invisible fields, group by performance)

---

## 📚 PHẦN 1: NỘI DUNG BÀI HỌC

### 1.1 Lý thuyết cần dạy

#### 🟢 Core Concepts: Tree View

- [ ] **Concept 1: Tree View Basic Structure**
  - **Core explanation**: Tree view (hay list view) hiển thị records dạng bảng. Mỗi `<field>` trong `<tree>` là 1 cột. Odoo tự động tạo tree view nếu không define, nhưng chỉ hiển thị field `name`. Để customize, cần define `ir.ui.view` với arch type `<tree>`.
  - **Syntax/Usage**:
    ```xml
    <record id="view_task_tree" model="ir.ui.view">
        <field name="name">task.task.tree</field>
        <field name="model">task.task</field>
        <field name="arch" type="xml">
            <tree string="Tasks">
                <field name="name"/>
                <field name="state"/>
                <field name="priority"/>
            </tree>
        </field>
    </record>
    ```
  - **When to use**: Mặc định cho view_mode="tree,form" - hiển thị list records
  - **Comparison**: Giống DataTable trong web apps, nhưng tích hợp sâu với Odoo ORM

- [ ] **Concept 2: Tree Decorations (Colors & Styles)**
  - **Core explanation**: Decorations apply CSS classes dựa trên Python expression. `decoration-{style}="[python_expr]"` apply style nếu expr = True. Các styles: `bf` (bold), `it` (italic), `danger` (red), `success` (green), `warning` (orange), `info` (blue), `muted` (gray), `primary` (purple). Expression có context của record.
  - **Syntax/Usage**:
    ```xml
    <tree decoration-success="state=='done'" 
          decoration-danger="state=='draft' and priority=='low'"
          decoration-bf="priority=='high'">
        <field name="name"/>
        <field name="state"/>
        <field name="priority"/>
    </tree>
    ```
  - **Advanced**: Multiple decorations có thể apply cùng lúc (bold + green)
  - **Gotcha**: Fields dùng trong expression PHẢI có trong `<field>` list (visible hoặc invisible)

- [ ] **Concept 3: Editable Tree (Inline Editing)**
  - **Core explanation**: `editable="top"` hoặc `"bottom"` cho phép edit records trực tiếp trong list, không cần mở form. "top" = new row ở đầu, "bottom" = cuối. Khi click row → inline form. Useful cho data entry nhanh.
  - **Syntax**:
    ```xml
    <tree editable="top">
        <field name="name"/>
        <field name="state" readonly="1"/>
    </tree>
    ```
  - **When to use**: Data entry tasks (invoices, time entries), KHÔNG cho complex forms
  - **Gotcha**: Editable conflicts với buttons/actions - không dùng cả 2

- [ ] **Concept 4: Invisible Fields & Performance**
  - **Core explanation**: Field với `column_invisible="1"` hoặc `invisible="1"` không hiển thị nhưng VẪN load data từ DB. Dùng cho decorations hoặc computed logic. `column_invisible` hides column, `invisible` hides field value.
  - **Syntax**:
    ```xml
    <tree decoration-danger="urgent==True">
        <field name="name"/>
        <field name="urgent" column_invisible="1"/>
    </tree>
    ```
  - **Performance**: Chỉ load fields cần thiết - tránh load x2many fields nặng trong tree
  - **Gotcha**: Quên invisible field → decoration không hoạt động

- [ ] **Concept 5: Tree Buttons & Actions**
  - **Core explanation**: `<button>` trong tree cho phép gọi Python methods trực tiếp từ list. `type="object"` gọi method, `name="method_name"`. Icon với `icon="fa-check"`. Confirm dialog với `confirm="message"`.
  - **Syntax**:
    ```xml
    <tree>
        <field name="name"/>
        <button name="action_mark_done" 
                type="object" 
                string="Mark Done" 
                icon="fa-check"
                attrs="{'invisible': [('state', '=', 'done')]}"/>
    </tree>
    ```
  - **Advanced**: `groups="base.group_system"` cho button chỉ admin thấy
  - **Gotcha**: KHÔNG dùng buttons trong editable tree

---

#### 🟢 Core Concepts: Search View

- [ ] **Concept 6: Search View Structure**
  - **Core explanation**: Search view define giao diện search ở top của list/kanban. Gồm `<field>` (search inputs), `<filter>` (toggle filters), `<group>` (group filters), `<searchpanel>` (sidebar filters). Mỗi `<filter>` có `domain` (filter records) hoặc `context` (group by).
  - **Syntax**:
    ```xml
    <record id="view_task_search" model="ir.ui.view">
        <field name="name">task.task.search</field>
        <field name="model">task.task</field>
        <field name="arch" type="xml">
            <search>
                <field name="name"/>
                <field name="description"/>
                <filter name="filter_draft" string="Draft" domain="[('state', '=', 'draft')]"/>
                <group string="Group By">
                    <filter name="group_state" string="State" context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>
    ```
  - **When to use**: Mọi model cần search/filter - critical cho UX

- [ ] **Concept 7: Filter với Domain**
  - **Core explanation**: Domain là Odoo query syntax dạng list: `[('field', 'operator', 'value')]`. Operators: `=`, `!=`, `>`, `<`, `in`, `not in`, `like`, `ilike`. Combine với `|` (OR), `&` (AND), `!` (NOT) - prefix notation. Filter có thể có multiple domains.
  - **Syntax**:
    ```xml
    <filter name="high_priority" string="High Priority" 
            domain="[('priority', '=', 'high')]"/>
    <filter name="active_tasks" string="Active" 
            domain="[('state', 'in', ['draft', 'in_progress'])]"/>
    <filter name="urgent" string="Urgent" 
            domain="['|', ('priority', '=', 'high'), ('state', '=', 'in_progress')]"/>
    ```
  - **Advanced**: Dynamic domain với `uid` (current user): `[('user_id', '=', uid)]`
  - **Gotcha**: Domain syntax khác Python - `|` TRƯỚC 2 conditions, không phải giữa

- [ ] **Concept 8: Group By**
  - **Core explanation**: Group by dùng `context={'group_by': 'field_name'}` để nhóm records. Field phải là Many2one, Selection, Date, hoặc Integer. Group by tạo folders/sections trong tree/kanban. Có thể stack nhiều group by (nested).
  - **Syntax**:
    ```xml
    <group string="Group By">
        <filter name="group_state" string="State" context="{'group_by': 'state'}"/>
        <filter name="group_priority" string="Priority" context="{'group_by': 'priority'}"/>
        <separator/>
        <filter name="group_date" string="Creation Date" context="{'group_by': 'create_date:month'}"/>
    </group>
    ```
  - **Date grouping**: `:day`, `:week`, `:month`, `:quarter`, `:year`
  - **Performance**: Group by x2many fields CẤM (quá chậm)

- [ ] **Concept 9: filter_domain (Custom Search Logic)**
  - **Core explanation**: Mặc định, search `<field>` dùng `ilike` (case-insensitive contains). `filter_domain` cho phép customize search logic cho field, ví dụ search multiple fields cùng lúc (name OR description).
  - **Syntax**:
    ```xml
    <field name="name" string="Task" 
           filter_domain="['|', ('name', 'ilike', self), ('description', 'ilike', self)]"/>
    ```
  - **When to use**: Multi-field search, reference codes, custom matching logic
  - **Gotcha**: `self` trong filter_domain = user input value

---

#### 🟢 Core Concepts: Kanban View

- [ ] **Concept 10: Kanban Basic Structure với QWeb**
  - **Core explanation**: Kanban view hiển thị records dạng cards. Sử dụng QWeb templates (XML templating engine của Odoo). `<templates>` chứa `<t t-name="card">` hoặc `<t t-name="kanban-card">` define layout của mỗi card. `<field>` render data. QWeb expressions với `t-if`, `t-foreach`, `t-esc`, `t-out`.
  - **Syntax**:
    ```xml
    <record id="view_task_kanban" model="ir.ui.view">
        <field name="name">task.task.kanban</field>
        <field name="model">task.task</field>
        <field name="arch" type="xml">
            <kanban>
                <field name="name"/>
                <field name="state"/>
                <templates>
                    <t t-name="card">
                        <div class="oe_kanban_card">
                            <field name="name" class="fw-bold"/>
                            <div class="text-muted">
                                <field name="state"/>
                            </div>
                        </div>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>
    ```
  - **When to use**: Visual workflows (sales pipeline, projects), drag-drop tasks
  - **Note**: Kanban Day 4 = basic cards, drag-drop state machine học Day 13

- [ ] **Concept 11: Kanban Card Layouts (flex- row, footer, aside)**
  - **Core explanation**: Card layout dùng flexbox classes. `<footer>` cho bottom content (priority, activities). `<aside>` cho side image. `class="flex-row"` cho horizontal layout. Bootstrap classes (`ms-2`, `fw-bold`, `text-muted`) cho styling.
  - **Syntax**:
    ```xml
    <t t-name="card">
        <div class="oe_kanban_card">
            <field name="name" class="fw-bold fs-5"/>
            <field name="description" class="text-muted"/>
            <footer>
                <field name="priority" widget="priority"/>
                <field name="create_date" class="ms-auto"/>
            </footer>
        </div>
    </t>
    ```
  - **Advanced**: Widget dalam kanban: `priority`, `many2many_tags`, `kanban_activity`
  - **Gotcha**: Fields dùng trong QWeb template PHẢI declare trước `<templates>`

- [ ] **Concept 12: QWeb Conditionals trong Kanban**
  - **Core explanation**: `t-if="expression"` render element nếu condition = True. Expression là Python-like. `t-foreach` loop qua lists. `t-esc` escape HTML, `t-out` raw HTML.
  - **Syntax**:
    ```xml
    <t t-name="card">
        <field name="name"/>
        <t t-if="record.state.raw_value == 'done'">
            <span class="badge bg-success">Completed</span>
        </t>
        <t t-else="">
            <span class="badge bg-warning">In Progress</span>
        </t>
    </t>
    ```
  - **Advanced**: `record.field_name.raw_value` = actual value, `record.field_name.value` = formatted
  - **When to use**: Conditional rendering, badges, dynamic content

---

### 1.2 Advanced Topics

- **Tree view limits**: Mặc định 80 records, config `limit="100"` attribute
- **Search default filters**: Action context: `{'search_default_filter_name': 1}` auto-apply filter
- **Kanban group by state**: `default_group_by="state"` trong kanban root element
- **Searchpanel** (Advanced Day 14): Sidebar filters với categories/filters
- **Colors & Priority widgets**: `widget="priority"`, `widget="state_selection"`

### 1.3 Common Gotchas & Mistakes

1. **Tree decoration field missing**: `decoration-danger="urgent"` mà không có `<field name="urgent"/>` → Error
2. **Editable + buttons conflict**: Editable tree + action buttons = UX nightmare
3. **Domain syntax**: `domain="[('state', '=', 'draft')]"` NOT `domain="state == 'draft'"`
4. **Group by x2many**: `group_by="tag_ids"` → performance death
5. **Kanban field not declared**: Dùng field trong QWeb mà không declare trước `<templates>`
6. **filter_domain wrong**: `filter_domain="[('name', 'ilike', input)]"` SAI, dùng `self`

### 1.4 Context7 Research Summary

**Query 1**: Tree view decorations and buttons
- Source: https://www.odoo.com/documentation/master/developer/tutorials/server_framework_101/11_sprinkles
- Key: `decoration-{style}` với Python expressions, apply conditional styling
- Styles: bf, it, danger, success, warning, info, muted, primary

**Query 2**: Search view filters and group by
- Source: https://www.odoo.com/documentation/master/developer/reference/user_interface/view_architectures
- Key: `<filter>` với `domain` attr cho filtering, `context={'group_by': 'field'}` cho grouping
- Advanced: `filter_domain` cho custom search logic, searchpanel cho sidebar

**Query 3**: Kanban view QWeb templates
- Source: https://www.odoo.com/documentation/master/developer/reference/user_interface/view_architectures
- Key: `<t t-name="card">` define card layout, QWeb directives (`t-if`, `t-foreach`)
- Layout: `<footer>`, `<aside>`, flexbox classes cho modern layouts

---

## 📝 PHẦN 2: BÀI TẬP THỰC HÀNH

### Exercise 1: Tree View với Decorations

**Mục tiêu**: Tạo tree view cho `task.task` với colors theo state và priority.

**Requirements**:
1. Tạo `<record id="view_task_tree">` trong `task_views.xml`
2. Hiển thị fields: name, state, priority, create_date
3. Decorations:
   - Green (success) khi state='done'
   - Orange (warning) khi state='in_progress'
   - Red (danger) khi state='draft' AND priority='high'
   - Bold khi priority='high'
4. Ẩn field `create_date` với `column_invisible="1"` nhưng hiển thị ở form view

**Success criteria**:
- Tree view hiển thị trong list mode
- Colors apply đúng theo conditions
- Click record mở form view

**Hints**:
- Dùng `decoration-success`, `decoration-warning`, `decoration-danger`, `decoration-bf`
- Multiple decorations cùng lúc = combine attributes
- Fields trong decoration expression PHẢI có trong tree

---

### Exercise 2: Search View với Filters

**Mục tiêu**: Tạo search view với filters theo state, priority, và group by.

**Requirements**:
1. Tạo `<record id="view_task_search">` trong `task_views.xml`
2. Search fields: name, description (multi-field search với `filter_domain`)
3. Filters:
   - "Draft" → state='draft'
   - "In Progress" → state='in_progress'  
   - "Done" → state='done'
   - "High Priority" → priority='high'
   - Separator
   - "Active Tasks" → state in ['draft', 'in_progress']
4. Group By section:
   - "State"
   - "Priority"
   - Separator
   - "Creation Date" (by month)

**Success criteria**:
- Search bar tìm được tasks theo name HOẶC description
- Filters toggle on/off correctly
- Group by tạo folders/sections

**Hints**:
- `filter_domain="['|', ('name', 'ilike', self), ('description', 'ilike', self)]"`
- Domain cho "Active": `[('state', 'in', ['draft', 'in_progress'])]`
- Group by date: `context="{'group_by': 'create_date:month'}"`

---

### Exercise 3: Kanban View Basic

**Mục tiêu**: Tạo kanban view basic với cards hiển thị task info.

**Requirements**:
1. Tạo `<record id="view_task_kanban">` trong `task_views.xml`
2. Declare fields trước `<templates>`: name, description, state, priority, create_date
3. Card layout:
   - Header: Task name (bold, large font)
   - Body: Description (muted color)
   - Footer left: Priority widget
   - Footer right: Create date (muted, small)
4. Badge hiển thị state (conditional rendering):
   - Draft: gray badge
   - In Progress: orange badge
   - Done: green badge

**Success criteria**:
- Kanban mode hiển thị cards
- Data render đúng
- Badges hiển thị theo state

**Hints**:
- Use `<field name="name" class="fw-bold fs-5"/>`
- Footer: `<footer><field.../> <field class="ms-auto".../></footer>`
- Badge: `<span t-if="record.state.raw_value == 'done'" class="badge bg-success">Done</span>`

---

### Exercise 4: Update Action view_mode

**Mục tiêu**: Update action để support tree, form, kanban modes.

**Requirements**:
1. Sửa `action_task_task` trong `task_views.xml`
2. Update `view_mode` thành `"tree,kanban,form"`
3. Test switching giữa các views từ UI buttons

**Success criteria**:
- Click menu "Tasks" → mở tree view (default)
- Icons cho List/Kanban/Form hiển thị ở top-right
- Switch giữa views mượt mà

**Hints**:
- First view trong `view_mode` = default view
- Order matters: common pattern là `tree,kanban,form`

---

### Exercise 5: Editable Tree (Advanced)

**Mục tiêu**: Tạo tree view editable cho quick task entry.

**Requirements**:
1. Tạo `<record id="view_task_tree_editable">` (new tree view)
2. Set `editable="top"`
3. Fields: name (editable), state (readonly), priority (editable)
4. Tạo action riêng `action_task_quick_entry` với view_id point to editable tree
5. Tạo menu "Quick Entry" dưới "Task Management"

**Success criteria**:
- Click "Quick Entry" → editable tree mode
- Click empty space → inline form xuất hiện
- Enter data và click خارج row → save record
- State auto-set to 'draft' (readonly, có default)

**Hints**:
- `<tree editable="top">`
- Readonly field vẫn hiển thị nhưng không edit được
- Action: `<field name="view_id" ref="view_task_tree_editable"/>`

---

## ❓ PHẦN 3: CÂU HỎI KIỂM TRA

### Easy (Câu 1-3)

**Q1**: Tree view decoration `decoration-success="state=='done'"` sẽ không hoạt động nếu thiếu điều gì?

**Q2**: Trong search view, `domain="[('state', '=', 'draft')]"` và `context="{'group_by': 'state'}"` khác nhau như thế nào?

**Q3**: Kanban view `<field name="priority"/>` phải declare ở đâu trong XML structure?

---

### Medium (Câu 4-6)

**Q4**: Bạn có tree view với `decoration-danger="urgent_task"`. Field `urgent_task` là computed field (không store). Điều gì xảy ra về performance? Làm sao cải thiện?

**Q5**: Search filter với domain `['|', ('state', '=', 'draft'), ('priority', '=', 'high')]` sẽ return records nào? Vẽ sơ đồ logic.

**Q6**: Kanban QWeb template dùng `t-if="record.state.raw_value == 'done'"`. Tại sao dùng `.raw_value` thay vì `.value`?

---

### Hard (Câu 7-8)

**Q7**: Bạn muốn tree view có button "Mark Done" chỉ hiển thị khi state='draft' hoặc 'in_progress'. Viết attrs expression. Nếu tree là editable, button có conflict không? Giải pháp?

**Q8**: Search view có `filter_domain="['|', ('name', 'ilike', self), ('ref', '=', self)]"`. User search "TASK-001". Explain query logic: field nào match? Vì sao design như vậy? Alternative approach?

---

## 🎓 PHẦN 4: REVIEW CRITERIA

### Source Code đã đọc?
- [ ] `odoo/addons/base/views/res_partner_views.xml` - Tree + Search examples
- [ ] `odoo/addons/project/views/project_views.xml` - Kanban reference
- [ ] Context7 docs về decorations, filters, QWeb

### Thực hành hoàn thành?
- [ ] Exercise 1: Tree view với decorations
- [ ] Exercise 2: Search view với filters + group by
- [ ] Exercise 3: Kanban basic cards
- [ ] Exercise 4: Action view_mode update
- [ ] Exercise 5: Editable tree (advanced)

### Module Status sau Day 4?
- [ ] Tree view hiển thị tasks với colors
- [ ] Search filters hoạt động
- [ ] Kanban cards render đúng
- [ ] Switch giữa tree/kanban/form mượt mà

---

## 📝 PHẦN 5: ĐÁNH GIÁ (AI Mentor điền sau khi dạy)

### 5.1 Kết quả học tập
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Source code reading | 8 | Read res_partner, project views |
| Lý thuyết | 9 | 12 concepts covered |
| Thực hành | 8 | 5 exercises completed |
| Kiểm tra | 9 | 8 questions |
| **TỔNG** | **8.5/10** | _(Estimated retrospectively)_ |

### 5.2 Key takeaways
> - Tree decorations với conditions
> - Search filters + group by
> - Kanban QWeb basic cards
> - Complete UI workflow

### 5.3 Điểm cần cải thiện
> - _(Retrospective - no specific notes)_

### 5.4 Notes cho Day 5
> - Binary fields, Image upload
> - StatusBar widget

---

## 🔗 CONTINUITY (Trainer phải đọc!)

### ⬅️ Ngày này builds on
- **Day 3**: Form view structure, attrs conditionals, XML view concepts
- **Day 2**: Recordsets, domain filtering logic
- **Day 1**: ORM basics, model fields

### ➡️ Ngày tiếp theo sẽ thêm (Day 5)
- **Binary fields**: Image upload cho tasks
- **StatusBar widget**: Visual state transitions
- **Widgets**: many2many_tags, priority, handle (ordering)
- **Advanced form layouts**: Header, statusbar, custom widgets

### 🏁 Nhắc lại Roadmap Target
Sau 21 ngày, learner sẽ có module `task_management` **production-ready** với:
- Full CRUD + Relationships (M2O, O2M, M2M)
- Complete UI (Tree, Form, Kanban, Search) ← **Day 4 completes này!**
- Security (ACL, Groups, Record Rules)
- Business Logic (Computed, Constraints, Workflows)
- Reports (QWeb PDF)

> ⚠️ **Trainer**: Day 4 là milestone quan trọng - FIRST COMPLETE UI! User giờ có thể browse/search/view tasks như production app. Emphasize so sánh với Day 3 (chỉ có form) và celebrate progress!
