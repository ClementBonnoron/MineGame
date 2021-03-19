import os
import datetime
from datetime import date, datetime
from zipfile import ZipFile
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

def predicate(event):
  return event.attachments is not None

#%H:%M:%S

@client.command(name='tmp')
async def tmp(ctx, passwd=None, arg1=None, arg2=None, fend_name=None):
	if passwd is None or str(passwd) != "yesiwanttosaveallfiles":
		await ctx.message.channel.send("Password is not correct !")
		return

	max = None
	mindate = None
	maxdate = None
	if arg1 is not None and arg1.isdecimal():
		max = int(arg1)
	else:
		try:
			mindate = datetime.strptime(arg1,"%d/%m/%Y")
			if arg2 is not None:
				maxdate = datetime.strptime(arg2, "%d/%m/%Y")
		except:
			pass

	
	image_types = ["png", "jpeg", "gif", "jpg"]
	dict_imgs = []
	zip_file_name = date.today().strftime("%d_%m_%Y") + "_imags" + ("_" + fend_name if fend_name is not None else "") + ".zip"

	with ZipFile(zip_file_name, 'w') as myzip:
		message = await ctx.message.channel.send("Loading...")
		count = 0
		async for entry in ctx.channel.history(limit=max):
			count += 1
			if len(entry.attachments) > 0:
				for attachment in entry.attachments:
					for image in image_types:
						if attachment.filename.lower().endswith(image) and not attachment.filename in dict_imgs and \
								(entry.created_at <= mindate if mindate is not None else True) and \
								(entry.created_at >= maxdate if maxdate is not None else True):
							new_name = entry.created_at.strftime("%Y%m%d%H%M%S") + \
								"__" + entry.author.name + \
								"__" + attachment.filename
							print(new_name)
							await attachment.save("./imgs/" + new_name)
							myzip.write("./imgs/" + new_name)
							os.remove("./imgs/" + new_name)
							dict_imgs.append(new_name)
						if not (entry.created_at >= maxdate if maxdate is not None else True):
							break
					if not (entry.created_at >= maxdate if maxdate is not None else True):
						break
				if not (entry.created_at >= maxdate if maxdate is not None else True):
					break
			if not (entry.created_at >= maxdate if maxdate is not None else True):
				break
			if (count % 500 == 0):
				await message.edit(content="{} messages chargés...!".format(count))

		
	await message.edit(content="Finished! {} messages loaded with {} downloads!".format(count, len(dict_imgs)))


if __name__ == '__main__':
	for extension in os.getenv('EXTENSION').split(","):
		try:
			client.load_extension(extension)
		except Exception as error:
			print('{} cannot be loaded [{}]'.format(extension, error))
	client.run(os.getenv('TOKEN'))

