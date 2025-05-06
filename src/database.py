from pymongo import MongoClient

def get_db():
    """
    Connect to the MongoDB database and return the database object.
    """
        
    client = MongoClient("mongodb+srv://admin:W0manslation_27@mj.c0pgxlq.mongodb.net/")
    db = client["womanslation_db"]

    return db