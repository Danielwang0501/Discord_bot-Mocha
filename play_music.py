import discord
import os
import datetime
import youtube_dl
import asyncio
import googleapiclient.discovery
import random


loop_one_song = False
loop_queue = False
song_queue = []
song_name_queue = []
google_key = os.environ['google dev key']
shuffled = False

async def loopswitch(ctx):

  global loop_one_song
  global loop_queue

  if loop_one_song == False:
    await ctx.send("單曲循環ON :love_you_gesture: ")
    loop_one_song = True
  else:
    await ctx.send("單曲循環OFF :mobile_phone_off: ")
    loop_one_song = False

async def loop_queue_switch(ctx):
  global loop_one_song
  global loop_queue

  if loop_queue == False:
    await ctx.send("歌單循環ON :love_you_gesture: ")
    loop_queue = True
    await ctx.send("單曲循環OFF :mobile_phone_off: ")
    loop_one_song = False
  else:
    await ctx.send("歌單循環OFF :mobile_phone_off: ")
    loop_queue = False


async def play(self, ctx, arg):
  FFMPEG_OPTIONS = {"before_options" : "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
  "options" : "-vn"}
  YDL_OPTIONS = {"format" : "bestaudio", "noplaylist" : "True", "ignoreerrors": False}
  vc = ctx.voice_client
  arg = str(arg)
  channel = ctx.channel
  if "&list" in arg:
    list_id = arg.split("&list=")[1].split("&index")[0]
    arg = f"https://www.youtube.com/playlist?list={list_id}"
  try:
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      if arg.startswith("https://"):
        if arg.startswith("https://www.youtube.com/playlist?list"):
          list_id = arg.split("?list=")[1]
          youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = google_key)
          request = youtube.playlists().list(part = "snippet,contentDetails", id = list_id, maxResults = 200)
          await asyncio.sleep(1)
          response = request.execute()
          await asyncio.sleep(1)
          playlist_title = response["items"][0]["snippet"]["title"]
          request = youtube.playlistItems().list(part = "snippet", playlistId = list_id, maxResults = 200)
          response = request.execute()
          await asyncio.sleep(1)
          playlist_items = []
          while request is not None:
            response = request.execute()
            playlist_items += response["items"]
            request = youtube.playlistItems().list_next(request, response)
          for i in range(0, len(playlist_items)):
            song_queue.append(playlist_items[i]["snippet"]["title"])
            song_name_queue.append(playlist_items[i]["snippet"]["title"])
        else:
          info = ydl.extract_info(arg, download = False)
          song_name = info["title"]
          duration = int(info["duration"])
          thumb_url = info["thumbnails"][0]["url"]
          dur_sec = duration % 60
          dur_min = duration // 60
          song_queue.append(arg)
          song_name_queue.append(song_name)
      else:
        info = ydl.extract_info(f"ytsearch:{arg}", download = False)
        song_name = info["entries"][0]["title"]
        duration = int(info["entries"][0]["duration"])
        thumb_url = info["entries"][0]["thumbnails"][0]["url"]
        song_queue.append(arg)
        song_name_queue.append(song_name)
        dur_sec = duration % 60
        dur_min = duration // 60

      if arg.startswith("https://www.youtube.com/playlist?list="):
        embed = discord.Embed(#訊息
        title = f"播放歌單:{playlist_title}",
        description = f"共有{len(playlist_items)}首歌",
        color = 0xe74c3c,
        timestamp = datetime.datetime.utcnow())

      else:
        embed = discord.Embed(#訊息
        title = f"已加入序列 : {song_name}",
        description = f"長度 : {dur_min}分{dur_sec}秒",
        color = 0x50edea,
        my_secret = os.environ['TOKEN'],
        timestamp = datetime.datetime.utcnow())
        embed.set_thumbnail(url = thumb_url)
      await channel.send(embed = embed)
  except Exception as error:
    embed = errorException(str(error), 1)
    await channel.send(embed = embed)
  if not vc.is_playing():
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      if arg.startswith("https://"):
        if arg.startswith("https://www.youtube.com/playlist?list"):
          info = ydl.extract_info(f"ytsearch:{song_queue[0]}", download = False)
          await asyncio.sleep(1)
          url2 = info["entries"][0]["formats"][0]["url"]
        else:
          info = ydl.extract_info(arg, download = False)
          url2 = info["formats"][0]["url"]
      else:
        info = ydl.extract_info(f"ytsearch:{arg}", download = False)
        await asyncio.sleep(1)
        url2 = info["entries"][0]["formats"][0]["url"]
      source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
    vc.play(source = source, after = lambda e: vc.loop.create_task(play_next(self, ctx)))

async def play_next(self, ctx):
  global loop_one_song
  global loop_queue
  
  if len(song_queue[0]):
    if loop_queue == True:
      song_queue.append(song_queue[0])
      del song_queue[0]
      song_name_queue.append(song_name_queue[0])
      del song_name_queue[0]
    elif loop_one_song == False:
      del song_queue[0]
      del song_name_queue[0]

  vc = ctx.voice_client

  if len(song_queue) >= 1:    
    FFMPEG_OPTIONS = {"before_options" : "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options" : "-vn"}
    YDL_OPTIONS = {"format" : "bestaudio", "noplaylist" : "True"}
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(f"ytsearch:{song_queue[0]}", download = False)
      await asyncio.sleep(1)
      url2 = info["entries"][0]["formats"][0]["url"]
      source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
    vc.play(source = source, after = lambda e: vc.loop.create_task(play_next(self, ctx)))
  else:
    await asyncio.sleep(90) 
    if not vc.is_playing() and len(song_queue):
      global shuffled
      shuffled = False
      await vc.disconnect()
      await ctx.send("沒事做!高歌離席!")

async def skip_song(self, ctx):
  vc = ctx.voice_client
  vc.stop()
  await ctx.send(f"我覺得這首挺好聽的說，但應{ctx.author.name}要求")

async def check_role_dj(self, ctx):
  for i in range(len(ctx.author.roles)):
    if ctx.author.roles[i].name == "DJ":
      return True
  for i in range(len(ctx.author.roles)):
    if ctx.author.roles[i].name == "37th 社員":
      return True  
  await ctx.send(f"就憑你也敢命令本小姐??({ctx.author.name}未持有DJ身分組)")
  return False

async def showsonglist(self, ctx):
  if shuffled == True:
    await ctx.send("很抱歉，技術不足，無法顯示SHUFFLE後的歌單")
  elif not len(song_name_queue):
    await ctx.send("裡面沒了喔，歡迎填滿我。")
  else:
    SONGNAME = "歌單:"
    if len(song_name_queue) > 5:
      await ctx.send("以下是我體內後5首的歌單")
      for i in range(5):
        SONGNAME += f"\n"
        SONGNAME += f"{i + 1}."
        SONGNAME += song_name_queue[i]
      await asyncio.sleep(1)
    else:
      for i in range(len(song_name_queue)):
        SONGNAME += f"\n"
        SONGNAME += f"{i + 1}."
        SONGNAME += song_name_queue[i]
    await ctx.send(SONGNAME)
      

async def shuffle(self, ctx):
  global shuffled
  if song_queue[0] != None:
    random.shuffle(song_queue)
    shuffled = True
    await ctx.send("(以精湛的口技完成SHUFFLE")
  else:
    await ctx.send("您確定這裡有東西...？您可憐的眼睛阿...")

async def clear(self, ctx):
  global song_name_queue
  global song_queue
  song_name_queue = []
  song_queue = []
  await ctx.send("榨乾了喔")
  

errors = {
  "notfound" : "HTTP Error 404",
  "wrongwebsite" : "Unsupported URL",
  "unreadable" : "Name or service not known"
}


def errorException(error, sec):
  if errors["notfound"] in error:
    _title = "網址格式有誤"
    des = "檢查下您的URL吧，用您那幾乎快瞎掉的眼睛。"
  elif errors["wrongwebsite"] in error:
    _title = "暫不支持這網站"
    des = "本小姐可沒連這垃圾網站都搭理的道理，可不是人家沒能力喔！"
  elif errors["unreadable"] in error:
    _title = "URL不存在"
    des = "說真的，您的頭腦是怎樣，不存在的都要餵給本小姐?？"
  else:
    _title = "未知的錯誤"
    des = "阿...出錯了...反正不是人家的錯就對了!"
  embed = discord.Embed(#訊息
  title = f"{_title}",
  description = f"{des}",
  color = 0xe74c3c,
  timestamp = datetime.datetime.utcnow())
  return embed