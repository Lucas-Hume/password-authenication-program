# This code is designed to create a password management program and:
# 1. Provide a simple CLI interface
# 2. Allow new users to register an account
# 3. Allow users to log in
# 4. Allow viewing of accounts once logged in
# 5. Use secure password hashing (bcrypt)
#
# Originally developed as a TAFE assignment and later independently refactored.

from database import create_db
from colorama import Fore, Style, init
from config import MAX_ATTEMPTS, IT_PHRASE
from security import hash_password, check_password
from auth_flows import Registration, LogIn, ViewAccounts, AdminPanel, ForgotPassword

init(autoreset=True)
create_db()

# Configuration 



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
    
    if any(cmd in user_input for cmd in ["Forgot","reset"]):
        return "reset"
    

    return None

#  Main Program 

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
    print(Fore.GREEN + "Reset     - Reset a forgotten password")
    print(Fore.RED   + "Quit      - Exit the program")

    user_input = input(Fore.MAGENTA + Style.BRIGHT + "> ")
    command = resolve_command(user_input)

    if command == "register":
        Registration()
    elif command =="reset":
        ForgotPassword()

    elif command == "login":
        logged_in_user, logged_in_role = LogIn()
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
            logged_in_user, logged_in_role = LogIn()
            if not logged_in_user:
                continue

        ViewAccounts(logged_in_user)

    elif command == "quit":
        print(Fore.CYAN + Style.BRIGHT + "Goodbye.")
        break

    else:
        print(Fore.RED + Style.BRIGHT +
              "Error - try 'register', 'login', 'view','reset' or 'quit'.")
