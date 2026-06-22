import socket
import os

HOST = 'localhost'
PORT = 50007

filename = input('Digite o nome do arquivo que deseja baixar: ')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.send(filename.encode('utf-8'))

    dados_recebidos = b''
    while True:
        chunk = s.recv(1024)
        if not chunk:
            break
        dados_recebidos += chunk

if dados_recebidos.startswith(b'ERRO'):
    print(dados_recebidos.decode('utf-8'))
else:
    # pasta "client" que fica do lado do script
    pasta_client = os.path.join(os.path.dirname(__file__), 'client')
    caminho_salvar = os.path.join(pasta_client, 'recebido_' + filename)

    with open(caminho_salvar, 'wb') as f:
        f.write(dados_recebidos)
    print(f'Arquivo salvo em "{caminho_salvar}" ({len(dados_recebidos)} bytes recebidos)')