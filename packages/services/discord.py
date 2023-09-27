"""module managing connecting to the discord api"""
import logging
from discord import Client, Message, Intents, PartialEmoji
from packages.counting.counting import check_next_count, reset_count
from packages.config.config import services

class DiscordClient(Client):
    """the client for the discord api"""
    async def on_ready(self):
        """called when the client is ready to send and recieve messages"""
        logging.info("bot started")
    async def on_message(self, message:Message):
        """handle new messages in the configured channel"""
        if message.channel != services["discord"]["channel"]:
            return

        if message.author == self.user:
            return

        if check_next_count(message.content):
            await message.add_reaction(PartialEmoji(name='✅'))
        else:
            reset_count()
            await message.channel.send(
                "That wasn't the correct count, the cycle begins anew.", mention_author=True)

def run()->None:
    """creates a new discord client"""
    bot = DiscordClient(
        intents=Intents(
            value=int(services["discord"]["permissions_integer"])))
    bot.run(token=services["discord"]["token"])
