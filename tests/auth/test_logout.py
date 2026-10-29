import pytest

from pages.board_page import BoardPage
from pages.login_page import LoginPage


@pytest.fixture
def logged_in(driver, base_url):
    LoginPage(driver).open(base_url).login("user", "password")
    board = BoardPage(driver, base_url).open()
    assert board.is_opened()
    return board


def test_logout_returns_to_login(logged_in, base_url):
    logged_in.logout()

    login = LoginPage(logged_in.driver)
    assert login.is_opened(), "После выхода должна открыться форма логина"


def test_cannot_access_board_after_logout(logged_in, base_url):
    logged_in.logout()
    logged_in.driver.get(base_url + "/#/")
    assert LoginPage(logged_in.driver).is_opened()