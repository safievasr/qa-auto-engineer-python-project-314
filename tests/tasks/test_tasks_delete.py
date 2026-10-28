from data.tasks import make_task
from pages.task_form_page import TaskFormPage


def _create(board_page, task):
    board_page.open()
    board_page.open_create_form()
    TaskFormPage(board_page.driver).wait_opened().fill(task).save()
    board_page.open()
    board_page.card_by_title(task["title"])


def test_delete_task_from_board(board_page):
    task = make_task("del")
    _create(board_page, task)

    board_page.open_edit_for(task["title"])
    TaskFormPage(board_page.driver).wait_opened().delete_current()

    board_page.open()
    board_page.wait_for_card_absence(task["title"])