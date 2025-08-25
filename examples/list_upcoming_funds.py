from dotenv import load_dotenv
from rich import print

from altpe_sdk import AlternativesPE, enums
from altpe_sdk.utils import format_as_xml


def main():
    load_dotenv()

    client = AlternativesPE()
    # Get funds with status filter for upcoming
    response = client.get_companies(
        limit=10,
        investment_stage=enums.InvestmentStage.PRE_SEED,
        countries=[enums.CountryCode.SGP, enums.CountryCode.MYS],
    )

    print(f"Total records: {response.data.total_records}")
    print(format_as_xml(response.data))


if __name__ == "__main__":
    main()
