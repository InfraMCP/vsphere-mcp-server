#!/usr/bin/env python3
"""vSphere API Discovery Script"""

import json
import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from vsphere_credentials import get_vsphere_credentials

disable_warnings(InsecureRequestWarning)


class vSphereAPIDiscovery:
    def __init__(self, host: str):
        self.host, self.username, self.password = get_vsphere_credentials(host)
        self.base_url = f"https://{self.host}/rest"
        self.session = requests.Session()
        self.session.verify = False
        self.token = None

    def authenticate(self) -> bool:
        """Authenticate and get session token."""
        try:
            response = self.session.post(
                f"{self.base_url}/com/vmware/cis/session",
                auth=(self.username, self.password)
            )
            if response.status_code == 200:
                self.token = response.json()['value']
                self.session.headers.update({'vmware-api-session-id': self.token})
                return True
            return False
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False

    def discover_endpoints(self) -> dict:
        """Discover available API endpoints."""
        if not self.authenticate():
            return {}

        endpoints = {}
        
        # Get system version
        try:
            response = self.session.get(f"{self.base_url}/appliance/system/version")
            endpoints['system'] = {
                'version': response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            print(f"Failed to get system info: {e}")

        # Discover services
        try:
            response = self.session.get(f"{self.base_url}")
            if response.status_code == 200:
                endpoints['available_services'] = response.json()
        except Exception as e:
            print(f"Failed to get services: {e}")

        return endpoints

    def save_discovery(self, filename: str = None):
        """Save discovery results to JSON file."""
        if not filename:
            filename = f"../docs/api-endpoints/{self.host.replace('.', '_')}_discovery.json"
        
        endpoints = self.discover_endpoints()
        with open(filename, 'w') as f:
            json.dump(endpoints, f, indent=2)
        
        print(f"Discovery saved to {filename}")
        return endpoints


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: api_discovery.py <vsphere_host>")
        sys.exit(1)
    
    discovery = vSphereAPIDiscovery(sys.argv[1])
    discovery.save_discovery()
