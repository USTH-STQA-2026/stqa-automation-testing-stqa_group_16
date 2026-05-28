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
    login, SCREENSHOT_DIR, wait_for_flutter
)


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name - results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)

    Description (*Mô tả*):
        Log in → search keyword "Flutter" → verify Flutter books appear in results.
        (*Đăng nhập → tìm kiếm từ khóa "Flutter" → kiểm tra có sách Flutter trong kết quả.*)

      📖 RIPR Model:
        [R] Reachability: Đăng nhập vào hệ thống và kích hoạt Flutter Semantics.
        [I] Infection: Nhập từ khóa "Flutter" vào ô tìm kiếm.
        [P] Propagation: Đợi hệ thống xử lý và cập nhật danh sách sách ra giao diện.
        [R✓] Revealability: Đếm số lượng phần tử chứa từ khóa "Flutter" xem có > 0 không.

    Hints (*Gợi ý*):
        - login(page, test_config)
        - flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
        - Verify: page.locator('flt-semantics[aria-label*="Flutter"]').count() > 0
    """
    # TODO: Students implement here (Sinh viên viết code ở đây)

    # [R] Reachability
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
    # Lưu ý: Nếu hệ thống tự tìm khi gõ thì không cần dòng dưới, nếu cần bấm nút thì giữ lại nút "Tìm kiếm"
    # flutter_click_button(page, "Tìm kiếm") 

    # [P] Propagation (Smart Wait)
    wait_for_flutter(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_book_by_name.png"))

    # [R✓] Revealability
    flutter_books = page.locator('flt-semantics[aria-label*="Flutter"]')
    assert flutter_books.count() > 0, \
        f"Search failed: No books found containing 'Flutter' " \
        f"(Tìm kiếm thất bại: Không thấy sách chứa 'Flutter')"


def test_search_book_no_result(page, test_config):
    """TC-05: Search book - no results (*Tìm kiếm sách — không có kết quả*)

    Description (*Mô tả*):
        Log in → search a non-existent keyword (e.g. "xyz_khong_ton_tai_12345")
        → verify no books are displayed.
        (*Đăng nhập → tìm kiếm từ khóa không tồn tại → kiểm tra không có sách nào hiển thị.*)

    📖 RIPR Model:
        [R] Reachability: Đăng nhập thành công và bật chế độ tương tác Semantics.
        [I] Infection: Nhập từ khóa rác chắc chắn không tồn tại "xyz_khong_ton_tai_12345".
        [P] Propagation: Hệ thống lọc không ra dữ liệu, UI cập nhật danh sách trống.
        [R✓] Revealability: Xác minh số lượng card sách hiển thị trên màn hình bằng 0.
    Hints (*Gợi ý*):
        - Verify: page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').count() == 0
    """
    # TODO: Students implement here (Sinh viên viết code ở đây)

    # [R] Reachability
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "xyz_khong_ton_tai_12345")

    # [P] Propagation (Smart Wait)
    wait_for_flutter(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_book_no_result.png"))

    # [R✓] Revealability
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    assert book_cards.count() == 0, \
        f"Expected 0 books displayed, but found {book_cards.count()} " \
        f"(Lỗi: Lẽ ra không có sách nào hiển thị)"


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại 'Công nghệ'*)

    Description (*Mô tả*):
        Log in → enter "Công nghệ" in the category filter → verify all displayed books
        belong to the "Công nghệ" category.
        (*Đăng nhập → nhập "Công nghệ" vào ô lọc thể loại → kiểm tra tất cả sách
        hiển thị đều thuộc thể loại Công nghệ.*)

    📖 RIPR Model:
        [R] Reachability: Tiến hành đăng nhập và chuẩn bị UI.
        [I] Infection: Điền "Công nghệ" vào ô lọc thể loại (Category filter).
        [P] Propagation: Hệ thống kích hoạt bộ lọc và render lại các card sách tương ứng.
        [R✓] Revealability: Vòng lặp kiểm tra từng card sách xem có chứa chữ "Công nghệ" ở thuộc tính aria-label không.

    Hints (*Gợi ý*):
        - flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "Công nghệ")
        - Get book list: page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
          (*Lấy danh sách sách*)
        - Loop through each book, verify aria-label contains "Công nghệ"
          (*Lặp qua từng sách, kiểm tra aria-label chứa "Công nghệ"*)
    """
    # TODO: Students implement here (Sinh viên viết code ở đây)

    # [R] Reachability
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection
    flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "Công nghệ")

    # [P] Propagation (Smart Wait)
    wait_for_flutter(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "filter_by_category.png"))

    # [R✓] Revealability
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    total_books = book_cards.count()
    
    # Kiểm tra xem có sách nào xuất hiện để check không
    assert total_books > 0, "No books found after applying 'Công nghệ' filter (Không có sách nào hiển thị sau khi lọc)"

    # Lặp qua từng sách để verify aria-label chứa "Công nghệ"
    for i in range(total_books):
        aria_label = book_cards.nth(i).get_attribute("aria-label") or ""
        assert "Công nghệ" in aria_label, \
            f"Book at index {i} does not belong to 'Công nghệ' category. Label: {aria_label} " \
            f"(Sách không thuộc thể loại Công nghệ)"



def test_search_by_author(page, test_config):
    """TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

    Description (*Mô tả*):
        Log in → search author name (e.g. "Nguyễn Minh Đức") → verify results found.
        (*Đăng nhập → tìm kiếm tên tác giả → kiểm tra có kết quả.*)

    📖 RIPR Model:
        [R] Reachability: Đăng nhập vào hệ thống, đảm bảo môi trường sẵn sàng.
        [I] Infection: Nhập tên tác giả "Nguyễn Minh Đức" vào ô tìm kiếm chung.
        [P] Propagation: Hệ thống tìm và truyền danh sách tác phẩm của tác giả ra màn hình.
        [R✓] Revealability: Kiểm tra xem các phần tử kết quả hiển thị có chứa tên tác giả mong muốn hay không.

    Hints (*Gợi ý*):
        - flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")
        - Verify: page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').count() > 0
    """
    # TODO: Students implement here (Sinh viên viết code ở đây)
    # [R] Reachability
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")

    # [P] Propagation (Smart Wait)
    wait_for_flutter(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_by_author.png"))

    # [R✓] Revealability
    author_results = page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]')
    assert author_results.count() > 0, \
        f"Search failed: No results found for author 'Nguyễn Minh Đức' " \
        f"(Không tìm thấy sách của tác giả Nguyễn Minh Đức)"
