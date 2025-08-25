"""Pydantic models for the Alternatives.PE API."""

from typing import Any, Optional, Union

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
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    hashed_name: Optional[str] = None


class Director(BaseApiModel):
    """Director model."""

    id: int
    name: str
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    hashed_name: Optional[str] = None


class Auditor(BaseApiModel):
    """Auditor model."""

    id: int
    name: str
    hashed_name: Optional[str] = None


class Investor(BaseApiModel):
    """Investor model in company context."""

    name: str
    amount_invested: str
    currency: str


class Company(BaseApiModel):
    """Company model."""

    id: int
    uen: Optional[str] = None
    additional_ids: Optional[list[str]] = None
    name: str
    description: Optional[str] = None
    headquaters: Optional[str] = None
    website: Optional[str] = None
    date_incorporated: Optional[str] = None
    investment_stage: Optional[str] = None
    total_equity_funding: Optional[float] = None
    last_valuation: Optional[float] = None
    size_of_last_round: Optional[float] = None
    date_of_last_round: Optional[str] = None
    revenue: Optional[float] = None
    financial_year_end: Optional[str] = None
    revenue_growth: Optional[float] = None
    liquidation: Optional[str] = None
    liquidation_details: Optional[str] = None
    ebit: Optional[float] = None
    liabilities: Optional[float] = None
    status: Optional[str] = None
    company_raising: Optional[str] = None
    exit_type: Optional[str] = None
    female_founder: Optional[Union[bool, int]] = None
    updated_at: Optional[str] = None
    sectors: list[Sector] = Field(default_factory=list)
    themes: list[Theme] = Field(default_factory=list)
    founders: list[Founder] = Field(default_factory=list)
    directors: list[Director] = Field(default_factory=list)
    auditors: list[Auditor] = Field(default_factory=list)
    investors: list[Investor] = Field(default_factory=list)
    financial_statements_audited: Optional[Union[list, dict[str, str]]] = None
    financial_statements_extracted: Optional[Union[str, list[Any], dict[str, Any]]] = (
        None
    )


class Funding(BaseApiModel):
    """Funding model."""

    investment_quarter: int
    first_investment_date: str
    last_investment_date: str
    share_class_id: int
    series: str
    total_funding: float
    post_money_valuation: float
    pre_money_valuation: float
    max_share_price_paid: float
    average_share_price_paid: float
    total_shares_allocated: int


class AdditionalFunding(BaseApiModel):
    """Additional funding model."""

    investment_quarter: Optional[int] = None
    investment_date: Optional[str] = None
    series: str
    funding: float
    post_money_valuation: float
    currency: Optional[str] = None
    price_share: Optional[float] = None
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
    revenue_quarter: int
    revenue_year: int


class Shareholder(BaseApiModel):
    """Shareholder model."""

    investor_name: str
    is_founder: bool = Field(alias="isFounder")
    investment_date: str
    investor_uen: str
    current_share_holding_percentage: Union[int, float]
    value_of_investment_at_last_round_valuation: int
    sum_amount_invested: float
    sum_shares_allocated: int
    sum_shares_sold: Optional[int] = None
    sum_secondary_shares_purchased: Optional[int] = None

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
    type_of_investor: Optional[str] = None
    investor_name: str
    investor_uen: str
    amount_invested: Union[int, float]
    shares_allocated: int
    investment_date: str
    price_per_share: float


class PerShareClassSummary(BaseApiModel):
    """Per share class summary model."""

    share_class_id: int
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
    total_shares_allocated: int
    total_shares_sold: int
    total_secondary_shares: int
    total_invested: float
    total_seeds: float
    amount_invested_series_a: int
    amount_invested_series_b: int
    amount_invested_seed: float
    amount_invested_pre_seed: int
    amount_invested_series_c_and_beyond: int
    amount_invested_preference_ordinary: int
    amount_invested_ordinary: int
    amount_invested_preference: Optional[Any] = None
    max_price_per_share: Union[int, float]
    remaining_shares_after_sold: int
    value_of_investment_at_last_round_valuation: Union[int, float]
    value_of_investment_at_last_round_valuation_primary: Union[int, float]
    value_of_investment_at_last_round_valuation_seconday: int
    remaining_shares_without_secondary_after_sold: int
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
    total_invested: Union[int, float] | None = None
    amount_invested_seed: float | None = None
    amount_invested_series_a: Optional[float] = None
    amount_invested_series_b: Optional[float] = None
    amount_invested_series_c_and_beyond: Optional[float] = None


class FounderDetail(BaseApiModel):
    """Founder detail model."""

    id: int
    name: str
    description: Optional[str] = None
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    designation: str
    hashed_id: str
    company_id: int


class DirectorDetail(BaseApiModel):
    """Director detail model."""

    id: int
    name: str
    description: Optional[str] = None
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    designation: str
    hashed_id: str
    company_id: int


class AuditorDetail(BaseApiModel):
    """Auditor detail model."""

    id: int
    name: str
    description: Optional[str] = None
    linkedin_url: Optional[str] = None
    hashed_id: Optional[str] = None
    company_id: int


class PaginatedResponse(BaseApiModel):
    """Paginated response model."""

    total_records: int
    no_of_pages: int
    limit: int
    offset: int


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

    errors: Union[str, list[str]]
    message: Optional[str] = None


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
    registration_number: Optional[str] = None
    name: str
    category: list[str] = Field(default_factory=list)
    type: list[str] = Field(default_factory=list)
    hq: Optional[str] = None
    preferred_location: list[str] = Field(default_factory=list)
    preferred_deal_type: list[str] = Field(default_factory=list)
    preferred_fund_type: list[str] = Field(default_factory=list)
    preferred_sector: list[str] = Field(default_factory=list)
    preferred_theme: list[str] = Field(default_factory=list)


class Fund(BaseApiModel):
    """Fund model."""

    id: Union[str, int]
    alternatives_id: Optional[int] = None
    registration_number: Optional[str] = None
    name: str
    fund_manager_id: Optional[int] = None
    fund_manager: Optional[str] = None
    vintage_year: Optional[int] = None
    type: Optional[FundType] = None
    singleFundType: Optional[str] = None
    size: Optional[float] = None
    status: Optional[str] = None
    irr: Optional[float] = None
    net_multiple: Optional[float] = None
    dpi: Optional[float] = None
    rvpi: Optional[float] = None
    last_report_quarter: Optional[str] = None
    year: Optional[Union[int, str]] = None
    quarter: Optional[str] = None

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

    id: Union[str, int]
    fund_id: int
    source: Optional[str] = None
    source_name: Optional[str] = None
    capital_provider_source_acting_as: Optional[str] = None
    source_id: Optional[int] = None
    irr: Optional[float] = None
    dpi: Optional[float] = None
    rvpi: Optional[float] = None
    net_multiple: Optional[float] = None
    share_redemption: Optional[Union[str, float]] = None
    commited_capital: Optional[float] = None
    profit: Optional[float] = None
    retained_earnings: Optional[float] = None
    dividend: Optional[Union[str, float]] = None
    net_assets: Optional[float] = None
    quarter: Optional[str] = None
    year: Optional[Union[int, str]] = None
    report_path: Optional[str] = None
    reporting_period: Optional[str] = None

    @field_validator("source_id", mode="before")
    @classmethod
    def convert_empty_string_to_none(cls, v):
        """Convert empty strings to None for optional integer fields."""
        if v == "" or v is None:
            return None
        return v


class CommitmentDeal(BaseApiModel):
    """Commitment Deal model."""

    id: Union[str, int]
    alternatives_id: int
    limited_partner_id: int
    limited_partner_name: str
    limited_partner_type: list[LimitedPartnerType] = Field(default_factory=list)
    fund_id: int
    fund_name: str
    vintage_year: Optional[float] = None
    fund_manager_id: int
    fund_manager_name: str
    fund_type: Optional[str] = None
    size: Optional[Union[int, float]] = None
    category: Optional[str] = None
    deal_date: Optional[str] = None


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
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    job_titles: list[JobTitle] = Field(default_factory=list)


# Response models for VentureCap API
class CapitalProviderListResponse(BaseApiModel):
    """Capital Provider list response model."""

    total_records: int
    limit: int
    offset: int
    data: list[CapitalProvider]


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


class FundPerformanceResponse(BaseApiModel):
    """Fund Performance response model."""

    data: FundPerformance


class CommitmentDealListResponse(BaseApiModel):
    """Commitment Deal list response model."""

    total_records: int
    limit: int
    offset: int
    data: list[CommitmentDeal]


class CommitmentDealResponse(BaseApiModel):
    """Commitment Deal response model."""

    data: CommitmentDeal


class PersonListResponse(BaseApiModel):
    """Person list response model."""

    total_records: int
    limit: int
    offset: int
    data: list[Person]


class PersonResponse(BaseApiModel):
    """Person response model."""

    data: Person
