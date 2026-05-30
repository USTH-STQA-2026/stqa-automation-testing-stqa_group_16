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
    """TC-08: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)

    ✅ COMPLETED

    📖 RIPR Model:
        [R] Đăng nhập → chạm tới danh sách sách, tìm được sách "Có sẵn"
        [I] Click "Mượn sách này" + xác nhận dialog → kích hoạt logic mượn sách
        [P] Hệ thống cập nhật trạng thái sách → lan truyền ra UI ("Đang mượn")
        [R✓] Assert "Đang mượn" hoặc "thành công" xuất hiện → mượn thành công
    """
    # [R] Reachability: Đăng nhập và tìm sách có trạng thái "Có sẵn"
    login(page, test_config)

    # Tìm card sách đầu tiên có trạng thái "Có sẵn" (available book)
    available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    available_book.wait_for(state="visible", timeout=10000)  # Smart Wait

    # Lấy tên sách để dùng trong assert message (debug dễ hơn)
    book_aria = available_book.get_attribute("aria-label") or "Unknown book"

    # [I] Infection: Click nút "Mượn sách này" bên trong card sách đó
    borrow_btn = available_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_btn.wait_for(state="visible", timeout=5000)
    borrow_btn.click()

    # Chờ dialog xác nhận xuất hiện và bật lại semantics
    time.sleep(2)
    enable_flutter_semantics(page)

    # Chụp screenshot trạng thái dialog xác nhận
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC08_borrow_confirm_dialog.png"))

    # Click nút "Mượn" trong dialog xác nhận (bước 2 của flow mượn sách)
    confirm_btn = page.locator('flt-semantics[role="button"]:has-text("Mượn")').last
    confirm_btn.wait_for(state="visible", timeout=5000)
    confirm_btn.click()

    # [P] Propagation: Chờ hệ thống xử lý và cập nhật trạng thái sách
    time.sleep(3)
    enable_flutter_semantics(page)  # Bật lại semantics sau khi UI cập nhật

    # Chụp screenshot ghi lại trạng thái sau khi mượn
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC08_borrow_book_success.png"))

    # [R✓] Revealability: Test Oracle — kiểm tra mượn sách thành công
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # Điều kiện 1: Sách chuyển sang trạng thái "Đang mượn"
    has_borrowed_status = "Đang mượn" in sem_text

    # Điều kiện 2: Thông báo thành công xuất hiện
    success_keywords = ["thành công", "mượn thành công", "success", "successfully"]
    has_success_msg = any(kw in sem_text.lower() for kw in success_keywords)

    assert has_borrowed_status or has_success_msg, (
        f"TC-08 FAILED: Mượn sách '{book_aria[:80]}' nhưng KHÔNG thấy trạng thái 'Đang mượn' "
        f"hoặc thông báo thành công! "
        f"(Borrow action did not produce expected status change or success message.) "
        f"sem_text snippet: {sem_text[:300]}"
    )


def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)

    ✅ COMPLETED

    📖 RIPR Model:
        [R] Đăng nhập → chạm tới tab "Mượn / Trả" chứa danh sách sách đang mượn
        [I] Click tab "Mượn / Trả" → kích hoạt load danh sách sách đang mượn
        [P] Hệ thống load dữ liệu → hiển thị các sách có trạng thái "Đang mượn"
        [R✓] Assert có sách "Đang mượn" hoặc nút "Trả sách" → tab hoạt động đúng
    """
    # [R] Reachability: Đăng nhập để có thể truy cập tab "Mượn / Trả"
    login(page, test_config)

    # [I] Infection: Click vào tab "Mượn / Trả" — chuyển sang view danh sách đang mượn
    borrow_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_tab.wait_for(state="visible", timeout=10000)  # Smart Wait
    borrow_tab.click()

    # [P] Propagation: Chờ hệ thống load dữ liệu và render danh sách sách đang mượn
    time.sleep(3)
    enable_flutter_semantics(page)  # Bật lại semantics sau khi tab content load xong

    # Chụp screenshot ghi lại nội dung tab "Mượn / Trả"
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC09_view_borrowed_books.png"))

    # [R✓] Revealability: Test Oracle — kiểm tra tab hiển thị đúng nội dung
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # Điều kiện 1: Có sách với trạng thái "Đang mượn" trong danh sách
    borrowed_books_count = page.locator(
        'flt-semantics[role="group"][aria-label*="Đang mượn"]'
    ).count()
    has_borrowed_books = borrowed_books_count > 0

    # Điều kiện 2: Có nút "Trả sách" → tức là có sách đang mượn cần trả
    return_btn_count = page.locator(
        'flt-semantics[role="button"]:has-text("Trả sách")'
    ).count()
    has_return_button = return_btn_count > 0

    # Điều kiện 3: Tab đã được active (có text liên quan trong sem_text)
    tab_active = "Mượn / Trả" in sem_text or "Đang mượn" in sem_text or "Trả sách" in sem_text

    assert tab_active and (has_borrowed_books or has_return_button), (
        "TC-09 FAILED: Tab 'Mượn / Trả' KHÔNG hiển thị danh sách sách đang mượn! "
        "(Tab 'Mượn / Trả' did not show any borrowed books or return buttons.) "
        f"Borrowed book cards: {borrowed_books_count}. "
        f"Return buttons: {return_btn_count}. "
        f"sem_text snippet: {sem_text[:300]}"
    )


def test_return_book(page, test_config):
    """TC-10: Return a borrowed book (*Trả sách đang mượn*)

    ✅ COMPLETED

    📖 RIPR Model:
        [R] Đăng nhập → chuyển sang tab "Mượn / Trả" → chạm tới sách đang mượn
        [I] Click "Trả sách" → kích hoạt logic trả sách trong hệ thống
        [P] Hệ thống cập nhật trạng thái → sách chuyển từ "Đang mượn" về "Có sẵn"
        [R✓] Assert "Có sẵn" xuất hiện hoặc "Đang mượn" giảm → trả sách thành công
    """
    # [R] Reachability: Đăng nhập và chuyển sang tab "Mượn / Trả"
    login(page, test_config)

    # Chuyển sang tab "Mượn / Trả" để thấy danh sách sách đang mượn
    borrow_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_tab.wait_for(state="visible", timeout=10000)  # Smart Wait
    borrow_tab.click()

    # Chờ tab load xong và bật lại semantics
    time.sleep(3)
    enable_flutter_semantics(page)

    # Đếm số sách đang mượn TRƯỚC khi trả — dùng để so sánh sau khi trả
    borrowed_before = page.locator(
        'flt-semantics[role="group"][aria-label*="Đang mượn"]'
    ).count()

    # Lấy thông tin sách sắp trả (để debug)
    first_borrowed = page.locator(
        'flt-semantics[role="group"][aria-label*="Đang mượn"]'
    ).first
    book_aria = first_borrowed.get_attribute("aria-label") or "Unknown book"

    # Chụp screenshot trạng thái trước khi trả sách
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC10_before_return_book.png"))

    # [I] Infection: Click nút "Trả sách" — kích hoạt logic trả sách
    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    return_btn.wait_for(state="visible", timeout=5000)
    return_btn.click()

    # [P] Propagation: Chờ hệ thống xử lý và cập nhật trạng thái sách
    time.sleep(3)
    enable_flutter_semantics(page)  # Bật lại semantics sau khi UI thay đổi

    # Chụp screenshot ghi lại trạng thái sau khi trả sách
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC10_after_return_book.png"))

    # [R✓] Revealability: Test Oracle — kiểm tra trả sách thành công
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # Điều kiện 1: Số sách "Đang mượn" giảm đi → đã trả thành công
    borrowed_after = page.locator(
        'flt-semantics[role="group"][aria-label*="Đang mượn"]'
    ).count()
    books_count_decreased = borrowed_after < borrowed_before

    # Điều kiện 2: Xuất hiện thông báo trả thành công
    success_keywords = ["trả thành công", "thành công", "success", "returned"]
    has_success_msg = any(kw in sem_text.lower() for kw in success_keywords)

    # Điều kiện 3: Sách xuất hiện lại với trạng thái "Có sẵn" (sau khi trả)
    has_available_status = "Có sẵn" in sem_text

    assert books_count_decreased or has_success_msg or has_available_status, (
        f"TC-10 FAILED: Trả sách '{book_aria[:80]}' nhưng trạng thái KHÔNG thay đổi! "
        f"(Return book action did not produce expected status change or success message.) "
        f"Borrowed books before: {borrowed_before}, after: {borrowed_after}. "
        f"sem_text snippet: {sem_text[:300]}"
    )
