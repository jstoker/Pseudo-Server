import socket, threading
import config # ssend (server id send)

class Socket (threading.Thread):
	def __init__ (self):
		threading.Thread.__init__(self)
		self.socket = socket.socket()
		self.connected = False

	def connect (self, host, port):
		try:
			self.socket.connect (( str(host), int(port) ))
			self.connected = True
		except:
			self.connected = False
	
	def send (self, data):
		if self.connected:
			self.socket.send (str(data) + '\r\n')
		else:
			return False
	
	def receive (self, amount=2048):
		if self.connected:
			return self.socket.recv (int(amount))
		else:
			return 'Link is not connected.'

	def ssend (self, data):
		if self.connected:
			self.socket.send (':' + str(config.link_sid) + ' ' + str(data) + '\r\n')
		else:
			return False

	def usend (self, uid, data):
		if self.connected:
			self.socket.send (':' + str(config.link_sid) + str(uid) + ' ' + str(data) + '\r\n')
		else:
			return False
