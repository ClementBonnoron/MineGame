import os
from datetime import date, datetime
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

from message import MessageData, get_embed_message

load_dotenv()
client = commands.Bot(command_prefix = os.getenv('PREFIX'), help_command=None)

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	activity_string = '{} servers.'.format(len(client.guilds))
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity_string))

@client.event
async def on_disconnect():
	print('Deconnection of {0.user}'.format(client))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@client.command(name='load')
async def load(ctx, arg=None):
	if str(ctx.author.id) in os.getenv('ADMIN').split(","):
		embed=get_embed_message("Load extensions", description="Loading of extensions by {}".format(ctx.author.name), author_name=ctx.author.display_name, author_icon=ctx.author.avatar_url)
		for extension in (os.getenv('EXTENSION').split(",") if arg is None else [arg]):
			try:
				client.load_extension(extension)
				embed.add_field(name=extension, value="Loaded !", inline=False)
			except Exception as error:
				embed.add_field(name=extension, value="Not loaded : {} !".format(error), inline=False)
		embed.set_footer(text="Loading extension - {}".format(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
		await ctx.channel.send(embed=embed)
	else:
		await ctx.author.send("Vous n'avez pas les droits pour exécuter la commande load!")

@client.command(name='unload')
async def unload(ctx, arg=None):
	if str(ctx.author.id) in os.getenv('ADMIN').split(","):
		embed=get_embed_message("Unload extensions", description="Unloading extensions by {}".format(ctx.author.name), author_name=ctx.author.display_name, author_icon=ctx.author.avatar_url)
		for extension in (os.getenv('EXTENSION').split(",") if arg is None else [arg]):
			try:
				client.unload_extension(extension)
				embed.add_field(name=extension, value="Unloaded !", inline=False)
			except Exception as error:
				embed.add_field(name=extension, value="Not unloaded : {} !".format(error), inline=False)
		embed.set_footer(text="Unloading extension - {}".format(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
		await ctx.channel.send(embed=embed)
	else:
		await ctx.author.send("Vous n'avez pas les droits pour exécuter la commande unload!")

if __name__ == '__main__':
	for extension in os.getenv('EXTENSION').split(","):
		try:
			client.load_extension(extension)
		except Exception as error:
			print('{} cannot be loaded [{}]'.format(extension, error))
	client.run(os.getenv('TOKEN'))

