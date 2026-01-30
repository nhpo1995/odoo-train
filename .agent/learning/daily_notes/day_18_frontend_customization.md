# 📋 Day 18 - Frontend Customization (CSS/JS & QWeb)

> **Mode**: ⚡ ACCELERATED - Focus on "Heavy Custom Views" (CSS/JS/XPath)
> **Duration**: 7 giờ
> **Goal**: Can thiệp sâu vào giao diện, tạo custom widgets và style.

---

## 📋 THÔNG TIN CHUNG

| Field | Value |
|-------|-------|
| **Ngày** | Day 18 of 21 |
| **Chủ đề** | **Frontend Assets, JS Widgets, QWeb Inheritance** |
| **Thời lượng** | 7 tiếng |
| **Prerequisites** | Day 17 (Views), Day 15 (XPath) |
| **Mục tiêu chính** | "Làm đẹp" và "Hack" giao diện mặc định của Odoo |

---

## 🎯 LEARNING OBJECTIVES

By end of session:
- [ ] Hiểu cơ chế **Assets Bundles** (`web.assets_backend`).
- [ ] Inject **Custom CSS/SCSS** để sửa giao diện Odoo.
- [ ] Viết **JS Field Widget** cơ bản (kết nối Python data với JS UI).
- [ ] Sử dụng **QWeb Inheritance** để sửa cấu trúc Kanban/Report (khác với View Inheritance).

---

## Section 1: CONCEPTS (2 giờ)

### 1.1 Assets Management
- `__manifest__.py` vs `assets.xml` (Odoo 14 vs 15+ differences).
- `web.assets_backend`: Bundle chính cho giao diện nội bộ.
- Debug mode `?debug=assets`: Load file thô để debug.

### 1.2 QWeb Inheritance (`<xpath>` for Templates)
- Khác với View (Form/Tree) Inheritance.
- Dùng để sửa nội dung bên trong thẻ `<templates>` của Kanban hoặc Report.
- Syntax: `<xpath expr="//t[@t-name='kanban-box']//div[...]" position="...">`.

### 1.3 Javascript Field Widgets
- Class `AbstractField` / `DebouncedField`.
- Cơ chế: `init` -> `start` -> `render`.
- Đăng ký widget: `field_registry.add('my_widget', MyWidget);`.
- Sử dụng: `<field name="..." widget="my_widget"/>`.

---

## Section 2: EXERCISES (4.5 giờ)

### 🟢 Exercise 1: CSS Injection - "Overdue Red Alert" (60 phút)
**Target**: Task nào trễ hạn (`is_overdue`) thì Kanban Card chuyển màu nền đỏ nhạt.
1. Tạo file `static/src/css/task_style.css`.
2. Đăng ký vào `web.assets_backend`.
3. Sửa Kanban View: Thêm class `o_task_overdue` dựa trên field `is_overdue`.
4. Viết CSS: `.o_kanban_record.o_task_overdue { background-color: #ffebee; }`.

### 🟡 Exercise 2: QWeb Inheritance - "Kanban Progress Bar" (90 phút)
**Target**: Chèn một thanh progress bar vào **bên trong** Kanban Card của `task.project` mà không viết lại cả view.
1. Tìm template gốc của Project Kanban.
2. Dùng `<xpath>` để inject HTML `<progress>` bar vào sau tên Project.
3. Stylize bằng CSS.

### 🔴 Exercise 3: JS Widget - "Color Picker Badge" (120 phút)
**Target**: Tạo widget chọn màu (Click để đổi màu) cho field `color` của tag.
1. Tạo `static/src/js/color_widget.js`.
2. Extend `AbstractField`.
3. Render: Các hình tròn màu.
4. Events: Click hình tròn -> Gọi `_setValue`.
5. Áp dụng vào Form View của `task.tag`.

---

## Section 3: DEBUGGING SKILLS (0.5 giờ)

- [ ] Cách dùng **Browser DevTools** để CSS nhanh.
- [ ] Debug JS: `debugger;` statement và Console.
- [ ] Cache issues: Khi nào cần Regenerate Assets Bundle?

---

## Section 4: CHECKLIST FOR TRAINER

1. **Setup**: Đảm bảo file static được load đúng (Check Network tab).
2. **Version**: Odoo 14 JS syntax (dùng `require`, ko phải ES6 modules của Odoo 17).
3. **Syntax**: Check kỹ đóng mở thẻ trong QWeb và dấu `;` trong CSS.

---

## ✅ TIÊU CHÍ HOÀN THÀNH

| Tiêu chí | Đạt |
|----------|-----|
| Style CSS nhận diện được class động | ⬜ |
| Widget JS hoạt động (click đổi data) | ⬜ |
| Không lỗi JS console (trắng trang) | ⬜ |
