import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

license_string = "<br>***Lizenz (Text): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.de)***<br/>***Bildquelle:***"
author_mapping = {
    804580887563862076 :"[dr_phil_nagi](https://bohemiaspielkunst.itch.io/)",
    98511893890605056 :"[Nicrey/Tim](https://www.nightmaresundertrees.de/)",
    250854831110094848 :"[Moritz (Glgnfz)](https://seifenkiste.rsp-blogs.de)",
    522489090185232387 :"[Jonas (asri)](https://jasri.itch.io/)",
    464427420565504000 :"[Philipp](https://philippteich.carrd.co/)",
    238715208246231041 :"[Lyght](https://ducklyght.itch.io/)",
    195938166996336650 :"[René Kremer (Pen Paper Dice)](https://pen-paper-dice.de/)",
    696077043284312134 :"[nEw bEE (Michael)](https://steinbru.ch)",
    208063198505598977 :"[OlleKnolle](https://instagram.com/sweet_potatoe_01/)",
    310468422381076490 :"[Phybe](https://phyhigh.itch.io/)",
    1176441863566278727 :"[Seba](https://kritischerfehlschlag.de/)",
    286851934017683457 :"Klaudia Kloppstock",
    347768563307773953 :"[Gwynn (ProjektMyra)](http://myra.fandom.com/)"
}
# Tim, Jonas, Michael
legit_users = [98511893890605056, 522489090185232387, 696077043284312134]
bot_id = 1278755929474465825
@client.command()
async def einsammeln(ctx):
    # Collects entries from a public forum thread
    # Adds some blog related stuff like licenses and maps discord users to names that should be used on the blog
    # Sends the result to the command user in blocks of 1800 (2000 being the limit)
    try:
        print("Starting with collection")
        channel =  ctx.channel
        if ctx.author.id not in legit_users:
            await ctx.send("Nicht genug Berechtigungen. Bitte bei Jonas/Michael/Tim melden")
            return 
        if channel.type != discord.ChannelType.public_thread:
            await ctx.send(f"Nur in Foren nutzbar.")
            return

        history = channel.history()
        messages = []
        authors = []
        async for message in history:
            if message.content == "" or message.content == "!einsammeln" or message.content.startswith("https"):
                continue
            if message.author.id == bot_id:
                continue
            if message.author.id in author_mapping:
                authors.append(author_mapping[message.author.id])
            else:
                authors.append(message.author.display_name)
            messages.append(f"{message.content}")

        messages = '\n'.join(reversed(messages[:-1]))
        authors = ', '.join(set(reversed(authors)))
        title = channel.name
        await ctx.author.send(f"---------------- NEUE TABELLE: {title} ----------------------------")
        full_text = f"{title}\n**Idee:**<br>\n**Autor:innen:** {authors}\n{messages}\n{license_string}"
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
