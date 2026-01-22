# 📖 Odoo Quick Patterns Reference

> Các code patterns thường dùng trong Odoo development

---

## 🔹 Model Definition

```python
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class LibBook(models.Model):
    _name = 'lib.book'
    _description = 'Library Book'
    _order = 'name'
    
    name = fields.Char(string='Title', required=True)
    isbn = fields.Char(string='ISBN')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    ], default='draft')
    author_id = fields.Many2one('lib.author', string='Author')
```

---

## 🔹 Computed Field

```python
book_count = fields.Integer(compute='_compute_book_count', store=True)

@api.depends('book_ids')
def _compute_book_count(self):
    for record in self:
        record.book_count = len(record.book_ids)
```

---

## 🔹 Constraint

```python
from odoo.exceptions import ValidationError

_sql_constraints = [
    ('isbn_unique', 'UNIQUE(isbn)', 'ISBN must be unique!'),
]

@api.constrains('name')
def _check_name(self):
    for record in self:
        if not record.name or len(record.name) < 3:
            raise ValidationError("Name must be at least 3 characters!")
```

---

## 🔹 Onchange

```python
@api.onchange('author_id')
def _onchange_author(self):
    if self.author_id:
        self.description = f"Written by {self.author_id.name}"
```

---

## 🔹 Override Create/Write

```python
@api.model
def create(self, vals):
    # Pre-processing
    if not vals.get('code'):
        vals['code'] = self.env['ir.sequence'].next_by_code('lib.book')
    
    record = super().create(vals)
    
    # Post-processing
    _logger.info(f"Created book: {record.name}")
    return record

def write(self, vals):
    result = super().write(vals)
    # Post-processing
    return result
```

---

## 🔹 Search & Browse

```python
# Search with domain
books = self.env['lib.book'].search([
    ('state', '=', 'available'),
    '|',
    ('name', 'ilike', 'python'),
    ('author_id.name', 'ilike', 'john'),
])

# Browse by IDs
book = self.env['lib.book'].browse(1)
books = self.env['lib.book'].browse([1, 2, 3])

# Filtered & Mapped
available_books = books.filtered(lambda b: b.state == 'available')
book_names = books.mapped('name')
author_names = books.mapped('author_id.name')
```

---

## 🔹 Context

```python
# Read context
lang = self.env.context.get('lang', 'en_US')
active_id = self.env.context.get('active_id')

# With context
records = self.with_context(active_test=False).search([])
translated_record = record.with_context(lang='vi_VN')
```

---

## 🔹 Form View

```xml
<record id="view_book_form" model="ir.ui.view">
    <field name="name">lib.book.form</field>
    <field name="model">lib.book</field>
    <field name="arch" type="xml">
        <form>
            <header>
                <button name="action_confirm" type="object" string="Confirm"/>
                <field name="state" widget="statusbar"/>
            </header>
            <sheet>
                <group>
                    <group>
                        <field name="name"/>
                        <field name="author_id"/>
                    </group>
                    <group>
                        <field name="isbn"/>
                        <field name="state"/>
                    </group>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

---

## 🔹 Tree View

```xml
<record id="view_book_tree" model="ir.ui.view">
    <field name="name">lib.book.tree</field>
    <field name="model">lib.book</field>
    <field name="arch" type="xml">
        <tree>
            <field name="name"/>
            <field name="author_id"/>
            <field name="state"/>
        </tree>
    </field>
</record>
```

---

## 🔹 Search View

```xml
<record id="view_book_search" model="ir.ui.view">
    <field name="name">lib.book.search</field>
    <field name="model">lib.book</field>
    <field name="arch" type="xml">
        <search>
            <field name="name"/>
            <field name="author_id"/>
            <filter name="available" string="Available" domain="[('state', '=', 'available')]"/>
            <group expand="0" string="Group By">
                <filter name="group_author" string="Author" context="{'group_by': 'author_id'}"/>
            </group>
        </search>
    </field>
</record>
```

---

## 🔹 Action & Menu

```xml
<record id="action_book" model="ir.actions.act_window">
    <field name="name">Books</field>
    <field name="res_model">lib.book</field>
    <field name="view_mode">tree,form</field>
</record>

<menuitem id="menu_library_root" name="Library"/>
<menuitem id="menu_book" name="Books" parent="menu_library_root" action="action_book"/>
```

---

## 🔹 View Inheritance

```xml
<record id="view_partner_form_inherit" model="ir.ui.view">
    <field name="name">res.partner.form.inherit.library</field>
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="base.view_partner_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='phone']" position="after">
            <field name="library_card"/>
        </xpath>
    </field>
</record>
```

---

## 🔹 Security (ACL)

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_lib_book_user,lib.book.user,model_lib_book,base.group_user,1,0,0,0
access_lib_book_librarian,lib.book.librarian,model_lib_book,library_mgmt.group_librarian,1,1,1,1
```

---

## 🔹 Record Rule

```xml
<record id="rule_book_member" model="ir.rule">
    <field name="name">Member sees own borrowed books</field>
    <field name="model_id" ref="model_lib_book"/>
    <field name="domain_force">[('borrower_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('group_member'))]"/>
</record>
```

---

## 🔹 Controller (JSON)

```python
from odoo import http
from odoo.http import request

class LibraryController(http.Controller):
    
    @http.route('/api/books', type='json', auth='user')
    def get_books(self, **kwargs):
        books = request.env['lib.book'].search([])
        return [{'id': b.id, 'name': b.name} for b in books]
```

---

## 🔹 Domain Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equal | `[('state', '=', 'draft')]` |
| `!=` | Not equal | `[('state', '!=', 'draft')]` |
| `in` | In list | `[('state', 'in', ['draft', 'confirmed'])]` |
| `not in` | Not in list | `[('state', 'not in', ['cancelled'])]` |
| `like` | Pattern match (case-sensitive) | `[('name', 'like', 'Book%')]` |
| `ilike` | Pattern match (case-insensitive) | `[('name', 'ilike', '%python%')]` |
| `>`, `<`, `>=`, `<=` | Comparison | `[('date', '>', '2024-01-01')]` |
| `child_of` | Hierarchy | `[('parent_id', 'child_of', 1)]` |

**Logical operators**:
```python
# AND (default)
[('state', '=', 'available'), ('author_id', '!=', False)]

# OR
['|', ('name', 'ilike', 'a'), ('name', 'ilike', 'b')]

# NOT
['!', ('state', '=', 'cancelled')]
```

---

## 🔹 Debug Commands (Shell)

```python
# Khởi động shell
./odoo-bin shell -d database_name

# Trong shell
records = env['lib.book'].search([])
print(len(records))
print(records.mapped('name'))

# Bypass security
env['lib.book'].sudo().search([])

# Check user
print(env.user.name)
print(env.user.groups_id.mapped('name'))

# Change context
env['lib.book'].with_context(lang='vi_VN').search([])
```
