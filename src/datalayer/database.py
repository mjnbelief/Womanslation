from pymongo import MongoClient
import os
import time

def wait_for_db():
    """
    Wait for the MongoDB database to be ready.
    This function attempts to connect to the database multiple times
    until it is available or the maximum number of attempts is reached.
    """
    
    host = os.getenv("DB_HOST", "mongodb://localhost:27017/")
    max_attempts = 30
    attempt = 1

    while attempt <= max_attempts:
        try:
            print("Database is ready!")
            return MongoClient(host)
        
        except Exception as e:
            print(f"Waiting for database... Attempt {attempt}/{max_attempts}")
            time.sleep(1)
            attempt += 1
            
    raise Exception("Database not ready after maximum attempts.")

client = wait_for_db()
dbname = os.getenv("DB_NAME", "womanslation_db")


def get_db():
    """
    Connect to the MongoDB database and return the database object.
    """
    db = client[dbname]

    return db


# def insert_data_from_json():
#     """
#     Insert data from a JSON file into the specified MongoDB collection.
#     """
#     db = get_db()
#     json_file_path = r"././json.json"
#     collection_name = "phrases"
    
#     # Convert the DataFrame to a list of dictionaries
#     with open(json_file_path, "r") as file:
#         data = pd.read_json(file, orient="index")

#     a = data.to_dict(orient="records")  
    
#     # Insert the data into the specified collection
#     collection = db[collection_name]
#     result = collection.insert_many(a)

#     print(f"Inserted {len(result.inserted_ids)} records into {collection_name} collection.")


# insert_data_from_json()