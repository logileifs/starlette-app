setup:
	pip install pipenv
	pipenv install --dev

run:
	uvicorn api.app:app --port=8989 --reload

up:
	docker-compose up -d --force-recreate

down:
	docker-compose down

test:
	python -m unittest discover -v -s tests -p "*test*.py"

coverage:
	coverage run -a --include=api/* -m unittest discover tests/ -p "*test*.py" && coverage report

db-up:
	docker-compose up -d --force-recreate rethink

db-down:
	docker-compose rm -sf rethink

redis-up:
	docker-compose up -d --force-recreate redis

redis-down:
	docker-compose rm -sf redis
