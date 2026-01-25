# Odoo Onchange & UI Interaction Guide

## Overview
`@api.onchange` methods are used to implement dynamic UI interactions in Odoo's Form Views. They allow you to update fields, show warnings, or filter domains based on user input **in real-time**.

## Key Concepts

### 1. @api.onchange Decorator
- **Purpose**: Triggers python code when a specific field is modified by the user in the UI.
- **Behavior**: It modifies the `self` recordset in memory (virtual record). The changes are NOT saved to the database until the user clicks Save.
- **Example**:
  ```python
  @api.onchange('project_id')
  def _onchange_project_id(self):
      if self.project_id:
          self.assigned_user_id = self.project_id.manager_id
  ```

### 2. Onchange Return Patterns (Warning & Domain)
Onchange methods can return a dictionary to interact with the UI:
```python
@api.onchange('partner_id')
def _onchange_partner(self):
    if not self.partner_id.email:
        return {
            'warning': {
                'title': "Missing Contact Info",
                'message': "Selected partner has no email!"
            }
        }
    return {
        'domain': {'contact_person_id': [('parent_id', '=', self.partner_id.id)]}
    }
```

## Best Practices (vs Computed Fields)

| Feature | Onchange (`@api.onchange`) | Computed Field (`@api.depends`) |
|---------|----------------------------|--------------------------------|
| **Trigger** | UI interaction only | Create, Write, or UI change |
| **Consistency** | **Low**. Bypassed by code imports/create. | **High**. Always enforced by ORM. |
| **Use Case** | UI defaults, warnings, dynamic domains. | Business logic, state calculation, data integrity. |

**Rule of Thumb**:
- Use **Computed Fields** for logic that must *always* be true (e.g., `total = price * qty`).
- Use **Onchange** for "suggestions" that the user might want to override (e.g., defaulting `payment_term` when selecting a `partner`).

## Common Pitfalls

1. **Relying on Onchange for Integrity**:
   - **Mistake**: Using onchange to validate data (e.g., "End Date must be > Start Date").
   - **Risk**: If a record is created via API, Script, or CSV import, the onchange **will not run**, and bad data will enter the DB.
   - **Fix**: Use `@api.constrains` for validation.

2. **Onchange in `create()`**:
   - Onchange methods do not automatically run when you call `create()` or `write()` via Python code.
   - You must explicitly call `_onchange_...()` if you want to simulate the behavior in tests/scripts, but it's complex.

3. **Returning Values**:
   - **Do not return** the values dictionary (e.g., `return {'value': {...}}`) in modern Odoo (v8+). Just assign to `self.field = value`.
