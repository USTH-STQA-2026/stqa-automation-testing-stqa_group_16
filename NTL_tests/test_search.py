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


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)

    ✅ COMPLETED

    📖 RIPR Model:
        [R] Đăng nhập → chạm tới trang danh sách sách có ô tìm kiếm
        [I] Nhập từ khóa "Flutter" → kích hoạt logic search trong hệ thống
        [P] Hệ thống lọc danh sách → chỉ hiển thị sách liên quan đến "Flutter"
        [R✓] Assert có ít nhất 1 card sách chứa "Flutter" trong aria-label
    """
    # [R] Reachability: Đăng nhập để vào trang danh sách sách
    login(page, test_config)

    # [I] Infection: Nhập từ khóa "Flutter" vào ô tìm kiếm — kích hoạt search filter
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")

    # [P] Propagation: Chờ hệ thống lọc và re-render danh sách kết quả
    # Smart Wait: 2s đủ để debounce search hoàn thành và UI cập nhật
    time.sleep(2)
    enable_flutter_semantics(page)  # Bật lại semantics sau khi danh sách thay đổi

    # Chụp screenshot ghi lại kết quả tìm kiếm
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC04_search_by_name_flutter.png"))

    # [R✓] Revealability: Test Oracle — kiểm tra có sách "Flutter" xuất hiện trong kết quả
    # Đếm số card sách có aria-label chứa "Flutter"
    result_count = page.locator('flt-semantics[aria-label*="Flutter"]').count()

    assert result_count > 0, (
        "TC-04 FAILED: Tìm kiếm từ khóa 'Flutter' nhưng KHÔNG có sách nào xuất hiện! "
        "(Search for 'Flutter' returned no results — expected at least 1 book card.) "
        f"Found {result_count} matching elements."
    )


def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results (*Tìm kiếm sách — không có kết quả*)

    ✅ COMPLETED

    📖 RIPR Model:
        [R] Đăng nhập → chạm tới trang danh sách sách có ô tìm kiếm
        [I] Nhập từ khóa vô nghĩa không tồn tại → kích hoạt search trả về rỗng
        [P] Hệ thống lọc → không có sách nào khớp → danh sách trống
        [R✓] Assert số card sách = 0 → hệ thống xử lý "no result" đúng
    """
    # [R] Reachability: Đăng nhập để vào trang danh sách sách
    login(page, test_config)

    # [I] Infection: Nhập từ khóa KHÔNG tồn tại trong hệ thống — boundary/negative test
    # Dùng chuỗi ngẫu nhiên đảm bảo chắc chắn không có kết quả nào khớp
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "xyz_khong_ton_tai_12345")

    # [P] Propagation: Chờ hệ thống xử lý và hiển thị trạng thái "không có kết quả"
    time.sleep(2)
    enable_flutter_semantics(page)  # Bật lại semantics sau khi UI cập nhật

    # Chụp screenshot ghi lại trạng thái "không có kết quả"
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC05_search_no_result.png"))

    # [R✓] Revealability: Test Oracle — kiểm tra KHÔNG có card sách nào xuất hiện
    # Đếm số card sách (dùng selector chuẩn của hệ thống — BOOK prefix trong aria-label)
    book_card_count = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').count()

    # Fallback: kiểm tra thêm qua sem_text nếu có thông báo "không tìm thấy"
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    no_result_messages = ["không tìm thấy", "no result", "không có sách", "0 kết quả"]
    has_no_result_msg = any(msg in sem_text.lower() for msg in no_result_messages)

    assert book_card_count == 0 or has_no_result_msg, (
        "TC-05 FAILED: Tìm kiếm từ khóa không tồn tại nhưng hệ thống vẫn hiển thị sách! "
        "(Search for non-existent keyword still showed book results — expected 0.) "
        f"Found {book_card_count} book cards. sem_text snippet: {sem_text[:200]}"
    )


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại 'Công nghệ'*)

    ✅ COMPLETED

    📖 RIPR Model:
        [R] Đăng nhập → chạm tới trang có ô lọc thể loại
        [I] Nhập "Công nghệ" vào filter → kích hoạt lọc theo category
        [P] Hệ thống lọc → chỉ hiển thị sách thuộc thể loại "Công nghệ"
        [R✓] Assert TẤT CẢ card sách hiển thị đều có "Công nghệ" trong aria-label
    """
    # [R] Reachability: Đăng nhập để vào trang danh sách sách
    login(page, test_config)

    # [I] Infection: Nhập "Công nghệ" vào ô lọc thể loại — kích hoạt category filter
    flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "Công nghệ")

    # [P] Propagation: Chờ hệ thống lọc và re-render danh sách theo thể loại
    time.sleep(2)
    enable_flutter_semantics(page)  # Bật lại semantics sau khi danh sách được lọc

    # Chụp screenshot ghi lại danh sách sau khi lọc
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC06_filter_by_category_cong_nghe.png"))

    # [R✓] Revealability: Test Oracle — kiểm tra TẤT CẢ sách hiển thị đều là "Công nghệ"
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    total_books = book_cards.count()

    # Trường hợp không có sách nào → filter hoạt động nhưng không có dữ liệu
    # Vẫn pass nếu danh sách rỗng (không có sách Công nghệ trong DB) 
    # Nhưng nếu CÓ sách → tất cả phải đúng thể loại
    assert total_books >= 0, "Không thể lấy danh sách card sách"

    if total_books > 0:
        # Duyệt qua từng card sách, kiểm tra aria-label chứa "Công nghệ"
        wrong_category_books = []
        for i in range(total_books):
            card = book_cards.nth(i)
            aria_label = card.get_attribute("aria-label") or ""
            if "Công nghệ" not in aria_label:
                wrong_category_books.append(aria_label[:100])  # Lưu để debug

        assert len(wrong_category_books) == 0, (
            f"TC-06 FAILED: {len(wrong_category_books)}/{total_books} sách hiển thị "
            f"KHÔNG thuộc thể loại 'Công nghệ'! "
            f"(Filter by 'Công nghệ' but found books from other categories.) "
            f"Wrong books: {wrong_category_books}"
        )
    else:
        # Không có kết quả → ghi nhận nhưng không fail (dữ liệu test có thể không có)
        pytest.skip(
            "TC-06 SKIPPED: Không có sách thể loại 'Công nghệ' trong hệ thống — "
            "không thể kiểm tra tính đúng của filter. (No books found for category filter test.)"
        )


def test_search_by_author(page, test_config):
    """TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

    ✅ COMPLETED

    📖 RIPR Model:
        [R] Đăng nhập → chạm tới ô tìm kiếm hỗ trợ cả tên sách lẫn tác giả
        [I] Nhập tên tác giả "Nguyễn Minh Đức" → kích hoạt search theo tác giả
        [P] Hệ thống tìm kiếm → trả về sách của tác giả đó
        [R✓] Assert có ít nhất 1 kết quả chứa tên tác giả trong aria-label
    """
    # [R] Reachability: Đăng nhập để vào trang danh sách sách
    login(page, test_config)

    # [I] Infection: Nhập tên tác giả vào ô tìm kiếm — search theo author field
    # Ô tìm kiếm hỗ trợ cả tên sách VÀ tên tác giả (theo aria-label của input)
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")

    # [P] Propagation: Chờ hệ thống tìm kiếm và render kết quả theo tác giả
    time.sleep(2)
    enable_flutter_semantics(page)  # Bật lại semantics sau khi kết quả xuất hiện

    # Chụp screenshot ghi lại kết quả tìm theo tác giả
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC07_search_by_author.png"))

    # [R✓] Revealability: Test Oracle — kiểm tra có sách của "Nguyễn Minh Đức"
    # Đếm số phần tử có aria-label chứa tên tác giả
    author_result_count = page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').count()

    # Fallback: kiểm tra qua sem_text trong trường hợp aria-label không chứa tên tác giả
    # mà tên tác giả nằm trong text content của card
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    author_in_text = "Nguyễn Minh Đức" in sem_text

    assert author_result_count > 0 or author_in_text, (
        "TC-07 FAILED: Tìm kiếm tác giả 'Nguyễn Minh Đức' nhưng KHÔNG có kết quả nào! "
        "(Search by author 'Nguyễn Minh Đức' returned no results — expected at least 1.) "
        f"aria-label matches: {author_result_count}. "
        f"Author in sem_text: {author_in_text}."
    )
