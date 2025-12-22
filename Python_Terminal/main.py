from distutils.cmd import Command
import os
import datetime
#biblioteca para as cores
import colorama
#seta o autoreset para evitar que a cor vaze, foi o que ela disse
colorama.init(autoreset = True)

#modulos
from network import network_main

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
    
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def terminal(self):
        self.clear()
        print(f"{self.colors['verde']}██████╗             ██████╗ ")
        print(f"{self.colors['azul']}██╔══██╗    &       ██╔══██╗")
        print(f"{self.colors['verde2']}██████╔╝  █████╗    ██████╔╝")
        print(f"{self.colors['vermelho']}██╔══██╗  ╚════╝    ██╔══██╗")
        print(f"{self.colors['verde']}██████╔╝            ██████╔╝")
        print(f"{self.colors['verde']}╚═════╝             ╚═════╝ ")
        print()
        command = input(f"{datetime.datetime.now().strftime('%H:%M:%S')} >> ")
        return command

    def read(self):
        if self.terminal() == "net.DATA":
            print(network_main.Result().network_ip())

def main():
    Interface().terminal()
    Interface().read()

if __name__ == "__main__":
    main()
    