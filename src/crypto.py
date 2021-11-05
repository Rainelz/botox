import base64
import os
import hashlib
from pathlib import Path
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def preprocess_key(value: str) -> str:
    key = base64.b32encode(value.encode())
    c = hashlib.sha256()
    c.update(key)
    hashed_key = c.hexdigest()
    return hashed_key


class Crypto:
    def __init__(self):
        self.resources_path = Path('resources')
        salt_file = self.resources_path / 'init.botox'
        self._init_salt(salt_file)

    def _init_salt(self, salt_file):
        if not salt_file.exists():
            salt = os.urandom(16)
            with open(salt_file, 'wb') as f:
                f.write(base64.b32encode(salt))
        else:
            with open(salt_file, 'rb') as f:
                salt = f.read()
                salt = base64.b32decode(salt)
        self.salt = salt

    def encrypt(self, data):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        hashed_key = preprocess_key(data['password'])
        key = base64.urlsafe_b64encode(kdf.derive(hashed_key.encode()))
        f = Fernet(key)

        encoded_data = json.dumps(data, indent=2).encode()
        encrypted = f.encrypt(encoded_data)
        print(encrypted)
        return encrypted, hashed_key

    def decrypt(self, data, key):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(key.encode()))
        f = Fernet(key)
        decrypted = f.decrypt(data)
        decoded = json.loads(decrypted)
        return decoded


if __name__ == '__main__':
    test_string = 'prova'
    test_data = {'a': 1, 'password': test_string}
    c = Crypto()
    key = preprocess_key(test_string)
    decrypted = c.decrypt(c.encrypt(test_data), key)
    assert decrypted == test_data
