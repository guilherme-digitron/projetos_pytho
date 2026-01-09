import socket
import sys

host = input("Digite o IP (ex: 255.255.255.255) ou dominio (ex: google.com): ")

try:
    ip = socket.gethostbyname(host) 
except socket.gaierror:
    print(f"ERRO: nao foi possivel resolver o host {host}")
    exit()

print(f"Escaneando o IP {ip}")

for port in range(1, 65535):

    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.05)
        resultado = s.connect_ex((ip, port))
        if resultado == 0:
            print(f"Porta {port} [ABERTA]")
        s.close()

    except socket.error as e:
        print(f"Não foi possivel se conectar com o ip {ip} ERRO: {e}")
        break
print("Escaneamento Completo")