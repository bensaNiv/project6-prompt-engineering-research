"""Configuration module for loading environment variables and settings."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    """
    Configuration settings for the prompt engineering research project.

    Attributes
    ----------
    model_name : str
        Name of the Ollama model to use.
    ollama_host : str
        URL of the Ollama server.
    max_retries : int
        Maximum number of retry attempts for API calls.
    retry_delay : float
        Delay in seconds between retry attempts.
    runs_per_case : int
        Number of times to run each test case for consistency measurement.
    request_delay : float
        Delay between each API request to avoid rate limits.
    rate_limit_backoff : float
        Initial wait time on rate limit error.
    max_backoff : float
        Maximum wait time for rate limit backoff.
    """

    model_name: str = "llama3.2:3b"
    ollama_host: str = "http://localhost:11434"
    max_retries: int = 5
    retry_delay: float = 2.0
    runs_per_case: int = 2
    request_delay: float = 1.5
    rate_limit_backoff: float = 15.0
    max_backoff: float = 120.0

    @classmethod
    def from_env(cls, env_path: str | None = None) -> "Config":
        """
        Load configuration from environment variables.

        Parameters
        ----------
        env_path : str, optional
            Path to .env file. If None, uses default .env location.

        Returns
        -------
        Config
            Configuration instance with loaded values.
        """
        load_dotenv(env_path)

        return cls(
            model_name=os.getenv("MODEL_NAME", "llama3.2:3b"),
            ollama_host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            max_retries=int(os.getenv("MAX_RETRIES", "5")),
            retry_delay=float(os.getenv("RETRY_DELAY", "2.0")),
            runs_per_case=int(os.getenv("RUNS_PER_CASE", "2")),
            request_delay=float(os.getenv("REQUEST_DELAY", "1.5")),
            rate_limit_backoff=float(os.getenv("RATE_LIMIT_BACKOFF", "15.0")),
            max_backoff=float(os.getenv("MAX_BACKOFF", "120.0")),
        )
