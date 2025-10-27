import secrets
import string


def file_extension(value):
    item = value.split(',')
    return list(_.lower() for _ in item)

def generate_short_code(length = 8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))