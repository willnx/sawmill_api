.PHONY: clean bootstrap build uninstall install

clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -f tests/.coverage

bootstrap:
	pip install -U -r requirements-dev.txt
	pre-commit install

smsh: clean
	mkdir -p build
	antlr4 -o ./build -no-listener -Dlanguage=Python3 SMSH.g4
	mv ./build/*.py ./sawmill_api/lib/smsh/

build: clean
	python -m build --wheel

uninstall:
	pip uninstall --yes sawmill_api

install: uninstall build
	pip install ./dist/sawmill_api*.whl
