# bot.py
from keep_alive import keep_alive
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import timedelta
from datetime import datetime, date

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
print("hello")
bot = commands.Bot(command_prefix='$')

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
chainPend = False
chainKeys = []
chainChannels = []

@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return
    #chain
    if message.content == "chain on":
        await message.channel.send("send key")
        def check(m):
            return m.author == message.author and m.channel == message.channel
        msg = await bot.wait_for('message', check=check)
        chainKeys.append(msg.content)
        chainChannels.append(message.channel)
        #chainPend = True
        return
    elif message.content == "chain off": 
        await message.channel.send("k")
        index = chainChannels.index(message.channel)
        chainChannels.pop(index)
        chainKeys.pop(index)
        return
    if len(chainChannels) != 0:#and chainPend == False:
        if message.channel in chainChannels and message.content != chainKeys[chainChannels.index(message.channel)]:
            await message.channel.send(f'{message.author} broke the chain!')
    await bot.process_commands(message)


def get_mentions(message):
    ret = []
    for user in message.mentions:
        ret.append(user.name)
    for role in message.role_mentions:
        ret.append(role.name)
    return ret

@bot.event
async def on_message_delete(message):
    early = message.created_at;
    if(message.edited_at != None):
      early = message.edited_at
    delta = timedelta( seconds=12 )
    now = datetime.utcnow()
    if(now - early < delta and (message.mentions or message.mention_everyone)):
        embed=discord.Embed(title="Ghost Ping Found!")
        embed.add_field(name="Sender", value=message.author)
        if(len(message.content) >= 1024):
            embed.add_field(name="Mentions", value=get_mentions(message))
        else: 
            embed.add_field(name="Message", value=message.content)
        await message.channel.send(embed=embed)

    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Error')





keep_alive()
bot.run(TOKEN)





