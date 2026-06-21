import socket

CLIENT_FILES="client_files/"
SERVER = ("127.0.0.1", 12346)
my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while True:
    file_name = input("Nome do arquivo a baixar: ")
    my_sock.sendto(file_name.encode(), SERVER)

    header, source = my_sock.recvfrom(512)
    if header.startswith(b'OPS'):
        print('Arquivo não existe\n')
    else:
        print('Arquivo baixado com sucesso')
        tamanho = int.from_bytes(header, 'big')
        datagrama = 1
        with open(CLIENT_FILES + file_name, "wb") as fd:
            while tamanho > 0:
                data, _ = my_sock.recvfrom(4096)
                fd.write(data)
                tamanho -= len(data)
                print(f'Recebido datagrama {datagrama}. resta {tamanho}')
                datagrama += 1
        print("\nArquivo recebido com sucesso!\n")




