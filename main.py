import os
import discord
import requests
import json
import random
from replit import db
from discord.ext import commands
import music
import role
from discord_slash import SlashCommand
import school_system
from keep_alive import keep_alive

cogs = [music, role, school_system]
Token = os.environ['TOKEN']
keys = db.keys()
bot = commands.Bot(command_prefix = '-', intents = discord.Intents.all())
slash = SlashCommand(bot, sync_commands = True)


sad_words = ["不開心", "不爽", "心態崩了", "被搞", "壓抑", "憂鬱", "嗚嗚", "難受"]
St_encouragement = ["自己加油", "不哭", "活該", "嗯", "哈哈笑死"]

if "respontf" not in db.keys():
  db["respontf"] = "true"

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]


def delete_encouraging_message(index):
  encouragements = db["encouragements"]
  if index < 0:
    trf = 1
    return trf
  elif len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements
    trf = 0
    return trf
  else:
    trf = 1
    return trf


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)


for i in range(len(cogs)):
  cogs[i].setup(bot)


@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))



@slash.slash(name = "whoam1", description = "探索我的全部(說明)", guild_ids = [843724526381563924])
async def whoam1(ctx):
  embed = discord.Embed(title = "音樂機器人，但最近想轉行攬下更多工作", description = "生於2021/8/14", color = 0x56e1df)
  embed.set_author(name = "Daniel's 影分身")
  embed.set_thumbnail(url = "https://pics.me.me/thumb_ahegao-fondos-pinterest-anime-monster-girl-and-51432924.png")
  await ctx.send(embed = embed)


@bot.event
async def on_message(message):
  if message.author is bot.user:
    return
  else:
    await bot.process_commands(message)


keep_alive()
bot.run(Token)
