import unittest
import os
import yaml
from capital_gains.configuration.config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    TEST_CONFIG_FILE = "test_config.yml"

    def setUp(self):
        # Creamos un archivo YAML temporal
        data = {
            'taxes': {
                'sell': {
                    'percentage': 15,
                    'limit_without_taxes': 10000
                }
            }
        }
        with open(self.TEST_CONFIG_FILE, 'w') as f:
            yaml.dump(data, f)

    def tearDown(self):
        # Borramos el archivo al terminar
        if os.path.exists(self.TEST_CONFIG_FILE):
            os.remove(self.TEST_CONFIG_FILE)

    def test_load_valid_config(self):
        loader = ConfigLoader(self.TEST_CONFIG_FILE)

        # CORRECCIÓN 1: Accedemos directamente a .config (no .get_config())
        config = loader.config

        self.assertIsNotNone(config)
        self.assertEqual(config['taxes']['sell']['percentage'], 15)
        self.assertEqual(config['taxes']['sell']['limit_without_taxes'], 10000)

    def test_file_not_found(self):
        # CORRECCIÓN 2: Tu clase captura el error y devuelve None.
        # Así que verificamos que config sea None en lugar de esperar una excepción.
        loader = ConfigLoader("archivo_inexistente_123.yml")

        self.assertIsNone(loader.config)

    def test_invalid_yaml(self):
        # Test extra para cubrir el bloque "except yaml.YAMLError"
        with open("bad.yml", "w") as f:
            f.write("esto: no: es: un: yaml: valido")

        loader = ConfigLoader("bad.yml")
        self.assertIsNone(loader.config)

        if os.path.exists("bad.yml"):
            os.remove("bad.yml")