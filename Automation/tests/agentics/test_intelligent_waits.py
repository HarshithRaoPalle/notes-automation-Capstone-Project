"""Test intelligent waits module."""

import pytest
from unittest.mock import MagicMock, patch
from core.agentic.intelligent_waits import IntelligentWaits


def test_intelligent_waits_initialization():
    """Test that IntelligentWaits initializes with correct timeout and poll frequency."""
    mock_driver = MagicMock()

    with patch('core.agentic.intelligent_waits.config') as mock_config:
        mock_config.timeout = 10
        waits = IntelligentWaits(mock_driver)

        assert waits.driver == mock_driver
        assert waits.timeout == 10
        assert waits.poll_frequency == 1
