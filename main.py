import requests
import discord
from discord.ext import commands, tasks
from bs4 import BeautifulSoup

with open("CHANNEL.txt", 'r', encoding='utf-8') as file:
    CHANNEL_ID = int(file.read())



with open("TOKEN.txt", "r", encoding='utf-8') as file:
    TOKEN = file.read()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)


async def send_announcement(element, post_id):
    link = element.find("div").find("a").get("href")

    channel = client.get_channel(CHANNEL_ID)
    await channel.send(f"@everyone Pojawiło się nowe ogłoszenie na stronie szkoły!\n{link}",)
    

@tasks.loop(minutes=1)
async def call_tm1():
    response = requests.get("https://tm1.edu.pl")
    soup = BeautifulSoup(response.text, "html.parser")
    element = soup.find(id="ajax-content").find("article")
    post_id = element.get("id")


    with open("last_post.txt", "r+", encoding='utf-8') as file:
        try:
            file_content = file.read()
        except Exception:
                print("Something went wrong!")
                file.seek(0)
                file.write(post_id)
                file.truncate()

                file_content = None
        if post_id == file_content:
            print("Nothin's changed!")
        else:
            print("Change detected!")

            file.seek(0)
            file.write(post_id)
            file.truncate()

            await send_announcement(element, post_id)


@client.event
async def on_ready():
    print(f"Logged in. My name is {client.user}")
    if not call_tm1.is_running():
        call_tm1.start()


@client.command()
async def ping(ctx):
    await ctx.send("pong")


client.run(TOKEN)