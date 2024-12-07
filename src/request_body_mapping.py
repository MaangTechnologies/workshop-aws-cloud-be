from typing import Any
from typing import Optional

from pydantic import BaseModel

class ContactUs(BaseModel):
    name: str
    email: str
    phone: str
    subject: Optional[str] = None
    message: str
    app_name:str

class UpdateStatus(BaseModel):
    status: bool

class AccessToken(BaseModel):
    user_name: str
    password: str
