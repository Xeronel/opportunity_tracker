from .db import DBConfig as __DBConfig
from .web import WebConfig as __WebConfig
from .smtp import SMTPConfig as __SMTPConfig

db = __DBConfig()
web = __WebConfig()
smtp = __SMTPConfig()
__all__ = ['db', 'web', 'smtp']