import socket
import os

HOST = ''
PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f'Servidor escutando na porta {PORT}...')

    conn, addr = s.accept()
    with conn:
        print('Conectado por', addr)

        while True:
            filename = conn.recv(1024).decode('utf-8').strip()

            if filename == 'SAIR' or filename == '':
                print('Cliente encerrou a conexao.')
                break

            print(f'Cliente pediu o arquivo: {filename}')

            pasta_server = os.path.join(os.path.dirname(__file__), 'server')
            caminho_arquivo = os.path.join(pasta_server, filename)

            if not os.path.isfile(caminho_arquivo):
                conn.send(b'ERRO\n')
                continue  # volta pro topo do while, espera novo pedido

            with open(caminho_arquivo, 'rb') as f:
                f.seek(0, os.SEEK_END)
                tamanho = f.tell()
                f.seek(0)

                cabecalho = f'OK\n{tamanho}\n'.encode('utf-8')
                conn.send(cabecalho)

                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break

                    enviados = 0
                    while enviados < len(chunk):
                        enviados += conn.send(chunk[enviados:])

            print(f'Arquivo enviado com sucesso ({tamanho} bytes).')