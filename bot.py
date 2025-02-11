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
LEVELING_REQUIREMENT = 100
DEVELOPER = 610020302692417546
OWNER = 1141388902268153856
ANNOUNCEMENTS = 1322616470244429964
SNT_GUILD = 1318946168943677472
LEVELING_CHANNEL = 1327362472318996551

# -- Initialisation -- #
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client=client)

# -- Events -- #
@client.event
async def on_ready():
    await tree.sync()

    global WELCOME_CHANNEL,IMG_WELCOME,LEVELING_REQUIREMENT,LEVELING_CHANNEL
    with open("settings.json","r") as f:
        settingsData = json.load(f)
        WELCOME_CHANNEL = settingsData["welcome_channel"]
        IMG_WELCOME = settingsData["img_welcome"]
        LEVELING_REQUIREMENT = settingsData["leveling_requirement"]
        LEVELING_CHANNEL = settingsData["leveling_channel"]


@client.event
async def on_member_join(member: discord.Member):
    channel = await client.fetch_channel(WELCOME_CHANNEL)
    embed = discord.Embed(title=f"Welcome to {member.guild.name} {member.name}!",description="Please read the rules. Apply for the team via our application tickets. Enjoy!",colour=discord.Colour.purple())
    embed.set_image(url=IMG_WELCOME)
    await channel.send(f"Welcome {member.mention}!", embed=embed)

@client.event
async def on_message(message: discord.Message):
    if message.author.bot == False and message.guild.id == SNT_GUILD:
        with open("leveling.json","r") as f:
            levelingData:dict = json.load(f)

        try:
            levelingData[str(message.author.id)]["xp"] = levelingData[str(message.author.id)]["xp"] + 1
        except KeyError:
            levelingData[str(message.author.id)] = {"xp":0,"level":0}


        level = levelingData[str(message.author.id)]["xp"] // int(LEVELING_REQUIREMENT)
        if level > levelingData[str(message.author.id)]["level"]:
            levelingData[str(message.author.id)]["level"] = level

            await message.channel.send(f"Congratulations {message.author.mention}! You have reached level {level}!")

        with open("leveling.json","w") as f:
            json.dump(levelingData,f)
            f.close()

    if message.author.id == DEVELOPER:
        if message.content.startswith("!announce "):
            channel = await client.fetch_channel(ANNOUNCEMENTS)
            await channel.send(message.content[10:])
            
@client.event
async def on_reaction_add(reaction: discord.Reaction,member: discord.Member):
    with open("reaction_roles.json","r") as f:
        reactionRoles = json.load(f)
    
    try:
        role = discord.utils.get(member.guild.roles,id=reactionRoles[reaction.message.id][reaction.emoji])
        await member.add_roles(role)
    except KeyError:
        pass

@client.event
async def on_reaction_remove(reaction: discord.Reaction,member: discord.Member):
    with open("reaction_roles.json","r") as f:
        reactionRoles = json.load(f)
    
    try:
        role = discord.utils.get(member.guild.roles,id=reactionRoles[reaction.message.id][reaction.emoji])
        await member.remove_roles(role)
    except KeyError:
        pass

# -- Commands -- #
@tree.command(name="settings",description="Update bot settings")
@app_commands.describe(setting="Setting to update",value="Value to set")
@app_commands.choices(setting=[app_commands.Choice(name="Welcome Channel",value="Welcome Channel"),app_commands.Choice(name="Welcome Image",value="Welcome Image"),app_commands.Choice(name="Leveling Requirement",value="Leveling Requirement"),app_commands.Choice(name="Leveling Channel",value="Leveling Channel")])
async def settings(interaction: discord.Interaction, setting: str, value: str):
    if interaction.user.id == DEVELOPER or interaction.user.id == OWNER:
        global WELCOME_CHANNEL,IMG_WELCOME,LEVELING_REQUIREMENT,LEVELING_CHANNEL
        if setting == "Welcome Channel":
            WELCOME_CHANNEL = int(value)
            with open("settings.json","w") as f:
                json.dump({"welcome_channel":WELCOME_CHANNEL,"img_welcome":IMG_WELCOME,"leveling_requirement":LEVELING_REQUIREMENT,"leveling_channel":LEVELING_CHANNEL},f)
            
            await interaction.response.send_message(f"Updated welcome channel to {value}.",ephemeral=True)
        elif setting == "Welcome Image":
            IMG_WELCOME = value
            with open("settings.json","w") as f:
                json.dump({"welcome_channel":WELCOME_CHANNEL,"img_welcome":IMG_WELCOME,"leveling_requirement":LEVELING_REQUIREMENT,"leveling_channel":LEVELING_CHANNEL},f)
            
            await interaction.response.send_message(f"Updated welcome image to {value}.",ephemeral=True)
        elif setting == "Leveling Requirement":
            LEVELING_REQUIREMENT = int(value)
            with open("settings.json","w") as f:
                json.dump({"welcome_channel":WELCOME_CHANNEL,"img_welcome":IMG_WELCOME,"leveling_requirement":LEVELING_REQUIREMENT,"leveling_channel":LEVELING_CHANNEL},f)

            await interaction.response.send_message(f"Updated leveling requirement to {value}.",ephemeral=True)
        elif setting == "Leveling Channel":
            LEVELING_CHANNEL = int(value)
            with open("settings.json","w") as f:
                json.dump({"welcome_channel":WELCOME_CHANNEL,"img_welcome":IMG_WELCOME,"leveling_requirement":LEVELING_REQUIREMENT,"leveling_channel":LEVELING_CHANNEL},f)

            await interaction.response.send_message(f"Updated leveling channel to {value}.",ephemeral=True)
        else:
            await interaction.response.send_message("Invalid setting.",ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to run this command!")

@tree.command(name="level",description="Check your current level")
async def level(interaction: discord.Interaction):
    with open("leveling.json","r") as f:
        levelingData = json.load(f)

    if interaction.user.id not in levelingData:
        levelingData[interaction.user.id] = {"xp":0,"level":0}
    
    embed = discord.Embed(title=f"Level Information",colour=discord.Colour.blurple(),timestamp=interaction.created_at)
    embed.set_author(name=interaction.user.display_name,icon_url=client.user.avatar.url).set_thumbnail(url=interaction.user.avatar.url)
    embed.add_field(name="Level",value=levelingData[interaction.user.id]["level"]).add_field(name="XP",value=levelingData[interaction.user.id]["xp"])
    await interaction.response.send_message(embed=embed)

@tree.command(name="reaction-role",description="Add or remove a reaction role")
@app_commands.describe(message="Message to add reaction role to",emoji="Emoji to react with",role="Role to add", remove="Remove the reaction role")
async def reaction_roles(interaction: discord.Interaction, message: discord.Message, emoji: str, role: discord.Role, remove: bool = False):
    if interaction.user.id == DEVELOPER or interaction.user.id == OWNER:
        with open("reaction_roles.json","r") as f:
            reactionRoles = json.load(f)
        
        if remove:
            try:
                del reactionRoles[message.id][emoji]
            except KeyError:
                await interaction.response.send_message("Reaction role not found!",ephemeral=True)
        else:
            if message.id not in reactionRoles:
                reactionRoles[message.id] = {}
            
            reactionRoles[message.id][emoji] = role.id


        with open("reaction_roles.json","w") as f:
            json.dump(reactionRoles,f)

        await interaction.response.send_message("Reaction role updated!",ephemeral=True)            
    else:
        await interaction.response.send_message("You do not have permission to run this command!")


client.run(TOKEN)