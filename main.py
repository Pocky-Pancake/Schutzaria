import sqlite3, nextcord, dotenv, os
from nextcord import Intents, Interaction, Role, SlashOption, Embed
from nextcord.ext import commands, application_checks
from dotenv import load_dotenv
from typing import Optional
from utils import *
from permission_decalculator import DecalcPerms

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
    c.execute("""CREATE TABLE IF NOT EXISTS objectdata (
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

help_content = (
    "Receive help.", # 0 
    "Allows receiving and losing roles.", # 1
    "The role you want to receive or lose.", # 2
    "Display a list of all roles enabled on this server.", # 3
    "Display a list of the roles you currently have.", # 4
    "Create a new role selector.", # 5
    "Remove an existing role selector.", # 6
    "Add a role into the dropdown.", # 7
    "Remove a role from the dropdown.", # 8
    "The emoji shown in the dropdown.", # 9
    "The description shown in the dropdown.", # 10
    "The role you want to add.", # 11
    "The role you want to remove.", # 12
    "The name of the dropdown.", # 13
    "Display a list of the objects created on this server.", # 14
    "The page to display.", # 15
    "Choose a category of commands.", # 16
    "Pong! Check bot's latency.", # 17
    "Fetch a detailled profile.", # 18
    "User to fetch from.", # 19
    "Add content to object.", # 20
    "The name of the object." # 21
)

@bot.slash_command()
async def settings(interaction:Interaction):
    """Settings group"""
    pass

@settings.subcommand(description=help_content[5])
@application_checks.has_permissions(manage_roles=True)
async def dropdown_add(interaction:Interaction, dropdown_name:str = SlashOption(description=help_content[13])):
    """Create dropdown table"""
    if " " in dropdown_name or "." in dropdown_name or not dropdown_name.isalpha():
        await interaction.response.send_message("Cannot create dropdown, name contains space(s), period(s) or number(s).")
    elif "DROPDOWN" in dropdown_name:
        await interaction.response.send_message("Cannot create dropdown, name cannot be of the following:\n`DROPDOWN`")
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

@settings.subcommand(description=help_content[7])
@application_checks.has_permissions(manage_roles=True)
async def role_add(interaction:Interaction, dropdown_name:str = SlashOption(description=help_content[13]), role:Role = SlashOption(description=help_content[11]), emoji:Optional[str] = SlashOption(description=f"{help_content[9]} (Optional)"), desc:Optional[str] = SlashOption(description=f"{help_content[10]} (Optional)")):
    """Add to the dropdown"""

@settings.subcommand(description=help_content[8])
@application_checks.has_permissions(manage_roles=True)
async def role_remove(interaction:Interaction, dropdown_name:str = SlashOption(description=help_content[13]), role:Role = SlashOption(description=help_content[12])):
    """Remove from the dropdown"""

@bot.slash_command()
async def objects(interaction:Interaction):
    """List group"""
    pass

@objects.subcommand(name="list", description=help_content[14])
async def objlist(interaction:Interaction, page:Optional[int] = SlashOption(description=help_content[15])):
    """database list"""
    await get_obj_list(interaction, page, edit=0)

@objects.subcommand(description=help_content[20])
async def add_content(interaction:Interaction, object_name:str = SlashOption(description=help_content[21])):
    await interaction.response.send_modal(ObjectModal("DROPDOWN"))

@bot.slash_command(description=help_content[1])
async def roles(interaction:Interaction, role:Optional[Role] = SlashOption(description=f"{help_content[2]} (Optional)")):
    """Outputs RoleMenu or give/remove roles"""
    if role == None:
        view = RoleMenuView(interaction)
        await interaction.response.send_message("Select the roles you wish to receive or lose: ",view=view)
    else:
        await interaction.response.send_message("This feature isn't added.")

@bot.slash_command(description=help_content[0])
async def help(interaction:Interaction, category:Optional[int] = SlashOption(description=help_content[16], choices={"Main Commands":0,"Settings Commands":1,"List Commands":2})):
    """Help embed"""
    await get_help(interaction, category, help_content, edit=0)

@bot.slash_command(description=help_content[17])
async def ping(interaction:Interaction):
    embed = Embed(title="Pong!", description=f"💓⏲️ {bot.latency}", color=0xf1c40f)
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name="profile", description=help_content[18])
async def fetch_profile(interaction:Interaction, member:Optional[nextcord.Member] = SlashOption(description=help_content[19])):
    if not member:
        try_status = interaction.user.status # fixes weird bug
        guild = bot.get_guild(interaction.guild.id)
        member = await guild.fetch_member(interaction.user.id)
        user = await bot.fetch_user(interaction.user.id)
    else:
        user = await bot.fetch_user(member.id)
    def get_status_emoji(method):
        if method == "dnd":
            return "<:dnd:1051224321621757972>"
        elif method == "online":
            return "<:online:1051224319545577502>"
        elif method == "idle":
            return "<:idle:1051224316919943179>"
        elif method == "offline":
            return "<:offline:1051224324385820776>"
        else:
            return 0xff
    set_timeout = ""
    if member.nick:
        set_title = member.nick
        try:
            set_desc = get_status_emoji(try_status) + f" {try_status.replace('dnd','do not disturb').capitalize()}"
        except:
            set_desc = get_status_emoji(member.status) + f" {member.status.replace('dnd','do not disturb').capitalize()}"
        if member.communication_disabled_until != None:
            set_timeout = f"\nCurrently timed-out on this server until:\n{member.communication_disabled_until}"
    else:
        set_title = member.name
        try:
            set_desc = get_status_emoji(try_status) + f" {try_status.replace('dnd','do not disturb').capitalize()}"
        except:
            set_desc = get_status_emoji(member.status) + f" {member.status.replace('dnd','do not disturb').capitalize()}"
        if member.communication_disabled_until != None:
            set_timeout = f"\nCurrently timed-out on this server until:\n{member.communication_disabled_until}"
    embed = Embed(title=set_title, description=f"{set_desc}{set_timeout}", color=member.colour)
    if member.guild_avatar:
        embed.set_thumbnail(member.guild_avatar.url)
    else:
        embed.set_thumbnail(member.display_avatar.url)
    if member.banner:
        embed.set_image(member.banner.url)
    elif user.banner:
        embed.set_image(user.banner.url)
    if member.nick:
        embed.add_field(name="Identity", value=f"{member}\n{member.nick}\n{member.id}", inline=False)
    else:
        embed.add_field(name="Identity", value=f"{member}\n{member.id}", inline=False)
    role_field = ""
    for x in member.roles:
        if x.mention != "@everyone":
            role_field += f"{x.mention} "
    if role_field == "":
        role_field = "This user doesn't have any roles."
    if len(member.roles) == 2 or len(member.roles) == 1:
        embed.add_field(name="Role", value=role_field, inline=False)
    else:
        embed.add_field(name="Roles", value=role_field, inline=False)
    member_perms = DecalcPerms(member.guild_permissions.value)
    set_perms = ""
    for x in member_perms:
        set_perms += f"`{x}` "
    if set_perms == "":
        set_perms = "This user has no permissions."
    if len(member_perms) == 1 or len(member_perms) == 0:
        embed.add_field(name="Permission", value=set_perms, inline=False)
    else:
        embed.add_field(name="Permissions", value=set_perms, inline=False)
    embed.add_field(name="Join Date", value=f"Server: {member.joined_at}\nDiscord: {user.created_at}", inline=False)
    embed.set_footer(icon_url=interaction.guild.icon, text=interaction.guild)

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