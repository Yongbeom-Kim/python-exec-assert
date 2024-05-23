SHELL := /bin/bash

all: upload

build:
	python3 -m pip install --upgrade build
	python3 -m build

upload: build
	python3 -m pip install --upgrade twine
	if [[ -z "$${TEST}" ]]; then  \
		python3 -m twine upload dist/* ; \
	else \
		python3 -m twine upload --repository testpypi dist/* ; \
	fi