.PHONY: clean bootstrap smsh build uninstall install images migration migrate up

clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -f tests/.coverage
	docker system prune --force

bootstrap:
	pip install -U -r requirements-dev.txt
	pre-commit install
	curl -fsSL -o dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64
	chmod +x ./dbmate

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

migration:
	./dbmate --migrations-dir sawmill_api/migrations new $(filter-out $@,$(MAKECMDGOALS))

migrate:
	./dbmate --url "postgresql://sawmill:a@localhost:26257/sawmill?sslmode=require" --migrations-dir sawmill_api/migrations up --strict --verbose

up:
	docker compose up --abort-on-container-failure
