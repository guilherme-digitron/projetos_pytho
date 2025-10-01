from typing import Dict, List, Optional
import logging
from mac_vendor_lookup import MacLookup

logger = logging.getLogger(__name__)


class DeviceClassifier:
    def __init__(self):
        self.mac_lookup = MacLookup()
        try:
            self.mac_lookup.update_vendors()
            logger.info("MAC vendor database updated successfully")
        except Exception as e:
            logger.warning(f"Failed to update MAC vendor database: {e}. Using cached data.")
        
    ROUTER_INDICATORS = {
        'ports': [80, 443, 22, 23, 8080, 161],
        'services': ['http', 'https', 'ssh', 'telnet', 'snmp'],
        'vendors': ['cisco', 'netgear', 'tp-link', 'linksys', 'asus', 'd-link', 'ubiquiti', 'mikrotik'],
        'os_keywords': ['router', 'ios', 'junos', 'routeros']
    }
    
    SWITCH_INDICATORS = {
        'ports': [23, 80, 443, 161, 22],
        'services': ['telnet', 'http', 'https', 'snmp', 'ssh'],
        'vendors': ['cisco', 'hp', 'dell', 'netgear', 'ubiquiti', '3com', 'juniper'],
        'os_keywords': ['switch', 'catalyst', 'procurve', 'junos']
    }
    
    FIREWALL_INDICATORS = {
        'ports': [443, 22, 4443, 8443, 10443],
        'services': ['https', 'ssh'],
        'vendors': ['fortinet', 'palo alto', 'checkpoint', 'sophos', 'watchguard', 'sonicwall', 'cisco'],
        'os_keywords': ['firewall', 'fortigate', 'palo alto', 'asa', 'pfsense', 'opnsense']
    }
    
    def get_vendor(self, mac: str) -> str:
        try:
            vendor = self.mac_lookup.lookup(mac)
            return vendor
        except:
            return 'Unknown'
    
    def classify_device(self, device: Dict) -> str:
        device_type = 'Host'
        confidence_scores = {
            'router': 0,
            'switch': 0,
            'firewall': 0,
            'host': 0
        }
        
        mac = device.get('mac', '')
        vendor = self.get_vendor(mac) if mac and mac != 'Unknown' else 'Unknown'
        device['vendor'] = vendor
        
        open_ports = device.get('open_ports', [])
        services = [s.get('service', '').lower() for s in device.get('services', [])]
        os_guess = device.get('os_guess', '').lower()
        hostname = device.get('hostname', '').lower()
        
        for port in open_ports:
            if port in self.ROUTER_INDICATORS['ports']:
                confidence_scores['router'] += 1
            if port in self.SWITCH_INDICATORS['ports']:
                confidence_scores['switch'] += 1
            if port in self.FIREWALL_INDICATORS['ports']:
                confidence_scores['firewall'] += 1
        
        for service in services:
            if service in self.ROUTER_INDICATORS['services']:
                confidence_scores['router'] += 1
            if service in self.SWITCH_INDICATORS['services']:
                confidence_scores['switch'] += 1
            if service in self.FIREWALL_INDICATORS['services']:
                confidence_scores['firewall'] += 1
        
        vendor_lower = vendor.lower()
        for router_vendor in self.ROUTER_INDICATORS['vendors']:
            if router_vendor in vendor_lower:
                confidence_scores['router'] += 3
                
        for switch_vendor in self.SWITCH_INDICATORS['vendors']:
            if switch_vendor in vendor_lower:
                confidence_scores['switch'] += 3
                
        for firewall_vendor in self.FIREWALL_INDICATORS['vendors']:
            if firewall_vendor in vendor_lower:
                confidence_scores['firewall'] += 3
        
        combined_text = f"{os_guess} {hostname}"
        for keyword in self.ROUTER_INDICATORS['os_keywords']:
            if keyword in combined_text:
                confidence_scores['router'] += 2
                
        for keyword in self.SWITCH_INDICATORS['os_keywords']:
            if keyword in combined_text:
                confidence_scores['switch'] += 2
                
        for keyword in self.FIREWALL_INDICATORS['os_keywords']:
            if keyword in combined_text:
                confidence_scores['firewall'] += 2
        
        gateway_ip = device.get('is_gateway', False)
        if gateway_ip:
            confidence_scores['router'] += 5
        
        max_score = max(confidence_scores.values())
        
        if max_score > 3:
            for dev_type, score in confidence_scores.items():
                if score == max_score:
                    device_type = dev_type.capitalize()
                    break
        else:
            device_type = 'Host'
        
        device['device_type'] = device_type
        device['confidence_score'] = max_score
        
        logger.info(f"Classified {device['ip']} as {device_type} (confidence: {max_score})")
        
        return device_type
    
    def classify_devices(self, devices: List[Dict], gateway_ip: Optional[str] = None) -> List[Dict]:
        if gateway_ip:
            for device in devices:
                if device['ip'] == gateway_ip:
                    device['is_gateway'] = True
                else:
                    device['is_gateway'] = False
        
        for device in devices:
            self.classify_device(device)
            
        return devices
