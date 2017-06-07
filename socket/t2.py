import socket

HOST = '127.0.0.1'
PORT = 1919
BFSZ = 1024
ADDR = (HOST, PORT)

while True:
	cliSock = socket.create_connection(ADDR)
	data = input('> ').encode('gbk')
	if not data:
		break
	cliSock.send(data + b'\r\n')
	bf = cliSock.recv(BFSZ)
	print(bf.decode('gbk').strip())
	cliSock.close()