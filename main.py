from webserver import keep_alive
import os
try:
    import nextcord
except ImportError:
    print("Trying to Install required module: nextcord[voice]\n")
    os.system("python -m pip install nextcord[voice]")
import nextcord
from nextcord.ext import commands
import json
import requests
import random
import asyncio
from urllib.parse import quote_plus
from speedtest import Speedtest
import string
import datetime
from discord_together import DiscordTogether


def get_prefix(bot, message):
    with open("prefix.json", "r") as f:
        prefix = json.load(f)
    return prefix[str(message.guild.id)]


PREFIX = "$"
intents = nextcord.Intents().all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents) 
bot.remove_command("help")

version = "Bot v2.4"


@bot.event
async def on_guild_join(guild):
    with open("prefix.json", "r") as f:
        prefix = json.load(f)
    prefix[str(guild.id)] = "$"
    with open("prefix.json", "w") as f:
        json.dump(prefix, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open("prefix.json", "r") as f:
        prefix = json.load(f)
    prefix.pop(str(guild.id))
    with open("prefix.json", "w") as f:
        json.dump(prefix, f, indent=4)

@bot.event
async def on_message(message):
    if {i.lower().translate(str.maketrans('','', string. punctuation)) for i in message.content.split(' ')}\
    .intersection(set(json.load(open('cenz.json')))) != set():
        await message.channel.send(f'{message.author.mention}, yyy… кого по губам отшлепать??')
        await message.delete()
    
    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, new: str):
    with open("prefix.json", "r") as f:
        prefix = json.load(f)
    prefix[str(ctx.guild.id)] = new
    with open("prefix.json", "w") as f:
        json.dump(prefix, f, indent=4)
    await ctx.send(f"Новый префикс `{new}`")


@bot.event
async def on_ready():
    bot.togetherControl = await DiscordTogether("DISCORD_TOKEN")
    print(f"Bot logged as {bot.user} | {version}")
    await bot.change_presence(
        status=nextcord.Status.online, activity=nextcord.Game("$help")
    )


@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    test_e = nextcord.Embed(
        colour=nextcord.Colour.orange()
    )
    test_e.set_author(name=f"Мои команды:")
    test_e.add_field(name="help", value="Помощь с командами", inline=False)
    test_e.add_field(name="ping", value="Отображение пинга")
    test_e.add_field(name="clear", value="(Либо purge или clean) очистка чата")
    test_e.add_field(name="hello", value="Бот поздоровается с вами")
    test_e.add_field(name="github", value="Ссылка на мой GitHub")
    test_e.add_field(name="ver", value="Версия бота")
    test_e.add_field(name="say", value="Пересказывание чего-либо от имени бота")
    test_e.add_field(name="serverinfo", value="Информация о сервере")
    test_e.add_field(name="send_m", value="Отправка сообщений в ЛС от имени бота")
    test_e.add_field(name="nitro", value="NOT a free nitro")
    test_e.add_field(name="guess", value="Угадай число")
    test_e.add_field(name="монета", value="Орёл или Решка?")
    test_e.add_field(name="play", value="Играет музыку. Пример: $play Never Gonna Give You Up")
    test_e.add_field(name="loop", value="Ставит повтор воспроизведения")
    test_e.add_field(name="stop", value="Остановка воспроизведения (НЕ ПАУЗА)")
    test_e.add_field(name="pause", value="Ставит воспроизведение на паузу")

    await ctx.reply("Я отправил список команд тебе в ЛС", delete_after=5.0)
    await author.send(embed=test_e)


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
async def link(ctx):
  await ctx.send("Ссылка на добавления бота на свой сервер: https://discord.com/api/oauth2/authorize?client_id=833720975069282344&permissions=0&scope=applications.commands%20bot")

@bot.command()
async def ver(ctx):
    await ctx.send(f"{version} | Сделано CreeperXP#0363")
    print(f"[Logs:utils] Информация о боте была выведена | {PREFIX}ver")


@bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *, text):
    await ctx.message.delete
    await ctx.send(embed=nextcord.Embed(description=text))
    print(f"[Logs:utils] Сообщение пересказано ботом | {PREFIX}say")


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


@bot.command(aliases=["clear", "purge"])
@commands.has_permissions(administrator=True)
async def clean(ctx, amount=None):
    await ctx.channel.purge(limit=int(amount) + 1)
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
            "https://github.com/CreeperXP/xpyct_bot", ephemeral=True
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
@commands.has_permissions(administrator=True)
async def send_m(ctx, member: nextcord.Member, *, text):
    await member.send(
         f"От {ctx.author.name}:", embed=nextcord.Embed(description=text)
    )
    print(
        f"[Logs:utils] Сообщение от {ctx.author.name} было отправлено {member.name} | {PREFIX}send_m"
    )


class Google(nextcord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f"https://www.google.com/search?q={query}"
        self.add_item(nextcord.ui.Button(label="Google", url=url))


class Yandex(nextcord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f"https://yandex.ua/search/?text={query}"
        self.add_item(nextcord.ui.Button(label="Яндекс", url=url))


@bot.command(aliases=["поиск", "гугл"])
async def google(ctx, *, query: str):
    await ctx.reply(f"Результаты запроса `{query}`", view=Google(query))


@bot.command(aliases=["яндекс", "yndx"])
async def yandex(ctx, *, query: str):
    await ctx.reply(f"Результаты запроса `{query}`", view=Yandex(query))


st = Speedtest()
dl_speed = int(st.download() / 8000)
up_speed = int(st.upload() / 8000)
ethernet_speed = (
    f"Скорость закачки: {dl_speed} kb/s \n" f"Скорость выгрузки: {up_speed} kb/s"
)


@bot.command(aliases=["esp"])
async def ethspeed(ctx):
    await ctx.send(ethernet_speed)


@bot.command(aliases=["нитро", "nitro"])
async def freenitro(ctx):
 embed=nextcord.Embed(description=f"Click on the link and get a free nitro!\nhttps://clck.ru/9TFat")
 await ctx.reply(embed=embed)


@bot.command(aliases=["youtube", "ютуб"])
async def yt(ctx):
    link = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
    await ctx.send(f"{link}")


# COGS


@bot.command()  ## Стандартное объявление комманды
async def load(ctx, extensions):  ## объявление функции
    bot.load_extension(f"cogs.{extensions}")  ## загрузка доплонений
    await ctx.send("loaded")


@bot.command()
async def unload(ctx, extensions):
    bot.unload_extension(f"cogs.{extensions}")
    await ctx.send("unloaded")


@bot.command()
async def reload(ctx, extensions):
    bot.unload_extension(f"cogs.{extensions}")  # отгружаем ког
    bot.load_extension(f"cogs.{extensions}")  # загружаем
    await ctx.send("reloaded")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
