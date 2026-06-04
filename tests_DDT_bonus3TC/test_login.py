import os
import pytest 
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR

# DIVIDE INTO 2 FIELDS : POSITIVE (TC-01) AND NEGATIVE (TC-02, TC-03)
# POSITIVE 
def test_login_success(page, test_config):
    # [R] Reachability: Truy cập trang đăng nhập — chạm tới UI cần test
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập dữ liệu hợp lệ — kích hoạt logic đăng nhập trong hệ thống
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ trạng thái lan truyền ra UI — nút "Đăng xuất" xuất hiện
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # [R✓] Revealability: Kiểm tra kết quả — Test Oracle phát hiện lỗi nếu có
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found " \
        f"(Đăng nhập không thành công: không tìm thấy tên hoặc nút Đăng xuất)"

# NEGATIVE
@pytest.mark.parametrize(
    "email,password,expected_error,tc_id",
    [
        ("ba.nguyen@email.com", "wrongpassword", "Mật khẩu không đúng.", "TC-02"),
        ("", "", "Vui lòng nhập email và mật khẩu.", "TC-03"),
    ],
    ids=[
        "TC-02 Wrong Password",
        "TC-03 Empty Fields"
    ]
)
def test_login_fail(page, test_config, email, password, expected_error, tc_id):
# [R] Reachability
    page.goto(test_config["base_url"])
    enable_flutter_semantics(page)

# [I] Infection
    flutter_fill(page, "Email", email)
    flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")

# [P] Propagation
    wait_for_flutter(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"DDT_login_fail_{tc_id}.png"))

# [R✓] Revealability
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_error = expected_error in sem_text
    assert has_error, \
        f"Expected error message not found for {tc_id} (Không tìm thấy thông báo lỗi cho {tc_id})"