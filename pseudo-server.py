import asyncore, socket
import time, sys
import modules
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
		self.caps = []
		
		self.protocol = modules.load(conf['protocol'], self)

	def push (self, msg):
		self.sendq += '%s\r\n' % msg
	
	def handle_connect (self):
		print '!!!\tConnecting to %s:%d!' % (self.connectedto)
		if hasattr(self.protocol, 'connect'):
			self.protocol.connect()

	def handle_close (self):
		print '!!!\tClose.'
		modules.unload(self.protocol)
		self.close()
	
	def handle_read (self):
		self.recvq += self.recv(8192)
		for i in xrange(self.recvq.count('\r\n')):
			messages = self.recvq.split('\r\n')
			message = messages.pop(0)
			self.recvq = '\r\n'.join(messages)
			print 'Recv:\t%s' % message
			if message != '':
				self.protocol.parse(message)
	
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
