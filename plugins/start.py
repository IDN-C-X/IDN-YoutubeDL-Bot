from pyrogram import Client, filters, StopPropagation
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command(["start"]), group=-2)
async def start(client, message):
    # return
    joinButton = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Channel Update", url="https://t.me/IDNCoder")],
            [InlineKeyboardButton("Group Support", url="https://t.me/IDNCoderX")],
        ]
    )
    welcomed = f"Hey <b>{message.from_user.first_name}</b>\n/help for More info\n\n<b>Powered By</b> @IDNCoder"
    await message.reply_text(welcomed, reply_markup=joinButton)
    raise StopPropagation
