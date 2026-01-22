# 📋 Day 7 Teaching Session Log

> **Start Time**: 2026-01-20 16:06
> **Status**: 🟡 In Progress
> **Day Topic**: Computed Fields + @api.depends

---

## ✅ Pre-Teaching Preparation

### 0.0 Module Spec Reference
- [x] Read `.agent/learning/module_spec.md`
- [x] Day 7 targets confirmed:
  - task.project: task_count (compute, Integer)
  - task.task: hours_remaining (compute, Float)
  - task.task: progress (compute, Float)
  - task.task: is_overdue (compute, Boolean) ← ĐÃ CÓ ahead of schedule

### 0.1 Pre-Teaching Checklist
- [x] Learning objectives understood (8 objectives)
- [x] Concepts counted: **12 concepts**
- [x] Source files identified: **5 source files**
- [x] Exercises reviewed: **5 exercises**
- [x] Questions prepared: **10 questions**
- [x] Gotchas noted: 7 common mistakes

### 0.2 Current Code State (BEFORE Day 7)
**task.py (131 lines):**
- ✅ is_overdue = computed, @api.depends('due_date', 'state')
- ✅ has_urgent_tags = computed, @api.depends('tag_ids', 'tag_ids.name')
- ❌ hours_remaining = NOT YET
- ❌ progress = NOT YET

**project.py (21 lines):**
- ✅ task_ids = One2many
- ❌ task_count = NOT YET

---

## 📚 Session Content Tracking

### STEP 2: Source Code Reading
| # | File | Focus | Status |
|---|------|-------|--------|
| 1 | odoo/api.py | def depends() L185-207 | [ ] |
| 2 | odoo/api.py | def depends_context() L210-233 | [ ] |
| 3 | odoo/fields.py | class Field L116-280 | [ ] |
| 4 | odoo/fields.py | _setup_regular_full() L432-463 | [ ] |
| 5 | odoo/fields.py | resolve_depends() L639-674 | [ ] |

### STEP 3: Concepts Teaching
| # | Concept | Status |
|---|---------|--------|
| 1 | Computed Field Basics | [ ] |
| 2 | @api.depends Decorator | [ ] |
| 3 | store=True vs store=False | [ ] |
| 4 | compute_sudo Parameter | [ ] |
| 5 | inverse Method | [ ] |
| 6 | search Method | [ ] |
| 7 | @api.depends_context | [ ] |
| 8 | Cross-Model Dependencies | [ ] |
| 9 | Recursive Dependencies | [ ] |
| 10 | Related Fields Shortcut | [ ] |
| 11 | Field Recomputation Triggers | [ ] |
| 12 | Common Pitfalls & Debugging | [ ] |

### STEP 4: Exercises
| # | Exercise | Status |
|---|----------|--------|
| 1 | Add task_count to task.project | [ ] |
| 2 | Add hours_remaining to task.task | [ ] |
| 3 | Add progress with inverse | [ ] |
| 4 | Add search method for is_overdue | [ ] |
| 5 | Cross-model computed field | [ ] |

### STEP 5: Questions
| # | Level | Question | Correct? |
|---|-------|----------|----------|
| 1 | Easy | store default | [ ] |
| 2 | Easy | @api.depends usage | [ ] |
| 3 | Easy | inverse use case | [ ] |
| 4 | Medium | Debug: not updating | [ ] |
| 5 | Medium | O2M performance | [ ] |
| 6 | Medium | search method | [ ] |
| 7 | Medium | Missing assignment | [ ] |
| 8 | Hard | related vs compute | [ ] |
| 9 | Hard | total_revenue design | [ ] |
| 10 | Hard | Subtask progress | [ ] |

---

## 📊 Session Summary (To be filled at end)

| Metric | Value |
|--------|-------|
| Source files read | _/5 |
| Concepts taught | _/12 |
| Exercises completed | _/5 |
| Questions correct | _/10 |
| **Total Score** | _/10 |

### Session Notes
> _(To be filled during/after session)_

### Evaluation
| Tiêu chí | Weight | Điểm (/10) | Ghi chú |
|----------|--------|------------|---------|
| Hiểu computed vs regular fields | 15% | _ | |
| @api.depends usage correct | 20% | _ | |
| store=True/False decision | 15% | _ | |
| inverse method implementation | 15% | _ | |
| search method implementation | 10% | _ | |
| Debug computed issues | 15% | _ | |
| Trả lời câu hỏi (8+ correct) | 10% | _ | |
| **TỔNG** | **100%** | **_** | |
