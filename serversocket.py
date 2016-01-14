import socket
import os
import sys
import select

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('0.0.0.0', 30003))

serverSocket.listen(5)

while True:
	incomingSocket, address = serverSocket.accept()
	print('Incoming: {0}'.format(address))

	pid = os.fork()

	if pid == 0:
		# child process

		outSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		outSocket.connect(('www.google.com', 80))

		request = bytearray()
		while True:
			# get request
			incomingSocket.setblocking(0)
			try:
				partial = incomingSocket.recv(1024)
				if partial:
					outSocket.sendall(partial)
				else:
					break
			except socket.error as e:
				if(e.errno != 11):
					sys.exit()

			# get response
			outSocket.setblocking(0)
			try:
				partial = outSocket.recv(1024)
				if partial:
					incomingSocket.sendall(partial)
				else:
					break
			except socket.error as e:
				if(e.errno != 11):
					sys.exit()

			select.select([incomingSocket, outSocket], [], [incomingSocket, outSocket], 1)

		print('Exit: {0}'.format(address))
		sys.exit()