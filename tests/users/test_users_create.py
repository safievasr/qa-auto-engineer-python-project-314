import pytest
from data.users import make_user
from pages.user_form_page import UserFormPage


@pytest.mark.smoke
def test_create_form_opens(users_page):
    users_page.click_create()
    form = UserFormPage(users_page.driver).wait_opened()
    assert form.is_visible(form.EMAIL_INPUT)
    assert form.is_visible(form.FIRST_NAME_INPUT)
    assert form.is_visible(form.LAST_NAME_INPUT)


def test_create_user_appears_in_list(users_page, base_url):
    user = make_user()
    users_page.click_create()
    UserFormPage(users_page.driver).wait_opened().fill(user).save()

    users_page.open(base_url)
    users_page.row_by_text(user["email"])


def test_create_user_without_email_blocked(users_page, base_url):
    users_page.click_create()
    form = UserFormPage(users_page.driver).wait_opened()
    form.fill({"first_name": "NoMail", "last_name": "User"})

    form.save(expect_redirect=False)

    assert form.is_visible(form.FORM) or form.has_email_error(), \
        "Приложение не должно уходить с формы без email"