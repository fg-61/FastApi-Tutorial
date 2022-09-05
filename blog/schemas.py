from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    
class ShowBlog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode = True
        
        
# User
class User(BaseModel):
    name: str
    email: str
    password: str
    
# User response model
class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True