import yaml
import os


class ConfigLoader:
    """
    Loads configuration from a YAML file.
    """

    def __init__(self, file_path="config.yml"):
        self.file_path = file_path
        self.config = self.load_config()

    def load_config(self):
        """
        Reads and parses the YAML configuration file.

        Raises:
            FileNotFoundError: If the config file does not exist.
            yaml.YAMLError: If the file contains invalid YAML syntax.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Configuration file not found at: {self.file_path}")

        with open(self.file_path, "r") as file:
            return yaml.safe_load(file)