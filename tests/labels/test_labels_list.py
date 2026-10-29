import pytest


@pytest.mark.smoke
def test_labels_list_loads(labels_page):
    assert labels_page.is_visible(labels_page.TABLE)


def test_labels_table_shows_key_fields(labels_page):
    headers_text = labels_page.header_text()
    assert "name" in headers_text, headers_text


def test_labels_list_shows_expected_label(labels_page, created_label):
    row = labels_page.row_by_text(created_label["name"])

    assert created_label["name"] in row.text