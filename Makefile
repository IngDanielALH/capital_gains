.PHONY: setup test run clean docker-build docker-run sonar

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

SONAR_HOST = http://localhost:9000
SONAR_TOKEN = sqp_bf722cdd342793925e4a2f61ed87dd31fc3550ea
PROJECT_KEY = apital_gains
SRC_DIR = capital_gains

setup:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	@echo "✅ Entorno configurado."

test:
	$(PYTHON) -m pytest tests/ -v

test-coverage:
	@echo "🧪 Ejecutando tests con reporte de cobertura..."
	$(PYTHON) -m pytest --cov=$(SRC_DIR) --cov-report=xml:coverage.xml tests/ -v

run:
	$(PYTHON) -m capital_gains

clean:
	rm -rf __pycache__ **/__pycache__ .pytest_cache .coverage coverage.xml $(VENV)
	@echo "🧹 Limpieza completada."

docker-build:
	docker build -t capital-gains .

docker-run:
	docker run -i --rm capital-gains

sonar: test-coverage
	@echo "🚀 Iniciando escaneo con pysonar..."
	$(VENV)/bin/pysonar \
	  --sonar-host-url=$(SONAR_HOST) \
	  --sonar-token=$(SONAR_TOKEN) \
	  --sonar-project-key=$(PROJECT_KEY)