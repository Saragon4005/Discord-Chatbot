#!/usr/bin/python3.8
import atexit
import os
import discord

from dotenv import load_dotenv
import git

import Logger
from discord.ext import commands

import Database as db
from datetime import datetime, timedelta, timezone

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

Logger.start()

# initialize discord bot
bot = commands.Bot(command_prefix='%', description='A Bot which does a thing',
                   case_insensitive=True)


def updateSettings():  # TODO
    pass


updateSettings()


def isOwner(id):
    if id == 212686680052727814:
        return(True)
    else:
        return(False)


def supression(m):
    suppress = ["693964315790934098", "clo9d"]
    for i in suppress:
        if m in i:
            return(True)
    return(False)


def getUser(ctx, *arg):
    if arg == ():  # if no argument is passed go with sender
        return(ctx.author.id)
    else:
        return(arg[0].strip('<!@> '))  # remove metion parts


def save():
    # Commits to Database
    print("Attemting save")
    db.SQL.commit()


try:

    @bot.command(name="test", help="Responds with 'works!'")
    async def test(ctx: commands.Context):
        print('test triggered!')
        await ctx.send("works!")

    @bot.command(name="Moirail", help="Shows moirail counter for user",
                 aliases=["m"])
    async def Moirail(ctx: commands.Context, *arg):
        user = getUser(ctx, *arg)
        try:
            MoirailV = (db.QueryMoirail(user))[0]
            await ctx.send(f"{bot.get_user(int(user)).mention} "
                           f"was platonic {MoirailV} times")
        except TypeError:
            await ctx.send("No record for this user")

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
        if isOwner(ctx.author.id):
            repo = git.Repo('')
            repo.remotes.origin.pull()
        else:
            await ctx.send("You are not allowed to do that")
            print(f"{ctx.author.id} attemped pull")

    @bot.command(name="Owner",
                 help="Checks if you are allowed to do owner operations",
                 aliases=["sudo", "su", "root"])
    async def owner(ctx: commands.Context):
        if isOwner(ctx.author.id):
            await ctx.send("You are owner")
        else:
            await ctx.send("You are not owner")

    @bot.command(name="Stats")
    async def stats(ctx: commands.Context, *arg):
        Timezone = timezone(timedelta(hours=-7))
        user = getUser(ctx, *arg)
        info = [int(round(float(i))) for i in db.QueryUser(user)]
        seenTZ = datetime.fromtimestamp(info[1]).astimezone(Timezone)
        lastMesseageTZ = datetime.fromtimestamp(info[2]).astimezone(Timezone)
        seen = seenTZ.strftime("%m/%d/%Y, %H:%M:%S")
        lastMesseage = lastMesseageTZ.strftime("%m/%d/%Y, %H:%M:%S")

        await ctx.send(f'{bot.get_user(int(user)).mention} '
                       f'was last seen on {seen} '
                       f'Their last messeage was sent on {lastMesseage}')

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
    async def on_member_update(before, after: discord.Member):
        db.update(f"Seen = {datetime.timestamp(datetime.now())}",
                  f"Id={after.id}")
        try:  # this creates a log for the user even if it didn't exist before
            db.QueryMoirail(after.id)
        except TypeError:
            db.c.execute(f'''INSERT INTO Users(id)
                            Values({after.id})''')
        finally:
            db.SQL.commit()

    @bot.event
    async def on_message(message: discord.Message):
        if message.author == bot.user:
            return
        if '<>' in message.content:
            try:
                MoirailV = (db.QueryMoirail(message.author.id))[0] + 1
                db.update(f"Moirail = {MoirailV}", f"Id = {message.author.id}")
            except TypeError:
                db.c.execute(f'''INSERT INTO Users(id, Moirail)
                                 Values({message.author.id},1)''')
            finally:
                db.SQL.commit()
        if supression(message.content):
            await message.delete()
        try:
            await bot.process_commands(message)
        except AttributeError:
            print("Could not process commands \n"
                  "This is could be due to bot not being started \n"
                  "This is normal for testing")
        db.update(f"LastMessage = {message.created_at.timestamp()}",
                  f"Id={message.author.id}")
        try:  # this creates a log for the user even if it didn't exist before
            db.QueryMoirail(message.author.id)
        except TypeError:
            db.c.execute(f'''INSERT INTO Users(id)
                             Values({message.author.id})''')
        finally:
            db.SQL.commit()

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
