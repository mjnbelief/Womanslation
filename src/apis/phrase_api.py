from fastapi import FastAPI, HTTPException
from base import ResponseModel
from phrase import Phrase

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/phrases")
def get_phrases(page_number: int = 0, page_size: int = 10, search_text: str = "", tags: str = "") -> ResponseModel:
    try:
        result = Phrase.get_phrases(page_number, page_size, search_text, tags)
    
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
    
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/phrases")
def create_phrase(phrase: Phrase) -> ResponseModel:
    try:
        result = Phrase.create(phrase)
        
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/phrases/{phrase_id}")
def update_phrase(phrase_id: str, phrase: Phrase) -> ResponseModel:
    try:
        result = Phrase.update(phrase, phrase_id)
        
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/phrases/{phrase_id}")
def delete_phrase(phrase_id: str) -> ResponseModel:
    try:
        result = Phrase.delete(phrase_id)
        
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
