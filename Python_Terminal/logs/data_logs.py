import psutil

class Logs_DATA:
    def __init__(self) -> None:
        self.network_logs = []
        
    def get_CONNECTIONS(self):
        for i in psutil.net_connections(kind='inet'):
            self.network_logs.append(f"{i}\n")
        return self.network_logs