import ircbot

class Hah(ircbot.SingleServerIRCBot):
	def __init__(self, nick, channel, server):
		self.channel = channel
		servers = [(server, 6667)]
		ircbot.SingleServerIRCBot.__init__(self, servers, nick, 'hah!')

	def unleash(self):
		print 'unleashed.'
		self.start()
		self.connect()

	## triggers.
	def on_welcome(self, c, e):
		print 'joining %s' % self.channel
		c.join(self.channel)

	def on_privmsg(self, c, e):
		print '> %s: %s' % (c, str(e.arguments()))

	def on_pubmsg(self, c, e):
		print '%s: %s' % (c, str(e.arguments()))