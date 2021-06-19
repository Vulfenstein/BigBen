import asyncio
import discord
import os
import datetime
from discord.ext import commands
from dotenv import load_dotenv

# Load bot token #
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Declare bot, commands use '!'
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

# Assign voice channel here #
voice_channel_name = 'General'

# Start up #
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game('The Time Keeper'))

# At top of hour, join voice chat and play chimes
async def get_time(ctx):
    current = 0
    while True:
        await asyncio.sleep(10)
        if datetime.datetime.now().hour != current:
            current = datetime.datetime.now().hour
            voice_channel = discord.utils.get(ctx.guild.channels, name=voice_channel_name)
            if voice_channel != None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="big_ben_audio.mp3"))
                while vc.is_playing():
                    await asyncio.sleep(1)
                await ctx.voice_client.disconnect()
            else:
                await ctx.send(str(voice_channel_name) + " is not in a valid voice channel.")

# Start Big Ben loop # 
@bot.command()
async def play(ctx):
    bot.loop.create_task(get_time(ctx))

# Kick Big Ben from voice channel #
@bot.command()
async def exit(ctx):
    await ctx.voice_client.disconnect()
    return

#Run bot #
bot.run(TOKEN)