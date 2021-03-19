import os

import discord
from discord.ext import commands

from message import MessageData, send_message_error_access, get_embed_message
from content import Access
from user import Users
from datetime import date
from json import dumps

class UserCommands(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.users = Users.loadData(os.getenv('FILE_USERS'))

	def print(self, txt):
		print(txt)

	@commands.Cog.listener()
	async def on_command_completion(self, ctx):
		if ctx.author.id != os.getenv('BOT_ID') and not ctx.command.name in ['json', 'dropdb']:
			msg = MessageData(ctx.message)
			if not self.users.is_defined(msg):
				await self.users.create_user(msg)
		return

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		print("{} was invoked incorrectly !".format(ctx.command.name))
		print(error) 
			
	@commands.command(name='json')
	async def json(self, ctx):
		await ctx.channel.send(dumps(self.users.toJson(), indent=2))

	@commands.command(name='profile')
	async def profile(self, ctx):
		msg = MessageData(ctx.message)
		if not self.users.is_defined(msg):
			print("Perso non existant : {}".format(msg.aid))
			return
			
		data = self.users.user_profil(msg)
		embed=get_embed_message("Profile", description="", author_name=ctx.author.display_name, author_icon=ctx.author.avatar_url)

		answer = "Name : {}\n".format(data["name"])
		answer += "Date joined : {}\n".format(data["date_joined"])
		answer += "Money : {}".format(data["money"])
		embed.add_field(name="Utilisateur", value=answer, inline=False)

		blocks = data["blocks"]
		answer = ""
		for name, count in blocks.items():
			answer += "\t{}: {}\n".format(name.capitalize(), count)
		embed.add_field(name="Données", value=answer, inline=False)
		embed.set_footer(text="{} - {}".format(msg.aname, date.today().strftime("%d/%m/%Y, %H:%M:%S")))

		await msg.channel.send(embed=embed)
		return

	@commands.command(name='place')
	async def place(self, ctx):
		msg = MessageData(ctx.message)
		if not self.users.is_defined(msg):
			print("Perso non existant")
			return

		embed=discord.Embed(title="Place", url="https://realdrewdata.medium.com/", description="Current place : {}".format(self.users.get_user(msg).access.name.capitalize()), color=0xFF5733)
		await msg.channel.send(embed=embed)

		
	@commands.command(name='update')
	async def update(self, ctx):
		msg = MessageData(ctx.message)
		if not self.users.is_defined(msg):
			print("Perso non existant")
			return
		
		if msg.argc == 3 and msg.param[0] == 'message' and bool(msg.param[1]):
			self.users.set_display_mining_user(msg, msg.param[1].lower() == "true")
		self.__saveData()
		return

			
	@commands.command(name='upgrade')
	async def upgrade(self, ctx):
		msg = MessageData(ctx.message)
		if not self.users.is_defined(msg):
			print("Perso non existant")
			return

		await msg.channel.send(self.users.user_update_place(msg))
		self.__saveData()
		return


	@commands.command(name='mine')
	async def mine(self, ctx):
		msg = MessageData(ctx.message)
		if not self.users.is_defined(msg):
			print("Perso non existant")
			return

		if msg.argc == 2:
			place = msg.param[0].upper()

			if not Access.is_access(place):
				await msg.channel.send("'{}' is not a correct place !".format(msg.param[0]))
				return

			if not self.users.user_have_access(msg, place):
				await send_message_error_access(self.users, msg, place)
				return
			
			block_mined, place_mined, count = self.users.user_mine(msg, place)
			if self.users.user_display_msg(msg):
				await msg.channel.send("You have mined {} {} in {}!".format(count, block_mined.name.capitalize(), place_mined.name.capitalize()))
		else:
			block_mined, place_mined, count = self.users.user_mine(msg)
			if self.users.user_display_msg(msg):
				await msg.channel.send("You have mined {} {} in {}!".format(count, block_mined.name.capitalize(), place_mined.name.capitalize()))
		self.__saveData()
		return
				
	@commands.command(name='sell')
	async def sell(self, ctx):
		msg = MessageData(ctx.message)
		if not self.users.is_defined(msg):
			print("Perso non existant")
			return

		if msg.argc == 3:
			success, data = self.users.sell_user_block(msg, msg.param[0], msg.param[1])
			if success:
				answer = "Sale of {} :\n".format(msg.aname)
				for name, money_data in data.items():
					answer += "\t{} {} for {} gold\n".format(money_data[0], name.capitalize(), money_data[1])
				await msg.channel.send(answer)
		self.__saveData()
		return

	def __saveData(self):
		self.users.saveData(os.getenv('FILE_USERS'))
		return

def setup(bot):
	bot.add_cog(UserCommands(bot))