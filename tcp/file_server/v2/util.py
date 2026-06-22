def send_all(sock, data):
    enviado = 0
    while enviado < len(data):
        enviado += sock.send(data[enviado:])

def save(resource, data_len, sock):
    with open(resource, "wb") as fd:
        received = 0
        while received < data_len:
            data = sock.recv(4096)
            fd.write(data)
            received += len(data)
        print(f"Recebido {received} bytes")

    print("Arquivo recebido com sucesso!\n")
