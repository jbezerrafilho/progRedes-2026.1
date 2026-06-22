import socket
import os

HOST = 'localhost'
PORT = 50007

filename = input('Digite o nome do arquivo que deseja baixar: ')


def recv_linha(sock):
    """Lê do socket byte a byte até encontrar um '\n' (fim do cabeçalho)."""
    linha = b''
    while True:
        byte = sock.recv(1)
        if byte == b'\n' or byte == b'':
            break
        linha += byte
    return linha.decode('utf-8')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.send(filename.encode('utf-8'))

    # 1. lê a primeira linha do cabeçalho: "OK" ou "ERRO"
    status = recv_linha(s)

    if status == 'ERRO':
        print('ERRO: arquivo nao encontrado no servidor')
    else:
        # 2. lê a segunda linha do cabeçalho: o tamanho do arquivo
        tamanho_str = recv_linha(s)
        tamanho = int(tamanho_str)
        print(f'Tamanho informado pelo servidor: {tamanho} bytes')

        # 3. lê exatamente "tamanho" bytes de conteúdo
        dados_recebidos = b''
        while len(dados_recebidos) < tamanho:
            chunk = s.recv(1024)
            if not chunk:
                break  # conexão caiu antes do esperado
            dados_recebidos += chunk

        pasta_client = os.path.join(os.path.dirname(__file__), 'client')
        caminho_salvar = os.path.join(pasta_client, 'recebido_' + filename)

        with open(caminho_salvar, 'wb') as f:
            f.write(dados_recebidos)

        print(f'Arquivo salvo em "{caminho_salvar}" ({len(dados_recebidos)} bytes recebidos)')