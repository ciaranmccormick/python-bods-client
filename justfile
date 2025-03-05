
# lint the project
lint:
	# uv run mypy bods_client tests/**/*.py
	uv run flake8 bods_client tests
	uv run doc8 -q docs

# run all the tests
test-all:
	uv run pytest tests/

# run specific tests
test TEST:
	uv run pytest {{TEST}}

# check dependencies
check:
	uv run pip check
	uv run pip-audit

# lock and install poetry dependencies
linstall:
  uv sync

# Run all linting, checks and tests
all: lint check test-all
