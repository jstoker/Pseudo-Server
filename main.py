import threading, sock
import time # TS

import config

def currenttime ():
	return int(time.time())

class ServerLink (threading.Thread):
	def __init__ (self):
		threading.Thread.__init__ (self)
		self.sock = sock.Socket()
		self.uuid = {}
	
	def connect (self):
		self.sock.connect (config.link_remote, config.link_port)
		self.sock.send ('SERVER %s %s 0 %s :JCS serv' % (config.link_name, config.link_pass, config.link_sid))

	def addpseudoclient (self, uid, nick, host = config.link_name, ident = 'pseudoserver', modes = 'iIoH', gecos = 'Pseudo Server bot', opertype = config.bot_opertype):
		# Adding Client
		self.sock.ssend ('UID ' + config.link_sid + uid + ' ' + str(currenttime()) + ' ' + nick + ' ' + host + ' ' + host + ' ' + ident + ' 0.0.0.0 ' + str(currenttime()) + ' +' + modes + ' :' + gecos)
		self.uuid[config.link_sid+uid] = [nick + '!' + ident + '@' + host, '+' + modes]
		# Opering..
		self.sock.usend (uid ,'OPERTYPE %s' % opertype)

	def run (self):
		while 1:
			data = self.sock.receive (2048)
#			if data != '':
#				print data
			lines = data.split ('\r\n')
			for line in lines:
				if line.startswith( 'Link is not connected'):
					time.sleep (2)
					self.connect()
				if line == '':
					break
				
				print line
				
				words = line.split (' ')
				if words[0] == 'SERVER':
					if words[2] != config.link_remote_pass:
						print 'Remote send-pass is INVALID.'
						print 'Please make sure sendpass is the same as link_remote_pass.'
						raise SystemExit

					self.sock.ssend ('BURST')
					self.sock.send (':%s VERSION :JStoker - Pseudo Server - %s' % (config.link_name, config.link_version))
					# Here's where you could/should burst a few clients in here.
					self.addpseudoclient (config.bot_uid, config.bot_name)
					self.sock.ssend ('ENDBURST')
				
				if words[1] == 'PING':
					self.sock.ssend ('PONG %s' % words[3])
				
				if words[1] == 'UID':
					uuid = words[2]
					useridenthostmask = words[4] + '!' + words[7] + '@' + words[5]
					self.uuid[uuid] = [useridenthostmask, words[10][1:]]

				if words[1] == 'PRIVMSG':
					print self.uuid[words[0][1:]] 
					pass

				if words[0] == 'ERROR':
					print 'Fatal Error Occurred'
					raise SystemExit
if __name__ == '__main__':
	link = ServerLink()
	link.run()
