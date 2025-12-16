import hashlib

SALT = b'FGHRYSKGJTUSHFVO'


def get_string_hash(string: str) -> str:
    pwd_salt = SALT + string.encode('utf-8')
    hash_digest = hashlib.sha256(pwd_salt).hexdigest()
    return hash_digest


def verify_hashed_string(plain_string: str, hashed_string: str) -> bool:
    pwd_salt = SALT + plain_string.encode('utf-8')
    return hashlib.sha256(pwd_salt).hexdigest() == hashed_string
