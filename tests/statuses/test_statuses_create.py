import pytest
from data.statuses import make_status
from pages.status_form_page import StatusFormPage


@pytest.mark.smoke
def test_create_form_opens(statuses_page):
    statuses_page.click_create()
    form = StatusFormPage(statuses_page.driver).wait_opened()
    assert form.is_visible(form.NAME_INPUT)
    assert form.is_visible(form.SLUG_INPUT)


def test_create_status_appears_in_list(statuses_page, base_url):
    status = make_status()
    statuses_page.click_create()
    StatusFormPage(statuses_page.driver).wait_opened().fill(status).save()

    statuses_page.open(base_url)
    row = statuses_page.row_by_text(status["name"])
    assert status["slug"] in row.text


def test_create_status_without_required_fields_blocked(statuses_page):
    statuses_page.click_create()
    form = StatusFormPage(statuses_page.driver).wait_opened()

    if form.is_save_enabled():
        form.save(expect_redirect=False)

    assert not form.is_save_enabled() or form.is_visible(
        form.FIELD_ERROR, timeout=1
    ), "Пустая форма не должна сохраняться"