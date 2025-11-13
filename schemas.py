from pydantic import BaseModel

class Message(BaseModel):
    title: str
    content: str   
    published: bool = True
    