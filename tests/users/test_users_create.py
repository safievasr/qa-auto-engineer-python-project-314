import pytest
from selenium.webdriver.support import expected_conditions as EC

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
    user = make_user("nomail")
    users_page.click_create()
    form = UserFormPage(users_page.driver).wait_opened()
    form.fill({
        "first_name": user["first_name"],
        "last_name": user["last_name"],
    })

    form.save(expect_redirect=False)

    error = form.wait.until(EC.visibility_of_element_located(form.EMAIL_ERROR))
    assert error.text == "Required"
    assert form.values()["email"] == ""
    users_page.open(base_url)
    assert not users_page.is_present(user["first_name"], timeout=1)