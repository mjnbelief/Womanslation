from pydantic import BaseModel, ValidationError
from typing import Dict
from enum import Enum

class Base(BaseModel):
    """
    Base class for all models. This class is used to define the common attributes and methods for all models.
    """
    id: str
    create_date: str


class ResponseModel(ValidationError):
    """
    Custom response class.
    """
    success: bool
    message: str
    data: Dict[str, str]


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