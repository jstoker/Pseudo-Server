import socket, threading
import config
import time # UID ts generation, server die

SOCKET_RECIEVE_SIZE = 4092

class Socket (threading.Thread):
	def __init__ (self):
		threading.Thread.__init__ (self)
		self.deamon = True
		self.socket = socket.socket()
		self.queue = []
		self.ignore_commands = []
		self.handle_commands = []
		self.burst_clients = []
		self.bursted = False
		self.die = False
	
	def addclient (self, uid, nick, host = config.link['server'], ident = 'pseudo-server', modes = 'iIH', gecos = 'Pseudo-Server bot'):
		uuid = config.link ['sid'] + uid
		client = uidd + ' ' + str(int(time.time()))
		if self.bursted: # True if it HAS bursted.
			self.socket.ssend ('UID ' + client)
		else: # Not bursted			
			self.socket.ssend ('UID ' + client)
	
	def run (self):
		self.socket.connect (( str(config.link['remote_host']), int(config.link['remote_port']) ))
		self.send ( 'SERVER %s %s 0 %s :JStoker IRC Pseudo-Server' % ( config.link['server'], config.link['recvpass'], config.link['sid']) )
		while 1:
			if self.die:
				self.send ('ERROR :Dying.')
				time.sleep (5)
				return

			data = self.socket.recv (SOCKET_RECIEVE_SIZE)
			if data == '':
				break
			for line in data.splitlines():
				if line == '':
					break
				words = line.split (' ')

				if not words:
					break
				if len (words) == 1:
					break
		
				if words[0] in self.ignore_commands:
					pass # Capability messages. We ignore them, as they're pointless to us.

				elif words[0] == 'SERVER':
					if words[2] != config.link['sendpass']:
						print 'Server did NOT send a valid password.'
						self.send ('ERROR :Invalid password')
						raise SystemExit

					self.ssend ('BURST')
					self.send (':%s VERSION :JStoker IRC Pseudo-Server' % config.link['server'])
					if self.burst_clients:
						print 'Beginning burst.'
						print 'Heres where you\'d burst.'
						for client in self.burst_clients:
							self.socket.ssend ('UID ' + client)
						print 'Ending burst.'
					# Here's where we should burst the clients.
					self.ssend ('ENDBURST')
					self.bursted = True
				
				elif words[1] == 'PING':
					self.ssend ('PONG %s' % words[3])

				elif words[0] == 'ERROR':
					print
					print 'Remote Server error detected.'
					print ' '.join(words)
					print
					raise SystemExit

				elif words[1] in self.handle_commands:
					self.queue.append (line)
				print words
		
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
