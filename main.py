import sqlite3, nextcord, dotenv, os
from nextcord import Intents, Interaction, Role, SlashOption
from nextcord.ext import commands, application_checks
from dotenv import load_dotenv
from typing import Optional
from utils import *

load_dotenv()
print("Please input bot number: ")
f = open(".env", encoding='UTF-8')
list_bot = f.read().replace('\n', ' = ').split(' = ')
range_len = len(list_bot)
if range_len == 1:
    range_len = int(1)
else:
    range_len = int(range_len/2)
for x in range(0,range_len):
    list_bot.pop((x*2)-1)
for x in range(0,len(list_bot)):
    print(f"{x}. ",list_bot[x])
valid = False
while not valid:
    BOT_NB = input()
    try:
        os.getenv(list_bot[int(BOT_NB)])
        valid = True
        print(f"Loading {list_bot[int(BOT_NB)]}")
    except:
        print("Invalid number please re-input")

activity = nextcord.Game("main.py")

intents = Intents.all()
intents.message_content = True
bot = commands.Bot(activity=activity,intents=intents)

conn = sqlite3.connect("bot.db")
c = conn.cursor()

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready.")
    c.execute("""CREATE TABLE IF NOT EXISTS settings (
        guild_id integer,
        name text,
        value
    )
    """
    )

@bot.event
async def on_application_command_error(interaction:Interaction, error):
    error = getattr(error, "original", error)
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        await interaction.response.send_message("You lack the permission to perform this command.")
    elif isinstance(error, application_checks.ApplicationNotOwner):
        await interaction.response.send_message("You do not own this bot.")
    else:
        raise error

help_content = ("Receive help.", "Allows receiving and losing roles.", "The role you want to receive or lose.", "Display a list of all roles enabled on this server.", "Display a list of the roles you currently have.", "Create a new role selector.", "Remove an existing role selector.", "Add a role into the dropdown.", "Remove a role from the dropdown.", "The emoji shown in the dropdown.", "The description shown in the dropdown.", "The role you want to add.", "The role you want to remove.", "The name of the dropdown.", "Display a list of the objects created on this server.", "The page to display.", "Choose a category of commands.")
#                     0                           1                                      2                                           3                                                    4                                           5                                 6                                    7                                8                                 9                                         10                                    11                             12                          13                                          14                                      15                            16        

@bot.slash_command()
async def settings(interaction:Interaction):
    """Settings group"""
    pass

@settings.subcommand(description=help_content[5])
@application_checks.has_permissions(manage_roles=True)
async def dropdown_add(interaction:Interaction, dropdown_name:str = SlashOption(description=help_content[13])):
    """Create dropdown table"""
    if " " in dropdown_name or "." in dropdown_name:
        await interaction.response.send_message("Cannot create dropdown, name contains space(s) or period(s).")
    else:
        if c.execute(f"SELECT name FROM sqlite_master where name = 'DROPDOWN.{dropdown_name}.{interaction.guild.id}' and type = 'table'").fetchone() != None:
            await interaction.response.send_message(f"Role selector \"{dropdown_name}\" already exist.")
        else:
            c.execute(f"""CREATE TABLE 'DROPDOWN.{dropdown_name}.{interaction.guild.id}' (
                role text,
                emoji text,
                desc text,
                role_order integer
            )"""
            )
            await interaction.response.send_message(f"Role selector \"{dropdown_name}\" successfully created.")

@settings.subcommand(description=help_content[6])
@application_checks.has_permissions(manage_roles=True)
async def dropdown_remove(interaction:Interaction, dropdown_name:str = SlashOption(description=help_content[13])):
    """Remove dropdown table"""
    try:
        c.execute(f"DROP TABLE 'DROPDOWN.{dropdown_name}.{interaction.guild.id}'")
        await interaction.response.send_message(f"Role selector \"{dropdown_name}\" successfully deleted.")
    except:
        await interaction.response.send_message(f"Role selector \"{dropdown_name}\" does not exist.")

@settings.subcommand(description=help_content[14])
async def db_list(interaction:Interaction, page:Optional[int] = SlashOption(description=help_content[15])):
    """database list"""
    await get_page_dblist(interaction, page)

@settings.subcommand(description=help_content[7])
@application_checks.has_permissions(manage_roles=True)
async def role_add(interaction:Interaction, dropdown_name:str = SlashOption(description=help_content[13]), role:Role = SlashOption(description=help_content[11]), emoji:Optional[str] = SlashOption(description=f"{help_content[9]} (Optional)"), desc:Optional[str] = SlashOption(description=f"{help_content[10]} (Optional)")):
    """Add to the dropdown"""

@settings.subcommand(description=help_content[8])
@application_checks.has_permissions(manage_roles=True)
async def role_remove(interaction:Interaction, dropdown_name:str = SlashOption(description=help_content[13]), role:Role = SlashOption(description=help_content[12])):
    """Remove from the dropdown"""

@bot.slash_command(description=help_content[1])
async def roles(interaction:Interaction, role:Optional[Role] = SlashOption(description=f"{help_content[2]} (Optional)")):
    """Outputs RoleMenu or give/remove roles"""
    if role == None:
        view = RoleMenuView(interaction)
        await interaction.response.send_message("Select the roles you wish to receive or lose: ",view=view)
    else:
        await interaction.response.send_message("This feature isn't added.")

@bot.slash_command(description=help_content[0])
async def help(interaction:Interaction, category:Optional[str] = SlashOption(description=help_content[16], choices={"acommands":"acommands","bcommands":"bcommands"})):
    """Help embed"""
    acommands = f"""
    </roles:1047746068147875880>
    {help_content[1]}

    > `role` (Optional)
    > {help_content[2]}

    </help:1047746069347438592>
    {help_content[0]}
    """
    bcommands = f"""
    </settings dropdown_add:1048307053728370749>
    {help_content[5]}

    > `dropdown_name`
    > {help_content[13]}

    </settings dropdown_remove:1048307053728370749>
    {help_content[6]}

    > `dropdown_name`
    > {help_content[13]}

    </settings db_list:1048307053728370749>
    {help_content[14]}

    > `page`
    > {help_content[15]}
    """

    if category == "acommands":
        set_title = "Help - Main Commands:"
        set_desc = "This is the list of main commands."
        set_commands_1 = acommands
        set_commands_2 = " "

    embed = nextcord.Embed(title=set_title, description=set_desc, color=0xf1c40f)
    embed.add_field(name=" ", value=set_commands_1, inline=True)
    embed.add_field(name=" ", value=set_commands_2, inline=True)

    await interaction.response.send_message(embed=embed)

@bot.slash_command()
@application_checks.is_owner()
async def debug(interaction:Interaction):
    await interaction.response.send_message("enabled")
    loop = True
    while loop:
        print("You can input.")
        querry = input()
        if querry == "$stop":
            loop = False
        else:
            print(eval(querry))
    await interaction.channel.send("disabled")

try:
    bot.run(os.getenv(list_bot[int(BOT_NB)]))
except:
    print("No response. The token might be invalid or the connection failed.")