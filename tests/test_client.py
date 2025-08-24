"""Test the main client functionality."""

import pytest

from altpe_sdk import AlternativesPE
from altpe_sdk.enums import CompanyStatus, OrderDirection, ResponseType
from altpe_sdk.exceptions import AuthenticationError, NotFoundError


class TestClientInitialization:
    """Test client initialization."""

    def test_init_with_credentials(self):
        """Test initialization with explicit credentials."""
        client = AlternativesPE(
            client_id="test_id",
            client_secret="test_secret",
        )
        assert client._http_client.config.client_id == "test_id"
        assert client._http_client.config.client_secret == "test_secret"

    def test_init_without_credentials_uses_env(self):
        """Test initialization without explicit credentials uses environment."""
        # Since we have env vars set, this should work
        client = AlternativesPE()
        assert client._http_client.config.client_id is not None
        assert client._http_client.config.client_secret is not None


class TestCompanyMethods:
    """Test company-related methods."""

    async def test_get_companies_basic(self, client: AlternativesPE):
        """Test basic company retrieval."""
        response = await client.get_companies(limit=5)

        assert response.data is not None
        assert response.data.total_records > 0
        assert len(response.data.data) <= 5
        assert response.data.limit == 5
        assert response.data.offset == 0

    async def test_get_companies_with_filters(self, client: AlternativesPE):
        """Test company retrieval with filters."""
        response = await client.get_companies(
            limit=2,
            query="tech",
            status=CompanyStatus.ACTIVE,
            order_direction=OrderDirection.DESC,
            response_type=ResponseType.DETAILED,
        )

        assert response.data is not None
        assert len(response.data.data) <= 2

    async def test_get_company_by_id(
        self, client: AlternativesPE, sample_company_id: str
    ):
        """Test get company by ID."""
        response = await client.get_company_by_id(sample_company_id)

        assert response.data is not None
        assert response.data.id == int(sample_company_id)
        assert response.data.name is not None

    async def test_get_company_by_uen(
        self, client: AlternativesPE, sample_company_uen: str
    ):
        """Test get company by UEN."""
        response = await client.get_company_by_uen(sample_company_uen)

        assert response.data is not None
        assert response.data.uen == sample_company_uen
        assert response.data.name is not None

    async def test_get_company_financials_by_id(
        self, client: AlternativesPE, sample_company_id: str
    ):
        """Test get company financials by ID."""
        response = await client.get_company_financials_by_id(sample_company_id)

        assert response.data is not None
        # Check if at least one of the financial data lists is present
        assert (
            response.data.fundings
            or response.data.revenue
            or response.data.shareholders
            or response.data.per_share_class_summary
        )

    async def test_get_company_financials_by_uen(
        self, client: AlternativesPE, sample_company_uen: str
    ):
        """Test get company financials by UEN."""
        response = await client.get_company_financials_by_uen(sample_company_uen)

        assert response.data is not None

    async def test_get_company_not_found(self, client: AlternativesPE):
        """Test get company with invalid ID raises NotFoundError."""
        with pytest.raises(NotFoundError):
            await client.get_company_by_id("999999")


class TestInvestorMethods:
    """Test investor-related methods."""

    async def test_get_investors_basic(self, client: AlternativesPE):
        """Test basic investor retrieval."""
        response = await client.get_investors(limit=5)

        assert response.data is not None
        assert len(response.data.data) <= 5

    async def test_get_investor_by_id(
        self, client: AlternativesPE, sample_investor_id: str
    ):
        """Test get investor by ID."""
        response = await client.get_investor_by_id(sample_investor_id)

        assert response.data is not None
        assert response.data.id == int(sample_investor_id)
        assert response.data.investor_name is not None


class TestDirectorMethods:
    """Test director-related methods."""

    async def test_get_directors_basic(self, client: AlternativesPE):
        """Test basic director retrieval."""
        response = await client.get_directors(limit=5)

        assert response.data is not None
        assert len(response.data.data) <= 5

    async def test_get_director_by_id(
        self, client: AlternativesPE, sample_director_id: str
    ):
        """Test get director by ID."""
        response = await client.get_director_by_id(sample_director_id)

        assert response.data is not None
        assert response.data.id == int(sample_director_id)
        assert response.data.name is not None


class TestFounderMethods:
    """Test founder-related methods."""

    async def test_get_founders_basic(self, client: AlternativesPE):
        """Test basic founder retrieval."""
        response = await client.get_founders(limit=5)

        assert response.data is not None
        assert len(response.data.data) <= 5

    async def test_get_founder_by_id(
        self, client: AlternativesPE, sample_founder_id: str
    ):
        """Test get founder by ID."""
        response = await client.get_founder_by_id(sample_founder_id)

        assert response.data is not None
        assert response.data.id == int(sample_founder_id)
        assert response.data.name is not None


class TestAuditorMethods:
    """Test auditor-related methods."""

    async def test_get_auditors_basic(self, client: AlternativesPE):
        """Test basic auditor retrieval."""
        response = await client.get_auditors(limit=5)

        assert response.data is not None
        assert len(response.data.data) <= 5

    async def test_get_auditor_by_id(
        self, client: AlternativesPE, sample_auditor_id: str
    ):
        """Test get auditor by ID."""
        response = await client.get_auditor_by_id(sample_auditor_id)

        assert response.data is not None
        assert response.data.id == int(sample_auditor_id)
        assert response.data.name is not None


class TestCapitalProviderMethods:
    """Test VentureCap API capital provider methods."""

    async def test_get_capital_providers_basic(self, client: AlternativesPE):
        """Test basic capital provider retrieval."""
        response = await client.get_capital_providers(limit=5)

        assert response.totalRecords > 0
        assert len(response.data) <= 5
        assert response.limit == 5
        assert response.offset == 0

    async def test_get_capital_providers_with_filters(self, client: AlternativesPE):
        """Test capital provider retrieval with filters."""
        response = await client.get_capital_providers(
            limit=2,
            category="fund-manager",
            order_direction="desc",
        )

        assert len(response.data) <= 2
        for provider in response.data:
            assert "Fund Manager" in provider.category

    async def test_get_capital_provider_by_id(self, client: AlternativesPE):
        """Test get capital provider by ID."""
        # First get a list to find a valid ID
        providers = await client.get_capital_providers(limit=1)
        if providers.data:
            provider_id = providers.data[0].id
            response = await client.get_capital_provider_by_id(
                provider_id, category="fund-manager"
            )

            assert response.data.id == provider_id
            assert response.data.name is not None


class TestFundMethods:
    """Test VentureCap API fund methods."""

    async def test_get_funds_basic(self, client: AlternativesPE):
        """Test basic fund retrieval."""
        response = await client.get_funds(limit=5)

        assert response.total_records > 0
        assert len(response.data) <= 5
        assert response.limit == 5
        assert response.offset == 0

    async def test_get_funds_with_filters(self, client: AlternativesPE):
        """Test fund retrieval with filters."""
        response = await client.get_funds(
            limit=2,
            vintage_year_min=2020,
            vintage_year_max=2024,
            order_direction="desc",
        )

        assert len(response.data) <= 2
        for fund in response.data:
            if fund.vintage_year:
                assert 2020 <= fund.vintage_year <= 2024

    async def test_get_fund_by_id(self, client: AlternativesPE):
        """Test get fund by ID."""
        # First get a list to find a valid ID
        funds = await client.get_funds(limit=1)
        if funds.data:
            fund_id = int(funds.data[0].id)
            response = await client.get_fund_by_id(fund_id)

            assert int(response.data.id) == fund_id
            assert response.data.name is not None


class TestFundPerformanceMethods:
    """Test VentureCap API fund performance methods."""

    async def test_get_fund_performances_basic(self, client: AlternativesPE):
        """Test basic fund performance retrieval."""
        response = await client.get_fund_performances(limit=5)

        assert response.totalRecords > 0
        assert len(response.data) <= 5
        assert response.limit == 5
        assert response.offset == 0

    async def test_get_fund_performances_with_filters(self, client: AlternativesPE):
        """Test fund performance retrieval with filters."""
        response = await client.get_fund_performances(
            limit=2,
            irr_min=0,
            irr_max=100,
            order_direction="desc",
        )

        assert len(response.data) <= 2

    async def test_get_fund_performance_by_id(self, client: AlternativesPE):
        """Test get fund performance by ID."""
        # First get a list to find a valid ID
        performances = await client.get_fund_performances(limit=1)
        if performances.data:
            performance_id = int(performances.data[0].id)
            response = await client.get_fund_performance_by_id(performance_id)

            assert int(response.data.id) == performance_id
            assert response.data.fund_id is not None


class TestCommitmentDealMethods:
    """Test VentureCap API commitment deal methods."""

    async def test_get_commitment_deals_basic(self, client: AlternativesPE):
        """Test basic commitment deal retrieval."""
        response = await client.get_commitment_deals(limit=5)

        assert response.totalRecords > 0
        assert len(response.data) <= 5
        assert response.limit == 5
        assert response.offset == 0

    async def test_get_commitment_deals_with_filters(self, client: AlternativesPE):
        """Test commitment deal retrieval with filters."""
        response = await client.get_commitment_deals(
            limit=2,
            order_direction="desc",
        )

        assert len(response.data) <= 2

    async def test_get_commitment_deal_by_id(self, client: AlternativesPE):
        """Test get commitment deal by ID."""
        # First get a list to find a valid ID
        deals = await client.get_commitment_deals(limit=1)
        if deals.data:
            deal_id = int(deals.data[0].id)
            response = await client.get_commitment_deal_by_id(deal_id)

            assert int(response.data.id) == deal_id
            assert response.data.limited_partner_name is not None


class TestPeopleMethods:
    """Test VentureCap API people methods."""

    async def test_get_people_basic(self, client: AlternativesPE):
        """Test basic people retrieval."""
        response = await client.get_people(limit=5)

        assert response.totalRecords > 0
        assert len(response.data) <= 5
        assert response.limit == 5
        assert response.offset == 0

    async def test_get_people_with_filters(self, client: AlternativesPE):
        """Test people retrieval with filters."""
        response = await client.get_people(
            limit=2,
            order_by="first_name",
            order_direction="asc",
        )

        assert len(response.data) <= 2

    async def test_get_person_by_id(self, client: AlternativesPE):
        """Test get person by ID."""
        # First get a list to find a valid ID
        people = await client.get_people(limit=1)
        if people.data:
            person_id = people.data[0].id
            response = await client.get_person_by_id(person_id)

            assert response.data.id == person_id
            assert response.data.first_name is not None
            assert response.data.last_name is not None


class TestErrorHandling:
    """Test error handling."""

    async def test_invalid_credentials(self):
        """Test invalid credentials raise AuthenticationError."""
        async with AlternativesPE(
            client_id="invalid",
            client_secret="invalid",
        ) as client:
            with pytest.raises(AuthenticationError):
                await client.get_companies(limit=1)

    async def test_get_capital_provider_not_found(self, client: AlternativesPE):
        """Test get capital provider with invalid ID raises NotFoundError."""
        with pytest.raises(NotFoundError):
            await client.get_capital_provider_by_id(999999, category="fund-manager")

    async def test_get_fund_not_found(self, client: AlternativesPE):
        """Test get fund with invalid ID raises NotFoundError."""
        with pytest.raises(NotFoundError):
            await client.get_fund_by_id(999999)

    async def test_get_fund_performance_not_found(self, client: AlternativesPE):
        """Test get fund performance with invalid ID raises NotFoundError."""
        with pytest.raises(NotFoundError):
            await client.get_fund_performance_by_id(999999)

    async def test_get_commitment_deal_not_found(self, client: AlternativesPE):
        """Test get commitment deal with invalid ID raises NotFoundError."""
        with pytest.raises(NotFoundError):
            await client.get_commitment_deal_by_id(999999)

    async def test_get_person_not_found(self, client: AlternativesPE):
        """Test get person with invalid ID raises NotFoundError."""
        with pytest.raises(NotFoundError):
            await client.get_person_by_id(999999)
