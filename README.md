# CloudExify Internship — Month 1, Project 2
## Cryptography & Password Security

### Overview

This project implements a secure password authentication system and a symmetric
encryption/decryption system using Python. It demonstrates core cryptography
concepts including password hashing with bcrypt, salting, rate-limiting, and
Fernet symmetric encryption, along with a practical comparison against insecure
password storage methods like plain SHA-256.

### Files in this repository

| File | Purpose |
|---|---|
| `secure_auth.py` | Full authentication system: user registration, login, password strength validation, rate-limiting |
| `encryption_examples.py` | Fernet symmetric encryption/decryption demo |
| `password_hashing.py` | Basic bcrypt hashing and verification example |
| `sha_vs_bcrypt.py` | Side-by-side comparison of SHA-256 vs bcrypt |
| `test_checklist.py` | Automated test script covering all Section 5 checklist items |
| `test_setup.py` | Verifies all required libraries are installed correctly |
| `users.json` | Sample registered user data (bcrypt hashes only, no plaintext passwords) |
| `CloudExify_Project2_Screenshots/` | Screenshots documenting each stage of development and testing |

### Setup instructions

1. Install Python 3.10 or higher
2. Install required libraries:
   ```
   pip install bcrypt
   pip install cryptography
   ```
3. Run any script directly, for example:
   ```
   python secure_auth.py
   ```

### Findings

**Why bcrypt instead of SHA-256 for passwords**

SHA-256 is deterministic — the same input always produces the same output. This
was confirmed directly in testing: hashing the same password twice with SHA-256
produced identical results every time. This makes it vulnerable to rainbow table
attacks, where an attacker can precompute hashes for common passwords once and
match stolen hashes instantly.

bcrypt solves this by generating a random salt automatically on every hash
operation. Testing confirmed that hashing the same password twice with bcrypt
produced two completely different results, since each call embeds a fresh random
salt directly into the output string. This makes precomputed lookup tables
useless against it.

**How password verification works despite the random salt**

Since the salt is embedded inside the stored bcrypt hash itself (not stored
separately), `bcrypt.checkpw()` extracts the original salt from the stored hash,
re-hashes the entered password using that same salt, and compares the result.
This is why login verification still works correctly even though every stored
hash looks different.

**Why encryption (not hashing) was used for the credit card example**

Passwords only ever need to be verified, never retrieved — so hashing (a one-way
process) is appropriate. Sensitive data like a credit card number needs to be
retrieved and reused later (e.g., to process a payment), so it must be
reversible — which is why Fernet symmetric encryption was used instead of
hashing for that example.

**Testing results**

All Section 5 checklist items were tested and passed:
- bcrypt produces a different hash on each run
- Correct password verification returns `True`
- Incorrect password verification returns `False`
- Data encrypted with Fernet can be successfully decrypted with the correct key
- Attempting decryption with the wrong key raises an `InvalidToken` exception
- User registration correctly stores only the bcrypt hash, never the plaintext password
- Login verification works correctly for registered users
- Salting confirmed effective against rainbow table-style attacks

**Security improvements added beyond the base guide**

- Password strength validation: minimum 12 characters, must include at least
  one number and one special symbol
- Rate-limiting: accounts lock after 5 consecutive failed login attempts
- Input validation for empty usernames and passwords
- Graceful handling of a missing `users.json` file on first run

**Known limitations / not implemented in this scope**

- Multi-factor authentication (MFA) was not implemented. This would typically
  require an additional verification channel (e.g., email or SMS one-time
  codes) and was considered out of scope for this project's timeframe.
- HTTPS/TLS enforcement was reviewed conceptually (see Section 3, Step 6 of
  the project guide) but not deployed, since this project does not include a
  live web server component.

### Conclusion

This project demonstrates the practical difference between hashing and
encryption, why each is appropriate for different types of sensitive data, and
how bcrypt's salting mechanism defends against common password-cracking
techniques that plain hash functions like SHA-256 cannot resist.

### 15-day project plan

| Days | Task | Status | Est. Time |
|---|---|---|---|
| Jul 16 (Wed) | Environment setup | ✅ Completed | 1.5 hrs |
| Jul 17 (Thu) | Section 3 Step 2: bcrypt password hashing + verification script | ✅ Completed | 1.5 hrs |
| Jul 18 (Fri) | Section 3 Step 3: SHA-256 vs bcrypt comparison demo | ✅ Completed | 1 hr |
| Jul 19 (Sat) | Section 3 Step 4: Fernet symmetric encryption → `encryption_examples.py` | ✅ Completed | 2 hrs |
| Jul 20 (Sun) | Create GitHub repo `CloudExify-Project-2` (Public, empty) | ✅ Completed | 1 hr |
| Jul 21 (Mon) | Section 3 Step 5 (part 1): `SecureAuth` class skeleton | ✅ Completed | 1.5 hrs |
| Jul 22 (Tue) | Section 3 Step 5 (part 2): `register()` and `login()` methods → complete `secure_auth.py` | ✅ Completed | 1.5 hrs |
| Jul 23 (Wed) | Section 3 Step 6: SSL/TLS & HTTPS concepts (read-through) | ✅ Completed | 1 hr |
| Jul 24 (Thu) | Run full Section 5 Testing Checklist against the code | ✅ Completed | 2 hrs |
| Jul 25 (Fri) | Fix bugs/edge cases found during testing | ✅ Completed | 1.5 hrs |
| Jul 26 (Sat) | Verify Section 4 Best Practices Checklist against the code | ✅ Completed | 1 hr |
| Jul 27 (Sun) | Take screenshots of all working scripts | ✅ Completed | 1 hr |
| Jul 28 (Mon) | Browser upload: `.py` files + screenshots into `CloudExify-Project-2` | ✅ Completed | 1 hr |
| Jul 29 (Tue) | Write `README.md` report — overview, setup, how to run, findings | ✅ Completed | 1.5 hrs |
| Jul 30 (Wed) | Final check: repo public, all files present, submit link | ✅ Completed | 1 hr |
