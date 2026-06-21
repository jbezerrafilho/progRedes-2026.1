import socket

CLIENT_FILES="client_files/"
SERVER = ("127.0.0.1", 12346)
my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    file_name = input("Nome do arquivo a baixar: ")
    my_sock.sendto(file_name.encode(), SERVER)
    data, source = my_sock.recvfrom(16384)

    fd = open (CLIENT_FILES+file_name, "wb")
    fd.write(data)
    fd.close()