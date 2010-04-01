import imp

def load (mname, self):
	module = 'protocol/%s.py' % mname
	mod = imp.load_source ('protocol', module)
	protocol = mod.protocol()
	if not hasattr (protocol, 'init'):
		print 'No init function found in %s' % mod.__name__
		return
	protocol.init(self)
	return protocol

def unload (protocol):
	if not hasattr (protocol, 'fini'):
		print 'No fini function found in %s' % protocol.__name__
		return
	protocol.fini()
	del protocol
