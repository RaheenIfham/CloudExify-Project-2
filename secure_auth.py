import bcrypt
import json
import os
import re


class SecureAuth:
    def __init__(self, db_file='users.json', max_attempts=5):
        self.db_file = db_file
        self.users = self.load_users()
        self.max_attempts = max_attempts
        self.failed_attempts = {}

    def load_users(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.users, f)

    def validate_password_strength(self, password):
        if len(password) < 12:
            return "Password must be at least 12 characters!"
        if not re.search(r'[0-9]', password):
            return "Password must contain at least one number!"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return "Password must contain at least one special symbol!"
        return None

    def register(self, username, password):
        if not username or not username.strip():
            return "Username cannot be empty!"

        if not password or not password.strip():
            return "Password cannot be empty!"

        strength_error = self.validate_password_strength(password)
        if strength_error:
            return strength_error

        if username in self.users:
            return "User exists!"

        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )
        self.users[username] = hashed.decode()
        self.save_users()
        return "Registration successful!"

    def login(self, username, password):
        # Rate-limiting: check if account is locked
        attempts = self.failed_attempts.get(username, 0)
        if attempts >= self.max_attempts:
            return "Account locked! Too many failed attempts."

        if username not in self.users:
            self.failed_attempts[username] = attempts + 1
            return False

        stored_hash = self.users[username].encode()
        is_valid = bcrypt.checkpw(
            password.encode('utf-8'),
            stored_hash
        )

        if is_valid:
            # Reset counter on successful login
            self.failed_attempts[username] = 0
            return True
        else:
            self.failed_attempts[username] = attempts + 1
            remaining = self.max_attempts - self.failed_attempts[username]
            print(f"Failed attempt. {remaining} attempt(s) remaining before lockout.")
            return False


# Test the updated auth system
if __name__ == "__main__":
    if os.path.exists("users.json"):
        os.remove("users.json")

    auth = SecureAuth()
    print()
    print("="*50)
    print("STEP of Intructions:\n",
"1. Password must contain 12 min characters,numbers and special characters.\n",
"2. Username and password field must not be empty.\n",
"3. Too many login attempts will BLOCK the account.\n")
    print("="*50)
    print()
    print("=" * 50)
    print("TEST 1: Weak password - too short")
    print("=" * 50)
    print(auth.register("alice", "Short1!"))

    print()
    print("=" * 50)
    print("TEST 2: Weak password - no number")
    print("=" * 50)
    print(auth.register("alice", "NoNumbersHere!"))

    print()
    print("=" * 50)
    print("TEST 3: Weak password - no special symbol")
    print("=" * 50)
    print(auth.register("alice", "NoSymbolsHere123"))

    print()
    print("=" * 50)
    print("TEST 4: Strong password - meets all requirements")
    print("=" * 50)
    print(auth.register("alice", "SecurePass123!"))

    print()
    print("=" * 50)
    print("TEST 5: Rate limiting - 5 failed login attempts then lockout")
    print("=" * 50)
    for i in range(6):
        result = auth.login("alice", "WrongPassword")
        print(f"Attempt {i + 1}: {result}")

    print()
    print("=" * 50)
    print("TEST 6: Correct password after lockout (should still be locked)")
    print("=" * 50)
    print(auth.login("alice", "SecurePass123!"))