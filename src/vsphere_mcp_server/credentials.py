"""Credential management for vSphere MCP server."""

import json
import os
import platform
import subprocess
import time
from typing import Tuple


class CredentialError(RuntimeError):
    """Raised when credentials cannot be retrieved or managed."""


def extract_domain(hostname: str) -> str:
    """Extract domain from FQDN."""
    parts = hostname.split(".")
    if len(parts) > 2:
        return ".".join(parts[1:])
    return hostname


def get_credentials(hostname: str) -> Tuple[str, str]:
    """Get credentials for vSphere host.

    Resolution order:
    1. VSPHERE_USERNAME / VSPHERE_PASSWORD environment variables (all platforms)
    2. macOS Keychain cache (macOS only)
    3. macOS GUI prompt (macOS only)
    """
    # Env-var override works on any platform (required for WSL / Linux)
    env_user = os.environ.get("VSPHERE_USERNAME")
    env_pass = os.environ.get("VSPHERE_PASSWORD")
    if env_user and env_pass:
        return env_user, env_pass

    _ensure_supported_platform()

    domain = extract_domain(hostname)
    service_name = "vsphere-mcp"

    # Check for existing credentials
    try:
        result = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-s",
                service_name,
                "-a",
                domain,
                "-w",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        stored_data = json.loads(result.stdout.strip())

        # Check if credentials are expired
        if time.time() > stored_data.get("expires_at", 0):
            return _prompt_for_credentials(hostname, domain, service_name)

        return stored_data["username"], stored_data["password"]

    except (
        subprocess.CalledProcessError,
        json.JSONDecodeError,
        KeyError,
        FileNotFoundError,
    ):
        return _prompt_for_credentials(hostname, domain, service_name)


def _prompt_for_credentials(
    hostname: str, domain: str, service_name: str
) -> Tuple[str, str]:
    """Prompt for credentials using macOS GUI."""
    # Username prompt
    username_script = f"""
display dialog "Enter username for vSphere host {hostname}" ¬
    default answer "username@{domain}" ¬
    with title "vSphere Authentication" ¬
    with icon note ¬
    buttons {{"Cancel", "OK"}} ¬
    default button "OK"
"""

    try:
        result = subprocess.run(
            ["osascript", "-e", username_script],
            capture_output=True,
            text=True,
            check=True,
        )

        # Parse username from AppleScript output
        output = result.stdout.strip()
        if "text returned:" in output:
            username = output.split("text returned:")[1].strip()
        else:
            raise ValueError("Failed to parse username from dialog")

    except FileNotFoundError as exc:
        raise CredentialError(
            "macOS osascript is required for GUI authentication"
        ) from exc
    except (subprocess.CalledProcessError, IndexError, ValueError) as exc:
        raise CredentialError("Username input cancelled or failed") from exc

    # Password prompt
    display_username = (
        username.replace("@", "\\\\") if "@" in username else f"{domain}\\\\{username}"
    )
    password_script = f"""
display dialog "Enter password for {display_username}" ¬
    with title "vSphere Authentication" ¬
    with icon note ¬
    default answer "" ¬
    with hidden answer ¬
    buttons {{"Cancel", "OK"}} ¬
    default button "OK"
"""

    try:
        result = subprocess.run(
            ["osascript", "-e", password_script],
            capture_output=True,
            text=True,
            check=True,
        )

        # Parse password from AppleScript output
        output = result.stdout.strip()
        if "text returned:" in output:
            password = output.split("text returned:")[1].strip()
        else:
            raise ValueError("Failed to parse password from dialog")

    except FileNotFoundError as exc:
        raise CredentialError(
            "macOS osascript is required for GUI authentication"
        ) from exc
    except (subprocess.CalledProcessError, IndexError, ValueError) as exc:
        raise CredentialError("Password input cancelled or failed") from exc

    # Normalize username format
    if "@" not in username and "\\" not in username:
        username = f"{username}@{domain}"
    elif "\\" in username:
        username = username.replace("\\", "@")

    # Store credentials with TTL
    expires_at = time.time() + (4 * 60 * 60)  # 4 hours
    credential_data = {
        "username": username,
        "password": password,
        "expires_at": expires_at,
    }

    try:
        subprocess.run(
            [
                "security",
                "add-generic-password",
                "-U",  # Update if exists
                "-s",
                service_name,
                "-a",
                domain,
                "-w",
                json.dumps(credential_data),
            ],
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass  # Continue even if keychain storage fails

    return username, password


def clear_credentials(hostname: str) -> bool:
    """Clear stored credentials for domain."""
    _ensure_supported_platform()
    domain = extract_domain(hostname)
    service_name = "vsphere-mcp"

    try:
        subprocess.run(
            ["security", "delete-generic-password", "-s", service_name, "-a", domain],
            check=True,
            capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def _ensure_supported_platform() -> None:
    """Validate that the current platform supports the keychain/GUI credential flow."""
    if platform.system() != "Darwin":
        raise CredentialError(
            "Credential prompts require macOS Keychain and osascript; "
            "set VSPHERE_USERNAME and VSPHERE_PASSWORD environment variables "
            "to use this server on non-macOS platforms (Linux, WSL, containers)"
        )
