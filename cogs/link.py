import nextcord
from nextcord.ext import commands
from urllib.parse import quote_plus


class Link(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    class Google(nextcord.ui.View):
        def __init__(self, query: str):
            super().__init__()
            query = quote_plus(query)
            url = f'https://www.google.com/search?q={query}'
            self.add_item(nextcord.ui.Button(label='Click Here', url=url))


    @commands.command(alias = ["link", "google", "гугл", "поиск"])
    @commands.cooldown(1, 15, commands.BucketType.member)
    async def google(ctx, *, query: str):
        await ctx.send(f'Google Result for: `{query}`', view=Google(query))


def setup(bot:commands.Bot):
    bot.add_cog(Link(bot))