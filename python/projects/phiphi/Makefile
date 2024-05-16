
default_path = projects/phiphi/
phiphi_gitlab_repo = registry.gitlab.com/howtobuildup/phoenix/python/phiphi
tag ?= latest
image ?= "$(phiphi_gitlab_repo):$(tag)"

DEV_COMPOSE_COMMAND=docker compose -f compose.yaml -f compose.dev.yaml

up:
	@echo "Starting up the development environment..."
	$(DEV_COMPOSE_COMMAND) up

down:
	@echo "Shutting down the development environment..."
	$(DEV_COMPOSE_COMMAND) down

build:
	@echo "Building the development and CI environment..."
	docker compose build

clean:
	@echo "Clean the development environment..."
	docker compose down -v --remove-orphans

bash_in_api:
	@echo "Starting bash in the dev api environment"
	$(DEV_COMPOSE_COMMAND) exec api bash

all:
	@echo "Running `all` in ci environment"
	docker compose run api make all path=$(default_path)

test:
	@echo "Running `format` in ci environment"
	docker compose run api make test path=$(default_path)

format:
	@echo "Running `format` in ci environment"
	docker compose run api make format path=$(default_path)

# Usage: make create_prefect_deployments image=registry.gitlab.com/howtobuildup/phoenix/python/phiphi:main
# This function can be used in CI to create all prefect deployments with the image that it has
# just published
create_prefect_deployments:
	@echo "Create prefect deployments"
	$(DEV_COMPOSE_COMMAND) run api python projects/phiphi/phiphi/prefect_deployments.py --image $(image)

fix_local_permissions:
	sudo chown -R $(USER):$(USER) phiphi/

# We are using an extra docker compose file to run alembic commands
# because there are a few differences in the environment setup
# when running an alembic command.
ALEMBIC_DOCKER_COMPOSE_COMMAND=docker compose -f compose.yaml -f compose.alembic.yaml run api

alembic_revision:
	@if [ -z "$(message)" ]; then \
		echo "Path argument is required; add \`message=...\` to the make command."; \
		exit 1; \
	fi
	$(ALEMBIC_DOCKER_COMPOSE_COMMAND) alembic revision --autogenerate -m "$(message)"

UPGRADE_REVISION ?= heads
# Usage: make alembic_upgrade UPGRADE_REVISION=base
# Default is head
alembic_upgrade:
	$(ALEMBIC_DOCKER_COMPOSE_COMMAND) alembic upgrade $(UPGRADE_REVISION)

DOWNGRADE_REVISION ?= -1
# Usage: make alembic_downgrade DOWNGRADE_REVISION=base
# or
# make alembic_downgrade DOWNGRADE_REVISION=-1
# Default is -1
alembic_downgrade:
	$(ALEMBIC_DOCKER_COMPOSE_COMMAND) alembic downgrade $(DOWNGRADE_REVISION)


psql_dev:
	@echo "Connecting to the development database..."
	@echo "default password is 'password'"
	psql -h localhost -p 5432 -U postgres -d test_db

psql_test:
	@echo "Connecting to the test database..."
	@echo "default password is 'password'"
	psql -h localhost -p 5433 -U postgres -d test_db

reseed_testing:
	@echo "Reseeding the database with test data"
	docker compose run api python projects/phiphi/phiphi/seed/main.py --testing

