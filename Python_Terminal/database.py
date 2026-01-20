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
            #network comandos
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
                'command': 'net.HOST_ANALYZER',
                'description': 'analiza e monitora hosts publicos',
                'module': 'imports',
                'function': 'ddos',
                'banner_text': ''
            },
            {
                'command': 'net.WEB_SCANNER',
                'description': 'scanner web basico',
                'module': 'imports',
                'function': 'scanner_web',
                'banner_text': ''
            },
            {
                'command': 'net.NETCAT',
                'description': 'canivete suiço',
                'module': 'imports',
                'function': 'netcat',
                'banner_text': ''
            },
            {
                'command': 'net.SNIFFER',
                'description': 'sniffer basico de icmtp',
                'module': 'imports',
                'function': 'sniffer',
                'banner_text': ''
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
            },
            #calculos comandos
            {
                'command': 'calc.BASKARA',
                'description': 'calcula usando baskara equacoes de 2° grau',
                'module': 'imports',
                'function': 'baskara',
                'banner_text': None
            },
            #string analizer comandos
            {
                'command': 'anal.STRING',
                'description': 'analiza uma string inserida',
                'module': 'imports',
                'function': 'string_analizer',
                'banner_text': None
            },
            #conversor comandos
            {
                'command': 'con.BINARIO',
                'description': 'conversor Binario <=> Decimal',
                'module': 'imports',
                'function': 'c_binario',
                'banner_text': ''
            },
            #sorria
            {
                'command': 'sad',
                'description': 'Lets put a smile on that face.',
                'module': 'imports',
                'function': 'music',
                'banner_text': None
            },
            
            #Game, pedra papel e tesoura
            {
                'command': 'game.JOKENPO',
                'description': 'pedra, papel e tesoura',
                'module': 'imports',
                'function': 'pedra_papel_tesoura',
                'banner_text': 'Jokenpô'
            },
            #ferramentas gerais
            {
                'command': 'tool.PASSWORD',
                'description': 'gerador de senhas',
                'module': 'imports',
                'function': 'senhas',
                'banner_text': ''
            },
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