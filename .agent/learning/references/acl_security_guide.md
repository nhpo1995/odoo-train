# Odoo ACL Security Guide

## Overview

Access Control Lists (ACL) in Odoo define **MODEL-level** permissions. They control who can:
- **Read** - View records
- **Write** - Edit existing records  
- **Create** - Create new records
- **Unlink** - Delete records

## ir.model.access.csv Structure

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model access,model_my_model,base.group_user,1,1,1,1
```

### Columns:
| Column | Description |
|--------|-------------|
| `id` | Unique external ID (e.g., `access_task_task_user`) |
| `name` | Human-readable name |
| `model_id:id` | Model reference using `model_` prefix (e.g., `model_task_task`) |
| `group_id:id` | Group reference (empty = global access to unauthenticated users) |
| `perm_read` | 1 = allowed, 0 = denied |
| `perm_write` | 1 = allowed, 0 = denied |
| `perm_create` | 1 = allowed, 0 = denied |
| `perm_unlink` | 1 = allowed, 0 = denied |

## Key Concepts

### 1. Model Reference Format
- Model `task.task` → `model_task_task` (replace `.` with `_`)

### 2. Common Groups
- `base.group_user` - Internal Users (Employees)
- `base.group_public` - Public (website visitors)
- `base.group_portal` - Portal Users
- `base.group_system` - System (Admin)
- `base.group_erp_manager` - Settings Manager

### 3. Global vs Group Access
- **Empty `group_id`**: Applies to ALL users (including unauthenticated)
- **Specific group**: Applies only to users in that group

### 4. Permission Stacking
- Permissions are **additive** (OR logic)
- If user is in multiple groups, they get combined permissions
- More restrictive = define separate groups

## Best Practices (Context7)

1. **Always define ACL** for custom models - no ACL = no access (except admin)
2. Use `base.group_user` for internal-only models
3. Check logs for "access rights not defined" warnings
4. Use `check_access('write')` in code to explicitly verify permissions

## Programmatic Access Check

```python
# Check if current user has access
self.check_access('write')  # Raises AccessError if denied

# Check if user has specific group
if self.env.user.has_group('module.group_name'):
    # Do something
```

## AccessError Exception

When ACL denies access, Odoo raises `AccessError` with message:
- Which operation was denied
- Which groups have access
- Suggestion to contact admin

## Source Code Reference

- `IrModelAccess` class: `odoo/addons/base/models/ir_model.py` L1692-1869
- `check()` method: L1767-1834 - Core ACL check logic
- Example CSV: `odoo/addons/base/security/ir.model.access.csv`
