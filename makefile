.PHONY: check format test

check:
	.venv/bin/black --check pyquery tests
	.venv/bin/isort --check pyquery tests
	.venv/bin/mypy pyquery tests

format:
	.venv/bin/black pyquery tests
	.venv/bin/isort pyquery tests

test:
	.venv/bin/python -m pytest -x tests
