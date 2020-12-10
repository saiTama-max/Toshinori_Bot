from discord import Embed, Color 
from discord.ext import commands

class Help(commands.Cog):

	def __init__(self, bot: commands.bot):
		self.bot = bot

	@commands.command(brief='Get info about all commands and cogs')
	async def help(self, ctx, name: str=None):
		color = Color.blurple()
		char_repeat = 20
		prefix = self.bot.command_prefix

		embed = Embed(
		    title=f"{'-' * (char_repeat // 2)}Toshinori{'-' * (char_repeat // 2)}",
		    color=color
		)

		if name is None:
		    cogs = list(self.bot.cogs.keys())
		    field_body = "\n".join(cogs)
		    field_body = field_body.strip()

		    field_body += (
		        f"\n\nUsage: `{prefix}help [Cog | Command]`. Example: `{prefix}help fun`"
		    )

		    embed.add_field(name="Cogs", value=field_body, inline=False)

		else:
			cog = self.bot.cogs.get(name.title(), None)

			if cog is None:
				c = self.bot.get_command(name.lower())

				if c is not None:
					embed.title += "\n" + c.name

					field_body = (
					    c.description
					    if c.description != ""
					    else c.brief if c.brief != "" else "This command has no description."
					)
					field_body += "\n" + (
					    "Usage: `" + c.usage + "`"
					    if c.usage is not None
					    else ""
					)

					embed.add_field(
						name=c.name, value=field_body.strip(), inline=False
	                )
				else:
					field_body = (
						f"Error: Cog or command `{name}` not found! Use `{prefix}help` to see a list of cogs"
					)
					embed.add_field(name="Cogs", value=field_body, inline=False)
			else:
				embed.title += "\n" + name.title()

				for c in cog.get_commands():
					brief = c.brief if c.brief is not None else ""
					usage = ("Usage: `" + c.usage + "`") if c.usage is not None else ""

					field_body = f'{brief}\n{usage}'.strip()

					embed.add_field(
	                    name=c.name,
	                    value=(
	                        field_body + "\n"
	                        if field_body != ""
	                        else "This command has no help message"
	                    ),
	                    inline=False,
	                )

		await ctx.send(embed=embed)


def setup(bot: commands.bot):
	bot.add_cog(Help(bot))
