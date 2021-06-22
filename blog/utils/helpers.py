from secrets import token_urlsafe, token_hex, token_bytes, randbits
from hashlib import sha256
from base64 import b32encode
from time import time
import re


def gen_token():
    return token_hex(4)


def check_slug(url_id):
    return re.compile('^[-\w]+$').fullmatch(url_id)


def encrypt(source):
    return sha256(str(source).encode()).digest().hex()


def pk_gen():
    head = token_hex(5)
    middle = encrypt(time())[:6]    # by time
    end = encrypt(hash(head))[:6]   # by hash
    return f'{head}-{middle}-{end}'
