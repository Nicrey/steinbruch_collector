import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
# Tim, Jonas, Michael
legit_users = [98511893890605056, 522489090185232387, 696077043284312134]
bot_id = 1278755929474465825
@client.command()
async def einsammeln(ctx):
    try:
        print("Starting with collection")
        channel =  ctx.channel
        if ctx.author.id in legit_users:
            history = channel.history()
            messages = []
            async for message in history:
                if message.content == "" or message.content == "!einsammeln" or message.content.startswith("https"):
                    continue
                if message.author.id == bot_id:
                    continue
                #print(message.content)
                messages.append(f"{message.content}")

            messages = '\n'.join(reversed(messages[:-1]))
            authors = ', '.join(set(reversed([message.author.display_name async for message in channel.history()])))
            title = channel.name
            await ctx.author.send(f"---------------- NEUE TABELLE: {title} ----------------------------")
            full_text = f"{title} \nAutor:innen: {authors}\n{messages}"
            text_size = len(full_text)
            #print(full_text)
            i = 0
            limit = 1800
            while text_size >= 0:
                i += limit
                embed = f"```\n{full_text[i-limit:i]}\n```"
                await ctx.author.send(embed)
                text_size -= limit
            await ctx.author.send(f"---------------- Tabellenende: {title} ----------------------------")
            await ctx.send(f"Erfolgreich eingesammelt und an {ctx.author.display_name} versandt.")
        else:
            await ctx.send("Nicht genug Berechtigungen. Bitte bei Jonas/Michael/Tim melden")
    except Exception as e:
        await ctx.send(f"Irgendwas ist schief gelaufen. Bitte bei Nicrey/Tim melden.")
        raise e

@client.command()
async def aufräumen(ctx):
    if ctx.author.id in legit_users:
        if ctx.guild is None:
            channel = ctx.channel
            async for message in channel.history():
                if message.author.id == bot_id:
                    await message.delete()
client.run(TOKEN)
