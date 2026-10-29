import pytest

from pages.board_page import BoardPage
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_success(driver, base_url):
    LoginPage(driver).open(base_url).login("user", "password")

    board = BoardPage(driver, base_url).open()
    assert board.is_opened(), "После логина ожидали канбан-доску"
    assert not LoginPage(driver).is_opened(), "Форма логина должна исчезнуть"


def test_login_empty_credentials_stays_on_login(driver, base_url):
    page = LoginPage(driver).open(base_url)
    page.submit()
    assert page.is_opened(), "Ожидали остаться на странице логина"


def test_login_empty_password_stays_on_login(driver, base_url):
    page = LoginPage(driver).open(base_url)
    page.fill_username("user").submit()
    assert page.is_opened()