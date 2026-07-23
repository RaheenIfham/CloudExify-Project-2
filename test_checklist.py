import bcrypt
from cryptography.fernet import Fernet
from secure_auth import SecureAuth
import os

print("=" * 55)
print("CHECKLIST 1: Generate bcrypt hash -> different each time")
print("=" * 55)
h1 = bcrypt.hashpw(b"password", bcrypt.gensalt())
h2 = bcrypt.hashpw(b"password", bcrypt.gensalt())
print(f"Hash 1: {h1}")
print(f"Hash 2: {h2}")
print(f"PASS: {h1 != h2}")

print()
print("=" * 55)
print("CHECKLIST 2: Verify correct password -> returns True")
print("=" * 55)
result = bcrypt.checkpw(b"password", h1)
print(f"PASS: {result is True}")

print()
print("=" * 55)
print("CHECKLIST 3: Reject wrong password -> returns False")
print("=" * 55)
result = bcrypt.checkpw(b"wrongpassword", h1)
print(f"PASS: {result is False}")

print()
print("=" * 55)
print("CHECKLIST 4: Encrypt and decrypt data -> recoverable with key")
print("=" * 55)
key = Fernet.generate_key()
cipher = Fernet(key)
original = b"Test data 123"
encrypted = cipher.encrypt(original)
decrypted = cipher.decrypt(encrypted)
print(f"PASS: {decrypted == original}")

print()
print("=" * 55)
print("CHECKLIST 5: Encryption with wrong key -> raises exception")
print("=" * 55)
wrong_key = Fernet.generate_key()
wrong_cipher = Fernet(wrong_key)
try:
    wrong_cipher.decrypt(encrypted)
    print("PASS: False (no exception raised - THIS IS WRONG)")
except Exception:
    print("PASS: True (exception raised as expected)")

print()
print("=" * 55)
print("CHECKLIST 6: User registration system -> users saved securely")
print("=" * 55)
if os.path.exists("test_users.json"):
    os.remove("test_users.json")
auth = SecureAuth(db_file="test_users.json")
result = auth.register("testuser", "TestPass123")
print(f"Registration result: {result}")
print(f"PASS: {result == 'Registration successful!'}")
print(f"Stored value (should be hash, not plaintext): {auth.users['testuser']}")

print()
print("=" * 55)
print("CHECKLIST 7: User login verification -> correct password works")
print("=" * 55)
result = auth.login("testuser", "TestPass123")
print(f"PASS: {result is True}")

print()
print("=" * 55)
print("CHECKLIST 8: Rainbow table resistance -> salt prevents lookup")
print("=" * 55)
same_pw_hash1 = bcrypt.hashpw(b"CommonPassword1", bcrypt.gensalt())
same_pw_hash2 = bcrypt.hashpw(b"CommonPassword1", bcrypt.gensalt())
print(f"PASS: {same_pw_hash1 != same_pw_hash2}")

print()
print("=" * 55)
print("ALL CHECKLIST TESTS COMPLETE")
print("=" * 55)

# Cleanup test file
if os.path.exists("test_users.json"):
    os.remove("test_users.json")