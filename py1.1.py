import socket
import threading
import sys


class Server:
	connections = []
	def __init__(self, ServerIp, ServerPort):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((ServerIp, ServerPort))
		sock.listen(1)
		
		while True:
			c, a = sock.accept()
			cThread = threading.Thread(target=self.handler, args=(c, a))
			cThread.daemon = True
			cThread.start()
			self.connections.append(c)
			print(str(a[0]) + ':' + str(a[1]), "connected")
	def handler(self, c, a):
		while True:
			data = c.recv(1024)
			for connection in self.connections:
				print(str(a[0]) + ':' + str(a[1]) + ":- " + str(data, 'utf-8'))
			if not data:
				print(str(a[0]) + ':' + str(a[1]), "disconnected")
				self.connections.remove(c)
				c.close()
				break

class Client:
	def sendMsg(self, sock):
		while True:
			sock.send(bytes(input(""), 'utf-8'))
	def __init__(self, address, ServerPort):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((address, ServerPort))
		iThread = threading.Thread(target=self.sendMsg, args=(sock,))
		iThread.daemon = True
		iThread.start()
		
		while True:
			data = sock.recv(1024)
			if not data:
				break
			print(str(data, 'utf-8'))


print("Enter Server/Client IP Port \n")
tog, ServerIp, ServerPort = input("").split()
ServerPort = int(ServerPort)
if (tog == "Server"):
	server = Server(ServerIp, ServerPort)
elif (tog == 'Client'):
	client = Client(ServerIp, ServerPort)














		

