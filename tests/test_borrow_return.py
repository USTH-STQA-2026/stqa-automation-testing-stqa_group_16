"""
Borrow & Return Tests (*Kiểm thử Mượn & Trả sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 3 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 3 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - "Mượn / Trả" tab: role="tab", aria-label="Mượn / Trả"
    - Available books have "Có sẵn" in aria-label, borrowed books have "Đang mượn"
      (*Sách "Có sẵn" có aria-label chứa "Có sẵn", sách "Đang mượn" chứa "Đang mượn"*)
    - Borrow button: 'flt-semantics[role="button"]:has-text("Mượn sách này")'
      (*Nút mượn*)
    - After clicking "Mượn sách này", a confirmation dialog appears — click "Mượn" again
      (*Sau khi click "Mượn sách này" sẽ hiện dialog xác nhận — cần click nút "Mượn" lần nữa*)
    - Return button: 'flt-semantics[role="button"]:has-text("Trả sách")'
      (*Nút trả*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)
def test_borrow_book(page, test_config):
    
    login(page, test_config)

    page.wait_for_timeout(3000)

    book = page.locator(
        'flt-semantics[role="group"][aria-label*="Có sẵn"]'
    ).first

    book.locator(
        'flt-semantics[role="button"]:has-text("Mượn sách này")'
    ).click()

    page.wait_for_timeout(2000)

    enable_flutter_semantics(page)

    flutter_click_button(page, "Mượn")

    page.wait_for_timeout(3000)

    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    assert "Đang mượn" in sem_text or "thành công" in sem_text
    

# TC-09
def test_view_borrowed_books(page, test_config):
    login(page, test_config)

    page.wait_for_timeout(3000)

    page.locator(
        'flt-semantics[role="tab"][aria-label="Mượn / Trả"]'
    ).click()

    page.wait_for_timeout(3000)

    enable_flutter_semantics(page)

    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    has_borrowed = "Đang mượn" in sem_text
    has_return_button = "Trả sách" in sem_text

    assert has_borrowed or has_return_button

#TC 10
def test_return_book(page, test_config):
    login(page, test_config)

    page.wait_for_timeout(3000)

    page.locator(
        'flt-semantics[role="tab"][aria-label="Mượn / Trả"]'
    ).click()

    page.wait_for_timeout(3000)

    enable_flutter_semantics(page)

    return_button = page.locator(
        'flt-semantics[role="button"]:has-text("Trả sách")'
    ).first

    return_button.click()

    page.wait_for_timeout(3000)

    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    assert "thành công" in sem_text or "Có sẵn" in sem_text