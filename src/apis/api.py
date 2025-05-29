from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from datalayer import ResponseModel, SortEnum, get_ip, set_request_context, my_logger, insert_data_from_json
from Models import Meaning, Phrase, User_Vote

app = FastAPI()

#Allowing Site for API submission.
origins = [
    "https://womanslation.lovable.app"
]

#Allowing API submission from the entered site.
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

#Inserting default data into the database when launching the application
@app.on_event("startup")
def on_startup():
   insert_data_from_json()

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Womanslation."}

@app.get("/phrases", response_model=ResponseModel)
def get_phrases(page_number: int = 0, page_size: int = 10, pageOrder: SortEnum = SortEnum.newest, search_text: str = "", tags: str = "") -> ResponseModel:
    """
    Get a list of phrases with pagination and filtering options.
    
    Parameters:
        - page_number (int): The page number to retrieve (default is 0).
        - page_size (int): The number of phrases per page (default is 10).
        - pageOrder (SortEnum): The order in which to sort the phrases (default is SortEnum.newest).
        - search_text (str): Text to search for in phrases (default is empty string).
        - tags (str): Comma-separated tags to filter phrases by (default is empty string).

    Raises:
        HTTPException: If an error occurs during the retrieval of phrases.
    
    Returns:
        ResponseModel: The response model containing the list of phrases.
    """
    try:
        result = Phrase.get_phrases(pageIndex=page_number, pageSize=page_size, pageOrder=pageOrder, searchText=search_text, tags=tags)

        return result
    
    except Exception as e:
        my_logger.error(f"Error retrieving phrases: {e}")
        raise HTTPException(status_code=500, detail=str(e))
   
    
@app.post("/phrases", response_model=ResponseModel)
def create_phrase(phrase: Phrase) -> ResponseModel:
    """
    Create a new phrase.

    Args:
        phrase (Phrase): The phrase object to be created.
        
    Raises:
        HTTPException: If an error occurs during the creation of the phrase.

    Returns:
        ResponseModel: The response model containing the created phrase.
    """
    try:
        result = Phrase.create(phrase)
        
        return result

    except Exception as e:
        my_logger.error(f"Error creating phrase: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/phrases/{phrase_id}/view", response_model=ResponseModel)
def view_phrase(phrase_id: str) -> ResponseModel:
    """
    Mark a phrase as viewed.

    Parameters:
        phrase_id (str): The ID of the phrase to mark as viewed.

    Raises:
        HTTPException: If an error occurs during the marking of the phrase as viewed.

    Returns:
        ResponseModel: The response model containing the updated phrase.
    """
    try:
        result = Phrase.Phrase_viewed(phrase_id)
        return result

    except Exception as e:
        my_logger.error(f"Error viewing phrase {phrase_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/phrases/{phrase_id}", response_model=ResponseModel)
def update_phrase(phrase_id: str, phrase: Phrase) -> ResponseModel:
    """ 
    Update an existing phrase.
    Parameters:
        phrase_id (str): The ID of the phrase to be updated.
        
    Args:
        phrase (Phrase): The updated phrase object.
        
    Raises:
        HTTPException: If an error occurs during the update of the phrase.
        
    Returns:
        ResponseModel: The response model containing the updated phrase.
    """
    try:
        result = Phrase.update(phrase, phrase_id)
        
        return result

    except Exception as e:
        my_logger.error(f"Error updating phrase {phrase_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/phrases/{phrase_id}", response_model=ResponseModel)
def delete_phrase(phrase_id: str) -> ResponseModel:
    """
    Delete a phrase by its ID.
    Parameters:
        phrase_id (str): The ID of the phrase to be deleted.
        
    Raises:
        HTTPException: If an error occurs during the deletion of the phrase.
        
    Returns:
        ResponseModel: The response model indicating the success or failure of the deletion.
    """
    try:
        result = Phrase.delete(phrase_id)
        
        if not result.success:
            return result
        
        # delete all likes also
        User_Vote.delete_by_phrase_id(phrase_id)
        
        return result

    except Exception as e:
        my_logger.error(f"Error deleting phrase {phrase_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phrases/{phrase_id}/meanings", response_model=ResponseModel)
def get_meanings_by_phrase_id(phrase_id: str) -> ResponseModel:
    """
    Get meanings for a specific phrase by its ID.
    
    Parameters:
        phrase_id (str): The ID of the phrase for which to retrieve meanings.
        
    Raises:
        HTTPException: If an error occurs during the retrieval of meanings.
    """
    try:
        result = Meaning.get_meanings_by_phrase_id(phrase_id)
        
        return result
    
    except Exception as e:
        my_logger.error(f"Error retrieving meanings for phrase {phrase_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/phrases/{phrase_id}/meanings", response_model=ResponseModel)
def create_meaning(phrase_id: str, meaning: Meaning) -> ResponseModel:
    """
    Create a new meaning for a specific phrase.
    
    Parameters:
        phrase_id (str): The ID of the phrase for which to create the meaning.
        
    Args:
        meaning (Meaning): The meaning object to be created.

    Raises:
        HTTPException: If an error occurs during the creation of the meaning.
    """
    try:
        result = Meaning.create(meaning, phrase_id)
        
        return result
    
    except Exception as e:
        my_logger.error(f"Error adding meaning {meaning} for phrase {phrase_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.put("/phrases/{phrase_id}/meanings/{meaning_id}", response_model=ResponseModel)
def update_meaning(phrase_id: str, meaning_id: str, meaning: Meaning) -> ResponseModel:
    """
    Update an existing meaning for a specific phrase.
    
    Parameters:
        phrase_id (str): The ID of the phrase for which to update the meaning.
        meaning_id (str): The ID of the meaning to be updated.
        
    Args:
        meaning (Meaning): The updated meaning object.
        
    Raises:
        HTTPException: If an error occurs during the update of the meaning.
        
    returns:
        ResponseModel: The response model containing the updated meaning.
    """
    try:
        result = Meaning.update(meaning, phrase_id, meaning_id)
        
        return result
    
    except Exception as e:
        my_logger.error(f"Error updating meaning {meaning_id} for phrase {phrase_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.delete("/phrases/{phrase_id}/meanings/{meaning_id}", response_model=ResponseModel)
def delete_meaning(phrase_id: str, meaning_id: str) -> ResponseModel:
    """
    Parameters:
        phrase_id (str): The ID of the phrase for which to delete the meaning.
        meaning_id (str): The ID of the meaning to be delete.

    Raises:
        HTTPException: If an error occurs during the delete of the meaning.
        
    Returns:
        ResponseModel: The response model indicating the success or failure of the deletion.
    """
    try:
        result = Meaning.delete(phrase_id, meaning_id)
        
        if not result.success:
            return result
        
        # delete all likes also
        User_Vote.delete_by_meaning_id(meaning_id)
        
        return result
    
    except Exception as e:
        my_logger.error(f"Error deleting meaning {meaning_id} for phrase {phrase_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/phrases/{phrase_id}/meanings", response_model=ResponseModel)
def delete_meanings_by_phrase_id(phrase_id: str) -> ResponseModel:
    """
    Parameters:
        phrase_id (str): The ID of the phrase for which to delete the meanings.

    Raises:
        HTTPException: If an error occurs during the delete of the meanings.
        
    Returns:
        ResponseModel: The response model indicating the success or failure of the deletion.
    """
    try:
        result = Meaning.delete_meanings_by_phrase_id(phrase_id)
        
        if not result.success:
            return result

        # delete all likes also
        User_Vote.delete_by_phrase_id(phrase_id)

        return result
    
    except Exception as e:
        my_logger.error(f"Error deleting meanings for phrase {phrase_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


#custom user vote api
@app.post("/phrases/{phrase_id}/meanings/{meaning_id}/vote", response_model=ResponseModel)
def create_vote(phrase_id: str, meaning_id: str, like: bool, request: Request) -> ResponseModel:
    """
    like or unlike a meaning.
    when user votes again, it will update the vote automatically
    
    Parameters:
        phrase_id (str): The ID of the phrase.
        meaning_id (str): The ID of the meaning which to like.
        like (bool): for like True, for unlike False 

    Raises:
        HTTPException: If an error occurs during the like.
        
    Returns:
        ResponseModel: The response model containing the liked of unliked User_Vote.
    """
    try:
        user_ip = get_ip()

        vote = User_Vote(phrase_id=phrase_id, meaning_id=meaning_id, ip= user_ip, like=like)

        result = User_Vote.create(vote)

        return result
    
    except Exception as e:
        my_logger.error(f"Error creating vote for phrase {phrase_id} and meaning {meaning_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/user_vote/current_user", response_model=ResponseModel)
def get_current_user_vote() -> ResponseModel:
    """
    Get all current user's votes.
    
    Raises:
        HTTPException: If an error occurs during the getting current user's votes.
        
    Returns:
        ResponseModel: The response model containing list of liked User_Vote.
    """
    try:
        user_ip = get_ip()
        result = User_Vote.get_by_ip(user_ip)

        return result

    except Exception as e:
        my_logger.error(f"Error creating user vote: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/user_vote/{vote_id}", response_model=ResponseModel)
def delete_user_vote(vote_id: str) -> ResponseModel:
    
    """
    like or unlike a meaning.
    when user votes again, it will update the vote automatically
    
    Parameters:
        vote_id (str): The ID of the User_vote.

    Raises:
        HTTPException: If an error occurs during the delete of User_vote.

    Returns:
        ResponseModel: The response model indicating the success or failure of the deletion.
    """
    try:
        result = User_Vote.delete(vote_id)

        return result
    
    except Exception as e:
        my_logger.error(f"Error deleting user vote {vote_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))