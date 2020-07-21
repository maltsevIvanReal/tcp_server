import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 4658))
client_sock.sendall(b'1134 1C 19:45:21.999 00\r\n')
data = client_sock.recv(1024)
client_sock.close()
print(data.decode(encoding='utf-8'))
