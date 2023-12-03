"""module managing connecting to the discord api"""
import logging
from time import sleep
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
        self.emoji_string = ""
        super().__init__(intents=intents)

    async def on_ready(self):
        """called when the client is ready to send and recieve messages"""
        logging.info("bot started")
        self.fetch_guilds()
        guilds = [guild async for guild in self.fetch_guilds()]
        for guild in guilds:
            self.db_conn.initialize_server(str(guild.name), "discord")
            emoji_name = self.configs.get("reset_emoji", "discord")
            for emoji in await guild.fetch_emojis():
                if emoji.name == emoji_name:
                    self.emoji_string = str(emoji)

            channels = await guild.fetch_channels()
            for channel in channels:
                if channel.name == self.configs.get("channel", "discord"):
                    count, _ = self.db_conn.get_current_count(str(guild.name))
                    msg = f"""Hello from Snowball bot.
I just restarted, your last valid count was {count}"""
                    await channel.send(msg)

    async def __check_commands(self, message: Message) -> bool:
        # TODO: Move these to a command subsystem to call functions on match.
        commands = {
            "!commands": "",
            "!help": help_string,
            "!highscore": "Your server highscore is: ",
        }

        # this has to be done outside of the dict initialzation
        commands["!commands"] = "\n".join(commands.keys())

        # Check if is shutdown command, and if so, if allowed to shutdown
        if message.content.startswith("!shutdown"):
            await self.__shutdown(message)
            return True

        # check if known command
        reply = commands.get(message.content)
        if reply is not None:
            # TODO: wrap highscore in its own function that only would get called if match.
            if reply.startswith("Your server"):
                reply = reply + str(self.db_conn.get_highscore(str(message.guild.name)))
            await message.reply(reply)
            return True
        return False

    async def on_message(self, message: Message):
        """handle new messages in the configured channel"""
        if message.channel.name != self.configs.get("channel", "discord"):
            return

        if message.author.id == self.user.id:
            return

        if await self.__check_commands(message):
            return

        # Try to get lock, if unable, mark as invalid
        if self._lock.acquire(block=False):
            count, user = self.db_conn.get_current_count(str(message.guild.name))
            this_count, countable = parse_message(message.content)
            if not countable:
                self._lock.release()
                return
            if user == str(message.author.id):
                await message.add_reaction("🎭")
                await message.channel.send("a counting so nice you did it twice?")
            else:
                if this_count == -1:
                    self.db_conn.reset_count(message.guild.name)
                    await message.add_reaction("❎")

                    await message.channel.send(
                        f"{self.emoji_string} The cycle begins anew"
                    )
                elif this_count == count + 1:
                    self.db_conn.increment_count(
                        str(message.guild.name), str(message.author.id), count + 1
                    )
                    await message.add_reaction("✅")
                else:
                    self.db_conn.reset_count(str(message.guild.name))
                    await message.add_reaction("❎")
                    await message.channel.send(
                        f"{self.emoji_string} The cycle begins anew"
                    )
            self._lock.release()
        else:
            await message.add_reaction("🌨")

    async def __shutdown(self, message: Message):
        if message.guild.name == self.configs.get("admin_guild", "discord"):
            for role in message.author.roles:
                if self.configs.get("admin_role", "discord") == role.name:
                    await message.channel.send(
                        f"{self.configs.get('name')} is shutting down"
                    )
                    sleep(2)
                    raise KeyboardInterrupt


def run(configs) -> None:
    """creates a new discord client"""
    intents = Intents.default()
    intents.message_content = True
    intents.emojis = True
    bot = DiscordClient(configs, intents=intents)
    bot.run(token=configs.get("token", "discord"))
