import socket

HOST = ""
PORT = 50007
SERVER = "server/"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Servidor escutando na porta {PORT}...')

    conn, addr = s.accept()
    with conn:
        print('Conectado por', addr)

        filename = conn.recv(1024).decode()
        print(f'Cliente pediu o arquivo: {filename}', repr(filename))       
        resource = SERVER + filename

        try:
            with open(resource, 'rb') as f:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break

                    enviados = 0
                    while enviados < len(chunk):
                        enviados += conn.send(chunk[enviados:])
            print('Arquivo enviado com sucesso.')
        except FileNotFoundError:
            msg = "ERRO! Arquivo não existe!"
            print(msg)

           