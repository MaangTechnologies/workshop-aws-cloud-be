import email
import uuid

from sqlalchemy import Column, String, DateTime,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Boolean

from db import base


class ContactUs(base):
    __tablename__ = 'contactus'

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    subject = Column(String)
    message = Column(String)
    app_name = Column(String)
    status = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(String)
    modified_by = Column(String)
    created_date = Column(DateTime(timezone=False), server_default=func.now())
    modified_date = Column(DateTime(timezone=False), onupdate=func.now())

class Users(base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String,index=True,unique=True)
    phone = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_by = Column(String)
    modified_by = Column(String)
    created_date = Column(DateTime(timezone=False), server_default=func.now())
    modified_date = Column(DateTime(timezone=False), onupdate=func.now())

