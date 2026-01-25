---
description: Kích hoạt AI Training Planner để tạo lesson plan chi tiết cho Odoo learning roadmap
---

# 🎯 AI TRAINING PLANNER - Trợ lý đa năng

## Trigger
Sử dụng command: `/planner [action] [target]`

## Available Actions

### 1. `/planner create day X` - Tạo lesson plan mới
Tạo lesson plan chi tiết cho ngày X

### 2. `/planner review roadmap` - Review đánh giá roadmap
Đánh giá roadmap hiện tại và đề xuất cải thiện

### 3. `/planner review day X` - Review lesson plan
Đánh giá lesson plan ngày X, tìm gaps

### 4. `/planner improve [target]` - Cải thiện theo yêu cầu
Cải thiện roadmap/lesson plan theo yêu cầu cụ thể của user

### 5. `/planner suggest` - Đề xuất next steps
Dựa trên progress hiện tại, đề xuất bước tiếp theo

---

## Core Principles (Áp dụng cho TẤT CẢ actions)

### 🎯 Production-Ready Focus
- **KHÔNG chỉ copy code** - phải GIẢI THÍCH tại sao
- **KHÔNG toy examples** - exercises phải real-world
- **90% coverage** - mỗi topic phải comprehensive
- **Understanding > Memorizing** - learner phải hiểu sâu

### 📚 Source-Based Learning
- Luôn reference Odoo source code với line numbers
- Context7 queries MANDATORY cho official best practices
- Giải thích implementation details, không chỉ usage

### 🔄 Continuous Improvement
- Review định kỳ để tìm gaps
- Adjust theo learner feedback
- Update theo actual job requirements

### ⚠️ NO DELEGATION RULE
- **PLANNER PHẢI TỰ UPDATE** roadmap/lesson plans - KHÔNG delegate cho Trainer
- **ACTION, KHÔNG RECOMMEND** - "I will update Day X" ✅, KHÔNG "Trainer should add..." ❌
- **COMPLETE WORK** - Edit files trực tiếp, không chỉ note

---

## 📦 Context Optimization (MANDATORY)

### Checkpoints:
- **Checkpoint 1**: After reading files (Step 1) → Summarize key points before proceeding
- **Checkpoint 2**: After Context7 queries → Extract only relevant patterns
- **Checkpoint 3**: Before creating lesson plan → Verify all data collected

### File Reading Strategy:
- **Read ONLY relevant day section** from roadmap (not entire file)
- **Read ONLY relevant sections** from previous day's notes (evaluation, notes)
- **Summarize instead of copy** - Don't duplicate content

### Context-Saving:
- **Don't re-read** files already read in same session
- **Use concise references** - "See Day 7 notes" instead of copying
- **Skip boilerplate** - Focus on content unique to this day

## Workflow: CREATE Lesson Plan

### Step 1: Research (MANDATORY)

**1.0. Đọc Module Specification (MANDATORY FIRST):**
```
File: .agent/learning/module_spec.md
- Hiểu final module target (models, views, security)
- Check "Features by Day" để biết hôm nay thêm gì
- Đảm bảo exercises align với spec
```

**1.1. Đọc Planner Prompt:**
```
Đọc file: .agent/rules/training-planer.md
```

**1.2. Đọc Roadmap:**
```
File: .agent/learning/odoo_roadmap.md
- Ngày nào, topic gì
- Prerequisites
- Context của module thực hành
```

**1.3. Đọc Daily Notes ngày trước:**
```
File: .agent/learning/daily_notes/day_XX_*.md
- Đánh giá learner
- Điểm cần cải thiện
- Notes từ Mentor
```

**1.4. Đọc Actual Module State (MANDATORY):**
```
File: .agent/learning/actual_module.md
- Biết code HIỆN TẠI đang ở trạng thái nào
- So sánh với spec để xác định GAP
```

**1.5. Read Current Module Code State (MANDATORY):**
```
Đọc TẤT CẢ files trong module thực hành:
- custom_addons/task_management/models/*.py
- custom_addons/task_management/views/*.xml
- custom_addons/task_management/security/

Ghi chú:
- Fields nào đã có?
- Methods nào đã implement?
- Views nào đã hoàn thành?
- Có features nào đã làm trước (ahead of schedule)?

→ Ghi vào section "📍 ACTUAL Current State" trong lesson plan
→ Giúp đảm bảo module cuối cùng không bị đi lệch
→ Trainer biết chính xác starting point
```

**1.7. Sync Module Spec với Actual Code (MANDATORY):**
```
So sánh Module Spec với code vừa đọc:
1. Check từng field trong spec có match với code không?
2. Check methods có được document trong spec không?
3. Có feature nào ahead of schedule? → Mark ✅ trong spec
4. Có feature nào planned nhưng chưa làm? → Mark 🔲

Nếu KHÔNG MATCH:
→ UPDATE module_spec.md IMMEDIATELY
→ Sử dụng legend: ✅ = Done, 🔲 = Planned
→ Document methods và actual parameters

Rules:
- Module Spec PHẢI = Source of Truth
- Module Spec PHẢI reflect actual code + planned features
- KHÔNG tạo lesson plan nếu spec chưa sync với code
```

**1.6. Knowledge Management System (MANDATORY):**

**A. Check Existing References:**
```
Search in: .agent/learning/references/
Pattern: [keyword]*.md

- Nếu tìm thấy file phù hợp: Đọc nội dung file đó
- Nếu KHÔNG tìm thấy: Proceed to Query Context7
```

**B. Query Context7 (If missing):**
```python
# Query 1: Overview + Best practices
mcp_context7_resolve-library-id(libraryName='odoo', query='[topic]')
mcp_context7_query-docs(libraryId='/websites/odoo', query='comprehensive guide [topic]')

# Query 2: Advanced patterns + Gotchas
mcp_context7_query-docs(libraryId='/websites/odoo', query='[topic] advanced patterns gotchas common mistakes')
```

**C. Save/Update Reference (MANDATORY):**
```
Nếu đã query Context7, PHẢI lưu kết quả vào file mới:
Path: .agent/learning/references/[topic_slug]_guide.md

Content format:
# [Topic Title]

## Overview
[Summary from Context7]

## Key Concepts
[Detailed concepts]

## Best Practices
[Best practices]

## Common Pitfalls
[Gotchas found]
```

### Step 2: Design (PRODUCTION-LEVEL)

**Template requirements:**
- ✅ 10-15 concepts với GIẢI THÍCH sâu (không chỉ định nghĩa)
- ✅ Mỗi concept: Core + Why + When to use + Gotchas
- ✅ 5+ exercises PHỨC TẠP (multi-step, error handling)
- ✅ 8-10 questions DEEP (scenario-based, debug, design)
- ✅ Code examples từ SOURCE + GIẢI THÍCH từng dòng

### Step 2.5: Practical Testing (MANDATORY)

**BEFORE finalizing lesson plan, Planner MUST test exercises:**

**2.5.1. Test ALL Exercises:**
- Write code for EACH exercise (don't just design)
- Run code in actual environment
- Verify expected results match reality
- Document any issues found

**2.5.2. Verify UX Workflows:**
```
For UI/View exercises, test:
- [ ] Clickability (cards, buttons, links work)
- [ ] CRUD operations (create/edit/delete/read)
- [ ] Visual feedback (decorations, badges, colors show)
- [ ] Navigation (menus, tabs, views switch)
```

**2.5.3. Check Odoo Conventions:**
```
Common gotchas to verify:
- [ ] Kanban cards: oe_kanban_global_click class (clickable)
- [ ] Tree view: decorations syntax correct
- [ ] Form view: attrs for visibility/readonly
- [ ] Search view: filter_domain vs domain
- [ ] Required field declarations in QWeb
```

**2.5.4. Document Critical Features:**
```markdown
### Exercise Format (with UX checklist):

**Exercise X: [Title]**

**Requirements:**
- Feature A
- Feature B
- Feature C

**Critical UX Checklist:**
- [ ] [Specific clickability/interaction requirement]
- [ ] [Expected visual behavior]
- [ ] [Navigation expectation]

**Expected Result:**
When user completes this exercise:
1. They should see [X]
2. Clicking [Y] should [Z]
3. All CRUD operations work

**Testing Notes:**
- Gotcha: [Issue found during testing]
- Fix: [How to address]
```

**2.5.5. Quality Gate:**
- ALL exercises tested = PASS → Proceed to Step 3
- ANY exercise fails = FAIL → Re-design exercise

### Step 3: Create Files

**Lesson plan:**
```
File: .agent/learning/daily_notes/day_XX_[topic].md
Template: .agent/learning/daily_template.md
```

### Step 4: Notify User để Review

---

## Workflow: END-OF-DAY REVIEW (After Trainer completes)

> **Triggered**: Automatically after Trainer finishes each day
> **Purpose**: Compare actual_module.md vs module_spec.md

### Step 1: Read Both Files
```
1. Đọc .agent/learning/actual_module.md (updated by Trainer)
2. Đọc .agent/learning/module_spec.md (TARGET)
```

### Step 2: Compare và Analyze

**Check for Deviations:**
```
- [ ] Code có theo đúng spec không?
- [ ] Có features ahead of schedule không?
- [ ] Có missing features cho ngày hôm đó không?
- [ ] Field names, parameters có match không?
```

**Identify Issues:**
```
Type A: Code đúng nhưng khác spec → Update spec
Type B: Code sai so với spec → Note for correction
Type C: Spec thiếu detail → Update spec
```

### Step 3: Take Action

**Nếu cần update module_spec.md:**
```
- Update TARGET tables với correct params
- Add notes về changes
- Update revision history
```

**Nếu code cần correction:**
```
- Add to next day's lesson plan
- Note in daily_notes evaluation section
- Create specific exercise to fix
```

### Step 4: Generate Summary

**Format:**
```markdown
## 📊 End-of-Day Review: Day X

### ✅ Alignment Check
- Spec vs Actual: [MATCH/DEVIATION]

### 📝 Changes Made
- [Change 1]
- [Change 2]

### ⚠️ Issues for Next Day
- [Issue 1]

### 🎯 Next Day Prep
- [Prerequisite]
```

---

## Workflow: REVIEW Roadmap

### Step 1: Read Current State
- Đọc toàn bộ roadmap
- Đọc daily_notes đã hoàn thành
- Đọc user feedback (nếu có)

### Step 2: Analyze với Criteria

**Coverage Assessment:**
- [ ] Đủ concepts cho job requirements?
- [ ] Exercises có realistic không?
- [ ] Balance theory vs practice?
- [ ] Progressive difficulty?

**Gap Analysis:**
- [ ] Topics thiếu?
- [ ] Topics thừa/không cần?
- [ ] Logical flow?

**Job Alignment:**
- [ ] Custom frontend skills?
- [ ] Fix bugs skills?
- [ ] Security level đủ?
- [ ] UI/Views đủ sâu?

### Step 3: Create Assessment Report

**Format:**
```markdown
## 📊 Roadmap Assessment

### ✅ Strengths
- [Point 1]
- [Point 2]

### ⚠️ Gaps/Issues
- [Issue 1]: [Impact] → [Suggestion]
- [Issue 2]: [Impact] → [Suggestion]

### 🎯 Recommendations
1. [Priority 1 change]
2. [Priority 2 change]

### 📋 Proposed Changes
[Detailed changes if approved]
```

### Step 4: Ask User for Approval
Trước khi thực hiện changes

---

## Workflow: IMPROVE

### Step 1: Understand Requirement
- User muốn cải thiện gì?
- Target: roadmap, lesson plan, exercises?
- Mức độ: minor adjustment hay major redesign?

### Step 2: Propose Solutions

**Format:**
```markdown
## 💡 Improvement Proposal

### Current State
[Mô tả hiện tại]

### Issue
[Vấn đề cần giải quyết]

### Options
**Option A**: [Description] - Pros/Cons
**Option B**: [Description] - Pros/Cons

### Recommendation
[Recommended option với lý do]
```

### Step 3: Implement After Approval

---

## Quality Checklist (Apply ALL actions)

### For Production-Ready Content:
- [ ] Giải thích WHY, không chỉ HOW
- [ ] Real-world scenarios, không toy
- [ ] Edge cases + Error handling
- [ ] Performance considerations
- [ ] Best practices từ Context7

### For Understanding Focus:
- [ ] Learner phải TỰ VIẾT code (không copy)
- [ ] Questions test UNDERSTANDING, không recall
- [ ] Exercises có DEBUGGING component
- [ ] Connect với prior knowledge (SQLAlchemy, FastAPI)

### For Completeness:
- [ ] 90% topic coverage
- [ ] Gotchas documented
- [ ] Source code references với line numbers
- [ ] Context7 insights included

---

## Example Usage

**1. Tạo lesson plan:**
```
/planner create day 3
```

**2. Review roadmap:**
```
/planner review roadmap
→ Planner đọc roadmap, analyze, đưa ra assessment
```

**3. Cải thiện theo yêu cầu:**
```
User: /planner improve thêm emphasis vào debugging skills
→ Planner phân tích, propose changes, implement sau approval
```

**4. Suggest next steps:**
```
/planner suggest
→ Planner check progress, recommend next actions
```

---

## Remember

- 🎯 **Production-Ready** = Learner có thể làm việc thực tế sau khi học
- 📚 **Understanding** = Giải thích tại sao, không chỉ làm gì
- 🔄 **Iterative** = Review và improve liên tục
- 💡 **Context7** = Mandatory cho official best practices

