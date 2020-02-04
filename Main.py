#!/usr/bin/python3.8
import json
import os

from dotenv import load_dotenv

from discord.ext import commands
import Logger


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

Logger.start()

# initialize discord bot
bot = commands.Bot(command_prefix='&', description='description')

Moirail = {}

# saves variables to a json file


def save():
    with open('Moirail.json', 'w') as fp:
        print("Attemting save")
        json.dump(Moirail, fp)


try:
    with open('Moirail.json', 'r') as fp:
        Moirail = json.load(fp)
except json.decoder.JSONDecodeError:
    print("JSON failed to read the data might be corrupted")
except FileNotFoundError:
    print("No saves JSON found")

try:

    @bot.command(name="test", help="Responds with 'works!'")
    async def test(ctx):
        print('test triggered!')
        await ctx.message.send("works!")

    @bot.command(name="Moirail", help="Shows moirail counter for user")
    async def Moirail(ctx):
        await ctx.send(f"{ctx.author} was platonic"
                       f"{Moirail[ctx.author]} times")

    @bot.event
    async def on_ready():
        print(
            f'{bot.user} is connected to Discord\n'
            f'With {bot.command_prefix} as prefix\n'
            f"Can be mentioned with <@!{bot.user.id}>"
        )

    @bot.event
    async def on_connect():
        print("Connected!")

    @bot.event
    async def on_member_join(member):
        # set announcements as current channel
        channel = bot.get_channel(660987946085646367)
        await channel.send(f'Welcome {member.name}!')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        if '<>' in message.content:
            try:
                Moirail[message.author.username] += 1
            except KeyError:
                Moirail[message.author.username] = 1
        await bot.process_commands(message)
        # if message.content == f"<!@{bot.user.id}>":
        #    await message.channel.send(f"My prefix is {bot.command_prefix}")
        if message.content == f"{bot.command_prefix}help":
            await message.channel.send(bot.help_command.send_command_help())

    @bot.event
    async def on_error(event, *args, **kwargs):
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                raise
except Exception:  # Saves variables before quitting
    save()
    raise
