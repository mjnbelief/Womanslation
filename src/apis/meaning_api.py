from fastapi import FastAPI, HTTPException
from base import ResponseModel
from meaning import Meaning

app = FastAPI()

@app.get("/phrases/{phrase_id}/meanings")
def get_meanings_by_phrase_id(phrase_id: str) -> ResponseModel:
    try:
        
        result = Meaning.get_meanings_by_phrase_id(phrase_id)
        
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))