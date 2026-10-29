start:
	docker run --rm -p 5173:5173 hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app

install:
	uv sync --locked

smoke:
	uv run pytest -k smoke

lint:
	uv run ruff check .

test:
	uv run pytest

check: lint test

test-coverage:
	uv run pytest --cov=core --cov=pages --cov=data --cov=src --cov-report=xml:coverage.xml

auth:
	uv run pytest tests/auth -v

.PHONY: install update test lint selfcheck check build test-coverage smoke start auth
