"""module managing connecting to the discord api"""
import logging
from discord import Client, Intents, Message
from packages.config.config import services

class DiscordClient(Client):
    """the client for the discord api"""
    async def on_ready(self):
        """called when the client is ready to send and recieve messages"""
        logging.info("bot started")
        for channel in self.get_all_channels():
            if channel.name == services["discord"]["channel"]:
                await channel.send(
                    "Hello from the Snowball bot, I just restarted and your last valid count was #")

    async def on_message(self, message:Message):
        """handle new messages in the configured channel"""
        if message.channel.name != services["discord"]["channel"]:
            return

        if message.author.id == self.user.id:
            return
    
        await message.channel.send(
            "hello! I will respond to numbers in this channel when that feature has been added")

def run()->None:
    """creates a new discord client"""
    intents = Intents.default()
    intents.message_content = True
    intents.emojis = True
    bot = DiscordClient(intents=intents)
    bot.run(token=services["discord"]["token"])
