import os
import datetime
from datetime import date, datetime
from dotenv import load_dotenv

from discord.ext import commands

from message import MessageData, get_embed_message

load_dotenv()
client = commands.Bot(command_prefix = os.getenv('PREFIX'), help_command=None)

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


@client.command(name='load')
async def load(ctx, arg=None):
	if str(ctx.author.id) in os.getenv('ADMIN').split(","):
		embed=get_embed_message("Load extensions", description="Loading of extensions by {}".format(ctx.author.name), author_name=ctx.author.display_name, author_icon=ctx.author.avatar_url)
		for extension in (os.getenv('EXTENSION').split(",") if arg is None else arg):
			try:
				client.load_extension(extension)
				embed.add_field(name=extension, value="Loaded !", inline=False)
			except Exception as error:
				embed.add_field(name=extension, value="Not loaded : {} !".format(error), inline=False)
		embed.set_footer(text="Loading extension - {}".format(date.today().strftime("%d/%m/%Y, %H:%M:%S")))
		await ctx.channel.send(embed=embed)
	else:
		await ctx.author.send("T'as pas les droits fdp !")

@client.command(name='unload')
async def unload(ctx, arg=None):
	if str(ctx.author.id) in os.getenv('ADMIN').split(","):
		embed=get_embed_message("Unload extensions", description="Unloading of extensions by {}".format(ctx.author.name), author_name=ctx.author.display_name, author_icon=ctx.author.avatar_url)
		for extension in (os.getenv('EXTENSION').split(",") if arg is None else arg):
			try:
				client.unload_extension(extension)
				embed.add_field(name=extension, value="Loaded !", inline=False)
			except Exception as error:
				embed.add_field(name=extension, value="Not loaded : {} !".format(error), inline=False)
		embed.set_footer(text="Unloading extension - {}".format(date.today().strftime("%d/%m/%Y, %H:%M:%S")))
		await ctx.channel.send(embed=embed)
	else:
		await ctx.author.send("T'as pas les droits fdp !")

@client.command(name='dropdb')
async def dropdb(ctx):
	msg = MessageData(ctx.message)
	if msg.aid == int(os.getenv('AUTHOR_ID')):
		embed=get_embed_message("Place", description="{} havez drop the users database".format(msg.aname), author_name=ctx.author.display_name, author_icon=ctx.author.avatar_url)
		await msg.channel.send(embed=embed)
		os.open(os.getenv('FILE_USERS'), 'w').close()

if __name__ == '__main__':
	for extension in os.getenv('EXTENSION').split(","):
		print(extension)
		try:
			client.load_extension(extension)
		except Exception as error:
			print('{} cannot be loaded [{}]'.format(extension, error))
	print(client.cogs)
	client.run(os.getenv('TOKEN'))

