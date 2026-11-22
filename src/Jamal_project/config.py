"""Configuration loader for Jamal Project."""

import yaml
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parents[2] / "config.yaml"


def load_config() -> dict:
    """Load application settings from config.yaml."""

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_FILE}"
        )

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("Configuration file must contain a YAML mapping")

    return config