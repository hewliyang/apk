"""Pydantic models for the Alternatives.PE API."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BaseApiModel(BaseModel):
    """Base model for all API responses."""

    model_config = ConfigDict(extra="ignore", validate_assignment=True)


class Sector(BaseApiModel):
    """Sector model."""

    id: int
    name: str


class Theme(BaseApiModel):
    """Theme model."""

    id: int
    name: str


class Founder(BaseApiModel):
    """Founder model."""

    id: int
    name: str
    linkedin_url: str | None = None
    email: str | None = None
    hashed_name: str | None = None


class Director(BaseApiModel):
    """Director model."""

    id: int
    name: str
    linkedin_url: str | None = None
    email: str | None = None
    hashed_name: str | None = None


class Auditor(BaseApiModel):
    """Auditor model."""

    id: int
    name: str
    hashed_name: str | None = None


class Investor(BaseApiModel):
    """Investor model in company context."""

    name: str
    amount_invested: str
    currency: str


class Company(BaseApiModel):
    """Company model."""

    id: int
    uen: str | None = None
    additional_ids: list[str] | None = None
    name: str
    description: str | None = None
    headquaters: str | None = None
    website: str | None = None
    date_incorporated: str | None = None
    investment_stage: str | None = None
    total_equity_funding: float | None = None
    last_valuation: float | None = None
    size_of_last_round: float | None = None
    date_of_last_round: str | None = None
    revenue: float | None = None
    financial_year_end: str | None = None
    revenue_growth: float | None = None
    liquidation: str | None = None
    liquidation_details: str | None = None
    ebit: float | None = None
    liabilities: float | None = None
    status: str | None = None
    company_raising: str | None = None
    exit_type: str | None = None
    female_founder: bool | int | None = None
    updated_at: str | None = None
    sectors: list[Sector] = Field(default_factory=list)
    themes: list[Theme] = Field(default_factory=list)
    founders: list[Founder] = Field(default_factory=list)
    directors: list[Director] = Field(default_factory=list)
    auditors: list[Auditor] = Field(default_factory=list)
    investors: list[Investor] = Field(default_factory=list)
    financial_statements_audited: list | dict[str, str] | None = None
    financial_statements_extracted: str | list[Any] | dict[str, Any] | None = None


class Funding(BaseApiModel):
    """Funding model."""

    investment_quarter: int | float
    first_investment_date: str
    last_investment_date: str
    share_class_id: int | float
    series: str
    total_funding: float
    post_money_valuation: float
    pre_money_valuation: float
    max_share_price_paid: float
    average_share_price_paid: float
    total_shares_allocated: int | float


class AdditionalFunding(BaseApiModel):
    """Additional funding model."""

    investment_quarter: int | float | None = None
    investment_date: str | None = None
    series: str
    funding: float
    post_money_valuation: float
    currency: str | None = None
    price_share: float | None = None
    newslink: str
    title: str

    @field_validator("investment_quarter", mode="before")
    @classmethod
    def convert_empty_string_to_none(cls, v):
        """Convert empty strings to None for optional integer fields."""
        if v == "" or v is None:
            return None
        return v


class Revenue(BaseApiModel):
    """Revenue model."""

    revenue: float
    ebit: float
    revenue_quarter: int | float
    revenue_year: int | float


class Shareholder(BaseApiModel):
    """Shareholder model."""

    investor_name: str
    is_founder: bool = Field(alias="isFounder")
    investment_date: str
    investor_uen: str | None = None
    current_share_holding_percentage: int | float
    value_of_investment_at_last_round_valuation: int | float
    sum_amount_invested: float
    sum_shares_allocated: int | float
    sum_shares_sold: int | float | None = None
    sum_secondary_shares_purchased: int | float | None = None

    @field_validator("sum_shares_sold", "sum_secondary_shares_purchased", mode="before")
    @classmethod
    def convert_empty_string_to_none(cls, v):
        """Convert empty strings to None for optional integer fields."""
        if v == "" or v is None:
            return None
        return v


class FundingRoundAndValuation(BaseApiModel):
    """Funding round and valuation model."""

    investor_id: int
    type_of_investor: str | None = None
    investor_name: str
    investor_uen: str
    amount_invested: int | float
    shares_allocated: int | float
    investment_date: str
    price_per_share: float


class PerShareClassSummary(BaseApiModel):
    """Per share class summary model."""

    share_class_id: int | float
    share_class_name: str
    funding_rounds_and_valuation: list[FundingRoundAndValuation]


class CompanyFinancials(BaseApiModel):
    """Company financials model."""

    fundings: list[Funding]
    additional_fundings: list[AdditionalFunding]
    revenue: list[Revenue]
    shareholders: list[Shareholder]
    per_share_class_summary: list[PerShareClassSummary]


class InvestorCompany(BaseApiModel):
    """Company model in investor context."""

    id: int
    name: str
    uen: str
    description: str
    total_shares_allocated: int | float
    total_shares_sold: int | float
    total_secondary_shares: int | float
    total_invested: float
    total_seeds: float
    amount_invested_series_a: int | float
    amount_invested_series_b: int | float
    amount_invested_seed: float
    amount_invested_pre_seed: int | float
    amount_invested_series_c_and_beyond: int | float
    amount_invested_preference_ordinary: int | float
    amount_invested_ordinary: int | float
    amount_invested_preference: Any | None = None
    max_price_per_share: int | float
    remaining_shares_after_sold: int | float
    value_of_investment_at_last_round_valuation: int | float
    value_of_investment_at_last_round_valuation_primary: int | float
    value_of_investment_at_last_round_valuation_seconday: int | float
    remaining_shares_without_secondary_after_sold: int | float
    sectors: list[Sector]
    themes: list[Theme]


class InvestorDetail(BaseApiModel):
    """Investor detail model."""

    id: int
    investor_name: str
    investor_uen: str
    companies: list[InvestorCompany]


class InvestorSummary(BaseApiModel):
    """Investor summary model."""

    id: int
    investor_name: str
    investor_uen: str
    investment_date: str
    no_of_invested_companies: float
    total_invested: int | float | None = None
    amount_invested_seed: float | None = None
    amount_invested_series_a: float | None = None
    amount_invested_series_b: float | None = None
    amount_invested_series_c_and_beyond: float | None = None


class FounderDetail(BaseApiModel):
    """Founder detail model."""

    id: int
    name: str
    description: str | None = None
    linkedin_url: str | None = None
    email: str | None = None
    designation: str
    hashed_id: str
    company_id: int


class DirectorDetail(BaseApiModel):
    """Director detail model."""

    id: int
    name: str
    description: str | None = None
    linkedin_url: str | None = None
    email: str | None = None
    designation: str
    hashed_id: str
    company_id: int


class AuditorDetail(BaseApiModel):
    """Auditor detail model."""

    id: int
    name: str
    description: str | None = None
    linkedin_url: str | None = None
    hashed_id: str | None = None
    company_id: int


class PaginatedResponse(BaseApiModel):
    """Paginated response model."""

    total_records: int
    no_of_pages: int
    limit: int
    offset: int

    # Backwards-compat camelCase accessor used in tests
    @property
    def totalRecords(self) -> int:  # noqa: N802 - keep camelCase for BC
        return self.total_records


class CompanyListData(PaginatedResponse):
    """Company list data model."""

    data: list[Company]


class CompanyListResponse(BaseApiModel):
    """Company list response model."""

    data: CompanyListData


class CompanyResponse(BaseApiModel):
    """Company response model."""

    data: Company


class CompanyFinancialsResponse(BaseApiModel):
    """Company financials response model."""

    data: CompanyFinancials


class InvestorListData(PaginatedResponse):
    """Investor list data model."""

    data: list[InvestorSummary]


class InvestorListResponse(BaseApiModel):
    """Investor list response model."""

    data: InvestorListData


class InvestorResponse(BaseApiModel):
    """Investor response model."""

    data: InvestorDetail


class FounderListData(PaginatedResponse):
    """Founder list data model."""

    data: list[FounderDetail]


class FounderListResponse(BaseApiModel):
    """Founder list response model."""

    data: FounderListData


class FounderResponse(BaseApiModel):
    """Founder response model."""

    data: FounderDetail


class DirectorListData(PaginatedResponse):
    """Director list data model."""

    data: list[DirectorDetail]


class DirectorListResponse(BaseApiModel):
    """Director list response model."""

    data: DirectorListData


class DirectorResponse(BaseApiModel):
    """Director response model."""

    data: DirectorDetail


class AuditorListData(PaginatedResponse):
    """Auditor list data model."""

    data: list[AuditorDetail]


class AuditorListResponse(BaseApiModel):
    """Auditor list response model."""

    data: AuditorListData


class AuditorResponse(BaseApiModel):
    """Auditor response model."""

    data: AuditorDetail


class TokenResponse(BaseApiModel):
    """Token response model."""

    token: str


class ErrorResponse(BaseApiModel):
    """Error response model."""

    errors: str | list[str]
    message: str | None = None


# VentureCap API models
class LimitedPartnerType(BaseApiModel):
    """Limited Partner Type model."""

    lvl0: str
    lvl1: str


class FundType(BaseApiModel):
    """Fund Type model."""

    lvl0: str
    lvl1: str


class CapitalProvider(BaseApiModel):
    """Capital Provider model."""

    id: int
    registration_number: str | None = None
    name: str
    category: list[str] = Field(default_factory=list)
    type: list[str] = Field(default_factory=list)
    hq: str | None = None
    preferred_location: list[str] = Field(default_factory=list)
    preferred_deal_type: list[str] = Field(default_factory=list)
    preferred_fund_type: list[str] = Field(default_factory=list)
    preferred_sector: list[str] = Field(default_factory=list)
    preferred_theme: list[str] = Field(default_factory=list)


class Fund(BaseApiModel):
    """Fund model."""

    id: str | int
    alternatives_id: int | None = None
    registration_number: str | None = None
    name: str
    fund_manager_id: int | None = None
    fund_manager: str | None = None
    vintage_year: int | float | None = None
    type: FundType | None = None
    single_fund_type: str | None = Field(default=None, alias="singleFundType")
    size: float | None = None
    status: str | None = None
    irr: float | None = None
    net_multiple: float | None = None
    dpi: float | None = None
    rvpi: float | None = None
    last_report_quarter: str | None = None
    year: int | str | None = None
    quarter: str | None = None

    @field_validator(
        "fund_manager_id", "alternatives_id", "vintage_year", mode="before"
    )
    @classmethod
    def convert_empty_string_to_none(cls, v):
        """Convert empty strings to None for optional integer fields."""
        if v == "" or v is None:
            return None
        return v


class FundPerformance(BaseApiModel):
    """Fund Performance model."""

    id: str | int
    fund_id: int
    source: str | None = None
    source_name: str | None = None
    capital_provider_source_acting_as: str | None = None
    source_id: int | None = None
    irr: float | None = None
    dpi: float | None = None
    rvpi: float | None = None
    net_multiple: float | None = None
    share_redemption: str | float | None = None
    commited_capital: float | None = None
    profit: float | None = None
    retained_earnings: float | None = None
    dividend: str | float | None = None
    net_assets: float | None = None
    quarter: str | None = None
    year: int | str | None = None
    report_path: str | None = None
    reporting_period: str | None = None

    @field_validator("source_id", mode="before")
    @classmethod
    def convert_empty_string_to_none(cls, v):
        """Convert empty strings to None for optional integer fields."""
        if v == "" or v is None:
            return None
        return v


class CommitmentDeal(BaseApiModel):
    """Commitment Deal model."""

    id: str | int
    alternatives_id: int
    limited_partner_id: int
    limited_partner_name: str
    limited_partner_type: list[LimitedPartnerType] = Field(default_factory=list)
    fund_id: int
    fund_name: str
    vintage_year: float | None = None
    fund_manager_id: int
    fund_manager_name: str
    fund_type: str | None = None
    size: int | float | None = None
    category: str | None = None
    deal_date: str | None = None


class JobTitle(BaseApiModel):
    """Job Title model."""

    id: int
    job_title: str
    role_type: str
    company_name: str


class Person(BaseApiModel):
    """Person model."""

    id: int
    first_name: str
    last_name: str
    email: str | None = None
    linkedin_url: str | None = None
    job_titles: list[JobTitle] = Field(default_factory=list)


# Response models for VentureCap API
class CapitalProviderListResponse(BaseApiModel):
    """Capital Provider list response model."""

    total_records: int
    limit: int
    offset: int
    data: list[CapitalProvider]

    @property
    def totalRecords(self) -> int:  # noqa: N802 - keep camelCase for BC
        return self.total_records


class CapitalProviderResponse(BaseApiModel):
    """Capital Provider response model."""

    data: CapitalProvider


class FundListResponse(BaseApiModel):
    """Fund list response model."""

    total_records: int
    limit: int
    offset: int
    data: list[Fund]


class FundResponse(BaseApiModel):
    """Fund response model."""

    data: Fund


class FundPerformanceListResponse(BaseApiModel):
    """Fund Performance list response model."""

    total_records: int
    limit: int
    offset: int
    data: list[FundPerformance]

    @property
    def totalRecords(self) -> int:  # noqa: N802 - keep camelCase for BC
        return self.total_records


class FundPerformanceResponse(BaseApiModel):
    """Fund Performance response model."""

    data: FundPerformance


class CommitmentDealListResponse(BaseApiModel):
    """Commitment Deal list response model."""

    total_records: int
    limit: int
    offset: int
    data: list[CommitmentDeal]

    @property
    def totalRecords(self) -> int:  # noqa: N802 - keep camelCase for BC
        return self.total_records


class CommitmentDealResponse(BaseApiModel):
    """Commitment Deal response model."""

    data: CommitmentDeal


class PersonListResponse(BaseApiModel):
    """Person list response model."""

    total_records: int
    limit: int
    offset: int
    data: list[Person]

    @property
    def totalRecords(self) -> int:  # noqa: N802 - keep camelCase for BC
        return self.total_records


class PersonResponse(BaseApiModel):
    """Person response model."""

    data: Person
