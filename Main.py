#!/usr/bin/python3.8
import json
import os

from dotenv import load_dotenv

from discord.ext import commands
import Logger


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

Logger.start()

# initialize discord bot
bot = commands.Bot(command_prefix='%', description='A Bot which does a thing')

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
    print("No saves JSON found")

try:

    @bot.command(name="test", help="Responds with 'works!'")
    async def test(ctx):
        print('test triggered!')
        await ctx.message.channel.send("works!")

    @bot.command(name="Moirail", help="Shows moirail counter for user")
    async def Moirail(ctx):
        await ctx.message.channel.send(
            f"{ctx.author.name} was platonic "
            f"{MoirailCounter[ctx.author.name]} times")

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
