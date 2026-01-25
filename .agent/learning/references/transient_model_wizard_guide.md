# Odoo Wizards (TransientModel) Guide

## Overview
Wizards are interactive dialogs used for intermediate actions, such as reporting, batch updates, or complex configuration. They rely on the `TransientModel` class.

## Key Concepts

### 1. TransientModel
- **Class**: `models.TransientModel` (vs `models.Model`).
- **Persistence**: Data is stored in the database but is **temporary**.
- **Vacuum**: Odoo runs a scheduled job (`transient_vacuum`) to delete old records (default: every 24h or 5m depending on config).
- **Access Rights**: Simplified. Users can usually create and read their own transient records without complex ACLs (though `ir.model.access.csv` is still required).

### 2. Wizard Action (`target="new"`)
To open a view as a pop-up dialog (modal):
```xml
<record id="action_my_wizard" model="ir.actions.act_window">
    <field name="name">My Wizard</field>
    <field name="res_model">my.wizard</field>
    <field name="view_mode">form</field>
    <field name="target">new</field> <!-- Critical for Dialog -->
</record>
```

### 3. Binding to "Action" Menu aka Sidebar
To make the wizard appear in the "Action" gear menu of another model (e.g., selecting tasks -> Run Wizard):
```xml
<field name="binding_model_id" ref="model_task_task"/>
<field name="binding_view_types">list,form</field>
```

### 4. Handling `active_ids`
When launched from a source model (Current Record or Selection), Odoo passes context:
- `active_id`: ID of the record (Form view) or first selected ID.
- `active_ids`: List of IDs of selected records (List view).
- `active_model`: The model name (e.g., 'task.task').

**Usage in Wizard**:
```python
def default_get(self, fields):
    res = super().default_get(fields)
    active_ids = self.env.context.get('active_ids')
    # Pre-fill data based on selection
    return res

def action_apply(self):
    tasks = self.env['task.task'].browse(self.env.context.get('active_ids'))
    tasks.write({'state': self.new_state})
    return {'type': 'ir.actions.act_window_close'}
```

## Best Practices

1. **Relations**:
   - **Allowed**: `TransientModel` -> `Many2one` -> `Model` (Persistent).
   - **Forbidden**: `Model` (Persistent) -> `One2many` -> `TransientModel`.
     - *Why?* If `Model` refers to `Transient`, and the `Transient` record is vacuumed, the link breaks or causes integrity errors.

2. **Buttons**:
   - Use `special="cancel"` for the Cancel button to close the dialog without RPC calls.
   - Use `type="object"` for execution buttons.

3. **Returning Actions**:
   - Wizard methods often return an action dictionary to:
     - Close the window (`ir.actions.act_window_close`).
     - Reload the page (`client_action` -> `reload`).
     - Open another view (next step).
