import socket
import os

HOST = 'localhost'
PORT = 50007
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT = os.path.join(BASE_DIR, "client")

filename = input('Digite o nome do arquivo que deseja baixar: ')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(filename.encode())

    data = b''
    while True:
        chunk = s.recv(1024)
        if not chunk:
            break
        data += chunk

if data.startswith(b'ERRO!'):
    print(data.decode('utf-8'))
else:
    output = os.path.join(CLIENT, filename)
    with open(output, 'wb') as f:
        f.write(data)
    print(f'Arquivo salvo em "{output}" - {len(data)} bytes recebidos')