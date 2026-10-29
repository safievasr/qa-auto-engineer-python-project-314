import pytest

from data.labels import make_label
from pages.label_form_page import LabelFormPage


@pytest.mark.smoke
def test_create_form_opens(labels_page):
    labels_page.click_create()
    form = LabelFormPage(labels_page.driver).wait_opened()
    assert form.is_visible(form.NAME_INPUT)


def test_create_label_appears_in_list(labels_page):
    label = make_label()
    labels_page.click_create()
    LabelFormPage(labels_page.driver).wait_opened().fill(label).save()

    labels_page.open()
    labels_page.row_by_text(label["name"])


def test_create_label_without_name_blocked(labels_page):
    labels_page.click_create()
    form = LabelFormPage(labels_page.driver).wait_opened()

    if form.is_save_enabled():
        form.save(expect_redirect=False)

    assert not form.is_save_enabled() or form.is_visible(
        form.FIELD_ERROR, timeout=1
    ), "Пустая форма не должна сохраняться"