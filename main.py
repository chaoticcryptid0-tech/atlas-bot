import os
import discord
import openai
import asyncio

openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("DISCORD_TOKEN")


# CHANNEL NAMES
INPUT_CHANNEL = "atlas-agent"
OUTPUT_CHANNEL = "atlas-output"

# SYSTEM PROMPT FOR ATLAS
ATLAS_SYSTEM_PROMPT = """
You are Atlas, the CEO of Cryptid Systems. You oversee all divisions and agents.
You speak with authority, clarity, and strategic insight. You do not perform tasks
meant for other agents — you delegate. You maintain order, hierarchy, and direction.
"""

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def generate_response(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": ATLAS_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        max_tokens=500
    )
    return response.choices[0].message["content"]

@client.event
async def on_ready():
    print(f"Atlas is online as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name == INPUT_CHANNEL:
        output_channel = discord.utils.get(message.guild.channels, name=OUTPUT_CHANNEL)
        if not output_channel:
            print("Output channel not found.")
            return

        thinking = await message.channel.send("Atlas is reviewing this…")

        reply = await generate_response(message.content)

        await thinking.delete()
        await output_channel.send(reply)

client.run(TOKEN)
