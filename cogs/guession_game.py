import nextcord
from nextcord.ext import commands
import random
import asyncio


class GuessionGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def guess(ctx):
        await ctx.send('Введи число от 1 до 10')

        def is_correct(m):
         return m.author == ctx.author and m.content.isdigit()

        answer = random.randint(1, 10)

        try:
            guess = await bot.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.send(f'Извини, тебе потребовалось слишком много времени, чтобы это было {answer}.')

        if int(guess.content) == answer:
            await ctx.send('Ты угадал!')
        else:
            await ctx.send(f'Ты не угадал. Я загадывал {answer}.')


def setup(bot):
    bot.add_cog(GuessionGame(bot))