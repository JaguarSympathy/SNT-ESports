# *******************************************************
# This file is part of the SNT-Esports project. Please see the README.md file for information.
#  
# This file and its content can not be copied and/or distributed without the express
# permission of JaguarSympathy.
#
# The project is developed solely and indepedently by JaguarSympathy. All rights are reserved.
# *******************************************************

import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import json

load_dotenv()

# -- CONSTANTS -- #
TOKEN = os.getenv("DISCORD_CLIENT_TOKEN")
WELCOME_CHANNEL = 000000000000000000
IMG_WELCOME = "https://media.discordapp.net/attachments/1336054298400002108/1337101833629466625/standard_8.gif"

# -- Initialisation -- #
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client=client)

# -- Events -- #
@client.event
async def on_ready():
    await tree.sync()

    global WELCOME_CHANNEL,IMG_WELCOME
    with open("settings.json","r") as f:
        settingsData = json.load(f)
        WELCOME_CHANNEL = settingsData["welcome_channel"]
        IMG_WELCOME = settingsData["img_welcome"]


@client.event
async def on_member_join(member: discord.Member):
    channel = await client.fetch_channel(WELCOME_CHANNEL)
    embed = discord.Embed(title=f"Welcome to {member.guild.name} {member.name}!",description="Please read the rules. Apply for the team via our application tickets. Enjoy!",colour=discord.Colour.purple())
    embed.set_image(IMG_WELCOME)
    await channel.send(f"Welcome {member.mention}!", embed=embed)

# -- Commands -- #
@tree.command(name="settings",description="Update bot settings")
@app_commands.describe(setting="Setting to update",value="Value to set")
@app_commands.choices(setting=[app_commands.Choice(name="Welcome Channel",value="Welcome Channel"),app_commands.Choice(name="Welcome Image",value="Welcome Image")])
async def settings(interaction: discord.Interaction, setting: str, value: str):
    global WELCOME_CHANNEL,IMG_WELCOME
    if setting == "Welcome Channel":
        WELCOME_CHANNEL = value
        with open("settings.json","w") as f:
            json.dump({"welcome_channel":WELCOME_CHANNEL,"img_welcome":IMG_WELCOME},f)
        
        await interaction.response.send_message("Updated welcome channel.",ephemeral=True)
    elif setting == "Welcome Image":
        IMG_WELCOME = value
        with open("settings.json","w") as f:
            json.dump({"welcome_channel":WELCOME_CHANNEL,"img_welcome":IMG_WELCOME},f)

        await interaction.response.send_message("Updated welcome image.",ephemeral=True)
    else:
        await interaction.response.send_message("Invalid setting",ephemeral=True)

client.run(TOKEN)