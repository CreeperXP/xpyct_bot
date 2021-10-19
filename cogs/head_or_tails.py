import nextcord
from nextcord.ext import commands
import random

class head_or_tails(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
      if isinstance(error, commands.CommandOnCooldown):
          await ctx.send(f'Для использования команды повторно жди {round(error.retry_after, 2)} секунд')

    @commands.command(aliases = ["орёл_или_решка", "монетка", "монета"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def headortails(self, ctx, answer=None):
      if answer == None:
        await ctx.reply("Можно использовать только значения Орёл и Решка. Пример команды: $монета Орёл")
      else:
        if random.choice(["Орёл", "Решка"]) == answer:
          await ctx.reply("Ты выиграл!")
        else:
          await ctx.reply("Ты проиграл :(")


def setup(bot):
    bot.add_cog(head_or_tails(bot))