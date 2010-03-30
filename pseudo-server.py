import asyncore, socket
import time, sys
import config


currts = lambda: int(time.time())
class Sock (asyncore.dispatcher):
	def __init__ (self, name="default"):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.name = name
		conf = config.link[name]
		self.connectedto = conf['remote']
		self.connect (self.connectedto)
		self.sid = conf['sid']
		self.conf = conf
		
		self.sendq = ''
		self.recvq = ''

	def push (self, msg):
		self.sendq += ':%s %s\r\n' % (self.sid, msg)
	
	def handle_connect (self):
		print '!!!\tConnecting to %s:%d!' % (self.connectedto)
		
	def handle_close (self):
		print '!!!\tClose.'
		self.close()
	
	def handle_read (self):
		self.recvq += self.recv(8192)
		for i in xrange(self.recvq.count('\r\n')):
			messages = self.recvq.split('\r\n')
			message = messages.pop(0)
			self.recvq = '\r\n'.join(messages)
			print 'Recv:\t%s' % message
			if message != '':
				self.parse(message)
	
	def parse (self, message):
		words = message.split(' ')
		if words[0] == 'CAPAB':
			if words[1] == 'START':
				self.push ('CAPAB %s' % words[1])
			elif words[1] == 'CAPABILITIES':
				if message.find ('PROTOCOL') != -1:
					def getcap (msg, cap):
						cap = msg[msg.find(cap):]
						return cap[:cap.find(' ')]
					caps = []
					caps.append(getcap(message,'PROTOCOL'))   # CAPS that are apparently required.
					caps.append(getcap(message,'IP6SUPPORT'))  # Tested via trial & error.
					self.push ('CAPAB CAPABILITIES :%s' % ' '.join(caps))
			elif words[1] == 'END':
				self.push ('CAPAB END')
				self.push ('SERVER %s %s 0 %s :JStoker\'s Pseudo-Server 0.1.0' % (self.conf['server'], self.conf['recvpass'], self.conf['sid']))

		if words[0] == 'SERVER':
			if words[2] == config.link[self.name]['sendpass']:
				self.remote_sid = words[4]
				self.push ('BURST %s' % currts())
			else:
				self.push ('ERROR :Invalid credentials')
		elif words[1] == 'BURST':
			if words[0][1:] == self.remote_sid:
				self.push ('ENDBURST')
		if words[1] == 'PING':
			self.push ('PONG %s %s' % (words[3], words[2]))
			
	def writable (self):
		return len(self.sendq) > 0
	
	def handle_write (self):
		sent = self.send (self.sendq)
		for line in self.sendq[:sent].split('\r\n'):
			if line is not '':
				print 'Send:\t%s' % line
		self.sendq = self.sendq[sent:]
		
if __name__ == '__main__':
	print 'JStoker\'s Pseudo-Server - Version 0.1.0'
	print
	if len(sys.argv) != 2:
		print 'Usage: %s <name of config block>' % sys.argv[0]
		print 'where <name of config block> is replaced with the name of the config block you wish to connect to.'
		print
	else:
		s = Sock(sys.argv[1])
		asyncore.loop()
	print 'Pseudo-Server will now quit.'
	sys.exit(0)	
