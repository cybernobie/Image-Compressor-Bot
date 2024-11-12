import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Retrieve MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["image_compressor_bot"]
users_collection = db["users"]
stats_collection = db["stats"]

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
    stats_collection.update_one(
        {"date": datetime.utcnow().date().isoformat()},
        {
            "$inc": {
                "total_files_compressed": 1,
                "total_data_compressed": compressed_size
            }
        },
        upsert=True
    )

def get_user_activity(user_id):
    return users_collection.find_one({"user_id": user_id}, {"_id": 0, "files_compressed": 1, "total_data_compressed": 1})

def user_exists(user_id):
    return users_collection.find_one({"user_id": user_id}) is not None

def get_stats():
    total_users = users_collection.count_documents({})
    total_files_compressed = list(stats_collection.aggregate([{"$group": {"_id": None, "total": {"$sum": "$total_files_compressed"}}}]))
    total_data_compressed = list(stats_collection.aggregate([{"$group": {"_id": None, "total": {"$sum": "$total_data_compressed"}}}]))
    today_stats = stats_collection.find_one({"date": datetime.utcnow().date().isoformat()})
    return {
        "total_users": total_users,
        "total_files_compressed": total_files_compressed[0]["total"] if total_files_compressed else 0,
        "total_data_compressed": total_data_compressed[0]["total"] if total_data_compressed else 0,
        "today_files_compressed": today_stats.get("total_files_compressed", 0) if today_stats else 0,
        "today_data_compressed": today_stats.get("total_data_compressed", 0) if today_stats else 0
    }
