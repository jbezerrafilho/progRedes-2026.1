import socket
from config import SERVER, PORT

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Escutando em {SERVER}:{PORT}")
my_sock.bind((SERVER, PORT))

while True:
    msg, source = my_sock.recvfrom(512)
    print(f"Recebi/devolvendo a {source}: {msg}")
    my_sock.sendto(msg, source)

my_sock.close()