"""
Pseudo-Server.
Basic pseudo-server. Connects to inspircd 1.2 (may work on others).

Features:

- NickTracking.
- Connecting (and linking)
"""

import config

#Twisted stuff.
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver

class serverProtocol (LineReceiver):
	uuid = {}
	
	def ssendLine (self, msg):
		self.sendLine (':' + config.link['sid'] + ' ' + msg)

	def usendLine (self, user, msg):
		self.sendLine (':' + config.link['sid'] + user + ' ' + msg)

	def connectionMade(self):
		self.sendLine ( 'SERVER %s %s 0 %s :JStoker IRC Pseudo-Server' % ( config.link['server'], config.link['recvpass'], config.link['sid']) )

	def lineReceived(self, line):
		words = line.split (' ')
		if len(words) < 2:
			return
		print words
		if words[0] == 'SERVER':
			if words[2] == config.link['sendpass']:
				self.sendLine ('BURST')
				self.sendLine (':%s VERSION :JStoker IRC Pseudo-Server' % config.link['server'])
				# Burst UID's here.
				# self.sendLine ('UID blah')
				self.sendLine ('ENDBURST')
				self.privmsg_server ('Burst completed.')

		elif words[1] == 'PING':
			self.ssendLine ('PONG %s' % words[2])
			self.privmsg_server ('Pong.')

		# Nick Tracking
		if words[1] == 'UID':
			self.uuid [words[2]] = [words[4]]
		
		elif words [1] == 'NICK':
			self.uuid [words[0][1:]][0] = words [2]

	def getUuid (self, nick):
		for uuid in self.uuid.keys():
			if uuid[0] == nick:
				return uuid
	
	def getNick (self, uuid):
		return self.uuid [uuid]
#		self.sendLine(self.answers[line])

	def privmsg_server (self, msg):
		self.ssendLine ('PRIVMSG %s :%s' % (config.chan_log, msg))

class linkFactory(protocol.ClientFactory):
	protocol = serverProtocol

	def clientConnectionFailed(self, connector, reason):
		print "Connection failed!"
		reactor.stop()

	def clientConnectionLost(self, connector, reason):
		print "Connection lost!"
		reactor.stop()


# this connects the protocol to a server runing on port 8000
def main():
	f = linkFactory()
	reactor.connectTCP(config.link['remote_host'], config.link['remote_port'], f)
	reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
	main()
