import hashlib
import os


def verify_hashed_password(plain_password: str, hashed_password: str) -> bool:
    try:
        salt_hex, hash_digest = hashed_password.split(':')
        salt = bytes.fromhex(salt_hex)
        pwd_salt = salt + plain_password.encode('utf-8')
    except ValueError:
        return False

    return hashlib.sha256(pwd_salt).hexdigest() == hash_digest


def get_password_hash(password: str) -> str:
    salt = os.urandom(16)
    pwd_salt = salt + password.encode('utf-8')
    hash_digest = hashlib.sha256(pwd_salt).hexdigest()

    return salt.hex() + ':' + hash_digest
