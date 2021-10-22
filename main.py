from webserver import keep_alive
import os
import nextcord
from nextcord.ext import commands
import json
import requests
import random
import asyncio
from urllib.parse import quote_plus
import youtube_dl
from dotenv import load_dotenv


load_dotenv()


PREFIX = "$"
bot = commands.Bot(command_prefix=PREFIX, description="Hi")
bot.remove_command("help")


version = "Bot v2.1"

@bot.event
async def on_ready():
	print(f"Bot logged as {bot.user} | {version}")
	await bot.change_presence(status=nextcord.Status.online,activity=nextcord.Game("$help"))


@bot.command()
async def help(ctx):
	await ctx.send(
	    f"**My commands**: {PREFIX}help | {PREFIX}ping | {PREFIX}clear | {PREFIX}hello | {PREFIX}github | {PREFIX}ver | {PREFIX}say | {PREFIX}serverinfo | {PREFIX}clean | {PREFIX}send_m | **Games**: $guess, $headortails | **Music**: $play, $join, $leave"
	)
	print(
	    f"[Logs:utils] Информация о командах бота была выведена | {PREFIX}help"
	)


@bot.command(aliases=[
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
])
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
async def say(ctx, *, text):
	await ctx.message.delete()
	author = ctx.message.author
	username = author.name
	develop = "CreeperXP"
	if username == develop:
		await ctx.message.delete()
		await ctx.send(embed=nextcord.Embed(description=text))
		print(f"[Logs:utils] Сообщение пересказано ботом | {PREFIX}say")
	else:
		await ctx.send("Ты не разработчик бота!")

@bot.command()
async def time(ctx):
	await ctx.send(f"{ctime}")
	print(f"[Logs:utils] Время было выведено: {ctime} | {PREFIX}time")


@bot.command()
async def serverinfo(ctx):
	role_count = len(ctx.guild.roles)

	serverinfoEmbed = nextcord.Embed(color=ctx.author.color)

	serverinfoEmbed.add_field(name="Название",
	                          value=f"{ctx.guild.name}",
	                          inline=False)
	serverinfoEmbed.add_field(name="Кол-во юзеров",
	                          value=f"{ctx.guild.member_count}",
	                          inline=False)
	serverinfoEmbed.add_field(
	    name="Уровень безопасности",
	    value=f"{ctx.guild.verification_level}",
	    inline=False,
	)
	serverinfoEmbed.add_field(name="Кол-во ролей",
	                          value=f"{role_count}",
	                          inline=False)
	serverinfoEmbed.add_field(name="ID сервера",
	                          value=f"{ctx.guild.id}",
	                          inline=False)

	await ctx.send(embed=serverinfoEmbed)


@bot.command()
async def userinfo(ctx, user: nextcord.User):
	user_id = user.id
	username = user.name
	avatar = user.avatar.url
	await ctx.send(f"ID: {user_id} | NICK: {username}\n{avatar}")
	print(
	    f"[Logs:utils] Информация о {username} была выведена | {PREFIX}userinfo"
	)


@bot.command(aliases = ['clear', 'purge'])
async def clean(ctx, amount=None):
	await ctx.channel.purge(limit=int(amount) + 1)
	print(f"[Logs:utils] {amount} сообщений удалено | {PREFIX}clean")


class Confirm(nextcord.ui.View):
	def __init__(self):
		super().__init__()
		self.value = None

	@nextcord.ui.button(label="Да", style=nextcord.ButtonStyle.danger)
	async def confirm(self, button: nextcord.ui.Button,
	                  interaction: nextcord.Interaction):
		await interaction.response.send_message(
		    "https://github.com/CreeperXP/xpyct_bot", ephemeral=True)
		self.value = True
		self.stop()

	@nextcord.ui.button(label="Нет", style=nextcord.ButtonStyle.blurple)
	async def cancel(self, button: nextcord.ui.Button,
	                 interaction: nextcord.Interaction):
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
	author = ctx.message.author
	user_name = author.name
	develop = "CreeperXP"
	if user_name == develop:
		await member.send(f"От {ctx.author.name}:",
		                  embed=nextcord.Embed(description=text))
		print(
		    f"[Logs:utils] Сообщение от {ctx.author.name} было отправлено {member.name} | {PREFIX}send_m"
		)
	else:
		await ctx.send("Ты не разработчик бота!")
		time.sleep(7)
		await ctx.message.delete()


@bot.command()
async def mute(ctx):
	await ctx.send(file=nextcord.File("leopold-vd.mp4"))


class Google(nextcord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f'https://www.google.com/search?q={query}'
        self.add_item(nextcord.ui.Button(label='Google', url=url))


class Yandex(nextcord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f'https://yandex.ua/search/?text={query}'
        self.add_item(nextcord.ui.Button(label='Яндекс', url=url))


@bot.command(aliases = ["поиск", "гугл"])
async def google(ctx, *, query: str):
    await ctx.reply(f'Результаты запроса `{query}`', view=Google(query))


@bot.command(aliases = ['яндекс', "yndx"])
async def yandex(ctx, *, query: str):
    await ctx.reply(f'Результаты запроса `{query}`', view=Yandex(query))


#COGS


@bot.command()  ## Стандартное объявление комманды
async def load(ctx, extensions):  ## объявление функции
	bot.load_extension(f'cogs.{extensions}')  ## загрузка доплонений
	await ctx.send("loaded")


@bot.command()
async def unload(ctx, extensions):
	bot.unload_extension(f"cogs.{extensions}")
	await ctx.send('unloaded')


@bot.command()
async def reload(ctx, extensions):
	bot.unload_extension(f"cogs.{extensions}")  # отгружаем ког
	bot.load_extension(f"cogs.{extensions}")  # загружаем
	await ctx.send('reloaded')


for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.{filename[:-3]}")

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
