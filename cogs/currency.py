from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta
import asyncpg
import discord
import random
from discord.ext import commands

load_dotenv()

USERNAME = os.getenv("USERNAME")
HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
PASSWORD = os.getenv("PASSWORD")

common_qui = ['Engine', 'Voice', 'Gigantification', 'Hardening', 
    'Jet', 'Zero Gravity', 'Somnambulist', 'Navel Laser', 'Tail']
uncommon_qui = ['Air Propulsion', 'Electric', 'Warp gate',
    'Black hole', 'Permeation', 'Pop Off', 'Acid', 'Clones']
rare_qui = ['Dark Shadow', 'Cremation', 'Muscle Augmentation', 'Decay', 'Creation', 'Frog']
legend_qui = ['AFO', 'OFA', 'HHHC', 'Explosion', 'Overhaul', 'Fierce Wings', 'Hell flame']

shop_items = {"common spin": 3000, "uncommon spin": 50000, "rare spin": 150000}

class Database:
    def __init__(self):
        self.conn = None
        self.lock = asyncio.Lock()
        loop = asyncio.get_event_loop()
        loop.create_task(self.connect())

    async def connect(self):
         self.conn = await asyncpg.connect(host=HOST, user=USERNAME, database=DATABASE, password=PASSWORD)

    async def __aenter__(self):
        await self.lock.acquire()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()

class Currency(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	db = Database()

	@commands.group(brief='Gives you a random quirk', usage='t!spin [category (common, uncommon, rare)]')
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def spin(self, ctx):
		if not ctx.invoked_subcommand:
			await ctx.send("Category is not specified, Please provide which category to spin from, i.e `t!spin common`, `t!spin uncommon`, `t!spin rare`")
		
	@spin.command(brief="Get a random quirk from all categories, but chance of common quirk is the most",
				  usage="t!spin common")
	async def common(self, ctx):
		async with self.db as conn:
			await conn.execute("""CREATE TABLE IF NOT EXISTS quirks (
				username text,
				quirk text,
				c_spins integer,
				uc_spins integer,
				r_spins integer,
				userid bigint,
				current timestamptz,
				messages integer,
				guild bigint,
				yen bigint)""")
			if conn:
				emb = discord.Embed()
				i = random.randint(0, 100)
				quirk = ''
				if i <= 70:
					quirk = random.choice(common_qui)
					emb.title = f'__Common__ \n{quirk}'
					emb.color = discord.Color.lighter_grey()
				elif i <= 90:
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
						spins = await conn.fetchrow("SELECT c_spins FROM quirks WHERE userid=$1", ctx.author.id)
						spins = list(spins.values())[0] if spins else 0
						
						await conn.execute('''INSERT INTO quirks(username, quirk, userid) VALUES ($1, $2, $3)''',
										str(ctx.author), quirk, ctx.author.id)
						await ctx.send("Spinning....")
						await asyncio.sleep(3)
						if not spins:
							spins = 0				
						emb.description = f"You have now {spins} common spins left in total"
						await ctx.send(f"{ctx.author.mention}, you got")
						await ctx.send(embed=emb)
					else:
						spins = await conn.fetchrow("SELECT c_spins FROM quirks WHERE userid=$1", ctx.author.id)
						spins = list(spins.values())[0] if spins else 0
						if not spins:
							spins = 0	

						if spins > 0:
							await conn.execute('''UPDATE quirks SET quirk=$1, c_spins=$2, username=$3 WHERE userid=$4''',
											quirk, spins-1, str(ctx.author), ctx.author.id)
							spins = await conn.fetchrow("SELECT c_spins FROM quirks WHERE userid=$1", ctx.author.id)
							spins = list(spins.values())[0] if spins else 0	
							await ctx.send("Spinning....")
							await asyncio.sleep(3)
							emb.description = f"You have now {spins} common spins left in total"
							await ctx.send(f"{ctx.author.mention}, you got")
							await ctx.send(embed=emb)
						else:
							await ctx.send("You are out of common spins!, you can buy some from `t!shop`")
					
				except Exception as e:
					print(e)
			else:
				await ctx.send("Postgres Database is not properly set")
	@spin.command(brief="Get a random quirk from all categories except common, but chance of uncommon quirk is the most",
		  usage="t!spin uncommon")
	async def uncommon(self, ctx):
		async with self.db as conn:
			await conn.execute("""CREATE TABLE IF NOT EXISTS quirks (
				username text,
				quirk text,
				c_spins integer,
				uc_spins integer,
				r_spins integer,
				userid bigint,
				current timestamptz,
				messages integer,
				guild bigint,
				yen bigint)""")
			if conn:
				emb = discord.Embed()
				i = random.randint(0, 100)
				quirk = ''
				if i <= 70:
					quirk = random.choice(uncommon_qui)
					emb.title = f'__Uncommon__ \n{quirk}'
					emb.color = discord.Color.green()
				elif i <= 90:
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
						spins = await conn.fetchrow("SELECT uc_spins FROM quirks WHERE userid=$1", ctx.author.id)
						spins = list(spins.values())[0] if spins else 0
						if spins > 0:
							await conn.execute('''INSERT INTO quirks(username, quirk, userid) VALUES ($1, $2, $3)''',
											str(ctx.author), quirk, ctx.author.id)
							await ctx.send("Spinning....")
							await asyncio.sleep(3)
							if not spins:
								spins = 0				
							emb.description = f"You have now {spins} uncommon spins left in total"
							await ctx.send(f"{ctx.author.mention}, you got")
							await ctx.send(embed=emb)
						else:
							await ctx.send("You are out of uncommon spins!, you can buy some from `t!shop`")
					else:
						spins = await conn.fetchrow("SELECT uc_spins FROM quirks WHERE userid=$1", ctx.author.id)
						spins = list(spins.values())[0] if spins else 0
						if not spins:
							spins = 0	

						if spins > 0:
							await conn.execute('''UPDATE quirks SET quirk=$1, uc_spins=$2, username=$3 WHERE userid=$4''',
											quirk, spins-1, str(ctx.author), ctx.author.id)
							spins = await conn.fetchrow("SELECT uc_spins FROM quirks WHERE userid=$1", ctx.author.id)
							spins = list(spins.values())[0] if spins else 0	
							await ctx.send("Spinning....")
							await asyncio.sleep(3)
							emb.description = f"You have now {spins} uncommon spins left in total"
							await ctx.send(f"{ctx.author.mention}, you got")
							await ctx.send(embed=emb)
						else:
							await ctx.send("You are out of uncommon spins!, you can buy some from `t!shop`")
					
				except Exception as e:
					print(e)
			else:
				await ctx.send("Postgres Database is not properly set")

	@spin.command(brief="Get a random quirk from rare and legendary categories, but chance of rare quirk is the most",
		  usage="t!spin rare")
	async def rare(self, ctx):
		async with self.db as conn:
			await conn.execute("""CREATE TABLE IF NOT EXISTS quirks (
				username text,
				quirk text,
				c_spins integer,
				uc_spins integer,
				r_spins integer,
				userid bigint,
				current timestamptz,
				messages integer,
				guild bigint,
				yen bigint)""")
			if conn:
				emb = discord.Embed()
				i = random.randint(0, 100)
				quirk = ''

				if i <= 70:
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
						spins = await conn.fetchrow("SELECT r_spins FROM quirks WHERE userid=$1", ctx.author.id)
						spins = list(spins.values())[0] if spins else 0
						if spins > 0:
							await conn.execute('''INSERT INTO quirks(username, quirk, userid) VALUES ($1, $2, $3)''',
											str(ctx.author), quirk, ctx.author.id)
							await ctx.send("Spinning....")
							await asyncio.sleep(3)
							if not spins:
								spins = 0				
							emb.description = f"You have now {spins} rare spins left in total"
							await ctx.send(f"{ctx.author.mention}, you got")
							await ctx.send(embed=emb)
						else:
							await ctx.send("You are out of rare spins!, you can buy some from `t!shop`")
					else:
						spins = await conn.fetchrow("SELECT r_spins FROM quirks WHERE userid=$1", ctx.author.id)
						spins = list(spins.values())[0] if spins else 0
						if not spins:
							spins = 0	

						if spins > 0:
							await conn.execute('''UPDATE quirks SET quirk=$1, r_spins=$2, username=$3 WHERE userid=$4''',
											quirk, spins-1, str(ctx.author), ctx.author.id)
							spins = await conn.fetchrow("SELECT r_spins FROM quirks WHERE userid=$1", ctx.author.id)
							spins = list(spins.values())[0] if spins else 0	
							await ctx.send("Spinning....")
							await asyncio.sleep(3)
							emb.description = f"You have now {spins} rare spins left in total"
							await ctx.send(f"{ctx.author.mention}, you got")
							await ctx.send(embed=emb)
						else:
							await ctx.send("You are out of rare spins!, you can buy some from `t!shop`")
					
				except Exception as e:
					print(e)
			else:
				await ctx.send("Postgres Database is not properly set")

	@commands.command(brief="Shows your current quirk", usage='t!quirk')
	async def quirk(self, ctx, user: discord.Member=None):
		async with self.db as conn:
			await conn.execute("""CREATE TABLE IF NOT EXISTS quirks (
				username text,
				quirk text,
				c_spins integer,
				uc_spins integer,
				r_spins integer,
				userid bigint,
				current timestamptz,
				messages integer,
				guild bigint,
				yen bigint)""")
			if conn:
				user = ctx.author if not user else user
				try:
					row = await conn.fetchrow("SELECT quirk FROM quirks WHERE userid = $1", user.id)
					q = list(row.values())[0] if row else None
					emb = discord.Embed()
					emb.set_author(icon_url=user.avatar_url, name=f"{str(user.name)}'s Quirk-")

					if not q:
						desc = "User hasn't spinned for a quirk yet, use `t!spin [category]` to spin"
						color = discord.Color.blurple()

					elif q in common_qui:
						desc = '<:common:787616241119920129>  **Common**'
						color = discord.Color.lighter_grey()
					elif q in uncommon_qui:
						desc = '<:uncommon:787616344467963905>  **Uncommon**'
						color = discord.Color.green()

					elif q in rare_qui:
						desc = '<:rare:787616300356468766>  **Rare**'
						color = discord.Color.gold()

					elif q in legend_qui:
						desc = '<:legend:787617343114575884>  **Legendary**'
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
		quirk_emb.add_field(name="<:common:787616241119920129>  Common quirks: ", value=', '.join(common_qui), inline=False)
		quirk_emb.add_field(name="<:uncommon:787616344467963905>  Uncommon quirks: ", value=', '.join(uncommon_qui), inline=False)
		quirk_emb.add_field(name="<:rare:787616300356468766>  Rare quirks: ", value=', '.join(rare_qui), inline=False)
		quirk_emb.add_field(name="<:legend:787617343114575884>  Legendary quirks: ", value=', '.join(legend_qui), inline=False)

		await ctx.send(embed=quirk_emb)


	@commands.command(brief='Get the daily reward of spins', usage='t!daily')
	async def daily(self, ctx):
		try:
			async with self.db as conn:
				await conn.execute("""CREATE TABLE IF NOT EXISTS quirks (
					username text,
					quirk text,
					c_spins integer,
					uc_spins integer,
					r_spins integer,
					userid bigint,
					current timestamptz,
					messages integer,
					guild bigint,
					yen bigint)""")
				if conn:
					check = await conn.fetchrow("SELECT * FROM quirks WHERE userid=$1", ctx.author.id)
					when_added = await conn.fetchrow("SELECT current FROM quirks WHERE userid=$1", ctx.author.id)
					now = datetime.now(tz=pytz.timezone('est'))
					emb = discord.Embed()
					s_count = random.randint(10000, 15000)
					yen = await conn.fetchrow("SELECT yen FROM quirks WHERE userid=$1", ctx.author.id)
					message = ''
					desc = ''
					delta = ''
					when_added = list(when_added.values())[0] if when_added else 0
					if yen:
						yen = list(yen.values())[0]
					else:
						yen = 0

					if not check:
						if not yen:
							yen = 0
						await conn.execute("INSERT INTO quirks(current, userid, yen) VALUES($1, $2, $3)",
										now, ctx.author.id, s_count)
						message = f"Here is your yen!, Come back tomorrow!"
						desc = f"You received {s_count}¥ and now have a total of {yen+s_count} yen!"
						check = await conn.fetchrow("SELECT userid FROM quirks WHERE userid=$1", ctx.author.id)
					if not when_added and check:
						if not yen:
							yen = 0
						await conn.execute("UPDATE quirks SET current=$1, yen=$2 WHERE userid=$3",
										now, s_count, ctx.author.id)
						message = "Here is your yen!, Come back tomorrow!"
						desc = f"You received {s_count}¥ and now have a total of {yen+s_count} yen!"
					else:		
						delta = now - when_added
						if (delta.total_seconds())//3600 >= 24:
							await conn.execute("UPDATE quirks SET current=$1, yen=$2 WHERE userid=$3", now, yen+s_count, ctx.author.id)
							message = "Here is your yen!, Come back tomorrow!"
							desc = f"You received {s_count}¥ and now have a total of {yen+s_count} yen!"
						else:
							message = f"You already claimed your yen for today~"
							desc = f"Come back in {23 - delta.seconds//3600} hours and {(60-(delta.seconds%3600)//60)} minutes"
					emb.title = message
					emb.description = desc
					emb.color = discord.Color.blurple()
					await ctx.send(ctx.author.mention, embed=emb)
				else:
					await ctx.send("Postgres Database is not properly set")
		except Exception as e:
			print(e)

	@commands.command(brief="Get the amount of spins left", usage='t!spins')
	async def spins(self, ctx, user: discord.Member=None):
		try:
			async with self.db as conn:
				await conn.execute("""CREATE TABLE IF NOT EXISTS quirks (
					username text,
					quirk text,
					c_spins integer,
					uc_spins integer,
					r_spins integer,
					userid bigint,
					current timestamptz,
					messages integer,
					guild bigint,
					yen bigint)""")

				if conn:
					user = ctx.author if not user else user
					c_spins = await conn.fetchrow("SELECT c_spins FROM quirks WHERE userid=$1", user.id)
					uc_spins = await conn.fetchrow("SELECT uc_spins FROM quirks WHERE userid=$1", user.id)
					r_spins = await conn.fetchrow("SELECT r_spins FROM quirks WHERE userid=$1", user.id)
					c_spins = list(c_spins.values())[0] if c_spins else 0
					r_spins = list(r_spins.values())[0] if r_spins else 0
					uc_spins = list(uc_spins.values())[0] if uc_spins else 0

					sps = discord.Embed(title=f"{user.name}'s spin count", footer="You can buy more spins from the shop")
					sps.description = f"Common spins: {c_spins}\nUncommon spins: {uc_spins}\nRare spins: {r_spins}"

					await ctx.send(embed=sps)
				else:
					await ctx.send("Postgres Database is not properly set")
		except Exception as e:
			print(e)

	@commands.command(brief="See the items available in shop", usage="t!shop", aliases=("market", "shp"))
	async def shop(self, ctx):
		try:
			shop_items_dict_ = {"<:common:787616241119920129> Common spins": "3,000¥",
				  "<:uncommon:787616344467963905> Uncommon spins": "50,000¥",
				  "<:rare:787616300356468766> Rare spins": "150,000¥"}
			colors = [discord.Color.blurple(),
					  discord.Color.green(),
					  discord.Color.blue(),
					  discord.Color.magenta(),
					  discord.Color.teal(),
					  discord.Color.purple()]

			shop_emb = discord.Embed(title=":moneybag: Shop :moneybag:", color=random.choice(colors))
			for i in shop_items_dict_:
				shop_emb.add_field(name=i, value=shop_items_dict_[i], inline=False)
			shop_emb.description = "Use `t!buy [amount] [item]` to buy an item"
			await ctx.send(embed=shop_emb)
		except Exception as e:
			print(e)

	@commands.command(brief="Buy an item available in the shop", usage="t!buy [item]")
	async def buy(self, ctx, amount: int, *, item):
		async with self.db as conn:
			if amount < 1 or not isinstance(amount, int):
				await ctx.send("Nice try :p")
				return
			await conn.execute("""CREATE TABLE IF NOT EXISTS quirks (
				username text,
				quirk text,
				c_spins integer,
				uc_spins integer,
				r_spins integer,
				userid bigint,
				current timestamptz,
				messages integer,
				guild bigint,
				yen bigint)""")
			try:
				item = item.lower().strip("s")
				yen_count = await conn.fetchrow("SELECT yen FROM quirks WHERE userid=$1", ctx.author.id)
				if not any(item in i for i in shop_items):
					await ctx.send("Invalid Item")
				else:
					yen_count = list(yen_count.values())[0] if yen_count else 0

					if not yen_count:
						yen_count = 0
					
					if "common" in item:
						spin_count = await conn.fetchrow("SELECT c_spins FROM quirks WHERE userid=$1", ctx.author.id)
						spin_count = list(spin_count.values())[0] if list(spin_count.values())[0] else 0
						if yen_count >= shop_items[item] * amount:
							new_yen = yen_count - amount * shop_items[item]
							await conn.execute("UPDATE quirks SET yen=$1, c_spins=$3 WHERE userid=$2",
							 				   new_yen, ctx.author.id, spin_count+amount)
							await ctx.send(f"You bought {amount} common spins for {shop_items[item] * amount} yen")
						else:
							await ctx.send(f"You don't have enough yen to buy this, you need {amount*shop_items[item]-yen_count}¥ more yen")
					
					elif "uncommon" in item:
						spin_count = await conn.fetchrow("SELECT uc_spins FROM quirks WHERE userid=$1", ctx.author.id)
						spin_count = list(spin_count.values())[0] if list(spin_count.values())[0] else 0
						if yen_count >= shop_items[item] * amount:
							new_yen = yen_count - amount * shop_items[item]
							await conn.execute("UPDATE quirks SET yen=$1, uc_spins=$3 WHERE userid=$2",
							 				   new_yen, ctx.author.id, spin_count+amount)
							await ctx.send(f"You bought {amount} uncommon spins for {shop_items[item] * amount} yen")
						else:
							await ctx.send(f"You don't have enough yen to buy this, you need {amount*shop_items[item]-yen_count}¥ more yen")

					elif "rare" in item:
						spin_count = await conn.fetchrow("SELECT r_spins FROM quirks WHERE userid=$1", ctx.author.id)
						spin_count = list(spin_count.values())[0] if list(spin_count.values())[0] else 0
						if yen_count >= shop_items[item] * amount:
							new_yen = yen_count - amount * shop_items[item]
							await conn.execute("UPDATE quirks SET yen=$1, r_spins=$3 WHERE userid=$2",
							 				   new_yen, ctx.author.id, spin_count+amount)
							await ctx.send(f"You bought {amount} rare spins for {shop_items[item] * amount} yen")
						else:
							await ctx.send(f"You don't have enough yen to buy this, you need {amount*shop_items[item]-yen_count}¥ more yen")
			except Exception as e:
				print(e)

	@commands.command(brief="Get the wallet status of a user", usage="t!yen [user (optional)]", aliases=("money", "yen"))
	async def wallet(self, ctx, user: discord.Member=None):
		async with self.db as conn:
			await conn.execute("""CREATE TABLE IF NOT EXISTS quirks (
				username text,
				quirk text,
				c_spins integer,
				uc_spins integer,
				r_spins integer,
				userid bigint,
				current timestamptz,
				messages integer,
				guild bigint,
				yen bigint)""")
			try:
				user = ctx.author if not user else user
				yen_left = await conn.fetchrow("SELECT yen FROM quirks WHERE userid=$1", user.id)
				yen_left = list(yen_left.values())[0] if yen_left else 0
				
				if not user or user not in ctx.guild.members:
					await ctx.send("Invalid user")
					return
				if not yen_left:
					yen_left = 0
					await conn.execute("INSERT INTO quirks(userid, yen) VALUES($1, $2)", user.id, 0)


				yen_emb = discord.Embed(title=f"{user.name}'s wallet", color=user.color)
				yen_emb.description = f"Yen amount: {yen_left} ¥"
				yen_emb.set_footer(text="Use t!daily to get more yen daily") 
				await ctx.send(embed=yen_emb)
			except Exception as e:
				print(e)

	@commands.command(brief="Donate some yen to a person", usage="t!donate [user] [amount]", aliases=("give", "don"))
	async def donate(self, ctx, user: discord.Member, amount: int):
		async with self.db as conn:
			await conn.execute("""CREATE TABLE IF NOT EXISTS quirks (
				username text,
				quirk text,
				c_spins integer,
				uc_spins integer,
				r_spins integer,
				userid bigint,
				current timestamptz,
				messages integer,
				guild bigint,
				yen bigint)""")
			if not user or user not in ctx.guild.members:
				await ctx.send("Invalid user")
				return
			if amount < 1:
				await ctx.send("Amount cannot be less than 1")
				return
			author_amount = await conn.fetchrow("SELECT yen FROM quirks WHERE userid=$1", ctx.author.id)
			user_amount = await conn.fetchrow("SELECT yen FROM quirks WHERE userid=$1", user.id)
			author_amount = list(author_amount.values())[0] if author_amount else 0
			user_amount = list(user_amount.values())[0] if user_amount else 0
			if not user_amount:
				user_amount = 0
				await conn.execute("INSERT INTO quirks(userid, yen) VALUES($1, $2)", user.id, 0)
			if not author_amount:
				author_amount = 0
				await conn.execute("INSERT INTO quirks(userid, yen) VALUES($1, $2)", ctx.author.id, 0)

			if author_amount < amount:
				await ctx.send("You don't have that much yen to give")
				return
			await conn.execute("UPDATE quirks SET yen=$1 WHERE userid=$2", amount + user_amount, user.id)
			await conn.execute("UPDATE quirks SET yen=$1 WHERE userid=$2", author_amount - amount, ctx.author.id)

			await ctx.send(f"You gave {user.name} **{amount}**¥ yen, now you have {author_amount - amount} and they have {user_amount + amount}")


def setup(bot: commands.bot):
	bot.add_cog(Currency(bot))
