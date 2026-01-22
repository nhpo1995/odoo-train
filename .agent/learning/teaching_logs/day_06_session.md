# 📋 Day 6: Relational Fields - Teaching Session

> **Date Started:** 2026-01-19  
> **Learner:** Phong  
> **Topic:** Many2one, One2many, Many2many + Command Patterns  
> **Status:** ✅ Completed

---

## 📊 Session Summary

| Metric | Value |
|--------|-------|
| Started | 2026-01-19 11:27 |
| Completed | 2026-01-20 15:25 |
| Duration | ~2 days (with breaks) |
| Score | 9.0/10 🌟 |

---

## ✅ Pre-Teaching Preparation
- [x] Read Module Spec (`module_spec.md`)
- [x] Read Lesson Plan (`day_06_relational_fields.md`)
- [x] Verify current code state (task.py, project.py)
- [x] Prepare teaching materials

---

## 📖 PHẦN 1: Source Code Reading

### Source 1: class Many2one (L2548-2750) ✅
- [x] Learner đọc class definition + docstring
- [x] Hiểu column_type = int4 (tạo DB column)
- [x] Hiểu ondelete logic (cascade/restrict/set null)
- [x] Hiểu tất cả 7 attributes: comodel_name, domain, context, ondelete, auto_join, delegate, check_company
- [x] ✅ **Confirmed understanding** (Quick check: 3/3 đúng, sai syntax 1 lần)

### Source 2: class One2many (L3090-3373) ✅
- [x] Learner đọc class definition
- [x] Hiểu inverse_name parameter (tên M2O field ở model kia)
- [x] Hiểu O2M là virtual field (KHÔNG tạo DB column)
- [x] Hiểu limit parameter
- [x] ✅ **Confirmed understanding** (Quick check: 3/3 đúng)

### Source 3: class Many2many (L3375-3650) ✅
- [x] Learner đọc class definition
- [x] Hiểu relation table tự động tạo (format: {table1}_{table2}_rel)
- [x] Hiểu column1, column2 parameters
- [x] Hiểu ondelete chỉ có cascade/restrict (không có set null)
- [x] Hiểu auto_join và khi nào dùng
- [x] ✅ **Confirmed understanding** (Quick check: 1/3 đúng, sai _rel→_ref và comodel_name)

### Source 4: Command Patterns (L2935-2953) ✅
- [x] Learner đọc convert_to_cache method
- [x] Hiểu 7 commands: CREATE(0), UPDATE(1), DELETE(2), UNLINK(3), LINK(4), CLEAR(5), SET(6)
- [x] Hiểu tuple format: (code, id, values)
- [x] Hiểu LINK = set.add(id) - thêm vào tập không duplicate
- [x] ✅ **Confirmed understanding**

### Source 5: sale_order.py (Real usage - Optional)
- [ ] Review production patterns

---

## 📚 PHẦN 2: Concepts (7 concepts từ lesson plan)

| # | Concept | Status | Notes |
|---|---------|--------|-------|
| 1 | Many2one Field (M2O) - FK Relationship | ✅ | Hiểu column_type, ondelete, domain |
| 2 | One2many Field (O2M) - Virtual Reverse | ✅ | Hiểu inverse_name, virtual field |
| 3 | Many2many Field (M2M) - N:N Relationship | ✅ | Hiểu relation table, column1/2 |
| 4 | Command Patterns (CREATE/UPDATE/DELETE/LINK/UNLINK/CLEAR/SET) | ✅ | Thực hành trong shell |
| 5 | Dot Notation Access & Lazy Loading | ✅ | Hiểu N+1 problem |
| 6 | View Integration (Form/Tree/Kanban) | ✅ | many2many_tags, t-foreach |
| 7 | ACL cho Model mới (task.tag) | ✅ | Thêm ACL, fix Access Denied |

---

## 🔧 PHẦN 3: Exercises (5 từ lesson plan)

| # | Exercise | Status | Notes |
|---|----------|--------|-------|
| 1 | Tạo model task.tag (name, color, ACL, views) | ✅ | Hoàn thành |
| 2 | Thêm M2O vào task.task (project_id, assigned_user_id) | ✅ | ondelete, default |
| 3 | Thêm O2M vào task.project (task_ids, manager_id) | ✅ | inverse_name đúng |
| 4 | Thêm M2M và update Kanban (tag_ids) | ✅ | Fix circular relation |
| 5 | Master Command Patterns (Shell practice) | ✅ | link, create, set, clear |

---

## ❓ PHẦN 4: Questions (10 câu từ lesson plan)

### Easy (3 câu)
| # | Question | Correct? |
|---|----------|----------|
| 1 | M2O tạo column trong DB không? O2M thì sao? | ✅ |
| 2 | Viết M2O field link đến res.users với default=env.user | ✅ |
| 3 | ondelete='cascade' nghĩa là gì? Cho 2 examples | ✅ |

### Medium (4 câu)
| # | Question | Correct? |
|---|----------|----------|
| 4 | Debug: O2M luôn trả về empty recordset. 3 nguyên nhân? | ✅ |
| 5 | Viết code: thêm 2 tags mới, link 1 tag có sẵn, xóa 1 tag trong 1 write | ✅ |
| 6 | Khi nào dùng M2M vs model trung gian? | ✅ |
| 7 | Tại sao task.tag cần ACL? Điều gì nếu quên? | ✅ |

### Hard (3 câu)
| # | Question | Correct? |
|---|----------|----------|
| 8 | N+1 query problem: giải thích + code BAD/GOOD | ✅ |
| 9 | Design: Employee-Department-Skills (với level attribute) | ✅ |
| 10 | check_company=True làm gì? | ✅ |

**Score:** 10/10 correct 🌟

---

## 📊 PHẦN 5: Evaluation

| Tiêu chí | Weight | Điểm (/10) | Ghi chú |
|----------|--------|------------|---------|
| Hiểu M2O/O2M/M2M differences | 20% | 10 | Nắm chắc bản chất DB & Virtual |
| Implement relational fields | 20% | 9 | Code tốt, 1 lỗi syntax |
| Command patterns thành thạo | 15% | 8 | Cần practice thêm |
| Update views correctly | 15% | 9 | many2many_tags, t-foreach |
| Debug relational issues | 15% | 9 | Fix circular M2M |
| Trả lời câu hỏi (8+ correct) | 15% | 10 | 10/10 câu + Bonus |
| **TỔNG** | **100%** | **9.0/10** | **XUẤT SẮC** 🌟 |

---

## 📝 Session Notes

### Observations
> - Learner đọc source kỹ, hỏi nhiều câu hay về context vs domain
> - Hiểu được sự khác biệt giữa domain (filter data) và context (change behavior)
> - Cần thời gian để hiểu syntax, ban đầu viết sai `Many2one('cascade')` thay vì `Many2one('task.project', ondelete='cascade')`
> - Hỏi câu hay về M2M: "Có cần field ở cả 2 model không?" → Trả lời không, có thể dùng search
> - Nhầm lẫn `_rel` với `_ref` trong tên auto-generated table
> - Nhầm comodel_name `task.task` thay vì `task.tag` cho tag_ids field

### Learner Strengths
> - Đặt câu hỏi phản biện tốt (vd: "context có thay đổi UI không?")
> - Nhận ra lỗi trong ví dụ của trainer (show_archived nên dùng domain không phải context)

### Areas to Improve
> - Syntax của field definition (comodel_name là positional, ondelete là keyword)
> - LINK concept cần giải thích rõ hơn: "LINK = set.add(id) - thêm vào tập không duplicate"

### Recommendations for Next Day
> - Review lại Command patterns trước Day 7
