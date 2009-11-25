import sock
import threading

class serverLink (threading.Thread):
	def __init__ (self):
		threading.Thread.__init__(self)
		self.daemon = False
		self.sock = sock.Socket()
		self.sock.start()

	def run (self):
			while 1:
				print self.sock.recv()
				print 'lien'

if __name__ == '__main__':
	s = serverLink()
	try:
		s.start()
	except:
		raise 
