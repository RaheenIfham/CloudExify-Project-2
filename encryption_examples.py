from cryptography.fernet import Fernet

print("=" * 50)
print("FERNET SYMMETRIC ENCRYPTION DEMO")
print("=" * 50)

# Generate a key (save securely!)
key = Fernet.generate_key()
cipher = Fernet(key)

print(f"Generated Key: {key}")

# Encrypt sensitive data
sensitive = b"Credit card: 1234-5678-9012-3456"
encrypted = cipher.encrypt(sensitive)

print(f"\nOriginal Data:  {sensitive}")
print(f"Encrypted Data: {encrypted}")

# Decrypt (with correct key)
decrypted = cipher.decrypt(encrypted)
print(f"\nDecrypted Data: {decrypted}")
print(f"Match original? {decrypted == sensitive}")

print()
print("=" * 50)
print("TEST: Decryption with WRONG key (should fail)")
print("=" * 50)

# Generate a different (wrong) key
wrong_key = Fernet.generate_key()
wrong_cipher = Fernet(wrong_key)

try:
    wrong_cipher.decrypt(encrypted)
    print("Decrypted successfully (this should NOT happen!)")
except Exception as e:
    print(f"Decryption FAILED as expected!")
    print(f"Error type: {type(e).__name__}")
    print("-> This proves encryption prevents unauthorized access")