import os
from dotenv import load_dotenv
import discord
import Logger


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

Logger.start()

client = discord.Client()


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


async def on_connect():
    message.channel.send("Connected!")


async def on_member_join(member):
    await message.channel.send(f'Welcome {member.name}!')


async def on_message(message):
    print(message)
    if message.author == client.user:
        return
    if message.content.startswith('!test'):
        await message.channel.send('works!')


async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)
