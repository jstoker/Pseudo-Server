import time
current_ts = lambda: int(time.time())

class protocol:
	def init(self, socket):
		self.sock = socket
		self.send = self.sock.push
		self.conf = self.sock.conf

	def connect (self):
		self.send ('PASS %s :TS' % (self.conf['pass'], self.conf['sid']))
		self.send ('CAPAB :QS EX DE CHW IE QU DNCR SRV SIGNON')
		self.send ('SERVER %s 1 :Pseudo-Server - http://github.com/jstoker/pseudo-server' % self.conf['server'])
		self.send ('SVINFO 5 3 0 :%d' % current_ts())
	
	def parse (self, message):
		words = message.split(' ')
		if words[0] == 'PING':
			self.send ('PONG %s' % ' '.join(words[1:]))

	def fini(self):
		pass

