# Alternatives.PE SDK

Python SDK for the Alternatives.PE API.

## Installation

```bash
# pip
pip install git+https://github.com/hewliyang/apk.git
# uv
uv add git+https://github.com/hewliyang/apk.git
# poetry
poetry add git+https://github.com/hewliyang/apk.git
```

## Quickstart

Sync client (default):

```python
from altpe_sdk import AlternativesPE

client = AlternativesPE(
    client_id="your_client_id",
    client_secret="your_client_secret",
)

companies = client.get_companies(limit=5)
print(companies.data.total_records)
```

Async client:

```python
import asyncio
from altpe_sdk import AsyncAlternativesPE

async def main():
    client = AsyncAlternativesPE(
        client_id="your_client_id",
        client_secret="your_client_secret",
    )
    companies = await client.get_companies(limit=5)
    print(companies.data.total_records)

asyncio.run(main())
```

That's it. See enums in `altpe_sdk.enums` and models in `altpe_sdk.models` for details.

## License

MIT License
