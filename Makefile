.PHONY: setup run test test-core validate build browser clean

setup:
	python -m pip install -r requirements-dev.txt

run:
	python -m uvicorn services.api.civicshift.main:app --host 127.0.0.1 --port 8000

test-core:
	python -m pytest -m "not browser" --cov=services/api/civicshift --cov-report=term-missing

test: test-core validate

validate:
	python scripts/validate_repository.py

build:
	npm install
	npm run build

browser:
	npm run test:e2e

clean:
	python scripts/clean_generated.py
