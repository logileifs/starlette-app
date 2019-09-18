run:
	uvicorn api.app:app --port=8989 --reload

test:
	python -m unittest discover -s tests -p "*test*.py"

db-up:
	docker-compose up -d --force-recreate rethink
