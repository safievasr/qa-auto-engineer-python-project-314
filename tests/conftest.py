import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage
from pages.users_page import UsersPage
from data.users import make_user
from pages.user_form_page import UserFormPage
from pages.statuses_page import StatusesPage
from pages.status_form_page import StatusFormPage
from data.statuses import make_status
from pages.labels_page import LabelsPage
from pages.label_form_page import LabelFormPage
from data.labels import make_label
from pages.task_form_page import TaskFormPage
from pages.board_page import BoardPage
from data.tasks import make_task


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("APP_BASE_URL", "http://localhost:5173").rstrip("/")


@pytest.fixture
def driver():
    opts = Options()
    opts.add_argument("--window-size=1366,768")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--lang=ru-RU")
    if os.getenv("HEADLESS", "1") == "1":
        opts.add_argument("--headless=new")

    driver = webdriver.Chrome(options=opts)
    yield driver
    try:
        driver.quit()
    except Exception:
        pass


@pytest.fixture
def authorized_user(driver, base_url):
    LoginPage(driver).open(base_url).login("user", "password")
    yield driver


@pytest.fixture
def users_page(authorized_user, base_url):
    return UsersPage(authorized_user, base_url).open()


@pytest.fixture
def created_user(users_page, base_url):
    user = make_user()
    users_page.click_create()
    UserFormPage(users_page.driver).wait_opened().fill(user).save()

    users_page.open(base_url)
    users_page.row_by_text(user["email"])
    yield user

    users_page.open()
    if users_page.is_present(user["email"], timeout=1.0):
        users_page.delete_row(user["email"])


@pytest.fixture
def statuses_page(authorized_user, base_url):
    return StatusesPage(authorized_user, base_url).open()


@pytest.fixture
def created_status(statuses_page, base_url):
    status = make_status()
    statuses_page.click_create()
    StatusFormPage(statuses_page.driver).wait_opened().fill(status).save()

    statuses_page.open(base_url)
    statuses_page.row_by_text(status["name"])
    yield status

    statuses_page.open()
    if statuses_page.is_present(status["name"], timeout=1.0):
        statuses_page.delete_row(status["name"])


@pytest.fixture
def labels_page(authorized_user, base_url):
    return LabelsPage(authorized_user, base_url).open()


@pytest.fixture
def created_label(labels_page, base_url):
    label = make_label()
    labels_page.click_create()
    LabelFormPage(labels_page.driver).wait_opened().fill(label).save()

    labels_page.open()
    labels_page.row_by_text(label["name"])

    yield label

    labels_page.open()
    if labels_page.is_present(label["name"], timeout=1.0):
        labels_page.delete_row(label["name"])


@pytest.fixture
def board_page(authorized_user, base_url):
    return BoardPage(authorized_user, base_url).open()


@pytest.fixture
def created_task(board_page):
    task = make_task()

    board_page.open()
    board_page.open_create_form()
    TaskFormPage(board_page.driver).wait_opened().fill(task).save()

    board_page.open()
    board_page.card_by_title(task["title"])

    yield task

    board_page.open()
    board_page.clear_filters()
    if board_page.column_of_card(task["title"]):
        board_page.open_edit_for(task["title"])
        TaskFormPage(board_page.driver).wait_opened().delete_current()