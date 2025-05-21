.PHONY: clean bootstrap build uninstall install

clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -f tests/.coverage

bootstrap:
	pip install -U -r requirements-dev.txt
	pre-commit install

build: clean
	python -m build --wheel

uninstall:
	pip uninstall --yes sawmill_api

install: uninstall build
	pip install ./dist/sawmill_api*.whl
