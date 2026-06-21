import socket

SERVER_FILES="server_files/"
my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_sock.bind (('127.0.0.1', 12346))
print("Listen: localhost:12346")

while True:
    # Le do cliente o nome do arquivo
    file_name, source = my_sock.recvfrom(512)
    fd = open (SERVER_FILES+file_name.decode(), "rb")
    data = fd.read()
    fd.close()

    my_sock.sendto(data, source)