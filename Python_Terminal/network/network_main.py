#todos os modulos de Network

from network import data_network

class Result:
    def __init__(self) -> None:
        pass
    
    def network_ip(self):
        print(data_network.Network_DATA().get_IP())
        return data_network.Network_DATA().get_IP()