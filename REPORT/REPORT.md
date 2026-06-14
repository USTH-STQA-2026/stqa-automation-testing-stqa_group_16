# REPORT — Kiểm thử tự động Web UI

**Môn học**: Kiểm thử và Đảm bảo chất lượng phần mềm (STQA)  
**Hệ thống kiểm thử**: Quản lý mượn sách Thư viện ABC — https://stqa.rbc.vn  
**Công cụ**: Python 3 + Playwright + pytest  
**Nhóm**: Group 16 — Lớp 252ICT2012.L1 — HK2 2025-2026

| # | MSSV      | Họ và tên           | Vai trò     |
|---|-----------|---------------------|-------------|
| 1 | 23BA14028 | Vũ Minh Châu        | Nhóm trưởng |
| 2 | 23BA14184 | Nguyễn Minh Lương   | Thành viên  |
| 3 | 23BA14008 | Lương Quỳnh Anh     | Thành viên  |
| 4 | 23BA14183 | Nguyễn Thị Lương    | Thành viên  |
| 5 | 2410042   | Lê Hiền Anh         | Thành viên  |
| 6 | 23BA14167 | Trần Thị Khánh Linh | Thành viên  |

---

## 1. Tổng quan kết quả

| Hạng mục               | Số lượng |
|------------------------|----------|
| Test case bắt buộc     | 12       |
| Test case bonus (B1)   | 3        |
| Tổng test case         | 15       |
| Passed                 | 13       |
| Failed                 | 2        |

**Tỉ lệ pass (bắt buộc):** 12/12 (100%)  
**Tỉ lệ pass (tổng):** 13/15 (87%)

---

## 2. Test case bắt buộc (tests/)

### 2.1 Nhóm Đăng nhập — `test_login.py`

| TC     | Hàm kiểm thử                    | Mô tả kịch bản                                                                     | Kết quả |
|--------|---------------------------------|------------------------------------------------------------------------------------|---------|
| TC-01  | `test_login_success`            | Đăng nhập với email và mật khẩu hợp lệ. Kiểm tra tên hiển thị hoặc nút Đăng xuất xuất hiện. | PASSED  |
| TC-02  | `test_login_fail_wrong_password`| Đăng nhập với mật khẩu sai. Kiểm tra hệ thống không chuyển trang, hiển thị thông báo lỗi.  | PASSED  |
| TC-03  | `test_login_fail_empty_fields`  | Bỏ trống cả hai trường, nhấn Đăng nhập. Kiểm tra hệ thống vẫn ở trang đăng nhập.           | PASSED  |

**Ghi chú kỹ thuật:** Cả ba test case đều áp dụng mô hình RIPR: `page.goto()` (Reachability) → `flutter_fill()` (Infection) → `wait_for_flutter()` (Propagation) → `assert` (Revealability). Oracle ở TC-02 và TC-03 chấp nhận cả hai điều kiện (có thông báo lỗi _hoặc_ vẫn ở trang đăng nhập) để tránh phụ thuộc vào nội dung text cụ thể.

---

### 2.2 Nhóm Tìm kiếm & Lọc sách — `test_search.py`

| TC     | Hàm kiểm thử            | Mô tả kịch bản                                                                                   | Kết quả |
|--------|-------------------------|--------------------------------------------------------------------------------------------------|---------|
| TC-04  | `test_search_book_by_name`   | Tìm kiếm từ khóa "Flutter". Kiểm tra có ít nhất 1 card sách chứa từ khóa đó trong aria-label.   | PASSED  |
| TC-05  | `test_search_book_no_result` | Tìm kiếm từ khóa không tồn tại "xyz_khong_ton_tai_12345". Kiểm tra không có card sách nào hiển thị. | PASSED  |
| TC-06  | `test_filter_by_category`    | Lọc theo thể loại "Công nghệ". Kiểm tra từng card sách đều có "Công nghệ" trong aria-label (Strong Oracle). | PASSED  |
| TC-07  | `test_search_by_author`      | Tìm kiếm tên tác giả "Nguyễn Minh Đức". Kiểm tra có ít nhất 1 kết quả chứa tên tác giả.         | PASSED  |

**Ghi chú kỹ thuật:** TC-06 sử dụng Strong Oracle (vòng lặp kiểm tra từng phần tử) thay vì chỉ kiểm tra `count() > 0` — tương ứng với "Oracle C" trong bài tập lý thuyết BT5. Điều này cho phép phát hiện lỗi bộ lọc trả về sách không đúng thể loại.

---

### 2.3 Nhóm Mượn & Trả sách — `test_borrow_return.py`

| TC     | Hàm kiểm thử         | Mô tả kịch bản                                                                                                          | Kết quả |
|--------|---------------------|-------------------------------------------------------------------------------------------------------------------------|---------|
| TC-08  | `test_borrow_book`  | Tìm sách "Có sẵn", mượn và xác nhận qua dialog. Kiểm tra số sách có thể mượn giảm đi 1 sau thao tác.                   | PASSED  |
| TC-09  | `test_view_borrowed_books` | Chuyển sang tab "Mượn / Trả". Kiểm tra danh sách sách có trạng thái "Đang mượn" và mỗi sách đều có nút "Trả sách". | PASSED  |
| TC-10  | `test_return_book`  | Trong tab "Mượn / Trả", nhấn "Trả sách" trên sách đầu tiên. Kiểm tra số sách đang mượn giảm đi 1.                      | PASSED  |

**Ghi chú kỹ thuật:** TC-09 nâng cấp Oracle từ "kiểm tra text toàn trang" (Weak Oracle — đã comment out) lên "kiểm tra từng card sách có nút Trả sách" (Strong Oracle). TC-10 dùng `page.wait_for_timeout(1500)` do Flutter chưa phát ra signal text ổn định sau khi trả sách — đây là điểm có thể cải thiện bằng một selector chờ cụ thể hơn.

---

### 2.4 Nhóm Chức năng chung — `test_general.py`

| TC     | Hàm kiểm thử                    | Mô tả kịch bản                                                                                      | Kết quả |
|--------|---------------------------------|-----------------------------------------------------------------------------------------------------|---------|
| TC-11  | `test_logout`                   | Nhấn nút Đăng xuất. Kiểm tra hệ thống quay về trang đăng nhập và không còn nút Đăng xuất.           | PASSED  |
| TC-12  | `test_switch_language_to_english`| Nhấn nút "EN". Kiểm tra ít nhất 1 trong các từ khóa tiếng Anh xuất hiện trong Semantics Tree.       | PASSED  |

**Ghi chú kỹ thuật:** TC-11 và TC-12 dùng `time.sleep(3)` ở bước Propagation vì trang load lại toàn bộ sau đăng xuất / đổi ngôn ngữ, khiến `wait_for_flutter()` không thể xác định signal kết thúc. Đây là điểm flaky tiềm ẩn trên máy chạy chậm.

---

## 3. Test case bonus (tests_BONUS/)

Nhóm bổ sung 3 test case mới theo yêu cầu Bonus B1 (thêm ít nhất 3 TC ngoài 12 TC bắt buộc).

### 3.1 Tổng quan bonus

| File              | Nội dung                                           |
|-------------------|----------------------------------------------------|
| `test_login.py`   | TC-02, TC-03 viết lại dạng Data-Driven (parametrize) — Bonus B2 |
| `test_search.py`  | TC-04 đến TC-07 viết lại dạng Data-Driven với nhiều bộ dữ liệu — Bonus B2 |
| `3TC.py`          | TC-13, TC-14, TC-15 — 3 test case hoàn toàn mới — Bonus B1 |

---

### 3.2 Data-Driven Testing — `tests_BONUS/test_login.py`

TC-02 và TC-03 được gộp vào một hàm duy nhất `test_login_fail` với `@pytest.mark.parametrize`, chạy với 2 bộ dữ liệu:

| Bộ dữ liệu | Email             | Password      | Thông báo lỗi kỳ vọng              |
|------------|-------------------|---------------|------------------------------------|
| TC-02      | cu.le@email.com   | wrongpassword | Mật khẩu không đúng.               |
| TC-03      | (trống)           | (trống)       | Vui lòng nhập email và mật khẩu.  |

Oracle mạnh hơn so với `tests/test_login.py`: kiểm tra nội dung thông báo lỗi cụ thể thay vì chỉ kiểm tra "vẫn ở trang đăng nhập".

---

### 3.3 Data-Driven Testing — `tests_BONUS/test_search.py`

Bốn hàm tìm kiếm được mở rộng với nhiều bộ dữ liệu hơn:

| Hàm                        | Tham số hóa                                                 | Số lần chạy |
|----------------------------|-------------------------------------------------------------|-------------|
| `test_search_book_by_name` | `["Flutter", "flutter"]`                                    | 2           |
| `test_search_book_no_result`| `["xyz_khong_ton_tai_12345", "sach_doc_ban_2026"]`         | 2           |
| `test_filter_by_category`  | `["Công nghệ", "Quản trị", "Kinh tế"]`                     | 3           |
| `test_search_by_author`    | `["Nguyễn Minh Đức", "Lê Minh Khuê", "Trương Văn Phúc"]`  | 3           |

---

### 3.4 Ba test case mới — `tests_BONUS/3TC.py`

| TC     | Hàm kiểm thử                    | Mô tả kịch bản                                                                                                                                                  | Kết quả |
|--------|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| TC-13  | `test_borrow_more_than_3_books` | Mượn sách cho đến khi đạt giới hạn 3 quyển. Cố mượn quyển thứ 4 và kiểm tra hệ thống hiển thị thông báo "giới hạn mượn". Kiểm tra tổng số sách mượn vẫn là 3. | FAILED  |
| TC-14  | `test_invalid_member_cannot_borrow` (Suspended) | Tài khoản bị tạm ngưng (`cu.le@email.com`) thực hiện mượn sách. Kiểm tra hiển thị lỗi "Tài khoản đã bị tạm ngưng."       | FAILED  |
| TC-15  | `test_invalid_member_cannot_borrow` (Expired)   | Tài khoản hết hạn (`binh.pham@email.com`) thực hiện mượn sách. Kiểm tra hiển thị lỗi "Thành viên đã hết hạn."             | PASSED  |

**Phân tích lỗi TC-13 (BUG-02):** Hệ thống sử dụng điều kiện `> maxBooksPerMember` thay vì `>= maxBooksPerMember` trong logic kiểm tra giới hạn, khiến thành viên có thể mượn đến 4 quyển. Đây là lỗi ROR (Relational Operator Replacement) — thay `>=` bằng `>`. Test phát hiện đúng bug nhưng kết quả là FAILED vì hệ thống không từ chối lần mượn thứ 4.

**Phân tích lỗi TC-14 (BUG-04):** Tài khoản bị tạm ngưng nhận thông báo lỗi sai nội dung (nhận "Thành viên đã hết hạn" thay vì "Tài khoản đã bị tạm ngưng") — hệ thống xử lý nhầm trạng thái `suspended` và `expired`. TC-14 FAILED vì assertion kiểm tra text chính xác không khớp.

---

## 4. Bugs phát hiện trong hệ thống

| Bug ID | TC phát hiện | Mô tả                                                                                           | Mức độ  |
|--------|-------------|-------------------------------------------------------------------------------------------------|---------|
| BUG-02 | TC-13       | Giới hạn mượn sách dùng `> 3` thay vì `>= 3` — thành viên mượn được 4 quyển thay vì tối đa 3. | Trung bình |
| BUG-04 | TC-14       | Tài khoản bị tạm ngưng (`suspended`) nhận thông báo lỗi của tài khoản hết hạn (`expired`).     | Thấp    |

---

## 5. Nhận xét kỹ thuật

### 5.1 Những điểm làm tốt

**Xử lý Flutter Web (CanvasKit):** Toàn bộ test dùng đúng cơ chế Semantics Tree (`flt-semantics`) và Smart Wait (`wait_for_flutter()`), tránh dùng `time.sleep()` ở hầu hết các bước. Điều này giúp test ổn định và chạy nhanh hơn.

**Chất lượng Oracle:** TC-06 và TC-09 dùng Strong Oracle — kiểm tra từng phần tử trong danh sách thay vì chỉ kiểm tra sự tồn tại. Đây là cải tiến đáng kể so với Null Oracle hoặc Weak Oracle.

**Cấu trúc RIPR:** Mỗi test case đều có comment `[R]`, `[I]`, `[P]`, `[R✓]` rõ ràng, thể hiện hiểu đúng mô hình RIPR (Reachability, Infection, Propagation, Revealability).

**Data-Driven Testing:** `tests_BONUS/test_login.py` và `tests_BONUS/test_search.py` áp dụng `@pytest.mark.parametrize` đúng cách — một hàm test chạy nhiều bộ dữ liệu, giảm code trùng lặp.

### 5.2 Những điểm cần cải thiện

**Sử dụng `time.sleep()` ở TC-11 và TC-12:** Hai test case đăng xuất và đổi ngôn ngữ vẫn dùng `time.sleep(3)` ở bước Propagation. Nếu máy chạy CI chậm, đây là nguồn gốc của flaky test. Có thể thay bằng cách chờ một element cụ thể xuất hiện sau khi trang reload.

**TC-10 dùng `wait_for_timeout(1500)`:** Sau khi trả sách, test chờ 1.5 giây cố định. Nên thay bằng `wait_for_flutter(page, text="thành công")` hoặc chờ card sách biến mất khỏi danh sách.

**TC-13 phụ thuộc vào trạng thái ban đầu:** Test tính `remaining = 3 - current_count` và mượn đủ số sách còn thiếu. Nếu tài khoản đã mượn > 3 quyển (do bug BUG-02 từ lần chạy trước), logic này có thể lặp âm lần. Cần reset dữ liệu trước hoặc kiểm tra điều kiện đầu vào.

