"""module managing connecting to the discord api"""

import logging
from time import sleep
from multiprocessing import Lock
from discord import Client, Intents, Message
from packages.config.database import Database
from packages.counting.counting import parse_message
from packages.templates.help import help_string, status_string
from packages.templates.reset import reset_string


class DiscordClient(Client):
    """the client for the discord api"""

    def __init__(self, configs, intents: Intents):
        self._lock = Lock()
        self.configs = configs
        self.db_conn = Database(configs.get("database"))
        self.emoji_string = ""
        self.commands = {
            "!commands": self.__cmd_commands,
            "!help": self.__cmd_help,
            "!highscore": self.__cmd_highscore,
            "!status": self.__cmd_status,
        }
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
        # check if known command
        cmd_func = self.commands.get(message.content)
        if cmd_func is not None:
            await message.reply(cmd_func(str(message.guild.name)))
            return True
        return False

    def __cmd_status(self, guild: str) -> str:
        """method for getting !status response"""
        count, _ = self.db_conn.get_current_count(guild)
        highscore = self.db_conn.get_highscore(guild)
        return status_string.format(count=count, highscore=highscore)

    def __cmd_highscore(self, guild: str) -> str:
        """method for getting !highscore response"""
        highscore = self.db_conn.get_highscore(guild)
        return f"Your server highscore is {highscore}"

    def __cmd_help(self, guild: str) -> str:
        """method for getting !help response"""
        return help_string

    def __cmd_commands(self, guild: str) -> str:
        """method for getting !commands response"""
        return "\n".join(self.commands.keys())

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
            try:
                count, user = self.db_conn.get_current_count(str(message.guild.name))
                this_count, countable = parse_message(message.content)
                if not countable:
                    return
                if user == str(message.author.id):
                    await message.add_reaction("🎭")
                    await message.channel.send("a counting so nice you did it twice?")
                else:
                    if this_count == -1:
                        self.db_conn.reset_count(message.guild.name)
                        await message.add_reaction("❎")
                        await message.channel.send(
                            reset_string.format(
                                count=count + 1,
                                this_count=this_count,
                                emoji_string=self.emoji_string,
                            )
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
                            reset_string.format(
                                count=count + 1,
                                this_count=this_count,
                                emoji_string=self.emoji_string,
                            )
                        )
            except Exception as e:
                logging.error(e)
            finally:
                sleep(float(self.configs.get("mutex_hold", "discord")))
                self._lock.release()
        else:
            await message.add_reaction("🌨")


def run(configs) -> None:
    """creates a new discord client"""
    intents = Intents.default()
    intents.message_content = True
    intents.emojis = True
    bot = DiscordClient(configs, intents=intents)
    bot.run(token=configs.get("token", "discord"))
