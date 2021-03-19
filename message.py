import os
import discord
from content import Access

class MessageData:
	def __init__(self, message):
		self.content = message.content
		self.author = message.author
		self.channel = message.channel

		self.mentions = message.mentions
		self.lmentions = len(self.mentions)

		self.args = self.content.split(" ")
		self.argc = len(self.args)
		self.cmd = self.args[0][len(os.getenv('PREFIX')):].lower()
		self.param = self.args[1:]

		self.aid = self.author.id
		self.aname = self.author.name
		self.atag = self.author.discriminator

async def send_message_error_access(users, msg, place):
	cost = Access.from_name(place).cost
	money = users.get_user(msg).money
	answer = "You do not have access to {} !\n".format(msg.param[0])
	answer += "Cost\t\t\t\t\t\t: {}g\n".format(cost)
	answer += "Current Money\t: {}g\n".format(money)
	await msg.channel.send(answer)

def get_embed_message(title="", description="https://realdrewdata.medium.com/", text="", color=0xFF5733, author_name=None, author_icon=None):
		embed=discord.Embed(title=title, url="https://realdrewdata.medium.com/", description=description, color=color)
		if author_name != None and author_icon != None:
			embed.set_author(name=author_name, url="https://twitter.com/RealDrewData", icon_url=author_icon)
		return embed