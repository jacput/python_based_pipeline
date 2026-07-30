import sys
import json

REQUIRED_KEYS = [
    "source_file_path",
    "source_file_name",
    "logging_file_full_path"
]

def load_config(config_file_path):

    try:
        with open(config_file_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {config_file_path}")
        raise FileNotFoundError(f"Config file not found: {config_file_path}")
    except json.JSONDecodeError:
        print(f"Invalid JSON in config file: {config_file_path}")
        raise json.JSONDecodeError(f"Invalid JSON in config file: {config_file_path}")

    for key in REQUIRED_KEYS:
        if key not in config:
            raise ValueError(f"Missing config value: {key}")
        
    return config
