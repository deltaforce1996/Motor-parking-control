import discord
from discord import Interaction, ButtonStyle
from discord.ui import Button, View
from discord.ext import commands
from table2ascii import table2ascii, Alignment
import aiohttp
import asyncio

class Assets():
    def __init__(self, url):
        self.url = url

    async def get_assets_all(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    if response.status == 200:
                      return await response.json()

                    if response.status == 400:
                        return None

                    if response.status == 404:
                        return None
        except aiohttp.ClientError:
            print("HTTP Client Error, possibly the server is down")
            return None
        except asyncio.TimeoutError:
            print("Request timeout, possibly the server is down")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return None

    # def unlocked_assets(self, assetPath):
    #     try:
    #         async with aiohttp.ClientSession() as session:
    #             async with session.post(self.url) as response:
    #                 if response.status == 200:
    #                   return await response.json()

    #                 if response.status == 400:
    #                     return None

    #                 if response.status == 404:
    #                     return None
    #     except aiohttp.ClientError:
    #         print("HTTP Client Error, possibly the server is down")
    #         return None
    #     except asyncio.TimeoutError:
    #         print("Request timeout, possibly the server is down")
    #         return None
    #     except Exception as e:
    #         print(f"An unexpected error occurred: {str(e)}")
    #         return None



fetch_assets = Assets("http://localhost:3000/api/v1/assets")

class FetchButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=ButtonStyle.green, emoji='📒')

    async def callback(self, interaction: Interaction):

        data_response = await fetch_assets.get_assets_all()

        if data_response == None: 
            await interaction.response.send_message("⛔ Assets not found!!")
            return

        headers = ["Path", "Username", "Datetime", "Status"]
        rows = [[item["assetPath"].split(
                    "/")[-1], item["userName"], item["datetime"], '🔓' if item["userName"] == "" else '🔒'] for item in data_response["data"]]
        table = table2ascii(header=headers, body=rows, alignments=[
        Alignment.LEFT, Alignment.CENTER, Alignment.CENTER, Alignment.CENTER])

        await interaction.response.send_message(f"```\n{table}\n```", ephemeral=True)

       
class GridView(View):
    def __init__(self, response_data):
        super().__init__(timeout=None)
        for item in response_data["data"]:
            if item["userName"] != "":
                button = Button(label=item["assetPath"].split(
                    "/")[-1] + " -> by [" + item["userName"] + "]", custom_id=item["assetPath"], emoji='🔒')
                button.callback = self.on_interaction
                self.add_item(button)
        return

    async def interaction_check(self, interaction: Interaction) -> bool:
        return True

    async def on_interaction(self, interaction: Interaction):
        if self.interaction_check:
            await interaction.response.send_message(f"You unlocked 🔓 {interaction.data['custom_id']}! successfully 👌🏾", ephemeral=True)


class UnlockButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=ButtonStyle.primary, emoji='🔓')

    async def callback(self, interaction: Interaction):
        data_response = await fetch_assets.get_assets_all()

        if data_response == None: 
            await interaction.response.send_message("⛔ Assets not found!!")
            return

        view = GridView(data_response)
        await interaction.response.send_message("List of assets path", view=view, ephemeral=True)


TOKEN = 'MTE1NzkyMDI2OTY4ODYzNTQ0Mw.Gwg5ex.eYSu1Cf0icDAztkv4tJ5SpK8p1XSr_InK-R8r8'
PREFIX = '!'
CHANNEL_ID = 1157988285470216313

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

async def is_user(ctx):
    return ctx.author.id != bot.user.id


@bot.command()
@commands.check(is_user)
async def option(ctx):
    try:
        target_channel = bot.get_channel(CHANNEL_ID)

        view_content = View()
        view_content.add_item(FetchButton("Fatch Assets All"))
        view_content.add_item(UnlockButton("Unlock! Assets"))
        await target_channel.send("Hi! i am 🤖, Can i help you. :)", view=view_content)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# @bot.event
# async def on_message(message):
#     if message.author.id == bot.user.id and message.content != '!greet': return
#     if message.author.id != bot.user.id and message.content == '!greet': return
#     print("message user id : ", message.author.id)
#     print("bot user id : ", bot.user.id)
#     print("message content : ", message.content)
#     await bot.process_commands(message)

async def is_owner(ctx):
    return ctx.author.id == bot.user.id

@bot.command()
# @commands.check(is_owner)
async def greet(ctx):
    # response = ' '.join(args) if args else 'Hello!'
    try:
        target_channel = bot.get_channel(CHANNEL_ID)

        view_content = View()
        view_content.add_item(Button(label="Yes"))
        await target_channel.send(
            "Hello! Do you like this greeting?",
            view=view_content
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('⛔ Sorry, I do not recognize that command.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('⛔ You are missing a required argument.')
    else:
        await ctx.send('⛔ An error occurred while processing the command.')
        print(f'Error: {error}')

bot.run(TOKEN)
