import bcrypt

# User registers - hash their password
password = "MyPassword123"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(
    password.encode('utf-8'),
    salt
)

# Store ONLY the hashed version in database
# Do NOT store plaintext password!
print(f"Hashed: {hashed}")

# Later: User logs in - verify password
entered_password = "MyPassword123"
is_valid = bcrypt.checkpw(
    entered_password.encode('utf-8'),
    hashed
)

if is_valid:
    print("Login successful!")
else:
    print("Invalid password!")

# Bonus test: try with a WRONG password
wrong_password = "WrongPassword456"
is_valid_wrong = bcrypt.checkpw(
    wrong_password.encode('utf-8'),
    hashed
)

if is_valid_wrong:
    print("Login successful!")
else:
    print("Invalid password! (as expected)")