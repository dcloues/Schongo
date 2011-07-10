import MySQLdb
from threading import Thread
from ConfigParser import RawConfigParser

historyConfig = RawConfigParser()

def connection():
	opts = dict(historyConfig.items('Database'))
	return MySQLdb.connect(**opts)

class HistoryLoader(Thread):
	since = None

	def __init__(self, ctx, channel):
		Thread.__init__(self)
		self.ctx = ctx
		self.channel = channel

	def run(self):
		c = connection()
		cursor = c.cursor()
		
		query = 'SELECT chat, nick, chat_date FROM chatter WHERE channel=%s AND chat_date > '

		if self.since is not None:
			query = query + '%s'
			args = (self.channel, self.since)
		else:
			query = query + 'now() - INTERVAL 1 DAY'
			args = (self.channel)

		cursor.execute(query, args)
		while True:
			row = cursor.fetchone()
			if row is None:
				break
			
			self.ctx.reply('%s <%s> %s' % (row[2], row[1], row[0]))

		c.close()

class LastSeen(object):
	connection = None
	userChannels = {}

	def __init__(self):
		self.connection = connection()
	
	def close(self):
		if self.connection is not None:
			self.connection.close()

	def record(self, nick, chan):
		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO last_seen (nick, channel, last_seen) VALUES (%s, %s, now()) ON DUPLICATE KEY UPDATE last_seen=now()", (nick, chan))

		cursor.close()
		self.connection.commit()

	def recordQuit(self, nick):
		if nick not in self.userChannels:
			return

		for chan in self.userChannels[nick]:
			self.record(nick, chan)
		
		del self.userChannels[nick]

	def get(self, nick, chan):
		cursor = self.connection.cursor()
		cursor.execute('SELECT last_seen from last_seen WHERE channel=%s and nick=%s', (chan, nick))
		r = cursor.fetchone()
		last = r[0] if r is not None else None
		cursor.close()
		return last

	def joined(self, nick, chan):
		if nick not in self.userChannels:
			self.userChannels[nick] = [chan]
		elif chan not in self.userChannels[nick]:
			self.userChannels[nick].append(chan)

def onLoad():
	historyConfig.read("data/history.cfg")
	lastSeen = LastSeen()

	@command("history", 1)
	def onHistory(ctx, cmd, arg, *args):
		loader = HistoryLoader(ctx, arg)
		loader.start()

	@command("unseen", 1)
	def onUnseenHistory(ctx, cmd, arg, *args):
		loader = HistoryLoader(ctx, arg)
		loader.since = lastSeen.get(ctx.who.nick, arg)
		loader.start()
	
	@hook("message")
	def onMessage(ctx, msg):
		# don't log private mssages to the bot
		if ctx.chan[0] != '#':
			return

		c = connection()
		cursor = c.cursor()
		cursor.execute('INSERT INTO chatter (channel, nick, chat_date, chat) VALUES (%s,%s,now(),%s)', (ctx.chan, ctx.who.nick, msg))
		cursor.close()
		c.commit()
		c.close()
	
	@hook("join")
	def onJoin(ctx):
		lastSeen.joined(ctx.who.nick, ctx.chan)

	@hook("quit")
	def onQuit(ctx):
		lastSeen.recordQuit(ctx.who.nick)
	
	@hook("part")
	def onPart(ctx):
		lastSeen.record(ctx.who.nick, ctx.chan)
