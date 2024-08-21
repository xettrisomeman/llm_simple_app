from typing import Dict, Any
import yaml
from yaml.loader import SafeLoader


YAML_FILE = "components/app_interface/config.yaml"

config: Dict[str, Any]

with open(YAML_FILE) as file:
    config = yaml.load(file, Loader=SafeLoader)

