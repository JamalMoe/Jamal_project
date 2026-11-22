
import pytest
import yaml

from Jamal_project import config


def test_load_config_success(mocker, tmp_path):
    config_file = tmp_path / "config.yaml"

    config_file.write_text(
        """
scanner:
  default_threads: 100
  timeout: 0.5
""",
        encoding="utf-8"
    )

    mocker.patch.object(
        config,
        "CONFIG_FILE",
        config_file
    )

    result = config.load_config()

    assert result["scanner"]["default_threads"] == 100
    assert result["scanner"]["timeout"] == 0.5


def test_load_config_missing_file(mocker, tmp_path):
    missing_file = tmp_path / "missing.yaml"

    mocker.patch.object(
        config,
        "CONFIG_FILE",
        missing_file
    )

    with pytest.raises(FileNotFoundError):
        config.load_config()


def test_load_config_invalid_structure(mocker, tmp_path):
    config_file = tmp_path / "config.yaml"

    config_file.write_text(
        "- invalid\n- structure",
        encoding="utf-8"
    )

    mocker.patch.object(
        config,
        "CONFIG_FILE",
        config_file
    )

    with pytest.raises(ValueError, match="YAML mapping"):
        config.load_config()


def test_load_config_empty_file(mocker, tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("", encoding="utf-8")

    mocker.patch.object(
        config,
        "CONFIG_FILE",
        config_file
    )

    with pytest.raises(ValueError, match="YAML mapping"):
        config.load_config()


def test_load_config_malformed_yaml(mocker, tmp_path):
    config_file = tmp_path / "config.yaml"

    config_file.write_text(
        "scanner:\n  default_threads: [100",
        encoding="utf-8"
    )

    mocker.patch.object(
        config,
        "CONFIG_FILE",
        config_file
    )

    with pytest.raises(yaml.YAMLError):
        config.load_config()
