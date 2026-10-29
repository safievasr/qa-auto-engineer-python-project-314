import pytest
from selenium.webdriver.support import expected_conditions as EC

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
def test_edit_invalid_email_shows_error(
    users_page, created_user, bad_email, base_url
):
    users_page.open_edit_for(created_user["email"])
    form = UserFormPage(users_page.driver).wait_opened()

    form.fill({"email": bad_email})
    form.save(expect_redirect=False)

    error = form.wait.until(EC.visibility_of_element_located(form.EMAIL_ERROR))
    assert error.text == "Must be a valid email"
    assert form.values()["email"] == bad_email

    users_page.open(base_url)
    assert users_page.is_present(created_user["email"])
    assert not users_page.is_present(bad_email, timeout=1)