"""
Search & Filter Tests (*Kiểm thử Tìm kiếm & Lọc sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 4 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 4 test case trong file này.*)

Hints (*Gợi ý*):
    - After logging in, use flutter_fill() to type into the search box
      (*Sau khi đăng nhập, dùng flutter_fill() để nhập vào ô tìm kiếm*)
    - Search box aria-label: "Tìm kiếm theo tên sách hoặc tác giả..."
    - Category filter aria-label: "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    - Each book card has role="group" and aria-label containing book info
      (*Mỗi card sách có role="group" và aria-label chứa thông tin sách*)
    - Use login() helper from conftest.py to log in before testing
      (*Dùng login() helper từ conftest.py để đăng nhập trước khi test*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)

# TC-04 — test_search_book_by_name
def test_search_book_by_name(page, test_config):
    login(page, test_config)

    page.wait_for_timeout(3000)

    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "Flutter"
    )

    page.wait_for_timeout(3000)

    count = page.locator(
        'flt-semantics[aria-label*="Flutter"]'
    ).count()

    assert count > 0

#TC-05 — test_search_book_no_result

def test_search_book_no_result(page, test_config):
    login(page, test_config)

    page.wait_for_timeout(3000)

    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "xyz_khong_ton_tai_12345"
    )

    page.wait_for_timeout(3000)

    count = page.locator(
        'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'
    ).count()

    assert count == 0

# TC-06: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại 'Công nghệ'*)
def test_filter_by_category(page, test_config):
    login(page, test_config)

    page.wait_for_timeout(3000)

    flutter_fill(
        page,
        "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)",
        "Công nghệ"
    )

    page.wait_for_timeout(3000)

    books = page.locator(
        'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'
    )

    count = books.count()

    assert count > 0

    for i in range(count):

        text = books.nth(i).get_attribute("aria-label")

        assert "Công nghệ" in text

#TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

def test_search_by_author(page, test_config):
    login(page, test_config)

    page.wait_for_timeout(3000)

    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "Nguyễn Minh Đức"
    )

    page.wait_for_timeout(3000)

    count = page.locator(
        'flt-semantics[aria-label*="Nguyễn Minh Đức"]'
    ).count()

    assert count > 0
        
