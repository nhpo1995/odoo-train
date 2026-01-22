# 📦 Task Management Module - Specification

> **Purpose**: Blueprint của module CUỐI CÙNG (Day 21 target).  
> **Rule**: File này chỉ chứa TARGET. ACTUAL code được đọc trực tiếp từ source files.

---

## 🎯 Module Overview

| Property | Value |
|----------|-------|
| **Module name** | `task_management` |
| **Path** | `custom_addons/task_management/` |
| **Dependencies** | `base`, `mail` (Day 15+) |

---

## 📊 TARGET Models (Day 21)

### task.project

| Field | Type | Params | Day |
|-------|------|--------|-----|
| name | Char | required, index | 5 |
| description | Text | required | 5 |
| image | Image | max 1920x1080 | 5 |
| task_ids | One2many | → task.task.project_id | 6 |
| manager_id | Many2one | → res.users | 6 |
| task_count | Integer | compute | 7 |
| total_revenue | Float | compute, read_group | 9 |
| total_hours | Float | compute, read_group | 9 |
| company_id | Many2one | → res.company | 13 |
| _inherit | - | mail.thread, mail.activity.mixin | 15+ |

### task.task

| Field | Type | Params | Day |
|-------|------|--------|-----|
| name | Char | required | 1-5 |
| description | Text | required | 1-5 |
| state | Selection | draft/in_progress/done, group_expand | 1-5 |
| priority | Selection | low/medium/high | 1-5 |
| due_date | Datetime | - | 5 |
| hours_estimated | Float | digits=(6,2) | 5 |
| hours_spent | Float | digits=(6,2) | 5 |
| color | Integer | - | 5 |
| project_id | Many2one | → task.project, ondelete=cascade, index | 6 |
| assigned_user_id | Many2one | → res.users, default=env.user | 6 |
| tag_ids | Many2many | → task.tag | 6 |
| has_urgent_tags | Boolean | compute | 7 |
| is_overdue | Boolean | compute | 7 |
| hours_remaining | Float | compute | 7 |
| progress | Float | compute | 7 |
| amount | Float | digits=(16,2) | 9 |
| parent_id | Many2one | → task.task (self-ref) | 14 |
| child_ids | One2many | → task.task.parent_id | 14 |
| subtask_count | Integer | compute | 14 |
| company_id | Many2one | → res.company | 13 |
| _inherit | - | mail.thread, mail.activity.mixin | 15+ |

### task.tag (Day 6)

| Field | Type | Params |
|-------|------|--------|
| name | Char | required |
| color | Integer | default=0 |

### task.state.wizard (Day 9)

| Field | Type | Params |
|-------|------|--------|
| new_state | Selection | required |
| action_apply() | method | bulk update |

---

## 🎨 TARGET Views

| Model | View | Key Features |
|-------|------|--------------|
| task.task | Form | notebook, widgets, attrs |
| task.task | Tree | decorations, is_overdue |
| task.task | Kanban | color picker, tags, priority |
| task.task | Search | filters, group by |
| task.task | Calendar | due_date, assigned_user_id | Day 10 |
| task.project | Form | O2M tab, image widget |
| task.project | Kanban | cover image, task_count badge |
| task.tag | Form/Tree | basic CRUD |

---

## 🔐 TARGET Security (Day 11-13)

| Type | Name | Description |
|------|------|-------------|
| Group | group_manager | Full CRUD |
| Group | group_member | Limited access |
| Rule | member_tasks | See assigned/unassigned only |
| Rule | company_rule | Multi-company isolation |

---

## ⚙️ Features by Day

| Day | Features | Models |
|-----|----------|--------|
| 1-4 | Basic CRUD, Views | task.task |
| 5 | Fields, Binary/Image | task.task, task.project |
| **6** | **Relationships (M2O, O2M, M2M)** | **task.task, task.project, task.tag** |
| 7 | Computed fields | task.task, task.project |
| 8 | Constraints, Statusbar | task.task |
| 9 | Onchange, Wizard, amount, total_revenue | task.state.wizard, task.task, task.project |
| 10 | Context, Domain, Report, Calendar view, frontend assets (CSS/JS, QWeb inheritance) | task.task, task.project |
| 11-13 | Security (Groups, Rules, Multi-company) | All |
| 14 | Subtasks (parent_id, child_ids, subtask_count) | task.task |
| 15-17 | Inheritance, Debug, Chatter | res.partner extension |
| 18 | HTTP Controllers | API |
| 19 | Scheduled Actions | ir.cron |
| 20-21 | Review, Polish | All |

---

## � TARGET File Structure

```
task_management/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── task.py
│   ├── project.py
│   ├── tag.py              # Day 6
│   └── wizard.py           # Day 9
├── views/
│   ├── task_views.xml
│   ├── project_views.xml
│   ├── tag_views.xml       # Day 6
│   └── wizard_views.xml    # Day 9
├── security/
│   ├── ir.model.access.csv
│   ├── security.xml        # Day 11+ (groups, rules)
├── report/                  # Day 10
│   ├── task_report.xml
│   └── task_report_template.xml
├── static/                  # Day 10
│   └── src/
│       ├── css/
│       │   └── task_kanban.css
│       └── js/
│           └── task_debug.js
└── controllers/             # Day 18
    └── main.py
```

---

## 📦 __manifest__.py (Day 10 assets)

- Register assets in `web.assets_backend`
  - `task_management/static/src/css/task_kanban.css`
  - `task_management/static/src/js/task_debug.js`

Example snippet:
```python
'assets': {
    'web.assets_backend': [
        'task_management/static/src/css/task_kanban.css',
        'task_management/static/src/js/task_debug.js',
    ],
},
```

---

## 📝 Notes for Planner/Trainer

### Workflow Rules:
1. **KHÔNG duplicate code vào file này** - Đọc ACTUAL từ source files trực tiếp
2. **TARGET là fixed** - Không thay đổi trừ khi có lý do đặc biệt
3. **Lesson plan chứa ACTUAL snapshot** - Trong section "📍 ACTUAL Current State"
4. **Compare bằng cách đọc cả 2** - Spec + Source files

### Khi tạo Lesson Plan:
```
1. Đọc module_spec.md → Biết TARGET cho day hôm đó
2. Đọc source files → Biết ACTUAL hiện tại
3. So sánh → Xác định GAP
4. Ghi ACTUAL snapshot vào lesson plan (concise summary only)
```

---

## � Revision History

| Date | Change |
|------|--------|
| 2026-01-19 | Simplified structure - TARGET only, removed ACTUAL |
| 2026-01-22 | Added: amount (Day 9), total_revenue/total_hours (Day 9), subtasks (Day 14); Split Security Day 11-13, Subtasks Day 14 |
| 2026-01-22 | Added frontend assets for Day 10 (CSS/JS + QWeb inheritance) |
| 2026-01-22 | Added __manifest__.py assets registration notes |
| 2026-01-22 | Synced spec with actual: task.task description required, project_id index, has_urgent_tags field |
