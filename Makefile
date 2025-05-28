.PHONY: clean bootstrap smsh build uninstall install images up

clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -f tests/.coverage
	docker system prune --force

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

images: build
	docker build --file Dockerfiles/ApiDockerfile --tag sawmill/api .

up:
	docker compose up --abort-on-container-failure
