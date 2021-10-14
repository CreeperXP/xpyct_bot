from webserver import keep_alive
import os
import nextcord
from nextcord.ext import commands
import time
import json
import requests

PREFIX = "$"
bot = commands.Bot(command_prefix=PREFIX, description="Hi")
bot.remove_command("help")

version = "Bot v1.4"
ctime = time.strftime("Today is %X %x", time.localtime())


@bot.event
async def on_ready():
    print(f"Bot logged as {bot.user} | {version}")
    print(f"{ctime}")
    await bot.change_presence(
        status=nextcord.Status.online, activity=nextcord.Game("$help")
    )


@bot.command()
async def help(ctx):
    await ctx.send(
        f"Мои команды: {PREFIX}help | {PREFIX}ping | {PREFIX}clear | {PREFIX}hello | {PREFIX}github | {PREFIX}ver | {PREFIX}say | {PREFIX}serverinfo | {PREFIX}clean | {PREFIX}send_m"
    )
    print(f"[Logs:utils] Информация о командах бота была выведена | {PREFIX}help")


@bot.command(
    aliases=[
        "Ping",
        "PING",
        "pING",
        "ping",
        "Пинг",
        "ПИНГ",
        "пИНГ",
        "пинг",
        "Понг",
        "ПОНГ",
        "пОНГ",
        "понг",
    ]
)
async def __ping(
    ctx,
):  # Объявление асинхронной функции __ping с возможностью публикации сообщения
    ping = bot.ws.latency  # Получаем пинг клиента

    ping_emoji = "🟩🔳🔳🔳🔳"  # Эмоция пинга, если он меньше 100ms

    if ping > 0.10000000000000000:
        ping_emoji = "🟧🟩🔳🔳🔳"  # Эмоция пинга, если он больше 100ms

    if ping > 0.15000000000000000:
        ping_emoji = "🟥🟧🟩🔳🔳"  # Эмоция пинга, если он больше 150ms

    if ping > 0.20000000000000000:
        ping_emoji = "🟥🟥🟧🟩🔳"  # Эмоция пинга, если он больше 200ms

    if ping > 0.25000000000000000:
        ping_emoji = "🟥🟥🟥🟧🟩"  # Эмоция пинга, если он больше 250ms

    if ping > 0.30000000000000000:
        ping_emoji = "🟥🟥🟥🟥🟧"  # Эмоция пинга, если он больше 300ms

    if ping > 0.35000000000000000:
        ping_emoji = "🟥🟥🟥🟥🟥"  # Эмоция пинга, если он больше 350ms

    message = await ctx.send(
        "Пожалуйста, подождите. . ."
    )  # Переменная message с первоначальным сообщением
    await message.edit(
        content=f"Понг! {ping_emoji} `{ping * 1000:.0f}ms` :ping_pong:"
    )  # Редактирование первого сообщения на итоговое (На сам пинг)
    print(
        f"[Logs:utils] На данный момент пинг {ping * 1000:.0f}ms | {PREFIX}ping"
    )  # Вывод пинга в консоль


@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f"Привет, {author.mention}!")
    print(f"[Logs:utils] Приветствие было выведено | {PREFIX}hello")


@bot.command()
async def ver(ctx):
    await ctx.send(f"{version} | Сделано CreeperXP#0363")
    print(f"[Logs:utils] Информация о боте была выведена | {PREFIX}ver")


@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)
    print(f"[Logs:utils] {amount} сообщений удалено| {PREFIX}purge")


@bot.command()
async def say(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(embed=nextcord.Embed(description=text))
    print(f"[Logs:utils] Сообщение пересказано ботом | {PREFIX}say")


@bot.command()
async def time(ctx):
    await ctx.send(f"{ctime}")
    print(f"[Logs:utils] Время было выведено: {ctime} | {PREFIX}time")


@bot.command()
async def serverinfo(ctx):
    role_count = len(ctx.guild.roles)

    serverinfoEmbed = nextcord.Embed(color=ctx.author.color)

    serverinfoEmbed.add_field(name="Название", value=f"{ctx.guild.name}", inline=False)
    serverinfoEmbed.add_field(
        name="Кол-во юзеров", value=f"{ctx.guild.member_count}", inline=False
    )
    serverinfoEmbed.add_field(
        name="Уровень безопасности",
        value=f"{ctx.guild.verification_level}",
        inline=False,
    )
    serverinfoEmbed.add_field(name="Кол-во ролей", value=f"{role_count}", inline=False)
    serverinfoEmbed.add_field(name="ID сервера", value=f"{ctx.guild.id}", inline=False)

    await ctx.send(embed=serverinfoEmbed)


@bot.command()
async def userinfo(ctx, user: nextcord.User):
    user_id = user.id
    username = user.name
    avatar = user.avatar.url
    await ctx.send(f"ID: {user_id} | NICK: {username}\n{avatar}")
    print(f"[Logs:utils] Информация о {username} была выведена | {PREFIX}userinfo")


@bot.command()
async def clean(ctx, amount=None):
    await ctx.channel.purge(limit=int(amount))
    print(f"[Logs:utils] {amount} сообщений удалено | {PREFIX}clean")


class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Да", style=nextcord.ButtonStyle.danger)
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.send_message(
            "https://github.com/CreeperXP/creeper_bot", ephemeral=True
        )
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Нет", style=nextcord.ButtonStyle.blurple)
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.send_message("Ну ладно :(", ephemeral=True)
        self.value = False
        self.stop()


@bot.command()
async def github(ctx):
    view = Confirm()
    await ctx.send("Перейти на GiHub?", view=view)

    await view.wait()

    if not view.value == None:
        print("Timed Out")
    if view.value == True:
        print("Ссылка выведена")
    if view.value == False:
        print("Ссылка не выведена")
        print(f"[Logs:utils] Ссылка на GitHub была выведена | {PREFIX}github")


@bot.command()
async def send_m(ctx, member: nextcord.Member, *, text):
    await ctx.message.delete()
    await member.send(f"От {ctx.author.name}:", embed=nextcord.Embed(description=text))
    print(
        f"[Logs:utils] Сообщение от {ctx.author.name} было отправлено {member.name} | {PREFIX}send_m"
    )


@bot.command()
async def mute(ctx):
    await ctx.send(file=nextcord.File("leopold-vd.mp4"))


keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))