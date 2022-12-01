import sqlite3, nextcord, dotenv, os
from nextcord import Intents, Interaction
from nextcord.ext import commands
from nextcord.ui import View, RoleSelect, RoleSelectValues
from dotenv import load_dotenv

load_dotenv()

activity = nextcord.Game("main.py")

intents = Intents.all()
intents.message_content = True
bot = commands.Bot(activity=activity,intents=intents)

conn = sqlite3.connect("roleselect.db")
c = conn.cursor()

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready")

#roles_options = RoleSelectValues([nextcord.utils.get(interaction.guild.roles, id=901630465356759100)])

class RoleMenu(RoleSelect):
    def __init__(self, interaction):
        super().__init__(placeholder="Search Roles", max_values=5)
        self.caller = interaction.user

    async def callback(self, interaction:Interaction):
        if self.caller != interaction.user:
            await interaction.response.send_message("Only the caller can do that")
        else:
            await interaction.response.send_message(self.values)
            self.disabled(self, True)

class RoleMenuView(View):
    def __init__(self, interaction):
        super().__init__()
        self.add_item(RoleMenu(interaction))

@bot.slash_command(description="Testing")
async def role_select(interaction:Interaction):
    view = RoleMenuView(interaction)
    await interaction.response.send_message("Select the roles you wish to receive or lose: ",view=view)

bot.run(os.getenv('SCHUTZARIA'))