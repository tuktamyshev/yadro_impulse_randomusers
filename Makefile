DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
BASE_ENV = --env-file env/.env.default
ENV = --env-file env/.env.docker

ALL_FILE = docker_compose/all.yml
APP_FILE = docker_compose/app.yml
DB_FILE = docker_compose/db.yml

APP_CONTAINER = yadro-impulse-randomusers-app
DB_CONTAINER = yadro-impulse-randomusers-db

.PHONY: ruff
ruff:
	ruff format && ruff check --fix

.PHONY: alembic
alembic:
	alembic revision --autogenerate -m "$(m)"

.PHONY: all
all:
	$(DC) -f $(ALL_FILE) -f $(DB_FILE) $(BASE_ENV) $(ENV) up --build -d  --force-recreate

.PHONY: all-down
all-down:
	$(DC) -f $(ALL_FILE) -f $(DB_FILE) $(BASE_ENV) $(ENV) down

.PHONY: app
app:
	$(DC) -f $(APP_FILE) $(BASE_ENV) $(ENV) up --build -d  --force-recreate

.PHONY: app-shell
app-shell:
	$(EXEC) $(APP_CONTAINER) bash

.PHONY: app-down
app-down:
	$(DC) -f $(APP_FILE) $(BASE_ENV) $(ENV) down

.PHONY: app-logs
app-logs:
	$(LOGS) $(APP_CONTAINER) -f

.PHONY: db
db:
	$(DC) -f $(DB_FILE) $(BASE_ENV) $(ENV) up --build -d

.PHONY: db-shell
db-shell:
	$(EXEC) $(DB_CONTAINER) bash

.PHONY: db-down
db-down:
	$(DC) -f $(DB_FILE) $(BASE_ENV) $(ENV) down

.PHONY: db-logs
db-logs:
	$(LOGS) $(DB_CONTAINER) -f
