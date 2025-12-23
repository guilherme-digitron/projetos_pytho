#parte inicial com curses e feita com POO
"""import curses
from curses.textpad import Textbox
    
class Elements:
    
    def __init__(self, x, y, texto,stdscr) -> None:
        self.x = x
        self.y = y
        self.texto = texto
        self.stdscr = stdscr
    
    #formatacao
    
    def centralize_X(self):
        self.x = (curses.COLS//2) - (len(self.texto)//2)
        return self

    def centralize_Y(self):
         self.y = (curses.LINES//2)
         return self
    
    #elementos
    def addstring (self):
        self.stdscr.addstr(self.y, self.x, self.texto)
        
    def addstring_list (self, list_):
        for i in list_:
            self.stdscr.addstr(self.y, self.x, i)
            self.y += 1   
            
    def addinput(self, alt, lar):
        
        #crio a janela para o input e estilizo ela
        my_win = curses.newwin(alt, lar, self.y, self.x)
        my_win.attron(curses.color_pair(1))
        my_win.box()
        my_win.refresh()
        
        #crio o input
        my_input = Textbox(my_win.derwin(1,lar-2,1,1)).edit().strip()
        
        self.stdscr.addstr(10,10,f"{my_input}")

class Menus:
    def __init__(self, stdscr, x, y, y_cursor) -> None:
        self.stdscr = stdscr
        self.x = x
        self.y = y
        self.y_cursor = y_cursor
    
    def home(self):
        
    #logo do jogo
    # Note o \ no começo para ignorar a primeira quebra de linha do código
        logo_bb = [
        "██████╗             ██████╗ ",
        "██╔══██╗    &       ██╔══██╗",
        "██████╔╝  █████╗    ██████╔╝",
        "██╔══██╗  ╚════╝    ██╔══██╗",
        "██████╔╝            ██████╔╝",
        "╚═════╝             ╚═════╝ "
    ]
        #chama os objetos
        Elements(0, 2,logo_bb[1], self.stdscr).centralize_X().addstring_list(logo_bb)
        Elements(0, 9,"9 - Teste", self.stdscr).centralize_X().addstring_list(["1 - Teste","2 - Teste","3 - Teste","4 - Teste","5 - Teste","6 - Teste","7 - Teste","8 - Teste","9 - Teste"])

def main(stdscr):
    #configs
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)
    curses.start_color()
    stdscr.clear()
    
    #Inicia um conjunto de cores
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    #Principal - ondes menus e objetos sao chmados
    stdscr.clear()
    Menus(stdscr,2,5,5).home()
    stdscr.refresh()
    #desenha o input
    stdscr.nodelay(False)
    Elements(curses.COLS//2 - 20, 15,"", stdscr).addinput(3,40) 
    stdscr.refresh()
    stdscr.getch()
    
curses.wrapper(main)
"""

# config de um input estilizado com colorama
"""from datetime import datetime
from colorama import Fore, Style, init

# Inicializa o colorama (importante para Windows, conforme as fontes)
init(autoreset=True) 

# 1. Pega o horário atual formatado (Hora:Minuto:Segundo)
horario_atual = datetime.now().strftime('%H:%M:%S')

# 2. Constrói o prompt
# Fore.GREEN pinta o primeiro '>', Fore.YELLOW pinta o segundo '>'
# O horário é inserido logo depois, e o RESET garante que o texto digitado pelo usuário seja normal
texto_input = input(f"{Fore.GREEN}>{Fore.YELLOW}> {Fore.CYAN}[{horario_atual}]{Style.RESET_ALL} ")

print(f"Você digitou: {texto_input}")
"""

"""#Coletar dados do Network feita pelo gemini 3.5

import socket
import psutil # Biblioteca mencionada na fonte [1] para listar endereços
from colorama import init, Fore, Style

# Inicialização do Colorama
init(autoreset=True)

# Seu dicionário de cores (baseado na nossa conversa anterior)
cores = {
    'titulo': Fore.MAGENTA + Style.BRIGHT,
    'chave': Fore.CYAN,
    'valor': Fore.GREEN,
    'aviso': Fore.YELLOW,
    'reset': Style.RESET_ALL
}

def get_network_info():
    print(f"{cores['titulo']}=== INFORMAÇÕES GERAIS DE REDE ==={cores['reset']}")
    
    # 1. Nome da Máquina (Hostname)
    # A função gethostname retorna o nome da máquina na rede [4]
    hostname = socket.gethostname()
    print(f"{cores['chave']}Hostname:{cores['reset']} {cores['valor']}{hostname}{cores['reset']}")

    # 2. Endereço IP Local (Método simples via Socket)
    # Tenta conectar a um DNS externo para descobrir qual IP a máquina usa para sair [5]
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()
        s.close()
        print(f"{cores['chave']}IP Local (Rota Principal):{cores['reset']} {cores['valor']}{ip_local}{cores['reset']}")
    except Exception as e:
        print(f"{cores['aviso']}Não foi possível determinar IP de rota principal: {e}{cores['reset']}")

    print(f"\n{cores['titulo']}=== DETALHES DAS INTERFACES (NICs) ==={cores['reset']}")
    
    # 3. Iterando sobre as Interfaces com psutil
    # O método net_if_addrs retorna um dicionário com as interfaces e seus endereços [1]
    interfaces = psutil.net_if_addrs()
    
    for nome_interface, enderecos in interfaces.items():
        print(f"\n{cores['chave']}Interface:{cores['reset']} {cores['titulo']}{nome_interface}{cores['reset']}")
        
        for endereco in enderecos:
            # Verifica o tipo de família do endereço (IPv4, IPv6 ou MAC)
            if endereco.family == socket.AF_INET:
                tipo = "IPv4"
                dado = endereco.address
                mascara = endereco.netmask
                print(f"  {cores['chave']}[{tipo}]:{cores['reset']} {cores['valor']}{dado}{cores['reset']} | Máscara: {mascara}")
            
            elif endereco.family == socket.AF_INET6:
                tipo = "IPv6"
                dado = endereco.address
                print(f"  {cores['chave']}[{tipo}]:{cores['reset']} {cores['valor']}{dado}{cores['reset']}")
                
            elif endereco.family == psutil.AF_LINK:
                tipo = "MAC (Físico)"
                dado = endereco.address
                print(f"  {cores['chave']}[{tipo}]:{cores['reset']} {cores['aviso']}{dado}{cores['reset']}")

if __name__ == "__main__":
    get_network_info()

import platform
import subprocess
from colorama import Fore, init

init(autoreset=True)

def info_sistema_bruto():
    sistema = platform.system()
    
    # Define o comando baseado no SO
    if sistema == "Windows":
        comando = "ipconfig /all"
    else:
        comando = "ifconfig" # ou 'ip a' para Linux mais recentes
        
    print(f"{Fore.YELLOW}Executando comando nativo ({comando})...{Fore.RESET}\n")
    
    # Executa o comando e captura a saída
    # O uso de subprocess.run é recomendado para executar comandos do terminal [9], [10]
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    
    print(f"{Fore.GREEN}{resultado.stdout}{Fore.RESET}")

info_sistema_bruto()"""

#Coletar ainda mais informaçao para network com python notebook LM

import socket
import psutil
import subprocess
import platform
import re
from colorama import init, Fore, Style

# Inicializa o colorama
init(autoreset=True)

class NetworkAuditor:
    def __init__(self):
        self.colors = {
            'titulo': Fore.MAGENTA + Style.BRIGHT,
            'chave': Fore.CYAN,
            'valor': Fore.GREEN,
            'aviso': Fore.YELLOW,
            'erro': Fore.RED,
            'reset': Style.RESET_ALL
        }
        self.sistema = platform.system()

    def banner(self, texto):
        print(f"\n{self.colors['titulo']}=== {texto} ==={self.colors['reset']}")

    def get_open_ports(self):
        """
        Lista todas as portas TCP/UDP em estado de escuta (Listening) na máquina.
        Utiliza psutil para verificar conexões do sistema.
        """
        self.banner("PORTAS ABERTAS (LISTENING)")
        try:
            # Pega conexões do tipo INET (IPv4)
            conexoes = psutil.net_connections(kind='inet')
            for conn in conexoes:
                # Filtra apenas serviços que estão ouvindo (Portas abertas)
                if conn.status == 'LISTEN':
                    ip, porta = conn.laddr
                    # Tenta descobrir o nome do serviço (ex: 80 -> http)
                    try:
                        servico = socket.getservbyport(porta)
                    except:
                        servico = "desconhecido"
                    
                    pid = conn.pid
                    nome_processo = psutil.Process(pid).name() if pid else "System"
                    
                    print(f"{self.colors['chave']}Porta {porta}{self.colors['reset']} ({servico}) "
                          f"| {self.colors['valor']}Processo: {nome_processo} (PID: {pid}){self.colors['reset']}")
        except PermissionError:
            print(f"{self.colors['erro']}Erro: Execute como Administrador/Root para ver todos os processos.{self.colors['reset']}")

    def get_gateway_dns(self):
        """
        Obtém Gateway e DNS executando comandos do SO via subprocess.
        """
        self.banner("GATEWAY E DNS")
        
        # O módulo OS/Subprocess permite executar comandos do terminal [2, 3]
        if self.sistema == "Windows":
            comando = "ipconfig /all"
            regex_gateway = r"Gateway Padr.o . . . . . . . . . . . . . : ([0-9.]+)" # Ajuste para PT-BR
            regex_dns = r"Servidores DNS . . . . . . . . . . . . . : ([0-9.]+)"
        else:
            comando = "nmcli dev show" # Comum em distros Linux modernas
            # Alternativa Linux: ler /etc/resolv.conf ou usar 'ip route'
        
        try:
            # Executa o comando e captura a saída [2]
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, errors='ignore')
            saida = resultado.stdout
            
            print(f"{self.colors['aviso']}Nota: Exibindo dados brutos filtrados do sistema:{self.colors['reset']}\n")
            
            # Filtragem simples para Windows (exemplo)
            if self.sistema == "Windows":
                for linha in saida.splitlines():
                    if "Gateway" in linha or "DNS" in linha:
                        print(f"{self.colors['valor']}{linha.strip()}{self.colors['reset']}")
            else:
                # Exibe saída crua no Linux se não tiver regex específico
                print(saida)
                
        except Exception as e:
            print(f"{self.colors['erro']}Não foi possível obter detalhes via comando: {e}{self.colors['reset']}")

    def trace_route(self):
        """
        Realiza um traceroute para um IP externo (ex: Google DNS 8.8.8.8)
        para mostrar a rota da conexão.
        """
        self.banner("ROTA DE CONEXÃO (TRACEROUTE)")
        target = "8.8.8.8"
        
        if self.sistema == "Windows":
            cmd = ["tracert", "-d", target] # -d não resolve nomes (mais rápido)
        else:
            cmd = ["traceroute", "-n", target]

        print(f"{self.colors['aviso']}Mapeando rota para {target}... Isso pode demorar.{self.colors['reset']}")
        
        try:
            # Executa o comando e imprime linha a linha em tempo real
            processo = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            while True:
                linha = processo.stdout.readline()
                if not linha and processo.poll() is not None:
                    break
                if linha:
                    # Pinta os saltos (hops)
                    if any(char.isdigit() for char in linha): 
                        print(f"{self.colors['valor']}{linha.strip()}{self.colors['reset']}")
                    else:
                        print(linha.strip())
        except FileNotFoundError:
            print(f"{self.colors['erro']}Comando de traceroute não encontrado no sistema.{self.colors['reset']}")

if __name__ == "__main__":
    auditor = NetworkAuditor()
    auditor.get_open_ports()
    auditor.get_gateway_dns()
    auditor.trace_route()