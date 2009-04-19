import ircbot
import irclib
import urllib
import urllib2
import time
import re
import base64
import thread
import signal

class Hah(ircbot.SingleServerIRCBot):
	def __init__(self, nick, channel, server, user, pwd):
		# message matching this request are posted to twitter.
		self.twitter_re = re.compile('^hah[,:] (.*)')

		# init underlying ircbot.
		servers = [(server, 6667)]
		ircbot.SingleServerIRCBot.__init__(self, servers, nick, 'hah!')
		self.channel = channel
		self.user = user
		self.pwd = pwd


	def unleash(self):
		print 'unleashed.'
		try:
			self.start()
		except KeyboardInterrupt: print "hyorgh!"


	def on_welcome(self, c, e):
		print 'joining %s' % self.channel
		c.join(self.channel)

	def on_privmsg(self, c, e):
		pass

	def on_ctcp(self, c, e):
		if e.arguments()[0] == 'ACTION':
			nick = irclib.nm_to_n(e.source())
			msg = e.arguments()[1]
			update = nick + " " + msg
			self.twitter_post(update)

	def on_pubmsg(self, c, e):
		channel = e.target()
		nick = irclib.nm_to_n(e.source())
		msg = e.arguments()[0]
		print "<%s%s> %s" % (nick, channel, msg)

		thread.start_new_thread(self.twitterism, (c, msg, nick, channel))

	# parse message, react to messages matching regex.
	def twitterism(self, c, msg, nick, channel):
		match = self.twitter_re.match(msg)
		if (match):
			update = match.group(1)
			if (len(update) > 140):
				print 'update too long: not posted.'
				time.sleep(1) # simulate thought.
				c.privmsg(channel, "%s: brevity is the soul of wit." % nick)
				return
			update = "[%s] %s" % (nick, update)
			self.twitter_post(update)

	# HTTP POST status update.
	def twitter_post(self, update):
		headers = {}
		auth = base64.b64encode(self.user+":"+self.pwd)
		headers["Authorization"] = "Basic " + auth
		headers["X-Twitter-Client"] = 'hah'
		data = urllib.urlencode({"status" : update})
		req = urllib2.Request("http://twitter.com/statuses/update.json", data, headers)
		try:
			print "attempting twitterpost: " + update
			h = urllib2.urlopen(req)
		except urllib2.HTTPError:
			print "HTTPError :-("
			return
		print "probably successful."
