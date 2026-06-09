import socket

my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_sock.connect(('httpbin.org', 80))

my_sock.send(b'GET /image/png HTTP/1.1\r\n'+
             b'Host: httpbin.org\r\n'+
             b'\r\n')

data = my_sock.recv(4096)


pos2NL = data.find(b"\r\n\r\n")
headers = data[:pos2NL].split(b'\r\n')

len_data = -1
for header in headers[1:]:
    header = header.split(b':')
    if header[0] == b'Content-Length':
        len_data = int(header[1])


data = data[pos2NL+4:]
while len(data) < len_data:
    data += my_sock.recv(4096)
my_sock.close()

fd = open('porco.png', 'wb')
fd.write(data)
fd.close()

