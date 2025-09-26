# Datastores API

## List Datastores
- **Endpoint**: `GET /rest/vcenter/datastore`
- **Auth**: Session token
- **Response**: Array of datastore objects with capacity and usage

### Response Format
```json
{
  "value": [
    {
      "datastore": "datastore-100454",
      "name": "NTNX-local-ds-9HFHH62-A",
      "type": "VMFS|NFS|VSAN",
      "free_space": 19481493504,
      "capacity": 21206401024
    }
  ]
}
```

### Storage Types
- **VMFS**: VMware File System (block storage)
- **NFS**: Network File System
- **VSAN**: VMware vSAN (hyper-converged)

## Get Datastore Details
- **Endpoint**: `GET /rest/vcenter/datastore/{datastore-id}`
- **Auth**: Session token
- **Response**: Detailed datastore configuration and metrics

## MCP Tool Candidates
- `list_datastores()` - List all datastores with capacity info
- `get_datastore_details(datastore_id)` - Get detailed datastore info
- `get_datastore_usage()` - Get storage usage summary across all datastores
