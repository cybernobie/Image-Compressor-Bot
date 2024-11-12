import os
from pyrogram import Client, filters
from pyrogram.types import Message
from responses.compress_and_send_file import compress_and_send_file
from utils import get_user_data, set_user_data  # Import the functions
import logging

logger = logging.getLogger(__name__)

def handle_file(client: Client, message: Message):
    user_id = message.from_user.id
    file_name = message.document.file_name
    file_extension = os.path.splitext(file_name)[-1].lower()
    
    if file_extension not in [".webp", ".jpeg", ".jpg", ".png"]:
        client.send_message(message.chat.id, "⚠️ I only support WebP, JPEG, and PNG file formats. Please send a supported image file.")
        return
    
    selected_format = get_user_data(user_id, "selected_format")
    if selected_format:
        client.send_message(message.chat.id, "📥 Received your file! I will download and convert it now.")
        file_path = client.download_media(message.document.file_id)
        compress_and_send_file(client, message.chat.id, file_path, file_name, user_id, selected_format)
        set_user_data(user_id, "selected_format", None)
    else:
        client.send_message(message.chat.id, "📥 Received your file! I will download and compress it now.")
        file_path = client.download_media(message.document.file_id)
        compress_and_send_file(client, message.chat.id, file_path, file_name, user_id)
