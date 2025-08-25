"""Sync client for the Alternatives.PE SDK."""

from .config import AltPEConfig
from .enums import (
    CapitalProviderCategory,
    CapitalProviderOrderBy,
    CommitmentDealOrderBy,
    CompanyStatus,
    CompanyType,
    CountryCode,
    FundOrderBy,
    FundPerformanceOrderBy,
    InvestmentStage,
    OrderBy,
    OrderDirection,
    PersonOrderBy,
    ResponseType,
)
from .exceptions import ValidationError
from .http_client import SyncHTTPClient
from .models import (
    AuditorListResponse,
    AuditorResponse,
    CapitalProviderListResponse,
    CapitalProviderResponse,
    CommitmentDealListResponse,
    CommitmentDealResponse,
    CompanyFinancialsResponse,
    CompanyListResponse,
    CompanyResponse,
    DirectorListResponse,
    DirectorResponse,
    FounderListResponse,
    FounderResponse,
    FundListResponse,
    FundPerformanceListResponse,
    FundPerformanceResponse,
    FundResponse,
    InvestorListResponse,
    InvestorResponse,
    PersonListResponse,
    PersonResponse,
)


class AlternativesPE:
    """Sync client for Alternatives.PE API."""

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        config: AltPEConfig | None = None,
    ):
        """Initialize the client."""
        self._http_client = SyncHTTPClient(
            client_id=client_id,
            client_secret=client_secret,
            config=config,
        )

    def close(self):
        """Close the client."""
        self._http_client.close()

    def __enter__(self):
        """Sync context manager entry."""
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Sync context manager exit."""
        self.close()

    # Company methods
    def get_companies(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: OrderBy | None = None,
        order_direction: OrderDirection | None = OrderDirection.ASC,
        query: str | None = None,
        countries: str | list[CountryCode] | None = None,
        sectors: str | list[int] | None = None,
        themes: str | list[int] | None = None,
        investment_stage: InvestmentStage | None = None,
        valuation_min: float | None = None,
        valuation_max: float | None = None,
        total_funding_min: float | None = None,
        total_funding_max: float | None = None,
        revenue_min: float | None = None,
        revenue_max: float | None = None,
        revenue_growth_min: float | None = None,
        revenue_growth_max: float | None = None,
        status: CompanyStatus | None = None,
        female_founder: bool | None = None,
        response_type: ResponseType | None = ResponseType.SIMPLE,
        co_type: CompanyType | None = None,
        iso_code: CountryCode | None = None,
    ) -> CompanyListResponse:
        """Get list of companies."""
        params = {
            "limit": min(limit, 100),
            "offset": offset,
        }

        if order_by:
            params["order_by"] = order_by.value
        if order_direction:
            params["order_direction"] = order_direction.value
        if query:
            params["query"] = query
        if countries:
            if isinstance(countries, list):
                params["countries"] = ", ".join(
                    c.value if isinstance(c, CountryCode) else c for c in countries
                )
            else:
                params["countries"] = countries
        if sectors:
            if isinstance(sectors, list):
                params["sectors"] = ", ".join(str(s) for s in sectors)
            else:
                params["sectors"] = sectors
        if themes:
            if isinstance(themes, list):
                params["themes"] = ", ".join(str(t) for t in themes)
            else:
                params["themes"] = themes
        if investment_stage:
            params["investment_stage"] = investment_stage.value
        if valuation_min is not None:
            params["valuation_min"] = valuation_min
        if valuation_max is not None:
            params["valuation_max"] = valuation_max
        if total_funding_min is not None:
            params["total_funding_min"] = total_funding_min
        if total_funding_max is not None:
            params["total_funding_max"] = total_funding_max
        if revenue_min is not None:
            params["revenue_min"] = revenue_min
        if revenue_max is not None:
            params["revenue_max"] = revenue_max
        if revenue_growth_min is not None:
            params["revenue_growth_min"] = revenue_growth_min
        if revenue_growth_max is not None:
            params["revenue_growth_max"] = revenue_growth_max
        if status:
            params["status"] = status.value
        if female_founder is not None:
            params["female_founder"] = "1" if female_founder else "0"
        if response_type:
            params["response_type"] = response_type.value
        if co_type:
            params["co_type"] = co_type.value
        if iso_code:
            params["iso_code"] = iso_code.value

        response = self._http_client.get("/api/v2/companies", params=params)
        return CompanyListResponse(**response.json())

    def get_company_by_id(self, company_id: str) -> CompanyResponse:
        """Get company by ID."""
        response = self._http_client.get(f"/api/v2/companies/{company_id}")
        return CompanyResponse(**response.json())

    def get_company_by_uen(self, company_uen: str) -> CompanyResponse:
        """Get company by UEN."""
        response = self._http_client.get(f"/api/v2/companies/{company_uen}/uen")
        return CompanyResponse(**response.json())

    def get_company_financials_by_id(
        self, company_id: str
    ) -> CompanyFinancialsResponse:
        """Get company financials by ID."""
        response = self._http_client.get(f"/api/v2/companies/{company_id}/financials")
        return CompanyFinancialsResponse(**response.json())

    def get_company_financials_by_uen(
        self, company_uen: str
    ) -> CompanyFinancialsResponse:
        """Get company financials by UEN."""
        response = self._http_client.get(
            f"/api/v2/companies/{company_uen}/uen/financials"
        )
        return CompanyFinancialsResponse(**response.json())

    # Investor methods
    def get_investors(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: OrderBy | None = None,
        order_direction: OrderDirection | None = OrderDirection.ASC,
        query: str | None = None,
        sectors: int | None = None,
        themes: str | None = None,
        invested_in_stage: InvestmentStage | None = None,
        invested_on_from: str | None = None,
        invested_on_to: str | None = None,
        response_type: ResponseType | None = ResponseType.SIMPLE,
    ) -> InvestorListResponse:
        """Get list of investors."""
        params = {
            "limit": min(limit, 100),
            "offset": offset,
        }

        if order_by:
            params["order_by"] = order_by.value
        if order_direction:
            params["order_direction"] = order_direction.value
        if query:
            params["query"] = query
        if sectors is not None:
            params["sectors"] = sectors
        if themes:
            params["themes"] = themes
        if invested_in_stage:
            params["invested_in_stage"] = invested_in_stage.value
        if invested_on_from:
            params["invested_on_from"] = invested_on_from
        if invested_on_to:
            params["invested_on_to"] = invested_on_to
        if response_type:
            params["response_type"] = response_type.value

        response = self._http_client.get("/api/v2/investors", params=params)
        return InvestorListResponse(**response.json())

    def get_investor_by_id(self, investor_id: str) -> InvestorResponse:
        """Get a specific investor by ID."""
        response = self._http_client.get(f"/api/v2/investors/{investor_id}")
        return InvestorResponse(**response.json())

    # Director methods
    def get_directors(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: OrderBy | None = None,
        order_direction: OrderDirection | None = OrderDirection.ASC,
        query: str | None = None,
    ) -> DirectorListResponse:
        """Get list of directors."""
        params = {
            "limit": min(limit, 100),
            "offset": offset,
        }

        if order_by:
            params["order_by"] = order_by.value
        if order_direction:
            params["order_direction"] = order_direction.value
        if query:
            params["query"] = query

        response = self._http_client.get("/api/v2/directors", params=params)
        return DirectorListResponse(**response.json())

    def get_director_by_id(self, director_id: str) -> DirectorResponse:
        """Get a specific director by ID."""
        response = self._http_client.get(f"/api/v2/directors/{director_id}")
        return DirectorResponse(**response.json())

    # Founder methods
    def get_founders(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: OrderBy | None = None,
        order_direction: OrderDirection | None = OrderDirection.ASC,
        query: str | None = None,
    ) -> FounderListResponse:
        """Get list of founders."""
        params = {
            "limit": min(limit, 100),
            "offset": offset,
        }

        if order_by:
            params["order_by"] = order_by.value
        if order_direction:
            params["order_direction"] = order_direction.value
        if query:
            params["query"] = query

        response = self._http_client.get("/api/v2/founders", params=params)
        return FounderListResponse(**response.json())

    def get_founder_by_id(self, founder_id: str) -> FounderResponse:
        """Get a specific founder by ID."""
        response = self._http_client.get(f"/api/v2/founders/{founder_id}")
        return FounderResponse(**response.json())

    # Auditor methods
    def get_auditors(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: OrderBy | None = None,
        order_direction: OrderDirection | None = OrderDirection.ASC,
        query: str | None = None,
    ) -> AuditorListResponse:
        """Get list of auditors."""
        params = {
            "limit": min(limit, 100),
            "offset": offset,
        }

        if order_by:
            params["order_by"] = order_by.value
        if order_direction:
            params["order_direction"] = order_direction.value
        if query:
            params["query"] = query

        response = self._http_client.get("/api/v2/auditors", params=params)
        return AuditorListResponse(**response.json())

    def get_auditor_by_id(self, auditor_id: str) -> AuditorResponse:
        """Get a specific auditor by ID."""
        response = self._http_client.get(f"/api/v2/auditors/{auditor_id}")
        return AuditorResponse(**response.json())

    # VentureCap API methods
    def get_capital_providers(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: str | CapitalProviderOrderBy = CapitalProviderOrderBy.DISPLAY_NAME,
        order_direction: str | OrderDirection = OrderDirection.ASC,
        query: str | None = None,
        registration_number: str | None = None,
        category: str | CapitalProviderCategory | None = None,
        hq: int | None = None,
        preferred_location: int | None = None,
        preferred_fund_type: int | None = None,
        preferred_sector: int | None = None,
        preferred_theme: int | None = None,
    ) -> CapitalProviderListResponse:
        """Get list of capital providers."""
        params = {
            "limit": min(limit, 100),
            "offset": offset,
            "order_by": order_by.value if hasattr(order_by, "value") else order_by,
            "order_direction": order_direction.value
            if hasattr(order_direction, "value")
            else order_direction,
        }

        if query:
            params["query"] = query
        if registration_number:
            params["registration_number"] = registration_number
        if category:
            params["category"] = (
                category.value if hasattr(category, "value") else category
            )
        if hq is not None:
            params["hq"] = hq
        if preferred_location is not None:
            params["preferred_location"] = preferred_location
        if preferred_fund_type is not None:
            params["preferred_fund_type"] = preferred_fund_type
        if preferred_sector is not None:
            params["preferred_sector"] = preferred_sector
        if preferred_theme is not None:
            params["preferred_theme"] = preferred_theme

        response = self._http_client.get("/api/v2/capital-providers", params=params)
        return CapitalProviderListResponse(**response.json())

    def get_capital_provider_by_id(
        self, capital_provider_id: int, category: str | CapitalProviderCategory
    ) -> CapitalProviderResponse:
        """Get capital provider by ID."""
        params = {
            "category": category.value if hasattr(category, "value") else category
        }
        try:
            response = self._http_client.get(
                f"/api/v2/capital-providers/{capital_provider_id}/", params=params
            )
        except ValidationError:
            # Retry with a safe default category when server rejects the provided one
            params = {"category": "fund-manager"}
            response = self._http_client.get(
                f"/api/v2/capital-providers/{capital_provider_id}/", params=params
            )
        return CapitalProviderResponse(**response.json())

    def get_funds(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: str | FundOrderBy = FundOrderBy.NAME,
        order_direction: str | OrderDirection = OrderDirection.ASC,
        query: str | None = None,
        registration_number: str | None = None,
        vintage_year_min: int | None = None,
        vintage_year_max: int | None = None,
        fund_type: int | None = None,
        size_min: float | None = None,
        size_max: float | None = None,
        net_irr_min: float | None = None,
        net_irr_max: float | None = None,
        net_multiple_min: float | None = None,
        net_multiple_max: float | None = None,
        dpi_min: float | None = None,
        dpi_max: float | None = None,
        rvpi_min: float | None = None,
        rvpi_max: float | None = None,
        last_report_quarter: str | None = None,
        status: str | None = None,
    ) -> FundListResponse:
        """Get funds with filters."""
        params = {
            "limit": min(limit, 100),
            "offset": offset,
            "order_by": order_by.value if hasattr(order_by, "value") else order_by,
            "order_direction": order_direction.value
            if hasattr(order_direction, "value")
            else order_direction,
        }

        if query:
            params["query"] = query
        if registration_number:
            params["registration_number"] = registration_number
        if vintage_year_min is not None:
            params["vintage_year_min"] = vintage_year_min
        if vintage_year_max is not None:
            params["vintage_year_max"] = vintage_year_max
        if fund_type is not None:
            params["fund_type"] = fund_type
        if size_min is not None:
            params["size_min"] = size_min
        if size_max is not None:
            params["size_max"] = size_max
        if net_irr_min is not None:
            params["net_irr_min"] = net_irr_min
        if net_irr_max is not None:
            params["net_irr_max"] = net_irr_max
        if net_multiple_min is not None:
            params["net_multiple_min"] = net_multiple_min
        if net_multiple_max is not None:
            params["net_multiple_max"] = net_multiple_max
        if dpi_min is not None:
            params["dpi_min"] = dpi_min
        if dpi_max is not None:
            params["dpi_max"] = dpi_max
        if rvpi_min is not None:
            params["rvpi_min"] = rvpi_min
        if rvpi_max is not None:
            params["rvpi_max"] = rvpi_max
        if last_report_quarter:
            params["last_report_quarter"] = last_report_quarter
        if status:
            params["status"] = status

        response = self._http_client.get("/api/v2/funds/", params=params)
        return FundListResponse(**response.json())

    def get_fund_by_id(self, fund_id: int) -> FundResponse:
        """Get a specific fund by ID."""
        response = self._http_client.get(f"/api/v2/funds/{fund_id}")
        return FundResponse(**response.json())

    def get_fund_performances(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: str | FundPerformanceOrderBy = FundPerformanceOrderBy.DPI,
        order_direction: str | OrderDirection = OrderDirection.ASC,
        query: str | None = None,
        fund_id: int | None = None,
        reporting_period: str | None = None,
        irr_min: float | None = None,
        irr_max: float | None = None,
        dpi_min: float | None = None,
        dpi_max: float | None = None,
        rvpi_min: float | None = None,
        rvpi_max: float | None = None,
        net_multiple_min: float | None = None,
        net_multiple_max: float | None = None,
        net_assets_min: float | None = None,
        net_assets_max: float | None = None,
    ) -> FundPerformanceListResponse:
        """Get list of fund performances."""
        params = {
            "limit": min(limit, 100),
            "offset": offset,
            "order_by": order_by.value if hasattr(order_by, "value") else order_by,
            "order_direction": order_direction.value
            if hasattr(order_direction, "value")
            else order_direction,
        }

        if query:
            params["query"] = query
        if fund_id is not None:
            params["fund_id"] = fund_id
        if reporting_period:
            params["reporting_period"] = reporting_period
        if irr_min is not None:
            params["irr_min"] = irr_min
        if irr_max is not None:
            params["irr_max"] = irr_max
        if dpi_min is not None:
            params["dpi_min"] = dpi_min
        if dpi_max is not None:
            params["dpi_max"] = dpi_max
        if rvpi_min is not None:
            params["rvpi_min"] = rvpi_min
        if rvpi_max is not None:
            params["rvpi_max"] = rvpi_max
        if net_multiple_min is not None:
            params["net_multiple_min"] = net_multiple_min
        if net_multiple_max is not None:
            params["net_multiple_max"] = net_multiple_max
        if net_assets_min is not None:
            params["net_assets_min"] = net_assets_min
        if net_assets_max is not None:
            params["net_assets_max"] = net_assets_max

        response = self._http_client.get("/api/v2/fund-performances/", params=params)
        return FundPerformanceListResponse(**response.json())

    def get_fund_performance_by_id(
        self, fund_performance_id: int
    ) -> FundPerformanceResponse:
        """Get a specific fund performance by ID."""
        response = self._http_client.get(
            f"/api/v2/fund-performances/{fund_performance_id}"
        )
        return FundPerformanceResponse(**response.json())

    def get_commitment_deals(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: str | CommitmentDealOrderBy = CommitmentDealOrderBy.FUND_MANAGER_NAME,
        order_direction: str | OrderDirection = OrderDirection.ASC,
        query: str | None = None,
        limited_partner_id: int | None = None,
        fund_id: int | None = None,
        fund_type: int | None = None,
    ) -> CommitmentDealListResponse:
        """Get list of commitment deals."""
        params = {
            "limit": min(limit, 100),
            "offset": offset,
            "order_by": order_by.value if hasattr(order_by, "value") else order_by,
            "order_direction": order_direction.value
            if hasattr(order_direction, "value")
            else order_direction,
        }

        if query:
            params["query"] = query
        if limited_partner_id is not None:
            params["limited_partner_id"] = limited_partner_id
        if fund_id is not None:
            params["fund_id"] = fund_id
        if fund_type is not None:
            params["fund_type"] = fund_type

        response = self._http_client.get("/api/v2/commitment-deals/", params=params)
        return CommitmentDealListResponse(**response.json())

    def get_commitment_deal_by_id(self, deal_id: int) -> CommitmentDealResponse:
        """Get a specific commitment deal by ID."""
        response = self._http_client.get(f"/api/v2/commitment-deals/{deal_id}")
        return CommitmentDealResponse(**response.json())

    def get_people(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: str | PersonOrderBy = PersonOrderBy.ID,
        order_direction: str | OrderDirection = OrderDirection.ASC,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ) -> PersonListResponse:
        """Get list of people."""
        params = {
            "limit": min(limit, 100),
            "offset": offset,
            "order_by": order_by.value if hasattr(order_by, "value") else order_by,
            "order_direction": order_direction.value
            if hasattr(order_direction, "value")
            else order_direction,
        }

        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name
        if email:
            params["email"] = email

        headers = {"Accept": "application/json"}
        response = self._http_client.get(
            "/api/v2/people/", params=params, headers=headers
        )
        return PersonListResponse(**response.json())

    def get_person_by_id(self, person_id: int) -> PersonResponse:
        """Get a specific person by ID."""
        response = self._http_client.get(f"/api/v2/people/{person_id}")
        return PersonResponse(**response.json())
