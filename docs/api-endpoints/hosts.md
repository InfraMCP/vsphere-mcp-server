# ESXi Hosts API

## List Hosts
- **Endpoint**: `GET /rest/vcenter/host`
- **Auth**: Session token
- **Response**: Array of ESXi host objects

### Response Format
```json
{
  "value": [
    {
      "host": "host-100453",
      "name": "esx01.company.local",
      "connection_state": "CONNECTED|DISCONNECTED|NOT_RESPONDING",
      "power_state": "POWERED_ON|POWERED_OFF|STANDBY"
    }
  ]
}
```

## Get Host Details
- **Endpoint**: `GET /rest/vcenter/host/{host-id}`
- **Auth**: Session token
- **Response**: Detailed host configuration

## MCP Tool Candidates
- `list_hosts()` - List all ESXi hosts
- `get_host_details(host_id)` - Get detailed host info
