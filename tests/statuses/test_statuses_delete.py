import pytest
from data.statuses import make_status
from pages.status_form_page import StatusFormPage


def _create(statuses_page, base_url, status):
    statuses_page.click_create()
    StatusFormPage(statuses_page.driver).wait_opened().fill(status).save()
    statuses_page.open(base_url)
    statuses_page.row_by_text(status["name"])


def test_delete_single_status(statuses_page, base_url):
    status = make_status("del")
    _create(statuses_page, base_url, status)

    statuses_page.delete_row(status["name"])
    statuses_page.wait_for_absence(status["name"])


def test_bulk_delete_several_statuses(statuses_page, base_url):
    a, b = make_status("bulk1"), make_status("bulk2")
    _create(statuses_page, base_url, a)
    _create(statuses_page, base_url, b)

    statuses_page.select_row(a["name"])
    statuses_page.select_row(b["name"])
    statuses_page.bulk_delete_selected()

    statuses_page.wait_for_absence(a["name"])
    statuses_page.wait_for_absence(b["name"])


@pytest.mark.destructive
def test_delete_all_statuses_empties_list(statuses_page, base_url):
    for prefix in ("da1", "da2", "da3"):
        _create(statuses_page, base_url, make_status(prefix))
    assert len(statuses_page.rows()) >= 3, "Данные для проверки не созданы"

    statuses_page.delete_all()
    assert statuses_page.is_empty(), \
        "После массового удаления список должен быть пуст"