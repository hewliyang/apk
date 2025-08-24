#!/usr/bin/env python3
"""Live integration tests for the Alternatives.PE SDK.

This module contains live tests that make actual API calls to verify
SDK functionality. These tests require valid API credentials.

Usage:
    python live_tests.py
"""

import asyncio
import os
import traceback

from dotenv import load_dotenv

from altpe_sdk import AlternativesPE
from altpe_sdk.enums import (
    CapitalProviderCategory,
    CompanyStatus,
    OrderDirection,
    ResponseType,
)

load_dotenv()


async def test_companies(client: AlternativesPE):
    """Test company endpoints."""
    print("🏢 Testing Company Endpoints...")

    try:
        # Test basic company list
        response = await client.get_companies(limit=3)
        print(f"  ✓ get_companies: {len(response.data.data)} companies")

        if response.data.data:
            first_company = response.data.data[0]
            company_id = str(first_company.id)

            # Test get by ID
            company_detail = await client.get_company_by_id(company_id)
            print(f"  ✓ get_company_by_id: {company_detail.data.name}")

            # Test financials if available
            try:
                financials = await client.get_company_financials_by_id(company_id)
                print(
                    f"  ✓ get_company_financials: {len(financials.data.fundings)} fundings"
                )
            except Exception:
                print("  ⚠️  Financials not available for this company")

        return True
    except Exception as e:
        print(f"  ❌ Company tests failed: {e}")
        return False


async def test_capital_providers(client: AlternativesPE):
    """Test capital provider endpoints."""
    print("🏦 Testing Capital Providers...")

    try:
        # Test list endpoint
        response = await client.get_capital_providers(limit=3)
        print(f"  ✓ get_capital_providers: {response.total_records} total")

        if response.data:
            provider = response.data[0]
            print(f"  📋 Example: {provider.name} (ID: {provider.id})")

            # Test get by ID
            try:
                detail = await client.get_capital_provider_by_id(
                    provider.id, category=CapitalProviderCategory.FUND_MANAGER
                )
                print(f"  ✓ get_capital_provider_by_id: {detail.data.name}")
            except Exception as e:
                print(f"  ⚠️  Provider detail failed: {e}")

        return True
    except Exception as e:
        print(f"  ❌ Capital provider tests failed: {e}")
        return False


async def test_funds(client: AlternativesPE):
    """Test fund endpoints."""
    print("💰 Testing Funds...")

    try:
        response = await client.get_funds(limit=3)
        print(f"  ✓ get_funds: {response.total_records} total")

        if response.data:
            fund = response.data[0]
            print(f"  📋 Example: {fund.name} (${fund.size:,.0f})")

        return True
    except Exception as e:
        print(f"  ❌ Fund tests failed: {e}")
        return False


async def test_investors(client: AlternativesPE):
    """Test investor endpoints."""
    print("🤝 Testing Investors...")

    try:
        response = await client.get_investors(limit=3)
        print(f"  ✓ get_investors: {response.data.total_records} total")

        if response.data.data:
            investor = response.data.data[0]
            print(f"  📋 Example: {investor.investor_name}")

        return True
    except Exception as e:
        print(f"  ❌ Investor tests failed: {e}")
        return False


async def test_people(client: AlternativesPE):
    """Test people endpoints."""
    print("👥 Testing People...")

    try:
        response = await client.get_people(limit=3)
        print(f"  ✓ get_people: {response.total_records} total")

        if response.data:
            person = response.data[0]
            print(f"  📋 Example: {person.full_name}")

        return True
    except Exception as e:
        print(f"  ❌ People tests failed: {e}")
        return False


async def test_advanced_filtering(client: AlternativesPE):
    """Test advanced filtering capabilities."""
    print("🔍 Testing Advanced Filtering...")

    try:
        # Test companies with multiple filters
        companies = await client.get_companies(
            limit=3,
            query="tech",
            sectors="22,44",  # Financial Services, IT
            status=CompanyStatus.ACTIVE,
            response_type=ResponseType.SIMPLE,
            order_direction=OrderDirection.DESC,
        )
        print(f"  ✓ Multi-filter companies: {len(companies.data.data)} results")

        # Test valuation filtering
        valued_companies = await client.get_companies(
            limit=2,
            valuation_min=1000000,  # $1M+
            valuation_max=10000000,  # $10M max
        )
        print(f"  ✓ Valuation filter: {len(valued_companies.data.data)} companies")

        return True
    except Exception as e:
        print(f"  ❌ Advanced filtering failed: {e}")
        return False


async def main():
    """Main test runner."""
    print("🧪 Alternatives.PE SDK - Live Integration Tests")
    print("=" * 60)

    # Check credentials
    client_id = os.getenv("ALTPE_CLIENT_ID")
    client_secret = os.getenv("ALTPE_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("❌ Missing credentials in environment variables")
        print("Please set ALTPE_CLIENT_ID and ALTPE_CLIENT_SECRET")
        return False

    client = AlternativesPE(client_id=client_id, client_secret=client_secret)

    test_results = []

    try:
        # Run all test suites
        test_suites = [
            test_companies,
            test_capital_providers,
            test_funds,
            test_investors,
            test_people,
            test_advanced_filtering,
        ]

        for test_suite in test_suites:
            try:
                result = await test_suite(client)
                test_results.append(result)
            except Exception as e:
                print(f"❌ Test suite {test_suite.__name__} crashed: {e}")
                traceback.print_exc()
                test_results.append(False)

    finally:
        await client.close()

    # Summary
    passed = sum(test_results)
    total = len(test_results)

    print("\n📊 Test Summary:")
    print("=" * 40)
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {passed/total*100:.1f}%")

    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
