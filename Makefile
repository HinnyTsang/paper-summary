.PHONY: lint
lint:
	poetry run flake8 *.py **/*.py

.PHONY: format
format:
	poetry run black *.py **/*.py

.PHONY: secrets
secrets:
	blackbox_edit_start *.gpg