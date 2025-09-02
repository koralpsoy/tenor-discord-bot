import os
import random
import asyncio
import aiohttp
import discord
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TENOR_API_KEY = os.getenv("TENOR_API_KEY", "TENOR_EXAMPLE_KEY_1234567890")  # Platzhalter
TENOR_CLIENT_KEY = os.getenv("TENOR_CLIENT_KEY", "discord-reaction-bot")    # optional

if not DISCORD_TOKEN:
    raise RuntimeError("Environment-Variable DISCORD_TOKEN fehlt. Trage sie in .env ein.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Client(intents=intents)

COMMANDS: dict[str, str] = {
    "kick": "kick",
    "slap": "pokemon slap",
    "punch": "pokemon punch",
    "love": "pokemon love",
    "kiss": "pokemon kiss",
    "destroy": "pokemon destroy",
    "kamehameha": "kamehameha",
    "sad": "pokemon sad",
    "cry": "pokemon cry",
    "angry": "pokemon angry",
    "jealous": "pokemon jealous",
    "go": "lets go",
    "gg": "pokemon gg",
    "hug": "pokemon hug",
    "rich": "pokemon rich",
    "dance": "pokemon dance",
    "happy": "pokemon happy",
    "confused": "pokemon confused",
    "funny": "pokemon funny",
    "surprised": "pokemon surprised",
    "excited": "pokemon excited",
    "bored": "pokemon bored",
    "mad": "pokemon mad",
    "lol": "pokemon lol"
}

RESPONSES: dict[str, str] = {
    "kick": "{author} gibt {mentioned} einen schnellen Kick!",
    "slap": "{author} verpasst {mentioned} eine saftige Ohrfeige!",
    "punch": "{author} boxt {mentioned} mit voller Wucht!",
    "love": "{author} ist verliebt in {mentioned}!",
    "kiss": "{author} gibt {mentioned} einen süßen Kuss!",
    "destroy": "{author} zerstört {mentioned} mit purer Power!",
    "kamehameha": "{author} feuert eine Kamehameha auf {mentioned}!",
    "sad": "{author} ist wegen {mentioned} traurig…",
    "cry": "{author} weint wegen {mentioned}…",
    "angry": "{author} ist wütend auf {mentioned}!",
    "jealous": "{author} ist eifersüchtig auf {mentioned}…",
    "go": "{author} sagt {mentioned}: Go for it!",
    "gg": "{author} sagt GG zu {mentioned}!",
    "hug": "{author} umarmt {mentioned} ganz fest!",
    "rich": "{author} findet, {mentioned} ist steinreich!",
    "dance": "{author} tanzt mit {mentioned}!",
    "happy": "{author} ist glücklich mit {mentioned}!",
    "confused": "{author} ist verwirrt von {mentioned}…",
    "funny": "{author} findet {mentioned} urkomisch!",
    "surprised": "{author} ist überrascht von {mentioned}!",
    "excited": "{author} ist ganz aus dem Häuschen wegen {mentioned}!",
    "bored": "{author} ist gelangweilt von {mentioned}…",
    "mad": "{author} ist sauer auf {mentioned}!",
    "lol": "{author} lacht laut über {mentioned}!",
}

async def fetch_tenor_gif(search_term: str) -> str | None:
    base_url = "https://tenor.googleapis.com/v2/search"
    params = {
        "q": search_term,
        "key": TENOR_API_KEY,
        "client_key": TENOR_CLIENT_KEY,
        "limit": 50,
        "random": "true",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params, timeout=10) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
    except asyncio.TimeoutError:
        return None
    except aiohttp.ClientError:
        return None

    results = data.get("results") or []
    if not results:
        return None

    choice = random.choice(results)
    media = (choice.get("media_formats") or {})
    for key in ("gif", "tinygif", "nanogif"):
        url = (media.get(key) or {}).get("url")
        if url:
            return url
    return None


def build_response(command: str, author_mention: str, target_mention: str) -> str:
    template = RESPONSES.get(command)
    if not template:
        return f"{author_mention} macht etwas mit {target_mention}!"
    return template.format(author=author_mention, mentioned=target_mention)


def parse_command(content: str) -> str | None:
    content = content.strip().lower()
    if not content.startswith("?"):
        return None
    return content[1:].split()[0] if len(content) > 1 else None


@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    command = parse_command(message.content)
    if not command:
        return

    if command == "help":
        cmds = ", ".join(sorted(COMMANDS.keys()))
        await message.channel.send(
            "Verfügbare Commands: " + cmds +
            "Nutze `?command @user` oder antworte mit `?command` auf eine Nachricht."
        )
        return

    if command not in COMMANDS:
        return

    search_term = COMMANDS[command]

    target = None
    if message.reference and message.reference.message_id:
        try:
            replied = await message.channel.fetch_message(message.reference.message_id)
            if replied and replied.author:
                target = replied.author.mention
        except Exception:
            target = None

    if not target and message.mentions:
        target = message.mentions[0].mention

    if not target:
        target = message.author.mention

    response_text = build_response(command, message.author.mention, target)
    gif_url = await fetch_tenor_gif(search_term)

    if gif_url:
        embed = discord.Embed(description=response_text)
        embed.set_image(url=gif_url)
        await message.channel.send(embed=embed)
    else:
        await message.channel.send(f"{response_text}Kein GIF gefunden._")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)