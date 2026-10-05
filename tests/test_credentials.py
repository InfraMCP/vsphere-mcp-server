"""Test credential management functionality."""

import pytest

from vsphere_mcp_server.credentials import (
    CredentialError,
    extract_domain,
    get_credentials,
)


def test_extract_domain():
    """Test domain extraction from FQDN."""
    assert extract_domain("vcenter.company.local") == "company.local"
    assert extract_domain("host01.company.local") == "company.local"
    assert (
        extract_domain("simple.hostname") == "simple.hostname"
    )  # Only 2 parts, returns full hostname
    assert extract_domain("single") == "single"  # Single part, returns as-is


def test_get_credentials_from_env_vars(monkeypatch):
    monkeypatch.setenv("VSPHERE_USERNAME", "admin@vsphere.local")
    monkeypatch.setenv("VSPHERE_PASSWORD", "secret")

    assert get_credentials("vcenter.company.local") == ("admin@vsphere.local", "secret")


def test_get_credentials_rejects_non_macos_without_env_vars(monkeypatch):
    monkeypatch.delenv("VSPHERE_USERNAME", raising=False)
    monkeypatch.delenv("VSPHERE_PASSWORD", raising=False)
    monkeypatch.setattr(
        "vsphere_mcp_server.credentials.platform.system", lambda: "Linux"
    )

    with pytest.raises(CredentialError, match="VSPHERE_USERNAME"):
        get_credentials("vcenter.company.local")


def test_get_credentials_falls_back_when_security_missing(monkeypatch):
    monkeypatch.delenv("VSPHERE_USERNAME", raising=False)
    monkeypatch.delenv("VSPHERE_PASSWORD", raising=False)
    monkeypatch.setattr(
        "vsphere_mcp_server.credentials.platform.system", lambda: "Darwin"
    )

    def fake_run(*args, **kwargs):
        raise FileNotFoundError("security")

    monkeypatch.setattr("vsphere_mcp_server.credentials.subprocess.run", fake_run)
    monkeypatch.setattr(
        "vsphere_mcp_server.credentials._prompt_for_credentials",
        lambda hostname, domain, service_name: ("user@company.local", "secret"),
    )

    assert get_credentials("vcenter.company.local") == ("user@company.local", "secret")
