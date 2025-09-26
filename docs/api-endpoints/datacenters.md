# Datacenters API

## List Datacenters
- **Endpoint**: `GET /rest/vcenter/datacenter`
- **Auth**: Session token
- **Response**: Array of datacenter objects

### Response Format
```json
{
  "value": [
    {
      "name": "syd03",
      "datacenter": "datacenter-1001"
    }
  ]
}
```

## Get Datacenter Details
- **Endpoint**: `GET /rest/vcenter/datacenter/{datacenter-id}`
- **Auth**: Session token
- **Response**: Detailed datacenter configuration

## MCP Tool Candidates
- `list_datacenters()` - List all datacenters
- `get_datacenter_details(datacenter_id)` - Get detailed datacenter info
