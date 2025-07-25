.PHONY: test format check-format lint build-publish

test:
	poetry run pytest

test-all:
	poetry run pytest -m "cicd"

format:
	poetry run ruff format .

check-format:
	poetry run ruff check .

lint:
	poetry run mypy .

build-publish:
	poetry build
	poetry publish