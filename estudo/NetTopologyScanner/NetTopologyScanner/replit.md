# Network Mapping and Topology Discovery Tool

## Overview
A comprehensive Python-based network scanning and topology mapping tool that discovers devices on a network, identifies device types (routers, switches, firewalls, hosts), performs port scanning and service detection, and generates detailed reports in multiple formats.

## Recent Changes
- 2025-09-29: Initial implementation
  - Created network discovery with ARP and optional ICMP scanning
  - Implemented port scanning with nmap integration and fallback to socket-based scanning
  - Built device classifier to identify network infrastructure devices
  - Added topology mapper with layered network architecture
  - Created multi-format report generator (TXT, JSON, HTML)
  - Added privilege checking and graceful degradation for missing tools

## Project Architecture

### Core Modules
- `network_scanner.py`: Device discovery using ARP and ICMP protocols
- `port_scanner.py`: Port scanning and service detection with nmap
- `device_classifier.py`: Intelligent device classification based on multiple indicators
- `topology_mapper.py`: Network topology mapping with layered architecture
- `report_generator.py`: Multi-format report generation (TXT, JSON, HTML)
- `main.py`: CLI orchestration and user interface

### Key Features
- Network device discovery (ARP scan + optional ICMP ping sweep)
- Port scanning with multiple modes (fast, common, full)
- Device type identification (routers, switches, firewalls, hosts)
- MAC address vendor lookup
- OS fingerprinting (with elevated privileges)
- Service detection and enumeration
- Network topology visualization in text format
- Comprehensive reporting in TXT, JSON, and HTML formats

### Dependencies
- Python 3.11
- scapy: Packet crafting and network scanning
- python-nmap: Port scanning wrapper
- nmap (system): Port scanning and OS detection
- netifaces: Network interface information
- netaddr: IP address manipulation
- tabulate: Formatted text output
- jinja2: HTML report templating
- mac-vendor-lookup: MAC vendor identification

## Usage

### Basic Usage
```bash
python main.py                           # Scan local network
python main.py --network 192.168.1.0/24  # Scan specific network
python main.py --scan-type full          # Full port scan (all ports)
python main.py --use-icmp                # Use ARP + ICMP discovery
python main.py --no-port-scan            # Skip port scanning
```

### Elevated Privileges
For full functionality (ARP scanning, OS detection), run with sudo:
```bash
sudo python main.py
```

### Generated Reports
The tool generates timestamped reports in three formats:
- `network_report_YYYYMMDD_HHMMSS.txt`: Human-readable text report
- `network_report_YYYYMMDD_HHMMSS.json`: Machine-readable JSON data
- `network_report_YYYYMMDD_HHMMSS.html`: Interactive HTML report (recommended)

## Security Considerations
- This tool performs active network scanning which should only be used on networks you own or have permission to scan
- Requires elevated privileges for certain operations
- Use responsibly and in compliance with applicable laws and regulations
