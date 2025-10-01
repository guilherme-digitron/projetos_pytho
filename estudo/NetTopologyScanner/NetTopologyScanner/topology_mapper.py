from typing import List, Dict
import logging
import socket
import subprocess

logger = logging.getLogger(__name__)


class TopologyMapper:
    def __init__(self):
        self.topology = {}
        
    def trace_route(self, target_ip: str) -> List[str]:
        hops = []
        try:
            if subprocess.call(['which', 'traceroute'], stdout=subprocess.DEVNULL) == 0:
                result = subprocess.run(
                    ['traceroute', '-n', '-m', '10', '-w', '2', target_ip],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                for line in result.stdout.split('\n'):
                    parts = line.split()
                    if len(parts) > 1 and parts[0].replace('.', '').isdigit():
                        for part in parts[1:]:
                            if self._is_valid_ip(part):
                                hops.append(part)
                                break
        except Exception as e:
            logger.error(f"Traceroute error for {target_ip}: {e}")
        
        return hops
    
    def _is_valid_ip(self, ip: str) -> bool:
        try:
            parts = ip.split('.')
            return len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts)
        except:
            return False
    
    def determine_network_layer(self, device: Dict, gateway_ip: str) -> int:
        if device['ip'] == gateway_ip:
            return 1
        
        device_type = device.get('device_type', 'Host').lower()
        
        if device_type == 'router':
            return 1
        elif device_type == 'firewall':
            return 1
        elif device_type == 'switch':
            return 2
        else:
            return 3
    
    def build_topology(self, devices: List[Dict], gateway_ip: str) -> Dict:
        topology = {
            'layers': {
                1: [],
                2: [],
                3: []
            },
            'relationships': [],
            'gateway': gateway_ip
        }
        
        for device in devices:
            layer = self.determine_network_layer(device, gateway_ip)
            device['network_layer'] = layer
            topology['layers'][layer].append(device)
        
        for device in topology['layers'][3]:
            relationship = {
                'from': device['ip'],
                'to': gateway_ip,
                'type': 'connected_to'
            }
            topology['relationships'].append(relationship)
        
        for device in topology['layers'][2]:
            relationship = {
                'from': device['ip'],
                'to': gateway_ip,
                'type': 'managed_by'
            }
            topology['relationships'].append(relationship)
        
        self.topology = topology
        return topology
    
    def get_topology_text(self) -> str:
        if not self.topology:
            return "No topology data available"
        
        text = "NETWORK TOPOLOGY MAP\n"
        text += "=" * 80 + "\n\n"
        
        gateway = self.topology.get('gateway', 'Unknown')
        text += f"Gateway/Default Route: {gateway}\n\n"
        
        text += "Layer 1 - Network Infrastructure (Routers/Firewalls)\n"
        text += "-" * 80 + "\n"
        for device in self.topology['layers'][1]:
            text += f"  [{device['device_type']}] {device['ip']}"
            if device.get('hostname') and device['hostname'] != 'Unknown':
                text += f" ({device['hostname']})"
            if device.get('vendor') and device['vendor'] != 'Unknown':
                text += f" - {device['vendor']}"
            text += "\n"
        text += "\n"
        
        text += "Layer 2 - Network Access (Switches)\n"
        text += "-" * 80 + "\n"
        if self.topology['layers'][2]:
            for device in self.topology['layers'][2]:
                text += f"  [{device['device_type']}] {device['ip']}"
                if device.get('hostname') and device['hostname'] != 'Unknown':
                    text += f" ({device['hostname']})"
                if device.get('vendor') and device['vendor'] != 'Unknown':
                    text += f" - {device['vendor']}"
                text += "\n"
        else:
            text += "  No switches detected\n"
        text += "\n"
        
        text += "Layer 3 - End Devices (Hosts)\n"
        text += "-" * 80 + "\n"
        for device in self.topology['layers'][3]:
            text += f"  [{device['device_type']}] {device['ip']}"
            if device.get('hostname') and device['hostname'] != 'Unknown':
                text += f" ({device['hostname']})"
            if device.get('vendor') and device['vendor'] != 'Unknown':
                text += f" - {device['vendor']}"
            text += "\n"
        
        return text
