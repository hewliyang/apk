# Alternatives.PE SDK

Python SDK for the Alternatives.PE API, supporting both the original company/investor endpoints and the new VentureCap API endpoints.

## Installation

```bash
pip install altpe-sdk
```

## Quick Start

```python
import asyncio
from altpe_sdk import AlternativesPE
from altpe_sdk.enums import CapitalProviderCategory, OrderDirection

async def main():
    # Initialize client
    client = AlternativesPE(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    # Original API - Get companies
    companies = await client.get_companies(limit=10)
    print(f"Found {companies.data.total_records} companies")

    # VentureCap API - Get capital providers (fund managers)
    fund_managers = await client.get_capital_providers(
        category=CapitalProviderCategory.FUND_MANAGER,
        limit=10,
        order_direction=OrderDirection.DESC
    )
    print(f"Found {fund_managers.totalRecords} fund managers")

    # Get funds from 2020 onwards
    recent_funds = await client.get_funds(
        vintage_year_min=2020,
        limit=10
    )
    print(f"Found {recent_funds.total_records} recent funds")

    await client.close()

asyncio.run(main())
```

## API Coverage

### Original Alternatives.PE API

- **Companies**: Search, get by ID/UEN, financials
- **Investors**: Search, get by ID
- **Directors**: Search, get by ID
- **Founders**: Search, get by ID
- **Auditors**: Search, get by ID

### VentureCap API (New)

- **Capital Providers**: Fund managers, limited partners, family offices
- **Funds**: Fund information, performance metrics, vintage years
- **Fund Performances**: IRR, DPI, RVPI, net multiples, reporting periods
- **Commitment Deals**: LP-fund relationships, deal dates, fund types
- **People**: Team members, job titles, contact information

## VentureCap API Examples

### Capital Providers

```python
# Get fund managers
fund_managers = await client.get_capital_providers(
    category=CapitalProviderCategory.FUND_MANAGER,
    hq=40,  # Country ID for Singapore
    limit=50
)

# Get specific capital provider
provider = await client.get_capital_provider_by_id(
    1234,
    category=CapitalProviderCategory.FUND_MANAGER
)
```

### Funds

```python
# Get funds by vintage year and size
funds = await client.get_funds(
    vintage_year_min=2020,
    vintage_year_max=2024,
    size_min=100_000_000,  # $100M+
    status="Open",
    limit=25
)

# Get specific fund
fund = await client.get_fund_by_id(1234)
```

### Fund Performances

```python
# Get high-performing funds
high_performers = await client.get_fund_performances(
    irr_min=15.0,  # 15%+ IRR
    net_multiple_min=2.0,  # 2x+ net multiple
    order_by="irr",
    order_direction=OrderDirection.DESC,
    limit=20
)

# Get performance for specific fund
performance = await client.get_fund_performance_by_id(1234)
```

### Commitment Deals

```python
# Get recent commitment deals
deals = await client.get_commitment_deals(
    fund_type=10,  # Specific fund type ID
    limit=30
)

# Get specific deal
deal = await client.get_commitment_deal_by_id(1234)
```

### People

```python
# Search for people
people = await client.get_people(
    first_name="John",
    order_by=PersonOrderBy.LAST_NAME,
    limit=25
)

# Get specific person
person = await client.get_person_by_id(1234)
```

## Authentication

The SDK handles OAuth2 authentication automatically. You just need to provide your client credentials:

```python
# Via constructor
client = AlternativesPE(client_id="...", client_secret="...")

# Via environment variables
# ALTPE_CLIENT_ID=your_client_id
# ALTPE_CLIENT_SECRET=your_client_secret
client = AlternativesPE()
```

## Error Handling

```python
from altpe_sdk.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError
)

try:
    fund = await client.get_fund_by_id(999999)
except NotFoundError:
    print("Fund not found")
except AuthenticationError:
    print("Invalid credentials")
except RateLimitError:
    print("Rate limit exceeded")
```

## Enums and Constants

The SDK provides enums for better type safety:

```python
from altpe_sdk.enums import (
    CapitalProviderCategory,
    FundStatus,
    OrderDirection,
    PersonOrderBy,
    FundOrderBy,
    # ... and more
)
```

## Pagination

All list endpoints support pagination:

```python
# First page
page1 = await client.get_capital_providers(limit=100, offset=0)

# Second page
page2 = await client.get_capital_providers(limit=100, offset=100)

print(f"Total records: {page1.totalRecords}")
```

## Development

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run VentureCap endpoint tests specifically
python test_venturecap_runner.py

# Run example
python examples/venturecap_example.py
```

## License

MIT License
