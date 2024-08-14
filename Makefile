.PHONY: deps-compile deps-install install install-dev

deps-install: deps-compile install-dev

install-dev:
	pip install -e .[dev]

install:
	pip install -e .

deps-compile:
	pip-compile --upgrade requirements.in --resolver backtracking --no-emit-index-url --no-emit-trusted-host

deps-sync:
	pip-sync requirements.txt

use-pip-tools:
	pip install --upgrade pip
	pip install pip-tools

use-pre-commit:
	pip install pre-commit
	pre-commit install
