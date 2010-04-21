import time
current_ts = lambda: int(time.time())

class protocol:
	def init(self, socket):
		self.sock = socket
		self.send = self.sock.push
		self.conf = self.sock.conf
		self.caps = []

	def connect (self):
		pass
	
	def parse (self, message):
		words = message.split(' ')
		if words[0] == 'CAPAB':
			if words[1] == 'START':
				self.send ('CAPAB %s' % words[1])
			elif words[1] == 'CAPABILITIES':
				def getcap (msg, cap):
					cap = msg[msg.find(cap):]
					return cap[:cap.find(' ')]
				if message.find ('PROTOCOL') != -1:
					self.caps.append(getcap(message,'PROTOCOL'))   # CAPS that are apparently required.
				if message.find ('IP6SUPPORT') != -1:
					self.caps.append(getcap(message,'IP6SUPPORT'))  # Tested via trial & error.
				if len(self.caps) >1:
					self.send ('CAPAB CAPABILITIES :%s' % ' '.join(self.caps))
			elif words[1] == 'END':
				self.send ('CAPAB END')
				self.send ('SERVER %s %s 0 %s :Pseudo-Server - http://github.com/jstoker/pseudo-server' % (self.conf['server'], self.conf['pass'], self.conf['sid']))

		if words[0] == 'SERVER':
			self.remote_sid = words[4]
			self.send ('BURST %s' % currts())
		elif words[1] == 'BURST':
			if words[0][1:] == self.remote_sid:
				self.send ('ENDBURST')
		if words[1] == 'PING':
			self.send ('PONG %s %s' % (words[3], words[2]))

	def fini(self):
		pass
