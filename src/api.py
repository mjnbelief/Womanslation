from fastapi import FastAPI, Request, HTTPException

# from phrase import Phrase

# from src.base import ResponseModel
from src.phrase import Phrase

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/phrases")
def get_phrases():
    try:
        return Phrase.get_all_phrases()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))