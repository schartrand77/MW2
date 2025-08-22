docker-up:
	docker compose -f makerworks/infra/docker-compose.yml --env-file makerworks/infra/.env up --build

backend-test:
	cd makerworks/backend && python -m pytest

frontend-test:
	npm --prefix makerworks/frontend test

seed:
	python makerworks/backend/scripts/seed_demo.py

openapi:
	python makerworks/backend/scripts/generate_openapi.py && npx -y openapi-typescript makerworks/shared/openapi.json -o makerworks/shared/client.ts
