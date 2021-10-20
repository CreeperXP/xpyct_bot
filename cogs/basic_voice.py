import asyncio
import nextcord
import youtube_dl

from nextcord.ext import commands
import discord
from discord.ext import commands


class Youtube(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],
    }   

    def endSong(guild, path):
        os.remove(path)                                   

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        if not ctx.message.author.voice:
            await ctx.send('you are not connected to a voice channel')
            return

        else:
            channel = ctx.message.author.voice.channel

        voice_client = await channel.connect()

        guild = ctx.message.guild

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            file = ydl.extract_info(url, download=True)
            path = str(file['title']) + "-" + str(file['id'] + ".mp3")

        voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)

        await ctx.send(f'**Music: **{url}')
    


def setup(bot:commands.Bot):
    bot.add_cog Youtub(bot))