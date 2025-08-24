"""Enums for the Alternatives.PE SDK."""

from enum import Enum


class InvestmentStage(str, Enum):
    """Investment stage enum."""

    PRE_SEED = "PRE_SEED"
    SEED = "SEED"
    SERIES_A = "SERIES_A"
    SERIES_B = "SERIES_B"
    SERIES_C_AND_BEYOND = "SERIES_C_AND_BEYOND"


class CompanyStatus(str, Enum):
    """Company status enum."""

    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


class ResponseType(str, Enum):
    """Response type enum."""

    SIMPLE = "SIMPLE"
    DETAILED = "DETAILED"


class CompanyType(str, Enum):
    """Company type enum."""

    STARTUP = "startup"
    PRIVATE = "private"


class OrderDirection(str, Enum):
    """Order direction enum."""

    ASC = "asc"
    DESC = "desc"


class OrderBy(str, Enum):
    """Order by options for companies."""

    NAME = "name"
    ID = "id"
    NO_OF_INVESTED_COMPANIES = "no_of_invested_companies"


# Country codes - ISO3
class CountryCode(str, Enum):
    """ISO3 country codes."""

    SGP = "SGP"
    MYS = "MYS"
    IDN = "IDN"
    THA = "THA"
    VNM = "VNM"
    AUS = "AUS"
    PHL = "PHL"
    # Add more as needed - this is a subset from the API spec


# VentureCap API specific enums
class CapitalProviderCategory(str, Enum):
    """Capital Provider category enum."""

    FUND_MANAGER = "fund-manager"
    LIMITED_PARTNER = "limited-partner"
    FAMILY_OFFICE = "family-office"


class FundStatus(str, Enum):
    """Fund status enum."""

    OPEN = "Open"
    OPEN_WITHOUT_FIRST_CLOSE = "Open - Without first close"
    OPEN_WITH_FIRST_CLOSE = "Open - With first close"
    CLOSED = "Closed"
    EVERGREEN = "Evergreen"
    UPCOMING = "Upcoming"


class PersonOrderBy(str, Enum):
    """Order by options for people."""

    ID = "id"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"


class FundOrderBy(str, Enum):
    """Order by options for funds."""

    NAME = "name"


class CapitalProviderOrderBy(str, Enum):
    """Order by options for capital providers."""

    DISPLAY_NAME = "display_name"


class FundPerformanceOrderBy(str, Enum):
    """Order by options for fund performances."""

    DPI = "dpi"
    IRR = "irr"


class CommitmentDealOrderBy(str, Enum):
    """Order by options for commitment deals."""

    FUND_MANAGER_NAME = "fund_manager_name"
