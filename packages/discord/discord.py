from discord import Client, Intents, Message, PartialEmoji
from packages.counting.counting import check_next_count, reset_count
from packages.config.config import services
import logging

class DiscordClient(Client):
    async def on_ready(self):
        logging.info("bot started")
    
    async def on_message(self, message:Message):
        """handle new messages in the configured channel"""
        if message.channel != services["discord"]["channel"]:
            return

        if message.author == self.user:
            return

        if check_next_count(message):
            message.add_reaction(PartialEmoji('✅'))
        else:
            reset_count()
            message.channel.send("That wasn't the correct count, the cycle begins anew.", mention_author=True)
        

