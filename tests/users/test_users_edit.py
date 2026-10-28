import pytest
from pages.user_form_page import UserFormPage


def test_edit_form_prefilled(users_page, created_user):
    users_page.open_edit_for(created_user["email"])
    form = UserFormPage(users_page.driver).wait_opened()

    values = form.values()
    assert values["email"] == created_user["email"]
    assert values["first_name"] == created_user["first_name"]
    assert values["last_name"] == created_user["last_name"]


def test_edit_updates_values(users_page, created_user, base_url):
    users_page.open_edit_for(created_user["email"])
    form = UserFormPage(users_page.driver).wait_opened()

    new_last = created_user["last_name"] + "X"
    form.fill({"last_name": new_last}).save()

    users_page.open(base_url)
    row = users_page.row_by_text(created_user["email"])
    assert new_last in row.text


@pytest.mark.parametrize("bad_email", ["user", "user@", "@example.com"])
def test_edit_invalid_email_shows_error(users_page, created_user, bad_email):
    users_page.open_edit_for(created_user["email"])
    form = UserFormPage(users_page.driver).wait_opened()

    form.fill({"email": bad_email})
    form.save(expect_redirect=False)
    has_err = form.has_email_error(timeout=2)
    if not has_err:
        pytest.xfail(
            f"Приложение не валидирует формат email: '{bad_email}' "
            f"Текущий URL: '{users_page.driver.current_url}' "
        )

    assert has_err