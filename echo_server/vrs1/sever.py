import socket
from config import SERVER, PORT

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_sock.bind((SERVER, PORT))
print(f"Escutando na porta {PORT}")
while True:
    msg, source = my_sock.recvfrom(512)
    print(f"Recebendo {msg} de {source}")
    my_sock.sendto(msg, source)

my_sock.close()