import MySQLdb
from threading import Thread

class HistoryLoader(Thread):
	def __init__(self, ctx, channel):
		Thread.__init__(self)
		self.ctx = ctx
		self.channel = channel

	def run(self):
		c = MySQLdb.connect(user="root", db="chatter")
		cursor = c.cursor()

		cursor.execute('SELECT chat, nick, chat_date FROM chatter WHERE channel=%s AND chat_date > now() - INTERVAL 1 DAY', (self.channel,))
		while True:
			row = cursor.fetchone()
			if row is None:
				break
			
			self.ctx.reply('%s <%s> %s' % (row[2], row[1], row[0]))

		c.close()

def onLoad():
	
	@command("history", 1)
	def onHistory(ctx, cmd, arg, *args):
		ctx.reply("something: %s" % (arg))
		loader = HistoryLoader(ctx, arg)
		loader.start()
	
	@hook("message")
	def onMessage(ctx, msg):
		print("got a message: %s %s %s" % (ctx.chan, ctx.who.nick, msg))
		c = MySQLdb.connect(user="root", db="chatter")
		cursor = c.cursor()
		cursor.execute('INSERT INTO chatter (channel, nick, chat_date, chat) VALUES (%s,%s,now(),%s)', (ctx.chan, ctx.who.nick, msg))
		cursor.close()
		c.commit()
		c.close()

