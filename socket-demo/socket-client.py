import socket


HOST, PORT = "localhost", 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.sendall(b"Hello\n")
print(sock.recv(1024))

sock.sendall(b'quit\n')
print(sock.recv(1024))

# sock.recv(1024)

# print(sock.recv(1024))

