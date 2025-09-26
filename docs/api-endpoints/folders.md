# Folders API

## List Folders
- **Endpoint**: `GET /rest/vcenter/folder`
- **Auth**: Session token
- **Response**: Array of folder objects organized by type

### Response Format
```json
{
  "value": [
    {
      "folder": "group-d1",
      "name": "Datacenters",
      "type": "DATACENTER|HOST|NETWORK|DATASTORE|VIRTUAL_MACHINE"
    }
  ]
}
```

### Folder Types
- **DATACENTER**: Datacenter folders
- **HOST**: ESXi host folders
- **NETWORK**: Network folders
- **DATASTORE**: Datastore folders  
- **VIRTUAL_MACHINE**: VM folders (including vCLS, Discovered VMs)

## Get Folder Details
- **Endpoint**: `GET /rest/vcenter/folder/{folder-id}`
- **Auth**: Session token
- **Response**: Detailed folder configuration and contents

## MCP Tool Candidates
- `list_folders()` - List all folders by type
- `get_folder_details(folder_id)` - Get detailed folder info
- `list_vm_folders()` - List only VM folders for organization
