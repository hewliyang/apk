"""Test entity mappings."""

from altpe_sdk.mappings import EntityMappings


class TestEntityMappings:
    """Test entity mappings functionality."""

    def test_sectors_loaded(self):
        """Test that sectors are loaded correctly."""
        mappings = EntityMappings()

        assert len(mappings.sectors) > 0
        assert mappings.get_sector_name(22) == "Financial Services"
        assert mappings.get_sector_name(44) == "Information Technology"
        assert mappings.get_sector_name(47) == "Software / Internet"

    def test_themes_loaded(self):
        """Test that themes are loaded correctly."""
        mappings = EntityMappings()

        assert len(mappings.themes) > 0
        assert mappings.get_theme_name(13) == "Blockchain"
        assert mappings.get_theme_name(35) == "FinTech"

    def test_locations_loaded(self):
        """Test that locations are loaded correctly."""
        mappings = EntityMappings()

        assert len(mappings.locations) > 0
        # Test some known locations
        assert "Singapore" in mappings.get_location_name(147)
        assert "Thailand" in mappings.get_location_name(148)

    def test_fund_types_loaded(self):
        """Test that fund types are loaded correctly."""
        mappings = EntityMappings()

        assert len(mappings.fund_types) > 0
        assert mappings.get_fund_type_name(1) == "Private Equity - General"
        assert mappings.get_fund_type_name(2) == "Buyout"

    def test_unknown_ids(self):
        """Test handling of unknown IDs."""
        mappings = EntityMappings()

        assert "Unknown Sector (999)" in mappings.get_sector_name(999)
        assert "Unknown Theme (999)" in mappings.get_theme_name(999)
        assert "Unknown Location (999)" in mappings.get_location_name(999)
        assert "Unknown Fund Type (999)" in mappings.get_fund_type_name(999)

    def test_get_choices_methods(self):
        """Test get choices methods return copies."""
        mappings = EntityMappings()

        sector_choices = mappings.get_sector_choices()
        theme_choices = mappings.get_theme_choices()
        location_choices = mappings.get_location_choices()
        fund_type_choices = mappings.get_fund_type_choices()

        # Should have data
        assert len(sector_choices) > 0
        assert len(theme_choices) > 0
        assert len(location_choices) > 0
        assert len(fund_type_choices) > 0

        # Should be copies (modifying shouldn't affect original)
        original_count = len(mappings.sectors)
        sector_choices.clear()
        assert len(mappings.sectors) == original_count
