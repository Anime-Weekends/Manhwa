import os
import random
import shutil
import asyncio
from time import time
from loguru import logger

from pyrogram import Client, __version__ as pyro_version
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import utils as pyroutils


class Vars:
    API_ID = int(os.environ.get("API_ID", "28744454"))
    API_HASH = os.environ.get("API_HASH", "debd37cef0ad1a1ce45d0be8e8c3c5e7")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8130872612:AAEzw5W_dHbdW1EeUVH3L2vNAIVwx-K7fbc")

    plugins = dict(root="TG")

    LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "-1002693061800")
    UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "-1002410513772")
    DB_URL = os.environ.get(
        "DB_URL",
        "mongodb+srv://JeffyBackUp:JeffyBackUp@cluster0.hgbjdhr.mongodb.net/?retryWrites=true&w=majority",
    )

    PORT = int(os.environ.get("PORT", "8080"))
    ADMINS = [6266529037, 5548954124]

    IS_PRIVATE = os.environ.get("IS_PRIVATE", None)  # True or None
    CONSTANT_DUMP_CHANNEL = os.environ.get("CONSTANT_DUMP_CHANNEL", "True")
    WEBS_HOST = os.environ.get("WEBS_HOST", "True").lower() == "true"

    DB_NAME = "Manhwadb"
    PING = time()

    FORCE_SUB_CHANNEL = os.environ.get("FORCE_SUB_CHANNEL", "EmitingStars_Botz")
    SHORTENER = os.environ.get("SHORTENER", "True")
    SHORTENER_API = os.environ.get("SHORTENER_API", "https://shortxlinks.com/api?api=bea2b83467261cec3b811d76a9bd84533234219a&url={}")
    DURATION = int(os.environ.get("DURATION", "20"))  # hours

    PICS = (
        "https://telegra.ph/HgBotz-08-02",
    )


# Set Pyrogram's minimum accepted chat/channel IDs (for extreme ranges)
pyroutils.MIN_CHAT_ID = -99999999999999
pyroutils.MIN_CHANNEL_ID = -100999999999999


class ManhwaBot(Client, Vars):
    def __init__(self):
        super().__init__(
            "ManhwaBot",
            api_id=self.API_ID,
            api_hash=self.API_HASH,
            bot_token=self.BOT_TOKEN,
            plugins=self.plugins,
            workers=50,
        )
        self.logger = logger
        self.__version__ = pyro_version

    async def start(self):
        await super().start()

        async def run_flask():
            cmds = ("gunicorn", "app:app")
            process = await asyncio.create_subprocess_exec(
                *cmds,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                logger.error(f"Flask app failed to start: {stderr.decode()}")
            else:
                logger.info("Web app started successfully")

        usr_bot_me = await self.get_me()

        # Restart message
        if os.path.exists("restart_msg.txt"):
            with open("restart_msg.txt", "r") as f:
                chat_id, message_id = f.read().strip().split(":")
            try:
                await self.edit_message_text(int(chat_id), int(message_id), "<code>Restarted Successfully</code>")
            except Exception as e:
                logger.exception(e)
            os.remove("restart_msg.txt")

        # Clean up process folder
        if os.path.exists("Process"):
            shutil.rmtree("Process")

        # Banner log
        self.logger.info(r"""
 .    ▼￣＞-―-＜￣▼
　　Ｙ　            Ｙ
  /\   / 　 ●    o  ●）
＼  ｜　 つ　    ヽ
        """)

        self.username = usr_bot_me.username
        self.logger.info("Made by https://t.me/EmitingStars_Botz")
        self.logger.info(f"Manhwa Bot Started as {usr_bot_me.first_name} | @{usr_bot_me.username}")

        # Launch Flask app if enabled
        if self.WEBS_HOST:
            await run_flask()

        # Send online status update
        msg_text = """<blockquote><b>Sʏsᴛᴇᴍs ᴏɴʟɪɴᴇ. ʀᴇᴀᴅʏ ᴛᴏ ʀᴜᴍʙʟᴇ.
sʟᴇᴇᴘ ᴍᴏᴅᴇ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ. ɴᴇᴜʀᴀʟ ᴄᴏʀᴇs ᴀᴛ 100%. ғᴇᴇᴅ ᴍᴇ ᴛᴀsᴋs, ᴀɴᴅ ᴡᴀᴛᴄʜ ᴍᴀɢɪᴄ ʜᴀᴘᴘᴇɴ. ʟᴇᴛ’s ɢᴇᴛ ᴅᴀɴɢᴇʀᴏᴜs.</b></blockquote>"""

        photo = random.choice(self.PICS)

        buttons = [
            [
                InlineKeyboardButton("Sᴛᴀʀᴛ ɴᴏᴡ", url=f"https://t.me/{usr_bot_me.username}?start=start"),
                InlineKeyboardButton("Cʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz"),
            ]
        ]

        try:
            await self.send_photo(
                self.UPDATE_CHANNEL,
                photo=photo,
                caption=msg_text,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        except Exception as e:
            logger.warning(f"Failed to send update message: {e}")

    async def stop(self, *args):
        await super().stop()
        self.logger.info("Manhwa Bot Stopped")


Bot = ManhwaBot()
