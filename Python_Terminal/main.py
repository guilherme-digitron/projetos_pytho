import os
import datetime
import colorama
colorama.init(autoreset=True)

# Importa os módulos
from network import Network_DATA as net_data
from logs import Logs_DATA as logs
from database import CommandDatabase
from imports import Imports

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
            'verde2': colorama.Fore.LIGHTGREEN_EX,
            'reset': colorama.Style.RESET_ALL
        }
        
        # Inicializa o banco de dados
        self.db = CommandDatabase()
        
        # Mapeia os módulos disponíveis
        self.modules = {
            'network': net_data(),
            'logs': logs(),
            'imports': Imports()
        }
          
    def logo(self):
        print(f"{self.colors['verde']}██████╗             ██████╗ ")
        print(f"{self.colors['azul']}██╔══██╗    &       ██╔══██╗")
        print(f"{self.colors['verde2']}██████╔╝  █████╗    ██████╔╝")
        print(f"{self.colors['vermelho']}██╔══██╗  ╚════╝    ██╔══██╗")
        print(f"{self.colors['verde']}██████╔╝            ██████╔╝")
        print(f"{self.colors['verde']}╚═════╝             ╚═════╝ ")
        print()
        print("No dia mais claro, na noite mais densa, o mal sucumbirá ante a minha presença.")
        print("Todo aquele que venera o mal há de penar, quando o poder do B&B enfrentar!")
        print(f"\n{self.colors['ciano']}Digite 'help' para ver os comandos disponíveis{self.colors['reset']}\n")
    
    def banner(self, texto):
        print(f"\n{self.colors['vermelho']}====== {texto} ======\n")
    
    def show_help(self):
        commands = self.db.get_all_commands()
        
        for cmd in commands:
            print(f"{self.colors['ciano']}{cmd['command']:<20}{self.colors['reset']} - {cmd['description']}")
        print()
    
    def execute_command(self, cmd_data):
        """Executa um comando baseado nos dados do banco"""
        module_name = cmd_data['module']
        function_name = cmd_data['function']
        
        # Mostra o banner se houver
        if cmd_data['banner_text']:
            self.banner(cmd_data['banner_text'])
        
        # Comandos built-in
        if module_name == 'builtin':
            if function_name == 'show_help':
                self.show_help()
                return
            elif function_name == 'exit_terminal':
                print(f"{self.colors['verde']}Até logo!{self.colors['reset']}")
                exit()
        
        # Comandos de módulos
        if module_name in self.modules:
            module = self.modules[module_name]
            
            # Verifica se a função existe no módulo
            if hasattr(module, function_name):
                func = getattr(module, function_name)
                result = func()
                
                # Formatação especial para diferentes comandos
                if cmd_data['command'] == 'net.INTERFACES':
                    print(f"".join(result) + "\n")
                
                elif cmd_data['command'] == 'net.IP':
                    print(f"{result}\n")
                
                elif cmd_data['command'] == 'net.CONNECTIONS':
                    for ip, porta, servico, nome_processo, pid in result:
                        print(
                            f"{self.colors['ciano']}IP: {ip} Porta {porta}{self.colors['reset']} | "
                            f"({servico}) | "
                            f"{self.colors['verde']}Processo: {nome_processo} "
                            f"(PID: {pid}){self.colors['reset']}"
                        )
                    print()
                
                elif cmd_data['command'] == 'log.CONNECTIONS':
                    print(f"".join(result) + "\n")
                
                else:
                    # Formato padrão para novos comandos
                    print(result)
                    print()
            else:
                print(f"{self.colors['vermelho']}Erro: Função '{function_name}' não encontrada no módulo '{module_name}'{self.colors['reset']}\n")
        else:
            print(f"{self.colors['vermelho']}Erro: Módulo '{module_name}' não encontrado{self.colors['reset']}\n")
    
    def terminal(self):
        """Loop principal do terminal"""
        try:
            command = input(f"{datetime.datetime.now().strftime('%H:%M:%S')} >> ").strip()
            
            if not command:
                return

            cmd_data = self.db.get_command(command)
            
            if cmd_data:
                self.execute_command(cmd_data)
            else:
                print(f"{self.colors['vermelho']}Comando não reconhecido: '{command}'{self.colors['reset']}")
                print(f"{self.colors['ciano']}Digite 'help' para ver os comandos disponíveis{self.colors['reset']}\n")
        
        except KeyboardInterrupt:
            print(f"\n{self.colors['verde']}Use 'quit' para sair{self.colors['reset']}\n")
        except Exception as e:
            print(f"{self.colors['vermelho']}Erro ao executar comando: {e}{self.colors['reset']}\n")

def main():
    interface = Interface()
    interface.logo()
    
    try:
        while True:
            interface.terminal()
    except KeyboardInterrupt:
        print(f"\n{colorama.Fore.VERDE}Até logo!{colorama.Style.RESET_ALL}")
    finally:
        interface.db.close()

if __name__ == "__main__":
    main()