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

#TC11
def test_logout(page, test_config):
    login(page, test_config)

    page.wait_for_timeout(3000)

    page.locator(
        'flt-semantics[role="button"]:has-text("Đăng xuất")'
    ).click()

    page.wait_for_timeout(3000)

    enable_flutter_semantics(page)

    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    has_login = "Đăng nhập" in sem_text
    has_email = "Email" in sem_text

    assert has_login or has_email

#TC-12: Switch language to English (*Chuyển ngôn ngữ sang tiếng Anh*)
def test_switch_language_to_english(page, test_config):
    login(page, test_config)

    page.wait_for_timeout(3000)

    page.locator(
        'flt-semantics[role="button"]:has-text("EN")'
    ).click()

    page.wait_for_timeout(2000)

    enable_flutter_semantics(page)

    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    assert (
        "Logout" in sem_text
        or "Borrow" in sem_text
        or "Search" in sem_text
        or "Library" in sem_text
    )