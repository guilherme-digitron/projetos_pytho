import scapy.all as scapy
from scapy.layers.l2 import ARP, Ether
from scapy.layers.inet import IP, ICMP
import netifaces
import netaddr
import socket
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkScanner:
    def __init__(self):
        self.discovered_devices = []
        
    def get_local_network_info(self) -> Dict[str, str]:
        try:
            gateways = netifaces.gateways()
            default_gateway = gateways['default'][netifaces.AF_INET]
            gateway_ip = default_gateway[0]
            interface = default_gateway[1]
            
            addrs = netifaces.ifaddresses(interface)
            ip_info = addrs[netifaces.AF_INET][0]
            local_ip = ip_info['addr']
            netmask = ip_info['netmask']
            
            network = netaddr.IPNetwork(f"{local_ip}/{netmask}")
            cidr = str(network.cidr)
            
            return {
                'local_ip': local_ip,
                'gateway_ip': gateway_ip,
                'netmask': netmask,
                'network_cidr': cidr,
                'interface': interface
            }
        except Exception as e:
            logger.error(f"Error getting network info: {e}")
            return {}
    
    def arp_scan(self, target_network: str) -> List[Dict[str, str]]:
        logger.info(f"Starting ARP scan on {target_network}")
        devices = []
        
        try:
            arp_request = ARP(pdst=target_network)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            
            answered_list = scapy.srp(arp_request_broadcast, timeout=3, verbose=False)[0]
            
            for sent, received in answered_list:
                device = {
                    'ip': received.psrc,
                    'mac': received.hwsrc,
                    'method': 'arp'
                }
                devices.append(device)
                logger.info(f"Found device: {device['ip']} - {device['mac']}")
                
        except Exception as e:
            logger.error(f"Error during ARP scan: {e}")
            
        return devices
    
    def icmp_ping_sweep(self, target_network: str) -> List[Dict[str, str]]:
        logger.info(f"Starting ICMP ping sweep on {target_network}")
        devices = []
        
        try:
            network = netaddr.IPNetwork(target_network)
            
            for ip in network:
                ip_str = str(ip)
                if ip == network.network or ip == network.broadcast:
                    continue
                    
                try:
                    icmp_request = IP(dst=ip_str) / ICMP()
                    response = scapy.sr1(icmp_request, timeout=1, verbose=False)
                    
                    if response:
                        device = {
                            'ip': ip_str,
                            'mac': 'Unknown',
                            'method': 'icmp'
                        }
                        devices.append(device)
                        logger.info(f"ICMP response from: {ip_str}")
                except Exception as e:
                    pass
                    
        except Exception as e:
            logger.error(f"Error during ICMP sweep: {e}")
            
        return devices
    
    def get_hostname(self, ip: str) -> Optional[str]:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return None
    
    def merge_device_lists(self, *device_lists) -> List[Dict[str, str]]:
        merged = {}
        
        for device_list in device_lists:
            for device in device_list:
                ip = device['ip']
                if ip not in merged:
                    merged[ip] = device
                else:
                    if device.get('mac') and device['mac'] != 'Unknown':
                        merged[ip]['mac'] = device['mac']
                        
        return list(merged.values())
    
    def scan_network(self, target_network: Optional[str] = None, use_icmp: bool = False) -> List[Dict[str, str]]:
        if not target_network:
            network_info = self.get_local_network_info()
            target_network = network_info.get('network_cidr')
            
            if not target_network:
                logger.error("Could not determine network CIDR")
                return []
        
        logger.info(f"Scanning network: {target_network}")
        
        arp_devices = self.arp_scan(target_network)
        
        if use_icmp:
            icmp_devices = self.icmp_ping_sweep(target_network)
            all_devices = self.merge_device_lists(arp_devices, icmp_devices)
        else:
            all_devices = self.merge_device_lists(arp_devices)
        
        for device in all_devices:
            hostname = self.get_hostname(device['ip'])
            device['hostname'] = hostname if hostname else 'Unknown'
        
        self.discovered_devices = all_devices
        return all_devices
