import bcrypt
from cryptography.fernet import Fernet
import hashlib

print("bcrypt installed OK")
print("Fernet key generation test:", Fernet.generate_key())
print("hashlib test:", hashlib.sha256(b"test").hexdigest())