import socket
from config import *

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"Escutando em {SERVER}:{PORT}")
my_sock.bind((SERVER, PORT))
my_sock.settimeout(1.0)  
clientes = set()

try:
    msg = b''
    while msg != END:
        try:
            msg, source = my_sock.recvfrom(512)
        except socket.timeout:
            continue          
        clientes.add(source)
        print(f"Recebi de {source}: {msg} | {len(clientes)}º")
        for c in clientes:
            if c == source:
                continue
            my_sock.sendto(msg, c)
except KeyboardInterrupt:
    print("\nServidor interrompido (Ctrl+C).")
finally:
    print("Servidor sendo encerrado.")
    my_sock.close()