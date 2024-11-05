from pyrogram import Client, filters
from pyrogram.types import Message
from responses.compress_and_send_url import compress_and_send_url
import logging

logger = logging.getLogger(__name__)

def handle_url(client: Client, message: Message):
    user_id = message.from_user.id
    logger.info(f"Received image URL from {user_id}: {message.text}")
    client.send_message(message.chat.id, "📥 Received your URL! I will download and compress the image now.")
    
    compress_and_send_url(client, message.chat.id, message.text, user_id)
