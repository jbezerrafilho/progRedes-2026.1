import socket

my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_sock.connect(('httpbin.org', 80))

my_sock.send(b'GET /image/png HTTP/1.1\r\n'+
             b'Host: httpbin.org\r\n'+
             b'\r\n')

data = my_sock.recv(16384)
my_sock.close()

pos2NL = data.find(b"\r\n\r\n")
headers = data[:pos2NL].split(b'\r\n')
print(f"headers: {headers}")

fd = open('porco.png', 'wb')
fd.write(data[pos2NL+4:])
fd.close()