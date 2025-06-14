.PHONY: test format check-format lint

test:
	poetry run pytest

test-all:
	poetry run pytest -m "cicd"

format:
	poetry run black .

check-format:
	poetry run black --check .

lint:
	poetry run mypy .