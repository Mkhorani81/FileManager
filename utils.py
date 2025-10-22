from decouple import config

def file_extension(value):
    item = value.split(',')
    return list(_.lower() for _ in item)