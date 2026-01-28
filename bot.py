# bot.py
# Python 3.10+
# discord.py 2.x

import asyncio
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = "dBvnWnnQoWuh4xJYzEsCPMdwuBX19oVx"

INTENTS = discord.Intents.default()
INTENTS.voice_states = True

BOT_FOOTER = "made with 🧠&🩷 by apaxray"

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

FFMPEG_OPTIONS = {
    "before_options": (
        "-reconnect 1 "
        "-reconnect_streamed 1 "
        "-reconnect_delay_max 5"
    ),
    "options": "-vn",
}


class RadioSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=name,
                description="Bزن بریم یه vibe خفن 🎧",
                emoji=name.split()[0],
            )
            for name in RADIOS.keys()
        ]

        super().__init__(
            placeholder="🎶 Ye radio entekhab kon...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        voice_state = user.voice

        embed = discord.Embed(color=0x2F3136)

        if not voice_state or not voice_state.channel:
            embed.title = "❌ Voice Channel Nisti"
            embed.description = "اول بیا توی یه ویس، بعد radio entekhab kon 😅"
            embed.set_footer(text=BOT_FOOTER)
            await interaction.response.send_message(
                embed=embed, ephemeral=True
            )
            return

        channel = voice_state.channel
        radio_name = self.values[0]
        radio_url = RADIOS[radio_name]

        vc = interaction.guild.voice_client

        if vc and vc.is_connected():
            await vc.disconnect(force=True)

        vc = await channel.connect(self_deaf=True)

        source = discord.FFmpegPCMAudio(
            radio_url, **FFMPEG_OPTIONS
        )
        vc.play(source)

        embed.title = "📻 Radio Play Shod"
        embed.description = (
            f"**{radio_name}**\n"
            f"Enjoy kon va vibe begir 🔥"
        )
        embed.set_footer(text=BOT_FOOTER)

        await interaction.response.send_message(
            embed=embed, ephemeral=True
        )


class RadioView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(RadioSelect())


class RadioBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=INTENTS,
        )

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"✅ Logged in as {self.user}")

    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if not member.guild.voice_client:
            return

        vc = member.guild.voice_client
        channel = vc.channel

        if not channel:
            return

        humans = [
            m
            for m in channel.members
            if not m.bot
        ]

        if humans:
            return

        await asyncio.sleep(10)

        if not vc.is_connected():
            return

        channel = vc.channel
        humans = [
            m
            for m in channel.members
            if not m.bot
        ]

        if not humans:
            await vc.disconnect(force=True)


bot = RadioBot()


@bot.tree.command(
    name="radio",
    description="📻 Play radio ba vibe Finglish 😎",
)
async def radio(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎶 Radio Station",
        description="Ye radio entekhab kon va hal kon ✨",
        color=0x5865F2,
    )
    embed.set_footer(text=BOT_FOOTER)

    await interaction.response.send_message(
        embed=embed,
        view=RadioView(),
        ephemeral=True,
    )


bot.run(TOKEN)
