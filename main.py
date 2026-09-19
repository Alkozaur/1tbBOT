import requests
import discord
from discord.ext import commands, tasks
from bs4 import BeautifulSoup

with open("CHANNEL.txt", 'r') as file:
    CHANNEL_ID = file.read()

with open("TOKEN.txt", "r") as file:
    TOKEN = file.read()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)


async def send_announcement(element, post_id):
    link = element.find("div").find("a").get("href")
    
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(f"@everyone Pojawiło się nowe ogłoszenie na stronie szkoły!\n{link}")
    

@tasks.loop(minutes=1)
async def call_tm1():
    response = requests.get("https://tm1.edu.pl")
    soup = BeautifulSoup(response.text, "html.parser")
    element = soup.find(id="ajax-content").find("article")
    post_id = element.get("id")


    with open("last_post.txt", "w") as file:
        try:
            if post_id == file.read():
                return
            else:
                file.write(post_id)
                await send_announcement(element, post_id)
        except Exception:
            file.write(post_id)


@client.event
async def on_ready():
    print(f"Logged in. My name is {client.user}")
    if not call_tm1.is_running():
        call_tm1.start()


@client.command()
async def ping(ctx):
    await ctx.send("pong")


client.run(TOKEN)