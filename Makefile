.PHONY: install

install:
	poetry update
	poetry run pre-commit install
	poetry run pre-commit install --hook-type commit-msg
