import os
import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    page,
    wait_for_flutter,
    SCREENSHOT_DIR,
    login
)

"""
TC-13: Kiểm tra giới hạn mượn sách theo SRS (tối đa 3 quyển)
1. Login (ba.nguyen@email.com).
2. Check quantity books in Mượn / Trả tab
3. Borrow books until reach total 3 books (limit) - successful
4. Borrow 4th book - should be blocked with error message contains "giới hạn mượn"
5. Verify quantity books in Mượn / Trả tab 
"""
def get_count(page):
    return page.locator('flt-semantics[role="group"][aria-label*="Đang mượn"]').count()
def borrow_first_available_book(page, expect_success=True):
    available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]')
    assert available_book.count() > 0, "No available book found"
    book = available_book.first
    book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")').first.click()
    
    wait_for_flutter(page, text="Xác nhận")
    enable_flutter_semantics(page)
    
    confirm_button = page.locator('flt-semantics[role="button"]:has-text("Mượn")')
    assert confirm_button.count() > 0
    confirm_button.first.click()
    
    if expect_success:
        # wait_for_flutter(page, text="thành công")
        # enable_flutter_semantics(page)
        success_msg = page.locator('flt-semantics:has-text("thành công")').first
        success_msg.wait_for(state="visible", timeout=10000)
        success_msg.wait_for(state="hidden", timeout=10000)
        enable_flutter_semantics(page)
    else:
        page.wait_for_timeout(3000)
        has_error = page.locator('flt-semantics:has-text("giới hạn mượn")')
        assert has_error.count() > 0, "Borrow limit error dialog was not displayed"  

def test_borrow_more_than_3_books(page, test_config):
    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection
    flutter_fill(page, "Email", "ba.nguyen@email.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)
    
    # 1. Check current borrow count on "Mượn / Trả" tab
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()
    wait_for_flutter(page)
    current_count = get_count(page)
    
    # 2. Go to "Sách" tab to borrow up to the limit
    page.locator('flt-semantics[role="tab"][aria-label="Sách"]').first.click()
    wait_for_flutter(page)
    
    MAX_BOOKS = 3  
    remaining = MAX_BOOKS - current_count
    for _ in range(remaining):
        borrow_first_available_book(page, expect_success=True)
    
    # Reached the limit, try to borrow one more book
    borrow_first_available_book(page, expect_success=False)
    wait_for_flutter(page)
      
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_over_limit.png"))
    wait_for_flutter(page)
    
    # 3. Go back to "Mượn / Trả" to verify the count did not increase
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()
    wait_for_flutter(page)
    page.wait_for_timeout(3000)
    after_count = get_count(page)
    assert after_count == MAX_BOOKS, f"Expected {MAX_BOOKS} books, but found {after_count}"
    
# mượn quá giới hạn vẫn mượn được, UI có hiển thị nhưng không có sematic (VD UI hiển thị 4 nhưng chỉ có 3)

# # TC-14 + TC-15: account không hợp lệ (suspended / expired) → không được mượn sách
@pytest.mark.parametrize(
    "email,password,expected_error,tc_id",
    [
        ("cu.le@email.com", "password123", "Tài khoản đã bị tạm ngưng.", "TC-14"),
        ("binh.pham@email.com", "password123", "Thành viên đã hết hạn.", "TC-15"),
    ],
    ids=[
        "TC-14 Suspended Member",
        "TC-15 Expired Member"
    ]
)

def test_invalid_member_cannot_borrow(page,test_config,email,password, expected_error, tc_id):
    # [R] Reachability
    page.goto(test_config["base_url"])
    enable_flutter_semantics(page)

    # [I] Infection
    flutter_fill(page, "Email", email)
    flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")

    available_books = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]')
    book = available_books.first 

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

    # [P] Propagation - Wait UI update
    wait_for_flutter(page, text=expected_error)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR,f"borrow_denied_{expected_error}_{tc_id}.png"))

    # 6. [R] Revealability - Assert error message
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_error = expected_error in sem_text
    assert has_error, \
        f"Expected error message not found for {tc_id} (Không tìm thấy thông báo lỗi cho {tc_id})"
        





   