from pydantic import BaseModel

class Valentine_name(BaseModel):
    name:str

class UserCreate(BaseModel):
    name:str
    email:str
    password:str 

class UserLogin(BaseModel):
    email:str
    password:str
