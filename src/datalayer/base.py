import datetime
from pydantic import BaseModel, ValidationError
from typing import Dict, Optional
from enum import Enum

class Base(BaseModel):
    """
    Base class for all models. This class is used to define the common attributes and methods for all models.
    It includes an ID and a creation date.
    Attributes:
        id (str): The unique identifier for the model instance.
        create_date (datetime.datetime, optional): The date and time when the model instance was created.
    """
    
    id: Optional[str] = None
    _create_date: Optional[datetime.datetime] = None


class ResponseModel(BaseModel):
    """
    Custom response class.
    """
    success: bool
    message: Optional[str] = None
    data: Optional[object] = None


class ToneEnum(str, Enum):
    a = 'Passive-aggressive'
    b = 'Cold / Dismissive'
    c = 'Testing'
    d = 'Sarcastic'
    f = 'Hurt / Indirect'
    g = 'Playful'
    h = 'Angry / Confrontational'
    i = 'Guilt-inducing	'
    j = 'Disappointed'
    k = 'Flirty / Teasing'
    l = 'Neutral / Literal'
    m = 'Confusing on purpose'
    n = 'Manipulative'
    o = 'Affectionate / Sweet'
    p = 'Insecure'
    q = 'other'