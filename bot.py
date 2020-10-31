# bot.py
# Documentation: https://discordpy.readthedocs.io/en/latest/

import os

import discord
from dotenv import load_dotenv
import requests
import argparse
from discord.ext import commands
import random

load_dotenv()

# -------------------------------------------
# Look for Guild argument, or default to env
# -------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('-g', '--guildname', dest='guild', default=f'{os.getenv("DISCORD_GUILD")}')
args = parser.parse_args()

TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')
GUILD = args.guild

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


# client = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)

    print(f'Connected to {guild.name} ({guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


# await bot.change_presence(activity=discord.Game(name='with the API'))

# guild = discord.utils.get(client.guilds, name=GUILD)
#
# # for guild in client.guilds:
# #     print(f'{guild.name}')
#
# print(
#     f'{client.user} is connected to the following guild:\n'
#     f'{guild.name} (id: {guild.id})'
# )


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
    print(f'New Guild Member: {member.name} ({member.id})')


@bot.command(name='joke', help='Gives you a great bad joke')
async def joke(ctx):
    print('joke')
    joke_url = 'https://icanhazdadjoke.com'
    joke_headers = {'Accept': 'application/json'}
    joke_response = requests.get(joke_url, headers=joke_headers)
    if joke_response.status_code == 200:
        joke_text = joke_response.json()['joke']

    await ctx.send(joke_text)


@bot.command(name='thedonald', help='Gives a quote from POTUS')
async def donald(ctx):
    trump_url = 'https://www.tronalddump.io/random/quote'
    trump_response = requests.get(trump_url)
    trump_quote = trump_response.json()['value']
    trump_dateTime = trump_response.json()['appeared_at']

    await ctx.send(f'Donald J. Trump proclaims the following:\n"{trump_quote}"')


@bot.command(name='roll-dice', help='Roll some dice!')
async def roll_dice(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]

    await ctx.send(', '.join(dice))


@bot.command(name='create-tc', help='Creates a text channel')
@commands.has_role('admin')
async def create_tc(ctx, channel_name='text-channel'):
    guild = ctx.guild
    # counter = 1
    # while discord.utils.get(guild.channels, name=channel_name):
    #     channel_name += str(counter)
    #     counter += 1

    existing_channel = discord.utils.get(guild.channels, name=channel_name)

    if not existing_channel:
        print(f'Creating a new text channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.command(name='create-vc', help='Creates a voice channel')
@commands.has_role('admin')
async def create_tc(ctx, channel_name='New Channel'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new voice channel: {channel_name}')
        await guild.create_voice_channel(channel_name)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == 'hi':
        await message.channel.sent('hi')
    await bot.process_commands(message)


# @bot.event
# async def on_error(event, *args, **kwargs):
#     with open('err.log', 'a') as f:
#         if event == 'on_message':
#             f.write(f'Unhandled message: {args[0]}\n')
#         else:
#             raise

@bot.event
async def on_command_error(ctx, error):
    error_type = type(error).__name__
    ctx_message = ctx.message

    print(f'Error: {error}')

    with open('err.log', 'a') as f:
        f.write(f'{error_type} ("{str(error)}"): {ctx_message}\n')

    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(f'You do not have the correct role (`{error.missing_role}`) for this command.')


bot.run(TOKEN)
