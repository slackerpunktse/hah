from timing import timing
import ircbot
import irclib
import urllib
import urllib2
import time, sys, re
import thread, signal, yaml, base64


class Hah(ircbot.SingleServerIRCBot):
	def __init__(self, nick, channel, server):
		# message matching this request are posted to twitter.
		self.twitter_re = re.compile('^hah[,:] (.*)')
		self.twitterurl = "http://twitter.com/statuses/update.json"
		self.channel = channel

		# init underlying ircbot.
		servers = [(server, 6667)]
		ircbot.SingleServerIRCBot.__init__(self, servers, nick, 'hah!')

    
	# load credentials.
	# TODO> move function to module/function.
	# TODO> path should be var.
	def load_credentials(self):
		f = open('conf/credentials.yaml')
		credentials = yaml.load(f)
		f.close()
		try:
			self.twitteruser = credentials['twitteruser']
		#			self.twitterpass = credentials['twitterpass']
		except KeyError, key:
			sys.stderr.write("yaml load failed for key %s.\n" % key)
			sys.exit(1)


	@timing
	def unleash(self):
		self.load_credentials()
		print time.asctime()
		print 'unleashed.'
		try:
			self.start()
		except KeyboardInterrupt:
			print "hyorgh!"
			sys.exit(0)
	
	def on_heartbeat():
	    x = time.time()
	    print 'heartbeat> %s' % x
    
	@timing
	def on_welcome(self, c, e):
		print 'joining %s' % self.channel
		c.join(self.channel)
    
	@timing
	def on_privmsg(self, c, e):
		pass
	
	@timing
	def on_ctcp(self, c, e):
		if e.arguments()[0] == 'ACTION':
			nick = irclib.nm_to_n(e.source())
			msg = e.arguments()[1]
			update = nick + " " + msg
			thread.start_new.thread(self.twitter_post, update)
    
	@timing
	def on_pubmsg(self, c, e):
		channel = e.target()
		nick = irclib.nm_to_n(e.source())
		msg = e.arguments()[0]
		print "<%s%s> %s" % (nick, channel, msg)
		thread.start_new_thread(self.twitterism, (c, msg, nick, channel))

	# parse message, react to messages matching regex.
	@timing
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
	@timing
	def twitter_post(self, update):
		headers = {}
		auth = base64.b64encode(self.twitteruser+":"+self.twitterpass)
		headers["Authorization"] = "Basic " + auth
		headers["X-Twitter-Client"] = 'hah'
		data = urllib.urlencode({"status" : update})
		req = urllib2.Request(self.twitterurl, data, headers)
		try:
			print "attempting twitterpost: " + update
			h = urllib2.urlopen(req)
		except urllib2.HTTPError:
			print "HTTPError :-("
			return
		print "probably successful."

if __name__ == "__main__":
    print 'test> instantiate.'
    # add path?
    hah = Hah('','','')
