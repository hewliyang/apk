"""Main client for the Alternatives.PE SDK."""

from typing import Optional, Union

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
from .http_client import HTTPClient
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


class AsyncAlternativesPE:
    """Async client for Alternatives.PE API."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        config: Optional[AltPEConfig] = None,
    ):
        """Initialize the client."""
        self._http_client = HTTPClient(
            client_id=client_id,
            client_secret=client_secret,
            config=config,
        )

    async def close(self):
        """Close the client."""
        await self._http_client.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, _exc_type, _exc_val, _exc_tb):
        """Async context manager exit."""
        await self.close()

    # Company methods
    async def get_companies(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: Optional[OrderBy] = None,
        order_direction: Optional[OrderDirection] = OrderDirection.ASC,
        query: Optional[str] = None,
        countries: Optional[Union[str, list[CountryCode]]] = None,
        sectors: Optional[Union[str, list[int]]] = None,
        themes: Optional[Union[str, list[int]]] = None,
        investment_stage: Optional[InvestmentStage] = None,
        valuation_min: Optional[float] = None,
        valuation_max: Optional[float] = None,
        total_funding_min: Optional[float] = None,
        total_funding_max: Optional[float] = None,
        revenue_min: Optional[float] = None,
        revenue_max: Optional[float] = None,
        revenue_growth_min: Optional[float] = None,
        revenue_growth_max: Optional[float] = None,
        status: Optional[CompanyStatus] = None,
        female_founder: Optional[bool] = None,
        response_type: Optional[ResponseType] = ResponseType.SIMPLE,
        co_type: Optional[CompanyType] = None,
        iso_code: Optional[CountryCode] = None,
    ) -> CompanyListResponse:
        """Get companies with filters."""
        params = {
            "limit": min(limit, 100),  # API max is 100
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
                params["countries"] = ", ".join(c.value for c in countries)
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

        response = await self._http_client.get("/api/v2/companies", params=params)
        return CompanyListResponse(**response.json())

    async def get_company_by_id(self, company_id: str) -> CompanyResponse:
        """Get company by ID."""
        response = await self._http_client.get(f"/api/v2/companies/{company_id}")
        return CompanyResponse(**response.json())

    async def get_company_by_uen(self, company_uen: str) -> CompanyResponse:
        """Get company by UEN."""
        response = await self._http_client.get(f"/api/v2/companies/{company_uen}/uen")
        return CompanyResponse(**response.json())

    async def get_company_financials_by_id(
        self, company_id: str
    ) -> CompanyFinancialsResponse:
        """Get company financials by ID."""
        response = await self._http_client.get(
            f"/api/v2/companies/{company_id}/financials"
        )
        return CompanyFinancialsResponse(**response.json())

    async def get_company_financials_by_uen(
        self, company_uen: str
    ) -> CompanyFinancialsResponse:
        """Get company financials by UEN."""
        response = await self._http_client.get(
            f"/api/v2/companies/{company_uen}/uen/financials"
        )
        return CompanyFinancialsResponse(**response.json())

    # Investor methods
    async def get_investors(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: Optional[OrderBy] = None,
        order_direction: Optional[OrderDirection] = OrderDirection.ASC,
        query: Optional[str] = None,
        sectors: Optional[int] = None,
        themes: Optional[str] = None,
        invested_in_stage: Optional[InvestmentStage] = None,
        invested_on_from: Optional[str] = None,
        invested_on_to: Optional[str] = None,
        response_type: Optional[ResponseType] = ResponseType.SIMPLE,
    ) -> InvestorListResponse:
        """Get investors with filters."""
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

        response = await self._http_client.get("/api/v2/investors", params=params)
        return InvestorListResponse(**response.json())

    async def get_investor_by_id(self, investor_id: str) -> InvestorResponse:
        """Get investor by ID."""
        response = await self._http_client.get(f"/api/v2/investors/{investor_id}")
        return InvestorResponse(**response.json())

    # Director methods
    async def get_directors(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: Optional[OrderBy] = None,
        order_direction: Optional[OrderDirection] = OrderDirection.ASC,
        query: Optional[str] = None,
    ) -> DirectorListResponse:
        """Get directors with filters."""
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

        response = await self._http_client.get("/api/v2/directors", params=params)
        return DirectorListResponse(**response.json())

    async def get_director_by_id(self, director_id: str) -> DirectorResponse:
        """Get director by ID."""
        response = await self._http_client.get(f"/api/v2/directors/{director_id}")
        return DirectorResponse(**response.json())

    # Founder methods
    async def get_founders(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: Optional[OrderBy] = None,
        order_direction: Optional[OrderDirection] = OrderDirection.ASC,
        query: Optional[str] = None,
    ) -> FounderListResponse:
        """Get founders with filters."""
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

        response = await self._http_client.get("/api/v2/founders", params=params)
        return FounderListResponse(**response.json())

    async def get_founder_by_id(self, founder_id: str) -> FounderResponse:
        """Get founder by ID."""
        response = await self._http_client.get(f"/api/v2/founders/{founder_id}")
        return FounderResponse(**response.json())

    # Auditor methods
    async def get_auditors(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: Optional[OrderBy] = None,
        order_direction: Optional[OrderDirection] = OrderDirection.ASC,
        query: Optional[str] = None,
    ) -> AuditorListResponse:
        """Get auditors with filters."""
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

        response = await self._http_client.get("/api/v2/auditors", params=params)
        return AuditorListResponse(**response.json())

    async def get_auditor_by_id(self, auditor_id: str) -> AuditorResponse:
        """Get auditor by ID."""
        response = await self._http_client.get(f"/api/v2/auditors/{auditor_id}")
        return AuditorResponse(**response.json())

    # VentureCap API methods
    # Capital Provider methods
    async def get_capital_providers(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: Union[
            str, CapitalProviderOrderBy
        ] = CapitalProviderOrderBy.DISPLAY_NAME,
        order_direction: Union[str, OrderDirection] = OrderDirection.ASC,
        query: Optional[str] = None,
        registration_number: Optional[str] = None,
        category: Optional[Union[str, CapitalProviderCategory]] = None,
        hq: Optional[int] = None,
        preferred_location: Optional[int] = None,
        preferred_fund_type: Optional[int] = None,
        preferred_sector: Optional[int] = None,
        preferred_theme: Optional[int] = None,
    ) -> CapitalProviderListResponse:
        """Get capital providers with filters."""
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

        response = await self._http_client.get(
            "/api/v2/capital-providers", params=params
        )
        return CapitalProviderListResponse(**response.json())

    async def get_capital_provider_by_id(
        self, capital_provider_id: int, category: Union[str, CapitalProviderCategory]
    ) -> CapitalProviderResponse:
        """Get capital provider by ID."""
        params = {
            "category": category.value if hasattr(category, "value") else category
        }
        response = await self._http_client.get(
            f"/api/v2/capital-providers/{capital_provider_id}/", params=params
        )
        return CapitalProviderResponse(**response.json())

    # Fund methods
    async def get_funds(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: Union[str, FundOrderBy] = FundOrderBy.NAME,
        order_direction: Union[str, OrderDirection] = OrderDirection.ASC,
        query: Optional[str] = None,
        registration_number: Optional[str] = None,
        vintage_year_min: Optional[int] = None,
        vintage_year_max: Optional[int] = None,
        fund_type: Optional[int] = None,
        size_min: Optional[float] = None,
        size_max: Optional[float] = None,
        net_irr_min: Optional[float] = None,
        net_irr_max: Optional[float] = None,
        net_multiple_min: Optional[float] = None,
        net_multiple_max: Optional[float] = None,
        dpi_min: Optional[float] = None,
        dpi_max: Optional[float] = None,
        rvpi_min: Optional[float] = None,
        rvpi_max: Optional[float] = None,
        last_report_quarter: Optional[str] = None,
        status: Optional[str] = None,
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

        response = await self._http_client.get("/api/v2/funds/", params=params)
        return FundListResponse(**response.json())

    async def get_fund_by_id(self, fund_id: int) -> FundResponse:
        """Get fund by ID."""
        response = await self._http_client.get(f"/api/v2/funds/{fund_id}")
        return FundResponse(**response.json())

    # Fund Performance methods
    async def get_fund_performances(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: Union[str, FundPerformanceOrderBy] = FundPerformanceOrderBy.DPI,
        order_direction: Union[str, OrderDirection] = OrderDirection.ASC,
        query: Optional[str] = None,
        fund_id: Optional[int] = None,
        reporting_period: Optional[str] = None,
        irr_min: Optional[float] = None,
        irr_max: Optional[float] = None,
        dpi_min: Optional[float] = None,
        dpi_max: Optional[float] = None,
        rvpi_min: Optional[float] = None,
        rvpi_max: Optional[float] = None,
        net_multiple_min: Optional[float] = None,
        net_multiple_max: Optional[float] = None,
        net_assets_min: Optional[float] = None,
        net_assets_max: Optional[float] = None,
    ) -> FundPerformanceListResponse:
        """Get fund performances with filters."""
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

        response = await self._http_client.get(
            "/api/v2/fund-performances/", params=params
        )
        return FundPerformanceListResponse(**response.json())

    async def get_fund_performance_by_id(
        self, fund_performance_id: int
    ) -> FundPerformanceResponse:
        """Get fund performance by ID."""
        response = await self._http_client.get(
            f"/api/v2/fund-performances/{fund_performance_id}"
        )
        return FundPerformanceResponse(**response.json())

    # Commitment Deal methods
    async def get_commitment_deals(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: Union[
            str, CommitmentDealOrderBy
        ] = CommitmentDealOrderBy.FUND_MANAGER_NAME,
        order_direction: Union[str, OrderDirection] = OrderDirection.ASC,
        query: Optional[str] = None,
        limited_partner_id: Optional[int] = None,
        fund_id: Optional[int] = None,
        fund_type: Optional[int] = None,
    ) -> CommitmentDealListResponse:
        """Get commitment deals with filters."""
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

        response = await self._http_client.get(
            "/api/v2/commitment-deals/", params=params
        )
        return CommitmentDealListResponse(**response.json())

    async def get_commitment_deal_by_id(self, deal_id: int) -> CommitmentDealResponse:
        """Get commitment deal by ID."""
        response = await self._http_client.get(f"/api/v2/commitment-deals/{deal_id}")
        return CommitmentDealResponse(**response.json())

    # People methods
    async def get_people(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: Union[str, PersonOrderBy] = PersonOrderBy.ID,
        order_direction: Union[str, OrderDirection] = OrderDirection.ASC,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> PersonListResponse:
        """Get people with filters."""
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
        response = await self._http_client.get(
            "/api/v2/people/", params=params, headers=headers
        )
        return PersonListResponse(**response.json())

    async def get_person_by_id(self, person_id: int) -> PersonResponse:
        """Get person by ID."""
        response = await self._http_client.get(f"/api/v2/people/{person_id}")
        return PersonResponse(**response.json())
