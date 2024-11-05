from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from mongodb.mongodb import add_user
import logging

logger = logging.getLogger(__name__)

def start(client: Client, message: Message):
    user_id = message.from_user.id
    add_user(user_id)
    
    welcome_text = (
        "👋 Welcome to the Image Compressor Bot!\n"
        "I can help you compress images from a URL or by uploading a file.\n"
        "Just send me an image URL or upload an image file, and I'll do the rest! 📸"
    )
    start_button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Start Compressing", url="https://t.me/your_bot_username")]]
    )
    client.send_message(message.chat.id, welcome_text, reply_markup=start_button)
    logger.info(f"Start command received from {user_id}.")
