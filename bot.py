import os
import logging
import tinify
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from mongodb.mongodb import add_user, update_user_activity, get_user_activity

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve credentials from environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
TINIFY_API_KEY = os.getenv("TINIFY_API_KEY")

# Initialize Tinify API
tinify.key = TINIFY_API_KEY

# Create a Pyrogram client
app = Client("tinify_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Log the bot startup
logger.info("Bot is starting...")

# /start command
@app.on_message(filters.command("start"))
def start(client, message: Message):
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

# Handle file uploads
@app.on_message(filters.document)
def handle_file(client, message: Message):
    user_id = message.from_user.id
    logger.info(f"Received file upload from {user_id}.")
    client.send_message(message.chat.id, "📥 Received your file! I will download and compress it now.")
    
    file_path = client.download_media(message.document.file_id)
    compress_and_send_file(client, message.chat.id, file_path, message.document.file_name, user_id)

# Handle messages with an image URL
@app.on_message(filters.text)
def handle_url(client, message: Message):
    user_id = message.from_user.id
    logger.info(f"Received image URL from {user_id}: {message.text}")
    client.send_message(message.chat.id, "📥 Received your URL! I will download and compress the image now.")
    
    compress_and_send_url(client, message.chat.id, message.text, user_id)

def compress_and_send_file(client, chat_id, file_path, original_file_name, user_id):
    try:
        source = tinify.from_file(file_path)
        base, ext = os.path.splitext(original_file_name)
        compressed_file_name = f"{base}_compressed{ext}"
        compressed_image_path = compressed_file_name
        source.to_file(compressed_image_path)

        with open(compressed_image_path, "rb") as file:
            client.send_document(chat_id=chat_id, document=file)

        compressed_size = os.path.getsize(compressed_image_path)
        update_user_activity(user_id, compressed_size)

        os.remove(compressed_image_path)
        os.remove(file_path)

        client.send_message(chat_id, "✅ Your image has been compressed and sent! You can download it now.")
        logger.info(f"Compressed image sent to {chat_id} successfully from file upload.")
        
    except Exception as e:
        client.send_message(chat_id, f"❌ An error occurred: {e}")
        logger.error(f"Error compressing file: {e}")

def compress_and_send_url(client, chat_id, image_url, user_id):
    try:
        source = tinify.from_url(image_url)
        base = image_url.split("/")[-1]
        ext = os.path.splitext(base)[-1]
        compressed_file_name = f"{base}_compressed{ext}"
        compressed_image_path = compressed_file_name
        source.to_file(compressed_image_path)

        with open(compressed_image_path, "rb") as file:
            client.send_document(chat_id=chat_id, document=file)

        compressed_size = os.path.getsize(compressed_image_path)
        update_user_activity(user_id, compressed_size)

        os.remove(compressed_image_path)

        client.send_message(chat_id, "✅ Your image has been compressed and sent! You can download it now.")
        logger.info(f"Compressed image sent to {chat_id} successfully from URL.")
        
    except tinify.errors.AccountError:
        client.send_message(chat_id, "⚠️ The Tinify API key is invalid. Please check and try again.")
        logger.error("Invalid Tinify API key.")
    except tinify.errors.ClientError:
        client.send_message(chat_id, "⚠️ There was an issue with the image URL. Please ensure it's valid.")
        logger.error("Client error while processing the image URL.")
    except Exception as e:
        client.send_message(chat_id, f"❌ An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

# Run the bot
if __name__ == "__main__":
    app.run()
    logger.info("Bot has stopped.")
