import pytest


@pytest.mark.smoke
def test_statuses_list_loads(statuses_page):
    assert statuses_page.is_visible(statuses_page.TABLE)


def test_statuses_table_shows_key_fields(statuses_page):
    headers_text = statuses_page.header_text()
    assert "name" in headers_text, headers_text
    assert "slug" in headers_text, headers_text


def test_statuses_list_shows_expected_status_values(
    statuses_page, created_status
):
    row = statuses_page.row_by_text(created_status["name"])

    assert created_status["slug"] in row.text