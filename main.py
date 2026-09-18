import discord

with open("TOKEN.txt") as file:
    TOKEN = file.read()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in. My name is {client.user}")



client.run(TOKEN)