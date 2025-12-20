import unittest
import os
import yaml
from capital_gains.configuration.config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    TEST_CONFIG_FILE = "test_config_temp.yml"

    def setUp(self):
        data = {'taxes': {'sell': {'percentage': 15, 'limit_without_taxes': 10000}}}
        with open(self.TEST_CONFIG_FILE, 'w') as f:
            yaml.dump(data, f)

    def tearDown(self):
        if os.path.exists(self.TEST_CONFIG_FILE):
            os.remove(self.TEST_CONFIG_FILE)

    def test_load_valid_config(self):
        loader = ConfigLoader(self.TEST_CONFIG_FILE)
        self.assertEqual(loader.config['taxes']['sell']['percentage'], 15)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            ConfigLoader("archivo_inexistente_123.yml")

    def test_invalid_yaml(self):
        bad_file = "bad.yml"
        with open(bad_file, "w") as f:
            f.write("esto: no: es: un: yaml: valido: {[:")

        with self.assertRaises(yaml.YAMLError):
            ConfigLoader(bad_file)

        if os.path.exists(bad_file):
            os.remove(bad_file)