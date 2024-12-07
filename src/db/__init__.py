import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from const import POSTGRES_DB_PSWD, POSTGRES_DB_URL, POSTGRES_DB_USERNAME, POSTGRES_DB_NAME, POSTGRES_DATABASE_URL

try:
    #host = os.getenv(POSTGRES_DB_URL)
    #user = os.getenv(POSTGRES_DB_USERNAME)
    #db = os.getenv(POSTGRES_DB_NAME)
    #db_string = create_engine(f'postgresql://{user}:{os.getenv(POSTGRES_DB_PSWD)}@{host}/{db}')
    db_string = create_engine(POSTGRES_DATABASE_URL)
    Session = sessionmaker(bind=db_string)
    base = declarative_base()

except Exception as err:
    raise Exception(f'{err}')


class SessionHandler:
    def __init__(self):
        self.session_obj = None

        try:
            self.session_obj = Session()
            self.session_obj.begin()
            return
        except Exception as err:
            raise Exception(f'Unable to create Session : {err}')

    def get_active_session(self):
        return self.session_obj

    def begin(self, subtransactions=False, nested=False):
        if not self.session_obj.is_active:
            self.session_obj.begin()

    def commit(self):
        if self.session_obj.is_active:
            self.session_obj.commit()

    def rollback(self):
        self.session_obj.rollback()

    def close(self):
        self.session_obj.close()
