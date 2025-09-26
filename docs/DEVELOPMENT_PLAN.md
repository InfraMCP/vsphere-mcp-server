# vSphere MCP Server Development Plan

## Key Learnings from Existing MCP Servers

### 1. Authentication Pattern (from win-mcp-server & ssh-mcp-server)

**Domain-Based Credential Management:**
- Extract domain from FQDN: `vcenter.domain.local` → `domain.local`
- Service name: `vsphere-mcp` (consistent with `win-mcp`, `ssh-mcp`)
- Account format: `username@domain.local`
- TTL: 4 hours default with expiry checking

**GUI Authentication Flow:**
- Use macOS `osascript` for GUI prompts when credentials missing/expired
- Username prompt with suggested format: `username@domain.local`
- Hidden password prompt showing `domain\username` format
- Handle both `username@domain` and `domain\username` input formats

**Credential Caching:**
- Store in macOS Keychain with TTL metadata
- Check expiry before use, re-prompt if expired
- Support clearing credentials per domain

### 2. Tool Structure Pattern

**Core Tools Required:**
- `vsphere_clear_credentials(hostname)` - Clear cached credentials for domain
- All 15 discovered API tools with automatic credential handling

**Error Handling:**
- Consistent error format with troubleshooting steps
- Handle authentication failures gracefully
- Provide clear next steps for users

### 3. Project Structure (Consistent with Existing Servers)

```
vsphere-mcp-server/
├── src/
│   └── vsphere_mcp_server/
│       ├── __init__.py
│       ├── server.py          # Main MCP server with FastMCP
│       ├── credentials.py     # Domain-based auth management
│       └── vsphere_client.py  # vSphere API client wrapper
├── tests/
├── docs/
├── scripts/
├── pyproject.toml
├── requirements.txt
├── README.md
└── CHANGELOG.md
```

### 4. Dependencies & Configuration

**Core Dependencies:**
- `mcp==1.14.1` (consistent with other servers)
- `requests` for vSphere REST API
- `urllib3` for SSL handling

**Development Dependencies:**
- `pytest==8.3.3`
- `pytest-asyncio==0.24.0`
- `black==24.8.0`
- `isort==5.13.2`

## Implementation Plan

### Phase 1: Core Infrastructure
1. **Project Setup**
   - Create proper Python package structure
   - Set up pyproject.toml with consistent dependencies
   - Create entry points for MCP server

2. **Credential Management**
   - Implement domain extraction from vSphere FQDN
   - Create GUI authentication prompts using osascript
   - Implement keychain storage with TTL
   - Add credential clearing functionality

3. **vSphere Client Wrapper**
   - Create session management class
   - Handle authentication and token refresh
   - Implement SSL verification options
   - Add connection error handling

### Phase 2: Core MCP Tools
1. **Authentication Tools**
   - `vsphere_clear_credentials(hostname)` - Clear domain credentials

2. **VM Management Tools** (4 tools)
   - `list_vms()` - List all VMs with basic info
   - `get_vm_details(vm_id)` - Detailed VM configuration
   - `power_on_vm(vm_id)` - Power on VM
   - `power_off_vm(vm_id)` - Power off VM

3. **Infrastructure Tools** (6 tools)
   - `list_hosts()` - List ESXi hosts
   - `get_host_details(host_id)` - Host details
   - `list_datacenters()` - List datacenters
   - `get_datacenter_details(datacenter_id)` - Datacenter details
   - `list_datastores()` - List datastores with capacity
   - `get_datastore_details(datastore_id)` - Datastore details

### Phase 3: Organization & Networking Tools
1. **Organization Tools** (2 tools)
   - `list_folders()` - List folders by type
   - `get_folder_details(folder_id)` - Folder details

2. **Network Tools** (3 tools)
   - `list_networks()` - List networks with VLAN info
   - `get_network_details(network_id)` - Network details
   - `list_vlans()` - Extract VLAN info from network names

### Phase 4: Testing & Documentation
1. **Unit Tests**
   - Test credential management
   - Test API client wrapper
   - Mock vSphere API responses

2. **Integration Tests**
   - Test against real vSphere environment
   - Validate all 15 tools work correctly

3. **Documentation**
   - Update README with usage examples
   - Document all tools with parameters
   - Add troubleshooting guide

## Key Design Decisions

### 1. Consistent Authentication
- Follow exact pattern from win-mcp-server and ssh-mcp-server
- Domain-based credential caching
- GUI prompts for missing credentials
- 4-hour TTL with expiry checking

### 2. Error Handling
- Consistent error format across all tools
- Provide troubleshooting steps
- Handle network timeouts gracefully
- Clear authentication error messages

### 3. Tool Naming Convention
- Prefix all tools with `vsphere_` (except clear_credentials)
- Use descriptive names: `list_vms`, `get_vm_details`
- Consistent parameter naming: `vm_id`, `host_id`, etc.

### 4. Safety First
- Read-only operations by default
- Only VM power operations are write operations
- No destructive host operations (no maintenance mode)
- Clear warnings for power operations

## Success Criteria

1. **Seamless Authentication**: Users can authenticate once per domain and use all tools
2. **Comprehensive Coverage**: All 15 planned tools work reliably
3. **Consistent UX**: Matches behavior of existing win-mcp-server and ssh-mcp-server
4. **Production Ready**: Proper error handling, logging, and documentation
5. **Secure**: Credentials properly managed with TTL and clearing options

## Total Tools: 16
- 15 vSphere API tools
- 1 credential management tool (`vsphere_clear_credentials`)

This plan ensures the vSphere MCP server will be consistent with your existing MCP servers while providing comprehensive vSphere infrastructure management capabilities.
