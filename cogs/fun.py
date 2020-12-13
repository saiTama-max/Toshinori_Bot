import discord
import random
import async_cleverbot as ac
from discord.ext import commands


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
		
def setup(bot: commands.bot):
	bot.add_cog(Fun(bot))