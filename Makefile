down:
	docker-compose down


format:
	pip install -r requirements/dev-requirements.txt
	black --verbose --config black.toml src
	isort --recursive src


lint:
	pip install -r requirements/dev-requirements.txt
	flake8 src
	PYTHONPATH=src/ pylint src
	mypy src


local:
	docker-compose pull
	docker-compose up --build -d postgresql


test:
	pip install -r requirements/dev-requirements.txt
	pytest -s -vv


up:
	docker-compose pull
	docker-compose up --build -d
