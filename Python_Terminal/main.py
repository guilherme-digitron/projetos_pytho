import os
import datetime
#biblioteca para as cores
import colorama
#seta o autoreset para evitar que a cor vaze, foi o que ela disse
colorama.init(autoreset = True)

#modulos
from network import Network_DATA as net_data
from logs import Logs_DATA as logs

#limpa a tela
os.system('cls' if os.name == 'nt' else 'clear')
    
class Interface:
    def __init__(self) -> None:
        self.colors = {
            
            'vermelho': colorama.Fore.RED,
            'azul': colorama.Fore.BLUE,
            'preto': colorama.Fore.BLACK,
            'verde': colorama.Fore.GREEN,
            'branco': colorama.Fore.WHITE,
            'ciano': colorama.Fore.CYAN,
            'verde2': colorama.Fore.LIGHTGREEN_EX
        }
          
    def logo(self):
        print(f"{self.colors['verde']}██████╗             ██████╗ ")
        print(f"{self.colors['azul']}██╔══██╗    &       ██╔══██╗")
        print(f"{self.colors['verde2']}██████╔╝  █████╗    ██████╔╝")
        print(f"{self.colors['vermelho']}██╔══██╗  ╚════╝    ██╔══██╗")
        print(f"{self.colors['verde']}██████╔╝            ██████╔╝")
        print(f"{self.colors['verde']}╚═════╝             ╚═════╝ ")
        print()
    
    def banner(self, texto):
        print(f"\n{self.colors['vermelho']}====== {texto} ======\n")
    
    def terminal(self):
        command = input(f"{datetime.datetime.now().strftime('%H:%M:%S')} >> ")
        #comandos de redes
        if command == "net.IP":
            self.banner("YOUR LOCAL IP")
            print(f"{net_data().get_IP()}\n")
        if command == "net.INTERFACES":
            self.banner("YOUR NIC's")
            print(f"".join(net_data().get_INTERFACES())+"\n") 
        if command == "net.CONNECTIONS":
            self.banner("YOUR CONNECTIONS")
            for ip, porta, servico, nome_processo, pid in net_data().get_PORTS():
                print(
                    f"{self.colors['ciano']}IP: {ip} Porta {porta} {self.colors['reset']} |"
                    f"({servico}) | "
                    f"{self.colors['verde']}Processo: {nome_processo} "
                    f"(PID: {pid}){self.colors['reset']}"
                )
        #commandos de logs
        if command == "log.CONNECTIONS":
            self.banner("YOUR CONNECTIONS LOGS")
            print(f"".join(logs().get_CONNECTIONS())+"\n")
            
        if command == "quit":
            exit() 


    
def main():
    Interface().logo()
    while True:
        Interface().terminal()

if __name__ == "__main__":
    main()
    