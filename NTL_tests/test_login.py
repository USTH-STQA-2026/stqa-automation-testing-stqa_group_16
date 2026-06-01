"""
Login Tests (*Kiểm thử Đăng nhập*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

📖 Textbook concepts in this file:
   - RIPR Model (Ch.2): See [R], [I], [P], [R✓] comments in TC-01
   - Data-Driven Testing / @parametrize (Ch.3 §3.3.2): See hint in TC-02/TC-03

This file contains 1 completed example (TC-01).
Students must complete TC-02 and TC-03.

(*File này chứa 1 ví dụ mẫu (TC-01) đã hoàn chỉnh.
Sinh viên cần hoàn thành TC-02 và TC-03.*)
"""
import os
import time
import pytest
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR


def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials (*Đăng nhập thành công với thông tin hợp lệ*)

    ✅ COMPLETED — Use as a reference example.
    (*ĐÃ HOÀN THÀNH — Dùng làm ví dụ tham khảo.*)

    📖 RIPR Model (Textbook Ch.2 — Reachability → Infection → Propagation → Revealability):
        Mỗi dòng code trong test tương ứng với 1 bước trong chuỗi RIPR.
        Xem comment [R], [I], [P], [R✓] bên dưới.
    """
    # [R] Reachability: Truy cập trang đăng nhập — chạm tới UI cần test
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập dữ liệu hợp lệ — kích hoạt logic đăng nhập trong hệ thống
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ trạng thái lan truyền ra UI — nút "Đăng xuất" xuất hiện
    # (Smart Wait: thay vì time.sleep(5) — nhanh hơn và ổn định hơn)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # [R✓] Revealability: Kiểm tra kết quả — Test Oracle phát hiện lỗi nếu có
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found " \
        f"(Đăng nhập không thành công: không tìm thấy tên hoặc nút Đăng xuất)"


def test_login_fail_wrong_password(page, test_config):
    """TC-02: Login fail – wrong password (*Đăng nhập thất bại – sai mật khẩu*)

    ✅ COMPLETED

    📖 RIPR Model:
        [R] Truy cập trang đăng nhập — chạm tới UI cần test
        [I] Nhập mật khẩu sai — kích hoạt trạng thái lỗi trong hệ thống
        [P] Hệ thống xử lý → lỗi lan truyền ra UI (không chuyển trang / hiện thông báo)
        [R✓] Assert URL vẫn ở login HOẶC có thông báo lỗi — Test Oracle phát hiện lỗi
    """
    # [R] Reachability: Truy cập trang đăng nhập
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập email đúng nhưng mật khẩu SAI — tạo trạng thái lỗi
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "wrongpassword123")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ hệ thống phản hồi (Smart Wait — không dùng sleep cứng)
    # Chờ tối đa 4s để thông báo lỗi hoặc trạng thái thất bại xuất hiện
    time.sleep(4)
    enable_flutter_semantics(page)  # Bật lại semantics sau khi UI có thể re-render

    # Chụp screenshot để ghi lại trạng thái sau khi thử đăng nhập sai
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC02_login_fail_wrong_password.png"))

    # [R✓] Revealability: Test Oracle — kiểm tra hệ thống KHÔNG cho đăng nhập
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # Điều kiện 1: Vẫn còn ô "Email" hoặc nút "Đăng nhập" → chưa chuyển trang
    still_on_login = "Email" in sem_text or "Đăng nhập" in sem_text

    # Điều kiện 2: Xuất hiện thông báo lỗi (sai mật khẩu, tài khoản không tồn tại, v.v.)
    error_keywords = ["sai", "không đúng", "lỗi", "thất bại", "incorrect", "invalid", "error", "wrong"]
    has_error_message = any(kw in sem_text.lower() for kw in error_keywords)

    # Điều kiện phủ định: KHÔNG xuất hiện nút "Đăng xuất" (tức là chưa login thành công)
    not_logged_in = "Đăng xuất" not in sem_text and "Logout" not in sem_text

    assert (still_on_login or has_error_message) and not_logged_in, (
        "TC-02 FAILED: Hệ thống cho phép đăng nhập với mật khẩu sai! "
        "(System allowed login with wrong password — should have blocked it.) "
        f"sem_text snapshot: {sem_text[:300]}"
    )


def test_login_fail_empty_fields(page, test_config):
    """TC-03: Login fail – empty fields (*Đăng nhập thất bại – để trống các trường*)

    ✅ COMPLETED

    📖 RIPR Model:
        [R] Truy cập trang đăng nhập — chạm tới UI cần test
        [I] Không nhập gì, click đăng nhập ngay — kích hoạt validation trống
        [P] Hệ thống kiểm tra input rỗng → không chuyển trang / hiện cảnh báo
        [R✓] Assert vẫn ở trang login — Test Oracle xác nhận hệ thống chặn đúng
    """
    # [R] Reachability: Truy cập trang đăng nhập
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: KHÔNG nhập Email / Mật khẩu — click "Đăng nhập" với form trống
    # Đây là boundary case: kiểm tra validation phía client
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ hệ thống phản hồi (Smart Wait)
    # Hệ thống validation thường nhanh, 2s là đủ để UI cập nhật
    time.sleep(2)
    enable_flutter_semantics(page)  # Bật lại semantics sau khi UI có thể thay đổi

    # Chụp screenshot ghi lại trạng thái sau khi submit form rỗng
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC03_login_fail_empty_fields.png"))

    # [R✓] Revealability: Test Oracle — kiểm tra hệ thống KHÔNG cho đăng nhập khi bỏ trống
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # Điều kiện 1: Vẫn thấy ô "Email" hoặc nút "Đăng nhập" → trang chưa chuyển
    still_on_login = "Email" in sem_text or "Đăng nhập" in sem_text

    # Điều kiện 2: Hệ thống hiển thị cảnh báo validation (trường bắt buộc, v.v.)
    validation_keywords = [
        "bắt buộc", "không được để trống", "required", "vui lòng nhập",
        "please enter", "cannot be empty", "field required"
    ]
    has_validation_warning = any(kw in sem_text.lower() for kw in validation_keywords)

    # Điều kiện phủ định: KHÔNG thấy nút "Đăng xuất" → chưa đăng nhập thành công
    not_logged_in = "Đăng xuất" not in sem_text and "Logout" not in sem_text

    assert (still_on_login or has_validation_warning) and not_logged_in, (
        "TC-03 FAILED: Hệ thống cho phép đăng nhập khi bỏ trống Email và Mật khẩu! "
        "(System allowed login with empty fields — validation did not block it.) "
        f"sem_text snapshot: {sem_text[:300]}"
    )
