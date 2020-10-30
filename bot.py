# bot.py
import os

import discord
from dotenv import load_dotenv

import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

    print(f'Connected to {guild.name} ({guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


    # guild = discord.utils.get(client.guilds, name=GUILD)
    #
    # # for guild in client.guilds:
    # #     print(f'{guild.name}')
    #
    # print(
    #     f'{client.user} is connected to the following guild:\n'
    #     f'{guild.name} (id: {guild.id})'
    # )

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
    print(f'New Guild Member: {member.name} ({member.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == 'joke':
        joke_url = 'https://icanhazdadjoke.com'
        joke_headers = {'Accept':'application/json'}
        joke_response = requests.get(joke_url, headers = joke_headers)
        if joke_response.status_code == 200:
            joke_text = joke_response.json()['joke']

        await message.channel.send(joke_text)

client.run(TOKEN)
