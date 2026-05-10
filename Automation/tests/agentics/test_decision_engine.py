"""Test decision engine module."""

import pytest
from core.agentic.decision_engine import decide_action, RetryDecision
from selenium.common.exceptions import TimeoutException


def test_decide_action_returns_correct_decision():
    """Test that decide_action returns the correct decision for different exceptions."""
    assert decide_action(AssertionError("test")) == RetryDecision.FAIL_FAST
    assert decide_action(TimeoutException("test")) == RetryDecision.RETRY
    assert decide_action(TimeoutException("test"), ("id", "element")) == RetryDecision.HEAL_AND_RETRY
