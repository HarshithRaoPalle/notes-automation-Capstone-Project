"""Test self healing module."""

import pytest
from unittest.mock import MagicMock
from core.agentic.self_healing import SelfHealingLocator


def test_self_healing_locator_simple_value_extraction():
    """Test that _simple_value correctly extracts values from different locator formats."""
    healer = SelfHealingLocator(MagicMock())

    assert healer._simple_value("#my_element") == "my_element"
    assert healer._simple_value("[data-testid='my-test']") == "my-test"
    assert healer._simple_value("//div[@id='test']") == ""
    assert healer._simple_value("regular_element") == "regular_element"
