
# lint the project
lint:
	poetry run mypy bods_client tests/**/*.py
	poetry run flake8 bods_client tests
	poetry run doc8 -q docs

# run all the tests
test-all:
	poetry run pytest tests/

# run specific tests
test TEST:
	poetry run pytest {{TEST}}

# check dependencies
check:
	poetry check
	poetry run pip check
	poetry run safety check --full-report

# Run all linting, checks and tests
all: lint check test-all
