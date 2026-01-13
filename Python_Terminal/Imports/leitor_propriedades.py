#Sim eu refatoro com IA como soube ?
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class AnalisadorString:
    """Analisa características de uma string fornecida pelo usuário"""
    
    def __init__(self):
        self.texto = ""
        self.analises = []
    
    def banner(self):
        """Exibe o banner do analisador"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}    🔍 ANALISADOR DE STRINGS")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    def solicitar_entrada(self):
        """Solicita entrada do usuário"""
        self.texto = input(f"Digite algo para analisar: ")
        return self.texto
    
    def analisar(self):
        """Realiza todas as análises sobre o texto"""
        if not self.texto:
            return None
        
        self.analises = [
            {
                'nome': 'Tipo primitivo',
                'emoji': '🏷️',
                'resultado': type(self.texto).__name__,
                'bool': None
            },
            {
                'nome': 'É somente espaço?',
                'emoji': '⬜',
                'resultado': self.texto.isspace(),
                'bool': True
            },
            {
                'nome': 'É numérico?',
                'emoji': '🔢',
                'resultado': self.texto.isnumeric(),
                'bool': True
            },
            {
                'nome': 'É alfabético?',
                'emoji': '🔤',
                'resultado': self.texto.isalpha(),
                'bool': True
            },
            {
                'nome': 'É alfanumérico?',
                'emoji': '🔡',
                'resultado': self.texto.isalnum(),
                'bool': True
            },
            {
                'nome': 'É maiúsculo?',
                'emoji': '🔠',
                'resultado': self.texto.isupper(),
                'bool': True
            },
            {
                'nome': 'É minúsculo?',
                'emoji': '🔡',
                'resultado': self.texto.islower(),
                'bool': True
            },
            {
                'nome': 'Está capitalizada?',
                'emoji': '📝',
                'resultado': self.texto.istitle(),
                'bool': True
            },
            {
                'nome': 'Comprimento',
                'emoji': '📏',
                'resultado': len(self.texto),
                'bool': None
            }
        ]
        
        return self.analises
    
    def formatar_resultado(self, resultado, is_bool):
        """Formata o resultado com cores apropriadas"""
        if is_bool is None:
            return f"{Fore.CYAN}{resultado}{Style.RESET_ALL}"
        
        if resultado:
            return f"{Fore.GREEN}✓ Sim{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}✗ Não{Style.RESET_ALL}"
    
    def exibir_resultados(self):
        """Exibe os resultados da análise de forma organizada"""
        if not self.analises:
            print(f"{Fore.RED}Nenhuma análise realizada!{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.MAGENTA}📊 RESULTADOS DA ANÁLISE:{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Texto analisado: '{self.texto}'{Style.RESET_ALL}\n")
        
        for analise in self.analises:
            emoji = analise['emoji']
            nome = analise['nome']
            resultado = self.formatar_resultado(analise['resultado'], analise['bool'])
            
            print(f"  {emoji} {nome:<25} {resultado}")
        
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    def executar(self, texto=None):
        """Executa o analisador completo"""
        self.banner()
        
        if texto is None:
            self.solicitar_entrada()
        else:
            self.texto = texto
            print(f"{Fore.GREEN}Analisando: '{texto}'{Style.RESET_ALL}")
        
        self.analisar()
        self.exibir_resultados()
        
        return self.analises


def main():
    """Função principal"""
    analisador = AnalisadorString()
    analisador.executar()
    
    # Opção para analisar outro texto
    while True:
        print(f"{Fore.CYAN}Deseja analisar outro texto? (s/n): {Style.RESET_ALL}", end="")
        opcao = input().lower()
        
        if opcao == 's':
            print()
            analisador.executar()
        else:
            print(f"\n{Fore.GREEN}Até logo! 👋{Style.RESET_ALL}\n")
            break


if __name__ == "__main__":
    main()