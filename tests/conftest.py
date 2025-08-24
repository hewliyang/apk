"""Test configuration."""

import os
from collections.abc import Generator

import pytest
from dotenv import load_dotenv

from altpe_sdk import AlternativesPE
from altpe_sdk.config import AltPEConfig

# Load environment variables
load_dotenv()


@pytest.fixture
def config() -> AltPEConfig:
    """Get test configuration."""
    return AltPEConfig(
        client_id=os.getenv("ALTERNATIVES_PE_CLIENT_ID"),
        client_secret=os.getenv("ALTERNATIVES_PE_CLIENT_SECRET"),
    )


@pytest.fixture
async def client(config: AltPEConfig) -> Generator[AlternativesPE, None, None]:
    """Get test client."""
    async with AlternativesPE(
        client_id=config.client_id,
        client_secret=config.client_secret,
    ) as altpe_client:
        yield altpe_client


@pytest.fixture
def sample_company_id() -> str:
    """Sample company ID for testing."""
    return "2"  # Based on the OpenAPI spec example


@pytest.fixture
def sample_company_uen() -> str:
    """Sample company UEN for testing."""
    return "201935876D"  # Based on the OpenAPI spec example


@pytest.fixture
def sample_investor_id() -> str:
    """Sample investor ID for testing."""
    return "4"  # Based on the OpenAPI spec example


@pytest.fixture
def sample_director_id() -> str:
    """Sample director ID for testing."""
    return "4"  # Based on the OpenAPI spec example


@pytest.fixture
def sample_founder_id() -> str:
    """Sample founder ID for testing."""
    return "2"  # Based on the OpenAPI spec example


@pytest.fixture
def sample_auditor_id() -> str:
    """Sample auditor ID for testing."""
    return "2"  # Based on the OpenAPI spec example
