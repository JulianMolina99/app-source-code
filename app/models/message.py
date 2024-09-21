from pydantic import BaseModel

class Message(BaseModel):
    message: str
    to: str
    from_: str
    timeToLifeSec: int
