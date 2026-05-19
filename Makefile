.PHONY: install

install:
	poetry update
	poetry run pre-commit install
