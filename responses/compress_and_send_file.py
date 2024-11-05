import os
import tinify
from mongodb.mongodb import update_user_activity
import logging

logger = logging.getLogger(__name__)

def compress_and_send_file(client, chat_id, file_path, original_file_name, user_id, target_format=None):
    try:
        client.send_message(chat_id, "⏳ Compressing your image, please wait...")
        source = tinify.from_file(file_path)
        base, ext = os.path.splitext(original_file_name)
        if target_format:
            ext = f".{target_format}"
        compressed_file_name = f"{base}_compressed{ext}"
        compressed_image_path = compressed_file_name
        source.to_file(compressed_image_path)

        with open(compressed_image_path, "rb") as file:
            client.send_document(chat_id=chat_id, document=file)

        original_size = os.path.getsize(file_path)
        compressed_size = os.path.getsize(compressed_image_path)
        compression_ratio = round((original_size - compressed_size) / original_size * 100, 2)
        update_user_activity(user_id, compressed_size)

        os.remove(compressed_image_path)
        os.remove(file_path)

        client.send_message(chat_id, f"✅ Your image has been compressed and sent! Compression ratio: {compression_ratio}%")
        logger.info(f"Compressed image sent to {chat_id} successfully from file upload.")
        
    except tinify.errors.AccountError:
        client.send_message(chat_id, "⚠️ The Tinify API key is invalid. Please check and try again.")
        logger.error("Invalid Tinify API key.")
    except tinify.errors.ClientError:
        client.send_message(chat_id, "⚠️ There was an issue with the image. Please ensure it's valid.")
        logger.error("Client error while processing the image.")
    except Exception as e:
        client.send_message(chat_id, f"❌ An error occurred: {e}")
        logger.error(f"Error compressing file: {e}")

def compress_and_send_url(client, chat_id, image_url, user_id):
    try:
        client.send_message(chat_id, "⏳ Compressing your image, please wait...")
        source = tinify.from_url(image_url)
        base = image_url.split("/")[-1]
        ext = os.path.splitext(base)[-1]
        compressed_file_name = f"{base}_compressed{ext}"
        compressed_image_path = compressed_file_name
        source.to_file(compressed_image_path)

        with open(compressed_image_path, "rb") as file:
            client.send_document(chat_id=chat_id, document=file)

        original_size = os.path.getsize(compressed_image_path)
        compressed_size = os.path.getsize(compressed_image_path)
        compression_ratio = round((original_size - compressed_size) / original_size * 100, 2)
        update_user_activity(user_id, compressed_size)

        os.remove(compressed_image_path)

        client.send_message(chat_id, f"✅ Your image has been compressed and sent! Compression ratio: {compression_ratio}%")
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
