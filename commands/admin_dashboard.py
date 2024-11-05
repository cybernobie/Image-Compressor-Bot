from pyrogram import Client, filters
from pyrogram.types import Message
from mongodb.mongodb import get_stats
import logging

logger = logging.getLogger(__name__)

def admin_dashboard(client: Client, message: Message):
    if message.from_user.id != int(os.getenv("ADMIN_ID")):
        client.send_message(message.chat.id, "⚠️ You are not authorized to access the admin dashboard.")
        return

    stats = get_stats()
    dashboard_text = (
        f"📊 Admin Dashboard:\n"
        f"Total Users: {stats['total_users']}\n"
        f"Total Photos Compressed: {stats['total_files_compressed']}\n"
        f"Total Data Compressed: {stats['total_data_compressed']} bytes\n"
        f"Photos Compressed Today: {stats['today_files_compressed']}\n"
        f"Data Compressed Today: {stats['today_data_compressed']} bytes\n"
    )
    client.send_message(message.chat.id, dashboard_text)
    logger.info(f"Admin dashboard accessed by {message.from_user.id}.")
