# Test Report — Library Book Borrowing System

## Summary

| Total Test Cases | Passed | Failed |
|:----------------:|:------:|:------:|
| 15 | 12 | 3 |

---

## test_login.py

| Test ID | Function | Description | Pass / Fail |
|---------|----------|-------------|:-----------:|
| TC-01 | `test_login_success` | Ensures valid credentials allow login and the user session is established (display name or Logout button appears). | ✅ PASSED |
| TC-02 | `test_login_fail_wrong_password` | Ensures login is rejected when the correct email is paired with a wrong password; user stays on the login page. | ✅ PASSED |
| TC-03 | `test_login_fail_empty_fields` | Ensures login is rejected when both fields are empty; the page does not navigate away. | ✅ PASSED |

---

## test_search.py

| Test ID | Function | Description | Pass / Fail |
|---------|----------|-------------|:-----------:|
| TC-04 | `test_search_book_by_name` | Searching by keyword "Flutter" must return at least one matching book result. | ✅ PASSED |
| TC-05 | `test_search_book_no_result` | A nonsense keyword returns zero results, confirming the search filter works correctly. | ✅ PASSED |
| TC-06 | `test_filter_by_category` | Filtering by the category "Công nghệ" shows only books that carry that category label. | ✅ PASSED |
| TC-07 | `test_search_by_author` | Searching by author name "Nguyễn Minh Đức" returns at least one result containing that name in the book card. | ✅ PASSED |

---

## test_borrow_return.py

| Test ID | Function | Description | Pass / Fail |
|---------|----------|-------------|:-----------:|
| TC-08 | `test_borrow_book` | Confirms a user can borrow an available book; the available-copy count decreases by one after confirming the dialog. | ✅ PASSED |
| TC-09 | `test_view_borrowed_books` | Confirms the "Mượn / Trả" tab lists currently borrowed books with "Đang mượn" status and a return button for each. | ✅ PASSED |
| TC-10 | `test_return_book` | Confirms a user can return a borrowed book; the borrowed-book count decreases by one after clicking "Trả sách". | ✅ PASSED |

---

## test_general.py

| Test ID | Function | Description | Pass / Fail |
|---------|----------|-------------|:-----------:|
| TC-11 | `test_logout` | Clicking "Đăng xuất" ends the session and redirects to the login page; the Logout button is no longer visible. | ✅ PASSED |
| TC-12 | `test_switch_language_to_english` | Clicking the "EN" button switches the UI to English; at least one English keyword (e.g. "Logout", "Borrow") appears. | ✅ PASSED |

---

## bonus3TC.py

| Test ID | Function | Description | Pass / Fail |
|---------|----------|-------------|:-----------:|
| TC-13 | `test_borrow_more_than_3_books` | Verifies the 3-book borrow limit; attempting a 4th borrow must show an error ("giới hạn mượn") and keep the count at 3. | ❌ FAILED |
| TC-14 | `test_invalid_member_cannot_borrow` *(Suspended)* | A suspended account (`cu.le@email.com`) must receive the error "Tài khoản đã bị tạm ngưng." when attempting to borrow. | ❌ FAILED |
| TC-15 | `test_invalid_member_cannot_borrow` *(Expired)* | An expired-membership account (`binh.pham@email.com`) must receive the error "Thành viên đã hết hạn." when attempting to borrow. | ✅ PASSED |
