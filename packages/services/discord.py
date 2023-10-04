"""module managing connecting to the discord api"""
import logging
from multiprocessing import Lock
from discord import Client, Intents, Message
from packages.config.database import Database
from packages.counting.counting import parse_message
from packages.templates.help import help_string 

class DiscordClient(Client):
    """the client for the discord api"""

    def __init__(self, configs, intents: Intents):
        self._lock = Lock()
        self.configs = configs
        self.db_conn = Database(configs.get("database"))
        super().__init__(intents=intents)

    async def on_ready(self):
        """called when the client is ready to send and recieve messages"""
        logging.info("bot started")
        self.fetch_guilds()
        guilds = [guild async for guild in self.fetch_guilds()]
        for guild in guilds:
            self.db_conn.initialize_server(str(guild.id), "discord")
            channels = await guild.fetch_channels()
            for channel in channels:
                if channel.name == self.configs.get("channel", "discord"):
                    count, _ = self.db_conn.get_current_count(str(guild.id))
                    msg = f"""Hello from Snowball bot.
I just restarted, your last valid count was {count}"""
                    await channel.send(msg)

    async def __check_commands(self, message:Message)->bool:
        commands = {
            "!commands": "",
            "!help":  help_string,
            "!highscore":  "high score is not implemented yet"
        }
        # this has to be done outside of the dict initialzation
        commands["!commands"] = "\n".join(commands.keys())
       
        reply = commands.get(message.content)
        if reply is not None:
            await message.reply(reply)
            return True
        return False

    async def on_message(self, message:Message):
        """handle new messages in the configured channel"""
        if message.channel.name != self.configs.get("channel", "discord"):
            return

        if message.author.id == self.user.id:
            return
        
        if await self.__check_commands(message):
            return

        # Try to get lock, if unable, mark as invalid
        if self._lock.acquire(block=False):
            count, user = self.db_conn.get_current_count(str(message.guild.id))
            this_count, countable = parse_message(message.content)
            if not countable:
                self._lock.release()
                return
            if user == str(message.author.id):
                await message.add_reaction('🎭')
                await message.channel.send("a counting so nice you did it twice?")
            else:
                if this_count == -1:
                    self.db_conn.reset_count(str(message.guild.id))
                    await message.add_reaction('❎')
                    await message.channel.send('the cycle begins anew')
                elif this_count == count + 1:
                    self.db_conn.increment_count(
                        str(message.guild.id),
                        str(message.author.id),
                        count+1)
                    await message.add_reaction('✅')
                else:
                    self.db_conn.reset_count(str(message.guild.id))
                    await message.add_reaction('❎')
                    await message.channel.send('the cycle begins anew')         
            self._lock.release()
        else:
            await message.add_reaction('🌨')

def run(configs)->None:
    """creates a new discord client"""
    intents = Intents.default()
    intents.message_content = True
    intents.emojis = True
    bot = DiscordClient(configs, intents=intents)
    bot.run(token=configs.get("token", "discord"))
