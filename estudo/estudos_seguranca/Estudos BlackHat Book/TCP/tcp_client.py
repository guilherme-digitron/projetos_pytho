import socket

target_host = input("Digite o DNS:\n ")
target_port = int(input("Digite a porta para conexão:\n "))

#cria um objeto socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#conectar o cliente
client.connect((target_host, target_port))

#envia alguns dados
client.send(b"GET / HTTP/1.1\nHost: bancocn.com\r\n\r\n")

#recebe alguns dados
response = client.recv(4096)

print(response.decode())
