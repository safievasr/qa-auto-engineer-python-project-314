from data.tasks import make_task
from pages.task_form_page import TaskFormPage


def test_edit_form_prefilled(board_page, created_task):
    board_page.open_edit_for(created_task["title"])
    form = TaskFormPage(board_page.driver).wait_opened()

    title_el = board_page.driver.find_element(*form.TITLE_INPUT)
    assert title_el.get_attribute("value") == created_task["title"]


def test_edit_form_prefilled_with_content(board_page):
    task = make_task("content", content="Написать автотесты")
    board_page.open()
    board_page.open_create_form()
    TaskFormPage(board_page.driver).wait_opened().fill(task).save()

    board_page.open()
    board_page.card_by_title(task["title"])
    board_page.open_edit_for(task["title"])
    form = TaskFormPage(board_page.driver).wait_opened()

    content_el = board_page.driver.find_element(*form.CONTENT_INPUT)
    assert content_el.get_attribute("value") == task["content"]

    form.delete_current()


def test_edit_updates_title(board_page, created_task):
    board_page.open_edit_for(created_task["title"])
    form = TaskFormPage(board_page.driver).wait_opened()

    new_task = make_task("renamed")
    form.type(form.TITLE_INPUT, new_task["title"])
    form.save()

    board_page.open()
    board_page.card_by_title(new_task["title"])
    board_page.wait_for_card_absence(created_task["title"])