import yaml


class ConfigLoader:

    def __init__(self, file_path="config.yml"):
        self.file_path = file_path
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.file_path, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print("Error: No se encontró el archivo de configuración.")
            return None
        except yaml.YAMLError as e:
            print(f"Error al leer el archivo YAML: {e}")
            return None
