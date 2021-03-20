from discord.ext import commands
import os
from datetime import date, datetime
from zipfile import ZipFile

class ArchCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='saveimgs')
    async def saveimgs(self, ctx, passwd=None, arg1=None, arg2=None, fend_name=None):
        if passwd is None or str(passwd) != "yesiwanttosaveallfiles":
            await ctx.message.channel.send("Password is not correct !")
            return

        max = None
        mindate = None
        maxdate = None
        if arg1 is not None and arg1.isdecimal():
            max = int(arg1)
        else:
            if arg1 is not None:
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
                                print("saving : '" + new_name + "'")
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

def setup(bot):
    bot.add_cog(ArchCommands(bot))