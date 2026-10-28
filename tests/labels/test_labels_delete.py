import pytest
from data.labels import make_label
from pages.label_form_page import LabelFormPage


def _create(labels_page, label):
    labels_page.click_create()
    LabelFormPage(labels_page.driver).wait_opened().fill(label).save()
    labels_page.open()
    labels_page.row_by_text(label["name"])


def test_delete_single_label(labels_page):
    label = make_label("del")
    _create(labels_page, label)

    labels_page.delete_row(label["name"])
    labels_page.wait_for_absence(label["name"])


def test_delete_several_labels(labels_page):
    a, b = make_label("bulk1"), make_label("bulk2")
    _create(labels_page, a)
    _create(labels_page, b)

    labels_page.select_row(a["name"])
    labels_page.select_row(b["name"])
    labels_page.bulk_delete_selected()

    labels_page.wait_for_absence(a["name"])
    labels_page.wait_for_absence(b["name"])