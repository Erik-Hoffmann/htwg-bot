# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bs4 import BeautifulSoup
import requests
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

MENSA_HTWG = 'https://seezeit.com/essen/speiseplaene/mensa-htwg/'

# Utility
def validateIngr(sup):
    return bool(re.match("\((\d\w?,?)+\)", sup))

# Commands
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='mensa', help='Responds with the current menu')
async def menu(ctx):
    page_response = requests.get(MENSA_HTWG)
    soup = BeautifulSoup(page_response.content, 'html.parser')
    contents = soup.find('div', class_='contents_aktiv')
    menus = contents.find_all('div', class_='speiseplanTagKat')
    
    response = discord.Embed(
                title="In der Mensa gibt es:",
                url=MENSA_HTWG
            )
    for menu in menus:
        category=menu.find('div', class_='category')
        food=menu.find('div', class_='title_preise_1').find('div', class_='title')
        for sup in food.select('sup'):
            if not validateIngr(sup.text): sup.unwrap()
            else : sup.decompose()
        response.add_field(name=category.text, value=f"{food.text})", inline=True)
    
    await ctx.send(embed=response)


bot.run(TOKEN)

