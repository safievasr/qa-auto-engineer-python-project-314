import pytest

from data.users import make_user
from pages.user_form_page import UserFormPage


def _create(users_page, base_url, user):
    users_page.click_create()
    UserFormPage(users_page.driver).wait_opened().fill(user).save()

    users_page.open(base_url)
    users_page.row_by_text(user["email"])


def test_delete_single_user(users_page, base_url):
    user = make_user("del")
    _create(users_page, base_url, user)

    users_page.delete_row(user["email"])
    users_page.wait_for_absence(user["email"])


def test_bulk_delete_several_users(users_page, base_url):
    a, b = make_user("bulk1"), make_user("bulk2")
    _create(users_page, base_url, a)
    _create(users_page, base_url, b)

    users_page.select_row(a["email"])
    users_page.select_row(b["email"])
    users_page.bulk_delete_selected()

    users_page.wait_for_absence(a["email"])
    users_page.wait_for_absence(b["email"])


@pytest.mark.destructive
def test_select_all_and_delete_users_leaves_empty_list(users_page):
    assert users_page.rows(), "Для массового удаления нужен непустой список"

    users_page.delete_all()

    assert users_page.is_empty(timeout=10), "Список пользователей не пуст"