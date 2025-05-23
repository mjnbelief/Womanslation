from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from base import ResponseModel, SortEnum, get_ip, set_request_context
from meaning import Meaning
from phrase import Phrase
from user_vote import User_Vote

app = FastAPI()

origins = [
    "https://preview--api-view-sweet-thing.lovable.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to store the request globally
@app.middleware("http")
async def add_request_context(request: Request, call_next):
    set_request_context(request)
    response = await call_next(request)
    return response

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/phrases", response_model=ResponseModel)
def get_phrases(page_number: int = 0, page_size: int = 10, pageOrder: SortEnum = SortEnum.newest, search_text: str = "", tags: str = "") -> ResponseModel:
    try:
        result = Phrase.get_phrases(page_number, page_size, pageOrder, search_text, tags)

        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/phrases", response_model=ResponseModel)
def create_phrase(phrase: Phrase) -> ResponseModel:
    try:
        result = Phrase.create(phrase)
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/phrases/{phrase_id}/view", response_model=ResponseModel)
def view_phrase(phrase_id: str) -> ResponseModel:
    try:
        result = Phrase.Phrase_viewed(phrase_id)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/phrases/{phrase_id}", response_model=ResponseModel)
def update_phrase(phrase_id: str, phrase: Phrase) -> ResponseModel:
    try:
        result = Phrase.update(phrase, phrase_id)
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/phrases/{phrase_id}", response_model=ResponseModel)
def delete_phrase(phrase_id: str) -> ResponseModel:
    try:
        result = Phrase.delete(phrase_id)
        
        if not result.success:
            return result
        
        # delete all likes also
        User_Vote.delete_by_phrase_id(phrase_id)
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/phrases/{phrase_id}/meanings", response_model=ResponseModel)
def get_meanings_by_phrase_id(phrase_id: str) -> ResponseModel:
    try:
        
        result = Meaning.get_meanings_by_phrase_id(phrase_id)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/phrases/{phrase_id}/meanings", response_model=ResponseModel)
def create_meaning(phrase_id: str, meaning: Meaning) -> ResponseModel:
    try:
        
        result = Meaning.create(meaning, phrase_id)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/phrases/{phrase_id}/meanings/{meaning_id}", response_model=ResponseModel)
def update_meaning(phrase_id: str, meaning_id: str, meaning: Meaning) -> ResponseModel:
    try:
        result = Meaning.update(meaning, phrase_id, meaning_id)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/phrases/{phrase_id}/meanings/{meaning_id}", response_model=ResponseModel)
def delete_meaning(phrase_id: str, meaning_id: str) -> ResponseModel:
    try:
        result = Meaning.delete(phrase_id, meaning_id)
        
        if not result.success:
            return result
        
        # delete all likes also
        User_Vote.delete_by_meaning_id(meaning_id)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/phrases/{phrase_id}/meanings", response_model=ResponseModel)
def delete_meanings_by_phrase_id(phrase_id: str) -> ResponseModel:
    try:
        result = Meaning.delete_meanings_by_phrase_id(phrase_id)
        
        if not result.success:
            return result

        # delete all likes also
        User_Vote.delete_by_phrase_id(phrase_id)

        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/phrases/{phrase_id}/meanings/{meaning_id}/vote", response_model=ResponseModel)
def create_vote(phrase_id: str, meaning_id: str, like: bool, request: Request) -> ResponseModel:
    """
    Create a vote for a meaning.
    for update user same api url, it will update the vote automatically    
    """
    try:
        user_ip = get_ip()

        vote = User_Vote(phrase_id=phrase_id, meaning_id=meaning_id, ip= user_ip, like=like)

        result = User_Vote.create(vote)

        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/phrases/{phrase_id}/meanings/{meaning_id}/vote", response_model=ResponseModel)
def delete_vote(vote_id: str) -> ResponseModel:
    """
    Delete a vote for a meaning.
    """
    try:
        result = User_Vote.delete(vote_id)

        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))