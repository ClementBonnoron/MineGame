import discord
from discord.ext import commands
import os

from message import MessageData, get_embed_message

class AdminCommands(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		self.admins = os.getenv('ADMIN').split(",")

	@commands.command(name='dropdb')
	async def dropdb(self, ctx):
		msg = MessageData(ctx.message)
		embed=get_embed_message("Place", description="{} have drop the users database".format(msg.aname), author_name=ctx.author.display_name, author_icon=ctx.author.avatar_url)
		await msg.channel.send(embed=embed)
		with open(os.getenv('FILE_USERS'), 'w') as file:
			file.write('{}')
		self.bot.get_cog('UserCommands').users.data = {}


	@commands.command(name='shutdown')
	async def shutdown(self, ctx):
		msg = MessageData(ctx.message)
		if msg.aid == int(os.getenv('AUTHOR_ID')):
			embed=get_embed_message("Shutdown", description="{} disconnected the bot!".format(msg.aname), author_name=ctx.author.display_name, author_icon=ctx.author.avatar_url)
			await msg.channel.send(embed=embed)
			await self.bot.change_presence(activity=discord.Game(name="Python"))
			await self.bot.logout()
		else:
			await ctx.author.send("Vous n'avez pas les droits pour exécuter la commande logout, seul le propriétaire du bot peut le faire!")

def setup(bot):
	bot.add_cog(AdminCommands(bot))