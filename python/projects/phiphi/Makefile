
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
