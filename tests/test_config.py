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
            model_name="test-model",
            ollama_host="http://test:11434",
            max_retries=5,
            retry_delay=2.0,
            runs_per_case=5,
        )

        assert config.model_name == "test-model"
        assert config.ollama_host == "http://test:11434"
        assert config.max_retries == 5
        assert config.retry_delay == 2.0
        assert config.runs_per_case == 5

    def test_config_default_values(self) -> None:
        """Test Config default values."""
        config = Config()

        assert config.model_name == "llama3.2:3b"
        assert config.ollama_host == "http://localhost:11434"
        assert config.max_retries == 5
        assert config.retry_delay == 2.0
        assert config.runs_per_case == 2

    @patch.dict(os.environ, {}, clear=True)
    def test_config_from_env_defaults(self) -> None:
        """Test loading Config from environment with defaults."""
        config = Config.from_env()

        assert config.model_name == "llama3.2:3b"
        assert config.ollama_host == "http://localhost:11434"

    @patch.dict(
        os.environ,
        {
            "MODEL_NAME": "custom-model",
            "OLLAMA_HOST": "http://custom:11434",
            "MAX_RETRIES": "10",
            "RETRY_DELAY": "5.0",
            "RUNS_PER_CASE": "7",
        },
    )
    def test_config_from_env_custom_values(self) -> None:
        """Test loading Config with custom environment values."""
        config = Config.from_env()

        assert config.model_name == "custom-model"
        assert config.ollama_host == "http://custom:11434"
        assert config.max_retries == 10
        assert config.retry_delay == 5.0
        assert config.runs_per_case == 7
