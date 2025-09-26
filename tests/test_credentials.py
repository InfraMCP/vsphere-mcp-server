"""Test credential management functionality."""

import pytest
from vsphere_mcp_server.credentials import extract_domain


def test_extract_domain():
    """Test domain extraction from FQDN."""
    assert extract_domain("vcenter.vocus.local") == "vocus.local"
    assert extract_domain("syd03pvcs02.vocus.local") == "vocus.local"
    assert extract_domain("simple.hostname") == "hostname"
    assert extract_domain("single") == "single"
