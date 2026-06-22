import socket
from util import send_all, save
import os

SERVER = ("192.168.13.100", 5000)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT = os.path.join(BASE_DIR, "client")

def get_file(sock, filename):
    b_name = filename.encode()
    send_all(sock, len(b_name).to_bytes(2, "big"))
    send_all(sock, b_name)

    header = sock.recv(4)
    data_len = int.from_bytes(header, "big")

    if data_len == 0:
        print("Arquivo não existe\n")
        return
    else:
        resource = os.path.join(CLIENT, filename)
        save(resource, data_len, sock)
   

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(SERVER)
        print(f"Conectado ao servidor {SERVER}")

        while True:
            filename = input("Nome do arquivo a baixar (ou 'sair'): ")
            if filename == "sair":
                break
            get_file(sock, filename)

if __name__ == "__main__":
    main()