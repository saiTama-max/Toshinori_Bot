import discord
from discord.ext import commands
import numpy as np
from PIL import Image
import cv2
import random
from io import BytesIO
from collections import Counter

class Images(commands.Cog):

	def __init__(self, bot: commands.bot):
		self.bot = bot

	@staticmethod
	def dominant_color(image: Image) -> tuple:
	    """Get the most occuring color in the image in rgb form as a tuple."""
	    image = image.convert("RGB")
	    arr = np.array(image)
	    ls = []
	    for pixel in arr:
	        for rgb in pixel:
	            ls.append(tuple(rgb))
	    return Counter(ls).most_common(1)[0][0]

	@commands.command(brief="Shows the pixelated avatar of the user/author",
	         usage="t!pixelate [user (optional)]",
	         aliases=['pixel', 'blockify', 'pix'])
	async def pixelate(self, ctx, user: discord.Member = None) -> None:
		"""Pixelate command, takes in an optional parameter user else pixelates author's avatar."""
		async with ctx.channel.typing():
		    user = ctx.author.avatar_url if not user else user.avatar_url
		    img_bytes = user.read()
		    image = Image.open(BytesIO(await img_bytes))

		    img_color = self.dominant_color(image)

		    img_small = image.resize((24, 24), resample=Image.BILINEAR)
		    result = img_small.resize((1024, 1024), Image.NEAREST)

		    buffer = BytesIO()
		    result.save(buffer, format="PNG")
		    buffer.seek(0)

		    img_file = discord.File(buffer, filename="pixelated.png")
		    img_url = 'attachment://pixelated.png'

		    img_emb = discord.Embed(color=discord.Color.from_rgb(int(img_color[0]), int(img_color[1]), int(img_color[2])))
		    img_emb.set_author(name="Here is your pixelated Image", icon_url=user)
		    img_emb.set_image(url=img_url)

		    await ctx.send(embed=img_emb, file=img_file)



	@commands.command(aliases=['spook', 'ghost'], brief='spookify a pfp', usage='t!ghostify [user (optional)]')
	async def ghostify(self, ctx, dude: discord.Member=None):
	    dude = dude
	    image_bytes = ctx.author.avatar_url.read() if not dude else dude.avatar_url.read()
	    img = Image.open(BytesIO(await image_bytes))
	    img = img.convert("RGB")
	    img = np.array(img)
	    gh_arr = cv2.bitwise_not(img)
	    final = Image.fromarray(gh_arr)
	    buffer = BytesIO()
	    final.save(buffer, format="PNG")
	    buffer.seek(0)
	    file = discord.File(buffer, filename='spooky.png')

	    await ctx.send(content="Here's your Ghostified avatar", file=file)
	@commands.command(brief='Get a triggered gif of a pfp', usage='t!trigger [user (optional)]', aliases=['triggered', 'angered'])
	async def trigger(self, ctx, dude: discord.Member=None):
	    user = ctx.author.avatar_url if not dude else dude.avatar_url
	    await user.save('images/pfp.png')
	    img = Image.open('images/pfp.png')
	    img = img.convert("RGB")
	    trigger = Image.open('images/triggered.png')
	    trigger = trigger.resize((206, 50), Image.NEAREST)
	    img = img.resize((206, 206), Image.NEAREST)
	    Image.Image.paste(img, trigger, (1, 155))
	    
	    img = np.array(img)
	    frames = []
	    fin = []
	    for pixel in img:
	        for rgb in pixel:
	            rgb[0] = 170
	    
	    for i in range(10):
	        frame = cv2.blur(img, (1, random.randint(3, 20)))
	        frames.append(frame)
	    for fra in frames:
	        a = Image.fromarray(np.array(fra))
	        fin.append(a)
	    a.save('images/triggered.gif', save_all=True, append_images=fin, loop=0)
	    await ctx.send(file=discord.File('images/triggered.gif'))

def setup(bot: commands.bot):
	bot.add_cog(Images(bot))