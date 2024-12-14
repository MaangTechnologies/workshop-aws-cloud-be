import os
from urllib.parse import quote

POSTGRES_DB_USERNAME = ''
POSTGRES_DB_PSWD = ''
encoded_password = quote(POSTGRES_DB_PSWD, safe='')
POSTGRES_DB_URL = ''
POSTGRES_DB_NAME = ''

POSTGRES_DATABASE_URL = 'sqlite:///./aws.db'
# POSTGRES_DATABASE_URL = f'postgresql://{POSTGRES_DB_USERNAME}:{encoded_password}@{POSTGRES_DB_URL}/{POSTGRES_DB_NAME}'

PREFIX_URL = "/contact"
USER_NAME = "FangLing"
PW = "FangLing@123"