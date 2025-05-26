import datetime
import logging
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from contextvars import ContextVar
from fastapi import Request

my_logger = logging.getLogger("my_logger")
logging.basicConfig(level=logging.ERROR, filename="my_logger.log")

_request_context: ContextVar[Request] = ContextVar("request")

def set_request_context(request: Request):
    _request_context.set(request)

def get_current_request() -> Request:
    return _request_context.get()

def get_ip() -> str:
    """
    Get the IP address of the current request.
    """
    x_forwarded_for = get_current_request().headers.get("x-forwarded-for")
    if x_forwarded_for:
        user_ip = x_forwarded_for.split(",")[0].strip()
    else:
        user_ip = get_current_request().client.host
    return user_ip

class Base(BaseModel):
    """
    Base class for all models. This class is used to define the common attributes and methods for all models.
    It includes an ID and a creation date.
    Attributes:
        id (str): The unique identifier for the model instance.
        create_date (datetime.datetime, optional): The date and time when the model instance was created.
    """
    
    id: Optional[str] = None
    create_date: Optional[datetime.datetime] = None


class ResponseModel(BaseModel):
    """
    Custom response class.
    """
    success: bool
    message: Optional[str] = None
    data: Optional[object] = None


class SortEnum(str, Enum):
    A_Z = 'A-Z'
    Z_A = 'Z-A'
    oldest = 'oldest'
    newest = 'newest'
    most_viewed = 'most_viewed'

class ToneEnum(str, Enum):
    a = 'Passive-aggressive'
    b = 'Cold / Dismissive'
    c = 'Testing'
    d = 'Sarcastic'
    f = 'Hurt / Indirect'
    g = 'Playful'
    h = 'Angry / Confrontational'
    i = 'Guilt-inducing'
    j = 'Disappointed'
    k = 'Flirty / Teasing'
    l = 'Neutral / Literal'
    m = 'Confusing on purpose'
    n = 'Manipulative'
    o = 'Affectionate / Sweet'
    p = 'Insecure'
    q = 'other'