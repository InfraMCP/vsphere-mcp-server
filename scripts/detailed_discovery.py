#!/usr/bin/env python3
"""Detailed vSphere API endpoint discovery"""

import json
from api_discovery import vSphereAPIDiscovery


class DetailedDiscovery(vSphereAPIDiscovery):
    def discover_detailed_endpoints(self):
        """Discover detailed API endpoints."""
        if not self.authenticate():
            return {}

        endpoints = {}
        
        # Core API categories to explore
        api_paths = [
            'vcenter/vm',
            'vcenter/host', 
            'vcenter/cluster',
            'vcenter/datastore',
            'vcenter/network',
            'vcenter/folder',
            'vcenter/datacenter',
            'vcenter/content/library',
            'vcenter/deployment',
            'appliance/system',
            'appliance/networking'
        ]
        
        for path in api_paths:
            try:
                response = self.session.get(f"{self.base_url}/{path}")
                endpoints[path] = {
                    'status': response.status_code,
                    'data': response.json() if response.status_code == 200 else None,
                    'error': response.text if response.status_code != 200 else None
                }
            except Exception as e:
                endpoints[path] = {'error': str(e)}
        
        return endpoints

    def save_detailed_discovery(self):
        """Save detailed discovery results."""
        filename = f"../docs/api-endpoints/{self.host.replace('.', '_')}_detailed.json"
        endpoints = self.discover_detailed_endpoints()
        
        with open(filename, 'w') as f:
            json.dump(endpoints, f, indent=2)
        
        print(f"Detailed discovery saved to {filename}")
        return endpoints


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: detailed_discovery.py <vsphere_host>")
        sys.exit(1)
    
    discovery = DetailedDiscovery(sys.argv[1])
    discovery.save_detailed_discovery()
