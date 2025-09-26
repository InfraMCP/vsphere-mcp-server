#!/usr/bin/env python3
"""Secure credential management for vSphere connections."""

import getpass
import subprocess
import time
from typing import Optional


def keychain_get_password(service: str, account: str) -> Optional[str]:
    """Get password from macOS Keychain."""
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", service, "-a", account, "-w"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except subprocess.CalledProcessError:
        return None


def keychain_set_password(service: str, account: str, password: str, ttl_hours: int = 4):
    """Store password in macOS Keychain with TTL."""
    # Delete existing entry if present
    subprocess.run(
        ["security", "delete-generic-password", "-s", service, "-a", account],
        capture_output=True,
        check=False,
    )

    # Add new entry
    expiry_time = int(time.time()) + (ttl_hours * 3600)
    subprocess.run([
        "security", "add-generic-password",
        "-s", service, "-a", account, "-w", password,
        "-j", f"Expires: {expiry_time}"
    ], check=True)


def get_vsphere_credentials(host: str) -> tuple[str, str, str]:
    """Get vSphere credentials, prompting if not in keychain."""
    service = f"vsphere-{host}"
    
    # Try to get from keychain
    username = keychain_get_password(service, "username")
    password = keychain_get_password(service, "password")
    
    if not username:
        username = input(f"vSphere username for {host}: ")
        keychain_set_password(service, "username", username)
    
    if not password:
        password = getpass.getpass(f"vSphere password for {username}@{host}: ")
        keychain_set_password(service, "password", password)
    
    return host, username, password


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: vsphere_credentials.py <host>")
        sys.exit(1)
    
    host, username, password = get_vsphere_credentials(sys.argv[1])
    print(f"Credentials stored for {username}@{host}")
