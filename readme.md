# Account Management CLI (Python)

A command-line user authentication and account management system written in
Python. The program uses bcrypt to securely hash passwords and stores account
data in a JSON file.

This project was originally developed as part of a TAFE assessment and was
later independently refactored and extended to follow industry-aligned
security and design practices.

---

## Features

- User registration with password length enforcement
- Secure password hashing using bcrypt
- Login system with limited attempts
- Role support (user / admin)
- Account status tracking (active / disabled)
- Admin-only account overview
- Flexible natural-language command input
- Automatic migration of legacy user data formats
- Simple, readable procedural structure

---

## Security Design

- Passwords are **never stored or displayed in plaintext**
- bcrypt hashing prevents password recovery
- Administrators can manage accounts but **cannot view passwords**
- Login attempts are limited to reduce brute-force attempts

---

## Project Structure

.
├── app.py
├── users.json
├── requirements.txt
└── README.md

yaml
Copy code

---

## Requirements

Install dependencies using:

pip install -r requirements.txt

go
Copy code

`requirements.txt`:
bcrypt
colorama

yaml
Copy code

---

## Running the Program

python app.py

yaml
Copy code

Commands may be entered in natural language, for example:
- `register`
- `log in`
- `view accounts`
- `exit`

---

## Disclaimer

This project is intended for learning and portfolio demonstration purposes.
It is not production-ready software and would require additional hardening
(logging, encryption at rest, access controls, auditing) before real-world use.