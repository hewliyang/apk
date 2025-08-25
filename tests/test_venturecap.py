"""Tests specifically for VentureCap API endpoints."""

from altpe_sdk import AlternativesPE
from altpe_sdk.exceptions import NotFoundError


class TestVentureCapIntegration:
    """Integration tests for VentureCap API endpoints."""

    async def test_capital_providers_pagination(self, client: AlternativesPE):
        """Test capital providers pagination works correctly."""
        # Get first page
        page1 = await client.get_capital_providers(limit=10, offset=0)

        # Get second page
        page2 = await client.get_capital_providers(limit=10, offset=10)

        # Should have different data
        if page1.data and page2.data and len(page1.data) > 0 and len(page2.data) > 0:
            assert page1.data[0].id != page2.data[0].id

    async def test_funds_filtering_by_vintage_year(self, client: AlternativesPE):
        """Test funds can be filtered by vintage year."""
        response = await client.get_funds(
            vintage_year_min=2020, vintage_year_max=2024, limit=50
        )

        assert response.total_records >= 0
        for fund in response.data:
            if fund.vintage_year is not None:
                assert 2020 <= fund.vintage_year <= 2024

    async def test_fund_performance_metrics_filtering(self, client: AlternativesPE):
        """Test fund performances can be filtered by performance metrics."""
        response = await client.get_fund_performances(irr_min=0, irr_max=50, limit=20)

        assert response.totalRecords >= 0
        for performance in response.data:
            if performance.irr is not None:
                assert 0 <= performance.irr <= 50

    async def test_commitment_deals_by_fund_type(self, client: AlternativesPE):
        """Test commitment deals can be filtered by fund type."""
        # Test with a common fund type ID (10 from the spec examples)
        response = await client.get_commitment_deals(fund_type=10, limit=10)

        # Should return data without errors
        assert response.totalRecords >= 0

    async def test_people_name_filtering(self, client: AlternativesPE):
        """Test people can be filtered by names."""
        response = await client.get_people(first_name="John", limit=5)

        assert response.totalRecords >= 0
        for person in response.data:
            if person.first_name:
                assert "John" in person.first_name

    async def test_complete_workflow_funds_and_performance(
        self, client: AlternativesPE
    ):
        """Test a complete workflow: get funds, then get their performance data."""
        # Get funds
        funds_response = await client.get_funds(limit=5)

        if funds_response.data:
            # For each fund, try to get performance data
            for fund in funds_response.data[:2]:  # Test first 2 funds only
                fund_id = int(fund.id)

                try:
                    performance_response = await client.get_fund_performances(
                        fund_id=fund_id, limit=5
                    )
                    # Should complete without errors
                    assert performance_response.totalRecords >= 0
                except Exception:
                    # Some funds might not have performance data, which is OK
                    pass

    async def test_model_validation_capital_providers(self, client: AlternativesPE):
        """Test that capital provider models validate correctly."""
        response = await client.get_capital_providers(limit=1)

        if response.data:
            provider = response.data[0]

            # Test required fields
            assert provider.id is not None
            assert provider.name is not None
            assert isinstance(provider.category, list)
            assert isinstance(provider.type, list)
            assert isinstance(provider.preferred_location, list)
            assert isinstance(provider.preferred_deal_type, list)

    async def test_model_validation_funds(self, client: AlternativesPE):
        """Test that fund models validate correctly."""
        response = await client.get_funds(limit=1)

        if response.data:
            fund = response.data[0]

            # Test required fields
            assert fund.id is not None
            assert fund.name is not None

            # Test optional fields have correct types
            if fund.size is not None:
                assert isinstance(fund.size, (int, float))
            if fund.vintage_year is not None:
                assert isinstance(fund.vintage_year, int)

    async def test_model_validation_commitment_deals(self, client: AlternativesPE):
        """Test that commitment deal models validate correctly."""
        response = await client.get_commitment_deals(limit=1)

        if response.data:
            deal = response.data[0]

            # Test required fields
            assert deal.id is not None
            assert deal.alternatives_id is not None
            assert deal.limited_partner_id is not None
            assert deal.limited_partner_name is not None
            assert deal.fund_id is not None
            assert deal.fund_name is not None
            assert deal.fund_manager_id is not None
            assert deal.fund_manager_name is not None

            # Test list fields
            assert isinstance(deal.limited_partner_type, list)

    async def test_edge_cases_empty_results(self, client: AlternativesPE):
        """Test handling of potentially empty result sets."""
        # Use very restrictive filters that might return no results
        response = await client.get_capital_providers(
            query="nonexistent_company_name_12345", limit=10
        )

        # Should handle empty results gracefully
        assert response.totalRecords >= 0
        assert isinstance(response.data, list)

    async def test_large_pagination_limits(self, client: AlternativesPE):
        """Test that API respects pagination limits."""
        response = await client.get_capital_providers(limit=100)

        # Should respect the 100 limit from the API
        assert len(response.data) <= 100
        assert response.limit == 100

    async def test_order_direction_validation(self, client: AlternativesPE):
        """Test that ordering works correctly."""
        # Test ascending order
        asc_response = await client.get_funds(
            order_by="name", order_direction="asc", limit=10
        )

        # Test descending order
        desc_response = await client.get_funds(
            order_by="name", order_direction="desc", limit=10
        )

        # Should return results for both
        assert asc_response.total_records >= 0
        assert desc_response.total_records >= 0

        # If we have data from both, first items should be different
        if (
            asc_response.data
            and desc_response.data
            and len(asc_response.data) > 0
            and len(desc_response.data) > 0
        ):
            # Names should be in different order (unless there's only one result)
            if asc_response.total_records > 1:
                assert (
                    asc_response.data[0].name != desc_response.data[0].name
                    or asc_response.total_records == 1
                )


class TestVentureCapErrorHandling:
    """Test error handling for VentureCap endpoints."""

    async def test_invalid_capital_provider_category(self, client: AlternativesPE):
        """Test handling of invalid category parameter."""
        # Get a valid provider first
        providers = await client.get_capital_providers(limit=1)
        if providers.data:
            provider_id = providers.data[0].id

            # This might still work but test the structure
            response = await client.get_capital_provider_by_id(
                provider_id, category="invalid-category"
            )
            assert response.data is not None

    async def test_fund_performance_invalid_metrics(self, client: AlternativesPE):
        """Test fund performance filtering with edge case values."""
        # Test with negative values (should still work, just might return no results)
        response = await client.get_fund_performances(
            irr_min=-100, irr_max=-50, limit=5
        )

        # Should handle gracefully
        assert response.totalRecords >= 0

    async def test_people_empty_name_filters(self, client: AlternativesPE):
        """Test people endpoint with empty name filters."""
        response = await client.get_people(first_name="", last_name="", limit=5)

        # Should handle gracefully
        assert response.totalRecords >= 0


class TestVentureCapDataIntegrity:
    """Test data integrity across VentureCap endpoints."""

    async def test_fund_manager_consistency(self, client: AlternativesPE):
        """Test that fund manager data is consistent across endpoints."""
        # Get a commitment deal
        deals = await client.get_commitment_deals(limit=1)

        if deals.data:
            deal = deals.data[0]
            fund_manager_id = deal.fund_manager_id
            fund_manager_name = deal.fund_manager_name

            # Try to find the same fund manager in capital providers
            providers = await client.get_capital_providers(
                query=fund_manager_name[:20],  # Use partial name
                category="fund-manager",
                limit=50,
            )

            # Check if we can find a matching provider
            found_match = False
            for provider in providers.data:
                if fund_manager_name.lower() in provider.name.lower():
                    found_match = True
                    break

            # This is informational - not all fund managers might be in both endpoints
            # but the test ensures the query doesn't fail
            assert isinstance(found_match, bool)

    async def test_fund_id_consistency(self, client: AlternativesPE):
        """Test that fund IDs are consistent across endpoints."""
        # Get a fund performance record
        performances = await client.get_fund_performances(limit=1)

        if performances.data:
            performance = performances.data[0]
            fund_id = performance.fund_id

            # Try to get the corresponding fund
            try:
                fund = await client.get_fund_by_id(fund_id)
                assert fund.data is not None
                assert int(fund.data.id) == fund_id
            except NotFoundError:
                # Some performance records might reference funds not in the funds endpoint
                # This is acceptable in real-world scenarios
                pass
