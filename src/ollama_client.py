"""Ollama API client wrapper with retry logic and latency tracking."""

import time
import requests
from dataclasses import dataclass

from .config import Config


@dataclass
class APIResponse:
    """
    Response from Ollama API call.

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


class OllamaClient:
    """
    Client for interacting with the Ollama API.

    Parameters
    ----------
    config : Config
        Configuration instance with settings.
    host : str
        Ollama host URL. For WSL accessing Windows Ollama, use the Windows host IP.
    """

    def __init__(self, config: Config, host: str | None = None) -> None:
        """Initialize the Ollama client with configuration."""
        self.config = config
        # Default to localhost, but WSL needs Windows host IP
        self.host = host or "http://localhost:11434"
        self.model = config.model_name

    def query(self, prompt: str) -> APIResponse:
        """
        Send a prompt to Ollama and get a response.

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

        for attempt in range(self.config.max_retries):
            try:
                start_time = time.perf_counter()

                response = requests.post(
                    f"{self.host}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                    },
                    timeout=120,  # 2 minute timeout for slower local models
                )

                end_time = time.perf_counter()
                latency_ms = (end_time - start_time) * 1000

                if response.status_code == 200:
                    result = response.json()
                    return APIResponse(
                        text=result.get("response", "").strip(),
                        latency_ms=latency_ms,
                        success=True,
                    )
                else:
                    last_error = f"HTTP {response.status_code}: {response.text}"

            except requests.exceptions.ConnectionError as e:
                last_error = f"Connection error: {str(e)}"
                print(f"  Cannot connect to Ollama at {self.host}")

            except requests.exceptions.Timeout:
                last_error = "Request timed out"
                print(f"  Timeout on attempt {attempt + 1}/{self.config.max_retries}")

            except Exception as e:
                last_error = str(e)

            if attempt < self.config.max_retries - 1:
                wait_time = self.config.retry_delay * (attempt + 1)
                print(f"  Error: {str(last_error)[:50]}... retrying in {wait_time:.0f}s")
                time.sleep(wait_time)

        return APIResponse(
            text="",
            latency_ms=0.0,
            success=False,
            error=last_error,
        )

    def list_models(self) -> list[str]:
        """List available models from Ollama."""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [m["name"] for m in models]
        except Exception:
            pass
        return []
