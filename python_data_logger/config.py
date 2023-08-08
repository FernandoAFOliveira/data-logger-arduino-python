#config.py
import yaml
import os
from pathlib import Path
from configparser import ConfigParser

INVALID_FILENAME_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
MAX_DIRECTORY_LENGTH = 20  # max length of directory name
MAX_FILENAME_LENGTH = 20    # This does not include the appended timestamp

# Paths
DEFAULTS_PATH = os.path.join("config", "defaults.ini")
LAST_SUCCESSFUL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config', 'last_successful.yaml'))
CURRENT_DIR = Path(__file__).parent
CURRENT_SETTINGS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config', 'current_settings.yaml'))

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
