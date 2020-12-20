import discord
import random
import json
from discord.ext import commands
from cogs.currency import USERNAME, HOST, DATABASE, PASSWORD
import asyncio
import asyncpg

with open("resources/moves.json") as moves:
	moves = json.load(moves)

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

class Fun(commands.Cog):

	def __init__(self, bot: commands.bot):
		self.bot = bot

	db = Database()

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
	@commands.command(brief="Fight someone with your quirk", usage="t!fight [user]", aliases=("duel", "fgt"))
	async def fight(self, ctx, user: discord.Member=None):
		if not user:
			await ctx.send("You need to provide a user")
			return
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
			quirk1 = await conn.fetchrow("SELECT quirk FROM quirks WHERE userid=$1", ctx.author.id)
			quirk2 = await conn.fetchrow("SELECT quirk FROM quirks WHERE userid=$1", user.id)
			if not quirk1:
				await ctx.send("You don't have a quirk to fight with, you can spin for one by `t!spin [category]`")
				return
			if not quirk2:
				await ctx.send("Opponent doesn't have a quirk to fight with, they can spin for one by `t!spin [category]`")
				return
			quirk1, quirk2 = list(quirk1.values())[0], list(quirk2.values())[0]

			player1 = {"member": ctx.author, 
					   "health": 100,
					   "quirk": quirk1}
			player2 = {"member": user,
			 		   "health": 100,
			 		   "quirk": quirk2}

			player1.update({"moves": [f"{c+1}. {i['Name']}" for c, i in enumerate(moves[player1["quirk"]])],
			 		   		"damage": [i["Damage"] for i in moves[player1["quirk"]]],
			 		   		"cooldown": [i["Cooldown"] for i in moves[player1["quirk"]]],
			 		   		"serial": [c+1 for c in range(len(moves[player1["quirk"]]))]})

			player2.update({"moves": [f"{c+1}. {i['Name']}" for c, i in enumerate(moves[player2["quirk"]])],
			 		   		"damage": [i["Damage"] for i in moves[player2["quirk"]]],
			 		   		"cooldown": [i["Cooldown"] for i in moves[player2["quirk"]]],
			 		   		"serial": [c+1 for c in range(len(moves[player2["quirk"]]))]})

			switch = {player1: player2, player2: player1}
			current_p = random.choice(list(switch.keys()))
			dmg = random.randint(current_p["damage"][0], current_p["damage"][0])
			c_moves = "\n".join(current_p["moves"])
			count = 1
			resp = ''

			await ctx.send(f"The fight begins!, first chance goes to {current_p['member'].mention}")
			while True:
				emb = discord.Embed()
				if player1["Health"] <= 0:
					emb.description = f"{ctx.author.name} Lost the match! Winner is {user.name}"
					break
				if player2["Health"] <= 0:
					emb.description = f"{user.name} Lost the match! Winner is {ctx.author.name}"
					break
				emb.title = f"{str(current_p['member'])}"
				c_moves = "\n".join(current_p["moves"])
				emb.description = f"Available moves {c_moves}"
				emb.set_footer(text="Choose one of the available moves by sending the serial number in the chat")
				await ctx.send(embed=emb)
				def check(m):
					try:
						int(m.content)
						return m.author == current_p["member"]
					except ValueError:
						return False
				try:
					resp = await self.bot.wait_for("message", check=check, timeout=75.0)
					if resp in current_p["serial"]:
						dmg = random.randint(current_p["damage"][int(resp-1)][0], current_p["damage"][int(resp)-1][1])
						switch[current_p]["health"] -= dmg
						await ctx.send(f'{current_p["member"].name} used {current_p["moves"][int(resp)-1][3:]} on {switch[current_p]["member"].name}')
						await ctx.send(f"{switch[current_p]['member'].name}'s health is now {switch[current_p]['health']} and {current_p['member'].name}'s health is now {current_p['health']}")
					count += 1
					current_p = switch[current_p]
				except:
					await ctx.send(f"{current_p['member']} didn't answer in time, {switch[current_p]['member'].mention} wins")

		
def setup(bot: commands.bot):
	bot.add_cog(Fun(bot))