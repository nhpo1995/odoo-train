# 📋 DAILY LESSON PLAN TEMPLATE (v2.0)

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
| **Ngày** | Day __ of 21 |
| **Chủ đề** | <!-- PLANNER: Điền chủ đề chi tiết --> |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | <!-- PLANNER: Liệt kê days cần hoàn thành trước --> |
| **Mục tiêu chính** | <!-- PLANNER: 1-2 câu mô tả mục tiêu đo lường được --> |

---

## 📦 MODULE PROGRESS (Trainer phải đọc!)

<!-- 
PLANNER: Section này giúp Trainer hiểu đây là module BUILD XUYÊN SUỐT,
không phải chỉ là ví dụ đơn thuần.
-->

### 📍 Trước Day [X]
<!-- PLANNER: Module có gì từ days trước -->
- [Liệt kê features đã có từ days trước]

### ✅ Sau Day [X] (Hôm nay)
<!-- PLANNER: Module sẽ có thêm gì sau ngày này -->
- [Liệt kê features sẽ thêm hôm nay]

### ⭐ Production Target (Từ Roadmap)
<!-- PLANNER: Nhắc lại vision từ roadmap -->
```
Task Management Module sẽ có:
- 3 Models: task.project, task.task, task.tag
- Views: Tree, Form, Kanban, Search
- Security: Manager vs Member
- Workflows, Computed fields, Reports
```

### 🔗 Đây là ngày [X]/19 của việc build complete module

---

## 🎯 LEARNING OBJECTIVES

By end of day, learner will be able to:
<!-- PLANNER: 5-7 objectives measurable -->
- [ ] Objective 1: [Cụ thể, đo lường được]
- [ ] Objective 2: [...]
- [ ] Objective 3: [...]
- [ ] Objective 4: [...]
- [ ] Objective 5: [...]

---

## 📊 COVERAGE CHECKLIST (For Planner - MUST verify)

- [ ] Context7 queried (min 2 queries documented in 1.4)
- [ ] Source code line numbers verified
- [ ] 10-15 concepts covered (basic + advanced)
- [ ] 5+ complex exercises (multi-step, real-world)
- [ ] 8-10 questions (mixed Easy/Medium/Hard)
- [ ] Advanced topics section filled
- [ ] Gotchas/Common mistakes documented
- [ ] Performance considerations included

---

## Section 1: NỘI DUNG BÀI HỌC

### 1.1 Lý thuyết cần dạy

<!-- PLANNER: 
REQUIREMENTS:
- Minimum 10 concepts total
- Each concept: Core + Examples + When to use + Gotchas
- Use Context7 for best practices & advanced patterns
- Include code examples from source + Context7
-->

#### 🟢 Core Concepts (Basic - Must know)

- [ ] **Concept 1: [Tên chi tiết]**
  - **Core explanation**: (Chi tiết ≥5 dòng, không chỉ định nghĩa)
  - **Syntax/Usage**:
    ```python
    # Basic example từ source hoặc Context7
    ```
  - **When to use**: [Use cases cụ thể]
  - **Comparison**: vs [SQLAlchemy/FastAPI equivalent if relevant]

<!-- Lặp lại pattern cho Concept 2-7 -->

#### 🟡 Advanced Topics (Nice to have)

- [ ] **Advanced 1: [Tên pattern/technique]**
  - **Deep dive**: (Giải thích chi tiết advanced usage)
  - **Example**:
    ```python
    # Complex real-world example
    ```
  - **Edge cases**: [Các trường hợp đặc biệt]
  - **Performance**: [Implications và optimization tips]

<!-- Lặp lại cho Advanced 2-3 -->

#### ⚠️ Gotchas & Common Mistakes (Critical)

- **Mistake 1: [Mô tả lỗi phổ biến]**
  - ❌ Wrong way: `code example`
  - ✅ Correct way: `code example`
  - Why: [Giải thích tại sao]

- **Mistake 2: [...]**
  - ❌ Wrong: ...
  - ✅ Correct: ...
  - Why: ...

<!-- List 3-5 gotchas -->

### 1.2 Source code cần đọc

<!-- PLANNER: 
- File path chính xác (relative từ odoo root)
- Class/Method name
- EXACT line range (verified!)
- Focus point cụ thể
-->

| File | Class/Method | Line range | Focus |
|------|--------------|------------|-------|
| `odoo/models.py` | `BaseModel.[method]` | L____ - L____ | [Điểm CỤ THỂ cần chú ý] |
| `odoo/[...]` | `[...]` | L____ - L____ | [...] |

### 1.3 Kiến thức liên quan

<!-- PLANNER: Map concepts với Python/FastAPI/SQLAlchemy background -->

| Odoo Concept | Tương đương Python/Framework | Khác biệt quan trọng |
|--------------|------------------------------|---------------------|
| [Concept 1] | [Python equivalent] | [Key difference] |
| [Concept 2] | [...] | [...] |

### 1.4 Context7 Research Notes

<!-- PLANNER: MANDATORY - Document insights từ queries -->

**Query 1**: `[exact query text]`
```
Library: [library ID used]
Key insights:
- Insight 1: [...]
- Insight 2: [...]
- Best practice discovered: [...]
```

**Query 2**: `[exact query text]`
```
Library: [library ID]
Key insights:
- Advanced pattern: [...]
- Gotcha discovered: [...]
```

---

## Section 2: THỰC HÀNH

### 2.1 Bài tập code

<!-- PLANNER:
REQUIREMENTS:
- Minimum 5 exercises
- Progressive difficulty: Basic → Intermediate → Advanced
- Multi-step scenarios
- Include error handling
- Real-world contexts
-->

**Exercise 1: [Basic - Single Concept] - Warmup**

**Scenario**: [1-2 dòng context thực tế]

**Requirements**:
1. [Specific task using concept X]
2. [Expected behavior]

**Expected Input**: [Cụ thể]
**Expected Output**: [Cụ thể với example]

**Hints** (Optional):
- [Hint nếu cần]

---

**Exercise 2: [Intermediate - Combine 2-3 Concepts]**

**Scenario**: [Real-world scenario 2-3 dòng]

**Requirements** (Multi-step):
1. Step 1: [Task A using concept X]
2. Step 2: [Task B building on A, using concept Y]
3. Step 3: [Task C combining X+Y]

**Constraints**:
- Must handle empty recordsets
- [Other constraints]

**Expected Output**: [Detailed expected result]

**Hints**:
- For step 1: [...]
- For step 2: [...]

---

**Exercise 3-4: [Advanced - Real-world Scenarios]**

**Scenario**: [Complex real-world task từ job requirements]

**Requirements**:
- [Multi-step complex task]
- [Performance consideration]
- [Error handling required]
- [Edge cases to handle]

**Expected behavior**:
- [Detailed expectations]

**Challenges**:
- Challenge 1: [...]
- Challenge 2: [...]

--- 

**Exercise 5: [Expert - Design Challenge]**

**Scenario**: [Open-ended real problem]

**Goal**: [What to achieve]

**Constraints**:
- [Technical constraints]
- [Performance requirements]

**Self-assessment**:
- Does it work for edge case X?
- Is it performant for Y records?

### 2.2 Shell commands

<!-- PLANNER: Specific commands để test concepts trong shell -->

```python
# Purpose: Test concept X basic usage
[command 1]

# Purpose: Test edge case Y
[command 2]

# Purpose: Compare performance: method A vs B
[command 3]

# Purpose: Debug scenario Z
[command 4]
```

### 2.3 Debug tasks

<!-- PLANNER: Realistic debug scenarios -->

- [ ] **Debug 1: Find the bug**
  - Scenario: [Mô tả tình huống]
  - Buggy code:
    ```python
    # Code with subtle bug
    ```
  - Expected: [What should happen]
  - Actual: [What actually happens]
  - Hint: [Related to concept X]

- [ ] **Debug 2: Performance issue**
  - Scenario: [Slow code scenario]
  - Problem code:
    ```python
    # Inefficient implementation
    ```
  - Issue: [Why it's slow]
  - Goal: Optimize using [concept Y]

### 2.4 Real-World Scenarios

<!-- PLANNER: Map exercises to actual job tasks -->

**Scenario A: Custom Frontend Task**
- **Task description**: [Từ job requirement]
- **Concepts used**: [List concepts X, Y, Z]
- **Expected outcome**: [What learner should achieve]
- **Difficulty**: [Intermediate/Advanced]

**Scenario B: Fix Bug Task**
- **Bug description**: [Real bug pattern]
- **Debug approach**: [Steps to identify]
- **Solution approach**: [High-level solution using concepts]
- **Prevention**: [How to avoid in future]

---

## Section 3: KIỂM TRA KIẾN THỨC

### 3.1 Câu hỏi self-check

<!-- PLANNER: 
REQUIREMENTS:
- 8-10 questions total
- Mix difficulty: Easy (recall) → Medium (apply) → Hard (analyze)
- Include scenario-based questions
-->

#### 🟢 Easy (Recall - Q1-3)

1. Define [concept X]. What does it return?
2. List [Y types of Z]. What is each used for?
3. What is the syntax for [operation A]?

#### 🟡 Medium (Apply - Q4-6)

4. Compare [X] vs [Y]. When would you use each?
5. What happens if you [scenario]? Why?
6. How would you [achieve goal] using [concept]?

#### 🔴 Hard (Analyze - Q7-10)

7. **Scenario**: You have [complex situation]. How would you solve it? Consider [constraints].

8. **Debug**: This code has a bug. Find it and explain why it's wrong:
   ```python
   # Buggy code
   ```

9. **Design**: Given requirements [A, B, C], design a solution. Explain your choice of [concepts/patterns].

10. **Optimize**: This code works but is inefficient:
    ```python
    # Slow code
    ```
    Why is it slow? How would you optimize it?

### 3.2 Đáp án

<details>
<summary>Xem đáp án</summary>

#### Easy Answers:

1. **[Question 1]**
   - Answer: [Chi tiết]
   - Why: [Giải thích]
   - Related concept: [Link to concept in 1.1]

<!-- Lặp lại cho Q2-3 -->

#### Medium Answers:

4. **[Question 4]**
   - Comparison:
     - X: [Characteristics, when to use]
     - Y: [Characteristics, when to use]
   - Rule of thumb: [Decision guide]

<!-- Lặp lại Q5-6 -->

#### Hard Answers:

7. **[Scenario question]**
   - Approach: [Step-by-step solution]
   - Concepts used: [X, Y, Z]
   - Trade-offs: [Considerations]
   - Alternative: [Other approach if applicable]

<!-- Lặp lại Q8-10 -->

</details>

---

## Section 4: TIÊU CHÍ HOÀN THÀNH

<!-- PLANNER: Strict, measurable criteria -->

| Tiêu chí | Đạt | Chưa đạt |
|----------|-----|----------|
| Giải thích được [core concept 1] với ví dụ | ⬜ | ⬜ |
| Viết được code sử dụng [concept 2] không lỗi | ⬜ | ⬜ |
| Phân biệt được [X] vs [Y] và khi nào dùng | ⬜ | ⬜ |
| Hoàn thành exercises 1-3 đúng | ⬜ | ⬜ |
| Debug được bài tập debug 1 | ⬜ | ⬜ |
| Hiểu gotchas [liệt kê] và cách tránh | ⬜ | ⬜ |
| Trả lời đúng ≥7/10 câu hỏi | ⬜ | ⬜ |

---

## Section 5: ĐÁNH GIÁ (AI Mentor điền sau khi dạy)

### 5.1 Kết quả học tập
| Block | Điểm (/10) | Ghi chú |
|-------|------------|---------|
| Lý thuyết | _ | _(Mentor điền)_ |
| Thực hành | _ | _(Mentor điền)_ |
| Kiểm tra | _ | _(Mentor điền)_ |
| **TỔNG** | **_/10** | |

### 5.2 Key takeaways
<!-- MENTOR: Ghi những gì learner đã nắm được -->
> _(Mentor điền)_

### 5.3 Điểm cần cải thiện
<!-- MENTOR: Ghi những gì cần ôn lại -->
> _(Mentor điền)_

### 5.4 Lưu ý cho ngày tiếp theo
<!-- MENTOR: Chuẩn bị gì cho day kế tiếp -->
> _(Mentor điền)_

---

## 🔄 14 ↔ 19 DIFFERENCES

<!-- PLANNER: Chỉ ra differences nếu có, để learner aware -->

| Aspect | Odoo 14 | Odoo 17/19 | Impact | Notes |
|--------|---------|------------|--------|-------|
| [Feature X] | [Behavior] | [New behavior] | [Low/Medium/High] | [Migration notes] |

---

## 🔗 CONTINUITY (Trainer phải đọc!)

<!-- 
PLANNER: Section này giúp Trainer hiểu tính liên tục giữa các ngày.
Module được build dần dần, không phải exercises riêng lẻ.
-->

### ⬅️ Ngày này builds on
<!-- PLANNER: Liệt kê concepts/features từ days trước được sử dụng hôm nay -->
- Day [X-1]: [Feature/concept sử dụng hôm nay]
- Day [X-2]: [Feature/concept sử dụng hôm nay]

### ➡️ Ngày tiếp theo sẽ thêm
<!-- PLANNER: Preview ngày tiếp theo -->
- Day [X+1]: [Feature/concept sẽ thêm]

### 🏁 Nhắc lại Roadmap Target
Sau 21 ngày, learner sẽ có module `task_management` **production-ready** với:
- Full CRUD + Relationships (M2O, O2M, M2M)
- Complete UI (Tree, Form, Kanban, Search)
- Security (ACL, Groups, Record Rules)
- Business Logic (Computed, Constraints, Workflows)
- Reports (QWeb PDF)

> ⚠️ **Trainer**: Mỗi ngày là một bước trong việc build module hoàn chỉnh, KHÔNG phải exercises riêng lẻ!
