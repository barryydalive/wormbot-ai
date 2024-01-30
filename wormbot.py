import discord
import openai
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set up your OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set up your Discord bot client
client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message.content,
        max_tokens=50
    )

    await message.channel.send(response.choices[0].text.strip())

# Run your bot with the Discord token
client.run(DISCORD_TOKEN)