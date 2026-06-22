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

        pasta_server = os.path.join(os.path.dirname(__file__), 'server')
        caminho_arquivo = os.path.join(pasta_server, filename)

        if not os.path.isfile(caminho_arquivo):
            # cabeçalho de erro: tamanho 0 sinaliza que não há conteúdo
            conn.send(b'ERRO\n')
        else:
            with open(caminho_arquivo, 'rb') as f:
                # descobre o tamanho usando seek/tell
                f.seek(0, os.SEEK_END)
                tamanho = f.tell()
                f.seek(0)  # volta pro início antes de ler!

                # 1. manda o cabeçalho: "OK" + tamanho + delimitador
                cabecalho = f'OK\n{tamanho}\n'.encode('utf-8')
                conn.send(cabecalho)
                print(f'Enviando cabeçalho: {cabecalho}')

                # 2. manda o conteúdo do arquivo em blocos
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break

                    enviados = 0
                    while enviados < len(chunk):
                        enviados += conn.send(chunk[enviados:])

            print(f'Arquivo enviado com sucesso ({tamanho} bytes).')