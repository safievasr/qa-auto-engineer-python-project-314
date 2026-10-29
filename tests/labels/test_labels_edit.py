from selenium.webdriver.support import expected_conditions as EC

from data.labels import make_label
from pages.label_form_page import LabelFormPage


def test_edit_form_prefilled(labels_page, created_label):
    labels_page.open_edit_for(created_label["name"])
    form = LabelFormPage(labels_page.driver).wait_opened()

    values = form.values()
    assert values["name"] == created_label["name"]


def test_edit_updates_name(labels_page, created_label):
    labels_page.open_edit_for(created_label["name"])
    form = LabelFormPage(labels_page.driver).wait_opened()

    new_name = make_label("renamed")["name"]
    form.fill({"name": new_name}).save()

    labels_page.open()

    labels_page.row_by_text(new_name)
    labels_page.wait_for_absence(created_label["name"])


def test_edit_to_empty_name_blocked(labels_page, created_label):
    labels_page.open_edit_for(created_label["name"])
    form = LabelFormPage(labels_page.driver).wait_opened()

    form.type(form.NAME_INPUT, "")
    form.save(expect_redirect=False)

    error = form.wait.until(EC.visibility_of_element_located(form.NAME_ERROR))
    assert error.text == "Required"
    assert form.values()["name"] == ""

    labels_page.open()
    assert labels_page.is_present(created_label["name"])