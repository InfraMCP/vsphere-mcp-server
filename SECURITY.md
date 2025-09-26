# Security Policy

## Supply Chain Security

This project implements several measures to protect against supply chain attacks:

### Dependency Management

- **Pinned Versions**: All dependencies use exact version pins in `requirements.txt` and `pyproject.toml`
- **Dependency Tracking**: Comprehensive dependency reports generated automatically
- **Security Scanning**: Automated vulnerability scanning with Safety and pip-audit
- **Regular Updates**: Weekly automated security checks via GitHub Actions

### Dependency Documentation

- `docs/DEPENDENCIES.md` - Human-readable dependency report
- `docs/dependency-report.json` - Machine-readable dependency data
- Generated automatically by `scripts/generate_dependency_report.py`

### Security Workflow

1. **Before Updates**: Review current dependency report
2. **During Updates**: Update pinned versions in both `requirements.txt` and `pyproject.toml`
3. **After Updates**: Regenerate dependency report and review changes
4. **Continuous**: Monitor security advisories for listed dependencies

### Vulnerability Response

If a security vulnerability is discovered in a dependency:

1. Check `docs/DEPENDENCIES.md` to see if we use the affected package/version
2. If affected, update to a patched version immediately
3. Regenerate dependency report to document the change
4. Test thoroughly before deploying

### Tools

- **Safety**: Checks for known security vulnerabilities
- **pip-audit**: OSV database vulnerability scanning
- **GitHub Dependabot**: Automated dependency updates (if enabled)

### Manual Security Checks

```bash
# Install security tools
pip3 install safety pip-audit

# Check for vulnerabilities
safety check
pip-audit

# Generate fresh dependency report
python3 scripts/generate_dependency_report.py
```

## vSphere Security Considerations

### Authentication Security
- **Credential Storage**: Uses macOS Keychain for secure credential storage
- **Session Management**: Session tokens with automatic cleanup
- **Domain-based Caching**: Credentials organized by domain with TTL
- **GUI Prompts**: TouchID/password authentication for credential access

### Connection Security
- **SSL/TLS**: HTTPS connections to vSphere API endpoints
- **Certificate Handling**: SSL verification disabled for enterprise environments (common practice)
- **Session Tokens**: Short-lived session tokens instead of persistent credentials
- **Connection Timeouts**: Proper timeout and retry logic

### Access Control
- **Read-Only Focus**: Most tools are read-only for safety
- **Explicit Permissions**: Power operations require explicit approval
- **Least Privilege**: Only necessary vSphere permissions required
- **Audit Trail**: All operations logged through MCP framework

### Best Practices
- Use dedicated service accounts with minimal vSphere permissions
- Regularly rotate vSphere credentials
- Monitor vSphere audit logs for unusual activity
- Implement network segmentation for vSphere management
- Use strong passwords and consider multi-factor authentication

### Credential Security
- **No Hardcoded Credentials**: All credentials stored securely in Keychain
- **TTL Enforcement**: 4-hour credential expiry with automatic renewal
- **Domain Isolation**: Credentials isolated by domain for multi-environment support
- **Secure Prompts**: GUI authentication prompts with system integration

## Network Security

### vSphere API Communication
- All communication over HTTPS (port 443)
- Session-based authentication reduces credential exposure
- Proper error handling prevents information leakage
- Connection pooling with secure cleanup

### Enterprise Environment Considerations
- SSL verification disabled by design for self-signed certificates
- Network access should be restricted to management networks
- Consider VPN or bastion host access for remote management
- Implement firewall rules for vSphere API access

## Reporting Security Issues

Please report security vulnerabilities to: rory.mcmahon@vocus.com.au

Do not create public GitHub issues for security vulnerabilities.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Security Checklist

### Before Deployment
- [ ] Review dependency report for vulnerabilities
- [ ] Verify vSphere service account has minimal permissions
- [ ] Confirm network access restrictions are in place
- [ ] Test credential storage and retrieval
- [ ] Validate SSL/TLS configuration

### Regular Maintenance
- [ ] Weekly dependency vulnerability scans
- [ ] Monthly credential rotation
- [ ] Quarterly security review
- [ ] Monitor vSphere audit logs
- [ ] Review access permissions

### Incident Response
1. **Identify**: Monitor for security alerts and unusual activity
2. **Contain**: Disable affected credentials or network access
3. **Investigate**: Review logs and determine scope of impact
4. **Remediate**: Apply patches, rotate credentials, update configurations
5. **Document**: Record lessons learned and update procedures
