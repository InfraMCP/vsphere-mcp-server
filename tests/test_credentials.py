"""Test credential management functionality."""

import pytest
from vsphere_mcp_server.credentials import extract_domain


def test_extract_domain():
    """Test domain extraction from FQDN."""
    assert extract_domain("vcenter.company.local") == "company.local"
    assert extract_domain("host01.company.local") == "company.local"
    assert extract_domain("simple.hostname") == "simple.hostname"  # Only 2 parts, returns full hostname
    assert extract_domain("single") == "single"  # Single part, returns as-is
