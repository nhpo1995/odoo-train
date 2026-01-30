# 📋 DAILY LESSON PLAN: Day 11 - ACL (Access Control List)

> **Hướng dẫn cho AI Training Planner:**
> 1. Đọc `odoo_roadmap.md` để hiểu overview của ngày cần plan
> 2. **MANDATORY**: Query Context7 ≥2 lần để lấy best practices
> 3. Copy template này thành file mới: `day_XX_[topic].md`
> 4. Điền chi tiết vào các phần `<!-- PLANNER: ... -->`
> 5. AI Mentor sẽ dùng file này để dạy và fill phần Đánh giá

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 11 of 21 |
| **Chủ đề** | **ACL (Access Control List) - Model-level Security** |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Day 10 (Context, sudo()), Basic understanding of Groups |
| **Mục tiêu chính** | Master ACL to control who can CRUD which models in task_management |

---

## 📦 MODULE PROGRESS (Trainer phải đọc!)

### 📍 Trước Day 11 (Day 10 hoàn thành ở máy khác)
- **task.task**: Full model với constraints, computed fields, wizard
- **task.project**: Image, Manager, Relations, total_revenue
- **Reports**: QWeb PDF report (từ Day 10)
- **Security**: Chỉ có basic ACL cho `base.group_user` (tất cả permissions)

### ✅ Sau Day 11 (Hôm nay)
- **Security Groups**: Định nghĩa `group_manager` và `group_member`
- **ACL Refinement**: Phân quyền CRUD theo groups
- **Testing**: Hiểu AccessError và cách debug

### ⭐ Production Target (Từ Roadmap)
```
Task Management Module Security:
- Manager: Full CRUD tất cả models
- Member: Read all, Create tasks, Write own tasks, No Delete
```

### 🔗 Đây là ngày 11/21 - Bắt đầu Phase 3 (Security)

---

## 🎯 LEARNING OBJECTIVES

By end of day, learner will be able to:
- [ ] Hiểu ACL là MODEL-level security (không phải record-level)
- [ ] Viết file `ir.model.access.csv` chuẩn format
- [ ] Định nghĩa Security Groups trong XML
- [ ] Phân biệt ACL vs Record Rules (Day 12)
- [ ] Debug AccessError và hiểu cách Odoo check permissions
- [ ] Test permissions với different users

---

## 📊 COVERAGE CHECKLIST (For Planner - MUST verify)

- [x] Context7 queried (ACL best practices)
- [x] Source code line numbers verified (IrModelAccess L1692-1869)
- [x] 10 concepts covered (ACL structure, Groups, Permissions)
- [x] 5 complex exercises (Create groups, refine ACL, test)
- [x] 8 questions (mixed difficulty)
- [x] Advanced topics covered (Programmatic check, sudo bypass)
- [x] Gotchas documented (empty group_id, no ACL warning)

---

## Section 1: NỘI DUNG BÀI HỌC

### 1.1 Lý thuyết cần dạy

#### 🟢 Core Concepts (Basic - Must know)

1. **Concept 1: ACL là gì?**
   - **Core**: ACL = Access Control List, kiểm soát ai được CRUD model nào
   - **Scope**: MODEL-level, không phải record-level (đó là Record Rules - Day 12)
   - **Rule**: Không có ACL = Không ai access được (trừ admin), logs sẽ warning

2. **Concept 2: ir.model.access.csv Format**
   - **Core**: File CSV định nghĩa permissions
   - **Columns**:
     ```csv
     id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
     ```
   - **model_id:id**: Prefix `model_` + model name (dots → underscores)
     - `task.task` → `model_task_task`
   - **Values**: `1` = allowed, `0` = denied

3. **Concept 3: Security Groups (res.groups)**
   - **Core**: Tập hợp users có cùng permissions
   - **XML Definition**:
     ```xml
     <record id="group_task_manager" model="res.groups">
         <field name="name">Task Manager</field>
         <field name="category_id" ref="base.module_category_hidden"/>
     </record>
     ```
   - **Hierarchy**: Groups có thể implied từ group khác (inheritance)

4. **Concept 4: group_id:id trong ACL**
   - **Empty**: Global access (thường cho public models)
   - **base.group_user**: Internal Users (employees)
   - **base.group_public**: Public visitors
   - **Custom**: `task_management.group_task_manager`

5. **Concept 5: Permission Stacking**
   - **Rule**: Permissions là ADDITIVE (OR logic)
   - **Example**: User thuộc 2 groups → lấy MAX permissions của cả 2
   - **Design**: Tạo groups riêng để restrictive

6. **Concept 6: AccessError Exception**
   - **When**: User không có permission thực hiện operation
   - **Message**: Cho biết operation nào bị denied, groups nào có quyền
   - **Debug**: Check logs "Access Denied by ACLs"

7. **Concept 7: Registering ACL in __manifest__.py**
   - **Location**: `data` key (được load khi install/update)
   - **Order**: Security files nên load trước views
   - **Example**:
     ```python
     'data': [
         'security/security.xml',       # Groups first
         'security/ir.model.access.csv', # ACL second
         'views/...',
     ],
     ```

#### 🟡 Advanced Topics (Nice to have)

8. **Concept 8: Programmatic Access Check**
   - **Method**: `self.check_access('write')` - raises AccessError if denied
   - **User check**: `self.env.user.has_group('module.group_name')`
   - **When**: Trong business logic cần verify before sensitive operations

9. **Concept 9: sudo() Bypass**
   - **Core**: `sudo()` bypasses ACL completely
   - **Caution**: Chỉ dùng khi system operations, không phải user actions
   - **Remember**: From Day 10 - sudo() cho backend, không cho user-facing

10. **Concept 10: IrModelAccess.check() Method**
    - **Location**: `odoo/addons/base/models/ir_model.py` L1767-1834
    - **Logic**:
      1. Check if superuser → allow all
      2. Check user's groups for model + mode
      3. Check global rules (empty group_id)
      4. Raise AccessError if denied

#### ⚠️ Gotchas & Common Mistakes (Critical)

- **Mistake 1: Empty group_id = All users**
  - ❌ Think: Empty = no one
  - ✅ Reality: Empty = EVERYONE (including unauthenticated!)
  - Fix: Always specify group for internal models

- **Mistake 2: Forgot to register CSV in manifest**
  - ❌ File exists nhưng không load
  - ✅ Check `__manifest__.py` data list
  - Symptom: "No access rights" warning in logs

- **Mistake 3: Wrong model_id format**
  - ❌ `task.task` → sai
  - ✅ `model_task_task` → đúng
  - Rule: `model_` prefix + replace `.` with `_`

- **Mistake 4: Confusing ACL with Record Rules**
  - ❌ Use ACL to hide specific records
  - ✅ ACL = model level, Record Rules = record level
  - Day 12 will cover Record Rules

### 1.2 Source code cần đọc

| File | Class/Method | Line range | Focus |
|------|--------------|------------|-------|
| `odoo/addons/base/models/ir_model.py` | `IrModelAccess` | L1692-1705 | Fields definition |
| `odoo/addons/base/models/ir_model.py` | `IrModelAccess.check()` | L1767-1834 | Core check logic |
| `odoo/addons/base/security/ir.model.access.csv` | - | Toàn file | Real examples |
| `odoo/addons/project/security/project_security.xml` | Groups | - | Group definition examples |

### 1.3 Kiến thức liên quan

| Odoo Concept | Tương đương Python/Framework | Khác biệt quan trọng |
|--------------|------------------------------|---------------------|
| ACL | Role-based Access Control (RBAC) | CSV-based, additive permissions |
| res.groups | User Roles | XML-defined, can inherit (implied) |
| AccessError | HTTPException(403) | More descriptive message |
| check_access() | @require_permission decorator | Explicit method call |

### 1.4 Context7 Research Notes

**Query 1**: `ACL access control list ir.model.access csv security permissions`
```
Library: /websites/odoo
Key insights:
- ACL file defines permissions per model per group
- No ACL = no access (warning in logs)
- Use check_access('write') for programmatic checks
```

**Query 2**: Source code analysis
```
Library: odoo/addons/base/models/ir_model.py
Key insights:
- IrModelAccess.check() cached per user/model/mode
- Permission check: specific group rules first, then global (empty group)
- Error message includes which groups have access
```

---

## Section 2: THỰC HÀNH

### 2.1 Bài tập code

**Exercise 1: Analyze Current ACL**

**Scenario**: Module đã có basic ACL. Phân tích và hiểu structure.

**Requirements**:
1. Mở file `custom_addons/task_management/security/ir.model.access.csv`
2. Identify: Có bao nhiêu models? Groups nào được assign?
3. Trả lời: Với ACL hiện tại, user "demo" có thể delete task không?

**Expected Output**: Hiểu rõ current ACL state

---

**Exercise 2: Create Security Groups**

**Scenario**: Tạo 2 groups: Manager (full access) và Member (limited access)

**Requirements**:
1. Tạo file `security/security.xml`
2. Define 2 groups:
   - `group_task_manager`: Task Manager
   - `group_task_member`: Task Member
3. Manager implied Member (manager có tất cả quyền của member + thêm)
4. Register file trong `__manifest__.py` TRƯỚC `ir.model.access.csv`

**Expected Output**:
```xml
<record id="group_task_member" model="res.groups">
    <field name="name">Task Member</field>
    <field name="category_id" ref="base.module_category_hidden"/>
</record>

<record id="group_task_manager" model="res.groups">
    <field name="name">Task Manager</field>
    <field name="category_id" ref="base.module_category_hidden"/>
    <field name="implied_ids" eval="[(4, ref('group_task_member'))]"/>
</record>
```

---

**Exercise 3: Refine ACL Permissions**

**Scenario**: Phân quyền theo groups:
- **Manager**: Full CRUD tất cả models
- **Member**: task.task (CRUD), task.project (Read only), task.tag (Read only)

**Requirements**:
1. Sửa file `ir.model.access.csv`
2. Remove old entries
3. Add new entries với proper groups

**Expected Output**:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
# Manager - Full Access
access_task_task_manager,task.task manager,model_task_task,task_management.group_task_manager,1,1,1,1
access_task_project_manager,task.project manager,model_task_project,task_management.group_task_manager,1,1,1,1
access_task_tag_manager,task.tag manager,model_task_tag,task_management.group_task_manager,1,1,1,1

# Member - Limited Access
access_task_task_member,task.task member,model_task_task,task_management.group_task_member,1,1,1,0
access_task_project_member,task.project member,model_task_project,task_management.group_task_member,1,0,0,0
access_task_tag_member,task.tag member,model_task_tag,task_management.group_task_member,1,0,0,0
```

---

**Exercise 4: Test Permissions with Demo User**

**Scenario**: Verify ACL works correctly

**Requirements**:
1. Upgrade module: `-u task_management`
2. Login as "demo" user (có thể cần tạo)
3. Add demo to `group_task_member`
4. Test:
   - Can read projects? ✓
   - Can create project? ✗ (should AccessError)
   - Can create task? ✓
   - Can delete task? ✗ (should AccessError)

**Expected Behavior**: AccessError messages khi denied

---

**Exercise 5: Programmatic Access Check**

**Scenario**: Thêm explicit check trong action method

**Requirements**:
1. Trong `task.task`, thêm method `action_admin_only()`
2. Method check nếu user là Manager trước khi execute
3. Raise UserError nếu không phải Manager

**Expected Code**:
```python
def action_admin_only(self):
    if not self.env.user.has_group('task_management.group_task_manager'):
        raise UserError('Only Managers can perform this action!')
    # ... rest of logic
```

---

### 2.2 Shell commands

```python
# Check user's groups
self.env.user.groups_id.mapped('name')

# Check if user has specific group
self.env.user.has_group('task_management.group_task_manager')

# Check ACL for model
self.env['ir.model.access'].check('task.task', 'unlink', raise_exception=False)

# See which groups have access to model
self.env['ir.model.access'].group_names_with_access('task.task', 'write')

# Test as different user (admin context)
demo = self.env.ref('base.user_demo')
self.env['task.task'].with_user(demo).check_access('unlink')
```

### 2.3 Debug tasks

- [ ] **Debug 1: Find why user can't access model**
  - Scenario: User reports "You are not allowed to access..."
  - Steps:
    1. Check logs: "Access Denied by ACLs"
    2. Check which groups have access
    3. Check if user in correct group
    4. Verify CSV format correct

- [ ] **Debug 2: ACL not loading**
  - Scenario: Changed CSV but permissions không thay đổi
  - Checklist:
    1. File registered in `__manifest__.py`?
    2. Module upgraded (`-u`)?
    3. CSV format correct (no typos)?
    4. Check server logs for errors

---

## Section 3: KIỂM TRA KIẾN THỨC

### 3.1 Câu hỏi self-check

#### 🟢 Easy (Recall - Q1-3)

1. ACL controls access at which level: Model or Record?
2. What prefix is used for `model_id:id` in CSV? (e.g., for `sale.order`)
3. If `group_id:id` is empty, who can access?

#### 🟡 Medium (Apply - Q4-6)

4. Compare ACL vs Record Rules. When use which?
5. Write CSV entry: `project.task` model, `base.group_user` group, read-only.
6. User is in 2 groups: one allows write, one denies. What happens?

#### 🔴 Hard (Analyze - Q7-8)

7. **Scenario**: User can see model in menu but gets AccessError when clicking. Debug steps?

8. **Design**: You need:
   - Public users: read-only products
   - Portal users: read-only orders
   - Internal users: full CRUD
   
   Design the ACL structure.

### 3.2 Đáp án
<details>
<summary>Xem đáp án</summary>

1. **Model level**. Record-level là Record Rules.

2. **model_sale_order**. Prefix `model_` + replace dots with underscores.

3. **Everyone** including unauthenticated users. Dangerous for internal models!

4. **ACL** = Model-level (can user access ANY record of this model?). **Record Rules** = Record-level (WHICH specific records can user see?). Use ACL first, then refine with Record Rules.

5. ```csv
   access_project_task_user,project.task user,model_project_task,base.group_user,1,0,0,0
   ```

6. **User can write**. Permissions are ADDITIVE (OR logic). Most permissive wins.

7. Debug steps:
   - Check logs for "Access Denied"
   - `ir.model.access.group_names_with_access(model, 'read')` - which groups have access?
   - Check if user is in correct group
   - Verify CSV format and model name

8. Design:
   ```csv
   # Public - read products
   access_product_public,product public,model_product_product,base.group_public,1,0,0,0
   # Portal - read orders
   access_order_portal,order portal,model_sale_order,base.group_portal,1,0,0,0
   # Internal - full CRUD
   access_product_user,product user,model_product_product,base.group_user,1,1,1,1
   access_order_user,order user,model_sale_order,base.group_user,1,1,1,1
   ```

</details>

---

## ✅ Section 4: TIÊU CHÍ HOÀN THÀNH

| Tiêu chí | Đạt | Chưa đạt |
|----------|-----|----------|
| Hiểu ACL là model-level security | ⬜ | ⬜ |
| Viết được ir.model.access.csv đúng format | ⬜ | ⬜ |
| Tạo được Security Groups trong XML | ⬜ | ⬜ |
| Test được permissions với different users | ⬜ | ⬜ |
| Debug được AccessError | ⬜ | ⬜ |
| Phân biệt ACL vs Record Rules (concept) | ⬜ | ⬜ |
| Trả lời đúng ≥6/8 câu hỏi | ⬜ | ⬜ |

---

## 📝 Section 5: ĐÁNH GIÁ (AI Mentor điền sau khi dạy)

### 5.1 Kết quả học tập
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Lý thuyết | _ | _(Mentor điền)_ |
| Thực hành | _ | _(Mentor điền)_ |
| Kiểm tra | _ | _(Mentor điền)_ |
| **TỔNG** | **_/10** | |

### 5.2 Key takeaways
> _(Mentor điền)_

### 5.3 Điểm cần cải thiện
> _(Mentor điền)_

### 5.4 Lưu ý cho ngày tiếp theo
> _(Mentor điền)_

---

## 🔄 14 ↔ 19 DIFFERENCES

| Aspect | Odoo 14 | Odoo 17/19 | Impact | Notes |
|--------|---------|------------|--------|-------|
| ACL format | Same | Same | None | CSV format unchanged |
| Groups | Same | Same | None | XML definition same |

---

## 🔗 CONTINUITY (Trainer phải đọc!)

### ⬅️ Ngày này builds on
- Day 10: `sudo()` để bypass ACL (sẽ test contrast)
- Day 6: Relationships (models cần ACL)

### ➡️ Ngày tiếp theo sẽ thêm
- Day 12: **Record Rules** - Record-level security (filter WHICH records)
- Day 13: Multi-company, Security Debug

### 🏁 Nhắc lại Roadmap Target
Sau 21 ngày, learner sẽ có module `task_management` **production-ready** với:
- Full CRUD + Relationships (M2O, O2M, M2M)
- Complete UI (Tree, Form, Kanban, Search)
- **Security (ACL, Groups, Record Rules)** ← PHASE 3 BẮT ĐẦU
- Business Logic (Computed, Constraints, Workflows)
- Reports (QWeb PDF)

> ⚠️ **Note cho Trainer**: Day 10 code (Reports) có thể chưa có trên máy này. Day 11 KHÔNG phụ thuộc vào Report code, chỉ cần hiểu `sudo()` concept từ Day 10.
