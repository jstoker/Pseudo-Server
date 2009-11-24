import threading, sock
import time # TS
import re # ModeParsing

import config

def currenttime ():
	return int(time.time())

class ServerLink (threading.Thread):
	def __init__ (self):
		threading.Thread.__init__ (self)
		self.sock = sock.Socket()
	
	def connect (self):
		self.sock.connect (config.link_remote, config.link_port)
		self.sock.send ('SERVER %s %s 0 %s :JCS serv' % (config.link_name, config.link_pass, config.link_sid))

	def addpseudoclient (self, uid, nick, host = config.link_name, ident = 'pseudoserver', modes = 'iIoH', gecos = 'Pseudo Server bot', opertype = config.bot_opertype):
		# Adding Client
		uuid = config.link_sid + uid
		self.sock.ssend ('UID ' + uuid + ' ' + str(currenttime()) + ' ' + nick + ' ' + host + ' ' + host + ' ' + ident + ' 0.0.0.0 ' + str(currenttime()) + ' +' + modes + ' :' + gecos)
		# Opering..
		self.sock.usend (uid ,'OPERTYPE %s' % opertype)

	def channel_join (self, bot, channel, modes='oa'):
		self.sock.ssend ('FJOIN %s %s + :%s,%s' % (channel, currenttime (), modes, bot))

	def run (self):
		while 1:
			data = self.sock.receive (2048)
			lines = data.split ('\r\n')
			for line in lines:
				if line.startswith( 'Link is not connected'): # Socket has been dropped. Reconnecting.
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
				
				if words[1] == 'PRIVMSG':
					self.channel_join (words[2], words[3][1:])
				
				if words[0] == 'ERROR':
					print 'Fatal Error Occurred'
					raise SystemExit

if __name__ == '__main__':
	link = ServerLink()
	link.run()
