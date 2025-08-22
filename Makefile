docker-up:
	docker compose -f makerworks/infra/docker-compose.yml --env-file makerworks/infra/.env up --build

backend-test:
	cd makerworks/backend && python -m pytest

frontend-test:
	npm --prefix makerworks/frontend test
