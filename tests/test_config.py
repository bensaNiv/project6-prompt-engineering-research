"""Tests for the configuration module."""

import os
from unittest.mock import patch

import pytest

from src.config import Config


class TestConfig:
    """Tests for Config class."""

    def test_config_creation_with_values(self) -> None:
        """Test creating Config with explicit values."""
        config = Config(
            api_key="test_key",
            model_name="test-model",
            max_retries=5,
            retry_delay=2.0,
            runs_per_case=5,
        )

        assert config.api_key == "test_key"
        assert config.model_name == "test-model"
        assert config.max_retries == 5
        assert config.retry_delay == 2.0
        assert config.runs_per_case == 5

    def test_config_default_values(self) -> None:
        """Test Config default values."""
        config = Config(api_key="test_key")

        assert config.model_name == "gemini-2.5-flash-lite"
        assert config.max_retries == 5
        assert config.retry_delay == 2.0
        assert config.runs_per_case == 2

    @patch.dict(os.environ, {"GEMINI_API_KEY": "env_test_key"}, clear=True)
    def test_config_from_env(self) -> None:
        """Test loading Config from environment variables."""
        config = Config.from_env()

        assert config.api_key == "env_test_key"
        assert config.model_name == "gemini-2.5-flash-lite"

    @patch.dict(os.environ, {}, clear=True)
    def test_config_from_env_missing_key(self) -> None:
        """Test Config raises error when API key is missing."""
        with pytest.raises(ValueError, match="GEMINI_API_KEY"):
            Config.from_env(env_path="/nonexistent/.env")

    @patch.dict(
        os.environ,
        {
            "GEMINI_API_KEY": "test_key",
            "MODEL_NAME": "custom-model",
            "MAX_RETRIES": "10",
            "RETRY_DELAY": "5.0",
            "RUNS_PER_CASE": "7",
        },
    )
    def test_config_from_env_custom_values(self) -> None:
        """Test loading Config with custom environment values."""
        config = Config.from_env()

        assert config.api_key == "test_key"
        assert config.model_name == "custom-model"
        assert config.max_retries == 10
        assert config.retry_delay == 5.0
        assert config.runs_per_case == 7
