import socket
from config import PORT

def get_my_ip10():
    return [addr[4][0] for addr in socket.getaddrinfo(socket.gethostname(), 80) if addr[4][0].startswith('192.')]

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_ip = get_my_ip10()[0]
print(f"Escutando em {my_ip}:{PORT}")
my_sock.bind((my_ip, PORT))

msg = b''
while msg != END:
    msg, source = my_sock.recvfrom(512)
    print(f"Recebi/devolvendo a {source}: {msg}")
    my_sock.sendto(msg, source)

my_sock.close()