import json
import os

project_directory_path = os.path.dirname(os.path.dirname(__file__))

config_file_path = os.path.join(project_directory_path, "settings/config.json")

try:
    with open(config_file_path) as config_file:
        configs = json.loads(config_file.read())
except Exception as ex:
    raise FileNotFoundError("Improperly configured environment variables.") from ex

DATABASE_URI = configs["DATABASE_URI"]
DREMIO_USERNAME = configs["DREMIO_USERNAME"]
DREMIO_PASSWORD = configs["DREMIO_PASSWORD"]
