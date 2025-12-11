# ADR 001: Use Ollama for Local LLM Execution

## Status

Accepted

## Date

2025-12-01

## Context

This research project requires executing hundreds of LLM inference calls to test different prompt engineering techniques. We need to choose between:

1. **Cloud APIs** (OpenAI, Anthropic, Google): Pay-per-use, requires API keys, subject to rate limits
2. **Local LLMs** (Ollama, llama.cpp, vLLM): Free execution, requires local hardware, no rate limits
3. **Hybrid approach**: Use cloud for some tests, local for others

Key considerations:
- **Cost**: Running 1000+ API calls with cloud providers would cost $10-50+
- **Reproducibility**: Cloud models may change over time, affecting reproducibility
- **Rate limits**: Cloud APIs have rate limits that slow experimentation
- **Privacy**: Test data stays local with no external transmission
- **Hardware**: Research team has access to machines with adequate GPU/CPU

## Decision

We chose **Ollama** as the local LLM runtime for this project.

### Reasons

1. **Zero Cost**: All inference is free after initial model download
2. **Simple Setup**: Single binary install, simple `ollama serve` to start
3. **REST API**: Standard HTTP interface compatible with existing HTTP clients
4. **Model Variety**: Access to Llama, Mistral, Gemma, and other open models
5. **Cross-Platform**: Works on Windows, macOS, Linux, and WSL
6. **Reproducibility**: Same model version produces consistent results

### Model Selection

We use `llama3.2:3b` as the default model because:
- Good balance of quality and speed for research purposes
- Small enough to run on modest hardware (8GB RAM)
- Representative of production-capable open models

## Consequences

### Positive

- **Cost eliminated**: $0 for all experiments vs estimated $30-50 with cloud APIs
- **No rate limits**: Can run experiments as fast as hardware allows
- **Full control**: Model version locked, results are reproducible
- **Privacy**: No data leaves local machine

### Negative

- **Hardware dependent**: Results vary by machine (CPU vs GPU, memory)
- **Model quality**: Open models may underperform proprietary ones
- **Setup required**: Users must install Ollama before running experiments

### Mitigation

- Document exact model version in results
- Provide clear installation instructions in README
- Support configurable OLLAMA_HOST for WSL/remote setups

## References

- [Ollama Documentation](https://ollama.ai/)
- [Llama 3.2 Model Card](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/)
