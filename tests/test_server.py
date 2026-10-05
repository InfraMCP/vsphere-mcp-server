"""Regression tests for server helpers and tool edge cases."""

from vsphere_mcp_server import server


class FakeClient:
    """Minimal fake client for server tool tests."""

    responses: dict = {}

    def __init__(self, hostname):
        self.hostname = hostname

    def get(self, endpoint):
        response = self.responses[endpoint]
        if isinstance(response, Exception):
            raise response
        return response

    def post(self, endpoint, data=None):
        response = self.responses[endpoint]
        if isinstance(response, Exception):
            raise response
        return response

    def close(self):
        return None


def test_looks_like_vm_moid():
    assert server._looks_like_vm_moid("vm-42") is True
    assert server._looks_like_vm_moid("vm-1") is True
    assert server._looks_like_vm_moid("vm-prod-app01") is False
    assert server._looks_like_vm_moid("my-vm") is False
    assert server._looks_like_vm_moid("vm-") is False


def test_get_vm_details_resolves_name_that_starts_with_vm_prefix(monkeypatch):
    monkeypatch.setattr(server, "VSphereClient", FakeClient)
    FakeClient.responses = {
        "vcenter/vm": {"value": [{"name": "vm-prod-app01", "vm": "vm-42"}]},
        "vcenter/vm/vm-42": {
            "value": {"name": "vm-prod-app01", "power_state": "POWERED_ON"}
        },
    }

    result = server.get_vm_details("vc.local", "vm-prod-app01")

    assert "ID: vm-42" in result
    assert "VM Details: vm-prod-app01" in result


def test_list_datastores_handles_null_capacity(monkeypatch):
    monkeypatch.setattr(server, "VSphereClient", FakeClient)
    FakeClient.responses = {
        "vcenter/datastore": {
            "value": [
                {
                    "name": "ds-1",
                    "datastore": "datastore-1",
                    "type": "VMFS",
                    "capacity": None,
                    "free_space": None,
                }
            ]
        }
    }

    result = server.list_datastores("vc.local")

    assert "ds-1" in result
    assert "Capacity: 0.0 GB" in result
