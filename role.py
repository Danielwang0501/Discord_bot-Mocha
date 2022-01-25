import discord
from discord.ext import commands

class role(commands.Cog):

  def __init__(self, bot):
    self.client = bot
    
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.message_id == 881830996356509716:
      guild = self.client.get_guild(payload.guild_id)
      if str(payload.emoji) == "🎧":
        role = guild.get_role(880427802439065610)
        await payload.member.add_roles(role)
      if str(payload.emoji) == "<:AHEGAO:875231964490248253>":
        role = guild.get_role(882244403622727710)
        await payload.member.add_roles(role)
      if str(payload.emoji) == "<:sirroland:881830996356509716>":
        role = guild.get_role(891157938339737652)
        await payload.member.add_roles(role)
        
  @commands.Cog.listener()      
  async def on_raw_reaction_remove(self, payload):
    if payload.message_id == 881830996356509716:
      guild = self.client.get_guild(payload.guild_id)
      user = guild.get_member(payload.user_id)
      if str(payload.emoji) == "🎧":
        role = guild.get_role(880427802439065610)
        await user.remove_roles(role)
      if payload.emoji.id == 875231964490248253:
        role = guild.get_role(882244403622727710)
        await user.remove_roles(role)
      if payload.emoji.id == 881830996356509716:
        role = guild.get_role(891157938339737652)
        await user.remove_roles(role)
      else:
        print(payload.emoji.name)

def setup(bot):
  bot.add_cog(role(bot))
