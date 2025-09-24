from scapy.all import sr1, IP, ICMP, sniff
import threading
import socket

host = input("Digite o IP (ex: 255.255.255.255) ou dominio (ex: google.com): ")
try:
    ip = socket.gethostbyname(host) 
except socket.gaierror:
    print(f"ERRO: nao foi possivel resolver o host {host}")
    exit()

def pacotes():
    sniff(filter = f"icmp and host {ip}",prn = lambda x: x.show(), count = 5)

def ping():
    for i in range(5):
        pacote = IP(dst = ip)/ICMP()
        resposta = sr1(pacote, timeout = 1, verbose = 0)
        if resposta:
            print(f"PING {i+1}: Recebido de {resposta.src}")

sniff_thread = threading.Thread(target=pacotes)
sniff_thread.start()
ping()
sniff_thread.join()

