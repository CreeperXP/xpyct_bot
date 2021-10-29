import discord
from discord.ext import commands


class InfoOfServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['info', 'осервере'])
    async def serverinfo(self, ctx):
        all = len(ctx.guild.members)
        members = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))
        emoji = 0
        anim_emoji = 0
        for emoji in ctx.guild.emojis:
            if emoji.animated == True:
                anim_emoji += 1
            elif emoji.animated == False:
                emoji += 1
        online = 0
        idle = 0
        offline = 0
        dnd = 0
        text = 0
        voice = 0
        for member in ctx.guild.members:
            if str(member.status) == "online":
                online += 1
            if str(member.status) == "idle":
                idle += 1
            if str(member.status) == "dnd":
                dnd += 1
            if str(member.status) == "offline":
                offline += 1
        for channel in ctx.guild.channels:
            if str(channel.type) == "text":
                text += 1
            if str(channel.type) == "voice":
                voice += 1
        region = ctx.guild.region
        owner = ctx.guild.owner.mention
        await ctx.send(f"👀 Всего участников - {all}\n🤖 Ботов - {bots}\n🙍‍♂️ Людей - {members}\n🤩 Анимированных смайлов - {anim_emoji}\n"
                       f"😎 Обычных смайлов - {emoji}\n🟢 Онлайн - {online}\nОффлайн - {offline}\n🟥 Нет на месте - {idle}\n"
                       f"🎤 Голосовых каналов - {voice}\n📰 Текстовых - {text}\n🌐 Регион - {region}\n👨‍💻 Владелец - {owner}")

    
def setup(bot):
    bot.add_cog(InfoOfServer(bot))
