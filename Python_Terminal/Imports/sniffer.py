#!/usr/bin/env python3
"""
Ping + ICMP Sniffer Simples
- Envia pings e/ou captura pacotes ICMP relacionados ao alvo
- Requer privilégios de administrador/root para sniff funcionar bem
"""

import argparse
import socket
import threading
import time
from scapy.all import sr1, IP, ICMP, sniff, conf
from colorama import init, Fore, Style

# Inicializa colorama
init(autoreset=True)

# Cores apenas na saída
G = Fore.GREEN + Style.BRIGHT
Y = Fore.YELLOW + Style.BRIGHT
R = Fore.RED + Style.BRIGHT
C = Fore.CYAN + Style.BRIGHT
DIM = Style.DIM
RESET = Style.RESET_ALL

# Desativa mensagens verbosas do Scapy por padrão
conf.verb = 0


def resolver_host(alvo: str) -> str:
    """Converte domínio ou IP para endereço IP"""
    try:
        return socket.gethostbyname(alvo)
    except socket.gaierror:
        raise ValueError(f"Não foi possível resolver o host: {alvo}")


def enviar_ping(ip: str, count: int = 5, timeout: float = 1.0):
    """Envia pacotes ICMP (ping) e mostra resultados"""
    print(f"\n{G}Enviando {count} pings para {ip}...{RESET}\n")
    
    for i in range(1, count + 1):
        try:
            pacote = IP(dst=ip) / ICMP()
            resposta = sr1(pacote, timeout=timeout, verbose=0)
            
            if resposta:
                src = resposta.src
                tempo = resposta.time - pacote.sent_time
                print(f"{G}PING {i:2d}:{RESET} Recebido de {src}  tempo={tempo*1000:.1f}ms")
            else:
                print(f"{Y}PING {i:2d}:{RESET} * Timeout *")
                
            time.sleep(0.5)  # pequeno delay entre pings
            
        except Exception as e:
            print(f"{R}Erro no ping {i}: {e}{RESET}")


def capturar_icmp(ip: str, count: int = 5):
    """Captura pacotes ICMP relacionados ao IP alvo"""
    filtro = f"icmp and host {ip}"
    
    print(f"\n{Y}Iniciando captura de pacotes ICMP (filtro: {filtro}){RESET}")
    print(f"  Aguardando até {count} pacotes ou Ctrl+C para parar...\n")
    
    def mostrar_pacote(pkt):
        if pkt.haslayer(ICMP):
            tipo = pkt[ICMP].type
            codigo = pkt[ICMP].code
            src = pkt[IP].src
            dst = pkt[IP].dst
            
            if tipo == 8:
                msg = "Echo Request"
            elif tipo == 0:
                msg = "Echo Reply"
            elif tipo == 3:
                msg = f"Destination Unreachable (code {codigo})"
            elif tipo == 11:
                msg = f"Time Exceeded (code {codigo})"
            else:
                msg = f"Tipo {tipo} / Código {codigo}"
                
            print(f"{DIM}{src} → {dst} | {msg}{RESET}")
            # pkt.show()  # descomente se quiser ver pacote completo

    try:
        sniff(filter=filtro, prn=mostrar_pacote, count=count, store=0)
    except Exception as e:
        print(f"\n{R}Erro na captura: {e}{RESET}")
        print(f"{Y}Dica: execute o script como administrador/root para sniff funcionar.{RESET}")


def show_menu():
    print(f"\n{C}Ping + ICMP Sniffer{RESET}")
    print("-" * 50)
    print(f" {G}1{Y}  Enviar pings simples")
    print(f" {G}2{Y}  Capturar pacotes ICMP (sniff)")
    print(f" {G}3{Y}  Fazer ping + capturar pacotes ao mesmo tempo")
    print(f" {R}0{Y}  Sair")
    print("-" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Ping e/ou captura de pacotes ICMP",
        epilog="""
Exemplos:
  python icmp_tool.py --target 8.8.8.8 --ping --count 10
  python icmp_tool.py --target google.com --sniff
  python icmp_tool.py --target 192.168.1.1 --both
        """
    )
    parser.add_argument("--target", help="IP ou domínio alvo")
    parser.add_argument("--ping", action="store_true", help="Apenas enviar pings")
    parser.add_argument("--sniff", action="store_true", help="Apenas capturar pacotes ICMP")
    parser.add_argument("--both", action="store_true", help="Ping + captura simultânea")
    parser.add_argument("--count", type=int, default=5, help="Quantidade de pacotes/pings")
    
    args = parser.parse_args()

    # Modo CLI
    if args.target:
        try:
            ip = resolver_host(args.target)
            print(f"{G}Alvo resolvido: {args.target} → {ip}{RESET}\n")
            
            if args.ping or args.both:
                enviar_ping(ip, args.count)
            
            if args.sniff or args.both:
                if args.both:
                    print(f"\n{DIM}Aguardando 1s antes de iniciar captura...{RESET}")
                    time.sleep(1)
                capturar_icmp(ip, args.count)
                
        except ValueError as e:
            print(f"{R}{e}{RESET}")
        except KeyboardInterrupt:
            print(f"\n{Y}Interrompido pelo usuário.{RESET}")
        return

    # Modo interativo
    while True:
        show_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print(f"{Y}Saindo...{RESET}")
            break

        elif opcao in ("1", "2", "3"):
            alvo = input("Digite IP ou domínio (ex: 8.8.8.8 ou google.com): ").strip()
            if not alvo:
                print(f"{R}Alvo obrigatório.{RESET}")
                continue

            try:
                ip = resolver_host(alvo)
                print(f"{G}Alvo resolvido: {alvo} → {ip}{RESET}")
            except ValueError as e:
                print(f"{R}{e}{RESET}")
                continue

            count_str = input("Quantos pacotes/pings? (padrão 5): ").strip()
            count = int(count_str) if count_str.isdigit() else 5

            if opcao == "1":
                enviar_ping(ip, count)
            elif opcao == "2":
                capturar_icmp(ip, count)
            elif opcao == "3":
                sniff_thread = threading.Thread(target=capturar_icmp, args=(ip, count))
                sniff_thread.daemon = True
                sniff_thread.start()
                
                time.sleep(0.8)  # pequena espera para o sniff iniciar
                enviar_ping(ip, count)
                
                sniff_thread.join(timeout=count + 3)

        else:
            print(f"{R}Opção inválida.{RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}Programa interrompido.{RESET}")
    except Exception as e:
        print(f"{R}Erro inesperado: {e}{RESET}")