"""Simple app to add configuration options to a Django project."""
from options.constants import FLOAT, INT, STRING, FILE, TYPE_CHOICES, CONVERTER
from options.helpers import get_option_model, get_user_option_model

default_app_config = "options.apps.ConfigurationsConfig"

__all__ = [
    "get_option_model",
    "get_user_option_model",
    "FLOAT",
    "INT",
    "STRING",
    "FILE",
    "TYPE_CHOICES",
    "CONVERTER",
]
__version__ = "2.0.0"
