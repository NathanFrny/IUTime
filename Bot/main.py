from discord import *
from discord.ext import commands, tasks
import datetime
import json
from request import lessons_TP, trie
from constants import TOKEN, AVAILABLETP, LOGOPATH, AUTHORS, DATASOURCES

intents = Intents.default()
bot = Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})') #Bot connection confirmation

@bot.command(description="Ask your schedule")
async def schedule(ctx: ApplicationContext, tp : str): 
    """Main Feature: 
    Using /schedule on discord channel or bot's DMs
    return in DMs the choiced TP shedule's for the day
    
    Update soon : return schedule for tommorrow if hour >= 7pm"""

    user = ctx.author
    if tp.upper() in AVAILABLETP:
        date = datetime.date.today()
        schedule = trie(lessons_TP(tp))
        embed = Embed(
            title=f'Schedule {date}',
            description=f"Voici l'emploi du temps du {tp}",
            color=0x9370DB  #Purple
        )
        #embed.set_thumbnail(url = LOGOPATH) HEBERGER LE LOGO SUR INGUR
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
        await ctx.interaction.response.send_message("Done!") #Responding to user
    else:
        message = "Les arguments attendus sont :"
        for element in AVAILABLETP:
            message += element + ", "
        message = message[:-2]
        await ctx.interaction.response.send_message(message) #Responding if bad argument

@bot.command(description = "Activer ou non les notifications des cours")
async def notif(ctx : ApplicationContext, boolean : bool):
    """Permet aux utilisateurs d'activer ou désactiver les notifcations de prochains cours"""
    id = ctx.author
    with open(DATASOURCES, "x") as f:
        js = f.load()
        if id in js.keys() and id["notify"] != boolean:
            id["notify"] = boolean
        else:
            js[id] = boolean
        json.dump(js, f)
    await ctx.interaction.response.send_message("Done!")
    
            
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

if __name__ == "__main__":
    send_private_messages.start()
    bot.run(TOKEN)
