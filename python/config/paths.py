# Paths
from pathlib import Path

# Base directories
PROJECT_ROOT_DIR = Path(__file__).parent.parent
PYTHON_DIR = PROJECT_ROOT_DIR / "python"
SETTINGS_DIR = PYTHON_DIR / "settings"
LOG_DIR = PYTHON_DIR / "system_logs"
SRC_DIR = PYTHON_DIR / "src"
CONFIG_DIR = PYTHON_DIR / "config"

# Settings paths
DEFAULTS_PATH = SETTINGS_DIR / "defaults.ini"
LAST_SUCCESSFUL_PATH = SETTINGS_DIR / "last_successful.yaml"
CURRENT_SETTINGS_PATH = SETTINGS_DIR / "current_settings.yaml"