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


# Eat the extra arg for the migration name to avoid having Make treat it as a target.
ifeq ($(firstword $(MAKECMDGOALS)),migration)
%:
	@:
endif

migration:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Error: Migration name required (e.g. 'make migration add_users_table')"; \
		exit 1; \
	fi
	touch sawmill_api/migrations/V$(shell date +%Y%m%d%H%M%S)__$(filter-out $@,$(MAKECMDGOALS)).sql

migrate:
	docker run -it --rm --network sawmill_api_default \
		-v $(shell pwd)/sawmill_api/migrations:/flyway/sql \
		flyway/flyway:latest \
		-url=jdbc:postgresql://oltp:26257/sawmill \
		-user=sawmill \
		-password=a \
		migrate

up:
	docker compose up
