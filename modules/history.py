import MySQLdb
from threading import Thread

class HistoryLoader(Thread):
	since = None

	def __init__(self, ctx, channel):
		Thread.__init__(self)
		self.ctx = ctx
		self.channel = channel

	def run(self):
		c = MySQLdb.connect(user="root", db="chatter")
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

	def __init__(self):
		self.connection = MySQLdb.connect(user="root", db="chatter")
	
	def close(self):
		if self.connection is not None:
			self.connection.close()

	def record(self, nick, chan):
		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO last_seen (nick, channel, last_seen) VALUES (%s, %s, now()) ON DUPLICATE KEY UPDATE last_seen=now()", (nick, chan))

		cursor.close()
		self.connection.commit()

	def get(self, nick, chan):
		cursor = self.connection.cursor()
		cursor.execute('SELECT last_seen from last_seen WHERE channel=%s and nick=%s', (chan, nick))
		r = cursor.fetchone()
		last = r[0] if r is not None else None
		cursor.close()
		return last

def onLoad():
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
		if ctx.chan[0] is not '#':
			return

		c = MySQLdb.connect(user="root", db="chatter")
		cursor = c.cursor()
		cursor.execute('INSERT INTO chatter (channel, nick, chat_date, chat) VALUES (%s,%s,now(),%s)', (ctx.chan, ctx.who.nick, msg))
		cursor.close()
		c.commit()
		c.close()

	@hook("quit")
	def onQuit(ctx):
		lastSeen.record(ctx.who.nick, ctx.chan)
	
	@hook("part")
	def onPart(ctx):
		lastSeen.record(ctx.who.nick, ctx.chan)
