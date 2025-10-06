import json
import os
from typing import Dict, Any

class Config:
    """Manages application settings, loading from and saving to a JSON file."""

    def __init__(self, config_path: str):
        self.config_path = config_path
        # Default settings are loaded first
        self.settings = self._get_default_settings()
        # Then, we try to load settings from the file, which might override defaults
        self.load_settings()

    def _get_default_settings(self) -> Dict[str, Any]:
        """Returns the default settings structure."""
        return {
            # No default settings for now in the simplified version
        }

    def load_settings(self) -> None:
        """
        Loads settings from the JSON file. If the file doesn't exist,
        it saves a new one with default values. If it's corrupted,
        it also falls back to defaults.
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_settings = json.load(f)
                # Merge user settings with defaults to ensure all keys are present
                self.settings.update(user_settings)
            except (json.JSONDecodeError, FileNotFoundError):
                # If file is corrupted or not found, create a new one with defaults
                self.save_settings()
        else:
            self.save_settings() # Create the file if it doesn't exist

    def save_settings(self) -> None:
        """Saves the current settings to the JSON file."""
        # Ensure the directory exists before writing
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        """Gets a setting value by key."""
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Sets a setting value and immediately saves it."""
        self.settings[key] = value
        self.save_settings()