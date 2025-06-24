# scripts/ingest_telegram.py

from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos, InputMessagesFilterDocument
import json
import os

# Replace with your credentials
api_id = '23581125'
api_hash = 'c8f632f303a3cf994a641a52ad8528a5'
phone = '+251939278100'

client = TelegramClient('ethio_session', api_id, api_hash)

async def fetch_messages(channel_username, limit=1000):
    await client.start(phone=phone)
    messages = []

    async for message in client.iter_messages(channel_username, limit=limit):
        if message.message:  # Text messages only
            msg = {
                "channel": channel_username,
                "text": message.message,
                "timestamp": str(message.date),
                "views": message.views,
                "id": message.id,
                "sender_id": message.sender_id,
                "has_media": message.media is not None,
                "image_url": None
            }

            # Download images (optional)
            if message.photo:
                path = f"data/raw/{channel_username}_{message.id}.jpg"
                await message.download_media(file=path)
                msg["image_url"] = path

            messages.append(msg)

    return messages

async def main():
    # 📌 Add at least 5 channels
    channels = ['shageronlinestore', 'addisdeals', 'ethiomall', 'mobilebazarethiopia', 'shewastore']
    all_data = []

    for ch in channels:
        msgs = await fetch_messages(ch)
        all_data.extend(msgs)

    # Save as JSON
    os.makedirs("data/raw/", exist_ok=True)
    with open("data/raw/telegram_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

with client:
    client.loop.run_until_complete(main())
