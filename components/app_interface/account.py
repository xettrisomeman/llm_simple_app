from pydantic import BaseModel





## LOGIN
class Login(BaseModel):
    username: str
    password: str  


class Register(BaseModel):
    username: str
    password: str
    password2: str
