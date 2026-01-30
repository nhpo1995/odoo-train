# 📋 Day 17 - View Masterclass (Advanced Reporting)

> **Mode**: ⚡ ACCELERATED - Focus on "Heavy Custom Views" requirement
> **Duration**: 7 giờ
> **Goal**: Tạo các View báo cáo chuyên nghiệp (Graph, Pivot, Dashboard)

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 17 of 21 (View Masterclass) |
| **Chủ đề** | **Advanced Views: Graph, Pivot, Calendar, Dashboard** |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Day 6 (Relationships), Day 16 (Inheritance) |
| **Mục tiêu chính** | Biến data thô thành báo cáo "sếp thích xem" |

---

## 🎯 LEARNING OBJECTIVES

By end of session:
- [ ] Master **Graph View** (Bar, Line, Pie)
- [ ] Master **Pivot View** (Excel-like analysis)
- [ ] Master **Calendar View** (Schedule management)
- [ ] Tạo **Dashboard Actions** (Ghép nhiều view)
- [ ] Thêm **Smart Buttons** vào Form View

---

## Section 1: CONCEPTS (1.5 giờ)

### 1.1 Graph View (`<graph>`)
- Dùng để visualize data. `type="bar"`, `stacked="True"`.
- Attributes: `type`, `sample` (hiện data mẫu khi trống).
- Tags: `<field name="..." type="measure"/>` (Số liệu), `<field name="..." type="row"/>` (Trục X).

### 1.2 Pivot View (`<pivot>`)
- Bảng xoay chiều (giống Excel).
- Rất mạnh cho báo cáo tổng hợp.
- Attributes: `disable_linking` (không click để xem record).

### 1.3 Calendar View (`<calendar>`)
- Hiển thị task theo time.
- Attributes: `date_start`, `date_stop`, `color` (phân loại màu), `mode` (month/week/day).

### 1.4 Smart Button / Stat Button
- Nút bấm trên đầu Form View hiển thị số liệu thống kê.
- Pattern:
```xml
<div class="oe_button_box" name="button_box">
    <button class="oe_stat_button" icon="fa-tasks">
        <field name="task_count" widget="statinfo"/>
    </button>
</div>
```

---

## Section 2: EXERCISES (5 giờ)

### 🟢 Exercise 1: Calendar View (45 phút)
**Target**: Xem Task trên lịch theo `due_date`.
- Tạo view `task_task_view_calendar`.
- Hiện Task name.
- Màu sắc theo `project_id`.
- Thêm filter "My Tasks" vào search view làm mặc định.

### 🟢 Exercise 2: Graph View - Task Analytics (45 phút)
**Target**: Biểu đồ cột (Bar Chart).
- Trục X: `project_id`.
- Measure: `hours_estimated` vs `hours_spent`.
- Group by: `state`.
- Yêu cầu: Stacked Bar Chart.

### 🟡 Exercise 3: Pivot View - Performance Report (60 phút)
**Target**: Báo cáo hiệu suất team.
- Rows: `assigned_user_id`.
- Cols: `create_date` (Month).
- Measures: Count, Sum `hours_spent`.
- Default: Expand all rows.

### 🟡 Exercise 4: Smart Button on Project (60 phút)
**Target**: Nút "Tasks" trên Project Form.
- Mở `task.project` form view (inherit hoặc sửa file cũ).
- Thêm `oe_button_box`.
- Button hiển thị số lượng tasks (`task_count` field - đã làm ở Day 7).
- Action: Click vào nhảy sang Tree View các task của project đó.

### 🔴 Exercise 5: Dashboard Action (90 phút)
**Target**: Một Menu "Dashboard" riêng biệt.
- Tạo `ir.actions.act_window` mode `graph,pivot`.
- Khi click menu "Dashboard", mặc định mở Graph view.
- Tạo Search Filter mặc định "This Month".

---

## Section 3: ADVANCED CHALLENGE (Cuối ngày)

### Exercise 6: Cohort View (Optional - Nếu cài Enterprise)
*Lưu ý: Odoo Community không có Cohort/Gantt view mặc định.*
Thay vào đó: **Custom Search Panel**.
- Thêm `<searchpanel>` vào bên trái Tree View.
- Filter nhanh theo `Project`, `Status`, `Tags` (có icon).

---

## Section 4: CHECKLIST FOR TRAINER

1. **Verify**: User có hiểu sự khác biệt giữa `store=True` field và computed field trong Pivot view không? (Pivot cần stored field để nhanh).
2. **Review**: XML syntax của user (đóng tag, attributes).
3. **UX**: Màu sắc Graph view có hợp lý không?

---

## ✅ TIÊU CHÍ HOÀN THÀNH

| Tiêu chí | Đạt |
|----------|-----|
| Calendar view chạy mượt (kéo thả task) | ⬜ |
| Graph view hiển thị đúng 2 cột measure | ⬜ |
| Pivot view filter được theo ngày tháng | ⬜ |
| Smart button link đúng action | ⬜ |
