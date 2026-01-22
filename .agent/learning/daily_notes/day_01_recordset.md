# Day 1: Recordset - Lý do bạn "mù" khi đọc module

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 1 of 21 |
| **Chủ đề** | Recordset - Hiểu vì sao `self` luôn là collection |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Python basics, decorators, context managers |
| **Mục tiêu chính** | Hiểu Recordset là gì, tại sao `self` trong Odoo luôn là collection (0..n records), không phải single object |

---

## 📚 PHẦN 1: NỘI DUNG BÀI HỌC

### 1.1 Lý thuyết cần dạy

- [ ] **Recordset concept - Core của Odoo ORM**
  - Giải thích: Recordset là một collection chứa 0 hoặc nhiều records. Mọi model instance trong Odoo đều là recordset, kể cả khi chỉ có 1 record duy nhất. Đây là điểm khác biệt căn bản so với ORM khác.
  - Ví dụ:
    ```python
    # self LUÔN là recordset
    books = env['lib.book'].search([])  # recordset với n records
    book = env['lib.book'].browse(1)    # recordset với 1 record
    empty = env['lib.book'].browse([])  # recordset với 0 records
    ```

- [ ] **`env` - ORM entry point**
  - Giải thích: `env` không phải là data, mà là context + registry + security. `env['model_name']` trả về recordset rỗng của model đó.
  - Ví dụ:
    ```python
    # env = Environment(context, registry, uid, cursor)
    self.env.context  # dict với thông tin request
    self.env.user     # user hiện tại
    self.env.cr        # database cursor
    ```

- [ ] **Magic methods: `__iter__`, `__len__`, `__bool__`**
  - Giải thích: Recordset implement Python container protocol, cho phép iterate, check length, boolean.
  - Ví dụ:
    ```python
    for record in self:      # __iter__
        print(record.name)
    
    count = len(self)        # __len__
    
    if self:                 # __bool__
        print("not empty")
    ```

- [ ] **Singleton vs Multi-record**
  - Giải thích: Không bao giờ giả định `self` là singleton. Dùng `ensure_one()` khi cần chắc chắn chỉ 1 record.
  - Ví dụ:
    ```python
    # WRONG - nguy hiểm!
    name = self.name  # Lỗi nếu self có nhiều records
    
    # RIGHT - an toàn
    for record in self:
        name = record.name
    
    # HOẶC khi chắc chắn singleton
    self.ensure_one()
    name = self.name
    ```

- [ ] **`browse()`, `search()`, `exists()`**
  - Giải thích:
    - `browse(ids)`: Tạo recordset từ IDs (lazy, không query DB ngay)
    - `search(domain)`: Query DB thật với domain
    - `exists()`: Check record có tồn tại trong DB không
  - Ví dụ:
    ```python
    # browse - lazy
    book = env['lib.book'].browse(1)  # Chưa query DB
    print(book.name)                   # Bây giờ mới query
    
    # search - query ngay
    books = env['lib.book'].search([('state', '=', 'available')])
    
    # exists - verify
    if book.exists():
        print("Book still in DB")
    ```

- [ ] **Domain syntax - AND/OR prefix notation**
  - Giải thích: Domain dùng prefix notation kiểu Lisp. `|` (OR) chỉ ăn đúng 2 điều kiện tiếp theo.
  - Ví dụ:
    ```python
    # AND (mặc định)
    [('state', '=', 'available'), ('author_id', '!=', False)]
    
    # OR - chú ý: | chỉ ăn 2 điều kiện
    ['|', ('name', 'ilike', 'python'), ('name', 'ilike', 'odoo')]
    
    # Complex: (A OR B) AND C
    ['&', '|', ('name', 'ilike', 'a'), ('name', 'ilike', 'b'), ('state', '=', 'available')]
    ```

- [ ] **`_rec_name` và display name**
  - Giải thích: `_rec_name` chỉ định field nào dùng làm display name (mặc định là `name`). UI tự gọi `name_get()` để hiển thị.
  - Ví dụ:
    ```python
    class LibBook(models.Model):
        _name = 'lib.book'
        _rec_name = 'title'  # Dùng title thay vì name
        
        title = fields.Char('Title')
    ```

### 1.2 Source code cần đọc

| File | Class/Method | Line range | Focus |
|------|--------------|------------|-------|
| `odoo/models.py` | `BaseModel` | L254 - L6428 | Class definition, docstring |
| `odoo/models.py` | `BaseModel.__len__` | L5587 - L5589 | Return size của recordset |
| `odoo/models.py` | `BaseModel.__bool__` | L5582 - L5584 | Check recordset empty/not empty |
| `odoo/models.py` | `BaseModel.__iter__` | L5591 - L5599 | Iterate qua từng record |
| `odoo/models.py` | `BaseModel.browse` | L4998 - L5019 | Create recordset từ IDs (lazy) |
| `odoo/models.py` | `BaseModel.search` | L1699 - L1720 | Query DB với domain |
| `odoo/models.py` | `BaseModel.exists` | L4718 - L4738 | Verify records tồn tại |

### 1.3 Kiến thức liên quan

| Odoo | Tương đương SQLAlchemy/FastAPI | Khác biệt |
|------|-------------------------------|-----------|
| Recordset | Query object (lazy evaluation) | Odoo recordset còn chứa data khi evaluated |
| `env['model']` | `Session().query(Model)` | Odoo env là singleton per request |
| `browse([1,2,3])` | `session.query(Model).filter(Model.id.in_([1,2,3]))` | Odoo lazy hơn, không query ngay |
| Domain | SQLAlchemy filter expressions | Odoo dùng prefix notation |
| `self` trong method | `self` trong SQLAlchemy model | Odoo `self` luôn là collection |

---

## 💻 PHẦN 2: THỰC HÀNH

### 2.1 Bài tập code

**Exercise 1**: Tạo model `lib.book`
```python
# Yêu cầu: Tạo model cơ bản trong custom_addons/library_mgmt/models/book.py
# Expected: Module load không lỗi, có thể browse trong shell
# File: custom_addons/library_mgmt/models/book.py

from odoo import models, fields

class LibBook(models.Model):
    _name = 'lib.book'
    _description = 'Library Book'
    
    name = fields.Char('Title', required=True)
    isbn = fields.Char('ISBN')

# Hints: 
# - Nhớ thêm file __init__.py import model này
# - Thêm model vào __manifest__.py trong 'data': []
```

**Exercise 2**: Debug `len(self)` trong method
```python
# Yêu cầu: Tạo method print số records trong self
# Expected: Khi gọi từ UI, thấy self có bao nhiêu records
# File: Thêm vào model lib.book

import logging
_logger = logging.getLogger(__name__)

def debug_recordset_size(self):
    _logger.info(f"self has {len(self)} records")
    _logger.info(f"IDs: {self.ids}")
    for idx, record in enumerate(self):
        _logger.info(f"  Record {idx}: {record.id}")
```

**Exercise 3**: Test `exists()`
```python
# Yêu cầu: Test exists() với record đã delete
# Expected: Hiểu lazy evaluation của browse
# Shell commands:
book = env['lib.book'].browse(999)  # ID không tồn tại
print(book)                          # Vẫn có object
print(book.exists())                 # False - bây giờ mới check DB
if book.exists():
    print(book.name)                 # Safe
```

### ✅ 2.4 Module đã tạo thực tế

**Module**: `library_mgmt`
**Location**: `custom_addons/library_mgmt/`

**Cấu trúc module:**
```
library_mgmt/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── book.py              ← Model library.book
├── views/
│   └── book_views.xml       ← Tree, Form, Action, Menu
└── security/
    └── ir.model.access.csv  ← ACL cho base.group_user
```

**Model: `library.book`**
```python
# custom_addons/library_mgmt/models/book.py
import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)

class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Book"
    _rec_name = "name"

    name = fields.Char(required=True, index=True)
    active = fields.Boolean(default=True)
    parent_id = fields.Many2one("library.book", string="Parent Book")

    def name_get(self):
        _logger.info("name_get called with ids=%s len=%s", self.ids, len(self))
        return [(rec.id, f"[{rec.id}] {rec.name}") for rec in self]
```

**Views: Tree + Form**
- Tree view: Hiển thị name, parent_id, active
- Form view: Simple form với 3 fields
- Action: `action_library_book` 
- Menu: Library → Books

**Security:**
```csv
access_library_book_user,library.book user,model_library_book,base.group_user,1,1,1,1
```
→ Internal users có full CRUD access

**Highlights đã practice:**
✅ Tạo model với `_name`, `_description`, `_rec_name`
✅ Override `name_get()` với custom format `[ID] Name`
✅ Thêm `_logger` để debug UI calls
✅ Tạo views (tree/form) hoàn chỉnh
✅ Setup action + menu
✅ Config ACL security


### 2.2 Shell commands

```python
# Mục đích: Test recordset basics
books = env['lib.book'].search([])
print(f"Type: {type(books)}")        # odoo.addons.library_mgmt.models.book.LibBook
print(f"Length: {len(books)}")
print(f"Boolean: {bool(books)}")

# Mục đích: Test iteration
for book in books:
    print(f"{book.id}: {book.name}")

# Mục đích: Test domain
available_books = env['lib.book'].search([('state', '=', 'available')])

# Mục đích: Test OR domain
search_books = env['lib.book'].search([
    '|', ('name', 'ilike', 'python'), ('name', 'ilike', 'odoo')
])

# Mục đích: Debug name_get (observe UI calls)
# Thêm _logger vào name_get và xem UI tự gọi
```

### 2.3 Debug tasks

- [ ] **Debug 1**: Thêm `_logger.info()` vào method để xem UI tự gọi `name_get()` khi nào
  - Tạo method name_get()
  - Log mỗi khi được gọi
  - Observe: dropdown gọi với len(self) = nhiều, sau khi chọn gọi với len(self) = 1

- [ ] **Debug 2**: Test lazy evaluation của browse
  - `book = env['lib.book'].browse(1)` (chưa có query)
  - `print(book.name)` (bây giờ mới query)
  - Check log SQL để verify

---

## ❓ PHẦN 3: KIỂM TRA KIẾN THỨC

### 3.1 Câu hỏi self-check

1. Vì sao `self` trong Odoo không bao giờ đảm bảo là 1 record?
2. Recordset rỗng khác `None` như thế nào?
3. `for record in self` hoạt động nhờ magic method nào?
4. `browse()` và `search()` khác nhau thế nào về timing query DB?
5. Domain `['|', ('a', '=', 1), ('b', '=', 2), ('c', '=', 3)]` sai ở đâu?
6. `_rec_name` dùng để làm gì?

### 3.2 Đáp án

<details>
<summary>Xem đáp án</summary>

1. **Vì sao `self` không đảm bảo là 1 record?**
   - Bởi vì Odoo design `self` luôn là recordset (collection 0..n records). Method có thể được gọi với multi-records (ví dụ: chọn nhiều records trong list view rồi click action). Nếu giả định singleton, code sẽ crash.

2. **Recordset rỗng vs None:**
   - Recordset rỗng là object valid (len = 0, bool = False) nhưng NOT None
   - `bool(empty_recordset)` → False
   - `empty_recordset is None` → False
   - `empty_recordset == None` → False

3. **`for record in self` dùng magic method:**
   - `__iter__` (line 5591-5599)
   - Trả về generator yield từng record singleton

4. **`browse()` vs `search()`:**
   - `browse(ids)`: Lazy, chỉ tạo recordset, chưa query DB. Query khi access field.
   - `search(domain)`: Query DB ngay để get IDs matching domain.

5. **Domain sai:**
   - Sai vì `|` chỉ ăn 2 điều kiện, nhưng có 3 điều kiện
   - Đúng: `['|', '|', ('a', '=', 1), ('b', '=', 2), ('c', '=', 3)]`
   - Hoặc: `['|', ('a', '=', 1), '|', ('b', '=', 2), ('c', '=', 3)]`

6. **`_rec_name`:**
   - Chỉ định field nào làm "display name" của record
   - Mặc định là `'name'`
   - UI dùng để hiển thị trong dropdown, breadcrumb, etc.

</details>

---

## ✅ PHẦN 4: TIÊU CHÍ HOÀN THÀNH

| Tiêu chí | Đạt | Chưa đạt |
|----------|-----|----------|
| Giải thích được vì sao `self` không đảm bảo là 1 record | ⬜ | ⬜ |
| Viết được model `lib.book` load không lỗi | ⬜ | ⬜ |
| Chạy được `env['lib.book'].search([])` trong shell | ⬜ | ⬜ |
| Phân biệt được recordset rỗng vs None | ⬜ | ⬜ |
| Hiểu lazy evaluation của `browse()` | ⬜ | ⬜ |
| Viết được domain với OR operator đúng | ⬜ | ⬜ |
| Quan sát được UI tự gọi `name_get()` (qua _logger) | ⬜ | ⬜ |

---

## 📝 PHẦN 5: ĐÁNH GIÁ (AI Mentor điền sau khi dạy)

### 5.1 Kết quả học tập
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Lý thuyết | 10 | Hiểu rõ tất cả 7 concepts |
| Thực hành | 9 | Complete exercises, debug tốt |
| Kiểm tra | 10 | Trả lời đúng 100% |
| **TỔNG** | **9.5/10** | ✅ Xuất sắc! |

### 5.2 Key takeaways
> ✅ **Recordset (100%)**: `self` luôn là recordset (0..n), không giả định singleton
> ✅ **env (100%)**: env = context + registry + security, không phải data
> ✅ **browse/search/exists (100%)**: Phân biệt lazy vs query DB thật
> ✅ **Singleton handling (100%)**: Biết khi nào dùng `.field`, `mapped()`, `loop`, `ensure_one()`
> ✅ **Domain logic (100%)**: Hiểu prefix notation, `|` chỉ ăn 2 điều kiện
> ⚠️ **UI behavior (90%)**: Thấy UI tự gọi `name_get()`, quan sát `len(self)` thay đổi
> ✅ **Display name (100%)**: Hiểu `_rec_name` / `name`

### 5.3 Điểm cần cải thiện
> ⚠️ **UI behavior**: Chỉ 90% - cần thêm practice với nhiều case khác để quan sát UI gọi methods ngầm
> 💡 Tip: Thêm `_logger` vào nhiều methods khác nhau để observe patterns

### 5.4 Lưu ý cho ngày tiếp theo
> 🚀 **Sẵn sàng cho Day 2**: `mapped()`, `filtered()`, `sorted()` - vectorized methods
> 💪 Nền tảng vững chắc từ Day 1 sẽ giúp hiểu sâu các transformation methods
> 🎯 Focus: Apply recordset knowledge vào practical operations

---

## 🔄 14 ↔ 19 DIFFERENCES

| Aspect | Odoo 14 | Odoo 17/19 | Notes |
|--------|---------|------------|-------|
| Recordset concept | Giống | Giống | Core concept không đổi |
| `env` | Giống | Giống | API không đổi |
| Domain syntax | Giống | Giống | Backward compatible |
| Magic methods | Giống | Giống | `__iter__`, `__len__`, `__bool__` giữ nguyên |
