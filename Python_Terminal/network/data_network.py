from cmath import nan
from concurrent.futures import process
from multiprocessing import connection
import socket
import psutil
import subprocess
import platform

class Network_DATA:
    def __init__(self) -> None:
        #universal
        self.error = ""
        self.system = platform.system()
        #returns
        self.ip = 0
        self.interfaces = []
        self.ports = []
    
    def get_IP(self):
        try:
            # meu socket UDP, tão fofinho
            a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            a.connect(("8.8.8.8", 80))
            ip = a.getsockname()
            a.close()
            self.ip = ip[0]
            return self.ip
        except Exception as erro:
            self.error = f"ERRO [{erro}] ao obter endereço IP..."
            return self.error
        
    def get_INTERFACES(self):
        try:
            for name, addresses in psutil.net_if_addrs().items():
                for address in addresses:
                    if address.family == socket.AF_INET:
                        type_address = 'IPv4'
                        data = address.address
                        mask = address.netmask
                        self.interfaces.append(f"\n Interface:{name}\n Endereço: {type_address ,data}\n Mascara: {mask} \n----------------------------------------------------")
            return self.interfaces
        except 1==1 as erro:
            self.error == f"ERRO [{erro}] ao coletar dados da NIC..."
            return self.error
                        
    def get_PORTS(self):
        try:
            connections = psutil.net_connections(kind='inet')
            for connection in connections:
                if connection.status == 'LISTEN':
                    ip, port = connection.laddr
                    try:
                        service = socket.getservbyport((port))
                    except:
                        service = "unknown"
                        
                    pid = connection.pid
                    process_name = psutil.Process(pid).name() if pid else "System"
                    self.ports.append([ip, port, service, process_name, pid])
            return self.ports
        except Exception as erro:
            self.error = f"ERRO [{erro}] ao verificar conexoes..."
            return self.error
                               
