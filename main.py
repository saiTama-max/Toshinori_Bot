import discord
from discord.ext import commands
import os
import dotenv

dotenv.load_dotenv()
intents = discord.Intents.all()
toshi = commands.Bot(command_prefix='t!', case_insensitive=True, help_command=None, intents=intents)

print('Loading cogs...')
toshi.load_extension('cogs.fun')
toshi.load_extension('cogs.images')
toshi.load_extension('cogs.utility')
toshi.load_extension('cogs.help')
print('Cogs successfully loaded')
print("Preparing bot...")

@toshi.event
async def on_ready():
    print("Connected as {}".format(str(toshi.user)))

@toshi.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(error)

@toshi.command(brief="Reload the specified cogs, owner only",
			   usage="t!reload [cog]",
			   aliases=('reset', 'rl'))
@commands.has_permissions(administrator=True)
async def reload(ctx, *, modules):
	try:
		if "all" in modules:
			for cog in os.listdir('./cogs'):
				if cog.endswith(".py"):
					toshi.unload_extension(f"cogs.{cog[:-3]}")
					toshi.load_extension(f"cogs.{cog[:-3]}")

			await ctx.message.add_reaction("👌")
			await ctx.send("All cogs reloaded.")
		else:
			toshi.unload_extension(f"cogs.{modules}")
			toshi.load_extension(f"cogs.{modules}")
			await ctx.message.add_reaction("👌")
			await ctx.send(f"{modules} reloaded")
	except Exception as e:
		await ctx.send(f":x: Cogs reloading unsuccessful, \n`{e}`")
		raise e

@toshi.command(brief="load the specified cogs, owner only",
			   usage="t!reload [cog]")
@commands.has_permissions(administrator=True)
async def load(ctx, *, modules):
	try:
		toshi.load_extension(f"cogs.{modules}")
		await ctx.message.add_reaction("👌")
		await ctx.send(f"{modules} loaded")
	except Exception as e:
		await ctx.send(f":x: Cogs loading unsuccessful, \n`{e}`")
		raise e

@toshi.command(brief="unload the specified cogs, owner only",
			   usage="t!reload [cog]")
@commands.has_permissions(administrator=True)
async def unload(ctx, *, modules):
	try:
		if "all" in modules:
			for cog in os.listdir('./cogs'):
				if cog.endswith(".py"):
					toshi.unload_extension(f"cogs.{cog[:-3]}")
			await ctx.message.add_reaction("👌")
			await ctx.send(f"All cogs unloaded")
		else:
			toshi.unload_extension(f"cogs.{modules}")
			await ctx.message.add_reaction("👌")
			await ctx.send(f"{modules} unloaded")
	except Exception as e:
		await ctx.send(f":x: Cogs unloading unsuccessful, \n`{e}`")
		raise e

@toshi.event
async def on_message(self, message):
		empty_pings = ["Why are you pinging me for no reason lol",
				 	   "Do you want something?",
				 	   "<:pingree:786651403056709642>"]
		if message.author == toshi.user:
			return

		if message.content == f"<@{toshi.id}>":
			await message.channel.send(random.choice(empty_pings))
		elif f"<@{toshi.id}>" in message.content:
			await message.channel.send(f'{message.author.mention}{message.content.replace(f"<@{toshi.id}>", " ")}')
		toshi.process_commands(message)
TOKEN = os.getenv("TOKEN")
toshi.run(TOKEN)
