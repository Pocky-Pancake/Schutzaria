import sqlite3, nextcord
from nextcord import Interaction, SelectOption, ButtonStyle
from nextcord.ui import View, Select, Button

conn = sqlite3.connect("bot.db")
c = conn.cursor()

async def get_page_dblist(interaction, page:int) -> None:
    nextpage = Button(label="Next", style=ButtonStyle.blurple)
    prevpage = Button(label="Prev", style=ButtonStyle.blurple)
    refreshpage = Button(label="Refresh", style=ButtonStyle.blurple)
    view = View(timeout=600)
    view.add_item(prevpage)
    view.add_item(refreshpage)
    view.add_item(nextpage)

    db_data = c.execute("SELECT name FROM sqlite_master where type = 'table'").fetchall()
    db_data.remove(('settings',))

    db_content = "This is the list of objects registered on this server.\n\n"

def get_help(interaction, category) -> None:
    print("x")

class HelpDropdown(Select):
    """Help Dropdown"""
    def __init__(self, interaction):
        HelpOptions = [
            SelectOption(label="Main Commands", value=0)
        ]
        super().__init__(placeholder="Choose category", min_values=1, max_values=1, options=HelpOptions)
        self.slash_interaction = interaction
    
    async def callback(self, interaction:Interaction):
        if slash_interaction.user == interaction.user:
            print("x")
        else:
            await interaction.response.send_message("Only the caller can do that", ephemeral=True)

class HelpView(View):
    def __init__(self, interaction):
        super().__init__()
        self.add_item(HelpDropdown(interaction))

class RoleMenu(Select):
    """Dropdown UI"""
    def __init__(self, interaction):
        RoleOptions = [
            SelectOption(label="Drama CD Editor", emoji="💿", value="Drama CD Editor")
        ]
        max_value = 1
        super().__init__(placeholder="Select Roles", min_values=1, max_values=max_value, options=RoleOptions)
        self.caller = interaction.user

    async def callback(self, interaction:Interaction):
        if self.caller != interaction.user:
            await interaction.response.send_message("Only the caller can do that", ephemeral=True)
        else:
            return await interaction.response.send_message(self.values)

class RoleMenuView(View):
    def __init__(self, interaction):
        super().__init__()
        self.add_item(RoleMenu(interaction))