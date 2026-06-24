from colorama import Fore, Style
from config import MAX_ATTEMPTS, IT_PHRASE
from security import hash_password, check_password
from database import get_user,get_all_users,add_user, user_exists, update_password, make_admin

# ---------------- Registration ----------------

def Registration():
    print(Fore.CYAN + Style.BRIGHT + "\n================")
    print(" Registration")
    print(Fore.CYAN + Style.BRIGHT + "================")

    auth_phrase = input("Please enter the IT pass phrase: ").strip()
    if auth_phrase != IT_PHRASE:
        print(Fore.RED + Style.BRIGHT +
              "Authentication failed. Please contact IT.")
        return

    new_username = input("Enter a new username: ").strip()
    if not new_username:
        print(Fore.RED + "Username cannot be empty.")
        return

    if user_exists(new_username):
        print(Fore.RED + "Username already exists.")
        return

    while True:
        new_password = input(
            "Enter a password (12–17 characters): ").strip()

        if not 12 <= len(new_password) <= 17:
            print(Fore.RED +
                  "Password must be between 12 and 17 characters.")
            continue

        add_user(new_username, hash_password(new_password))

        print(Fore.BLUE + Style.BRIGHT +
              f"New account created for {new_username}.")
        break

def ForgotPassword():
    print(Fore.CYAN + Style.BRIGHT + "\n ========")
    print(" Forgot Password")
    print(Fore.CYAN + Style.BRIGHT + "\n ========")
    auth_phrase= input("Please enter the IT pass phrase: ").strip()
    if auth_phrase != IT_PHRASE:
        print(Fore.RED + Style.BRIGHT+
              "Authentication failed.Please contact IT")
        return
    
    username= input("Enter the username to reset: ").strip()
    if not user_exists(username):
        print(Fore.RED +"No account with that username exists")
        return
    while True:
        new_password= input(
            "Enter a new password (12-17 characters): ").strip()
        if not 12 <= len(new_password) <= 17:
            print(Fore.RED+ 
                  "PAssword must be 12-17 characters.")
            continue
        update_password(username, hash_password(new_password))
        print(Fore.BLUE + Style.BRIGHT +
              f"Password sucessfully reset for {username}.")
        break


# ---------------- Login ----------------

def LogIn():
    print(Fore.CYAN + Style.BRIGHT + "\n================")
    print(" Login")
    print(Fore.CYAN + Style.BRIGHT + "================")

    attempts = 0

    while attempts < MAX_ATTEMPTS:
        username_input = input("Username: ").strip()
        password_input = input("Password: ").strip()

        user = get_user(username_input)

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

def ViewAccounts(logged_in_user):
    print(Fore.CYAN + Style.BRIGHT + "\n================")
    print(" View Existing Accounts")
    print(Fore.CYAN + Style.BRIGHT + "================")

    if not logged_in_user:
        print(Fore.RED + "You must be logged in.")
        return False

    users = get_all_users()
    if not users:
        print("No accounts found.")
        return False

    print("\nExisting Accounts:")
    for row in users:
        print(f"- {row['username']}")

    print(Fore.YELLOW + Style.BRIGHT +
          f"\nTotal number of users: {len(users)}")
    return True

# Admin Panel

def AdminPanel():
    users = get_all_users()

    print(Fore.YELLOW + Style.BRIGHT + "\n=== ADMIN PANEL ===")
    if not users:
        print("No accounts found.")
        return
    for row in users:
        status = "ACTIVE" if row["active"] else "DISABLED"
        print(f"{row['username']} | {row['role']} | {status}")

#Might make a make a user an admin feature
    
