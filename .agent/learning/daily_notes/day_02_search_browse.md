# Day 2: search / browse / filtered / mapped

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 2 of 21 |
| **Chủ đề** | Vectorized operations - transform và filter recordsets |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Day 1: Recordset basics |
| **Mục tiêu chính** | Master 4 methods quan trọng nhất để query và transform recordsets: `search()`, `browse()`, `filtered()`, `mapped()` |

---

## 📚 PHẦN 1: NỘI DUNG BÀI HỌC

### 1.1 Lý thuyết cần dạy

- [ ] **`search()` vs `browse()` - Query DB**
  - Giải thích:
    - `search(domain)`: Query DB với điều kiện, trả về recordset matching
    - `browse(ids)`: Tạo recordset từ IDs có sẵn (lazy loading)
  - Ví dụ:
    ```python
    # search - query DB ngay
    books = env['lib.book'].search([('state', '=', 'available')])
    # → SELECT id FROM lib_book WHERE state = 'available'
    
    # browse - lazy, không query ngay
    books = env['lib.book'].browse([1, 2, 3])
    # → Chưa có query
    print(books[0].name)  # Bây giờ mới query
    # → SELECT * FROM lib_book WHERE id IN (1,2,3)
    ```

- [ ] **`mapped()` - Transform recordset**
  - Giải thích: Apply function/field path lên tất cả records, trả về list hoặc recordset
  - Ví dụ:
    ```python
    # Map field name → list
    names = books.mapped('name')
    # → ['Book A', 'Book B', 'Book C']
    
    # Map M2O field → recordset (union, no duplicates)
    authors = books.mapped('author_id')
    # → recordset of authors
    
    # Traverse relationships
    emails = books.mapped('author_id.email')
    # → ['email1@test.com', 'email2@test.com']
    
    # Map với lambda
    totals = books.mapped(lambda b: b.price * b.quantity)
    # → [100, 200, 150]
    ```

- [ ] **`filtered()` - Filter recordset in-memory**
  - Giải thích: Lọc recordset theo condition, chạy in-memory (không query DB)
  - Ví dụ:
    ```python
    # Filter với lambda
    expensive_books = books.filtered(lambda b: b.price > 50)
    
    # Filter với field path (string)
    books_with_author = books.filtered('author_id')
    # Giống: books.filtered(lambda b: b.author_id)
    
    # Complex condition
    books_in_stock = books.filtered(
        lambda b: b.state == 'available' and b.quantity > 0
    )
    ```

- [ ] **`sorted()` - Sort recordset**
  - Giải thích: Sort recordset theo key, trả về recordset mới
  - Ví dụ:
    ```python
    # Sort by field
    sorted_books = books.sorted('name')
    sorted_books = books.sorted(key=lambda b: b.name)
    
    # Reverse order
    sorted_books = books.sorted('name', reverse=True)
    
    # Sort by computed value
    sorted_books = books.sorted(lambda b: b.price * b.quantity)
    ```

- [ ] **`ids` property - Get list of IDs**
  - Giải thích: Property trả về list các IDs của recordset
  - Ví dụ:
    ```python
    books = env['lib.book'].search([])
    print(books.ids)  # → [1, 2, 3, 4, 5]
    
    # Useful for: pass IDs to other methods
    env['lib.book'].browse(books.ids)
    ```

- [ ] **Chaining methods - Functional style**
  - Giải thích: Các methods này return recordset, có thể chain
  - Ví dụ:
    ```python
    # Chain: search → filtered → mapped 
    author_names = env['lib.book'].search([
        ('state', '=', 'available')
    ]).filtered(
        lambda b: b.price > 50
    ).mapped('author_id.name')
    
    # Tương đương:
    books = env['lib.book'].search([('state', '=', 'available')])
    expensive_books = books.filtered(lambda b: b.price > 50)
    author_names = expensive_books.mapped('author_id.name')
    ```

### 1.2 Source code cần đọc

| File | Class/Method | Line range | Focus |
|------|--------------|------------|-------|
| `odoo/models.py` | `BaseModel.search` | L1699 - L1720 | Query DB với domain |
| `odoo/models.py` | `BaseModel.browse` | L4998 - L5019 | Create recordset từ IDs (lazy) |
| `odoo/models.py` | `BaseModel.mapped` | L5270 - L5306 | Transform: func hoặc field path |
| `odoo/models.py` | `BaseModel.filtered` | L5322 - L5342 | Filter in-memory với lambda |
| `odoo/models.py` | `BaseModel.sorted` | L5445 - L5464 | Sort recordset |

### 1.3 Kiến thức liên quan

| Odoo | Tương đương Python/Functional | Khác biệt |
|------|------------------------------|-----------|
| `mapped('name')` | `map(lambda x: x.name, items)` hoặc `[x.name for x in items]` | Odoo trả về list hoặc recordset |
| `filtered(lambda x: x.state)` | `filter(lambda x: x.state, items)` | Odoo trả về recordset, Python trả về iterator |
| `sorted(lambda x: x.name)` | `sorted(items, key=lambda x: x.name)` | Odoo trả về recordset |
| Chaining | Functional composition | Odoo tích hợp sẵn |

---

## 💻 PHẦN 2: THỰC HÀNH

### 2.1 Bài tập code

**Exercise 1**: Test `search()` với nhiều domains
```python
# Yêu cầu: Query books với điều kiện khác nhau
# Expected: Hiểu cách viết domain và kết quả

# Shell commands:
# Tìm tất cả books
all_books = env['lib.book'].search([])
print(f"Total: {len(all_books)}")

# Tìm books available
available = env['lib.book'].search([('state', '=', 'available')])

# Tìm books có tên chứa "python"
python_books = env['lib.book'].search([('name', 'ilike', 'python')])

# Complex: available VÀ có author
complex = env['lib.book'].search([
    ('state', '=', 'available'),
    ('author_id', '!=', False)
])
```

**Exercise 2**: Practice `mapped()`
```python
# Yêu cầu: Transform recordset theo nhiều cách
# Expected: Hiểu mapped trả về list vs recordset

books = env['lib.book'].search([], limit=5)

# Map tên (list)
names = books.mapped('name')
print(type(names))  # → list
print(names)

# Map author (recordset)
authors = books.mapped('author_id')
print(type(authors))  # → recordset
print(len(authors))

# Traverse: author emails
emails = books.mapped('author_id.email')
print(emails)

# Lambda: total prices
totals = books.mapped(lambda b: float(b.price or 0))
print(sum(totals))
```

**Exercise 3**: Practice `filtered()`
```python
# Yêu cầu: Filter recordset in-memory
# Expected: Hiểu filtered không query DB

books = env['lib.book'].search([])  # Get all

# Filter with lambda
expensive = books.filtered(lambda b: float(b.price or 0) > 50)
print(f"Expensive books: {len(expensive)}")

# Filter with field path
with_author = books.filtered('author_id')
print(f"Books with author: {len(with_author)}")

# Complex condition
in_stock = books.filtered(
    lambda b: b.state == 'available' and (b.quantity or 0) > 0
)
```

**Exercise 4**: Chaining methods
```python
# Yêu cầu: Combine search → filtered → mapped
# Expected: Hiểu functional composition

# Get names of expensive available books
result = env['lib.book'].search([
    ('state', '=', 'available')
]).filtered(
    lambda b: float(b.price or 0) > 50
).mapped('name')

print(result)  # → list of names
```

### 2.2 Shell commands

```python
# Mục đích: Compare search() vs filtered()
books_all = env['lib.book'].search([])
expensive_search = env['lib.book'].search([('price', '>', 50)])  # Query DB
expensive_filter = books_all.filtered(lambda b: float(b.price or 0) > 50)  # In-memory

# Observe: cùng kết quả, khác method

# Mục đích: Test sorted()
sorted_by_name = books.sorted('name')
print(sorted_by_name.mapped('name'))

# Mục đích: Get IDs
print(books.ids)  # → [1, 2, 3, ...]
```

### 2.3 Debug tasks

- [ ] **Debug 1**: So sánh performance search() vs filtered()
  - Query 1000 records với `search()`
  - Query all rồi `filtered()`
  - Observe: search() nhanh hơn với điều kiện đơn giản

- [ ] **Debug  2**: Test `mapped()` với empty recordset
  - `empty = env['lib.book'].browse([])`
  - `print(empty.mapped('name'))  # → []`
  - Không crash!

---

## ❓ PHẦN 3: KIỂM TRA KIẾN THỨC

### 3.1 Câu hỏi self-check

1. `search([('state', '=', 'draft')])` vs `browse([]).filtered(lambda x: x.state == 'draft')` - khác nhau thế nào?
2. `books.mapped('name')` trả về list hay recordset?
3. `books.mapped('author_id')` trả về list hay recordset?
4. `filtered()` có query DB không?
5. Viết chain: Tìm books available, expensive (>50), lấy tên authors
6. `books.ids` vs `books.mapped('id')` - khác nhau gì?

### 3.2 Đáp án

<details>
<summary>Xem đáp án</summary>

1. **search() vs filtered():**
   - `search()`: Query DB với WHERE clause → nhanh với data lớn
   - `filtered()`: Load tất cả records rồi filter in-memory → chậm với data lớn
   - Use case: Dùng `search()` khi có thể, `filtered()` khi logic phức tạp không thể viết domain

2. **`mapped('name')` → list**
   - Vì `name` là field primitive (Char)
   - List of strings

3. **`mapped('author_id')` → recordset**
   - Vì `author_id` là Many2one (relationship)
   - Recordset của model `lib.author`
   - Union tất cả authors, không có duplicate

4. **`filtered()` không query DB**
   - Chạy hoàn toàn in-memory
   - Iterate qua recordset đã có, apply lambda

5. **Chain:**
   ```python
   author_names = env['lib.book'].search([
       ('state', '=', 'available')
   ]).filtered(
       lambda b: float(b.price or 0) > 50
   ).mapped('author_id.name')
   ```

6. **`ids` vs `mapped('id')`:**
   - `books.ids` → list of ints - property, nhanh
   - `books.mapped('id')` → list of ints - method call, chậm hơn
   - Kết quả giống nhau, dùng `.ids` preferred

</details>

---

## ✅ PHẦN 4: TIÊU CHÍ HOÀN THÀNH

| Tiêu chí | Đạt | Chưa đạt |
|----------|-----|----------|
| Phân biệt được khi nào dùng `search()` vs `filtered()` | ⬜ | ⬜ |
| Viết được `books.mapped('name')` và hiểu trả về list | ⬜ | ⬜ |
| Viết được `books.mapped('author_id')` và hiểu trả về recordset | ⬜ | ⬜ |
| Viết được `books.filtered(lambda b: ...)` đúng syntax | ⬜ | ⬜ |
| Chain được search → filtered → mapped | ⬜ | ⬜ |
| Hiểu `filtered()` không query DB (in-memory) | ⬜ | ⬜ |
| Dùng được `sorted()` và `.ids` property | ⬜ | ⬜ |

---

## 📝 PHẦN 5: ĐÁNH GIÁ (AI Mentor điền sau khi dạy)

### 5.1 Kết quả học tập
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Lý thuyết | 10 | Hiểu rõ tất cả 6 concepts |
| Thực hành | 9 | Hoàn thành exercises, ban đầu nhầm search/filtered |
| Kiểm tra | 10 | Trả lời đúng câu hỏi tổng hợp |
| **TỔNG** | **9.5/10** | ✅ Xuất sắc! |

### 5.2 Key takeaways
> ✅ **search() vs browse() (100%)**: Hiểu rõ lazy loading, timing query DB
> ✅ **mapped() (100%)**: Field path vs lambda, return type (list vs recordset), traverse relationships
> ✅ **filtered() (100%)**: In-memory filter, không query DB, performance implication
> ✅ **sorted() (100%)**: Immutable, advanced multi-criteria sorting
> ✅ **.ids property (100%)**: Nhanh hơn mapped('id')
> ✅ **Chaining (100%)**: Functional composition - filter → sort → map
> ✅ **exists() use case**: Verify recordset, loại bỏ IDs không tồn tại

### 5.3 Điểm cần cải thiện
> ⚠️ Ban đầu nhầm lẫn giữa `search()` (query DB) vs `filtered()` (in-memory) trong Exercise 1
> ✅ Đã tự sửa và làm lại đúng sau khi được hướng dẫn
> 💡 Tip: Nhớ `search()` = query DB, `filtered()` = in-memory filter

### 5.4 Lưu ý cho ngày tiếp theo
> 🚀 **Sẵn sàng cho Day 3**: create/write/unlink + Form View
> 💪 Nền tảng vững: Day 1 (Recordset) + Day 2 (Transform/Filter) → Day 3 sẽ học CRUD lifecycle
> 🎯 Focus: Apply recordset knowledge vào data manipulation
> 💡 Tip: Thêm fields (state, price) vào library.book để practice Day 3 tốt hơn

---

## 🔄 14 ↔ 19 DIFFERENCES

| Aspect | Odoo 14 | Odoo 17/19 | Notes |
|--------|---------|------------|-------|
| `mapped()` | Giống | Giống | API không đổi |
| `filtered()` | Giống | Giống | API không đổi |
| `sorted()` | Giống | Giống | API không đổi |
| Performance | Good | Better | Odoo 17+ optimize recordset operations |
