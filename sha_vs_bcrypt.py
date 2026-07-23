import hashlib
import bcrypt

password = "password"

print("=" * 50)
print("SHA-256 TEST (run this script twice to compare)")
print("=" * 50)

# BAD: Plain SHA-256 (fast, vulnerable to brute force)
sha_hash1 = hashlib.sha256(password.encode()).hexdigest()
sha_hash2 = hashlib.sha256(password.encode()).hexdigest()

print(f"SHA-256 hash (attempt 1): {sha_hash1}")
print(f"SHA-256 hash (attempt 2): {sha_hash2}")
print(f"Are they identical? {sha_hash1 == sha_hash2}")
print("-> Same input ALWAYS gives same output")
print("-> Vulnerable to rainbow tables & fast brute-force attacks!")

print()
print("=" * 50)
print("BCRYPT TEST")
print("=" * 50)

# GOOD: bcrypt (slow, adds salt automatically)
bcrypt_hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
bcrypt_hash2 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

print(f"bcrypt hash (attempt 1): {bcrypt_hash1}")
print(f"bcrypt hash (attempt 2): {bcrypt_hash2}")
print(f"Are they identical? {bcrypt_hash1 == bcrypt_hash2}")
print("-> Different hash EVERY time due to random salt")
print("-> Much harder to crack, resistant to rainbow tables!")

print()
print("=" * 50)
print("CONCLUSION")
print("=" * 50)
print("SHA-256: Fast but insecure for passwords")
print("bcrypt:  Slower but secure (built-in salting)")