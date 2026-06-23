from colorama import Fore, Style
import bcrypt
from config import MAX_ATTEMPTS, IT_PHRASE
from storage import load_users, save_users
from database import create_db



# ---------------- Password Handling ----------------

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode())

# ---------------- Registration ----------------

def Registration(users):
    print(Fore.CYAN + Style.BRIGHT + "\n================")
    print(" Registration")
    print(Fore.CYAN + Style.BRIGHT + "================")

    auth_phrase = input("Please enter the IT pass phrase: ").strip()
    if auth_phrase != IT_PHRASE:
        print(Fore.RED + Style.BRIGHT +
              "Authentication failed. Please contact IT.")
        return

    users = load_users()

    new_username = input("Enter a new username: ").strip()
    if not new_username:
        print(Fore.RED + "Username cannot be empty.")
        return

    if new_username in users:
        print(Fore.RED + "Username already exists.")
        return

    while True:
        new_password = input(
            "Enter a password (12–17 characters): ").strip()

        if not 12 <= len(new_password) <= 17:
            print(Fore.RED +
                  "Password must be between 12 and 17 characters.")
            continue

        users[new_username] = {
            "password": hash_password(new_password),
            "role": "user",
            "active": True
        }

        save_users(users)
        print(Fore.BLUE + Style.BRIGHT +
              f"New account created for {new_username}.")
        break

# ---------------- Login ----------------

def LogIn(users):
    print(Fore.CYAN + Style.BRIGHT + "\n================")
    print(" Login")
    print(Fore.CYAN + Style.BRIGHT + "================")

    users = load_users()
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        username_input = input("Username: ").strip()
        password_input = input("Password: ").strip()

        user = users.get(username_input)

        if user and user["active"]:
            if check_password(password_input, user["password"]):
                print(Fore.GREEN + Style.BRIGHT +
                      f"Login successful. Welcome {username_input}.")
                return username_input, user["role"]

        attempts += 1
        print(Fore.RED + "Access denied.")

    print(Fore.RED + "Too many failed login attempts.")
    return None, None

# ---------------- View Accounts ----------------

def ViewAccounts(users, logged_in_user):
    print(Fore.CYAN + Style.BRIGHT + "\n================")
    print(" View Existing Accounts")
    print(Fore.CYAN + Style.BRIGHT + "================")

    if not logged_in_user:
        print(Fore.RED + "You must be logged in.")
        return False

    users = load_users()
    if not users:
        print("No accounts found.")
        return False

    print("\nExisting Accounts:")
    for username in users:
        print(f"- {username}")

    print(Fore.YELLOW + Style.BRIGHT +
          f"\nTotal number of users: {len(users)}")
    return True

# Admin Panel

def AdminPanel():
    users = load_users()

    print(Fore.YELLOW + Style.BRIGHT + "\n=== ADMIN PANEL ===")

    for username, data in users.items():
        status = "ACTIVE" if data["active"] else "DISABLED"
        print(f"{username} | {data['role']} | {status}")
