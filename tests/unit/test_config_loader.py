import unittest
import os
import yaml
from capital_gains.configuration.config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    TEST_CONFIG_FILE = "test_config.yml"

    def setUp(self):
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
        if os.path.exists(self.TEST_CONFIG_FILE):
            os.remove(self.TEST_CONFIG_FILE)

    def test_load_valid_config(self):
        loader = ConfigLoader(self.TEST_CONFIG_FILE)

        config = loader.config

        self.assertIsNotNone(config)
        self.assertEqual(config['taxes']['sell']['percentage'], 15)
        self.assertEqual(config['taxes']['sell']['limit_without_taxes'], 10000)

    def test_file_not_found(self):
        loader = ConfigLoader("archivo_inexistente_123.yml")

        self.assertIsNone(loader.config)

    def test_invalid_yaml(self):
        with open("bad.yml", "w") as f:
            f.write("esto: no: es: un: yaml: valido")

        loader = ConfigLoader("bad.yml")
        self.assertIsNone(loader.config)

        if os.path.exists("bad.yml"):
            os.remove("bad.yml")