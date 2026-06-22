import socket
import os

HOST = 'localhost'
PORT = 50007


def recv_linha(sock):
    linha = b''
    while True:
        byte = sock.recv(1)
        if byte == b'\n' or byte == b'':
            break
        linha += byte
    return linha.decode('utf-8')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        filename = input('Digite o nome do arquivo (ou "sair" para encerrar): ')

        if filename.lower() == 'sair':
            s.send(b'SAIR')
            print('Conexao encerrada.')
            break

        s.send(filename.encode('utf-8'))

        status = recv_linha(s)

        if status == 'ERRO':
            print('ERRO: arquivo nao encontrado no servidor')
            continue  # volta pro topo do while, pede outro arquivo

        tamanho_str = recv_linha(s)
        tamanho = int(tamanho_str)
        print(f'Tamanho informado pelo servidor: {tamanho} bytes')

        dados_recebidos = b''
        while len(dados_recebidos) < tamanho:
            chunk = s.recv(1024)
            if not chunk:
                break
            dados_recebidos += chunk

        pasta_client = os.path.join(os.path.dirname(__file__), 'client')
        caminho_salvar = os.path.join(pasta_client, 'recebido_' + filename)

        with open(caminho_salvar, 'wb') as f:
            f.write(dados_recebidos)

        print(f'Arquivo salvo em "{caminho_salvar}" ({len(dados_recebidos)} bytes recebidos)')