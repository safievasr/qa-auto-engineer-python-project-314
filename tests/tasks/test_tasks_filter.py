from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.labels import make_label
from data.tasks import make_task
from pages.label_form_page import LabelFormPage
from pages.labels_page import LabelsPage
from pages.task_form_page import TaskFormPage


def _open_and_pick(driver, field: str, value: str):
    wrapper = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//div[@data-source='{field}']")
        )
    )
    clickable = wrapper.find_element(By.CSS_SELECTOR, ".MuiInputBase-root")
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});", clickable
    )
    try:
        clickable.click()
    except Exception:
        driver.execute_script("arguments[0].click();", clickable)

    WebDriverWait(driver, 5).until(
        lambda d: any(
            o.is_displayed()
            for o in d.find_elements(
                By.CSS_SELECTOR,
                "li[role='option'], div[role='option'], li.MuiMenuItem-root",
            )
        )
    )
    opts = driver.find_elements(
        By.CSS_SELECTOR,
        "li[role='option'], div[role='option'], li.MuiMenuItem-root",
    )
    for opt in opts:
        if opt.is_displayed() and value in (opt.text or ""):
            try:
                opt.click()
            except Exception:
                driver.execute_script("arguments[0].click();", opt)
            return
    raise AssertionError(
        f"Опция {value!r} не найдена в фильтре {field!r}. "
        f"Доступные: {[o.text for o in opts if o.is_displayed()]}"
    )


def _create_task(board_page, task):
    board_page.open()
    board_page.open_create_form()
    TaskFormPage(board_page.driver).wait_opened().fill(task).save()
    board_page.open()
    board_page.card_by_title(task["title"])


def _delete_task(board_page, title):
    board_page.clear_filters()
    board_page.open()
    board_page.open_edit_for(title)
    TaskFormPage(board_page.driver).wait_opened().delete_current()


def test_filter_by_status(board_page, created_task):
    board_page.open()
    target = created_task["status"]
    other_status = next(
        (t for t in board_page.column_titles() if t != target), None
    )
    assert other_status, (
        f"На доске только одна колонка ({target!r}) — не с чем сравнивать"
    )

    other = make_task("flt-other", status=other_status)
    _create_task(board_page, other)

    try:
        assert board_page.column_of_card(created_task["title"]) == target
        assert board_page.column_of_card(other["title"]) == other_status

        _open_and_pick(board_page.driver, "status_id", target)

        board_page.wait_for_card_absence(other["title"])
        assert board_page.column_of_card(created_task["title"]) == target
    finally:
        _delete_task(board_page, other["title"])


def test_filter_by_assignee(board_page, created_task):
    board_page.open()
    current = created_task["assignee"]
    other_assignee = (
        "emily@example.com"
        if current != "emily@example.com"
        else "michael@example.com"
    )

    matching = make_task(
        "flt-assignee-match",
        status=created_task["status"],
        assignee=current,
    )
    non_matching = make_task(
        "flt-assignee-other",
        status=created_task["status"],
        assignee=other_assignee,
    )

    try:
        _create_task(board_page, matching)
        _create_task(board_page, non_matching)
        assert board_page.column_of_card(matching["title"]) == matching["status"]
        assert (
            board_page.column_of_card(non_matching["title"])
            == non_matching["status"]
        )

        _open_and_pick(board_page.driver, "assignee_id", current)

        assert board_page.column_of_card(matching["title"]) == matching["status"]
        board_page.wait_for_card_absence(non_matching["title"])
    finally:
        _delete_task(board_page, matching["title"])
        _delete_task(board_page, non_matching["title"])


def test_filter_by_label(board_page, base_url):
    labels_page = LabelsPage(board_page.driver, base_url).open()
    label = make_label("flt-lbl")
    labels_page.click_create()
    LabelFormPage(labels_page.driver).wait_opened().fill(label).save()
    labels_page.open()
    labels_page.row_by_text(label["name"])

    task_with = make_task("flt-with-lbl", labels=[label["name"]])
    task_without = make_task("flt-no-lbl")

    try:
        _create_task(board_page, task_with)
        _create_task(board_page, task_without)

        _open_and_pick(board_page.driver, "label_id", label["name"])

        board_page.wait_for_card_absence(task_without["title"])
        assert board_page.column_of_card(task_with["title"]) is not None
    finally:
        _delete_task(board_page, task_with["title"])
        _delete_task(board_page, task_without["title"])
        labels_page.open()
        labels_page.delete_row(label["name"])
        labels_page.wait_for_absence(label["name"])