from pydantic import BaseModel

class UserLogin(BaseModel):
    identifier: str  # Email or Phone
    password: str
