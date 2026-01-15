import requests
import socket
import time
from urllib.parse import urlparse
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class AnalisadorRede:
    """Analisador de hosts, IPs e status de conexão"""
    
    def __init__(self):
        self.host = None
        self.ip = None
        self.hostname = None
        self.url = None
        self.timeout = 5  # Timeout padrão em segundos
    
    def banner(self):
        """Exibe o banner"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}    ANALISADOR DE REDE E HOST")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def solicitar_host(self):
        """Solicita o host do usuário"""
        print(f"{Fore.GREEN}Digite o IP ou domínio:{Style.RESET_ALL}")
        print(f"  Exemplos: {Fore.CYAN}google.com, 8.8.8.8, github.com{Style.RESET_ALL}")
        
        self.host = input("\nHost: ").strip()
        
        # Remove protocolo se vier com http:// ou https://
        if '://' in self.host:
            parsed = urlparse(self.host)
            self.host = parsed.netloc or parsed.path
        
        return self.host
    
    def verificar_tipo_host(self):
        """
        Verifica se é IP ou domínio
        
        Returns:
            str: 'ip' ou 'domain'
        """
        try:
            # Tenta interpretar como IP
            socket.inet_aton(self.host)
            return 'ip'
        except socket.error:
            return 'domain'
    
    def resolver_host(self):
        """
        Resolve informações do host (IP, hostname)
        
        Returns:
            bool: True se resolveu com sucesso
        """
        tipo = self.verificar_tipo_host()
        
        print(f"\n{Fore.MAGENTA}Analisando host...{Style.RESET_ALL}\n")
        
        try:
            if tipo == 'ip':
                # Se for IP, tenta fazer reverse DNS
                try:
                    hostname, _, ip_list = socket.gethostbyaddr(self.host)
                    self.hostname = hostname
                    self.ip = ip_list[0] if isinstance(ip_list, list) else self.host
                    
                    print(f"  {Fore.GREEN}OK{Style.RESET_ALL} Tipo: {Fore.CYAN}Endereco IP{Style.RESET_ALL}")
                    print(f"  {Fore.GREEN}OK{Style.RESET_ALL} IP: {Fore.YELLOW}{self.ip}{Style.RESET_ALL}")
                    print(f"  {Fore.GREEN}OK{Style.RESET_ALL} Hostname: {Fore.YELLOW}{self.hostname}{Style.RESET_ALL}")
                    
                    self.url = f"http://{self.hostname}"
                
                except socket.herror:
                    # IP válido mas sem reverse DNS
                    self.ip = self.host
                    self.hostname = self.host
                    
                    print(f"  {Fore.GREEN}OK{Style.RESET_ALL} Tipo: {Fore.CYAN}Endereco IP{Style.RESET_ALL}")
                    print(f"  {Fore.GREEN}OK{Style.RESET_ALL} IP: {Fore.YELLOW}{self.ip}{Style.RESET_ALL}")
                    print(f"  {Fore.YELLOW}AVISO{Style.RESET_ALL} Reverse DNS nao disponivel")
                    
                    self.url = f"http://{self.host}"
            
            else:
                # Se for domínio, resolve o IP
                self.ip = socket.gethostbyname(self.host)
                self.hostname = self.host
                
                print(f"  {Fore.GREEN}OK{Style.RESET_ALL} Tipo: {Fore.CYAN}Nome de Dominio{Style.RESET_ALL}")
                print(f"  {Fore.GREEN}OK{Style.RESET_ALL} Dominio: {Fore.YELLOW}{self.hostname}{Style.RESET_ALL}")
                print(f"  {Fore.GREEN}OK{Style.RESET_ALL} IP: {Fore.YELLOW}{self.ip}{Style.RESET_ALL}")
                
                self.url = f"http://{self.host}"
            
            return True
        
        except socket.gaierror:
            print(f"  {Fore.RED}ERRO: Nao foi possivel resolver '{self.host}'{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}Verifique se o dominio esta correto{Style.RESET_ALL}")
            return False
        
        except Exception as e:
            print(f"  {Fore.RED}ERRO inesperado: {e}{Style.RESET_ALL}")
            return False
    
    def verificar_porta(self, porta=80):
        """
        Verifica se uma porta está aberta
        
        Args:
            porta (int): Número da porta
            
        Returns:
            bool: True se está aberta
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            resultado = sock.connect_ex((self.ip, porta))
            sock.close()
            return resultado == 0
        except:
            return False
    
    def testar_http(self, protocolo='http'):
        """
        Testa conexão HTTP/HTTPS
        
        Args:
            protocolo (str): 'http' ou 'https'
            
        Returns:
            dict: Informações da resposta ou None
        """
        url = f"{protocolo}://{self.hostname}"
        
        try:
            resposta = requests.get(url, timeout=self.timeout, allow_redirects=True)
            
            return {
                'sucesso': True,
                'status_code': resposta.status_code,
                'tempo_resposta': resposta.elapsed.total_seconds(),
                'tamanho': len(resposta.content),
                'url_final': resposta.url,
                'headers': dict(resposta.headers)
            }
        
        except requests.exceptions.SSLError:
            return {'sucesso': False, 'erro': 'Erro SSL'}
        except requests.exceptions.Timeout:
            return {'sucesso': False, 'erro': 'Timeout'}
        except requests.exceptions.ConnectionError:
            return {'sucesso': False, 'erro': 'Conexão recusada'}
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}
    
    def analise_completa(self):
        """Realiza análise completa do host"""
        print(f"\n{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}ANALISE COMPLETA{Style.RESET_ALL}\n")
        
        # Testa portas comuns
        portas = {
            80: 'HTTP',
            443: 'HTTPS',
            22: 'SSH',
            21: 'FTP',
            3306: 'MySQL',
            5432: 'PostgreSQL'
        }
        
        print(f"{Fore.YELLOW}Portas abertas:{Style.RESET_ALL}")
        portas_abertas = []
        
        for porta, servico in portas.items():
            if self.verificar_porta(porta):
                print(f"  {Fore.GREEN}OK{Style.RESET_ALL} Porta {porta} ({servico})")
                portas_abertas.append(porta)
            else:
                print(f"  {Fore.RED}FECHADA{Style.RESET_ALL} Porta {porta} ({servico})")
        
        # Testa HTTP e HTTPS
        print(f"\n{Fore.YELLOW}Testes de Conexao:{Style.RESET_ALL}")
        
        for protocolo in ['http', 'https']:
            resultado = self.testar_http(protocolo)
            
            if resultado['sucesso']:
                status = resultado['status_code']
                tempo = resultado['tempo_resposta']
                tamanho = resultado['tamanho']
                
                # Cor baseada no status
                if 200 <= status < 300:
                    cor_status = Fore.GREEN
                elif 300 <= status < 400:
                    cor_status = Fore.YELLOW
                else:
                    cor_status = Fore.RED
                
                print(f"\n  {Fore.GREEN}OK{Style.RESET_ALL} {protocolo.upper()}:")
                print(f"    Status: {cor_status}{status}{Style.RESET_ALL}")
                print(f"    Tempo: {Fore.CYAN}{tempo:.3f}s{Style.RESET_ALL}")
                print(f"    Tamanho: {Fore.CYAN}{tamanho:,} bytes{Style.RESET_ALL}")
                
                if resultado['url_final'] != f"{protocolo}://{self.hostname}":
                    print(f"    Redirect: {Fore.YELLOW}{resultado['url_final']}{Style.RESET_ALL}")
            else:
                print(f"\n  {Fore.RED}ERRO{Style.RESET_ALL} {protocolo.upper()}: {resultado['erro']}")
    
    def monitorar_status(self, intervalo=5, url_especifica=None):
        """
        Monitora o status de um site continuamente
        
        Args:
            intervalo (int): Intervalo entre checagens em segundos
            url_especifica (str): URL específica para monitorar
        """
        url = url_especifica or f"http://{self.hostname}"
        
        print(f"\n{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}MONITORANDO: {url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Pressione Ctrl+C para parar{Style.RESET_ALL}\n")
        
        tentativa = 0
        falhas_consecutivas = 0
        
        try:
            while True:
                tentativa += 1
                timestamp = time.strftime('%H:%M:%S')
                
                try:
                    inicio = time.time()
                    resposta = requests.get(url, timeout=self.timeout)
                    tempo_resposta = time.time() - inicio
                    
                    status = resposta.status_code
                    
                    # Cor baseada no status
                    if 200 <= status < 300:
                        cor = Fore.GREEN
                        simbolo = 'OK'
                        falhas_consecutivas = 0
                    elif 300 <= status < 400:
                        cor = Fore.YELLOW
                        simbolo = 'AVISO'
                        falhas_consecutivas = 0
                    else:
                        cor = Fore.RED
                        simbolo = 'ERRO'
                        falhas_consecutivas += 1
                    
                    print(f"[{timestamp}] {simbolo} Tentativa #{tentativa:03d} | "
                          f"Status: {cor}{status}{Style.RESET_ALL} | "
                          f"Tempo: {Fore.CYAN}{tempo_resposta:.3f}s{Style.RESET_ALL}")
                
                except requests.exceptions.Timeout:
                    falhas_consecutivas += 1
                    print(f"[{timestamp}] {Fore.RED}ERRO Tentativa #{tentativa:03d} | "
                          f"TIMEOUT (>{self.timeout}s){Style.RESET_ALL}")
                
                except requests.exceptions.ConnectionError:
                    falhas_consecutivas += 1
                    print(f"[{timestamp}] {Fore.RED}ERRO Tentativa #{tentativa:03d} | "
                          f"CONEXAO RECUSADA{Style.RESET_ALL}")
                
                except Exception as e:
                    falhas_consecutivas += 1
                    print(f"[{timestamp}] {Fore.RED}ERRO Tentativa #{tentativa:03d} | "
                          f"ERRO: {e}{Style.RESET_ALL}")
                
                # Alerta de múltiplas falhas
                if falhas_consecutivas >= 3:
                    print(f"\n{Fore.RED}ALERTA: {falhas_consecutivas} falhas consecutivas!{Style.RESET_ALL}\n")
                
                time.sleep(intervalo)
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Monitoramento interrompido pelo usuario{Style.RESET_ALL}")
            print(f"Total de tentativas: {tentativa}")
    
    def executar(self):
        """Executa o analisador"""
        self.banner()
        self.solicitar_host()
        
        if not self.resolver_host():
            return
        
        # Menu de opções
        print(f"\n{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Escolha uma opcao:{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}1{Style.RESET_ALL} - Analise completa (portas + HTTP/HTTPS)")
        print(f"  {Fore.YELLOW}2{Style.RESET_ALL} - Monitorar status continuamente")
        print(f"  {Fore.YELLOW}0{Style.RESET_ALL} - Sair")
        
        try:
            opcao = int(input("\nSua escolha: "))
            
            if opcao == 1:
                self.analise_completa()
            elif opcao == 2:
                intervalo = int(input("Intervalo entre checagens (segundos): ") or "5")
                self.monitorar_status(intervalo)
            
        except ValueError:
            print(f"{Fore.RED}Opcao invalida{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operacao cancelada{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}Ate logo!{Style.RESET_ALL}\n")


def main():
    """Função principal"""
    analisador = AnalisadorRede()
    analisador.executar()


if __name__ == "__main__":
    main()