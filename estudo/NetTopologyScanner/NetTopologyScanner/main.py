#!/usr/bin/env python3

import argparse
import sys
import os
import logging
from network_scanner import NetworkScanner
from port_scanner import PortScanner
from device_classifier import DeviceClassifier
from topology_mapper import TopologyMapper
from report_generator import ReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_privileges():
    if os.getpid() != 0:
        logger.warning("Not running with elevated privileges. Some features may not work.")
        print("WARNING: This tool works best with elevated privileges (sudo).")
        print("Some features like ARP scanning and OS detection require root access.")
        print()
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Network Mapping and Topology Discovery Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py                          # Scan local network with default settings
  python main.py --network 192.168.1.0/24 # Scan specific network
  python main.py --scan-type full         # Full port scan (all 65535 ports) with OS detection
  python main.py --use-icmp               # Use both ARP and ICMP for device discovery
  python main.py --no-port-scan           # Skip port scanning (faster)
  
Note: This tool requires elevated privileges (sudo) for full functionality.
        '''
    )
    
    parser.add_argument(
        '--network',
        type=str,
        help='Network to scan in CIDR notation (e.g., 192.168.1.0/24). Auto-detected if not specified.'
    )
    
    parser.add_argument(
        '--scan-type',
        type=str,
        choices=['fast', 'common', 'full'],
        default='common',
        help='Port scan type: fast (top 100 ports), common (common services), full (all 65535 ports + OS detection)'
    )
    
    parser.add_argument(
        '--no-port-scan',
        action='store_true',
        help='Skip port scanning (only do network discovery)'
    )
    
    parser.add_argument(
        '--use-icmp',
        action='store_true',
        help='Use ICMP ping sweep in addition to ARP scan (may require elevated privileges)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print("=" * 80)
    print("NETWORK MAPPING AND TOPOLOGY DISCOVERY TOOL")
    print("=" * 80)
    print()
    
    check_privileges()
    
    logger.info("Initializing network scanner...")
    scanner = NetworkScanner()
    
    logger.info("Getting local network information...")
    network_info = scanner.get_local_network_info()
    
    if not network_info:
        logger.error("Failed to get network information. Are you connected to a network?")
        sys.exit(1)
    
    print(f"Local IP:     {network_info['local_ip']}")
    print(f"Gateway IP:   {network_info['gateway_ip']}")
    print(f"Network CIDR: {network_info['network_cidr']}")
    print(f"Interface:    {network_info['interface']}")
    print()
    
    target_network = args.network if args.network else network_info['network_cidr']
    
    print(f"Scanning network: {target_network}")
    print("This may take a few minutes...")
    print()
    
    logger.info("Starting network discovery...")
    devices = scanner.scan_network(target_network, use_icmp=args.use_icmp)
    
    if not devices:
        logger.warning("No devices found on the network")
        print("\nNo devices found. You may need to run this script with elevated privileges (sudo).")
        sys.exit(0)
    
    print(f"\n✓ Found {len(devices)} devices")
    print()
    
    if not args.no_port_scan:
        logger.info("Starting port scanning and service detection...")
        port_scanner = PortScanner()
        
        if port_scanner.nm is None and args.scan_type == 'full':
            print("\nWARNING: nmap is not available or lacks privileges.")
            print("Full scan mode requires nmap with root privileges for OS detection and service versions.")
            print("Falling back to basic socket-based port scanning.\n")
        
        for i, device in enumerate(devices, 1):
            print(f"Scanning device {i}/{len(devices)}: {device['ip']}", end='\r')
            port_scanner.scan_device(device, scan_type=args.scan_type)
        
        print(f"\n✓ Port scanning completed")
        print()
    
    logger.info("Classifying devices...")
    classifier = DeviceClassifier()
    gateway_ip = network_info['gateway_ip']
    devices = classifier.classify_devices(devices, gateway_ip)
    
    print("✓ Device classification completed")
    print()
    
    logger.info("Building network topology...")
    topology_mapper = TopologyMapper()
    topology = topology_mapper.build_topology(devices, gateway_ip)
    
    print("✓ Network topology mapped")
    print()
    
    logger.info("Generating reports...")
    report_gen = ReportGenerator()
    report_files = report_gen.save_reports(devices, topology, network_info)
    
    print("=" * 80)
    print("SCAN COMPLETE!")
    print("=" * 80)
    print()
    print("Reports generated:")
    print(f"  📄 Text Report:  {report_files['txt']}")
    print(f"  📋 JSON Report:  {report_files['json']}")
    print(f"  🌐 HTML Report:  {report_files['html']}")
    print()
    
    print("QUICK SUMMARY:")
    print("-" * 80)
    device_types = {}
    for device in devices:
        dtype = device.get('device_type', 'Unknown')
        device_types[dtype] = device_types.get(dtype, 0) + 1
    
    for dtype, count in sorted(device_types.items()):
        print(f"  {dtype}: {count}")
    print()
    
    print("View the HTML report in your browser for the best experience!")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\nError: {e}")
        sys.exit(1)
