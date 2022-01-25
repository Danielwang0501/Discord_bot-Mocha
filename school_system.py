import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup as soup
from discord_slash import cog_ext
from replit import db


class school_system(commands.Cog):
  guild_ids = [
    843724526381563924, 888686203346513970, 888589355403333643,718777727855099904, 882515544073469952, 828524214239756300]

  def __init__(self, bot):
    self.client = bot


  @cog_ext.cog_slash(name = "setaccount", description = "設置您ischool的帳號", guild_ids = guild_ids)
  async def account_set_up(self, ctx, account, password):
    if str(ctx.author.id) not in db.keys():
      db[str(ctx.author.id)] = {"account" : account, "password" : password}
      await ctx.send(f"已為{ctx.author.name}建置好帳號~不用太感謝我~")
    else:
      db[str(ctx.author.id)] = {"account" : account, "password" : password}
      await ctx.send(f"已為{ctx.author.name}更新帳密，小事一樁~~")

  @cog_ext.cog_slash(name = "getscore", description = "夢魘...", guild_ids = guild_ids)
  async def get_score(self, ctx, private):
    payload = {
      "uid": f"{db[str(ctx.author.id)]['account']}@imail.hchs.hc.edu.tw", 
      "pwd": db[str(ctx.author.id)]["password"],
      "rememberMe": " ", 
      "lang": "ChineseTraditional"
    }
    login = requests.post("https://auth.ischool.com.tw/service/basicauth.php", data = payload)
    data = requests.get("https://web2.ischool.com.tw/?school=hchs.hc.edu.tw&dn=imail.hchs.hc.edu.tw")
    print(login.__dict__)

def setup(bot):
    bot.add_cog(school_system(bot))
