import pytest

from pages.login_page import LoginPage


@pytest.mark.smoke
def test_app_opens_login_form(driver, base_url):
    page = LoginPage(driver).open(base_url)
    assert page.is_opened(), "Форма логина не отображается"


@pytest.mark.smoke
def test_login_form_has_core_fields(driver, base_url):
    page = LoginPage(driver).open(base_url)
    assert page.is_visible(page.USERNAME), "Нет поля логина"
    assert page.is_visible(page.PASSWORD), "Нет поля пароля"
    assert page.is_visible(page.SUBMIT), "Нет кнопки входа"