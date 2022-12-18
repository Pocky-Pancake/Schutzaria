import sqlite3, nextcord
from nextcord import Interaction, SelectOption, ButtonStyle, Embed
from nextcord.ui import View, Select, Button, TextInput, Modal
from math import ceil

conn = sqlite3.connect("bot.db")
c = conn.cursor()

async def get_obj_list(interaction, page:int, edit:int) -> None:
    nextpage = Button(label="Next", style=ButtonStyle.blurple)
    prevpage = Button(label="Prev", style=ButtonStyle.blurple)
    refreshpage = Button(label="Refresh", style=ButtonStyle.blurple)
    view = View(timeout=600)
    view.add_item(prevpage)
    view.add_item(refreshpage)
    view.add_item(nextpage)

    obj_data_unfiltered = c.execute("SELECT name FROM sqlite_master where type = 'table'").fetchall()
    obj_data_unfiltered.remove(('settings',))
    obj_data_unfiltered.remove(('objectdata',))
    obj_data = []
    for x in obj_data_unfiltered:
        if str(interaction.guild.id) in x[0]: 
            obj_data.append(x[0])

    obj_content = "This is the list of objects registered on this server.\n\n"
    last_page = ceil(len(obj_data)/10)
    caller = interaction.user

    if page == None or page <= 0:
        if last_page == 0:
            page = int(0)
        else:
            page = int(1)
    elif page > last_page:
        page = last_page

    async def callback_next(interaction):
        if interaction.user == caller:
            await get_obj_list(interaction, page=page+1, edit=1)
        else:
            await get_obj_list(interaction, page=page+1, edit=2)

    async def callback_refresh(interaction):
        if interaction.user == caller:
            await get_obj_list(interaction, page=page, edit=1)
        else:
            await get_obj_list(interaction, page=page, edit=2)

    async def callback_prev(interaction):
        if interaction.user == caller:
            await get_obj_list(interaction, page=page-1, edit=1)
        else:
            await get_obj_list(interaction, page=page-1, edit=2)

    nextpage.callback = callback_next
    refreshpage.callback = callback_refresh
    prevpage.callback = callback_prev
    
    for x in obj_data[(((page*10)-10)):(10+((page*10)-10))]:
        try:
            data_split = x.split('.')
            obj_content += f"• {data_split[0]} - {data_split[1]}\n`{x}`\n\n"
        except:
            pass
    
    embed = Embed(title="Object List", description=obj_content, color=0xf1c40f)
    embed.set_footer(icon_url=interaction.guild.icon, text=f"{interaction.guild} • Page ({page}/{last_page})")
    if edit == 0:
        await interaction.response.send_message(embed=embed, view=view)
    elif edit == 1:
        await interaction.response.edit_message(embed=embed, view=view)
    elif edit == 2:
        await interaction.response.send_message(f"{interaction.user.mention}",embed=embed, view=view)

async def get_help(interaction, category:int, help_content:list, edit:int) -> None:
    class HelpDropdown(Select):
        """Help Dropdown"""
        def __init__(self, interaction):
            HelpOptions = [
                SelectOption(label="Main Commands", value=0),
                SelectOption(label="Settings Commands", value=1),
                SelectOption(label="List Commands", value=2)
            ]
            super().__init__(placeholder="Choose category", min_values=1, max_values=1, options=HelpOptions)
            self.caller = interaction.user
    
        async def callback(self, interaction:Interaction):
            if self.caller == interaction.user:
                await get_help(interaction, int(self.values[0]), help_content, edit=1)
            else:
                await get_help(interaction, int(self.values[0]), help_content, edit=2)
    class HelpView(View):
        def __init__(self, interaction):
            super().__init__(timeout=600)
            self.add_item(HelpDropdown(interaction))
    view = HelpView(interaction)

    if category == None:
        set_desc = """This is the help menu.

        *⬇️ Please select a category using the dropdown below. ⬇️*"""
        set_title = "Help"
    elif category == 0:
        set_desc = f"""
        </roles:1047746068147875880>
        {help_content[1]}

        > `role` [Role](Optional)
        > {help_content[2]}

        </help:1047746069347438592>
        {help_content[0]}

        > `category` [Choice](Optional)
        > {help_content[16]}

        </ping:1048634962808672256>
        {help_content[17]}"""
        set_title = "Help - Main Commands"
    elif category == 1:
        set_desc = f"""
        </settings dropdown_add:1048307053728370749>
        {help_content[5]}

        > `dropdown_name` [Text]
        > {help_content[13]}

        </settings dropdown_remove:1048307053728370749>
        {help_content[6]}

        > `dropdown_name` [Text]
        > {help_content[13]}"""
        set_title = "Help - Settings Commands"
    else:
        set_desc = "This category is invalid or <@544655732142768151> is too lazy to add it."
        set_title = "Help - Unknown"
    
    embed = Embed(title=set_title, description=set_desc, color=0xf1c40f)
    if edit == 0:
        await interaction.response.send_message(embed=embed, view=view)
    elif edit == 1:
        await interaction.response.edit_message(embed=embed, view=view)
    elif edit == 2:
        await interaction.response.send_message(f"{interaction.user.mention}",embed=embed, view=view)


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
        super().__init__(timeout=600)
        self.add_item(RoleMenu(interaction))

class ObjectModal(Modal):
    def __init__(self, object_type):
        ModalTitle = "Test"
        super().__init__(
            ModalTitle,
        )

        self.object_type = object_type

        self.selectname = TextInput(label="Role Name", min_length=1, required=True, placeholder="test", style=nextcord.TextInputStyle.short,)
        self.add_item(self.selectname)
        self.roleid = TextInput(label="Role ID", min_length=1, required=True, placeholder="test", style=nextcord.TextInputStyle.paragraph,)
        self.add_item(self.roleid)

    async def callback(self, interaction:Interaction) -> None:
        object_type = self.object_type
        
        selectname = self.selectname.value
        roleid = self.roleid.value

        await interaction.response.send_message("Test")
        return 0
