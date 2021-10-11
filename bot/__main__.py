import config

from pyrogram import Client


DOWNLOAD_LOCATION = "./Downloads"
BOT_TOKEN = config.BOT_TOKEN

APP_ID = config.APP_ID
API_HASH = config.API_HASH


plugins = dict(
    root="plugins",
)

Client(
    "IDNCoder",
    bot_token=BOT_TOKEN,
    api_id=APP_ID,
    api_hash=API_HASH,
    plugins=plugins,
    workers=100,
).run()
