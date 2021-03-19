from discord.ext import commands
import os

class AdminCommands(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		self.admins = os.getenv('ADMIN').split(",")

		async def cog_check(self, ctx):
			return ctx.author.id in self.admins

	
def setup(bot):
	bot.add_cog(AdminCommands(bot))