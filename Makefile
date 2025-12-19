.PHONY: install test run clean docker-build docker-run

# Variables
PYTHON = python
IMAGE_NAME = capital-gains

# Instala las dependencias del proyecto
install:
	pip install -r requirements.txt

# Ejecuta todos los tests con detalle
test:
	$(PYTHON) -m pytest tests/ -v

# Ejecuta la aplicación en modo interactivo
run:
	$(PYTHON) -m capital_gains

# Limpia archivos temporales y caché
clean:
	rm -rf .pytest_cache
	rm -rf **/__pycache__
	rm -rf capital_gains/__pycache__
	rm -rf tests/__pycache__
	rm -rf .coverage

# Construye la imagen de Docker
docker-build:
	docker build -t $(IMAGE_NAME) .

# Ejecuta la aplicación dentro de Docker
docker-run:
	@echo "Paste your JSON lines below (Ctrl+D to finish):"
	docker run -i --rm $(IMAGE_NAME)