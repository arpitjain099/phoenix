
default_path = projects/phiphi/

up:
	@echo "Starting up the development environment..."
	docker compose up

down:
	@echo "Shutting down the development environment..."
	docker compose down

build:
	@echo "Building the development environment..."
	docker compose build

clean:
	@echo "Clean the development environment..."
	docker compose down -v --remove-orphans

bash_in_api:
	@echo "Starting a bash into the api container..."
	docker compose exec api bash

all:
	docker compose run api make all path=$(default_path)

test:
	docker compose run api make test path=$(default_path)

format:
	docker compose run api make format path=$(default_path)

fix_local_permissions:
	sudo chown -R $(USER):$(USER) phiphi/

# We are using an extra docker compose file to run alembic commands
# because there are a few differences in the environment setup
# when running an alembic command.
ALEMBIC_DOCKER_COMPOSE_COMMAND=docker compose -f docker-compose.yaml -f docker-compose.alembic.yaml run api

alembic_revision:
	@if [ -z "$(message)" ]; then \
		echo "Path argument is required; add \`message=...\` to the make command."; \
		exit 1; \
	fi
	$(ALEMBIC_DOCKER_COMPOSE_COMMAND) alembic revision --autogenerate -m "$(message)"

# Usage: make alembic_upgrade REVISION=base
# Default is head
alembic_upgrade:
	REVISION="${REVISION:-head}"
	$(ALEMBIC_DOCKER_COMPOSE_COMMAND) alembic upgrade $(REVISION)

# Usage: make alembic_downgrade REVISION=base
# or
# make alembic_downgrade REVISION=-1
# Default is -1
alembic_downgrade:
	REVISION="${REVISION:--1}"
	$(ALEMBIC_DOCKER_COMPOSE_COMMAND) alembic downgrade $(REVISION)
