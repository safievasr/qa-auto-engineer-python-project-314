import pytest

from data.tasks import make_task
from pages.task_form_page import TaskFormPage


@pytest.mark.smoke
def test_create_form_opens(board_page):
    board_page.open_create_form()
    form = TaskFormPage(board_page.driver).wait_opened()
    assert form.is_visible(form.TITLE_INPUT)


def test_create_task_appears_on_board(board_page):
    task = make_task()
    board_page.open()
    board_page.open_create_form()
    TaskFormPage(board_page.driver).wait_opened().fill(task).save()

    board_page.open()
    board_page.card_by_title(task["title"])
    assert board_page.column_of_card(task["title"]) == "Draft"


def test_create_task_without_title_blocked(board_page):
    board_page.open()
    board_page.open_create_form()
    form = TaskFormPage(board_page.driver).wait_opened()

    if form.is_save_enabled():
        form.save(expect_redirect=False)

    assert not form.is_save_enabled() or form.is_visible(
        form.FIELD_ERROR, timeout=1
    ), "Пустая задача не должна сохраняться"