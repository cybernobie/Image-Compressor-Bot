user_data = {}

def set_user_data(user_id, key, value):
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id][key] = value

def get_user_data(user_id, key):
    return user_data.get(user_id, {}).get(key)
