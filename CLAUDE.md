# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Python SDK for the Alternatives.PE API that provides access to both the original company/investor endpoints and the new VentureCap API endpoints. The SDK handles OAuth2 authentication automatically and provides type-safe access to financial data for companies, investors, funds, and capital providers.

## Project Structure

- `altpe_sdk/` - Main SDK module
  - `client.py` - Main AlternativesPE client class with all API methods
  - `models.py` - Pydantic models for API responses
  - `enums.py` - Enumerations for API parameters (categories, order directions, etc.)
  - `config.py` - Configuration management
  - `http_client.py` - HTTP client wrapper with authentication
  - `exceptions.py` - Custom exceptions
  - `mappings.py` - Static mappings for sectors, themes, locations, fund types
- `tests/` - Test suite with pytest fixtures
- `examples/` - Usage examples including VentureCap API examples

## Development Commands

### Installation and Setup

```bash
# Install dependencies
poetry install

# Install with dev dependencies (default)
poetry install --with dev
```

### Testing

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_client.py

# Run with coverage
poetry run pytest --cov=altpe_sdk

# Run live integration tests (requires API credentials)
python live_tests.py
```

### Code Quality

```bash
# Format code with Black
poetry run black .

# Lint with Ruff
poetry run ruff check .

# Fix linting issues automatically
poetry run ruff check . --fix
```

### Examples and Development

```bash
# Run the main example
python example.py

# Run VentureCap specific example
python examples/venturecap_example.py

# Launch Jupyter for dev notebook
poetry run jupyter lab dev.ipynb
```

## Architecture

The SDK is built around a single `AlternativesPE` client class that provides async methods for all API endpoints. Key architectural components:

### Authentication

- Automatic OAuth2 token management via `HTTPClient`
- Credentials via constructor parameters or environment variables (`ALTPE_CLIENT_ID`, `ALTPE_CLIENT_SECRET`)

### API Coverage

- **Original API**: Companies, investors, directors, founders, auditors
- **VentureCap API**: Capital providers (fund managers, LPs), funds, fund performances, commitment deals, people

### Response Models

- All responses are typed using Pydantic models
- Base model (`BaseApiModel`) provides consistent configuration
- List responses include pagination metadata (`total_records`, `offset`, `limit`)

### Error Handling

- Custom exceptions in `exceptions.py`: `AuthenticationError`, `NotFoundError`, `RateLimitError`, `ValidationError`
- HTTP client handles retries and rate limiting

### Enums and Type Safety

- Comprehensive enums for all API parameters (categories, statuses, order directions)
- Static mappings for human-readable names of sectors, themes, locations

## Testing Configuration

Tests use pytest with async support and fixtures defined in `conftest.py`:

- `config()` - Test configuration from environment
- `client()` - Authenticated test client
- Sample IDs for various entity types

Environment variables required for testing:

- `ALTERNATIVES_PE_CLIENT_ID`
- `ALTERNATIVES_PE_CLIENT_SECRET`

## Key Development Patterns

- All API methods are async and use the `HTTPClient` wrapper
- Pydantic models handle response parsing and validation
- Enums provide type safety for API parameters
- Context manager support for proper resource cleanup (`async with AlternativesPE()`)
- Pagination support on all list endpoints with `limit` and `offset` parameters
