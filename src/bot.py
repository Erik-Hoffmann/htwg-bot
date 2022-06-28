# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import date

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

def attr_lookup(attribute):
    lookup = {
            "Veg": "Vegetarisch",
            "Vegan": "Vegan",
            "Sch": "Schwein",
            "R": "Rind/Kalb",
            "G": "Geflügel",
            "L": "Lamm",
            "W": "Wild",
            "F": "Fisch/Meeresfrüchte"
            }
    result = []
    if attribute:
        for attr in attribute:
            if attr in lookup:
                result.append(lookup[attr])
    return ", ".join(result) if result else ""

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
    page_response = requests.get(MENSA_HTWG)
    soup = BeautifulSoup(page_response.content, 'html.parser')
    contents = soup.find('div', class_='tx-speiseplan')
    date_tabs = contents.find_all('a', class_='tab')
    current_tab = None
    current_tab_class = None
    attr_class='speiseplanTagKatIcon'
    for tab in date_tabs:
        current_tab = tab.text
        if date.today().strftime("%d.%m.") in current_tab:
        # if "16.05." in current_tab:
            current_tab_class = tab.get('class')[1]
            break
    
            
    response = discord.Embed(
                title="In der Mensa gibt es:",
                url=MENSA_HTWG
            )
    if not current_tab_class is None:

        day = contents.find('div', {"id":current_tab_class})
        menus = day.find_all('div', class_='speiseplanTagKat')


        for menu in menus:
            category=menu.find('div', class_='category')
            food=menu.find('div', class_='title_preise_1').find('div', class_='title')
            for sup in food.select('sup'):
                if not validateIngr(sup.text): sup.unwrap()
                else : sup.decompose()
            attribute=menu.find('div', class_='title_preise_2').find('div', class_=attr_class)['class']
            response.add_field(name=f"{category.text} : {attr_lookup(attribute)}", value=f"{food.text}", inline=True)
    else:
        response.add_field(name="Heute wohl nix", value="Zu oder so :(\nVielleicht heitert dich ein Quiz auf?\nhttps://www.mensa.de/about/membership/online-iq-test/")

    await ctx.send(embed=response)


bot.run(TOKEN)

