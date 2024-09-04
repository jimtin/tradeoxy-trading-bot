import discord
import os


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


# Function to get the bot ready for Discord interaction
@client.event
async def on_ready():
    """
    Function to send a message to the channel on trading bot start up
    """
    # Print a message to the console
    print(f'TradeOxy Discord Bot up and running. We have logged in as {client.user}')
    
    
@client.event
async def on_message(message):
    """
    Discord message listener
    """
    # Don't respond to ourselves
    if message.author == client.user:
        return False
    
    # Check if the message starts with TradeOxy Alert:
    if message.content.startswith('TradeOxy Alert:'):
        # Get the message content
        msg = message.content
        print(msg)
        return True


def start_discord_bot(token):
    """
    Function to start the Discord bot
    """
    # Start the Discord bot
    client.run(token)
    return True
    
