from pydantic import BaseModel
from typing import List, Optional

class Auth_signatory(BaseModel):
    document:str#
    name:Optional[str]=None
    rank:Optional[str]=None
    designation:Optional[str]=None
    signed_for:str#