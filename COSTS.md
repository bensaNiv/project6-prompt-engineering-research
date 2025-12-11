# Cost Analysis

## Overview

This project uses **Ollama** with locally-hosted models, which means **zero API costs** for the actual experiments. All LLM inference runs on local hardware.

## Cost Breakdown

### API/Service Costs

| Service | Usage | Cost per Unit | Total Cost |
|---------|-------|---------------|------------|
| Ollama (local) | 1000+ API calls | $0.00 | **$0.00** |
| Gemini API | Not used | N/A | $0.00 |
| OpenAI API | Not used | N/A | $0.00 |

### Hardware Costs (Existing Equipment)

| Resource | Description | Estimated Value |
|----------|-------------|-----------------|
| GPU | Local GPU for inference | (existing hardware) |
| CPU | For Ollama serving | (existing hardware) |
| Storage | Model weights (~5GB) | (existing storage) |

### Development Time

| Activity | Estimated Hours |
|----------|-----------------|
| Dataset creation | 4-6 hours |
| Baseline implementation | 2-3 hours |
| Prompt techniques | 4-6 hours |
| Running experiments | 8-12 hours (mostly automated) |
| Analysis & visualization | 3-4 hours |
| Documentation | 2-3 hours |
| **Total** | **23-34 hours** |

## Model Selection Rationale

### Chosen Model: `llama3.2:3b`

**Why this model:**
- Fast inference (~3-5 seconds per query)
- Good balance of quality vs speed
- Fits in consumer GPU memory
- Open source, no API costs

**Alternatives considered:**
- `llama3.2:1b` - Too small, lower quality
- `llama3.1:8b` - Better quality but slower (~10-15s per query)
- `mistral:7b` - Good alternative, similar performance

## Cost Optimization Strategies

### 1. Local Model Hosting
Running Ollama locally eliminates all API costs, making it possible to run 1000+ queries for the experiment without budget concerns.

### 2. Batch Processing
Running experiments in batches with configurable delays to avoid overloading the local server.

### 3. Result Caching
Results are saved to CSV files, allowing re-analysis without re-running expensive LLM calls.

### 4. Selective Re-runs
Manual override system allows correcting individual results without re-running entire experiments.

## Budget Summary

| Category | Planned | Actual |
|----------|---------|--------|
| API Costs | $0 | $0 |
| Cloud Compute | $0 | $0 |
| Total | **$0** | **$0** |

## Notes

- This project was designed to be cost-free by using local inference
- For production deployment, consider API costs if switching to cloud-hosted models
- Estimated cloud API cost for equivalent 1000 queries: ~$5-10 (GPT-3.5) or ~$30-50 (GPT-4)
