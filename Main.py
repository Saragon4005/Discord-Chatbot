#!/usr/bin/python3.8
import atexit
import json
import os

from dotenv import load_dotenv
import git

import Logger
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

Logger.start()

# initialize discord bot
bot = commands.Bot(command_prefix='%', description='A Bot which does a thing',
                   case_insensitive=True)

MoirailCounter = {}

# saves variables to a json file


def save():
    with open('Moirail.json', 'w') as fp:
        print("Attemting save")
        json.dump(MoirailCounter, fp)


try:
    with open('Moirail.json', 'r') as fp:
        MoirailCounter = json.load(fp)
except json.decoder.JSONDecodeError:
    print("JSON failed to read the data might be corrupted")
except FileNotFoundError:
    print("No JSON saves found")

try:

    @bot.command(name="test", help="Responds with 'works!'")
    async def test(ctx):
        print('test triggered!')
        await ctx.send("works!")

    @bot.command(name="Moirail", help="Shows moirail counter for user",
                 aliases=["m"])
    async def Moirail(ctx):
        await ctx.send(
            f"{ctx.author.name} was platonic "
            f"{MoirailCounter[ctx.author.name]} times")

    @bot.command(name="Description", help="Shows basic info about bot",
                 aliases=["info", "desc", "i"])
    async def description(ctx):
        await ctx.send(f'''```{bot.user}:{bot.description}
        You can ask for {bot.command_prefix}help
        Further information can be found on the github:
        https://github.com/Saragon4005/Discord-Chatbot
        ```''')

    @bot.command(name="Git Pull", help="Updates bot from github repository",
                 aliases=["pull", "update"])
    async def gitPull(ctx):
        if ctx.author.id == 212686680052727814:
        repo = git.Repo('')
        repo.remotes.origin.pull()

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
                MoirailCounter[message.author.name] += 1
            except KeyError:
                MoirailCounter[message.author.name] = 1
        try:
            await bot.process_commands(message)
        except AttributeError:
            print("Could not process commands \n"
                  "This is could be due to bot not being started \n"
                  "This is normal for testing")
        # if message.content == f"<!@{bot.user.id}>":
        #    await message.channel.send(f"My prefix is {bot.command_prefix}")

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


def exit_handler():
    save()


atexit.register(exit_handler)
