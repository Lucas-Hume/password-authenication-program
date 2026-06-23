from config import MAX_ATTEMPTS, IT_PHRASE, USER_FILE
import os,json

# File Handling 

def load_users():
    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return {}

    # Auto-upgrade from legacy format (username: hash)
    upgraded = {}
    for username, value in data.items():
        if isinstance(value, str):
            upgraded[username] = {
                "password": value,
                "role": "user",
                "active": True
            }
        else:
            upgraded[username] = value

    if upgraded != data:
        save_users(upgraded)

    return upgraded

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)



def _row_to_dict(row):
    if row is None:
        return None
    _id, username, password, role, active = row
    return {
        #"id": _id,
        #"username": username,
        "password": password,
        "role": role,
        "active": bool(active)
    }
