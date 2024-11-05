import os
import logging
import tinify
from pyrogram import Client, filters
from pyrogram.handlers import CallbackQueryHandler  # Import CallbackQueryHandler
from dotenv import load_dotenv
from commands.start import start
from commands.about import about
from commands.handle_file import handle_file
from commands.handle_url import handle_url
from commands.admin_dashboard import admin_dashboard
from commands.usage_stats import usage_stats
from commands.convert_file_type import convert_file_type, handle_conversion_selection

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

# Temporary user data storage
user_data = {}

def set_user_data(user_id, key, value):
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id][key] = value

def get_user_data(user_id, key):
    return user_data.get(user_id, {}).get(key)

# Log the bot startup
logger.info("Bot is starting...")

# Register command handlers
app.add_handler(filters.command("start"), start)
app.add_handler(filters.command("about"), about)
app.add_handler(filters.command("admin"), admin_dashboard)
app.add_handler(filters.command("stats"), usage_stats)
app.add_handler(filters.command("convert"), convert_file_type)
app.add_handler(filters.document, handle_file)
app.add_handler(filters.text & (filters.command != True), handle_url)  # Corrected line for handling URLs
app.add_handler(CallbackQueryHandler(handle_conversion_selection))  # Corrected line for callback queries

# Run the bot
if __name__ == "__main__":
    app.run()
    logger.info("Bot has stopped.")
