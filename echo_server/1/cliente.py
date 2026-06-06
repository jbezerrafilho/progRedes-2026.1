import socket
import config

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg = input('Mensagem: ').encode()
    if msg:
        print(f"Enviando: {msg}")
        my_sock.sendto(msg, (SERVER, PORT))
        answer, source = my_sock.recvfrom(512)
        print(f"Recebido de {source}: {answer}")
    else:
        break
my_sock.close()