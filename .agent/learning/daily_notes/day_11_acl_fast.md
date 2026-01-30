# 📋 Day 11 - ACL Security (FAST-TRACK + Essential)

> **Mode**: ⚡ ACCELERATED - Job-critical skills với essential knowledge
> **Goal**: Viết được ACL và debug AccessError

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 11 of 21 (Fast-track) |
| **Chủ đề** | **ACL (Access Control List)** |
| **Thời lượng** | 3-4 tiếng |
| **Prerequisites** | Day 10 (sudo() concept) |
| **Mục tiêu chính** | Viết được ir.model.access.csv, tạo groups, debug ACL |

---

## ⚡ FAST-TRACK FOCUS

**Skip** (advanced):
- IrModelAccess source code deep dive
- Programmatic access checks (self.check_access)

**Keep** (essential):
- ✅ ir.model.access.csv format
- ✅ Security groups với implied_ids
- ✅ group_id types (base.group_user, etc.)
- ✅ AccessError debug
- ✅ 4 Common gotchas

---

## 🎯 LEARNING OBJECTIVES

By end of session:
- [ ] Hiểu ACL = MODEL-level security
- [ ] Viết được ir.model.access.csv
- [ ] Tạo được security groups
- [ ] Debug được AccessError
- [ ] Tránh được 4 common mistakes

---

## Section 1: CONCEPTS (8 concepts)

### Concept 1: ACL là gì? (5 phút)

- **ACL** = Access Control List
- **Scope**: MODEL-level (ai được CRUD model nào)
- **NOT**: Record-level (đó là Record Rules - Day 12)
- **Rule**: Không có ACL = KHÔNG ai access được (trừ admin)

### Concept 2: ir.model.access.csv Format (10 phút)

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_task_task_user,task.task access,model_task_task,base.group_user,1,1,1,1
```

| Column | Meaning | Example |
|--------|---------|---------|
| `id` | Unique ID | `access_task_task_user` |
| `name` | Description | `task.task access` |
| `model_id:id` | `model_` + model name | `model_task_task` |
| `group_id:id` | Group hoặc empty | `base.group_user` |
| `perm_*` | Permission flags | `1` = allowed, `0` = denied |

### Concept 3: Security Groups (10 phút)

```xml
<!-- security/security.xml -->
<odoo>
    <record id="group_task_member" model="res.groups">
        <field name="name">Task Member</field>
        <field name="category_id" ref="base.module_category_hidden"/>
    </record>

    <record id="group_task_manager" model="res.groups">
        <field name="name">Task Manager</field>
        <field name="implied_ids" eval="[(4, ref('group_task_member'))]"/>
    </record>
</odoo>
```

**Key**: `implied_ids` = Manager kế thừa tất cả quyền của Member

### Concept 4: group_id Types (5 phút) ⭐ Important

| Group | Who | Use for |
|-------|-----|---------|
| _(empty)_ | **EVERYONE** | ⚠️ Dangerous! Only for truly public |
| `base.group_public` | Public visitors | Website public pages |
| `base.group_portal` | Portal users | Customer portal |
| `base.group_user` | Internal users | Most internal models |
| `module.group_custom` | Custom group | Your defined groups |

### Concept 5: Permission Stacking (5 phút)

- Permissions là **ADDITIVE** (OR logic)
- User thuộc 2 groups → lấy **MAX** permissions của cả 2
- Design tip: Tạo groups restrictive, add permissions via inheritance

### Concept 6: AccessError Exception (10 phút) ⭐ Debug

```
odoo.exceptions.AccessError: 
You are not allowed to modify 'task.task' (task.task) records.
Allowed groups: Task Manager
```

**Debug steps**:
1. Check logs: "Access Denied by ACLs"
2. Xem error message → biết operation nào, groups nào được phép
3. Check user thuộc group nào
4. Verify CSV format và model name

### Concept 7: Register in Manifest (5 phút)

```python
'data': [
    'security/security.xml',       # Groups TRƯỚC
    'security/ir.model.access.csv', # ACL SAU
    'views/...',
],
```

**Order quan trọng**: Groups phải load trước CSV (vì CSV reference groups)

### Concept 8: sudo() Bypass Reminder (3 phút)

```python
# Bypass ACL hoàn toàn
self.sudo().write({'field': value})
```

⚠️ **Caution**: Chỉ dùng cho system operations, KHÔNG cho user-facing actions

---

## ⚠️ 4 COMMON GOTCHAS (Must know!)

### Mistake 1: Empty group_id = EVERYONE
```csv
# ❌ DANGEROUS - Everyone including anonymous can access!
access_task_task_all,task.task all,model_task_task,,1,1,1,1

# ✅ CORRECT - Only internal users
access_task_task_user,task.task user,model_task_task,base.group_user,1,1,1,1
```

### Mistake 2: Forgot to register CSV
- File exists nhưng không load
- Symptom: "No access rights" warning in logs
- Fix: Check `__manifest__.py` data list

### Mistake 3: Wrong model_id format
```csv
# ❌ WRONG
model_id:id = task.task

# ✅ CORRECT
model_id:id = model_task_task
```
Rule: `model_` prefix + replace `.` with `_`

### Mistake 4: Confusing ACL with Record Rules
- **ACL**: Ai được access MODEL (tất cả records)
- **Record Rules**: Ai được access RECORDS nào (filter specific)
- Day 12 sẽ cover Record Rules

---

## Section 2: EXERCISES

### Exercise 1: Analyze Current ACL (10 phút)

Mở `security/ir.model.access.csv`, trả lời:
1. Có bao nhiêu models được define?
2. Group nào được assign?
3. User demo có thể delete task không? Tại sao?

---

### Exercise 2: Create Security Groups (15 phút)

**Task**: Tạo `security/security.xml` với 2 groups:
- `group_task_member`: Task Member
- `group_task_manager`: Task Manager (implied Member)

---

### Exercise 3: Refine ACL Permissions (15 phút)

**Task**: Update `ir.model.access.csv`:

| Group | task.task | task.project | task.tag |
|-------|-----------|--------------|----------|
| Manager | Full CRUD | Full CRUD | Full CRUD |
| Member | R/W/C (no delete) | Read only | Read only |

---

### Exercise 4: Test Permissions (20 phút)

1. Upgrade module: `-u task_management`
2. Tạo user "test_member" → add to group Member
3. Login as test_member
4. Test và verify:
   - ✅ Read projects
   - ❌ Create project → AccessError
   - ❌ Delete task → AccessError

---

### Exercise 5: Debug AccessError (15 phút)

**Scenario**: User báo lỗi "You are not allowed to access..."

**Debug steps**:
1. Reproduce error
2. Check server logs
3. Identify: Model? Operation? Current user's groups?
4. Fix ACL hoặc add user to correct group

---

## Section 3: QUICK CHECK (5 phút)

1. ACL là model-level hay record-level?
2. `task.task` → model_id:id là gì?
3. Empty group_id nghĩa là gì?
4. Permissions stacking: OR hay AND logic?
5. Groups file register trước hay sau CSV?
6. Làm sao biết user thuộc group nào?
7. AccessError message cho biết thông tin gì?

<details>
<summary>Đáp án</summary>

1. **Model-level**
2. `model_task_task`
3. **Everyone** can access - dangerous!
4. **OR logic** - most permissive wins
5. **Groups TRƯỚC** CSV
6. User menu → Groups hoặc `self.env.user.groups_id`
7. Operation denied, groups có quyền, model name

</details>

---

## ✅ TIÊU CHÍ HOÀN THÀNH

| Tiêu chí | Đạt |
|----------|-----|
| Hiểu ACL scope (model vs record) | ✅ (cần ôn lại) |
| Viết được CSV đúng format | ✅ |
| Tạo được groups XML với implied_ids | ✅ |
| Register đúng thứ tự trong manifest | ✅ |
| Test được với demo user | ✅ |
| Debug được AccessError | ✅ |
| Biết 4 common gotchas | ✅ |

---

## 📝 ĐÁNH GIÁ

| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Concepts | 8 | Hiểu implied_ids, OR logic rất tốt. Cần ôn: ACL=model-level |
| Exercises | 9 | Tự viết CSV với permission stacking, test thành công |
| Debug skills | 9 | Debug task.tag AccessError thực tế |
| Questions | 6 | 4/7 đúng - nhầm model vs record level, OR vs AND |
| **TỔNG** | **8/10** | Thực hành tốt, lý thuyết cần ôn thêm |

### Key Takeaways
> - Groups dùng `implied_ids` để kế thừa permissions (OR logic)
> - CSV format: `model_` + replace `.` with `_`
> - Relationships require read access to ALL related models
> - Register groups XML BEFORE CSV in manifest

### Điểm cần cải thiện
> - ACL = MODEL-level (không phải record-level)
> - Permission stacking = OR logic (không phải AND)

---

## 🔗 NEXT

Sau Day 11:
- **Chiều nay**: Day 15 - View Inheritance (XPath)
- **Ngày mai**: Day 16 - Model Inheritance
