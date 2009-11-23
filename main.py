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
		self.uuid = {}
	
	def connect (self):
		self.sock.connect (config.link_remote, config.link_port)
		self.sock.send ('SERVER %s %s 0 %s :JCS serv' % (config.link_name, config.link_pass, config.link_sid))

	def addpseudoclient (self, uid, nick, host = config.link_name, ident = 'pseudoserver', modes = 'iIoH', gecos = 'Pseudo Server bot', opertype = config.bot_opertype):
		# Adding Client
		uuid = config.link_sid + uid
		self.sock.ssend ('UID ' + uuid + ' ' + str(currenttime()) + ' ' + nick + ' ' + host + ' ' + host + ' ' + ident + ' 0.0.0.0 ' + str(currenttime()) + ' +' + modes + ' :' + gecos)
		self.uuid[uuid] = [nick + '!' + ident + '@' + host, {}]
		for mode in modes:
			self.uuid [uuid][1][mode] = True
		# Opering..
		self.sock.usend (uid ,'OPERTYPE %s' % opertype)

	def run (self):
		while 1:
			data = self.sock.receive (2048)
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
					self.uuid[uuid] = [useridenthostmask, {}]
					for mode in words[10][1:]:
						self.uuid [uuid][1][mode] = True

				if words[1] == 'MODE':
					pass
					uuid = words[2]
					mode = words[3]
					self.user_mode_change (uuid, mode)

				if words[1] == 'PRIVMSG':
					user = words[0][1:]
					#print self.user_umode(user, 'o')
					print self.uuid[user][1]

				if words[0] == 'ERROR':
					print 'Fatal Error Occurred'
					raise SystemExit

	def user_mode (self, user, mode):
		if self.uuid[user][1][mode]:
			return True
		else:
			return False
	
	def user_mode_change (self, user, mode):
		modes = re.findall ('[+-][a-zA-Z]+', mode)
		for mode in modes:
			
			if mode[0] == '+':
				for char in modes:
					self.uuid[user][1][char[1]] = True
			else:
				for char in modes:
					self.uuid[user][1][char[1]] = False
	
	def get_user (self, uuid):
		return self.uuid[uuid][0]

if __name__ == '__main__':
	link = ServerLink()
	link.run()
