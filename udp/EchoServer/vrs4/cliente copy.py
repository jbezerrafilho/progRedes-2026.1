import socket
from config import *

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_sock.settimeout(1)
try:
    msg = b''
    while msg != END:
        
        msg = input('Mensagem: ').encode()

        if msg == END:
            print(f"Enviando: {msg}")
            my_sock.sendto(msg, (SERVER, PORT))
        else:
            print("Escuta: ")
            answer, source = my_sock.recvfrom(512)
            print(f"Recebido de {source}: {answer}")
    
        if answer == END:
            print("Servidor caiu!!")
            break
except KeyboardInterrupt:
    print(f"\n Interrompido pelo usuário!")
finally:
    print(f"Encerrando meu cliente!")
    my_sock.close()