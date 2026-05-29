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
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    wait_for_flutter,
    login,
    SCREENSHOT_DIR,
)

def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found"""

    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection
    login(page, test_config)

    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "Flutter"
    )

    # [P] Propagation
    wait_for_flutter(page, text="Flutter")

    page.screenshot(
        path=os.path.join(SCREENSHOT_DIR, "search_flutter.png")
    )

    # [R✓] Revealability
    books = page.locator(
        'flt-semantics[aria-label*="Flutter"]'
    )

    assert books.count() > 0, \
        "Search failed: No Flutter books found (Không tìm thấy sách Flutter)"


def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results"""

    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection
    login(page, test_config)

    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "xyz_khong_ton_tai_12345"
    )

    # [P] Propagation
    wait_for_flutter(page)

    page.screenshot(
        path=os.path.join(SCREENSHOT_DIR, "search_no_result.png")
    )

    # [R✓] Revealability
    books = page.locator(
        'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'
    )

    assert books.count() == 0, \
        "Search failed: Books still displayed (Vẫn còn sách hiển thị)"


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ'"""

    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection
    login(page, test_config)

    flutter_fill(
        page,
        "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)",
        "Công nghệ"
    )

    # [P] Propagation
    wait_for_flutter(page, text="Công nghệ")

    page.screenshot(
        path=os.path.join(SCREENSHOT_DIR, "filter_cong_nghe.png")
    )

    # [R✓] Revealability
    books = page.locator(
        'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'
    )

    count = books.count()

    assert count > 0, \
        "Filter failed: No books displayed (Không có sách nào hiển thị)"

    for i in range(count):
        text = books.nth(i).get_attribute("aria-label")

        assert "Công nghệ" in text, \
            f"Book does not belong to Công nghệ category: {text}"


def test_search_by_author(page, test_config):
    """TC-07: Search book by author name"""

    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection
    login(page, test_config)

    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "Nguyễn Minh Đức"
    )

    # [P] Propagation
    wait_for_flutter(page, text="Nguyễn Minh Đức")

    page.screenshot(
        path=os.path.join(SCREENSHOT_DIR, "search_author.png")
    )

    # [R✓] Revealability
    books = page.locator(
        'flt-semantics[aria-label*="Nguyễn Minh Đức"]'
    )

    assert books.count() > 0, \
        "Search failed: No books by Nguyễn Minh Đức found"
