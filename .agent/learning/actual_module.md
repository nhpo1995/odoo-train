# 📍 Actual Module State

> **Purpose**: Snapshot của code HIỆN TẠI. Trainer update cuối mỗi ngày.  
> **Last Updated**: 2026-01-24 (After Day 8)

---

## 📊 Current Models

### task.task

| Field | Type | Status | Notes |
|-------|------|--------|-------|
| name | Char(required) | ✅ | |
| description | Text(required) | ✅ | |
| state | Selection | ✅ | draft/in_progress/done, group_expand |
| priority | Selection | ✅ | low/medium/high |
| due_date | Datetime | ✅ | |
| hours_estimated | Float | ✅ | digits=(6,2) |
| hours_spent | Float | ✅ | digits=(6,2) |
| color | Integer | ✅ | |
| is_overdue | Boolean(compute) | ✅ | **Ahead of schedule** (Day 7 content) |
| project_id | Many2one | ✅ | ondelete='cascade', index=True |
| assigned_user_id | Many2one | ✅ | default=lambda self: self.env.user |
| tag_ids | Many2many | ✅ | relation='task_task_tag_rel', column1/2 explicit |
| has_urgent_tags | Boolean(compute) | ✅ | @api.depends('tag_ids', 'tag_ids.name') |
| hours_remaining | Float(compute,store) | ✅ | hours_estimated - hours_spent |
| progress | Float(compute,store,inverse) | ✅ | (hours_spent/hours_estimated)*100 |

**Constraints:**
- ✅ `_sql_constraints`: name_project_id_unique, hours_estimated_check, hours_spent_check
- ✅ `@api.constrains`: _check_hours_on_done (hours_spent <= estimated), _check_due_date (future)

**Methods:**
- ✅ `_expand_states()` - Kanban columns
- ✅ `_compute_is_overdue()` - @api.depends
- ✅ `_compute_has_urgent_tag()` - Check for urgent tag
- ✅ `_compute_hours_remaining()` - hours_estimated - hours_spent
- ✅ `_compute_progress()` - percentage with inverse
- ✅ `_inverse_progress()` - update hours_spent from progress
- ✅ `_search_is_overdue()` - search method for non-stored field
- ✅ `create()` - Override with logging
- ✅ `write()` - Override with validation
- ✅ `unlink()` - Override to prevent deleting 'done' tasks
- ✅ `action_mark_done()`, `action_delete()`, `action_admin_only()`
- ✅ `action_mark_urgent()` - Add urgent tag
- ✅ `action_remove_all_tags()` - Clear tags

---

### task.project

| Field | Type | Status | Notes |
|-------|------|--------|-------|
| name | Char(required, index) | ✅ | |
| description | Text | ✅ | |
| image | Image | ✅ | max 1920x1080 |
| task_ids | One2many | ✅ | inverse='project_id' |
| manager_id | Many2one | ✅ | res.users |
| task_count | Integer(compute,store) | ✅ | len(task_ids) |

---

### task.tag

| Field | Type | Status | Notes |
|-------|------|--------|-------|
| name | Char(required) | ✅ | |
| color | Integer | ✅ | For color picker widget |
| task_ids | Many2many | ✅ | Inverse of task.task.tag_ids |

---

## 🎨 Current Views

| Model | View | Status | Features |
|-------|------|--------|----------|
| task.task | Tree | ✅ | decorations, is_overdue, **clean_draft header btn** |
| task.task | Form | ✅ | header/statusbar, 2 columns, notebook, relational fields |
| task.task | Kanban | ✅ | color picker, dropdown, tags with t-foreach |
| task.task | Search | ✅ | filters, group by project |
| task.project | Tree | ✅ | basic |
| task.project | Form | ✅ | image widget, O2M tasks tab |
| task.project | Kanban | ✅ | cover image |
| task.tag | Tree | ✅ | name, color |
| task.tag | Form | ✅ | basic |

---

## 🔐 Current Security

| File | Status | Content |
|------|--------|---------|
| ir.model.access.csv | ✅ | task.task, task.project, task.tag ACL |
| Groups | ❌ | Not defined |
| Record Rules | ❌ | Not defined |

---

## 📁 Current File Structure

```
task_management/
├── __init__.py ✅
├── __manifest__.py ✅
├── models/
│   ├── __init__.py ✅
│   ├── task.py ✅ (~120 lines)
│   ├── project.py ✅ (~20 lines)
│   └── tag.py ✅ (~25 lines)
├── views/
│   ├── task_views.xml ✅ (~220 lines)
│   ├── project_views.xml ✅
│   └── tag_views.xml ✅
├── security/
│   └── ir.model.access.csv ✅ (includes task.tag)
└── (other dirs not created yet)
```

---

## 📈 Progress Summary

| Phase | Days | Status |
|-------|------|--------|
| Phase 1: Foundation | 1-4 | ✅ Complete |
| Phase 2: Business Logic | 5-10 | 🔄 Day 7 done |
| Phase 3: Security | 11-14 | ⏳ Not started |
| Phase 4: Advanced | 15-21 | ⏳ Not started |

---

## ⚠️ Deviations from Spec

| Feature | Spec Says | Actual | Action |
|---------|-----------|--------|--------|
| is_overdue | Day 7 | ✅ Done in Day 5 | Update spec to reflect |
| description | optional | required=True | Keep as is (stricter) |

---

## 📝 Update Log

| Date | Day | Updated By | Changes |
|------|-----|------------|---------|
| 2026-01-19 | After Day 5 | Planner | Initial snapshot |
| 2026-01-20 | After Day 6 | Trainer | Added M2O, O2M, M2M to all models; task.tag model created; views updated |
| 2026-01-22 | After Day 7 | Trainer | Added computed fields: hours_remaining, progress (with inverse), task_count; search method for is_overdue |
| 2026-01-24 | After Day 8 | Planner | Added constraints (SQL & Python); Statusbar widget; Unlink protection |
| 2026-01-24 | After Day 8 | Planner | Added constraints (SQL & Python); Statusbar widget; Unlink protection |
