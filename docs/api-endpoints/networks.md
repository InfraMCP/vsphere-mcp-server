# Networks API

## List Networks
- **Endpoint**: `GET /rest/vcenter/network`
- **Auth**: Session token
- **Response**: Array of network objects with VLAN information

### Response Format
```json
{
  "value": [
    {
      "name": "v1184-hx02-SYD03-vDOM-WebNMS-FWtoQFX",
      "type": "DISTRIBUTED_PORTGROUP|STANDARD_PORTGROUP",
      "network": "dvportgroup-1115"
    }
  ]
}
```

### Network Types
- **DISTRIBUTED_PORTGROUP**: vSphere Distributed Switch port groups
- **STANDARD_PORTGROUP**: Standard vSwitch port groups

### VLAN Information
Network names often contain VLAN IDs:
- `v1184-*` = VLAN 1184
- `VLAN1320 - *` = VLAN 1320
- Pattern: `v{vlan_id}-{description}` or `VLAN{id} - {description}`

## Get Network Details
- **Endpoint**: `GET /rest/vcenter/network/{network-id}`
- **Auth**: Session token
- **Response**: Detailed network configuration including VLAN settings

## MCP Tool Candidates
- `list_networks()` - List all networks with VLAN info
- `get_network_details(network_id)` - Get detailed network configuration
- `list_vlans()` - Extract and list available VLANs from network names
- `find_networks_by_vlan(vlan_id)` - Find networks for specific VLAN
