.PHONY: setup test run clean docker-build docker-run sonar

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

setup:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	@echo "✅ Entorno configurado. Usa 'make test' o 'make run' directamente."

test:
	$(PYTHON) -m pytest tests/ -v

run:
	$(PYTHON) -m capital_gains

clean:
	rm -rf __pycache__
	rm -rf **/__pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf $(VENV)

docker-build:
	docker build -t capital-gains .

docker-run:
	docker run -i --rm capital-gains

docker: docker-build docker-run