import socket
from config import PORT

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip = input(" IP/nome do servidor: ")

while True:
    msg = input('Mensagem: ').encode()
    if msg:
        print(f"Enviando: {msg}")
        my_sock.sendto(msg, (server_ip, PORT))
        answer, source = my_sock.recvfrom(512)
        print(f"Recebido de {source}: {answer}")
    else:
        break
my_sock.close()