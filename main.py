import requests
import discord
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
from urllib.parse import urljoin

CHANNEL_ID = 1543887723763339346


async def send_announcement(element, post_id):
    link = element.find("div").find("a").get("href")
    print(link)
    response = requests.get(link, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    soup = BeautifulSoup(response.text, "html.parser")
    text_element = soup.find(id=post_id).find("div").find("div")
    

    channel = client.get_channel(CHANNEL_ID)
    await channel.send(f"```html\n{text_element}\n```")
    



@tasks.loop(minutes=1)
async def call_tm1():
    response = requests.get("https://tm1.edu.pl", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    soup = BeautifulSoup(response.text, "html.parser")
    element = soup.find(id="ajax-content").find("article")
    post_id = element.get("id")
    await send_announcement(element, post_id) #
    print(post_id)
    with open("last_post.txt", "w") as file:
        try:
            if post_id == file.read():
                return
            else:
                file.write(post_id)
                send_announcement(element, post_id)
        except Exception:
            file.write(post_id)



with open("TOKEN.txt", "r") as file:
    TOKEN = file.read()
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"Logged in. My name is {client.user}")
    if not call_tm1.is_running():
        call_tm1.start()

@client.command()
async def ping(ctx):
    await ctx.send("pong")

client.run(TOKEN)