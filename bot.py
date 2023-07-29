from discord import app_commands
import discord
import discord.ui

import datetime
import pytz
import os


from dotenv import load_dotenv
load_dotenv()

token = os.getenv("BOT_TOKEN")

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

def epoch_time_in_seconds(time_date_str, timezone_str):
    # Parse the input string to a datetime object
    local_tz = pytz.timezone(timezone_str)
    naive_dt = datetime.datetime.strptime(time_date_str, "%m/%d/%y %I:%M %p")
    
    # Attach the timezone info to the datetime object
    local_dt = local_tz.localize(naive_dt)
    
    # Convert the localized datetime to UTC
    utc_dt = local_dt.astimezone(pytz.utc)
    
    # Calculate the epoch time in seconds
    epoch_time_seconds = (utc_dt - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
    return int(epoch_time_seconds)

class TimestampModal(discord.ui.Modal, title="Timezone"):
    timezone = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Timezone",
        required=True,
        placeholder="US/Eastern, US/Central, US/Mountain, US/Pacific"
    )

    dateandtime = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Date and Time",
        required=True,
        placeholder="M/D/Y H:M AM/PM (7/29/23 12:30 PM)",
        max_length=17,
        min_length=14,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        epoch_time = epoch_time_in_seconds(self.dateandtime.value, self.timezone.value)
        embed=discord.Embed(color=0xe60000)
        embed.set_author(name="Timestamp Generator")
        embed.add_field(name="Full Date", value="`<t:" + str(epoch_time) + ":F>`\n<t:" + str(epoch_time) + ":F>", inline=False)
        embed.add_field(name="Full Date w/o Day", value="`<t:" + str(epoch_time) + ":f>`\n<t:" + str(epoch_time) + ":f>", inline=False)
        embed.add_field(name="Time", value="`<t:" + str(epoch_time) + ":t>`\n<t:" + str(epoch_time) + ":t>", inline=False)
        embed.add_field(name="Date", value="`<t:" + str(epoch_time) + ":D>`\n<t:" + str(epoch_time) + ":D>", inline=False)
        embed.add_field(name="Relative", value="`<t:" + str(epoch_time) + ":R>`\n<t:" + str(epoch_time) + ":R>", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=776551430794117132))
    print('Bot ready')

@tree.command(name = "timestamp", description = "Generate Timestamp", guild=discord.Object(id=776551430794117132))
async def timestamp(interaction):
    await interaction.response.send_modal(TimestampModal())


client.run(token)
