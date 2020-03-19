#!/usr/bin/python3.8
import atexit
import json
import os
import discord

from dotenv import load_dotenv
import git

import Logger
from discord.ext import commands

import Database as db

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

Logger.start()

# initialize discord bot
bot = commands.Bot(command_prefix='%', description='A Bot which does a thing',
                   case_insensitive=True)

MoirailCounter = {}


def save():
    # Commits to Database
    print("Attemting save")
    db.SQL.commit()


try:
    with open('Moirail.json', 'r') as fp:
        MoirailCounter = json.load(fp)
except json.decoder.JSONDecodeError:
    print("JSON failed to read the data might be corrupted")
except FileNotFoundError:
    print("No JSON saves found")

try:

    @bot.command(name="test", help="Responds with 'works!'")
    async def test(ctx: commands.Context):
        print('test triggered!')
        await ctx.send("works!")

    @bot.command(name="Moirail", help="Shows moirail counter for user",
                 aliases=["m"])
    async def Moirail(ctx: commands.Context, *arg):
        if arg == ():  # if no argument is passed go with sender
            user = ctx.author.id
        else:
            user = arg[0].strip('<!@> ')
        try:
            MoirailV = (db.QueryID(user))[0]
        except TypeError:
            await ctx.send("No record for this user")
            return
        await ctx.send(
            f"""{bot.get_user(user).mention} was platonic {MoirailV} times""")

    @bot.command(name="Description", help="Shows basic info about bot",
                 aliases=["info", "desc", "i"])
    async def description(ctx: commands.Context):
        await ctx.send(f'''```{bot.user}:{bot.description}
        You can ask for {bot.command_prefix}help
        Further information can be found on the github:
        https://github.com/Saragon4005/Discord-Chatbot
        ```''')

    @bot.command(name="Git Pull", help="Updates bot from github repository",
                 aliases=["pull", "update"])
    async def gitPull(ctx: commands.Context):
        if ctx.author.id == 212686680052727814:
            repo = git.Repo('')
            repo.remotes.origin.pull()
        else:
            await ctx.send("You are not allowed to do that")
            print(f"{ctx.author.id} attemped pull")

    @bot.command(name="Owner",
                 help="Checks if you are allowed to do owner operations",
                 aliases=["sudo", "su", "root"])
    async def owner(ctx: commands.Context):
        if ctx.author.id == 212686680052727814:
            await ctx.send("You are owner")
        else:
            await ctx.send("You are not owner")

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
    async def on_member_join(member: discord.Member):
        # set announcements as current channel
        channel = bot.get_channel(660987946085646367)
        await channel.send(f'Welcome {member.name}!')

    @bot.event
    async def on_message(message: discord.Message):
        if message.author == bot.user:
            return
        if '<>' in message.content:
            try:
                MoirailV = (db.QueryID(message.author.id))[0] + 1
                db.update(f"Moirail = {MoirailV}", f"Id = {message.author.id}")
            except TypeError:
                db.c.execute(f'''INSERT INTO Users(id, Moirail)
                                 Values({message.author.id},1)''')
            finally:
                db.SQL.commit()
        try:
            await bot.process_commands(message)
        except AttributeError:
            print("Could not process commands \n"
                  "This is could be due to bot not being started \n"
                  "This is normal for testing")

    @bot.event
    async def on_error(event, *args, **kwargs):
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                raise

    @bot.event
    async def on_command_error(ctx, error):
        await ctx.send(error)
        print(error)

except Exception:  # Saves variables before quitting
    save()
    raise


def exit_handler():
    save()


atexit.register(exit_handler)
