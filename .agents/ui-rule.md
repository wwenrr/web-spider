---
description: UI Design System, Color Palette, Typography, and Layout Guidelines
globs: "**/*.{html,erb,css,scss,js,ts,tsx,jsx,rb}"
---

# Chi Tiết Phong Cách UI

## Tổng Quan Phong Cách UI

Giao diện này thể hiện phong cách **Minimalist (Tối giản) hiện đại** với đặc trưng **Clean UI** và **Data-Driven Design**. Đây là thiết kế quản trị (Admin Dashboard) tập trung vào trải nghiệm người dùng, sự rõ ràng và khả năng quét thông tin nhanh chóng.

## Chi Tiết Màu Sắc

### Bảng Màu Chủ Đạo

**Màu nền chính:**
- **Trắng tinh khiết (#FFFFFF)**: Chiếm 85-90% diện tích giao diện, tạo cảm giác thoáng đãng, sạch sẽ.
- Mục đích: Giảm tải nhận thức (cognitive load), tạo không gian thở cho nội dung.

**Màu nhấn chính (Accent Color):**
- **Xanh lá cây mềm mại** (ước lượng #40C57C hoặc #3DB97F): Sử dụng cho sidebar, logo, và nút hành động quan trọng.
- Công dụng:
  - Biểu tượng thương hiệu và nhận diện
  - Nút "Create New" - hành động chính (Primary CTA)
  - Highlight trạng thái hoạt động trong navigation
- Tại sao màu xanh lá: Thể hiện sự tăng trưởng, tin cậy, ổn định và hành động tích cực trong UI/UX.

**Màu phụ và trung tính:**
- **Xám nhạt (#F8F9FA - #FAFAFA)**: Nền của các dòng table xen kẽ (zebra striping).
- **Xám vừa (#6C757D - #7F8C9B)**: Text phụ, mô tả, placeholder.
- **Xám đậm (#212529 - #2D3748)**: Text chính, tiêu đề.
- **Viền nhẹ (#DEE2E6 - #E5E7EB)**: Đường phân cách giữa các dòng và cột.

### Quy Tắc Sử Dụng Màu

1. **Giới hạn 3 màu chủ đạo**: Trắng (nền), Xanh lá (nhấn), Xám (phụ trợ).
2. **Tỷ lệ tương phản WCAG AA**:
   - Text thường: tối thiểu 4.5:1 với nền.
   - Text lớn (18px+): tối thiểu 3:1 với nền.
   - UI components: tối thiểu 3:1.
3. **Màu xanh cho hành động tích cực**: Confirmation, success, create, active state.

## Không Gian Trắng (White Space)

### Nguyên Tắc White Space

**Macro White Space (Không gian lớn):**
- Khoảng cách giữa sidebar và content chính: 24-32px.
- Padding nội dung chính: 32-48px từ các cạnh.
- Khoảng cách giữa các section lớn: 40-56px.

**Micro White Space (Không gian nhỏ):**
- Padding trong table cell: 12-16px (vertical), 16-24px (horizontal).
- Khoảng cách giữa các dòng table: 1px border line.
- Line height cho text: 1.5-1.6 lần font size.
- Khoảng cách giữa icon và text: 8-12px.

### Hệ Thống 8px Grid

**Quy tắc cốt lõi:**
- Tất cả spacing, margin, padding phải là bội số của 8: 8, 16, 24, 32, 40, 48, 56, 64, 80px.
- Ngoại lệ: Có thể dùng 4px cho spacing cực kỳ chặt chẽ.

**Áp dụng cụ thể:**
- Padding nút: 12px (vertical) × 24px (horizontal).
- Margin giữa các thành phần: 16px, 24px, 32px.
- Line height: Bội số của 8 hoặc 4 để kiểm soát typography chính xác.

**Lý do sử dụng 8px:**
- Scalability: Chia hết cho 2, 4, tương thích với mọi độ phân giải màn hình.
- Efficiency: Dễ giao tiếp giữa designer và developer.
- Aesthetics: Tạo rhythm thị giác hài hòa.

**Nguyên tắc Internal ≤ External:**
- Padding bên trong element ≤ Margin bên ngoài element.
- Giúp phân biệt rõ ràng các nhóm và element riêng lẻ.

### Lợi Ích White Space
1. **Cải thiện khả năng đọc**: Giảm visual noise, tăng focus vào nội dung quan trọng.
2. **Tạo visual hierarchy**: Hướng dẫn mắt người dùng theo thứ tự ưu tiên.
3. **Giảm cognitive load**: Ít element hơn = dễ xử lý thông tin hơn.
4. **Tăng tính thẩm mỹ**: Cảm giác sang trọng, hiện đại, tinh tế.

## Typography (Chữ)

### Font Family

**Lựa chọn tối ưu:**
- **Sans-serif fonts**: Dễ đọc trên màn hình, hiện đại, sạch sẽ.
- Các font được khuyến nghị:
  - **Inter**: Universal, variable font, dễ đọc, x-height cao.
  - **Roboto**: Google Material Design standard.
  - **Open Sans**: Phổ biến, an toàn, dễ đọc.
  - **Public Sans**: Neutral, professional.
  - **Manrope**: Modern, geometric.

**Lý do tránh serif fonts:**
- Serif font tạo thêm visual noise không cần thiết trong data table.
- Sans-serif dễ đọc hơn ở kích thước nhỏ trên màn hình.

### Font Size & Weight

**Cấp bậc Typography:**
- **Header chính**: 24-32px, font-weight: 600-700 (semibold/bold).
- **Section title**: 18-20px, font-weight: 600.
- **Table header**: 14-16px, font-weight: 600-700 (bold để phân biệt với data).
- **Body text/Table data**: 14-16px, font-weight: 400 (regular).
- **Secondary text**: 12-14px, font-weight: 400.

**Đặc điểm font tốt cho UI:**
- X-height cao: Phần chữ thường cao, dễ đọc ở kích thước nhỏ.
- Letter spacing thoải mái: Không quá chặt.
- Variable fonts: Tiết kiệm bandwidth, flexible styling.
- Low contrast stroke: Độ dày đồng đều, minimal look.

### Typography Best Practices
1. **KHÔNG dùng ALL CAPS**: Giảm readability nghiêm trọng.
2. **KHÔNG overuse bold và italic**: Tạo visual noise.
3. **Line height**: 1.5-1.6× font size cho body text, 1.2-1.3× cho headings.
4. **Căn chỉnh (Alignment)**:
   - Text: Left-align.
   - Numbers: Right-align (dễ so sánh giá trị).
   - Tiêu đề cột: Match với data bên dưới.

## Bố Cục (Layout)

### Cấu Trúc Tổng Thể

**Left Sidebar Navigation:**
- **Width**: 240-280px (expanded), 56-64px (collapsed).
- **Position**: Fixed, luôn hiển thị.
- **Background**: Màu xanh lá nhạt hoặc trắng với accent xanh.
- **Padding**: 16-24px.

**Main Content Area:**
- **Background**: Trắng tinh khiết.
- **Padding**: 32-48px từ các cạnh.
- **Max-width**: 1440-1600px cho desktop.
- **Margin auto**: Center content khi màn hình rộng.

### Grid System

**12-Column Grid (Bootstrap standard):**
- **Columns**: 12 cột.
- **Gutter**: 24px (1.5rem).
- **Margin**: 60px mỗi bên cho desktop 1440px.
- **Responsive breakpoints**:
  - Mobile: <768px
  - Tablet: 768-1024px
  - Desktop: >1024px

## Thiết Kế Sidebar Navigation

### Cấu Trúc Sidebar
1. **Logo/Brand**: Phía trên cùng, 48-56px height.
2. **Navigation items**: List vertical, icon + text.
3. **Active state**: Background highlight, bold text, accent color.
4. **Hover state**: Subtle background change.
5. **Bottom section**: User profile hoặc updates.

**Spacing trong Sidebar:**
- Padding item: 12px (vertical) × 16px (horizontal).
- Margin giữa items: 4-8px.
- Margin giữa sections: 24-32px.

**Icon Design:**
- Size: 20-24px.
- Style: Line icons, consistent stroke width (1.5-2px).
- Spacing: 12px giữa icon và label.

### Best Practices Sidebar
1. **Optimal width**: 240-300px expanded, 48-64px collapsed.
2. **Highlight active section**: Background, bold text, accent border.
3. **Expandable sub-items**: Chevron icon, smooth animation.
4. **Quick search**: Ở đầu sidebar cho navigation nhanh.
5. **Responsive**: Collapse trên mobile, hamburger menu.

## Thiết Kế Data Table

### Cấu Trúc Table

**Table Header:**
- **Background**: Xám nhạt (#F8F9FA) hoặc trắng với border dày.
- **Text**: Bold (font-weight: 600-700), left-align text, right-align numbers.
- **Padding**: 12-16px vertical, 16-24px horizontal.
- **Border bottom**: 1-2px solid, màu đậm hơn data rows.

**Table Body:**
- **Row height**: 48-56px (thoải mái cho clicking).
- **Cell padding**: 12-16px vertical, 16-24px horizontal.
- **Border**: 1px solid #E5E7EB giữa các dòng.
- **Zebra striping**: Alternating background (#FAFAFA và #FFFFFF).

**Alignment:**
- **Text columns**: Left-align.
- **Number columns**: Right-align.
- **Date columns**: Left-align.
- **Action columns**: Center hoặc right-align.

### Hover & Interactive States

**Row Hover:**
- **Background**: Xám rất nhạt (#F3F4F6).
- **Transition**: 150-200ms ease.
- **Cursor**: Pointer nếu row clickable.
- **Z-index**: Không cần tăng, chỉ background change.

**Implementation Tips:**
- Apply hover lên toàn bộ `<tr>` trong `<tbody>`.
- Dùng class `.table-hover` (Bootstrap) hoặc `:hover` pseudo-class.
- Đảm bảo hover không conflict với button/icon hover bên trong cell.

### Action Buttons trong Table

**Vị trí:**
- **Action column**: Cột cuối cùng bên phải.
- **Alignment**: Right-align hoặc center.

**Thiết kế Button:**
- **Style**: Icon-only buttons hoặc text buttons, KHÔNG dùng filled buttons.
- **Size**: 32-40px (touch-friendly).
- **Spacing**: 8-12px giữa các button.
- **Icons**: View, Edit, Delete, More (3-dot menu).

**Best Practices:**
- **Giới hạn số lượng**: Tối đa 3-4 actions visible, phần còn lại vào dropdown menu.
- **Overflow menu**: Dùng 3-dot icon cho nhiều actions.
- **Hover**: Hiển thị tooltip cho icon-only buttons.
- **Color coding**: Destructive actions (delete) dùng màu đỏ.

### Pagination Design

**Vị trí & Layout:**
- **Position**: Bottom của table, center-aligned.
- **Spacing**: 32-48px margin từ table.

**Thành phần:**
1. **Page numbers**: 1, 2, 3, 4, 5.
2. **Current page**: Bold, background highlight, accent color.
3. **Previous/Next buttons**: "< Previous" và "Next >".
4. **First/Last**: Optional, "« First" và "Last »".
5. **Ellipsis**: "..." cho large page ranges.

**Spacing & Sizing:**
- **Clickable area**: Tối thiểu 40×40px (touch-friendly).
- **Margin giữa items**: 4-8px.
- **Font size**: 14-16px.
- **Border radius**: 4-8px cho page buttons.

**Best Practices:**
1. **Large clickable areas**: 40×40px minimum.
2. **KHÔNG underline**: Gây nhầm lẫn với hyperlinks.
3. **Identify current page**: Bold + background + accent color.
4. **Space out page links**: Đủ khoảng cách để tránh misclick.
5. **Show context**: "Page 5 of 20" hoặc "1-10 of 200 items".
6. **Items per page**: Cho phép user chọn 10, 25, 50, 100.

### Responsive Table Design

**Mobile Strategies:**

**1. Horizontal Scroll (Simplest):**
- Wrap table trong container có `overflow-x: auto`.
- Sticky header khi scroll.

**2. Card Layout (Recommended):**
- Mỗi row thành 1 card vertical.
- Header column thành label cho mỗi field.

**3. Collapsed Columns:**
- Ẩn các cột ít quan trọng trên mobile.
- Cho phép user chọn columns hiển thị.

## Icon Design

### Đặc Điểm Icon

**Style:**
- **Line icons**: Outline style, không fill.
- **Stroke width**: 1.5-2px, consistent.
- **Style**: Minimal, geometric, modern.
- **Corners**: Smooth rounded corners (border-radius: 1-2px).

**Size:**
- **Sidebar navigation**: 20-24px.
- **Table actions**: 16-20px.
- **Buttons**: 16-20px.
- **Large icons**: 32-48px (features, empty states).

**Icon Library Recommendations:**
- **Heroicons**: Clean, consistent, free.
- **Feather Icons**: Minimal, beautiful.
- **Untitled UI Icons**: Professional, 4600+ icons.
- **Lucide**: Modern fork of Feather.

### Icon Usage
1. **Sidebar navigation**: Icon + label cho clarity.
2. **Action buttons**: Icon-only nếu rõ nghĩa (edit, delete, view).
3. **Tooltip**: Luôn có tooltip cho icon-only buttons.
4. **Consistency**: Dùng 1 icon library cho toàn bộ project.
5. **Optical alignment**: Điều chỉnh position để balance với text.

## Button Design

### Button Types

**Primary Button (CTA chính):**
- **Background**: Accent color (xanh lá).
- **Text**: Trắng, font-weight: 600.
- **Padding**: 12px vertical × 24px horizontal.
- **Border radius**: 6-8px.
- **Example**: "Create New" button.

**Secondary Button:**
- **Style**: Outline, border 1-2px solid.
- **Color**: Accent color text + border.
- **Background**: Transparent hoặc hover với background nhạt.
- **Use case**: Actions ít quan trọng hơn.

**Text Button:**
- **Style**: No background, no border.
- **Color**: Accent color hoặc gray.
- **Hover**: Underline hoặc background nhạt.
- **Use case**: Tertiary actions, cancel.

**Icon Button:**
- **Size**: 32-40px (square hoặc circle).
- **Icon**: 16-20px.
- **Background**: Transparent, hover với background.
- **Use case**: Table actions, toolbar.

### Button States

**Default:**
- Màu sắc chuẩn, shadow nhẹ (optional).

**Hover:**
- Background tối hơn 10-15%.
- Cursor: pointer.
- Transition: 150-200ms ease.
- Optional: Subtle scale (1.02) hoặc shadow tăng.

**Active (Pressed):**
- Background tối hơn 20-25%.
- Optional: Scale down (0.98).

**Disabled:**
- Opacity: 0.5-0.6.
- Cursor: not-allowed.
- KHÔNG clickable.
- Có tooltip giải thích tại sao disabled.

**Focus:**
- Outline: 2-3px solid accent color.
- Offset: 2px.
- Đảm bảo keyboard navigation.

### Border Radius Guidelines

**Common Values:**
- **4px**: Subtle, professional, safe choice.
- **6-8px**: Modern, friendly, balanced.
- **12-16px**: Innovative, playful.
- **50% / 100vh**: Fully rounded pill buttons.

**Recommendations:**
- Buttons nhỏ: 4-6px.
- Buttons vừa: 6-8px.
- Buttons lớn: 8-12px.
- Icon buttons: 50% (circle) hoặc 6-8px (rounded square).

**Consistency:**
- Dùng cùng border-radius cho tất cả buttons cùng loại.
- Có thể khác nhau giữa primary và secondary.

## Accessibility (Khả Năng Tiếp Cận)

### Color Contrast

**WCAG AA Requirements:**
- **Regular text (< 18px)**: Minimum 4.5:1 contrast ratio.
- **Large text (≥ 18px hoặc ≥ 14px bold)**: Minimum 3:1.
- **UI components**: Minimum 3:1 (buttons, borders, icons).

**WCAG AAA (Enhanced):**
- **Regular text**: 7:1.
- **Large text**: 4.5:1.

### Keyboard Navigation
1. **Tab order**: Logical, left-to-right, top-to-bottom.
2. **Focus indicators**: Rõ ràng, contrast cao.
3. **Table navigation**: Arrow keys để di chuyển cells.
4. **Skip to content**: Link bỏ qua navigation.

### Screen Reader Support
1. **Semantic HTML**: `<table>`, `<th>`, `<td>`, proper structure.
2. **ARIA labels**: `aria-label`, `aria-describedby` cho icons.
3. **Table headers**: `scope="col"` và `scope="row"`.
4. **Alternative text**: Cho icons và images.

## Quy Tắc Thiết Kế Tổng Hợp

### Visual Hierarchy
1. **Size**: Larger = More important.
2. **Weight**: Bold = More emphasis.
3. **Color**: Accent color = Primary action/info.
4. **Position**: Top-left = Most important (F-pattern).
5. **White space**: More space around = More important.

### Consistency Rules
1. **Spacing**: Luôn dùng 8px grid system.
2. **Colors**: Stick to 3 main colors.
3. **Typography**: Maximum 2-3 font sizes per section.
4. **Icons**: 1 icon library, consistent size.
5. **Border radius**: Same value cho cùng component type.
6. **Shadows**: Subtle, consistent elevation system.

### Performance
1. **Variable fonts**: Reduce font file size.
2. **Icon sprites**: Combine icons into sprite sheet.
3. **Lazy loading**: Load table data on demand.
4. **Virtual scrolling**: For large datasets.
5. **Optimize images**: WebP format, compression.

### Responsive Design

**Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

**Strategies:**
- Sidebar: Collapse to hamburger menu on mobile.
- Table: Card layout hoặc horizontal scroll.
- Padding: Reduce từ 48px (desktop) xuống 16-24px (mobile).
- Font size: Scale down 1-2px on mobile.

### Design System Structure

**Components:**
1. **Atoms**: Buttons, inputs, icons.
2. **Molecules**: Search bar, pagination, table header.
3. **Organisms**: Sidebar, data table, header.
4. **Templates**: Dashboard layout, list page.

**Tokens:**
- **Colors**: Primary, secondary, gray scale.
- **Spacing**: 8px scale.
- **Typography**: Font family, size scale, weights.
- **Shadows**: Elevation system.
- **Border radius**: Small (4px), medium (8px), large (12px).