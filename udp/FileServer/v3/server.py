import socket
import time

SERVER_FILES="server_files/"
my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_sock.bind (('127.0.0.1', 12346))
print('Listen: localhost:12346')

while True:
    file_name, source = my_sock.recvfrom(512)
    try:
        with open(SERVER_FILES + file_name.decode(), "rb") as fd:
            tamanho = fd.seek(0, 2)
            my_sock.sendto(tamanho.to_bytes(4, 'big'), source)
            fd.seek(0)
            while tamanho:
                data = fd.read(4096)
                my_sock.sendto(data, source)
                tamanho -= len(data)
                time.sleep(0.001)
            print("Arquivo enviado com sucesso!")
    except FileNotFoundError:
        msg = 'OPS | Arquivo não existe'.encode()
        my_sock.sendto(msg, source)
        print(msg)
        continue