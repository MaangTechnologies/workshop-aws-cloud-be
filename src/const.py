import os
from urllib.parse import quote

POSTGRES_DB_USERNAME = 'workshop-aws-user'
POSTGRES_DB_PSWD = 'workshop-aws-user!?!?'
encoded_password = quote(POSTGRES_DB_PSWD, safe='')
POSTGRES_DB_URL = '178.16.139.18:5432'
POSTGRES_DB_NAME = 'workshop-aws'

# POSTGRES_DATABASE_URL = 'sqlite:///./spp.db'
POSTGRES_DATABASE_URL = f'postgresql://{POSTGRES_DB_USERNAME}:{encoded_password}@{POSTGRES_DB_URL}/{POSTGRES_DB_NAME}'

PREFIX_URL = "/contact"
USER_NAME = "FangLing"
PW = "FangLing@123"