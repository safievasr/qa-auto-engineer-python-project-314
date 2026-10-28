import pytest


@pytest.mark.smoke
def test_board_loads(board_page):
    titles = board_page.column_titles()
    assert titles, "На доске нет ни одной колонки"
    assert len(titles) >= 3


def test_created_task_appears_in_column(board_page, created_task):
    assert created_task["status"] in board_page.column_titles()
    assert board_page.is_task_in_column(
        created_task["title"], created_task["status"]
    )


def test_move_task_between_columns(board_page, created_task):
    board_page.open()
    other = next(
        (t for t in board_page.column_titles() if t != created_task["status"]),
        None,
    )
    assert other, "На доске только одна колонка"

    try:
        board_page.move_by_drag(created_task["title"], other)
    except Exception:
        board_page.move_via_edit(created_task["title"], other)

    board_page.open()
    assert board_page.is_task_in_column(
        created_task["title"], other, timeout=10
    ), (
        f"Задача не в колонке {other!r}. "
        f"Колонки: {board_page.column_titles()}"
    )