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

        filename = conn.recv(1024).decode('utf-8').strip()
        print(f'Cliente pediu o arquivo: {filename}')

        # pasta "server" que fica do lado do script
        pasta_server = os.path.join(os.path.dirname(__file__), 'server')
        caminho_arquivo = os.path.join(pasta_server, filename)

        if not os.path.isfile(caminho_arquivo):
            conn.send(b'ERRO: arquivo nao encontrado')
        else:
            with open(caminho_arquivo, 'rb') as f:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break

                    enviados = 0
                    while enviados < len(chunk):
                        enviados += conn.send(chunk[enviados:])

            print('Arquivo enviado com sucesso.')