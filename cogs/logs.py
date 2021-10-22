import nextcord
from nextcord.ext import commands


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        msg = f"{member.name} зашёл на сервер."
        await self.bot.get_channel(901001501202317322).send(msg)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        msg = f"{member.name} вышел с сервера."
        await self.bot.get_channel(901001501202317322).send(msg)

    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        msg = f"Сообщение от до изменений {before.content}\n" \
            f"Сообщение после изменений {after.content}"
        await self.bot.get_channel(901001501202317322).send(msg)


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        msg = f"Удалённое сообщение от: {message.content}\n"
        await self.bot.get_channel(901001501202317322).send(msg)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
        if before.channel is None:
            msg = f"{member.display_name} зашел в канал {after.channel.mention}"
        elif after.channel is None:
            msg = f"{member.display_name} покинул канап {before.channel.mention}"
        elif before.channel != after.channel:
            msg = f"{member.display_name} перешел из канала {before. channel.mention} в канал {after.channel.mention}"
        await self.bot.get_channel (901001501202317322).send(msg)

    
def setup(bot):
    bot.add_cog(Logs(bot))
