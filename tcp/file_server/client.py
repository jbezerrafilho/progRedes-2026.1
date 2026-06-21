import socket


HOST = input('Digite a url do servridor de arquivos: ')
PORT = ''
arq = input('Digite o nome do arquivos a ser baixado:')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, 80))

while True:
    sock.send(arq.decode())


