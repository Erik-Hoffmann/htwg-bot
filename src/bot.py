# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

import requests

from speiseplan import Speiseplan_extractor

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

MENSA_HTWG = 'https://seezeit.com/essen/speiseplaene/mensa-htwg/'

# Commands
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
        'I\'m the human form of the 💯 emoji.',
        'Love, it sustains you. It’s like oatmeal.',
        'You’re under arrest for ruining something perfect!',
        'Every time you talk, I hear that sound that plays when Pac-Man dies.',
        'I asked them if they wanted to embarrass you, and they instantly said yes.',
        'Fine, but in protest, I’m walking over there extremely slowly!',
        'Why don’t you just do the right thing and jump out of a window?'
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='bug', help='Found a bug? Report it!')
async def bug(ctx): 
    await ctx.send(f"Nobody is perfect! Report bugs here: https://github.com/Erik-Hoffmann/htwg-bot/issues")

@bot.command(name='mensa', help='Responds with the current menu')
async def menu(ctx):
    response = discord.Embed(
            title="In der Mensa gibt es:",
            url=Speiseplan_extractor.address
        )
    try:
        extractor = Speiseplan_extractor()
        data = extractor.get_tab_json()
        if not data:
            response.add_field(name="Heute wohl nix", value="Zu oder so :(\nVielleicht heitert dich ein Quiz auf?\nhttps://www.mensa.de/about/membership/online-iq-test/")
        else:
            for menu in data:
                response.add_field(name=f"{menu.get('category')} {': ' + str(menu.get('tags')) if menu.get('tags') else ''}", value=menu.get('food'), inline=True)

    except requests.ConnectionError as e:
        response.add_field(name="Fehler!", value=f"Seite nicht erreichbar!\n{e}")
    except IndexError as e:
        response.add_field(name="Fehler!", value=f"Tab ID nicht gefunden!\n{e}")
    except ValueError as e:
        response.add_field(name="Fehler!", value=e)
    except Exception as e:
        response.add_field(name="Fehler", value=f"Unhandled Exception:\n```{e}```")

    await ctx.send(embed=response)


bot.run(TOKEN)

