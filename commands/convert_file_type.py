from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from mongodb.mongodb import update_user_activity
from utils import get_user_data, set_user_data  # Import the functions
import logging

logger = logging.getLogger(__name__)

conversion_options = ["webp", "jpeg", "png"]

def convert_file_type(client: Client, message: Message):
    user_id = message.from_user.id
    conversion_text = "Please select the format you want to convert your image to:"
    buttons = [
        [InlineKeyboardButton(option.upper(), callback_data=f"convert_{option}") for option in conversion_options]
    ]
    client.send_message(message.chat.id, conversion_text, reply_markup=InlineKeyboardMarkup(buttons))
    logger.info(f"File type conversion requested by {user_id}.")

def handle_conversion_selection(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    selected_format = callback_query.data.split("_")[1]
    client.send_message(callback_query.message.chat.id, f"You have selected {selected_format.upper()}. Please send the image you want to convert.")
    set_user_data(user_id, "selected_format", selected_format)
    callback_query.answer()
    logger.info(f"User {user_id} selected {selected_format} for conversion.")
