import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect(('www.google.com', 80))

request = 'GET / HTTP/1.0\n\n'

clientSocket.sendall(request)

buffer = bytearray()
while True:
	partial = clientSocket.recv(1024)
	if partial:
		buffer.extend(partial)
	else:
		break

print(buffer.decode('UTF-8'))