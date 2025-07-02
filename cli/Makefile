.PHONY: test format check-format lint build-publish

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

build-publish:
	poetry build
	poetry publish