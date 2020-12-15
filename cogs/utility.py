import discord
import random
from discord.ext import commands
from io import BytesIO
import aiohttp
from urllib import parse
from collections import Counter
import numpy as np
from PIL import Image
import datetime
from dateutil.relativedelta import relativedelta
import asyncpg
# from cogs.currency import USERNAME, HOST, DATABASE, PASSWORD
import asyncio
from matplotlib import pyplot as plt


QUOTES = [
    "Get busy living or get busy dying.",
    "You only live once, but if you do it right, once is enough.",
    "Many of life’s failures are people who did not realize how close they were to success when they gave up.",
    "If you want to live a happy life, tie it to a goal, not to people or things.",
    "Not how long, but how well you have lived is the main thing.",
    "If life were predictable it would cease to be life, and be without flavor.",
    "The greatest glory in living lies not in never falling, but in rising every time we fall.",
    "The way to get started is to quit talking and begin doing.",
    "If you look at what you have in life, you'll always have more. If you look at what you don't have in life, you'll never have enough.",
    "If you set your goals ridiculously high and it's a failure, you will fail above everyone else's success.",
    "When you reach the end of your rope, tie a knot in it and hang on.",
    "Spread love everywhere you go. Let no one ever come to you without leaving happier.",
    "It is during our darkest moments that we must focus to see the light.",
    "Do not go where the path may lead, go instead where there is no path and leave a trail.",
    "Success usually comes to those who are too busy to be looking for it.",
    "If you really look closely, most overnight successes took a long time.",
    "The only place where success comes before work is in the dictionary.",
    "If you are not willing to risk the usual, you will have to settle for the ordinary." ,
    "Whether you think you can or you think you can't, you're right." ,
    "The question isn't who is going to let me; it's who is going to stop me.",
    "Everything you've ever wanted is on the other side of fear.",
    "Dream big and dare to fail.",
    "You may be disappointed if you fail, but you are doomed if you don't try.",
    "It does not matter how slowly you go as long as you do not stop.",
    "I didn't fail the test. I just found 100 ways to do it wrong."]


# class Database:
#     def __init__(self):
#         self.conn = None
#         self.lock = asyncio.Lock()
#         loop = asyncio.get_event_loop()
#         loop.create_task(self.connect())

#     async def connect(self):
#          self.conn = await asyncpg.connect(host=HOST, user=USERNAME, database=DATABASE, password=PASSWORD)

#     async def __aenter__(self):
#         await self.lock.acquire()
#         return self.conn

#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         self.lock.release()

class Utility(commands.Cog):

    def __init__(self, bot: commands.bot):
        self.bot = bot

    
    @staticmethod
    def get_time(a: datetime.datetime, b: datetime.datetime) -> list:
        try:
            final = []
            delta = relativedelta(a, b)
            years = abs(delta.years)
            months = abs(delta.months)
            days = abs(delta.days)
            hours = abs(delta.hours)
            minutes = abs(delta.minutes)

            if minutes and not months and not years:
                final.append(f'{minutes} minutes')

            if hours:
                final.append(f'{hours} hours')

            if days:
                final.append(f'{days} days')

            if months:
                final.append(f'{months} months')
            
            if years:
                final.append(f'{years} years')
            final = final[::-1]
            return final[:3]
        except Exception as e:
            print(e)

    @commands.command(brief='gives nice and motivational codes', usage='t!quote')
    async def quote(self, ctx):
        embed_quote = discord.Embed(title="Quote", description=random.choice(QUOTES), color=discord.Color.green())
        await ctx.send(embed=embed_quote)
        
    @commands.command(brief='Get the latency of the bot', usage='t!ping')
    async def ping(self, ctx):
        ping_emb = discord.Embed(title="Pong! 🏓",
                                 description=f'Ping is {round(self.bot.latency  * 1000)}ms',
                                 color=discord.Color.blurple())
        await ctx.send(embed=ping_emb)

    @commands.command(brief='Get the info about the user',
                    usage='t!userinfo [user (optional)]',
                    aliases=['ui', 'user', 'uinfo', 'useri'])
    async def userinfo(self, ctx, user: discord.Member=None):

        hypesquad = {'hypesquad_bravery': '<:bravery:784430728683323392>',
                     'hypesquad_brilliance': '<:brilliance:784430705118806036>',
                     'hypesquad_balance': '<:balance:784430681857720332>',}
        try:
            user = ctx.author if not user else user
            pfp = user.avatar_url
            created_time = self.get_time(datetime.datetime.utcnow(), user.created_at) 
            badges = user.public_flags

            joined_time = self.get_time(datetime.datetime.utcnow(), user.joined_at)
            info_emb = discord.Embed(color=user.color,
                                     title=str(user))
            if badges.hypesquad_bravery:
                info_emb.description = hypesquad['hypesquad_bravery']

            elif badges.hypesquad_brilliance:
                info_emb.description = hypesquad['hypesquad_brilliance']

            elif badges.hypesquad_balance:
                info_emb.description = hypesquad['hypesquad_balance']

            roles = []

            for i in user.roles[1:]:
                roles.append(f"<@&{i.id}>")
            roles = ', '.join(roles)

            statuses = {discord.Status.online: '<:online:782636673653407744>',
                        discord.Status.offline: '<:offline:782636856075616286>',
                        discord.Status.idle: '<:3929_idle:782638272483950623>',
                        discord.Status.dnd: '<:dnd:782637101464027136>'}

            info_emb.set_thumbnail(url=pfp)
            info_emb.add_field(name='User Information', value=f'Created: {", ".join(created_time)} ago\nProfile: {user.mention}\nID: {user.id}', inline=False)
            info_emb.add_field(name="Guild Profile", value=f"Joined: {', '.join(joined_time)} ago\nNickname: {user.nick}\nRoles: {roles}", inline=False)
            info_emb.add_field(name="Status", value=f'{statuses[user.mobile_status]} Mobile Client\n{statuses[user.web_status]} Web Client\n{statuses[user.desktop_status]} Desktop Client')

            await ctx.send(embed=info_emb)
        except Exception as e:
            print(e)
    # db = Database()
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     async with self.db as conn:
    #         await conn.execute("""CREATE TABLE IF NOT EXISTS quirks (
    #             username text,
    #             quirk text,
    #             c_spins integer,
    #             uc_spins integer,
    #             r_spins integer,
    #             userid bigint,
    #             current timestamptz,
    #             messages integer,
    #             guild bigint,
    #             yen bigint)""")

    #         if message.author == self.bot.user:
    #             return
    #         try:
    #             if conn:
    #                 check = await conn.fetchrow("SELECT userid FROM quirks WHERE userid=$1", message.author.id)
    #                 if not check:
    #                     await conn.execute("INSERT INTO quirks(userid, guild, messages) VALUES($1, $2, 1)",
    #                                        message.author.id, message.guild.id)
                    
    #                 else:
    #                     guild = await conn.fetch("SELECT guild FROM quirks WHERE userid=$1", message.author.id)
    #                     guild = [list(i.values()) for i in guild]
    #                     msg_count = await conn.fetchrow("SELECT messages FROM quirks WHERE userid=$1 AND guild=$2",
    #                                                     message.author.id, message.guild.id)
    #                     if msg_count:
    #                         msg_count = list(msg_count.values())[0] if list(msg_count.values())[0] else 0
    #                     else:
    #                         msg_count = 0
    #                     msg_count += 1
    #                     if [message.guild.id] in guild:
    #                         await conn.execute("UPDATE quirks SET messages=$3 WHERE userid=$1 AND guild=$2",
    #                                      message.author.id, message.guild.id, msg_count)
    #                     else:
    #                         await conn.execute("INSERT INTO quirks(userid, guild, messages) VALUES($1, $2, 1)",
    #                                        message.author.id, message.guild.id)
    #                 # await conn.close()
    #         except Exception as e:
    #             print(e)
            

    # @commands.command(brief="Show the top for people with the most messages in a guild",
    #                   usage="t!top",
    #                   aliases=('lb', 'leaderboard'))
    # async def top(self, ctx):
    #     async with self.db as conn:
    #         await conn.execute("""CREATE TABLE IF NOT EXISTS quirks (
    #             username text,
    #             quirk text,
    #             c_spins integer,
    #             uc_spins integer,
    #             r_spins integer,
    #             userid bigint,
    #             current timestamptz,
    #             messages integer,
    #             guild bigint,
    #             yen bigint)""")
    #         msgs = await conn.fetch("SELECT userid, messages FROM quirks WHERE guild=$1", ctx.guild.id)
    #         msgs = set(msgs)
    #         m_count = dict()
    #         for i in msgs:
    #             m_count.update({str(self.bot.get_user(list(i.values())[0])): list(i.values())[1]})
    #         m_count = {k: m_count[k] for k in sorted(m_count, key=lambda y: m_count[y])}
    #         msg_count = tuple(m_count.values())[::-1]
    #         name = tuple(m_count.keys())[::-1]

    #         fin = []
    #         c = 1
            
    #         for i in range(10):
    #             try:
    #                 fin.append(f"{c}. {name[i]}{' '*(25-len(name[i]))} - {msg_count[i]}")
    #                 c += 1
    #             except:
    #                 continue
    #         fin = "\n".join(fin)
    #         if fin:
    #             await ctx.send(f"```css\n{fin}```")
    #         else:
    #             await ctx.send("No messages yet")
    
    # @commands.command(brief="Get a graph based on the top messages in the guild",
    #                   usage="t!graph",
    #                   aliases=("topg", "topgraph", "tgraph"))
    # async def graph(self, ctx):
    #     try:
    #         async with self.db as conn:
    #             await conn.execute("""CREATE TABLE IF NOT EXISTS quirks (
    #                 username text,
    #                 quirk text,
    #                 c_spins integer,
    #                 uc_spins integer,
    #                 r_spins integer,
    #                 userid bigint,
    #                 current timestamptz,
    #                 messages integer,
    #                 guild bigint,
    #                 yen bigint)""")
    #             msgs = await conn.fetch("SELECT userid, messages FROM quirks WHERE guild=$1", ctx.guild.id)
    #             msgs = set(msgs)
    #             m_count = dict()
    #             for i in msgs:
    #                 m_count.update({str(self.bot.get_user(list(i.values())[0])): list(i.values())[1]})
    #             m_count = {k: m_count[k] for k in sorted(m_count, key=lambda y: m_count[y])}
    #             msg_count_y = list(m_count.values())[::-1]
    #             name_x = list(m_count.keys())[::-1]

    #             # plt.style.use("fivethirtyeight")
    #             fig, ax = plt.subplots(figsize =(16, 9))

    #             ax.barh(name_x, msg_count_y, color="#444444", edgecolor="#817E7E")
    #             for s in ['top', 'bottom', 'left', 'right']:
    #                 ax.spines[s].set_visible(False)

    #             ax.xaxis.set_ticks_position('none')
    #             ax.yaxis.set_ticks_position('none')

    #             ax.grid(b=True, color='#545454',
    #                     linestyle='-.', linewidth=0.5,
    #                     alpha=0.2)

    #             ax.invert_yaxis()

    #             for i in ax.patches:
    #                 plt.text(i.get_width() + 20, i.get_y() + 0.5,
    #                          str(round((i.get_width()), 2)),
    #                          fontsize=12, fontweight='bold',
    #                          color='grey')
    #             plt.title(f"Top messages in {ctx.guild.name}")
    #             plt.ylabel("Names")
    #             plt.xlabel("Message count")

    #             # plt.tight_layout()

    #             plt.savefig("images/graph.png")

    #             await ctx.send(file=discord.File("images/graph.png"))
    #     except Exception as e:
    #         print(e)

def setup(bot: commands.bot):
    bot.add_cog(Utility(bot))
