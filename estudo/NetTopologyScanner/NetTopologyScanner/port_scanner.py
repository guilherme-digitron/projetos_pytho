import nmap
import socket
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PortScanner:
    def __init__(self):
        try:
            self.nm = nmap.PortScanner()
            logger.info("nmap is available for port scanning")
        except Exception as e:
            logger.error(f"nmap not available or permission denied: {e}")
            logger.warning("Port scanning features will be limited")
            self.nm = None
        
    COMMON_PORTS = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        445: 'SMB',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        8080: 'HTTP-Alt',
        8443: 'HTTPS-Alt',
        161: 'SNMP',
        162: 'SNMP-Trap',
        389: 'LDAP',
        636: 'LDAPS',
        1433: 'MSSQL',
        27017: 'MongoDB'
    }
    
    ROUTER_PORTS = [80, 443, 22, 23, 8080, 161, 162]
    FIREWALL_PORTS = [443, 22, 4443, 8443]
    SWITCH_PORTS = [23, 80, 443, 161]
    
    def scan_ports(self, ip: str, ports: str = '1-1024', scan_type: str = 'fast') -> Dict:
        logger.info(f"Scanning ports on {ip} with scan type: {scan_type}")
        result = {
            'ip': ip,
            'open_ports': [],
            'services': [],
            'os_guess': 'Unknown'
        }
        
        if self.nm is None:
            logger.warning(f"nmap not available, using basic socket scan for {ip}")
            common_ports = list(self.COMMON_PORTS.keys())
            result['open_ports'] = self.quick_port_check(ip, common_ports)
            return result
        
        try:
            if scan_type == 'fast':
                self.nm.scan(ip, arguments='-F -T4')
            elif scan_type == 'common':
                port_list = ','.join(map(str, self.COMMON_PORTS.keys()))
                self.nm.scan(ip, port_list, arguments='-sV -T4')
            elif scan_type == 'full':
                logger.info(f"Full scan on {ip} may take several minutes...")
                self.nm.scan(ip, arguments='-p- -sV -O -T4')
            else:
                self.nm.scan(ip, ports, arguments='-T4')
            
            if ip in self.nm.all_hosts():
                host_info = self.nm[ip]
                
                if 'tcp' in host_info:
                    for port in host_info['tcp'].keys():
                        port_info = host_info['tcp'][port]
                        if port_info['state'] == 'open':
                            service_name = port_info.get('name', 'unknown')
                            service_product = port_info.get('product', '')
                            service_version = port_info.get('version', '')
                            
                            result['open_ports'].append(port)
                            
                            service_detail = {
                                'port': port,
                                'service': service_name,
                                'product': service_product,
                                'version': service_version
                            }
                            result['services'].append(service_detail)
                
                if 'osmatch' in host_info and host_info['osmatch']:
                    os_match = host_info['osmatch'][0]
                    result['os_guess'] = os_match.get('name', 'Unknown')
                    result['os_accuracy'] = os_match.get('accuracy', '0')
                    
        except Exception as e:
            logger.error(f"Error scanning {ip}: {e}")
        
        return result
    
    def quick_port_check(self, ip: str, ports: List[int]) -> List[int]:
        open_ports = []
        
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                open_ports.append(port)
                
        return open_ports
    
    def scan_device(self, device: Dict[str, str], scan_type: str = 'common') -> Dict:
        ip = device['ip']
        scan_result = self.scan_ports(ip, scan_type=scan_type)
        
        device.update({
            'open_ports': scan_result['open_ports'],
            'services': scan_result['services'],
            'os_guess': scan_result['os_guess']
        })
        
        return device
