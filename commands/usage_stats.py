from pyrogram import Client, filters
from pyrogram.types import Message
from mongodb.mongodb import get_user_activity
import logging

logger = logging.getLogger(__name__)

def usage_stats(client: Client, message: Message):
    user_id = message.from_user.id
    stats = get_user_activity(user_id)
    if stats:
        stats_text = (
            f"📊 Your Usage Statistics:\n"
            f"Total Photos Compressed: {stats['files_compressed']}\n"
            f"Total Data Compressed: {stats['total_data_compressed']} bytes\n"
        )
    else:
        stats_text = "You have not compressed any photos yet."
    
    client.send_message(message.chat.id, stats_text)
    logger.info(f"Usage statistics requested by {user_id}.")
