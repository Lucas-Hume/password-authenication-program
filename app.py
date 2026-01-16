# This code is designed to create a password management program and:
# 1. Provide a simple CLI interface
# 2. Allow new users to register an account
# 3. Allow users to log in
# 4. Allow viewing of accounts once logged in
# 5. Use secure password hashing (bcrypt)
#
# Originally developed as a TAFE assignment and later independently refactored.

import os
import json
import bcrypt
from colorama import Fore, Style, init

init(autoreset=True)

# ---------------- Configuration ----------------

MAX_ATTEMPTS = 3
IT_PHRASE = "2025"        # Simulated IT onboarding phrase
USER_FILE = "users.json"

# ---------------- File Handling ----------------

def load_users():
    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return {}

    # Auto-upgrade legacy format (username: hash)
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

#  Command Resolver 

def resolve_command(user_input):
    user_input = user_input.lower().strip()

    if any(cmd in user_input for cmd in ["register", "sign up", "signup"]):
        return "register"
    
    if any(cmd in user_input for cmd in["admin"]):
        return "admin"

    if any(cmd in user_input for cmd in ["login", "log in", "sign in"]):
        return "login"

    if any(cmd in user_input for cmd in ["view", "accounts", "show"]):
        return "view"

    if any(cmd in user_input for cmd in ["quit", "exit", "sign out"]):
        return "quit"
    

    return None

#  Main Program 

users = load_users()
logged_in_user = None
logged_in_role = None

while True:
    print(Fore.CYAN + Style.BRIGHT + "\n=============================")
    print(Fore.YELLOW + Style.BRIGHT +
          " Accounts Management Program")
    print(Fore.CYAN + Style.BRIGHT + "=============================")
    print(Fore.GREEN + "Register  - Create a new account")
    print(Fore.GREEN + "Login     - Log in to the system")
    print(Fore.GREEN + "View      - View existing accounts")
    print(Fore.RED   + "Quit      - Exit the program")

    user_input = input(Fore.MAGENTA + Style.BRIGHT + "> ")
    command = resolve_command(user_input)

    if command == "register":
        Registration(users)

    elif command == "login":
        logged_in_user, logged_in_role = LogIn(users)
        if logged_in_user:
            print(Fore.GREEN +
                  "You have successfully logged in.")
            if logged_in_role == "admin":
                AdminPanel()

    elif command == "admin":
        if not logged_in_user:
            print(Fore.RED + Style.BRIGHT +
              "Admin access denied. You must be logged in.")
        continue

        if logged_in_role != "admin":
            print(Fore.RED + Style.BRIGHT +
              "Admin access denied. Insufficient privileges.")
        continue

        AdminPanel()

    elif command == "view":
        if not logged_in_user:
            print(Fore.YELLOW + Style.BRIGHT +
                  "Must log in to view accounts.")
            logged_in_user, logged_in_role = LogIn(users)
            if not logged_in_user:
                continue

        ViewAccounts(users, logged_in_user)

    elif command == "quit":
        print(Fore.CYAN + Style.BRIGHT + "Goodbye.")
        break

    else:
        print(Fore.RED + Style.BRIGHT +
              "Error - try 'register', 'login', 'view', or 'quit'.")
