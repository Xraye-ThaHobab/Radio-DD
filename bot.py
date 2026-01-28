import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import Select, View
from discord import FFmpegPCMAudio
import asyncio

# ===== Bot setup =====
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

TOKEN = "dBvnWnnQoWuh4xJYzEsCPMdwuBX19oVx"

# ===== Radio List =====
RADIOS = {
    "🤠 Country Vibes": "https://radio.9craft.ir:7443/country",
    "🔥 HipHop Mood": "https://radio.9craft.ir:7443/hiphop",
    "🌙 Lofi Chill": "https://radio.9craft.ir:7443/lofi",
    "🎌 Anime OST": "https://radio.9craft.ir:7443/ost",
    "📼 Persian Oldschool": "https://radio.9craft.ir:7443/persian",
    "💀 Melo Phonk": "https://radio.9craft.ir:7443/phonk",
    "🕺 Funk Energy": "https://radio.9craft.ir:7443/phonk2",
    "🎤 Rap Farsi": "https://radio.9craft.ir:7443/prap",
}

# ===== Select Menu =====
class RadioSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=name, value=url)
            for name, url in RADIOS.items()
        ]
        super().__init__(placeholder="🎶 Radio ha ro entekhab kon ...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        if not user.voice or not user.voice.channel:
            await interaction.response.send_message("❌ Dar voice channel nisti!", ephemeral=True)
            return

        channel = user.voice.channel

        # Disconnect if already connected
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()

        # Connect and play
        vc = await channel.connect()
        source = FFmpegPCMAudio(self.values[0], options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
        vc.play(source)

        embed = discord.Embed(
            title="🎧 Now Playing",
            description=f"{self.values[0]} ro dar voice channel shoru kardim!",
            color=0x1abc9c
        )
        embed.set_footer(text="made with 🧠&🩷 by apaxray")
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Auto-leave task
        async def check_leave():
            await asyncio.sleep(10)
            if not vc.channel.members or len([m for m in vc.channel.members if not m.bot]) == 0:
                await vc.disconnect()
        bot.loop.create_task(check_leave())

# ===== View =====
class RadioView(View):
    def __init__(self):
        super().__init__()
        self.add_item(RadioSelect())

# ===== Slash command =====
@tree.command(name="radio", description="Radio ha ro entekhab kon")
async def radio(interaction: discord.Interaction):
    view = RadioView()
    await interaction.response.send_message("🎶 Radio ha ro entekhab kon:", view=view, ephemeral=True)

# ===== Events =====
@bot.event
async def on_ready():
    print(f"Bot Online: {bot.user}")
    await tree.sync()

# ===== Run Bot =====
bot.run(TOKEN)
