import discord
from discord import app_commands
import time
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
# wormbot users dict names -> id
Ujers = {
    "jlim": '145714500014833664',
    "ben": '186335071316213760',
    "alan": '140688756100300800',
    "ivan": '133805493603794944',
    "barry": '128374386943066112',
    "wyan": '163476014503034880',
    "davey": '127536847722250240',
    "jonkim": '127526148002414592',
    "jeff": '129094490614005761',
    "zach": '449418420572651521',
    "alan T": '336356690876170264'
}

def estimate_tokens(input_text, average_token_length=4):
    """
    Estimate the number of tokens based on the length of the input text
    and the average token length.

    Args:
        input_text (str): The input text to be processed.
        average_token_length (int, optional): The average length of a token.
            Defaults to 4 for GPT models.

    Returns:
        int: The estimated number of tokens.
    """
    # Calculate the length of the input text
    input_length = len(input_text)

    # Estimate the number of tokens
    estimated_tokens = input_length / average_token_length

    # Round up to the nearest integer
    estimated_tokens = int(estimated_tokens + 0.5)

    return estimated_tokens

user_token_usage = {}
token_limit = 100000

def canUserRequest(user_id, input_text):

    # if user is not in ujers reject
    if(user_id not in Ujers.values()):
        print('who are you', user_id)
        return False
    if(user_id not in user_token_usage):
        user_token_usage[user_id] = (0, time.time())
    # if 24 hours passed since timestamp reset token count and time
    if time.time() - user_token_usage[user_id][1] >= 24 * 3600:
        user_token_usage[user_id] = (0, time.time())
    
    estimated_tokens = estimate_tokens(input_text)

    if user_token_usage[user_id][0] + estimated_tokens > token_limit:
        print('limit reached, tokens remaining: ', token_limit - user_token_usage[user_id][0])
        return False
    
    user_token_usage[user_id] = (user_token_usage[user_id][0] + estimated_tokens, user_token_usage[user_id][1])

    return True

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPEN_AI_TOKEN')

# Set up your Discord bot client with intents
intents = discord.Intents.default()
intents.message_content = True


discordClient = discord.Client(intents=intents)
tree = app_commands.CommandTree(discordClient)

# Set up OpenAIClient
# print(os.getenv('OPENAI_API_KEY'))

openAIClient = AsyncOpenAI(api_key=OPENAI_API_KEY)

@discordClient.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {discordClient.user}')

# @discordClient.event
@tree.command(
    name='worm_ai',
    description="ask Wormbot AI"
)
async def askWormbot(interaction, prompt:str):
    
    print(interaction.user, prompt)
    if interaction.user == discordClient.user:
        return
    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
        # response = openai.Completion.create(
        #     model="gpt-3.5-turbo",
        #     prompt=prompt,
        #     max_tokens=100
        # )

    print('user: ', interaction.user.id, Ujers.values())
    if(canUserRequest(str(interaction.user.id), prompt)):
        await interaction.response.send_message('asking the Great Worm')
        completion = await openAIClient.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"system", "content":"you are wormbot and you respond to the best of your ability 69 percent of the time"},{"role": "user", "content": prompt}], max_tokens=150)

        await interaction.edit_original_response(content=f'**Prompt: {prompt}** \n\n {completion.choices[0].message.content}')

    else:
        await interaction.response.send_message("You have run out of credits, venmo Barry $100 to increase your daily credit limit")
        
    print(prompt)

# Run your bot with the Discord token
discordClient.run(DISCORD_TOKEN)