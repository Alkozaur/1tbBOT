import requests
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def call_tm1():
    response = requests.get("https://tm1.edu.pl", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    soup = BeautifulSoup(response.text, "html.parser")
    element = soup.find(id="ajax-content").find("article")
    print(element.get("id"))


with open("TOKEN.txt") as file:
    TOKEN = file.read()
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"Logged in. My name is {client.user}")
    call_tm1()

@client.command()
async def ping(ctx):
    await ctx.send("pong")

client.run(TOKEN)