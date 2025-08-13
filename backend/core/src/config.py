import os
import yaml

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../config.yaml")
with open(path, "r") as f:
    CONFIG = yaml.safe_load(f)
