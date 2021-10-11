from datetime import datetime, timedelta

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from helper.ytdlfunc import extractYt, create_buttons
from config import youtube_next_fetch
from bot import user_time


ytregex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"


@Client.on_message(filters.regex(ytregex))
async def ytdl(_, message):
    userLastDownloadTime = user_time.get(message.chat.id)
    try:
        if userLastDownloadTime > datetime.now():
            wait_time = round(
                (userLastDownloadTime - datetime.now()).total_seconds() / 60, 2
            )
            await message.reply_text(f"`Wait {wait_time} Minutes before next Request`")
            return
    except:
        pass

    url = message.text.strip()
    await message.reply_chat_action("typing")
    try:
        title, thumbnail_url, formats = extractYt(url)

        now = datetime.now()
        user_time[message.chat.id] = now + timedelta(minutes=youtube_next_fetch)

    except Exception:
        await message.reply_text(
            "`Failed To Fetch Youtube Data... Error Vro \nPossible Youtube Blocked server ip \n#error`"
        )
        return
    buttons = InlineKeyboardMarkup(list(create_buttons(formats)))
    sentm = await message.reply_text("Processing Youtube Url 🔎. . .")
    try:
        await message.reply_photo(thumbnail_url, caption=title, reply_markup=buttons)
        await sentm.delete()
    except Exception as e:
        try:
            thumbnail_url = "https://telegra.ph/file/fe64e5b1ebecba97ca1dd.png"
            await message.reply_photo(
                thumbnail_url, caption=title, reply_markup=buttons
            )
        except Exception as e:
            await sentm.edit(f"<code>{e}</code> #Error")
