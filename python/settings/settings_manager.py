#settings_manager.py
import yaml
from config.constants import DEFAULTS_PATH, LAST_SUCCESSFUL_PATH, CURRENT_SETTINGS_PATH
from pathlib import Path
from configparser import ConfigParser

# Load functions
def load_defaults():
    """
    Load default settings from the defaults.ini file.

    Returns:
    dict: A dictionary containing the default settings.
    """
    parser = ConfigParser()
    parser.read(DEFAULTS_PATH)
    return {section: dict(parser[section]) for section in parser.sections()}

def load_last_successful():
    """
    Load the last successful settings from the last_successful.yaml file.

    Returns:
    dict: A dictionary containing the last successful settings.
    """
    with open(LAST_SUCCESSFUL_PATH, 'r') as file:
        return yaml.safe_load(file)

def load_current_settings():
    """
    Load the current settings from the current_settings.yaml file.

    Returns:
    dict: A dictionary containing the current settings.
    """
    with open(CURRENT_SETTINGS_PATH, 'r') as file:
        return yaml.safe_load(file)

# Save functions
def save_last_successful(settings):
    """
    Save the last successful settings to the last_successful.yaml file.

    Args:
    settings (dict): A dictionary containing the last successful settings.
    """
    with open(LAST_SUCCESSFUL_PATH, "w") as file:
        yaml.safe_dump(settings, file, indent=4)

def save_current_settings(settings):
    """
    Save the current settings to the current_settings.yaml file.

    Args:
    settings (dict): A dictionary containing the current settings.
    """
    with open(CURRENT_SETTINGS_PATH, 'w') as file:
        yaml.safe_dump(settings, file, indent=4)

print(os.path.abspath(CURRENT_SETTINGS_PATH))
