import socket, threading
import config

SOCKET_RECIEVE_SIZE = 2048

class Socket (threading.Thread):
	def __init__ (self):
		threading.Thread.__init__ (self)
		self.deamon = True
		self.socket = socket.socket()
		self.queue = []
		
		
	def run (self):
		self.socket.connect (( str(config.link['remote_host']), int(config.link['remote_port']) ))
		self.send ( 'SERVER %s %s 0 %s :JStoker IRC Pseudo-Server' % ( config.link['server'], config.link['recvpass'], config.link['sid']) )
		while 1:
			data = self.socket.recv (SOCKET_RECIEVE_SIZE)
			if data == '':
				break

			for line in data.splitlines():
				if line == '':
					break
				words = line.split (' ')
				if words[0] in ['CAPAB']:
					pass # Capability messages. We ignore them, as they're pointless to us.
				
				elif words[0] == 'SERVER':
					if words[2] != config.link['sendpass']:
						print 'Server did NOT send a valid password.'
						self.send ('ERROR :Invalid password')
						raise SystemExit
					self.ssend ('BURST')
					self.send (':%s VERSION :JStoker IRC Pseudo-Server' % config.link['server'])

					self.ssend ('ENDBURST')
				elif words[1] == 'PING':
					self.ssend ('PONG %s' % words[3])
				else:
					self.queue.append (line)
		
	def send (self, data):
		self.socket.send ( str(data) + '\r\n' ) # As I always forget to \r\n otherwise.

	def ssend (self, data):
		self.send (':' + config.link['sid'] + ' ' + str(data))

	def recv (self, amount = 2048):
		if self.queue:
			return self.queue.pop(0)
		else:
			return None
	
	def err (self, err):
		raise SystemExit

if __name__ == '__main__':
	s = Socket ()
	##s.deamon = False
	#s.start()
	s.run()
