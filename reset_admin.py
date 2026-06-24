import sqlite3
from security import hash_password

new_password = input("Enter a new password for lucasanthony (12-17 chars): ").strip()

if not 12 <= len(new_password) <= 17:
    print("Password must be between 12 and 17 characters. Try again.")
else:
    hashed = hash_password(new_password)

    conn = sqlite3.connect("users.db")
    conn.execute(
        "UPDATE users SET password = ?, role = 'admin' WHERE username = ?",
        (hashed, "lucasanthony")
    )
    conn.commit()
    conn.close()

    print("Password reset and admin role granted for lucasanthony.")