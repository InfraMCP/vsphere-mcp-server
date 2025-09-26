# vSphere Authentication API

## Session Management

### Create Session
- **Endpoint**: `POST /rest/com/vmware/cis/session`
- **Auth**: Basic Auth (username/password)
- **Response**: Session token
- **Usage**: Initial authentication

```json
{
  "value": "session-token-string"
}
```

### Get Session Info
- **Endpoint**: `GET /rest/com/vmware/cis/session`
- **Auth**: Session token
- **Response**: Current session details

### Delete Session
- **Endpoint**: `DELETE /rest/com/vmware/cis/session`
- **Auth**: Session token
- **Response**: 200 OK

## Headers
All authenticated requests require:
```
vmware-api-session-id: <session-token>
```
