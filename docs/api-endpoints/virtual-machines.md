# Virtual Machines API

## List VMs
- **Endpoint**: `GET /rest/vcenter/vm`
- **Auth**: Session token
- **Response**: Array of VM objects

### Response Format
```json
{
  "value": [
    {
      "memory_size_MiB": 8192,
      "vm": "vm-100079",
      "name": "VM-NAME",
      "power_state": "POWERED_ON|POWERED_OFF|SUSPENDED",
      "cpu_count": 4
    }
  ]
}
```

## Get VM Details
- **Endpoint**: `GET /rest/vcenter/vm/{vm-id}`
- **Auth**: Session token
- **Response**: Detailed VM configuration

## VM Power Operations
- **Power On**: `POST /rest/vcenter/vm/{vm-id}/power/start`
- **Power Off**: `POST /rest/vcenter/vm/{vm-id}/power/stop`
- **Reset**: `POST /rest/vcenter/vm/{vm-id}/power/reset`
- **Suspend**: `POST /rest/vcenter/vm/{vm-id}/power/suspend`

## VM Configuration
- **Update VM**: `PATCH /rest/vcenter/vm/{vm-id}`
- **Delete VM**: `DELETE /rest/vcenter/vm/{vm-id}`

## MCP Tool Candidates
- `list_vms()` - List all VMs with basic info
- `get_vm_details(vm_id)` - Get detailed VM configuration
- `power_on_vm(vm_id)` - Power on VM
- `power_off_vm(vm_id)` - Power off VM
- `restart_vm(vm_id)` - Reset VM
