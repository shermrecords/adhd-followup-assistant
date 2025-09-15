from pydantic import BaseModel
from typing import List

class ChatIn(BaseModel):
    patient_id: str
    message: str

class Cite(BaseModel):
    title: str
    source: str
    snippet: str

class ChatOut(BaseModel):
    reply: str
    cites: List[Cite] = []
    followups: List[str] = []
