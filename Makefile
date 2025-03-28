DOCKER_COMPOSE_FILE = docker-compose.yml
POSTGRES_DB = demo

container-name = api_demo
docker-cmd = docker exec -it ${container-name} sh -c
venv-cmd = source .venv/bin/activate
test-cmd = pytest -n logical --dist loadscope

logs:
	docker logs -f ${container-name}


up:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d --remove-orphans

down:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

build:
	docker compose -f $(DOCKER_COMPOSE_FILE) build --no-cache

start:
	$(MAKE) build
	$(MAKE) up


functional-test:
	$(docker-cmd) "${test-cmd} functional_tests"

api-stop:
	docker stop ${container-name}


db-reset:
	docker exec -it postgres_demo psql -U postgres -c "DROP DATABASE IF EXISTS demo;" && \
	docker exec -it postgres_demo psql -U postgres -c "CREATE DATABASE demo;"

db: api-stop db-reset up

