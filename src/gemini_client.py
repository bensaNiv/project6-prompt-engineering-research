"""Gemini API client wrapper with retry logic and latency tracking."""

import time
from dataclasses import dataclass

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

from .config import Config


@dataclass
class APIResponse:
    """
    Response from Gemini API call.

    Attributes
    ----------
    text : str
        The generated text response.
    latency_ms : float
        Time taken for the API call in milliseconds.
    success : bool
        Whether the API call was successful.
    error : str, optional
        Error message if the call failed.
    """

    text: str
    latency_ms: float
    success: bool
    error: str | None = None


class GeminiClient:
    """
    Client for interacting with the Gemini API.

    Parameters
    ----------
    config : Config
        Configuration instance with API key and settings.
    """

    def __init__(self, config: Config) -> None:
        """Initialize the Gemini client with configuration."""
        self.config = config
        genai.configure(api_key=config.api_key)
        self.model = genai.GenerativeModel(config.model_name)

    def query(self, prompt: str) -> APIResponse:
        """
        Send a prompt to Gemini and get a response with rate limiting.

        Parameters
        ----------
        prompt : str
            The prompt to send to the model.

        Returns
        -------
        APIResponse
            Response containing text, latency, and success status.
        """
        last_error = None
        backoff = self.config.rate_limit_backoff

        for attempt in range(self.config.max_retries):
            try:
                start_time = time.perf_counter()
                response = self.model.generate_content(prompt)
                end_time = time.perf_counter()

                latency_ms = (end_time - start_time) * 1000

                # Delay after successful request to avoid hitting rate limits
                time.sleep(self.config.request_delay)

                return APIResponse(
                    text=response.text.strip(),
                    latency_ms=latency_ms,
                    success=True,
                )

            except ResourceExhausted as e:
                last_error = str(e)
                # Exponential backoff for rate limit errors
                wait_time = min(backoff * (2 ** attempt), self.config.max_backoff)
                print(f"  Rate limited (429), waiting {wait_time:.0f}s before retry {attempt + 1}/{self.config.max_retries}...")
                time.sleep(wait_time)

            except Exception as e:
                last_error = str(e)
                if attempt < self.config.max_retries - 1:
                    wait_time = self.config.retry_delay * (attempt + 1)
                    print(f"  Error: {str(e)[:50]}... retrying in {wait_time:.0f}s")
                    time.sleep(wait_time)

        return APIResponse(
            text="",
            latency_ms=0.0,
            success=False,
            error=last_error,
        )
