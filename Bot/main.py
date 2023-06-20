"""
# REVIEW générale : le code est pas mal, mais il y a quelques points à améliorer :

- un petit docstring à chaque fonction, même basique, c'est toujours mieux que rien

- Le token, c'est pas une bonne idée de le mettre en clair dans le code, il faut le mettre dans un fichier de config ou un .env

- au niveau de la structure du projet, pas trop compris l'intérêt du Script/main.py

- et un dernier tips, je conseille de faire un fichier pour gérer l'ICS à part, {ça permet de séparer les fonctionnalités et de rendre le code plus lisible} ← copilot
"""

from discord import *
from discord.ext import commands, tasks
import datetime

intents = Intents.default()

# REVIEW - a mettre dans un .env ou un fichier de config
TOKEN = "MTExMDk2NzMxODU1MDQzMzgyMw.GiO2NB.1Gevd3Q159xq0hvItQd016xH97EnSP4RpaMofI"

# REVIEW - le command_prefix est pas utilisé à ma connaissance, vu qu'on utilise les interactions (commandes slash)
bot = Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command(description = "Teste")
async def ping(ctx : ApplicationContext):
    await ctx.interaction.response.send_message(f"Pong! {bot.latency*1000:.0f} ms")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@tasks.loop(hours=1)
async def send_private_messages():
    users = [479649694033641502, 363011509564997642, 534827724183699476, 238995072740229121]

    current_time = datetime.datetime.now().strftime('%H:%M')

    if current_time == '23:2':
        for user_id in users:
            print('ok')
            user = await bot.fetch_user(user_id)
            await user.send("Ceci est un message privé planifié.")

@send_private_messages.before_loop
async def before_send_private_messages():
    now = datetime.datetime.now()
    target_time = now.replace(hour=23, minute=24, second=0) 
    if now > target_time:
        target_time += datetime.timedelta(days=1)
    time_until_target = (target_time - now).total_seconds()

    await asyncio.sleep(time_until_target)

send_private_messages.start()

bot.run(TOKEN)
