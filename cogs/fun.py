import asyncpg
import discord
import random
import async_cleverbot as ac
from discord.ext import commands
import asyncio
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
PASSWORD = os.getenv("PASSWORD")
credentials = [USERNAME, HOST, DATABASE, PASSWORD]
common_qui = ['Engine', 'Voice', 'Gigantification', 'Hardening', 
    'Jet', 'Regeneration', 'Zero Gravity', 'Somnambulist', 'Navel Laser', 'Tail']
uncommon_qui = ['Air Propulsion', 'Electric', 'Shock Absorption', 'Warp gate',
    'Black hole', 'Permeation', 'Pop Off', 'Acid', 'Clones', "Copy"]
rare_qui = ['Dark Shadow', 'Cremation', 'Quirkless', 'Muscle Augmentation', 'Decay', 'Creation', 'Frog']
legend_qui = ['AFO', 'OFA', 'HHHC', 'Explosion', 'Overhaul', 'Fierce Wings', 'Hell flame']

async def main():
	try:
		conn = await asyncpg.connect(user=USERNAME, password=PASSWORD,
									database=DATABASE, host=HOST)
		await conn.execute("""CREATE TABLE IF NOT EXISTS quirks (
					username text,
					quirk text,
					spins integer,
					userid bigint,
					current timestamptz)""")
		return conn
	except:
		return False

class Fun(commands.Cog):

	def __init__(self, bot: commands.bot):
		self.bot = bot

	@commands.command(aliases=['eightball', '8b'],
					  brief='you can get answers to questions in 8ball', usage='t!8ball [question]')
	async def _8ball(self, ctx, *, question):
	    responses = [
	        'It is certain',
	        'Yes, definately',
	        'Without a doubt',
	        'Thats for sure',
	        'Most likely',
	        'try again',
	        'Didnt quite get that',
	        'Concentrate and try again',
	        'Not likely at all',
	        'My reply is no',
	        'Obviously not!',
	        'No...',
	        'Nuh uh']
	    answer_emb = discord.Embed(description=random.choice(responses), color=discord.Color.purple())
	    await ctx.send(embed=answer_emb)

	@commands.command(brief='flips a coin for you', usage='t!flip [heads/tails]')
	async def flip(self, ctx, *, toss):
	    coin_ = ['heads', 'tails']
	    toss_res = random.choice(coin_)
	    my_embed = discord.Embed(title=toss_res, color=discord.Color.red(), description=f'{ctx.author.mention} won the toss!')
	    my_embed_2 = discord.Embed(title=toss_res, color=discord.Color.red(), description=f'{ctx.author.mention} lost the toss!')
	    if toss == toss_res:
	        await ctx.send(embed=my_embed)
	        
	    elif toss.lower() not in coin_:
	        await ctx.send('Enter heads or tails! 😛')
	    else:
	        await ctx.send(embed=my_embed_2)

	@commands.command(brief='play a game of rock paper scissors with Tanjiro', usage='t!play [rock/paper/scissor]')
	async def play(self, ctx, *, response=None):
	    response = response.lower()
	    options = ['rock', 'paper', 'scissors']
	    bot_choice = random.choice(options)
	    win = "I win lol"
	    lose = "I lose oof"
	    choose = f'I choose {bot_choice}'
	    message = ''
	    if response not in options:
	        message = "Please choose between rock, paper or scissors"
	    elif response == bot_choice:
	        message = f"I choose {bot_choice}\nOh, we got a tie"
	        
	    elif response == 'rock':
	        message = f'{choose}\n{win if bot_choice == "paper" else lose}'
	        
	    elif response == 'paper':
	        message = f'{choose}\n{win if bot_choice == "scissors" else lose}'   
	   
	    elif response in ('scissors', 'scissor'):
	        message = f'{choose}\n{win if bot_choice == "rock" else lose}'

	    await ctx.send(message)



	@commands.command(brief='Gives you a random quirk', usage='t!spin')
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def spin(self, ctx):
		conn = await main()
		if conn:

			emb = discord.Embed()
			i = random.randint(0, 100)
			quirk = ''
			if i <= 55:
				quirk = random.choice(common_qui)
				emb.title = f'__Common__ \n{quirk}'
				emb.color = discord.Color.lighter_grey()
			elif i <= 85:
				quirk = random.choice(uncommon_qui)
				emb.title = f'__Uncommon__ \n{quirk}'
				emb.color = discord.Color.green()
			elif i <= 97:
				quirk = random.choice(rare_qui)
				emb.title = f'__Rare__ \n{quirk}'
				emb.color = discord.Color.gold()
			else:
				quirk = random.choice(legend_qui)
				emb.title = f'__LEGENDARY__ \n{quirk}'
				emb.color = discord.Color.red()
			try:
					
				row = await conn.fetchrow("SELECT userid FROM quirks WHERE userid = $1", ctx.author.id)
				

				if not row:
					spins = await conn.fetchrow("SELECT spins FROM quirks WHERE userid=$1", ctx.author.id)
					spins = list(spins.values())[0] if spins else 0
					
					await conn.execute('''INSERT INTO quirks(username, quirk, userid) VALUES ($1, $2, $3)''',
									str(ctx.author), quirk, ctx.author.id)
					await ctx.send("Spinning....")
					await asyncio.sleep(3)
					if not spins:
						spins = 0				
					emb.description = f"You have now {spins} left in total"
					await ctx.send(f"{ctx.author.mention}, you got")
					await ctx.send(embed=emb)
				else:
					spins = await conn.fetchrow("SELECT spins FROM quirks WHERE userid=$1", ctx.author.id)
					spins = list(spins.values())[0] if spins else 0
					if not spins:
						spins = 0	

					if spins > 0:
						await conn.execute('''UPDATE quirks SET quirk=$1, spins=$2, username=$3 WHERE userid=$4''',
										quirk, spins-1, str(ctx.author), ctx.author.id)
						spins = await conn.fetchrow("SELECT spins FROM quirks WHERE userid=$1", ctx.author.id)
						spins = list(spins.values())[0] if spins else 0	
						await ctx.send("Spinning....")
						await asyncio.sleep(3)
						emb.description = f"You have now {spins} left in total"
						await ctx.send(f"{ctx.author.mention}, you got")
						await ctx.send(embed=emb)
					else:
						await ctx.send("You are out of spins!, use `t!daily` to claim more spins.")
				
			except Exception as e:
				print(e)
		else:
			await ctx.send("Postgres Database is not properly set")

	@commands.command(brief="Shows your current quirk", usage='t!quirk')
	async def quirk(self, ctx, user: discord.Member=None):
		conn = await main()
		if conn:
			user = ctx.author if not user else user
			try:
				row = await conn.fetchrow("SELECT quirk FROM quirks WHERE userid = $1", user.id)
				q = list(row.values())[0] if row else ''
				emb = discord.Embed()
				emb.set_author(icon_url=user.avatar_url, name=f"{str(user.name)}'s Quirk-")

				if not q:
					desc = "User hasn't spinned for a quirk yet, use `t!spin` to spin"
					color = discord.Color.blurple()

				elif q in common_qui:
					desc = '<:common:781895727654764565>  **Common**'
					color = discord.Color.lighter_grey()
				elif q in uncommon_qui:
					desc = '<:uncommon:781896517308252181>  **Uncommon**'
					color = discord.Color.green()

				elif q in rare_qui:
					desc = '<:rare:781896642885451797>  **Rare**'
					color = discord.Color.gold()

				elif q in legend_qui:
					desc = '<:legendary:781896293567823872>  **Legendary**'
					color = discord.Color.red()

				emb.add_field(name="Quirk name: ", value=f'**`{q}`**', inline=False)
				emb.add_field(name="Rarity: ", value=desc)
				emb.color = color
				await ctx.send(embed=emb)
			except Exception as e:
				print(e)
		else:
			await ctx.send("Postgres Database is not properly set")

	@commands.command(brief='Get the list of quirks available', usage='t!quirklist')
	async def quirklist(self, ctx):
		quirk_emb = discord.Embed(color=discord.Color.blurple())
		quirk_emb.add_field(name="<:common:781895727654764565>  Common quirks: ", value=', '.join(common_qui), inline=False)
		quirk_emb.add_field(name="<:uncommon:781896517308252181>  Uncommon quirks: ", value=', '.join(uncommon_qui), inline=False)
		quirk_emb.add_field(name="<:rare:781896642885451797>  Rare quirks: ", value=', '.join(rare_qui), inline=False)
		quirk_emb.add_field(name="<:legendary:781896293567823872>  Legendary quirks: ", value=', '.join(legend_qui), inline=False)

		await ctx.send(embed=quirk_emb)


	@commands.command(brief='Get the daily reward of spins', usage='t!daily')
	async def daily(self, ctx):
		conn = await main()
		if conn:
			check = await conn.fetchrow("SELECT * FROM quirks WHERE userid=$1", ctx.author.id)
			when_added = await conn.fetchrow("SELECT current FROM quirks WHERE userid=$1", ctx.author.id)
			now = datetime.now(tz=pytz.timezone('est'))
			emb = discord.Embed()
			s_count = random.randint(3, 6)
			spins = await conn.fetchrow("SELECT spins FROM quirks WHERE userid=$1", ctx.author.id)
			message = ''
			desc = ''
			delta = ''
			when_added = list(when_added.values())[0] if when_added else 0
			spins = list(spins.values())[0] if spins else 0

			if not check:
				spins = list(spins.values())[0] if spins else 0
				await conn.execute("INSERT INTO quirks(current, userid, spins) VALUES($1, $2, $3)",
								now, ctx.author.id, s_count)
				message = f"Here are your spins!, Come back tomorrow!"
				desc = f"You received {s_count} spins and now have a total of {spins+s_count} spins!"
				check = await conn.fetchrow("SELECT userid FROM quirks WHERE userid=$1", ctx.author.id)
			if not when_added and check:
				spins = list(spins.values())[0] if spins else 0
				await conn.execute("UPDATE quirks SET current=$1, spins=$2 WHERE userid=$3",
								now, s_count, ctx.author.id)
				message = "Here are your spins!,\nCome back tomorrow!"
				desc = f"You received {s_count} spins and now have a total of {spins+s_count} spins!"
			else:		
				delta = now - when_added
				if (delta.total_seconds())//3600 >= 24:
					await conn.execute("UPDATE quirks SET current=$1, spins=$2 WHERE userid=$3", now, spins+s_count, ctx.author.id)
					message = "Here are your spins!,\nCome back tomorrow!"
					desc = f"You received {s_count} spins and now have a total of {spins+s_count} spins!"
				else:
					message = f"You already claimed your spins for today~"
					desc = f"Come back in {23 - delta.seconds//3600} hours and {(60-(delta.seconds%3600)//60)} minutes"
			emb.title = message
			emb.description = desc
			emb.color = discord.Color.blurple()
			await ctx.send(ctx.author.mention, embed=emb)
		else:
			await ctx.send("Postgres Database is not properly set")

	@commands.command(brief="Get the amount of spins left", usage='t!spins')
	async def spins(self, ctx, user: discord.Member=None):
		conn = await main()
		if conn:
			user = ctx.author if not user else user
			spins = await conn.fetchrow("SELECT spins FROM quirks WHERE userid=$1", user.id)
			spins = list(spins.values())[0] if spins else 0

			sps = discord.Embed(title=f"{ctx.author.name}'s spin count\n{spins}", description="Use `t!daily` to get more spins daily")

			await ctx.send(embed=sps)
		else:
			await ctx.send("Postgres Database is not properly set")
		
def setup(bot: commands.bot):
	bot.add_cog(Fun(bot))