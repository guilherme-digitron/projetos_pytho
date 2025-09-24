import requests
import socket

host = input("Digite o IP (ex: 255.255.255.255) ou dominio (ex: google.com): ")

try:
    nome, _,ip = socket.gethostbyaddr(host) 
    print(f"O seu HOST [{host}], direciona para {nome}, com o IP [{ip}]")
    url = f"http://{nome}"
except socket.herror:

    try:
        ip = socket.gethostbyname(host) 
        print(f"O seu HOST [{host}], direciona para o IP [{ip}]")
        url = f"http://{host}"
    except socket.gaierror:
        print(f"ERRO: nao foi possivel resolver o IP {host}")
        exit()

while True:
    try:
        r = requests.get(url)
        print(r.status_code)
    except Exception as e:
        print(f"Erro ao conectar: {e}")