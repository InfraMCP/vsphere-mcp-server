# vSphere MCP Server API Documentation

This directory contains documentation for vSphere REST API endpoints discovered during development.

## Structure

- `api-endpoints/` - Individual markdown files for each API endpoint group
- Discovery JSON files from actual vSphere instances

## API Discovery Process

1. Run credential setup: `python scripts/vsphere_credentials.py <host>`
2. Run API discovery: `python scripts/api_discovery.py <host>`
3. Document endpoints in individual markdown files

## Endpoint Categories

Based on vSphere REST API structure:

- **Authentication** - Session management
- **Virtual Machines** - VM lifecycle operations  
- **Hosts** - ESXi host management
- **Clusters** - Cluster operations
- **Datastores** - Storage management
- **Networks** - Network configuration
- **Content Libraries** - Template/ISO management
- **Tasks** - Async operation tracking
