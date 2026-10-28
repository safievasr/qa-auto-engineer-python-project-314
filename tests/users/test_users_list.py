import pytest
from pages.users_page import UsersPage


@pytest.mark.smoke
def test_users_list_loads(users_page):
    assert users_page.is_visible(users_page.TABLE)


def test_users_table_shows_key_fields(users_page):
    headers_text = users_page.header_text()
    assert "email" in headers_text, headers_text
    assert ("first name" in headers_text or "first_name" in headers_text or "firstname" in headers_text), headers_text
    assert ("last name" in headers_text or "last_name" in headers_text or "lastname" in headers_text), headers_text