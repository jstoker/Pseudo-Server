import time
current_ts = lambda: int(time.time())

class protocol:
	def init(self, socket):
		self.sock = socket
		self.send = self.sock.push
		self.conf = self.sock.conf

	def connect (self):
		self.send ('PASS %s TS 6 %s' % (self.conf['recvpass'], self.conf['sid']))
		self.send ('CAPAB :QS EX IE KLN UNKLN ENCAP TB SERVICES EUID EOPMOD')
		self.send ('SERVER %s 1 :Pseudo-Server - http://github.com/jstoker/pseudo-server' % self.conf['server'])
	
	def parse (self, message):
		words = message.split(' ')
		if words[0] == 'PING':
			self.send ('PONG %s' % ' '.join(words[1:]))
			self.send ('PING %s' % ' '.join(words[1:]))

	def fini(self):
		pass

