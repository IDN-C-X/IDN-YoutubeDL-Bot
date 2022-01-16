import asyncio
import yt_dlp

from __future__ import unicode_literals
from utils.util import humanbytes

from pyrogram import Client, filters, StopPropagation
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def buttonmap(item):
    quality = item["format"]
    if "audio" in quality:
        return [
            InlineKeyboardButton(
                f"{quality} 🎵 {humanbytes(item['filesize'])}",
                callback_data=f"ytdata||audio||{item['format_id']}||{item['yturl']}",
            )
        ]
    else:
        return [
            InlineKeyboardButton(
                f"{quality} 📹 {humanbytes(item['filesize'])}",
                callback_data=f"ytdata||video||{item['format_id']}||{item['yturl']}",
            )
        ]


def create_buttons(quailitylist):
    return map(buttonmap, quailitylist)


def extractYt(yturl):
    ydl = yt_dlp.YoutubeDL()
    with ydl:
        r = ydl.extract_info(yturl, download=False)
        qualityList = [
            {
                "format": format["format"],
                "filesize": format["filesize"],
                "format_id": format["format_id"],
                "yturl": yturl,
            }
            for format in r["formats"]
            if "dash" not in str(format["format"]).lower()
        ]

        return r["title"], r["thumbnail"], qualityList


async def downloadvideocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print(e_response)
    return t_response.split("Merging formats into")[-1].split('"')[1]


async def downloadaudiocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print("Download error:", e_response)

    return (
        t_response.split("Destination")[-1].split("Deleting")[0].split(":")[-1].strip()
    )
