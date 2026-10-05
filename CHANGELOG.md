# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-10-05

### Added
- Environment-variable authentication via `VSPHERE_USERNAME` / `VSPHERE_PASSWORD`,
  enabling the server to run on Linux, WSL, and containers (not just macOS). The
  macOS Keychain path is unchanged and still used when env vars are absent (#6).

### Fixed
- Credential-layer errors (`FileNotFoundError` from a missing `security` binary,
  `RuntimeError` from a cancelled prompt) are now normalized to `CredentialError`
  and handled by `authenticate()` instead of crashing (#6).
- `list_datastores()` no longer raises `TypeError` when vSphere returns null
  capacity/free-space values (#6).
- `get_vm_details()` now resolves VMs whose name begins with `vm-` instead of
  mistaking the name for a managed-object ID and returning a 404 (#6).

### Security
- Bumped `mcp` 1.14.1 → 1.28.1: WebSocket Host/Origin validation
  (GHSA-vj7q-gjh5-988w), HTTP transport principal verification
  (GHSA-jpw9-pfvf-9f58), DNS rebinding (GHSA-9h52-p55h-vw2f).
- Bumped `urllib3` 2.5.0 → 2.8.0: cross-origin header leak on proxied redirects
  (GHSA-qccp-gfcp-xxvc) and multiple decompression-bomb bypasses.
- Bumped `requests` 2.32.5 → 2.33.0: insecure temp-file reuse (GHSA-gc5v-m9x4-r6x2).
- Bumped dev tooling for advisories: `pytest` 8.3.3 → 9.0.3 (CVE-2025-71176),
  `black` 24.8.0 → 26.3.1 (CVE-2026-32274), `pytest-asyncio` 0.24.0 → 1.4.0.

## [0.1.1] - 2025-10-06

### Changed
- Dependency and packaging maintenance release.

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
