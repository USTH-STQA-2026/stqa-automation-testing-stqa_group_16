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
    login, SCREENSHOT_DIR, page,
)


def test_borrow_book(page, test_config):
    """TC-08: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → find an "Available" book → click "Mượn sách này" → confirm dialog
        → verify book status changes to "Borrowed".
        (*Đăng nhập → tìm sách "Có sẵn" → click "Mượn sách này" → xác nhận dialog
        → kiểm tra sách chuyển sang trạng thái "Đang mượn".*)

    Suggested steps (*Gợi ý các bước*):
        1. login(page, test_config)
        2. Find available book: page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]')
           (*Tìm sách Có sẵn*)
        3. Click "Mượn sách này" button inside that book card
           (*Click nút "Mượn sách này" trong sách đó*)
        4. Wait for confirmation dialog, re-enable semantics
           (*Đợi dialog xác nhận, bật lại semantics*)
        5. Click "Mượn" button (confirm button in dialog)
           (*Click nút "Mượn" — nút xác nhận trong dialog*)
        6. Assert: "Đang mượn" or "thành công" appears
           (*Assert: "Đang mượn" hoặc "thành công" xuất hiện*)
    """
    # TODO: Students implement here (Sinh viên viết code ở đây)
    # pytest.skip("Not implemented — student must complete (Chưa hoàn thành)")
    # 1. Login
    login(page, test_config)
    enable_flutter_semantics(page)

    # 2. Find available books
    available_books = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]')
    assert available_books.count() > 0, "No available books found"
    book = available_books.first 

    # Debug
    # print(f"\nAvailable books count: {available_books.count()}")

    # 3. Click borrow button
    # nen dung local khong dung global "page"
    borrow_buttons = book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_buttons.first.click()

    # 4. Wait confirmation dialog
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    # 5. Confirm borrow
    # flutter_click_button(page, "Mượn") # khong dung helper vi khi khong co sach hop le bi fail 
    button = page.locator('flt-semantics[role="button"]:has-text("Mượn")')
    assert button.count() > 0, "Confirm button not found"
    button.first.click()
        
    # Wait UI update
    page.wait_for_timeout(3000) 
    enable_flutter_semantics(page)

    # Screenshot
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_book.png"))

    # 6. Assert
    # cnay cung global khong nen dung 
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_borrowed = ("Đang mượn" in sem_text)
    # has_borrowed = ("Đang mượn" in book.inner_text()) # sao cach nay sai ? 
    assert has_borrowed, \
        f"Borrow book failed " \
        f"(Không tìm thấy dấu hiệu mượn sách thành công)"


def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → switch to "Mượn / Trả" tab → verify borrowed books are shown.
        (*Đăng nhập → chuyển sang tab "Mượn / Trả" → kiểm tra có sách đang mượn.*)

    Hints (*Gợi ý*):
        - Click tab: page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
        - Verify: books with "Đang mượn" in aria-label, or "Trả sách" button exists
          (*Kiểm tra: có sách với aria-label chứa "Đang mượn" hoặc có nút "Trả sách"*)
    """
    # TODO: Students implement here (Sinh viên viết code ở đây)
    # pytest.skip("Not implemented — student must complete (Chưa hoàn thành)")
    # 1. Login
    login(page, test_config)
    enable_flutter_semantics(page)

    # 2. Click tab "Mượn / Trả"
    borrow_return_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_return_tab.first.wait_for(state="visible", timeout=10000)
    borrow_return_tab.first.click()
    
    # 3. Check list books
    borrowing_books = page.locator('flt-semantics[role="group"][aria-label*="Đang mượn"]')
    borrowing_books.first.wait_for(state="visible", timeout=10000)

    # 3. Check return button
    return_buttons = page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
    return_buttons.first.wait_for(state="visible", timeout=10000)
    
    # Wait UI update
    # page.wait_for_timeout(3000) # tuy may ma toc do khac nhau -> weak
    page.wait_for_load_state("networkidle")
    enable_flutter_semantics(page)

    # Screenshot
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "view_borrow_books.png"))

    # 6. Assert
    # weak
    # sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    # has_borrowed = ("Đang mượn" in sem_text)
    # has_return = ("Trả sách" in sem_text)
    borrowing_books = page.locator('flt-semantics[role="group"][aria-label*="Đang mượn"]')
    assert borrowing_books.count() > 0, "No borrowed books found"
    for book in borrowing_books.all():
        button = book.locator('flt-semantics[role="button"]:has-text("Trả sách")')
        assert button.count() > 0, "Return button not found in borrowed book"


def test_return_book(page, test_config):
    """TC-10: Return a borrowed book (*Trả sách đang mượn*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → go to "Mượn / Trả" tab → click "Trả sách" → verify book is returned.
        (*Đăng nhập → tab "Mượn / Trả" → click "Trả sách" → kiểm tra sách được trả.*)

    Hints (*Gợi ý*):
        - Switch to "Mượn / Trả" tab (*Chuyển tab "Mượn / Trả"*)
        - Find return button: page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
          (*Tìm nút "Trả sách"*)
        - Click and verify status change or success message
          (*Click và kiểm tra sách chuyển trạng thái hoặc có thông báo thành công*)
    """
    # TODO: Students implement here (Sinh viên viết code ở đây)
    pytest.skip("Not implemented — student must complete (Chưa hoàn thành)")
