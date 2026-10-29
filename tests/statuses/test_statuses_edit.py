from pages.status_form_page import StatusFormPage


def test_edit_form_prefilled(statuses_page, created_status):
    statuses_page.open_edit_for(created_status["name"])
    form = StatusFormPage(statuses_page.driver).wait_opened()

    values = form.values()
    assert values["name"] == created_status["name"]
    assert values["slug"] == created_status["slug"]


def test_edit_updates_name(statuses_page, created_status, base_url):
    statuses_page.open_edit_for(created_status["name"])
    form = StatusFormPage(statuses_page.driver).wait_opened()

    new_name = created_status["name"] + " X"
    form.fill({"name": new_name}).save()

    statuses_page.open(base_url)
    statuses_page.row_by_text(new_name)


def test_edit_updates_slug(statuses_page, created_status, base_url):
    statuses_page.open_edit_for(created_status["name"])
    form = StatusFormPage(statuses_page.driver).wait_opened()

    new_slug = created_status["slug"] + "-x"
    form.fill({"slug": new_slug}).save()

    statuses_page.open(base_url)
    row = statuses_page.row_by_text(created_status["name"])
    assert new_slug in row.text
