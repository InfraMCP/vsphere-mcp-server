"""vSphere REST API client wrapper."""

import base64
from typing import Dict, Any, Optional

import requests
import urllib3

from .credentials import get_credentials


class VSphereClient:
    """vSphere REST API client with session management."""

    def __init__(self, hostname: str, verify_ssl: bool = False):
        self.hostname = hostname
        self.base_url = f"https://{hostname}/rest"
        self.session = requests.Session()
        self.session_token: Optional[str] = None

        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.session.verify = False

    def authenticate(self) -> None:
        """Authenticate and get session token."""
        username, password = get_credentials(self.hostname)

        # Create basic auth header
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers = {"Authorization": f"Basic {credentials}"}

        try:
            response = self.session.post(
                f"{self.base_url}/com/vmware/cis/session", headers=headers, timeout=30
            )
            response.raise_for_status()

            self.session_token = response.json()["value"]
            self.session.headers.update({"vmware-api-session-id": self.session_token})

        except requests.exceptions.RequestException as e:
            raise Exception(f"Authentication failed: {str(e)}") from e

    def get(self, endpoint: str) -> Dict[str, Any]:
        """Make authenticated GET request."""
        if not self.session_token:
            self.authenticate()

        try:
            response = self.session.get(f"{self.base_url}/{endpoint}", timeout=30)

            if response.status_code == 401:
                # Token expired, re-authenticate
                self.authenticate()
                response = self.session.get(f"{self.base_url}/{endpoint}", timeout=30)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}") from e

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make authenticated POST request."""
        if not self.session_token:
            self.authenticate()

        try:
            response = self.session.post(
                f"{self.base_url}/{endpoint}", json=data, timeout=30
            )

            if response.status_code == 401:
                # Token expired, re-authenticate
                self.authenticate()
                response = self.session.post(
                    f"{self.base_url}/{endpoint}", json=data, timeout=30
                )

            response.raise_for_status()
            return response.json() if response.content else {}

        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}") from e

    def close(self) -> None:
        """Close session and logout."""
        if self.session_token:
            try:
                self.session.delete(f"{self.base_url}/com/vmware/cis/session")
            except requests.exceptions.RequestException:
                pass  # Ignore logout errors
        self.session.close()
