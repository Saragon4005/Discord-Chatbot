#!/usr/bin/python3.8
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import Logger
import json


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

Logger.start()

client = discord.Client()

bot = commands.Bot(command_prefix='!')

Moirail = {}
with open('Moirail.json', 'r') as fp:
    Moirail = json.load(fp)


def save():
    with open('Moirail.json', 'w') as fp:
        json.dump(Moirail, fp)


try:
    @bot.command(name="Test", help="Responds with 'works!'")
    async def test(ctx):
        await ctx.send("works!")

    @client.event
    async def on_ready():
        for guild in client.guilds:
            if guild.name == GUILD:
                break

        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

    @client.event
    async def on_connect():
        print("Connected!")

    @client.event
    async def on_member_join(member):
        channel = client.get_channel(660987946085646367)
        await channel.send(f'Welcome {member.name}!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content.startswith('!test'):
            await message.channel.send('works!')
        if message.content.incudes('<>'):
            Moirail[message.author] += 1

    @client.event
    async def on_error(event, *args, **kwargs):
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                raise
except:
    save()
    raise


client.run(TOKEN)
bot.run(TOKEN)
