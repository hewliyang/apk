"""Configuration for the Alternatives.PE SDK."""

from pydantic import Field
from pydantic_settings import BaseSettings


class AltPEConfig(BaseSettings):
    """Configuration for Alternatives.PE SDK."""

    base_url: str = Field(default="https://api.alternatives.pe")
    client_id: str | None = Field(default=None, alias="ALTERNATIVES_PE_CLIENT_ID")
    client_secret: str | None = Field(
        default=None, alias="ALTERNATIVES_PE_CLIENT_SECRET"
    )
    timeout: float = Field(default=30.0)
    max_retries: int = Field(default=3)

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "allow",
    }
