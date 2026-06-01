"""
Logout & Language Tests (*Kiểm thử Đăng xuất & Chuyển ngôn ngữ*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 2 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 2 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - Logout button: 'flt-semantics[role="button"]:has-text("Đăng xuất")'
      (*Nút Đăng xuất*)
    - Language switch EN button: 'flt-semantics[role="button"]:has-text("EN")'
      (*Nút chuyển ngôn ngữ EN*)
    - After logout: page returns to login (has "Đăng nhập" button and "Email" input)
      (*Sau đăng xuất: trang quay về login*)
    - After switching to EN: text "Logout", "Borrow", "Search", "Library" may appear
      (*Sau chuyển EN: text tiếng Anh có thể xuất hiện*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)


def test_logout(page, test_config):
    """TC-11: Logout success (*Đăng xuất thành công*)

    ✅ COMPLETED

    📖 RIPR Model:
        [R] Đăng nhập thành công — chạm tới trạng thái cần test (đã đăng nhập)
        [I] Click "Đăng xuất" — kích hoạt logic logout trong hệ thống
        [P] Session bị xóa → UI chuyển về trang đăng nhập
        [R✓] Assert thấy ô "Email" hoặc nút "Đăng nhập" — xác nhận logout thành công
    """
    # [R] Reachability: Dùng helper login() để đạt trạng thái "đã đăng nhập"
    # (Tái sử dụng TC-01 làm precondition — không lặp lại code)
    login(page, test_config)

    # [I] Infection: Tìm và click nút "Đăng xuất" — kích hoạt flow logout
    logout_btn = page.locator('flt-semantics[role="button"]:has-text("Đăng xuất")')
    logout_btn.wait_for(state="visible", timeout=10000)  # Smart Wait: chờ nút sẵn sàng
    logout_btn.click()

    # [P] Propagation: Chờ hệ thống xử lý logout và UI re-render về trang login
    time.sleep(3)
    enable_flutter_semantics(page)  # Bật lại semantics sau khi trang thay đổi

    # Chụp screenshot ghi lại trạng thái sau khi đăng xuất
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC11_logout_success.png"))

    # [R✓] Revealability: Test Oracle — kiểm tra đã quay về trang đăng nhập
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # Điều kiện 1: Nút "Đăng nhập" xuất hiện lại → đã về trang login
    has_login_button = "Đăng nhập" in sem_text

    # Điều kiện 2: Ô input "Email" xuất hiện → form đăng nhập hiển thị
    has_email_input = "Email" in sem_text

    # Điều kiện phủ định: Không còn nút "Đăng xuất" → session đã bị hủy
    session_cleared = "Đăng xuất" not in sem_text and "Logout" not in sem_text

    assert (has_login_button or has_email_input) and session_cleared, (
        "TC-11 FAILED: Sau khi click Đăng xuất, hệ thống KHÔNG quay về trang đăng nhập! "
        "(After clicking Logout, system did NOT return to login page.) "
        f"sem_text snapshot: {sem_text[:300]}"
    )


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English (*Chuyển ngôn ngữ sang tiếng Anh*)

    ✅ COMPLETED

    📖 RIPR Model:
        [R] Đăng nhập thành công — chạm tới UI chính có nút chuyển ngôn ngữ
        [I] Click nút "EN" — kích hoạt cơ chế i18n của hệ thống
        [P] Ngôn ngữ thay đổi → toàn bộ text UI được render lại bằng tiếng Anh
        [R✓] Assert thấy text tiếng Anh ("Logout", "Borrow", "Library", v.v.)
    """
    # [R] Reachability: Dùng helper login() để vào trang chính (có nút EN)
    login(page, test_config)

    # [I] Infection: Tìm và click nút "EN" — kích hoạt chuyển ngôn ngữ
    lang_btn = page.locator('flt-semantics[role="button"]:has-text("EN")')
    lang_btn.wait_for(state="visible", timeout=10000)  # Smart Wait: chờ nút sẵn sàng
    lang_btn.click()

    # [P] Propagation: Chờ hệ thống i18n re-render toàn bộ UI sang tiếng Anh
    time.sleep(2)
    enable_flutter_semantics(page)  # Bật lại semantics sau khi UI re-render

    # Chụp screenshot ghi lại UI sau khi chuyển sang tiếng Anh
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC12_switch_language_english.png"))

    # [R✓] Revealability: Test Oracle — kiểm tra UI đã hiển thị bằng tiếng Anh
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # Danh sách các từ tiếng Anh kỳ vọng xuất hiện sau khi chuyển ngôn ngữ
    english_keywords = ["Logout", "Borrow", "Search", "Library", "Book", "Return", "Profile"]

    # Tìm tất cả các từ tiếng Anh xuất hiện trong UI (để debug dễ hơn)
    found_keywords = [kw for kw in english_keywords if kw in sem_text]

    assert len(found_keywords) > 0, (
        "TC-12 FAILED: Sau khi click nút 'EN', giao diện KHÔNG chuyển sang tiếng Anh! "
        "(After clicking 'EN', UI did NOT switch to English.) "
        f"Expected one of: {english_keywords}. "
        f"sem_text snapshot: {sem_text[:300]}"
    )
