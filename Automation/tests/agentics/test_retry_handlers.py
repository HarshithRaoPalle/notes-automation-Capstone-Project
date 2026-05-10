"""Test retry handlers module."""

import pytest
from core.agentic.retry_handler import retry_on_flaky_action
from selenium.common.exceptions import StaleElementReferenceException


def test_retry_on_flaky_action_retries_on_exception():
    """Test that retry_on_flaky_action retries when a flaky exception occurs."""
    call_count = 0

    @retry_on_flaky_action(retries=3, delay=0)
    def flaky_function():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise StaleElementReferenceException("Stale element")
        return "success"

    result = flaky_function()
    assert result == "success"
    assert call_count == 2
