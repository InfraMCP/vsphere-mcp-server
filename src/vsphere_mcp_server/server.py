"""vSphere MCP Server - Main server implementation."""

import re

from mcp.server.fastmcp import FastMCP
from .vsphere_client import VSphereClient
from .credentials import clear_credentials


# Initialize MCP server
mcp = FastMCP("vSphere MCP Server")


def _handle_error(e: Exception, operation: str) -> str:
    """Handle errors consistently across all tools."""
    error_msg = str(e)

    if "Authentication failed" in error_msg:
        return (
            f"Authentication failed for {operation}. "
            "Try clearing credentials with vsphere_clear_credentials."
        )
    if "Connection" in error_msg or "timeout" in error_msg.lower():
        return f"Connection failed for {operation}. Check network connectivity and hostname."
    return f"Error in {operation}: {error_msg}"


# Credential Management Tool
@mcp.tool()
def vsphere_clear_credentials(hostname: str) -> str:
    """Clear stored vSphere credentials for a domain.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
    """
    try:
        success = clear_credentials(hostname)
        if success:
            return f"Credentials cleared for domain extracted from {hostname}"
        return f"No stored credentials found for domain extracted from {hostname}"
    except Exception as e:
        return _handle_error(e, "clearing credentials")


# VM Management Tools
@mcp.tool()
def list_vms(hostname: str) -> str:
    """List all virtual machines with basic information.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
    """
    client = VSphereClient(hostname)
    try:
        response = client.get("vcenter/vm")
        vms = response.get("value", [])

        if not vms:
            return "No virtual machines found"

        result = f"Found {len(vms)} virtual machines:\n\n"
        for vm in vms:
            result += f"• {vm.get('name', 'Unknown')} (ID: {vm.get('vm')})\n"
            result += f"  Power State: {vm.get('power_state', 'Unknown')}\n"
            result += f"  CPU Count: {vm.get('cpu_count', 'Unknown')}\n"
            result += f"  Memory: {vm.get('memory_size_MiB', 'Unknown')} MiB\n\n"

        return result.strip()

    except Exception as e:
        return _handle_error(e, "listing VMs")
    finally:
        client.close()


@mcp.tool()
def get_vm_details(hostname: str, vm_id: str) -> str:
    """Get detailed information about a specific virtual machine.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
        vm_id: Virtual machine ID or name
    """
    client = VSphereClient(hostname)
    try:
        # If vm_id doesn't start with 'vm-', assume it's a name and look up the ID
        if not vm_id.startswith('vm-'):
            vms_response = client.get("vcenter/vm")
            vms = vms_response.get("value", [])

            # Find VM by name (case-insensitive)
            vm_id_found = None
            for vm in vms:
                if vm.get("name", "").lower() == vm_id.lower():
                    vm_id_found = vm.get("vm")
                    break

            if not vm_id_found:
                return f"Virtual machine '{vm_id}' not found by name"

            vm_id = vm_id_found

        response = client.get(f"vcenter/vm/{vm_id}")
        vm = response.get("value", {})

        if not vm:
            return f"Virtual machine {vm_id} not found"

        result = f"VM Details: {vm.get('name', 'Unknown')}\n"
        result += f"ID: {vm_id}\n"
        result += f"Power State: {vm.get('power_state', 'Unknown')}\n"
        result += f"CPU Count: {vm.get('cpu', {}).get('count', 'Unknown')}\n"
        result += f"Memory: {vm.get('memory', {}).get('size_MiB', 'Unknown')} MiB\n"
        result += f"Guest OS: {vm.get('guest_OS', 'Unknown')}\n"
        result += (
            f"Hardware Version: {vm.get('hardware', {}).get('version', 'Unknown')}\n"
        )

        # Network info
        nics = vm.get("nics", [])
        if nics:
            result += "\nNetwork Interfaces:\n"
            for i, nic in enumerate(nics):
                network_name = "Unknown"
                if isinstance(nic, dict):
                    backing = nic.get("backing", {})
                    if isinstance(backing, dict):
                        network_name = backing.get("network_name", "Unknown")
                result += f"  NIC {i}: {network_name}\n"

        return result

    except Exception as e:
        return _handle_error(e, f"getting VM {vm_id} details")
    finally:
        client.close()


@mcp.tool()
def power_on_vm(hostname: str, vm_id: str) -> str:
    """Power on a virtual machine.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
        vm_id: Virtual machine ID
    """
    client = VSphereClient(hostname)
    try:
        client.post(f"vcenter/vm/{vm_id}/power/start")
        return "Power on initiated for VM " + vm_id

    except Exception as e:
        return _handle_error(e, f"powering on VM {vm_id}")
    finally:
        client.close()


@mcp.tool()
def power_off_vm(hostname: str, vm_id: str) -> str:
    """Power off a virtual machine.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
        vm_id: Virtual machine ID
    """
    client = VSphereClient(hostname)
    try:
        client.post(f"vcenter/vm/{vm_id}/power/stop")
        return f"Power off initiated for VM {vm_id}"

    except Exception as e:
        return _handle_error(e, f"powering off VM {vm_id}")
    finally:
        client.close()


# Infrastructure Tools
@mcp.tool()
def list_hosts(hostname: str) -> str:
    """List all ESXi hosts.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
    """
    client = VSphereClient(hostname)
    try:
        response = client.get("vcenter/host")
        hosts = response.get("value", [])

        if not hosts:
            return "No ESXi hosts found"

        result = f"Found {len(hosts)} ESXi hosts:\n\n"
        for host in hosts:
            result += f"• {host.get('name', 'Unknown')} (ID: {host.get('host')})\n"
            result += f"  Connection State: {host.get('connection_state', 'Unknown')}\n"
            result += f"  Power State: {host.get('power_state', 'Unknown')}\n\n"

        return result.strip()

    except Exception as e:
        return _handle_error(e, "listing hosts")
    finally:
        client.close()


@mcp.tool()
def get_host_details(hostname: str, host_id: str) -> str:
    """Get detailed information about an ESXi host.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
        host_id: ESXi host ID
    """
    client = VSphereClient(hostname)
    try:
        response = client.get(f"vcenter/host/{host_id}")
        host = response.get("value", {})

        if not host:
            return f"ESXi host {host_id} not found"

        result = f"Host Details: {host.get('name', 'Unknown')}\n"
        result += f"ID: {host_id}\n"
        result += f"Connection State: {host.get('connection_state', 'Unknown')}\n"
        result += f"Power State: {host.get('power_state', 'Unknown')}\n"

        return result

    except Exception as e:
        return _handle_error(e, f"getting host {host_id} details")
    finally:
        client.close()


@mcp.tool()
def list_datacenters(hostname: str) -> str:
    """List all datacenters.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
    """
    client = VSphereClient(hostname)
    try:
        response = client.get("vcenter/datacenter")
        datacenters = response.get("value", [])

        if not datacenters:
            return "No datacenters found"

        result = f"Found {len(datacenters)} datacenters:\n\n"
        for dc in datacenters:
            result += f"• {dc.get('name', 'Unknown')} (ID: {dc.get('datacenter')})\n"

        return result.strip()

    except Exception as e:
        return _handle_error(e, "listing datacenters")
    finally:
        client.close()


@mcp.tool()
def get_datacenter_details(hostname: str, datacenter_id: str) -> str:
    """Get detailed information about a datacenter.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
        datacenter_id: Datacenter ID
    """
    client = VSphereClient(hostname)
    try:
        response = client.get(f"vcenter/datacenter/{datacenter_id}")
        dc = response.get("value", {})

        if not dc:
            return f"Datacenter {datacenter_id} not found"

        result = f"Datacenter Details: {dc.get('name', 'Unknown')}\n"
        result += f"ID: {datacenter_id}\n"

        return result

    except Exception as e:
        return _handle_error(e, f"getting datacenter {datacenter_id} details")
    finally:
        client.close()


@mcp.tool()
def list_datastores(hostname: str) -> str:
    """List all datastores with capacity information.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
    """
    client = VSphereClient(hostname)
    try:
        response = client.get("vcenter/datastore")
        datastores = response.get("value", [])

        if not datastores:
            return "No datastores found"

        result = f"Found {len(datastores)} datastores:\n\n"
        for ds in datastores:
            capacity = ds.get("capacity", 0)
            free_space = ds.get("free_space", 0)
            used_space = capacity - free_space
            used_pct = (used_space / capacity * 100) if capacity > 0 else 0

            result += f"• {ds.get('name', 'Unknown')} (ID: {ds.get('datastore')})\n"
            result += f"  Type: {ds.get('type', 'Unknown')}\n"
            result += f"  Capacity: {capacity / (1024**3):.1f} GB\n"
            result += f"  Used: {used_space / (1024**3):.1f} GB ({used_pct:.1f}%)\n"
            result += f"  Free: {free_space / (1024**3):.1f} GB\n\n"

        return result.strip()

    except Exception as e:
        return _handle_error(e, "listing datastores")
    finally:
        client.close()


@mcp.tool()
def get_datastore_details(hostname: str, datastore_id: str) -> str:
    """Get detailed information about a datastore.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
        datastore_id: Datastore ID
    """
    client = VSphereClient(hostname)
    try:
        response = client.get(f"vcenter/datastore/{datastore_id}")
        ds = response.get("value", {})

        if not ds:
            return f"Datastore {datastore_id} not found"

        capacity = ds.get("capacity", 0) or 0
        free_space = ds.get("free_space", 0) or 0

        # Ensure values are positive
        if capacity <= 0 or free_space < 0:
            result = f"Datastore Details: {ds.get('name', 'Unknown')}\n"
            result += f"ID: {datastore_id}\n"
            result += f"Type: {ds.get('type', 'Unknown')}\n"
            result += "Capacity information not available or invalid\n"
            return result

        used_space = capacity - free_space
        used_pct = (used_space / capacity * 100) if capacity > 0 else 0

        result = f"Datastore Details: {ds.get('name', 'Unknown')}\n"
        result += f"ID: {datastore_id}\n"
        result += f"Type: {ds.get('type', 'Unknown')}\n"
        result += f"Capacity: {capacity / (1024**3):.1f} GB\n"
        result += f"Used: {used_space / (1024**3):.1f} GB ({used_pct:.1f}%)\n"
        result += f"Free: {free_space / (1024**3):.1f} GB\n"

        return result

    except Exception as e:
        return _handle_error(e, f"getting datastore {datastore_id} details")
    finally:
        client.close()


# Organization Tools
@mcp.tool()
def list_folders(hostname: str, folder_type: str = "VIRTUAL_MACHINE") -> str:
    """List folders by type.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
        folder_type: Folder type (VIRTUAL_MACHINE, HOST, DATACENTER, DATASTORE, NETWORK)
    """
    client = VSphereClient(hostname)
    try:
        response = client.get(f"vcenter/folder?filter.type={folder_type}")
        folders = response.get("value", [])

        if not folders:
            return f"No {folder_type} folders found"

        result = f"Found {len(folders)} {folder_type} folders:\n\n"
        for folder in folders:
            result += (
                f"• {folder.get('name', 'Unknown')} (ID: {folder.get('folder')})\n"
            )

        return result.strip()

    except Exception as e:
        return _handle_error(e, f"listing {folder_type} folders")
    finally:
        client.close()


@mcp.tool()
def get_folder_details(hostname: str, folder_id: str) -> str:
    """Get detailed information about a folder.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
        folder_id: Folder ID
    """
    client = VSphereClient(hostname)
    try:
        response = client.get(f"vcenter/folder/{folder_id}")
        folder = response.get("value", {})

        if not folder:
            return f"Folder {folder_id} not found or inaccessible"

        result = f"Folder Details: {folder.get('name', 'Unknown')}\n"
        result += f"ID: {folder_id}\n"
        result += f"Type: {folder.get('type', 'Unknown')}\n"

        return result

    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            return f"Folder {folder_id} not found or access denied (may be a system folder)"
        return _handle_error(e, f"getting folder {folder_id} details")
    finally:
        client.close()


# Network Tools
@mcp.tool()
def list_networks(hostname: str) -> str:
    """List all networks with VLAN information.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
    """
    client = VSphereClient(hostname)
    try:
        response = client.get("vcenter/network")
        networks = response.get("value", [])

        if not networks:
            return "No networks found"

        result = f"Found {len(networks)} networks:\n\n"
        for network in networks:
            name = network.get("name", "Unknown")
            result += f"• {name} (ID: {network.get('network')})\n"
            result += f"  Type: {network.get('type', 'Unknown')}\n"

            # Extract VLAN info from name
            vlan_match = re.search(r"v(\d+)-|VLAN(\d+)", name)
            if vlan_match:
                vlan_id = vlan_match.group(1) or vlan_match.group(2)
                result += f"  VLAN ID: {vlan_id}\n"

            result += "\n"

        return result.strip()

    except Exception as e:
        return _handle_error(e, "listing networks")
    finally:
        client.close()


@mcp.tool()
def get_network_details(hostname: str, network_id: str) -> str:
    """Get detailed information about a network.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
        network_id: Network ID
    """
    client = VSphereClient(hostname)
    try:
        response = client.get(f"vcenter/network/{network_id}")
        network = response.get("value", {})

        if not network:
            return f"Network {network_id} not found or inaccessible"

        name = network.get("name", "Unknown")
        result = f"Network Details: {name}\n"
        result += f"ID: {network_id}\n"
        result += f"Type: {network.get('type', 'Unknown')}\n"

        # Extract VLAN info from name
        vlan_match = re.search(r"v(\d+)-|VLAN(\d+)", name)
        if vlan_match:
            vlan_id = vlan_match.group(1) or vlan_match.group(2)
            result += f"VLAN ID: {vlan_id}\n"

        return result

    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            return (f"Network {network_id} not found or is a distributed portgroup "
                   "(not accessible via this API)")
        return _handle_error(e, f"getting network {network_id} details")
    finally:
        client.close()


@mcp.tool()
def get_vlan_info(hostname: str, vlan_query: str) -> str:
    """Get information about a VLAN by name or VLAN ID.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
        vlan_query: VLAN name (e.g., v1306-MEL03-Secure-Management) or VLAN ID (e.g., 1306)
    """
    client = VSphereClient(hostname)
    try:
        response = client.get("vcenter/network")
        networks = response.get("value", [])

        if not networks:
            return "No networks found"

        matches = []

        # Search by name (partial match, case-insensitive)
        for network in networks:
            name = network.get("name", "")
            if vlan_query.lower() in name.lower():
                matches.append(network)

        # If no name matches and query is numeric, search by VLAN ID
        if not matches and vlan_query.isdigit():
            vlan_id = vlan_query
            for network in networks:
                name = network.get("name", "")
                vlan_match = re.search(r"v(\d+)-|VLAN(\d+)", name)
                if vlan_match:
                    extracted_vlan = vlan_match.group(1) or vlan_match.group(2)
                    if extracted_vlan == vlan_id:
                        matches.append(network)

        if not matches:
            return f"No VLAN found matching '{vlan_query}'"

        result = f"VLAN Search Results for '{vlan_query}':\n\n"

        for network in matches:
            name = network.get("name", "Unknown")
            result += f"• {name}\n"
            result += f"  Network ID: {network.get('network', 'Unknown')}\n"
            result += f"  Type: {network.get('type', 'Unknown')}\n"

            # Extract VLAN ID from name
            vlan_match = re.search(r"v(\d+)-|VLAN(\d+)", name)
            if vlan_match:
                vlan_id = vlan_match.group(1) or vlan_match.group(2)
                result += f"  VLAN ID: {vlan_id}\n"

            result += "\n"

        result += f"Found {len(matches)} matching network(s)"
        return result

    except Exception as e:
        return _handle_error(e, f"searching for VLAN '{vlan_query}'")
    finally:
        client.close()


@mcp.tool()
def list_vlans(hostname: str) -> str:
    """Extract and list VLAN information from network names.

    Args:
        hostname: vSphere hostname (e.g., vcenter.domain.local)
    """
    client = VSphereClient(hostname)
    try:
        response = client.get("vcenter/network")
        networks = response.get("value", [])

        if not networks:
            return "No networks found"

        vlans = {}
        for network in networks:
            name = network.get("name", "Unknown")
            vlan_match = re.search(r"v(\d+)-|VLAN(\d+)", name)
            if vlan_match:
                vlan_id = vlan_match.group(1) or vlan_match.group(2)
                if vlan_id not in vlans:
                    vlans[vlan_id] = []
                vlans[vlan_id].append(name)

        if not vlans:
            return "No VLAN information found in network names"

        result = f"Found {len(vlans)} VLANs:\n\n"
        for vlan_id in sorted(vlans.keys(), key=int):
            result += f"VLAN {vlan_id}:\n"
            for network_name in vlans[vlan_id]:
                result += f"  • {network_name}\n"
            result += "\n"

        return result.strip()

    except Exception as e:
        return _handle_error(e, "extracting VLAN information")
    finally:
        client.close()


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
