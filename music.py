import discord
from discord.ext import commands
from discord_slash import cog_ext
# import datetime
import play_music
# from replit import db 



class music(commands.Cog):

  guild_ids = [843724526381563924, 888686203346513970, 888589355403333643, 718777727855099904, 882515544073469952, 828524214239756300]

  def __init__(self, bot):
    self.client = bot

  @cog_ext.cog_slash(name = "disconnect", description = "斷開你我的連結", guild_ids = guild_ids)
  async def disconnect(self, ctx):
    if await play_music.check_role_dj(self, ctx):
      if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send(f"{ctx.author.name}不要我了...(啜泣")
      else:
        await ctx.send("我都還沒進去...(尚未連接語音頻道)")

  @cog_ext.cog_slash(name = "join", description = "進...進來了...", guild_ids = guild_ids)
  async def join(self, ctx):
    if ctx.author.voice is None:
      await ctx.send("你是想要我進去哪裡？(找不到語音頻道)")
    else:
      voice_channel = ctx.author.voice.channel
      if ctx.voice_client is None:
        if await play_music.check_role_dj(self, ctx):
          await voice_channel.connect()
          await ctx.send(f"來了~~(加入{voice_channel})")

      else:
        if await play_music.check_role_dj(self, ctx):
          await ctx.voice_client.move_to(voice_channel)
          await ctx.send(f"來了~~(加入{voice_channel})")

  @cog_ext.cog_slash(name = "play", description = "音浪來襲！(播放)", guild_ids = guild_ids)
  async def play(self, ctx, *, songname):
    if await play_music.check_role_dj(self, ctx):
      if ctx.voice_client is not None:#原語音頻道
        await play_music.play(self, ctx, songname)
      else:
        if ctx.author.voice is None:#作者無vc
          await ctx.send("你是想要我進去哪裡？")   
        else:
          voice_channel = ctx.author.voice.channel
          
          if ctx.voice_client is None:#作者有vc
            await voice_channel.connect()
            await ctx.send(f"來了~~(加入{voice_channel})")
            await play_music.play(self, ctx, songname)
          else:#作者和機器人都有vc
            await ctx.voice_client.move_to(voice_channel)
            await play_music.play(self, ctx, songname)

  @cog_ext.cog_slash(name = "pause", description = "暫時，寂靜。(暫停)", guild_ids = guild_ids)
  async def pause(self, ctx):
    if await play_music.check_role_dj(self, ctx):
      if ctx.voice_client.is_playing():
        await ctx.send("暫停溜！")
        ctx.voice_client.pause()
      else:
        await ctx.send("蛤！")

  @cog_ext.cog_slash(name = "resume", description = "自萬籟沉寂中解脫。(繼續)", guild_ids = guild_ids)
  async def resume(self, ctx):
    if await play_music.check_role_dj(self, ctx):
      if ctx.voice_client.is_paused():
        await ctx.send("繼續~~")
        ctx.voice_client.resume()
      else:
        await ctx.send("蛤！")

  @cog_ext.cog_slash(name = "loop", description = "喔？你想在曲中沉淪嗎?(單曲循環)", guild_ids = guild_ids)
  async def loop(self, ctx):
    if await play_music.check_role_dj(self, ctx):
      await play_music.loopswitch(ctx)

  @cog_ext.cog_slash(name = "loopqueue", description = "呵！真是貪心，全都想要是吧。(歌單循環)", guild_ids = guild_ids)
  async def loopqueue(self, ctx):
    if await play_music.check_role_dj(self, ctx):
      await play_music.loop_queue_switch(ctx)
  
  @cog_ext.cog_slash(name = "show", description = "揭示萬物。(顯示歌單)", guild_ids = guild_ids)
  async def show(self, ctx):
    if await play_music.check_role_dj(self, ctx):
      await play_music.showsonglist(self, ctx)

  @cog_ext.cog_slash(name = "skip", description = "自惱人的旋律中解放。(跳過)", guild_ids = guild_ids)
  async def skip(self, ctx):
    if await play_music.check_role_dj(self, ctx):
      await play_music.skip_song(self, ctx)
  
  @cog_ext.cog_slash(name = "shuffle", description = "規律？不值一提。(打亂順序)", guild_ids = guild_ids)
  async def shuffle(self, ctx):
    await play_music.shuffle(self, ctx)

  @cog_ext.cog_slash(name = "clear", description = "煥然一新。(清空歌單)", guild_ids = guild_ids)
  async def clear(self, ctx):
    await play_music.clear(self, ctx)

  @cog_ext.cog_slash(name = "saysomething", description = "興許你也想以我之嘴傳遞給那唯一的他\她", guild_ids = guild_ids)
  async def saysomething(self, ctx, *, something):
    channel = ctx.channel
    await channel.send(something)


def setup(bot):
  bot.add_cog(music(bot))