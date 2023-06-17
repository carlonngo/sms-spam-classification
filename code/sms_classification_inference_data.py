from pydantic import BaseModel
from typing import List

#Pydantic data classes for data validation
class SpamClassificationRequest(BaseModel): 
    messages: List[str]

class SingleResponse(BaseModel):
    body: str
    label: str

class SpamClassificationResponse(BaseModel):
    response: List[SingleResponse]
    