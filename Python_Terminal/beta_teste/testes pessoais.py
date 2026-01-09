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

#banco de dados

import sqlite3
import os

class CommandDatabase:
    def __init__(self, db_name='commands.db'):
        """Inicializa o banco de dados"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()
        self.populate_default_commands()
    
    def connect(self):
        """Conecta ao banco de dados"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def create_table(self):
        """Cria a tabela de comandos se não existir"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT UNIQUE NOT NULL,
                description TEXT,
                module TEXT NOT NULL,
                function TEXT NOT NULL,
                banner_text TEXT,
                active INTEGER DEFAULT 1
            )
        ''')
        self.conn.commit()
    
    def populate_default_commands(self):
        """Popula o banco com os comandos padrão (se ainda não existirem)"""
        default_commands = [
            {
                'command': 'net.IP',
                'description': 'Mostra seu IP local',
                'module': 'network',
                'function': 'get_IP',
                'banner_text': 'YOUR LOCAL IP'
            },
            {
                'command': 'net.INTERFACES',
                'description': 'Lista suas interfaces de rede',
                'module': 'network',
                'function': 'get_INTERFACES',
                'banner_text': 'YOUR NIC\'s'
            },
            {
                'command': 'net.CONNECTIONS',
                'description': 'Mostra suas conexões ativas',
                'module': 'network',
                'function': 'get_PORTS',
                'banner_text': 'YOUR CONNECTIONS'
            },
            {
                'command': 'log.CONNECTIONS',
                'description': 'Mostra logs de conexões',
                'module': 'logs',
                'function': 'get_CONNECTIONS',
                'banner_text': 'YOUR CONNECTIONS LOGS'
            },
            {
                'command': 'help',
                'description': 'Lista todos os comandos disponíveis',
                'module': 'builtin',
                'function': 'show_help',
                'banner_text': 'COMANDOS DISPONÍVEIS'
            },
            {
                'command': 'quit',
                'description': 'Sai do terminal',
                'module': 'builtin',
                'function': 'exit_terminal',
                'banner_text': None
            }
        ]
        
        for cmd in default_commands:
            try:
                self.add_command(**cmd)
            except sqlite3.IntegrityError:
                # Comando já existe, ignora
                pass
    
    def add_command(self, command, description, module, function, banner_text=None, active=1):
        """Adiciona um novo comando ao banco"""
        self.cursor.execute('''
            INSERT INTO commands (command, description, module, function, banner_text, active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (command, description, module, function, banner_text, active))
        self.conn.commit()
    
    def get_command(self, command):
        """Busca um comando específico no banco"""
        self.cursor.execute('''
            SELECT command, description, module, function, banner_text, active
            FROM commands
            WHERE command = ? AND active = 1
        ''', (command,))
        
        result = self.cursor.fetchone()
        if result:
            return {
                'command': result[0],
                'description': result[1],
                'module': result[2],
                'function': result[3],
                'banner_text': result[4],
                'active': result[5]
            }
        return None
    
    def get_all_commands(self):
        """Lista todos os comandos ativos"""
        self.cursor.execute('''
            SELECT command, description, module, function, banner_text
            FROM commands
            WHERE active = 1
            ORDER BY command
        ''')
        
        commands = []
        for row in self.cursor.fetchall():
            commands.append({
                'command': row[0],
                'description': row[1],
                'module': row[2],
                'function': row[3],
                'banner_text': row[4]
            })
        return commands
    
    def update_command(self, command, **kwargs):
        """Atualiza um comando existente"""
        allowed_fields = ['description', 'module', 'function', 'banner_text', 'active']
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                values.append(value)
        
        if updates:
            values.append(command)
            query = f"UPDATE commands SET {', '.join(updates)} WHERE command = ?"
            self.cursor.execute(query, values)
            self.conn.commit()
    
    def delete_command(self, command):
        """Desativa um comando (soft delete)"""
        self.cursor.execute('UPDATE commands SET active = 0 WHERE command = ?', (command,))
        self.conn.commit()
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.conn:
            self.conn.close()