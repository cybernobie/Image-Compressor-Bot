from pyrogram import Client, filters
from pyrogram.types import Message
from mongodb.mongodb import get_stats
import logging

logger = logging.getLogger(__name__)

def about(client: Client, message: Message):
    stats = get_stats()
    about_text = (
        f"📊 Bot Statistics:\n"
        f"Total Users: {stats['total_users']}\n"
        f"Total Photos Compressed: {stats['total_files_compressed']}\n"
        f"Total Data Compressed: {stats['total_data_compressed']} bytes\n"
        f"Photos Compressed Today: {stats['today_files_compressed']}\n"
        f"Data Compressed Today: {stats['today_data_compressed']} bytes\n"
    )
    client.send_message(message.chat.id, about_text)
    logger.info(f"About command received from {message.from_user.id}.")
