"""module managing connecting to the discord api"""

import logging
from time import sleep
from multiprocessing import Lock
from multiprocessing.pool import ThreadPool as Pool
from datetime import datetime as dt

from functools import reduce
from dateutil import parser as dtparser
from dateutil import relativedelta as rtd
from discord import Client, Intents, Message, DMChannel
from packages.config.database import Database
from packages.counting.counting import parse_message
from packages.templates.help import HELP_STRING, STATUS_STRING
from packages.templates.reset import RESET_STRING
from packages.templates.stats import success, struggle
from packages.counting.stats import process_message, coalesce, OUTPUT_KEYS


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
        return STATUS_STRING.format(count=count, highscore=highscore)

    def __cmd_highscore(self, guild: str) -> str:
        """method for getting !highscore response"""
        highscore = self.db_conn.get_highscore(guild)
        return f"Your server highscore is {highscore}"

    def __cmd_help(self, _: str) -> str:
        """method for getting !help response"""
        return HELP_STRING

    def __cmd_commands(self, _: str) -> str:
        """method for getting !commands response"""
        return "\n".join(self.commands.keys())

    async def __cmd_recap(self, trigger: Message):
        start = dtparser.parse(f"{(dt.now() - rtd.relativedelta(years=1)).year}-01-01")
        channel = trigger.channel

        pool = Pool(5)

        messages = [
            m
            async for m in channel.history(after=start)
            if m.author.id == trigger.author.id
        ]
        logging.info(
            "Pulled %d messages from channel history for %s",
            len(messages),
            trigger.author.name,
        )

        data = pool.map(process_message, messages)
        output = reduce(coalesce, data, {f"{k}-s": 0 for k in OUTPUT_KEYS})

        if output["success-s"] > output["failure-s"]:
            msg_out = success(start.year, output)
        else:
            msg_out = struggle(start.year, output)

        await trigger.author.send(msg_out)

    async def on_message(self, message: Message):
        """handle new messages in the configured channel"""
        if isinstance(message.channel, DMChannel):
            return

        if message.channel.name != self.configs.get("channel", "discord"):
            return

        if message.author.id == self.user.id:
            return

        if await self.__check_commands(message):
            return

        if message.content == "!recap":
            await self.__cmd_recap(message)
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
                            RESET_STRING.format(
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
                        cycle_time = self.db_conn.get_current_cycle_time(
                            str(message.guild.name)
                        )
                        self.db_conn.reset_count(str(message.guild.name))
                        await message.add_reaction("❎")
                        await message.channel.send(
                            RESET_STRING.format(
                                count=count + 1,
                                this_count=this_count,
                                emoji_string=self.emoji_string,
                                cycle_time_string=cycle_time,
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
