import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["image_compressor_bot"]
users_collection = db["users"]

def add_user(user_id):
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({
            "user_id": user_id,
            "files_compressed": 0,
            "total_data_compressed": 0
        })

def update_user_activity(user_id, compressed_size):
    users_collection.update_one(
        {"user_id": user_id},
        {
            "$inc": {
                "files_compressed": 1,
                "total_data_compressed": compressed_size
            }
        }
    )

def get_user_activity(user_id):
    return users_collection.find_one({"user_id": user_id}, {"_id": 0, "files_compressed": 1, "total_data_compressed": 1})

def user_exists(user_id):
    return users_collection.find_one({"user_id": user_id}) is not None
