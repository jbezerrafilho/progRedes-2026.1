import socket
from util import send_all
import os

HOST, PORT = "", 5000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER = os.path.join(BASE_DIR, "server")


def send_file(conn, filename):
    try:
        resource = os.path.join(SERVER, filename)
        with open(resource, "rb") as fd:
            data = fd.read()
            data_len = len(data)
            send_all(conn, data_len.to_bytes(4, "big"))
            send_all(conn, data)
            print(f"Arquivo '{filename}' enviado com sucesso! ({data_len} bytes)")
    except FileNotFoundError:
        send_all(conn, (0).to_bytes(4, "big"))
        print(f"OPS | Arquivo '{filename}' nao existe")


def handle_client(conn, addr):
    print(f"Cliente conectado: {addr}")
    with conn:
        while True:
            header = conn.recv(2)
            if not header:
                break
            name_len = int.from_bytes(header, "big")
            filename = conn.recv(name_len).decode()
            send_file(conn, filename)

    print(f"Cliente desconectado: {addr}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print(f"Listen: {HOST}:{PORT}")

        while True:
            conn, addr = sock.accept()
            handle_client(conn, addr)


if __name__ == "__main__":
    main()