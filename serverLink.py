import sock
import threading
import time # Timestamp generation.
import config

class serverLink (threading.Thread):
	def __init__ (self):
		threading.Thread.__init__(self)
		self.daemon = False
		self.sock = sock.Socket()
		self.sock.start()
		self.commands = serverCommands (self.sock)

	def run (self):
		try:
			while 1:
				r = self.sock.recv()
				if r:
					r = r.split (' ')
					print r
				else:
					time.sleep (.1)
		except KeyboardInterrupt:
			self.sock.die = True
			print 'Dying...'
			while self.sock.is_alive():
				pass
			print 'Socket successfully closed.'
			
			return

class serverCommands:
	def __init__ (self, sock):
		self.sock = sock
	
	def ADD_UID (self, uid, nick, host=config.link['server'], ident='pseudo-bot', umode = 'iIoH', gecos = 'JStoker IRC Pseudo-Server Client'):
		uuid = config.link['sid'] + uid
		self.sock.ssend ('UID ' + uuid + ' ' + str(int(time.time())) + ' ' + nick + ' ' + host + ' ' + host + ' ' +  ident + ' 0.0.0.0 ' + str(int(time.time())) + ' +' + umode + ' :' + gecos)

if __name__ == '__main__':
	s = serverLink()
	s.start()
