import socket
import psutil

class Network_DATA:
    def __init__(self) -> None:
        self.error = ""
        pass
    
    def get_IP(self):
        try:
            # meu socket UDP, tão fofinho
            a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            a.connect(("8.8.8.8", 80))
            ip = a.getsockname()
            a.close()
            return ip
        except Exception:
            self.error = "Erro ao obter endereço IP"
            return self.error
    
    