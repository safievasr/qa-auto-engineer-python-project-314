import pytest


@pytest.mark.smoke
def test_statuses_list_loads(statuses_page):
    assert statuses_page.is_visible(statuses_page.TABLE)


def test_statuses_table_shows_key_fields(statuses_page):
    headers_text = statuses_page.header_text()
    assert "name" in headers_text, headers_text
    assert "slug" in headers_text, headers_text