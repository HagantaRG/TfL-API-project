"""
This module provides access to settings stored in configuration files within
this directory.
"""

# Import from standard libraries
from pathlib import Path
from typing import Final

# Import from private libraries
from toml_reader import Toml
from db_client import DBClient


# Define constants
DIR: Final[Path] = Path(__file__).parent
"""The path to this directory."""
ROOT_DIR: Final[Path] = DIR.parent
"""The path to the root directory of the project."""
SETTINGS_PATH: Final[Path] = DIR / "settings.toml"
"""The path to the settings.toml file."""

# Define TOML settings object
SETTINGS: Toml = Toml(SETTINGS_PATH)

# Define clients
DEFAULT_DB_CLIENT: Final[DBClient] = DBClient(
    password=SETTINGS.load("DB_Settings.DB_Password"),
    dbname=SETTINGS.load("DB_Settings.DB_Name"),
    hostname=SETTINGS.load("DB_Settings.DB_Host"),
    port=SETTINGS.load("DB_Settings.DB_Port"),
    user=SETTINGS.load("DB_Settings.DB_User"),
)