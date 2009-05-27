from timing import timing

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