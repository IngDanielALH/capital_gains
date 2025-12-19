.PHONY: setup test run clean docker-build docker-run sonar

# Configuración del entorno
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# --- COMANDOS PRINCIPALES ---

# 1. SETUP: Crea el entorno virtual E instala dependencias automáticamente
setup:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	@echo "✅ Entorno configurado. Usa 'make test' o 'make run' directamente."

# 2. TEST: Usa explícitamente el Python del venv (no requiere activar)
test:
	$(PYTHON) -m pytest tests/ -v

# 3. RUN: Ejecuta la app usando el venv
run:
	$(PYTHON) -m capital_gains

# --- UTILIDADES ---

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

sonar:
	$(PYTHON) -m pytest --cov=capital_gains --cov-report=xml
	sed -i '' "s|$$(pwd)|/usr/src|g" coverage.xml
	docker run --rm \
		-v "$$(pwd):/usr/src" \
		sonarsource/sonar-scanner-cli \
		-Dsonar.projectKey=capital-gains \
		-Dsonar.sources=. \
		-Dsonar.host.url=http://host.docker.internal:9000 \
		-Dsonar.token=$(token)