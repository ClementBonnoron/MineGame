import discord
from discord.ext import commands

from message import MessageData, get_embed_message

class InfoCommands(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='help')
	async def help(self, ctx):
		msg = MessageData(ctx.message)

		answer = "&profil                                        --> Display your profil\n"
		answer += "&mine [place]                          --> Mines in the selected place. If no place is defined, mine in the strongest place\n"
		answer += "&sell [block|all] [count|all]   --> Sells block of your choose. You can choose the quantity and the type of the block\n"
		answer += "&update message <bool>     --> Displays a message when you're mining if it's true\n"
		embed=get_embed_message(title="Help", description=answer)
		await msg.channel.send(embed=embed)

def setup(bot):
	bot.add_cog(InfoCommands(bot))