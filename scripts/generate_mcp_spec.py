#!/usr/bin/env python3
"""Generate MCP tool specifications from API discovery"""

import json


def generate_mcp_tools():
    """Generate MCP tool specifications based on discovered APIs."""
    
    tools = {
        # VM Management
        "list_vms": {
            "description": "List all virtual machines with basic information",
            "endpoint": "GET /rest/vcenter/vm",
            "parameters": {},
            "returns": "Array of VM objects with name, power_state, cpu_count, memory_size_MiB"
        },
        
        "get_vm_details": {
            "description": "Get detailed information about a specific virtual machine",
            "endpoint": "GET /rest/vcenter/vm/{vm_id}",
            "parameters": {
                "vm_id": {"type": "string", "description": "VM identifier (e.g., vm-100079)"}
            },
            "returns": "Detailed VM configuration"
        },
        
        "power_on_vm": {
            "description": "Power on a virtual machine",
            "endpoint": "POST /rest/vcenter/vm/{vm_id}/power/start",
            "parameters": {
                "vm_id": {"type": "string", "description": "VM identifier"}
            },
            "returns": "Operation status"
        },
        
        "power_off_vm": {
            "description": "Power off a virtual machine",
            "endpoint": "POST /rest/vcenter/vm/{vm_id}/power/stop",
            "parameters": {
                "vm_id": {"type": "string", "description": "VM identifier"}
            },
            "returns": "Operation status"
        },
        
        # Host Management
        "list_hosts": {
            "description": "List all ESXi hosts",
            "endpoint": "GET /rest/vcenter/host",
            "parameters": {},
            "returns": "Array of host objects with name, connection_state, power_state"
        },
        
        "get_host_details": {
            "description": "Get detailed information about a specific ESXi host",
            "endpoint": "GET /rest/vcenter/host/{host_id}",
            "parameters": {
                "host_id": {"type": "string", "description": "Host identifier"}
            },
            "returns": "Detailed host configuration"
        },
        
        # Datacenter Management
        "list_datacenters": {
            "description": "List all datacenters",
            "endpoint": "GET /rest/vcenter/datacenter",
            "parameters": {},
            "returns": "Array of datacenter objects with name and identifier"
        },
        
        "get_datacenter_details": {
            "description": "Get detailed information about a specific datacenter",
            "endpoint": "GET /rest/vcenter/datacenter/{datacenter_id}",
            "parameters": {
                "datacenter_id": {"type": "string", "description": "Datacenter identifier"}
            },
            "returns": "Detailed datacenter configuration"
        },
        
        # Datastore Management
        "list_datastores": {
            "description": "List all datastores with capacity and usage information",
            "endpoint": "GET /rest/vcenter/datastore",
            "parameters": {},
            "returns": "Array of datastore objects with name, type, capacity, and free_space"
        },
        
        "get_datastore_details": {
            "description": "Get detailed information about a specific datastore",
            "endpoint": "GET /rest/vcenter/datastore/{datastore_id}",
            "parameters": {
                "datastore_id": {"type": "string", "description": "Datastore identifier"}
            },
            "returns": "Detailed datastore configuration and metrics"
        },
        
        # Folder Management
        "list_folders": {
            "description": "List all folders organized by type (VM, Host, Network, etc.)",
            "endpoint": "GET /rest/vcenter/folder",
            "parameters": {},
            "returns": "Array of folder objects with name, type, and identifier"
        },
        
        "get_folder_details": {
            "description": "Get detailed information about a specific folder",
            "endpoint": "GET /rest/vcenter/folder/{folder_id}",
            "parameters": {
                "folder_id": {"type": "string", "description": "Folder identifier"}
            },
            "returns": "Detailed folder configuration and contents"
        },
        
        # Network Management
        "list_networks": {
            "description": "List all networks with VLAN information",
            "endpoint": "GET /rest/vcenter/network",
            "parameters": {},
            "returns": "Array of network objects with name, type, and VLAN details"
        },
        
        "get_network_details": {
            "description": "Get detailed information about a specific network",
            "endpoint": "GET /rest/vcenter/network/{network_id}",
            "parameters": {
                "network_id": {"type": "string", "description": "Network identifier"}
            },
            "returns": "Detailed network configuration including VLAN settings"
        },
        
        "list_vlans": {
            "description": "Extract and list available VLANs from network names",
            "endpoint": "GET /rest/vcenter/network (processed)",
            "parameters": {},
            "returns": "Array of VLAN IDs and descriptions extracted from network names"
        }
    }
    
    return tools


if __name__ == "__main__":
    tools = generate_mcp_tools()
    
    with open("../docs/mcp_tools_spec.json", "w") as f:
        json.dump(tools, f, indent=2)
    
    print("MCP tool specifications generated in ../docs/mcp_tools_spec.json")
    print(f"Total tools: {len(tools)}")
    
    for tool_name in tools.keys():
        print(f"  - {tool_name}")
