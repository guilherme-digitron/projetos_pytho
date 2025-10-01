import json
from datetime import datetime
from typing import List, Dict
from tabulate import tabulate
from jinja2 import Template
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def generate_text_report(self, devices: List[Dict], topology: Dict, network_info: Dict) -> str:
        report = []
        report.append("=" * 100)
        report.append("NETWORK MAPPING AND TOPOLOGY DISCOVERY REPORT")
        report.append("=" * 100)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        report.append("NETWORK INFORMATION")
        report.append("-" * 100)
        report.append(f"Local IP:      {network_info.get('local_ip', 'Unknown')}")
        report.append(f"Gateway IP:    {network_info.get('gateway_ip', 'Unknown')}")
        report.append(f"Network CIDR:  {network_info.get('network_cidr', 'Unknown')}")
        report.append(f"Netmask:       {network_info.get('netmask', 'Unknown')}")
        report.append(f"Interface:     {network_info.get('interface', 'Unknown')}")
        report.append("")
        
        report.append("DISCOVERED DEVICES SUMMARY")
        report.append("-" * 100)
        report.append(f"Total Devices Found: {len(devices)}")
        
        device_types = {}
        for device in devices:
            dtype = device.get('device_type', 'Unknown')
            device_types[dtype] = device_types.get(dtype, 0) + 1
        
        for dtype, count in sorted(device_types.items()):
            report.append(f"  {dtype}: {count}")
        report.append("")
        
        report.append("DETAILED DEVICE INFORMATION")
        report.append("-" * 100)
        
        for device in sorted(devices, key=lambda x: x.get('device_type', 'Host')):
            report.append("")
            report.append(f"Device: {device['ip']}")
            report.append(f"  Type:         {device.get('device_type', 'Unknown')}")
            report.append(f"  MAC Address:  {device.get('mac', 'Unknown')}")
            report.append(f"  Hostname:     {device.get('hostname', 'Unknown')}")
            report.append(f"  Vendor:       {device.get('vendor', 'Unknown')}")
            report.append(f"  OS Guess:     {device.get('os_guess', 'Unknown')}")
            
            open_ports = device.get('open_ports', [])
            if open_ports:
                report.append(f"  Open Ports:   {', '.join(map(str, sorted(open_ports)))}")
            
            services = device.get('services', [])
            if services:
                report.append("  Services:")
                for service in services:
                    svc_line = f"    Port {service['port']}: {service['service']}"
                    if service.get('product'):
                        svc_line += f" ({service['product']}"
                        if service.get('version'):
                            svc_line += f" {service['version']}"
                        svc_line += ")"
                    report.append(svc_line)
        
        report.append("")
        report.append("")
        from topology_mapper import TopologyMapper
        mapper = TopologyMapper()
        mapper.topology = topology
        report.append(mapper.get_topology_text())
        
        report.append("")
        report.append("=" * 100)
        report.append("END OF REPORT")
        report.append("=" * 100)
        
        return "\n".join(report)
    
    def generate_json_report(self, devices: List[Dict], topology: Dict, network_info: Dict) -> str:
        report = {
            'timestamp': datetime.now().isoformat(),
            'network_info': network_info,
            'summary': {
                'total_devices': len(devices),
                'device_types': {}
            },
            'devices': devices,
            'topology': topology
        }
        
        for device in devices:
            dtype = device.get('device_type', 'Unknown')
            report['summary']['device_types'][dtype] = report['summary']['device_types'].get(dtype, 0) + 1
        
        return json.dumps(report, indent=2)
    
    def generate_html_report(self, devices: List[Dict], topology: Dict, network_info: Dict) -> str:
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Network Topology Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
        }
        .info-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        .info-table th, .info-table td {
            padding: 12px;
            text-align: left;
            border: 1px solid #ddd;
        }
        .info-table th {
            background-color: #3498db;
            color: white;
        }
        .info-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .device-card {
            background-color: #fff;
            border: 1px solid #ddd;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        .device-card.router {
            border-left-color: #e74c3c;
        }
        .device-card.switch {
            border-left-color: #f39c12;
        }
        .device-card.firewall {
            border-left-color: #9b59b6;
        }
        .device-title {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .device-info {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 10px;
        }
        .info-item {
            padding: 5px;
        }
        .info-label {
            font-weight: bold;
            color: #555;
        }
        .topology-layer {
            background-color: #ecf0f1;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }
        .summary-box {
            background-color: #e8f4f8;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
        }
        .port-list {
            color: #27ae60;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Network Mapping and Topology Discovery Report</h1>
        <p><strong>Generated:</strong> {{ timestamp }}</p>
        
        <h2>📊 Network Information</h2>
        <table class="info-table">
            <tr><th>Parameter</th><th>Value</th></tr>
            <tr><td>Local IP</td><td>{{ network_info.local_ip }}</td></tr>
            <tr><td>Gateway IP</td><td>{{ network_info.gateway_ip }}</td></tr>
            <tr><td>Network CIDR</td><td>{{ network_info.network_cidr }}</td></tr>
            <tr><td>Netmask</td><td>{{ network_info.netmask }}</td></tr>
            <tr><td>Interface</td><td>{{ network_info.interface }}</td></tr>
        </table>
        
        <h2>📈 Summary</h2>
        <div class="summary-box">
            <p><strong>Total Devices Discovered:</strong> {{ total_devices }}</p>
            <ul>
            {% for dtype, count in device_types.items() %}
                <li><strong>{{ dtype }}:</strong> {{ count }}</li>
            {% endfor %}
            </ul>
        </div>
        
        <h2>🖥️ Discovered Devices</h2>
        {% for device in devices %}
        <div class="device-card {{ device.device_type|lower }}">
            <div class="device-title">
                {{ device.ip }} - {{ device.device_type }}
            </div>
            <div class="device-info">
                <div class="info-item">
                    <span class="info-label">MAC:</span> {{ device.mac }}
                </div>
                <div class="info-item">
                    <span class="info-label">Hostname:</span> {{ device.hostname }}
                </div>
                <div class="info-item">
                    <span class="info-label">Vendor:</span> {{ device.vendor }}
                </div>
                <div class="info-item">
                    <span class="info-label">OS:</span> {{ device.os_guess }}
                </div>
                {% if device.open_ports %}
                <div class="info-item">
                    <span class="info-label">Open Ports:</span> 
                    <span class="port-list">{{ device.open_ports|join(', ') }}</span>
                </div>
                {% endif %}
            </div>
            {% if device.services %}
            <div style="margin-top: 10px;">
                <strong>Services:</strong>
                <ul>
                {% for service in device.services %}
                    <li>Port {{ service.port }}: {{ service.service }}
                    {% if service.product %}({{ service.product }}{% if service.version %} {{ service.version }}{% endif %}){% endif %}
                    </li>
                {% endfor %}
                </ul>
            </div>
            {% endif %}
        </div>
        {% endfor %}
        
        <h2>🗺️ Network Topology</h2>
        
        <div class="topology-layer">
            <h3>Layer 1 - Network Infrastructure</h3>
            {% for device in topology.layers['1'] %}
            <p>• [{{ device.device_type }}] {{ device.ip }} 
               {% if device.hostname != 'Unknown' %}({{ device.hostname }}){% endif %}
               {% if device.vendor != 'Unknown' %}- {{ device.vendor }}{% endif %}
            </p>
            {% endfor %}
        </div>
        
        <div class="topology-layer">
            <h3>Layer 2 - Network Access (Switches)</h3>
            {% if topology.layers['2'] %}
                {% for device in topology.layers['2'] %}
                <p>• [{{ device.device_type }}] {{ device.ip }}
                   {% if device.hostname != 'Unknown' %}({{ device.hostname }}){% endif %}
                   {% if device.vendor != 'Unknown' %}- {{ device.vendor }}{% endif %}
                </p>
                {% endfor %}
            {% else %}
                <p>No switches detected</p>
            {% endif %}
        </div>
        
        <div class="topology-layer">
            <h3>Layer 3 - End Devices</h3>
            {% for device in topology.layers['3'] %}
            <p>• [{{ device.device_type }}] {{ device.ip }}
               {% if device.hostname != 'Unknown' %}({{ device.hostname }}){% endif %}
               {% if device.vendor != 'Unknown' %}- {{ device.vendor }}{% endif %}
            </p>
            {% endfor %}
        </div>
    </div>
</body>
</html>
        """
        
        device_types = {}
        for device in devices:
            dtype = device.get('device_type', 'Unknown')
            device_types[dtype] = device_types.get(dtype, 0) + 1
        
        topology_fixed = {
            'layers': {
                '1': topology['layers'][1],
                '2': topology['layers'][2],
                '3': topology['layers'][3]
            },
            'relationships': topology['relationships'],
            'gateway': topology['gateway']
        }
        
        template = Template(html_template)
        html = template.render(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            network_info=network_info,
            total_devices=len(devices),
            device_types=device_types,
            devices=sorted(devices, key=lambda x: x.get('device_type', 'Host')),
            topology=topology_fixed
        )
        
        return html
    
    def save_reports(self, devices: List[Dict], topology: Dict, network_info: Dict):
        txt_report = self.generate_text_report(devices, topology, network_info)
        json_report = self.generate_json_report(devices, topology, network_info)
        html_report = self.generate_html_report(devices, topology, network_info)
        
        txt_filename = f"network_report_{self.timestamp}.txt"
        json_filename = f"network_report_{self.timestamp}.json"
        html_filename = f"network_report_{self.timestamp}.html"
        
        with open(txt_filename, 'w') as f:
            f.write(txt_report)
        logger.info(f"Text report saved: {txt_filename}")
        
        with open(json_filename, 'w') as f:
            f.write(json_report)
        logger.info(f"JSON report saved: {json_filename}")
        
        with open(html_filename, 'w') as f:
            f.write(html_report)
        logger.info(f"HTML report saved: {html_filename}")
        
        return {
            'txt': txt_filename,
            'json': json_filename,
            'html': html_filename
        }
