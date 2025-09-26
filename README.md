# vSphere MCP Server

[![Pylint](https://github.com/rorymcmahon/vsphere-mcp-server/actions/workflows/pylint.yml/badge.svg)](https://github.com/rorymcmahon/vsphere-mcp-server/actions/workflows/pylint.yml)
[![Safety Security Scan](https://github.com/rorymcmahon/vsphere-mcp-server/actions/workflows/safety-scan.yml/badge.svg)](https://github.com/rorymcmahon/vsphere-mcp-server/actions/workflows/safety-scan.yml)
[![Dependency Security Check](https://github.com/rorymcmahon/vsphere-mcp-server/actions/workflows/dependency-security.yml/badge.svg)](https://github.com/rorymcmahon/vsphere-mcp-server/actions/workflows/dependency-security.yml)

MCP server for VMware vSphere infrastructure management. Provides comprehensive access to vSphere environments through the Model Context Protocol.

## Features

- **Seamless Authentication**: Domain-based credential caching with GUI prompts
- **VM Management**: List, inspect, and control virtual machines
- **Infrastructure Monitoring**: Monitor hosts, datacenters, and datastores
- **Network Discovery**: Explore networks and extract VLAN information
- **Organization Tools**: Navigate folders and organizational structures
- **Secure Credential Storage**: macOS Keychain integration with TTL

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd vsphere-mcp-server

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "vsphere": {
      "command": "python",
      "args": ["-m", "vsphere_mcp_server.server"]
    }
  }
}
```

## Available Tools

### Authentication
- `vsphere_clear_credentials(hostname)` - Clear cached credentials for domain

### Virtual Machine Management
- `list_vms(hostname)` - List all VMs with basic info
- `get_vm_details(hostname, vm_id)` - Detailed VM configuration
- `power_on_vm(hostname, vm_id)` - Power on VM
- `power_off_vm(hostname, vm_id)` - Power off VM

### Infrastructure Management
- `list_hosts(hostname)` - List ESXi hosts
- `get_host_details(hostname, host_id)` - Host details
- `list_datacenters(hostname)` - List datacenters
- `get_datacenter_details(hostname, datacenter_id)` - Datacenter details
- `list_datastores(hostname)` - List datastores with capacity
- `get_datastore_details(hostname, datastore_id)` - Datastore details

### Organization
- `list_folders(hostname, folder_type)` - List folders by type
- `get_folder_details(hostname, folder_id)` - Folder details

### Networking
- `list_networks(hostname)` - List networks with VLAN info
- `get_network_details(hostname, network_id)` - Network details
- `list_vlans(hostname)` - Extract VLAN info from network names

## Usage Examples

### Basic VM Operations
```bash
# List all virtual machines
list_vms("vcenter.domain.local")

# Get detailed VM information
get_vm_details("vcenter.domain.local", "vm-123")

# Power operations
power_on_vm("vcenter.domain.local", "vm-123")
power_off_vm("vcenter.domain.local", "vm-123")
```

### Infrastructure Monitoring
```bash
# Check datastore capacity
list_datastores("vcenter.domain.local")

# Monitor host status
list_hosts("vcenter.domain.local")
get_host_details("vcenter.domain.local", "host-456")
```

### Network Discovery
```bash
# Explore network configuration
list_networks("vcenter.domain.local")

# Extract VLAN information
list_vlans("vcenter.domain.local")
```

### Credential Management
```bash
# Clear stored credentials if needed
vsphere_clear_credentials("vcenter.domain.local")
```

## Authentication

The server uses domain-based credential caching:

1. **First Use**: GUI prompts for username and password
2. **Credential Storage**: Stored in macOS Keychain with 4-hour TTL
3. **Automatic Renewal**: Re-prompts when credentials expire
4. **Domain Extraction**: `vcenter.domain.local` → `domain.local`

### Supported Username Formats
- `username@domain.local`
- `domain\username` (converted to @ format)
- `username` (domain auto-appended)

## Security

- Credentials stored securely in macOS Keychain
- 4-hour TTL prevents stale credential usage
- SSL verification disabled by default (common in enterprise environments)
- Session tokens used for API authentication
- Automatic session cleanup on exit

## Error Handling

The server provides clear error messages with troubleshooting steps:

- **Authentication Errors**: Suggests clearing credentials
- **Connection Errors**: Indicates network/hostname issues
- **API Errors**: Shows specific vSphere API responses

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/
```

## Troubleshooting

### Authentication Issues
1. Clear credentials: `vsphere_clear_credentials("hostname")`
2. Verify username format includes domain
3. Check network connectivity to vCenter

### Connection Issues
1. Verify hostname is reachable
2. Check vCenter is running and accessible
3. Confirm SSL/TLS configuration

### Permission Issues
1. Verify user has required vSphere permissions
2. Check role assignments in vCenter
3. Ensure user can access required objects

## License

MIT License - see LICENSE file for details.
