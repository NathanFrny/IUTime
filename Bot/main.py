from discord import *
#from discord.ext import commands, tasks
import datetime
from request import lessons_TP, trie
from constants import TOKEN, AVAILABLETP, LOGOPATH, AUTHORS

intents = Intents.default()
bot = Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command(description="Ask your schedule")
async def schedule(ctx: ApplicationContext, tp : str):

    user = ctx.author
    if tp.upper() in AVAILABLETP:
        date = datetime.date.today()
        schedule = trie(lessons_TP(tp))
        embed = Embed(
            title='Schedule',
            description=f"Voici l'emploi du temps du {tp}",
            color=0x9370DB  # Couleur violette (vous pouvez modifier la couleur selon vos préférences)
        )
        embed.set_thumbnail(url = LOGOPATH)
        embed.set_footer(text = f"Ecris par : {AUTHORS}")

        for heures in schedule.keys():
            debut = heures
            cours = schedule[heures]["Cours"]
            salle = schedule[heures]["Salle"]
            prof = schedule[heures]["Prof"]
            heure_fin = schedule[heures]["Heure de fin"]

            embed.add_field(
                name=cours,
                value=f"Début: {debut}\nSalle: {salle}\nProf: {prof}\nHeure de fin: {heure_fin}\n\n",
                inline=False
            )

        await user.send(embed=embed)
        await ctx.interaction.response.send_message("Done!")
    else:
        message = "Les arguments attendus sont :"
        for element in AVAILABLETP:
            message += element + ", "
        message = message[:-2]
        await ctx.interaction.response.send_message(message)

    


"""
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
"""

bot.run(TOKEN)
