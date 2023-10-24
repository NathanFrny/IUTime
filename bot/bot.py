import logging

import discord  # pycord library

logger = logging.getLogger(__name__)

bot = discord.Bot()

AppCtx = discord.commands.context.ApplicationContext


@bot.event
async def on_ready():
    logger.info("Bot is ready")


@bot.command(description="Ping the bot")
async def ping(ctx: AppCtx):
    print(type(ctx))
    await ctx.send("Pong!")
