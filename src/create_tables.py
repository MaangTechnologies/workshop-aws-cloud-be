from db import db_string
from db.models import base
def create():
    base.metadata.create_all(db_string)