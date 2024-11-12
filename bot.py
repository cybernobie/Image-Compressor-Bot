import os
import logging
import tinify
from pyrogram import Client, filters
from pyrogram.handlers import CallbackQueryHandler
from dotenv import load_dotenv
from commands.start import start
from commands.about import about
from commands.handle_file import handle_file
from commands.handle_url import handle_url
from commands.admin_dashboard import admin_dashboard
from commands.usage_stats import usage_stats
from commands.convert_file_type import convert_file_type, handle_conversion_selection
from utils import get_user_data, set_user_data  # Import the functions

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

# Register command handlers
@app.on_message(filters.command("start"))
def start_handler(client, message):
    start(client, message)

@app.on_message(filters.command("about"))
def about_handler(client, message):
    about(client, message)

@app.on_message(filters.command("admin"))
def admin_handler(client, message):
    admin_dashboard(client, message)

@app.on_message(filters.command("stats"))
def stats_handler(client, message):
    usage_stats(client, message)

@app.on_message(filters.command("convert"))
def convert_handler(client, message):
    convert_file_type(client, message)

@app.on_message(filters.document)
def document_handler(client, message):
    handle_file(client, message)

@app.on_message(filters.text & ~filters.command(["start", "about", "admin", "stats", "convert"]))
def text_handler(client, message):
    handle_url(client, message)

@app.on_callback_query()
def callback_query_handler(client, callback_query):
    handle_conversion_selection(client, callback_query)

# Run the bot
if __name__ == "__main__":
    app.run()
    logger.info("Bot has stopped.")
