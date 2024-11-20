import hashlib


def hash_password(password: str, salt: bytes) -> tuple[str, bytes]:
    key = hashlib.pbkdf2_hmac(
        'sha512',
        password.encode('utf-8'),
        salt,
        iterations=10000,
        dklen=64
    )
    return key.hex()