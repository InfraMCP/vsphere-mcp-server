# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-09-26

### Added
- Initial release of vSphere MCP Server
- Domain-based credential management with macOS Keychain integration
- 16 comprehensive vSphere management tools:
  - VM management (list, details, power operations)
  - Infrastructure monitoring (hosts, datacenters, datastores)
  - Network discovery with VLAN extraction
  - Organization tools (folders)
  - Credential management
- FastMCP server implementation
- Consistent error handling with troubleshooting guidance
- 4-hour credential TTL with automatic renewal
- SSL verification disabled for enterprise environments
- Session token management with automatic refresh
- Comprehensive documentation and usage examples
- Complete test suite with pytest
- Code quality improvements (pylint score 9.41/10)

### Fixed
- Credential prompting now works correctly for both username and password
- Fixed list object handling in get_vm_details
- Improved datastore capacity calculation with validation
- Added proper error messages for vSphere API limitations

### Working Tools (9/16)
- ✅ list_vms - Complete VM inventory with specs
- ✅ get_vm_details - Detailed VM information including NICs
- ✅ list_hosts - ESXi host inventory
- ✅ list_datacenters - Datacenter information
- ✅ get_datacenter_details - Datacenter details
- ✅ list_datastores - Storage inventory with capacity
- ✅ get_datastore_details - Storage details (with validation)
- ✅ list_networks - Network inventory with VLAN info
- ✅ list_vlans - VLAN extraction and grouping
- ✅ list_folders - Folder organization

### API Limitations (2/16)
- ⚠️ get_network_details - vSphere API doesn't expose distributed portgroup details
- ⚠️ get_folder_details - Folder IDs not accessible via detail endpoint

### Security
- Secure credential storage in macOS Keychain
- Session-based authentication with automatic cleanup
- Domain extraction for credential organization
- TTL-based credential expiry

### Changed
- Removed all domain-specific references from API discovery
- Made codebase completely generic and reusable
- Cleaned git history of sensitive files
