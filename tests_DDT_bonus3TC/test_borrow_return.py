import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR, page, wait_for_flutter,
)

# 3 TC 8, 9, 10 LOGIC DIFFERENT -> CONCENTRATE ON ONE AND USE DDT IN THIS
# TC-08 (POSITIVE): Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)
def test_borrow_book(page, test_config):
    # 1. Login
    login(page, test_config)

    # 2. Find available books
    available_books = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]')
    book = available_books.first 
    before_count = page.locator('flt-semantics[role="group"]:has-text("Mượn sách này")').count()

    # 3. Click borrow button (nen dung local khong dung global "page")
    borrow_button = book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_button.first.click()
    # 4. Wait confirmation dialog
    wait_for_flutter(page, text="Xác nhận")
    enable_flutter_semantics(page)

    # 5. Confirm borrow
    # flutter_click_button(page, "Mượn") # khong dung helper vi khi khong co sach hop le bi fail 
    button = page.locator('flt-semantics[role="button"]:has-text("Mượn")')
    assert button.count() > 0, "Confirm button not found"
    button.first.click()
    
    # Wait UI update
    wait_for_flutter(page, text="thành công")
    enable_flutter_semantics(page)
    print("\n===== PAGE CONTENT =====")
    print("\n".join(page.locator("flt-semantics").all_text_contents()))
    after_count = page.locator('flt-semantics[role="group"]:has-text("Mượn sách này")').count()

    # Screenshot
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_book_success.png"))

    # 6. Assert
    print(f"Before: {before_count}")
    print(f"After: {after_count}")
    assert after_count == before_count - 1, \
        f"Borrow book failed or invalid book status or over limit quantity of books" 
# TC 13, 14, 15 LOGIC SIMILAR -> DDT
# TC-13: Không được mượn quá 4 sách
# TC-14: Thành viên tạm ngưng không được mượn sách
# TC-15: Thành viên hết hạn không được mượn sách


# def test_view_borrowed_books(page, test_config):
#     """TC-09: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)

#     Description (*Mô tả*):
#         Log in → switch to "Mượn / Trả" tab → verify borrowed books are shown.
#         (*Đăng nhập → chuyển sang tab "Mượn / Trả" → kiểm tra có sách đang mượn.*)

#     Hints (*Gợi ý*):
#         - Click tab: page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
#         - Verify: books with "Đang mượn" in aria-label, or "Trả sách" button exists
#           (*Kiểm tra: có sách với aria-label chứa "Đang mượn" hoặc có nút "Trả sách"*)
#     """
#     # 1. Login
#     login(page, test_config)
#     enable_flutter_semantics(page)

#     # 2. Click tab "Mượn / Trả"
#     borrow_return_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
#     borrow_return_tab.first.wait_for(state="visible", timeout=10000)
#     borrow_return_tab.first.click()
    
#     # 3. Check list books
#     borrowing_books = page.locator('flt-semantics[role="group"][aria-label*="Đang mượn"]')
#     borrowing_books.first.wait_for(state="visible", timeout=10000)

#     # 3. Check return button
#     return_buttons = page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
#     return_buttons.first.wait_for(state="visible", timeout=10000)
    
#     # Wait UI update
#     # page.wait_for_timeout(3000) # tuy may ma toc do khac nhau -> weak
#     wait_for_flutter(page, text="Đang mượn")
#     enable_flutter_semantics(page)

#     # Screenshot
#     page.screenshot(path=os.path.join(SCREENSHOT_DIR, "view_borrow_books.png"))

#     # 6. Assert
#     # weak
#     # sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
#     # has_borrowed = ("Đang mượn" in sem_text)
#     # has_return = ("Trả sách" in sem_text)
#     borrowing_books = page.locator('flt-semantics[role="group"][aria-label*="Đang mượn"]')
#     assert borrowing_books.count() > 0, "No borrowed books found"
#     for book in borrowing_books.all():
#         button = book.locator('flt-semantics[role="button"]:has-text("Trả sách")')
#         assert button.count() > 0, "Return button not found in borrowed book"


# def test_return_book(page, test_config):
#     """TC-10: Return a borrowed book (*Trả sách đang mượn*)

#     Description (*Mô tả*):
#         Log in → go to "Mượn / Trả" tab → click "Trả sách" → verify book is returned.
#         (*Đăng nhập → tab "Mượn / Trả" → click "Trả sách" → kiểm tra sách được trả.*)

#     Hints (*Gợi ý*):
#         - Switch to "Mượn / Trả" tab (*Chuyển tab "Mượn / Trả"*)
#         - Find return button: page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
#           (*Tìm nút "Trả sách"*)
#         - Click and verify status change or success message
#           (*Click và kiểm tra sách chuyển trạng thái hoặc có thông báo thành công*)
#     """
#     # TODO: Students implement here (Sinh viên viết code ở đây)
#     # pytest.skip("Not implemented — student must complete (Chưa hoàn thành)")
#     # 1. Login
#     login(page, test_config)
#     enable_flutter_semantics(page)

#     # 2. Click tab "Mượn / Trả"
#     borrow_return_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
#     borrow_return_tab.first.wait_for(state="visible", timeout=10000)
#     borrow_return_tab.first.click()
    
#     # 3. Check list books
#     borrowing_books = page.locator('flt-semantics[role="group"][aria-label*="Đang mượn"]')
#     borrowing_books.first.wait_for(state="visible", timeout=10000)
#     assert borrowing_books.count() > 0, "No borrowed books found"
    
#     # 4. Click first return button
#     first_book = borrowing_books.first
#     return_button = first_book.locator('flt-semantics[role="button"]:has-text("Trả sách")')
#     return_button.first.wait_for(state="visible")
#     before_count = borrowing_books.count()    
#     return_button.first.click()

#     # 5. Wait UI update
#     page.wait_for_timeout(1500)
#     enable_flutter_semantics(page)

#     # Screenshot
#     page.screenshot(path=os.path.join(SCREENSHOT_DIR, "returned_book_success.png"))

#     # 6. Assert
#     assert borrowing_books.count() == before_count - 1, "Book was not returned successfully"
