start:
	docker run --rm -p 5173:5173 hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app

smoke:
	uv run pytest -k smoke

test:
	uv run pytest

auth:
	uv run pytest tests/auth -v

.PHONY: install update test lint selfcheck check build
